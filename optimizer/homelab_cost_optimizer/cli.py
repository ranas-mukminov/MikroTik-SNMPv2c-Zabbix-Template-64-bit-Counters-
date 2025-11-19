from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

import typer

from .collectors.docker_collector import DockerCollector
from .collectors.k8s_collector import KubernetesCollector
from .collectors.libvirt_collector import LibvirtCollector
from .collectors.proxmox_collector import ProxmoxCollector
from .collectors.base import build_snapshot
from .config import load_yaml
from .consolidators.heuristic_consolidator import HeuristicConsolidator
from .estimators.cost_estimator import CostEstimator
from .estimators.power_estimator import PowerEstimator
from .reporters import ai_reporter, markdown_reporter

app = typer.Typer(help="Homelab cost optimizer CLI")


@app.command()
def collect(
    source: str = typer.Option(..., help="Data source", case_sensitive=False),
    out: Path = typer.Option(..., help="Path to write inventory JSON"),
    mock_data: Path = typer.Option(None, help="Optional JSON fixture to use instead of API calls"),
) -> None:
    out = Path(out)
    dataset = _load_mock(mock_data) if mock_data else None
    collector = _collector_factory(source.lower(), dataset)
    snapshot = collector.collect()
    out.write_text(json.dumps(asdict(snapshot), indent=2), encoding="utf-8")
    typer.echo(f"Wrote inventory to {out}")


@app.command()
def analyze(
    inventory: Path = typer.Option(..., help="Path to inventory JSON"),
    electricity: Path = typer.Option(..., help="Electricity config YAML"),
    out: Path = typer.Option(..., help="Markdown report path"),
) -> None:
    out = Path(out)
    snapshot = _load_snapshot(inventory)
    power = PowerEstimator().estimate(snapshot)
    cfg = load_yaml(electricity)
    cost = CostEstimator(price_per_kwh=cfg.get("price_per_kwh", 0.2), currency=cfg.get("currency", "USD")).estimate(power)
    report = markdown_reporter.render_markdown(power, cost)
    out.write_text(report, encoding="utf-8")
    typer.echo(f"Report saved to {out}")


@app.command()
def suggest(
    inventory: Path = typer.Option(..., help="Inventory JSON"),
    electricity: Path = typer.Option(..., help="Electricity config"),
    scenario: str = typer.Option("consolidate-low-util", help="Scenario name"),
    out: Path = typer.Option(..., help="Output Markdown"),
    ai_report: bool = typer.Option(False, help="Include AI narrative"),
) -> None:
    out = Path(out)
    snapshot = _load_snapshot(inventory)
    consolidator = HeuristicConsolidator()
    plan = consolidator.consolidate(snapshot)
    power = PowerEstimator().estimate(snapshot)
    cfg = load_yaml(electricity)
    cost = CostEstimator(price_per_kwh=cfg.get("price_per_kwh", 0.2), currency=cfg.get("currency", "USD")).estimate(power)
    report = markdown_reporter.render_markdown(power, cost, plan.assignments)
    if ai_report:
        ai_summary = ai_reporter.render_ai_report(power, cost, scenario, plan.estimated_idle_watt_reduction)
        report = f"{report}\n\n---\n\n### AI summary\n\n{ai_summary}\n"
    out.write_text(report, encoding="utf-8")
    typer.echo(f"Suggestion report saved to {out}")


def _collector_factory(source: str, dataset: Dict[str, Any] | None):
    if source == "proxmox":
        return ProxmoxCollector(dataset)
    if source == "libvirt":
        return LibvirtCollector(dataset)
    if source == "docker":
        return DockerCollector(dataset)
    if source in {"k8s", "kubernetes"}:
        return KubernetesCollector(dataset)
    raise typer.BadParameter(f"Unknown source: {source}")


def _load_mock(path: Path | str) -> Dict[str, Any]:
    file_path = Path(path)
    return json.loads(file_path.read_text(encoding="utf-8"))


def _load_snapshot(path: Path | str):
    file_path = Path(path)
    data = json.loads(file_path.read_text(encoding="utf-8"))
    return build_snapshot(data)


def main() -> None:
    app()


if __name__ == "__main__":
    main()

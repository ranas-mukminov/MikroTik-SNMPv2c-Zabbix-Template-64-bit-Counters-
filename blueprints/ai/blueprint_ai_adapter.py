from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from ai_providers.base import AIProvider
from ai_providers.mock_provider import MockProvider


@dataclass
class HardwareNode:
    name: str
    cpu_cores: int
    memory_gb: int
    storage_tb: float


@dataclass
class BlueprintSuggestion:
    topology: str
    summary: str
    ai_notes: Optional[str] = None


def _default_provider() -> AIProvider:
    return MockProvider()


def suggest_blueprint(
    topology: str,
    nodes: Iterable[HardwareNode],
    constraints: Optional[Dict[str, Any]] = None,
    provider: Optional[AIProvider] = None,
) -> BlueprintSuggestion:
    """Return a suggestion for a blueprint configuration."""

    provider = provider or _default_provider()
    constraints = constraints or {}

    node_data = [node.__dict__ for node in nodes]
    baseline_summary = _describe_baseline(topology, node_data, constraints)

    ai_payload = {
        "topology": topology,
        "nodes": node_data,
        "constraints": constraints,
    }
    ai_notes = provider.generate_blueprint_suggestions(ai_payload)

    return BlueprintSuggestion(topology=topology, summary=baseline_summary, ai_notes=ai_notes)


def _describe_baseline(topology: str, nodes: List[Dict[str, Any]], constraints: Dict[str, Any]) -> str:
    node_count = len(nodes)
    cpu_total = sum(node["cpu_cores"] for node in nodes)
    ram_total = sum(node["memory_gb"] for node in nodes)
    storage_total = sum(node["storage_tb"] for node in nodes)
    constraint_summary = ", ".join(f"{k}={v}" for k, v in constraints.items()) or "no additional constraints"
    return (
        f"Baseline for {topology}: {node_count} nodes, {cpu_total} cores, "
        f"{ram_total} GB RAM, {storage_total:.1f} TB storage; {constraint_summary}."
    )

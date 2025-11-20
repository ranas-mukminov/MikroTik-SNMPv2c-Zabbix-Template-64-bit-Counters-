import json
from pathlib import Path

from homelab_cost_optimizer.cli import app

from typer.testing import CliRunner

runner = CliRunner()


def test_full_workflow(tmp_path: Path):
    inventory_path = tmp_path / "inventory.json"
    inventory_path.write_text(
        json.dumps(
            {
                "nodes": [
                    {"name": "n1", "kind": "hypervisor", "cpu_cores": 8, "memory_gb": 32},
                    {"name": "n2", "kind": "hypervisor", "cpu_cores": 8, "memory_gb": 32},
                ],
                "workloads": [
                    {
                        "name": "vm1",
                        "workload_type": "vm",
                        "cpu_cores": 2,
                        "memory_gb": 4,
                        "utilization": 0.3,
                        "node_name": "n1",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    electricity = tmp_path / "electricity.yaml"
    electricity.write_text("price_per_kwh: 0.2\ncurrency: USD\n", encoding="utf-8")

    analyze_out = tmp_path / "report.md"
    result = runner.invoke(
        app,
        [
            "analyze",
            "--inventory",
            str(inventory_path),
            "--electricity",
            str(electricity),
            "--out",
            str(analyze_out),
        ],
    )
    assert result.exit_code == 0
    assert analyze_out.exists()

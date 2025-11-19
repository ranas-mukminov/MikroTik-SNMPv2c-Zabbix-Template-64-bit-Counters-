import json
from pathlib import Path

from typer.testing import CliRunner

from homelab_cost_optimizer.cli import app


runner = CliRunner()


def test_collect_with_mock(tmp_path: Path):
    mock_data = tmp_path / "mock.json"
    mock_data.write_text(
        json.dumps({"nodes": [{"name": "n1", "kind": "proxmox", "cpu_cores": 4, "memory_gb": 8}], "workloads": []}),
        encoding="utf-8",
    )
    out = tmp_path / "inventory.json"
    result = runner.invoke(app, ["collect", "--source", "proxmox", "--out", str(out), "--mock-data", str(mock_data)])
    assert result.exit_code == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["nodes"][0]["name"] == "n1"

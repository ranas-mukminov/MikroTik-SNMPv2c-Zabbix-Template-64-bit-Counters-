from __future__ import annotations

from typing import Any, Dict, Optional

from .base import build_snapshot
from ..models import InventorySnapshot


class DockerCollector:
    def __init__(self, dataset: Optional[Dict[str, Any]] = None) -> None:
        self.dataset = dataset

    def collect(self) -> InventorySnapshot:
        data = self.dataset or _simulate_dataset()
        return build_snapshot(data)


def _simulate_dataset() -> Dict[str, Any]:
    return {
        "metadata": {"source": "docker", "note": "simulated"},
        "nodes": [
            {
                "name": "docker-host",
                "kind": "docker",
                "cpu_cores": 8,
                "memory_gb": 32,
                "power_profile": {"base_idle_watts": 70},
            }
        ],
        "workloads": [
            {
                "name": "web",
                "workload_type": "container",
                "cpu_cores": 1,
                "memory_gb": 0.5,
                "utilization": 0.5,
                "node_name": "docker-host",
            },
            {
                "name": "worker",
                "workload_type": "container",
                "cpu_cores": 2,
                "memory_gb": 1,
                "utilization": 0.4,
                "node_name": "docker-host",
            },
        ],
    }

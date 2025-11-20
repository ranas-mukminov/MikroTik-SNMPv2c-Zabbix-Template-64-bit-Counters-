from __future__ import annotations

from typing import Any

from ..models import InventorySnapshot
from .base import build_snapshot


class KubernetesCollector:
    def __init__(self, dataset: dict[str, Any] | None = None) -> None:
        self.dataset = dataset

    def collect(self) -> InventorySnapshot:
        data = self.dataset or _simulate_dataset()
        return build_snapshot(data)


def _simulate_dataset() -> dict[str, Any]:
    return {
        "metadata": {"source": "kubernetes", "note": "simulated"},
        "nodes": [
            {"name": "k3s-master", "kind": "k8s", "cpu_cores": 4, "memory_gb": 16},
            {"name": "k3s-agent-1", "kind": "k8s", "cpu_cores": 4, "memory_gb": 16},
        ],
        "workloads": [
            {
                "name": "api",
                "workload_type": "pod",
                "cpu_cores": 1,
                "memory_gb": 1,
                "utilization": 0.6,
                "node_name": "k3s-master",
            },
            {
                "name": "runner",
                "workload_type": "pod",
                "cpu_cores": 0.5,
                "memory_gb": 0.5,
                "utilization": 0.4,
                "node_name": "k3s-agent-1",
            },
        ],
    }

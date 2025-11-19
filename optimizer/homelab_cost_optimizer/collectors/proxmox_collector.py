from __future__ import annotations

from typing import Any, Dict, Optional

from .base import build_snapshot
from ..models import InventorySnapshot


class ProxmoxCollector:
    """Collector that normalizes Proxmox API responses into the common snapshot model."""

    def __init__(self, dataset: Optional[Dict[str, Any]] = None) -> None:
        self.dataset = dataset

    def collect(self) -> InventorySnapshot:
        data = self.dataset or _simulate_dataset()
        return build_snapshot(data)


def _simulate_dataset() -> Dict[str, Any]:
    return {
        "metadata": {"source": "proxmox", "note": "simulated"},
        "nodes": [
            {
                "name": "pve-1",
                "kind": "proxmox",
                "cpu_cores": 16,
                "memory_gb": 64,
                "power_profile": {
                    "base_idle_watts": 85,
                    "watts_per_cpu_core": 9,
                    "watts_per_gb_ram": 0.4,
                },
            }
        ],
        "workloads": [
            {
                "name": "router",
                "workload_type": "vm",
                "cpu_cores": 2,
                "memory_gb": 2,
                "utilization": 0.2,
                "node_name": "pve-1",
            }
        ],
    }

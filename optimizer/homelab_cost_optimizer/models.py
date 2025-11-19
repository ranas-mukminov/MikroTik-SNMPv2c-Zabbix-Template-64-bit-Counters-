from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PowerProfile:
    base_idle_watts: float = 60.0
    watts_per_cpu_core: float = 8.0
    watts_per_gb_ram: float = 0.5


@dataclass
class Node:
    name: str
    kind: str
    cpu_cores: int
    memory_gb: int
    power_profile: PowerProfile = field(default_factory=PowerProfile)
    metadata: Dict[str, str] = field(default_factory=dict)

    def capacity(self) -> Dict[str, int]:
        return {"cpu_cores": self.cpu_cores, "memory_gb": self.memory_gb}


@dataclass
class Workload:
    name: str
    workload_type: str
    cpu_cores: float
    memory_gb: float
    utilization: float
    node_name: str
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class InventorySnapshot:
    nodes: List[Node]
    workloads: List[Workload]
    metadata: Dict[str, str] = field(default_factory=dict)

    def node_by_name(self, name: str) -> Optional[Node]:
        for node in self.nodes:
            if node.name == name:
                return node
        return None

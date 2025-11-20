from __future__ import annotations

from dataclasses import dataclass, field


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
    metadata: dict[str, str] = field(default_factory=dict)

    def capacity(self) -> dict[str, int]:
        return {"cpu_cores": self.cpu_cores, "memory_gb": self.memory_gb}


@dataclass
class Workload:
    name: str
    workload_type: str
    cpu_cores: float
    memory_gb: float
    utilization: float
    node_name: str
    labels: dict[str, str] = field(default_factory=dict)


@dataclass
class InventorySnapshot:
    nodes: list[Node]
    workloads: list[Workload]
    metadata: dict[str, str] = field(default_factory=dict)

    def node_by_name(self, name: str) -> Node | None:
        for node in self.nodes:
            if node.name == name:
                return node
        return None

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..models import InventorySnapshot, Node, Workload


@dataclass
class ConsolidationPlan:
    assignments: Dict[str, str]
    nodes_to_power_down: List[str]
    estimated_idle_watt_reduction: float


class HeuristicConsolidator:
    def __init__(self, headroom: float = 0.8) -> None:
        self.headroom = headroom

    def consolidate(self, snapshot: InventorySnapshot) -> ConsolidationPlan:
        nodes = sorted(snapshot.nodes, key=lambda n: n.cpu_cores, reverse=True)
        usage = {node.name: {"cpu": 0.0, "ram": 0.0, "workloads": []} for node in nodes}
        assignments: Dict[str, str] = {}

        workloads = sorted(snapshot.workloads, key=lambda w: w.utilization)
        for workload in workloads:
            target = self._find_target_node(workload, nodes, usage)
            if not target:
                continue
            assignments[workload.name] = target.name
            usage[target.name]["cpu"] += workload.cpu_cores
            usage[target.name]["ram"] += workload.memory_gb
            usage[target.name]["workloads"].append(workload.name)

        nodes_to_power_down = [
            node.name for node in nodes if not usage[node.name]["workloads"]
        ]
        estimated_savings = sum(node.power_profile.base_idle_watts for node in nodes if node.name in nodes_to_power_down)

        return ConsolidationPlan(
            assignments=assignments,
            nodes_to_power_down=nodes_to_power_down,
            estimated_idle_watt_reduction=round(estimated_savings, 2),
        )

    def _find_target_node(self, workload: Workload, nodes: List[Node], usage: Dict[str, Dict[str, float]]) -> Node | None:
        for node in nodes:
            node_usage = usage[node.name]
            if self._fits(workload, node, node_usage):
                return node
        return None

    def _fits(self, workload: Workload, node: Node, node_usage: Dict[str, float]) -> bool:
        max_cpu = node.cpu_cores * self.headroom
        max_ram = node.memory_gb * self.headroom
        return (
            node_usage["cpu"] + workload.cpu_cores <= max_cpu
            and node_usage["ram"] + workload.memory_gb <= max_ram
        )

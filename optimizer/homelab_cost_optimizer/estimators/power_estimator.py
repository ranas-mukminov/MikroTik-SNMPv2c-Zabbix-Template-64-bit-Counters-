from __future__ import annotations

from ..models import InventorySnapshot, Node, Workload


class PowerEstimator:
    def estimate(self, snapshot: InventorySnapshot) -> dict[str, float]:
        per_node: dict[str, float] = {}
        for node in snapshot.nodes:
            workloads = [w for w in snapshot.workloads if w.node_name == node.name]
            per_node[node.name] = self._estimate_node(node, workloads)
        total = sum(per_node.values())
        per_node["total_watts"] = total
        return per_node

    def _estimate_node(self, node: Node, workloads: list[Workload]) -> float:
        profile = node.power_profile
        cpu_dynamic = sum(w.cpu_cores * max(w.utilization, 0) for w in workloads)
        ram_dynamic = sum(w.memory_gb * max(w.utilization, 0) for w in workloads)
        watts = profile.base_idle_watts
        watts += cpu_dynamic * profile.watts_per_cpu_core
        watts += ram_dynamic * profile.watts_per_gb_ram
        return round(watts, 2)

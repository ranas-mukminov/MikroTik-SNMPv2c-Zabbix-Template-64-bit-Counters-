from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ..models import InventorySnapshot, Node, PowerProfile, Workload


def build_snapshot(dataset: Dict[str, Any]) -> InventorySnapshot:
    nodes = [_node_from_dict(raw) for raw in dataset.get("nodes", [])]
    workloads = [_workload_from_dict(raw) for raw in dataset.get("workloads", [])]
    metadata = dataset.get("metadata", {})
    return InventorySnapshot(nodes=nodes, workloads=workloads, metadata=metadata)


def _node_from_dict(data: Dict[str, Any]) -> Node:
    profile_data = data.get("power_profile", {})
    profile = PowerProfile(**profile_data) if profile_data else PowerProfile()
    return Node(
        name=data["name"],
        kind=data.get("kind", "unknown"),
        cpu_cores=int(data.get("cpu_cores", 0)),
        memory_gb=int(data.get("memory_gb", 0)),
        power_profile=profile,
        metadata=data.get("metadata", {}),
    )


def _workload_from_dict(data: Dict[str, Any]) -> Workload:
    return Workload(
        name=data["name"],
        workload_type=data.get("workload_type", "vm"),
        cpu_cores=float(data.get("cpu_cores", 0)),
        memory_gb=float(data.get("memory_gb", 0)),
        utilization=float(data.get("utilization", 0)),
        node_name=data.get("node_name", "unknown"),
        labels=data.get("labels", {}),
    )

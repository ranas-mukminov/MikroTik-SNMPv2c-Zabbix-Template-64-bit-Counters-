#!/usr/bin/env bash
set -euo pipefail

python <<'PY'
from homelab_cost_optimizer.models import InventorySnapshot, Node, Workload
from homelab_cost_optimizer.estimators.power_estimator import PowerEstimator
from homelab_cost_optimizer.consolidators.heuristic_consolidator import HeuristicConsolidator

nodes = [Node(name=f"node-{i}", kind="hypervisor", cpu_cores=32, memory_gb=128) for i in range(10)]
workloads = [
    Workload(
        name=f"vm-{i}",
        workload_type="vm",
        cpu_cores=2,
        memory_gb=4,
        utilization=0.3,
        node_name=nodes[i % len(nodes)].name,
    )
    for i in range(200)
]

snapshot = InventorySnapshot(nodes=nodes, workloads=workloads)
power = PowerEstimator().estimate(snapshot)
plan = HeuristicConsolidator().consolidate(snapshot)
print(f"Total watts: {power['total_watts']}, idle savings estimate: {plan.estimated_idle_watt_reduction}")
PY

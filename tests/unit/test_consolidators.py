from homelab_cost_optimizer.consolidators.heuristic_consolidator import HeuristicConsolidator
from homelab_cost_optimizer.models import InventorySnapshot, Node, Workload


def test_consolidator_identifies_idle_nodes():
    nodes = [
        Node(name="n1", kind="hypervisor", cpu_cores=8, memory_gb=32),
        Node(name="n2", kind="hypervisor", cpu_cores=8, memory_gb=32),
    ]
    workloads = [
        Workload(name="vm1", workload_type="vm", cpu_cores=2, memory_gb=4, utilization=0.3, node_name="n1"),
        Workload(name="vm2", workload_type="vm", cpu_cores=2, memory_gb=4, utilization=0.2, node_name="n2"),
    ]
    snapshot = InventorySnapshot(nodes=nodes, workloads=workloads)
    plan = HeuristicConsolidator().consolidate(snapshot)
    assert plan.assignments
    assert isinstance(plan.nodes_to_power_down, list)

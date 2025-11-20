from homelab_cost_optimizer.estimators.cost_estimator import CostEstimator
from homelab_cost_optimizer.estimators.power_estimator import PowerEstimator
from homelab_cost_optimizer.models import InventorySnapshot, Node, PowerProfile, Workload


def build_snapshot() -> InventorySnapshot:
    node = Node(
        name="n1",
        kind="proxmox",
        cpu_cores=8,
        memory_gb=32,
        power_profile=PowerProfile(base_idle_watts=80),
    )
    workload = Workload(
        name="vm", workload_type="vm", cpu_cores=2, memory_gb=4, utilization=0.5, node_name="n1"
    )
    return InventorySnapshot(nodes=[node], workloads=[workload])


def test_power_estimator_sums_values():
    snapshot = build_snapshot()
    power = PowerEstimator().estimate(snapshot)
    assert "n1" in power
    assert power["total_watts"] >= power["n1"]


def test_cost_estimator_uses_price():
    power = {"n1": 100.0}
    cost = CostEstimator(price_per_kwh=0.25, currency="EUR", hours_per_month=720).estimate(power)
    assert cost["n1"]["monthly_cost"] == 18.0
    assert cost["n1"]["currency"] == "EUR"

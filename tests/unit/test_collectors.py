from homelab_cost_optimizer.collectors.proxmox_collector import ProxmoxCollector
from homelab_cost_optimizer.collectors.docker_collector import DockerCollector


def test_proxmox_collector_returns_snapshot():
    collector = ProxmoxCollector(
        dataset={
            "nodes": [{"name": "n1", "kind": "proxmox", "cpu_cores": 8, "memory_gb": 32}],
            "workloads": [
                {
                    "name": "vm1",
                    "workload_type": "vm",
                    "cpu_cores": 2,
                    "memory_gb": 4,
                    "utilization": 0.5,
                    "node_name": "n1",
                }
            ],
        }
    )
    snapshot = collector.collect()
    assert snapshot.nodes[0].name == "n1"
    assert snapshot.workloads[0].name == "vm1"


def test_docker_collector_simulation_has_containers():
    collector = DockerCollector()
    snapshot = collector.collect()
    assert snapshot.workloads, "Expected simulated docker workloads"

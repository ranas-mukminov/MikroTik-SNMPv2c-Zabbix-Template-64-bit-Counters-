from ai_providers.mock_provider import MockProvider
from blueprints.ai.blueprint_ai_adapter import HardwareNode, suggest_blueprint


def test_blueprint_ai_adapter_returns_summary():
    nodes = [HardwareNode(name="node1", cpu_cores=8, memory_gb=32, storage_tb=1.5)]
    suggestion = suggest_blueprint(
        "proxmox-homelab", nodes, {"vlan_count": 3}, provider=MockProvider()
    )
    assert "Baseline" in suggestion.summary
    assert "proxmox-homelab" in suggestion.summary
    assert "Mock suggestion" in suggestion.ai_notes

from __future__ import annotations

from typing import Any, Dict

from .base import AIProvider


class MockProvider(AIProvider):
    """Deterministic provider for tests and offline use."""

    def generate_blueprint_suggestions(self, payload: Dict[str, Any]) -> str:
        topology = payload.get("topology", "unknown")
        nodes = payload.get("nodes", [])
        node_count = len(nodes)
        return (
            f"Mock suggestion for {topology}: plan around {node_count} nodes, "
            "allocate storage tiers explicitly, and prefer VLAN-tagged networks."
        )

    def generate_cost_optimization_report(self, payload: Dict[str, Any]) -> str:
        savings = payload.get("savings", 0)
        scenario = payload.get("scenario", "baseline")
        return (
            f"Scenario '{scenario}' could save approximately {savings:.2f} currency units per month. "
            "Review workload affinity before executing the plan."
        )

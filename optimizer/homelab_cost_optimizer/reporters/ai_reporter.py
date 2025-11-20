from __future__ import annotations

from ai_providers.base import AIProvider
from ai_providers.mock_provider import MockProvider


def render_ai_report(
    power: dict[str, float],
    cost: dict[str, dict[str, float]],
    scenario: str,
    savings: float,
    provider: AIProvider | None = None,
) -> str:
    provider = provider or MockProvider()
    payload = {
        "scenario": scenario,
        "power": power,
        "cost": cost,
        "savings": savings,
    }
    return provider.generate_cost_optimization_report(payload)

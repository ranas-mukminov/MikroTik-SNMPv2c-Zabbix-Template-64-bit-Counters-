from __future__ import annotations


class CostEstimator:
    def __init__(
        self, price_per_kwh: float, currency: str = "USD", hours_per_month: int = 730
    ) -> None:
        self.price_per_kwh = price_per_kwh
        self.currency = currency
        self.hours_per_month = hours_per_month

    def estimate(self, power_by_node: dict[str, float]) -> dict[str, dict[str, float]]:
        result: dict[str, dict[str, float]] = {}
        for node, watts in power_by_node.items():
            if node == "total_watts":
                continue
            kwh = (watts * self.hours_per_month) / 1000
            cost = kwh * self.price_per_kwh
            result[node] = {
                "kwh": round(kwh, 2),
                "monthly_cost": round(cost, 2),
                "currency": self.currency,
            }
        total_cost = sum(entry["monthly_cost"] for entry in result.values())
        result["total"] = {"monthly_cost": round(total_cost, 2), "currency": self.currency}
        return result

from __future__ import annotations


def render_text(power: dict[str, float], cost: dict[str, dict[str, float]]) -> str:
    lines = ["Homelab cost optimizer report", "==============================", ""]
    lines.append("Power consumption (watts):")
    for node, watts in power.items():
        lines.append(f"- {node}: {watts}W")
    lines.append("")
    lines.append("Monthly cost estimates:")
    for node, data in cost.items():
        amount = data.get("monthly_cost")
        currency = data.get("currency")
        if amount is None:
            continue
        lines.append(f"- {node}: {amount} {currency}")
    return "\n".join(lines)

from __future__ import annotations


def render_markdown(
    power: dict[str, float], cost: dict[str, dict[str, float]], plan: dict[str, str] | None = None
) -> str:
    md = [
        "# Homelab cost optimizer report",
        "",
        "## Power consumption",
        "",
        "| Node | Watts |",
        "| --- | ---: |",
    ]
    for node, watts in power.items():
        md.append(f"| {node} | {watts} |")
    md.extend(["", "## Monthly cost", "", "| Node | Cost | Currency |", "| --- | ---: | --- |"])
    for node, data in cost.items():
        if "monthly_cost" not in data:
            continue
        md.append(f"| {node} | {data['monthly_cost']} | {data.get('currency', '?')} |")
    if plan:
        md.extend(["", "## Consolidation plan", "", "| Workload | Target node |", "| --- | --- |"])
        for workload, target in plan.items():
            md.append(f"| {workload} | {target} |")
    return "\n".join(md)

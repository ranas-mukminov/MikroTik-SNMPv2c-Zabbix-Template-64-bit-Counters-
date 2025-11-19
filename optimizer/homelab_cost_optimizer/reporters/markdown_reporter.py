from __future__ import annotations

from typing import Dict


def render_markdown(power: Dict[str, float], cost: Dict[str, Dict[str, float]], plan: Dict[str, str] | None = None) -> str:
    md = ["# Homelab cost optimizer report", "", "## Power consumption", "", "| Node | Watts |", "| --- | ---: |"]
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

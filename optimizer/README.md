# homelab-cost-optimizer package

The optimizer is a Python package powering the CLI described in the repository README. It is structured as follows:

```
homelab_cost_optimizer/
  models.py                  # Data classes for nodes, workloads, power profiles
  collectors/                # Pluggable collectors (Proxmox, libvirt, Docker, Kubernetes)
  estimators/                # Power & cost estimators
  consolidators/             # Heuristic consolidation planner
  reporters/                 # Text, Markdown, and AI reporters
  cli.py                     # Typer-based CLI entrypoint
  config.py                  # Helpers for YAML configs and defaults
```

Install locally:

```bash
pip install -e optimizer/
```

Run the CLI:

```bash
homelab-cost-optimizer --help
```

Developers should add unit tests for new modules under `tests/` and extend the documentation when adding scenarios or data sources.

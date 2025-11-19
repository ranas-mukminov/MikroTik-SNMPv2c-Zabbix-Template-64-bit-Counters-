# homelab-blueprints-run-as-daemon

This catalog offers reproducible IaC starting points for typical homelab and SMB environments. Every blueprint is intended to be modified before production deployment. The tree mirrors the main repository structure:

```
blueprints/
  docs/                      # Topology write-ups and diagrams
  terraform/                 # Base infrastructure per topology
  ansible/                   # Configuration management for services
  k3d/                       # Lightweight cluster definitions for local dev
  ai/                        # Optional AI helper to suggest variable sets
```

## Usage workflow

1. Review `docs/topology-overview.md` to select an appropriate baseline.
2. Copy the Terraform directory you need, adjust `variables.tf`, and initialize Terraform with a remote backend (documented per blueprint).
3. Apply the matching Ansible playbook from `ansible/playbooks/` using the provided inventory samples.
4. Bootstrap optional k3d clusters to test workloads before pushing to production.
5. (Optional) Use `blueprint_ai_adapter.py` with a mock or real AI provider to draft alternative resource allocations.

Blueprints deliberately expose every important variable—network CIDRs, VLAN tags, storage classes, CPU/memory sizing—so operators can reason about the resulting topology.

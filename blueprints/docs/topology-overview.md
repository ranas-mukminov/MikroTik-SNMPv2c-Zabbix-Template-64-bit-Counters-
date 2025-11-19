# Topology overview

| Blueprint | Target use case | Highlights |
| --------- | --------------- | ---------- |
| `proxmox-homelab` | Enthusiast homelab with virtualization, routing, and storage | Multiple Proxmox nodes, pfSense or OpenWrt edge, Ceph or ZFS-backed storage pools, management jump host |
| `k3s-ci-monitoring` | Lightweight Kubernetes with Git/CI and observability | K3s control-plane, Git service (Gitea), runner nodes, ArgoCD, Prometheus/Grafana |
| `micro-saas` | Minimal production stack for hobby SaaS or SMB portal | Reverse proxy, TLS termination, app nodes, PostgreSQL/Redis, scheduled backups |

Each Terraform blueprint includes notes on remote state, workspaces, and prerequisites. Pair them with the Ansible playbooks for configuration and the k3d manifests for local prototyping.

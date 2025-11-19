# Homelab / SMB Infra-as-Code Blueprints & Cost Optimizer

[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![CI](https://github.com/ranas-mukminov/homelab-cost-optimizer/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)

> Opinionated IaC blueprints for homelabs and small businesses, plus an AI-assisted cost optimizer for your VMs and containers.

---

## English

Homelabs and small offices often grow organically, mixing Proxmox clusters, pfSense firewalls, NAS boxes, and a handful of Docker or Kubernetes workloads. The result is rarely documented, hardly reproducible, and notoriously expensive to power. This repository combines two complementary toolsets to bring order and visibility:

1. **`homelab-blueprints-run-as-daemon`** – A curated catalog of Infra-as-Code blueprints that stitch together Terraform, Ansible, and k3d/k3s manifests for common homelab and SMB topologies.
2. **`homelab-cost-optimizer`** – A Python toolkit and CLI that collects utilization data from hypervisors and container runtimes, estimates power consumption, and proposes consolidation scenarios, optionally enriched by AI-generated reports.

### Motivation

* Homelabs tend to evolve faster than they are documented; rebuilds take weeks.
* Power prices and hardware footprints keep increasing, but capacity planning remains ad-hoc.
* Blog posts usually showcase a single bespoke setup rather than reusable, parameterized catalogs.
* SMBs require production-ready defaults with repeatable automation, not copy-pasted bash snippets.

### What this repository provides

| Area | Highlights |
| ---- | ---------- |
| **IaC blueprints** | Proxmox + OpenWrt/pfSense + NAS topology, K3s/K3d clusters with CI/CD + observability, “Home Office” VPN + storage + backup stack, and a “Micro-SaaS” production starter kit with reverse proxy, TLS, app runtime, database, and backups. |
| **Cost optimizer** | Collectors for Proxmox, libvirt, Docker, and Kubernetes; power estimations using per-node TDP hints + electricity configs; heuristic consolidation plans; Markdown and AI-generated narrative reports. |

### Architecture overview

```
Terraform -> hypervisors, storage, networks
        \-> modules for Proxmox, K3s, Micro-SaaS

Ansible  -> OS hardening, services (OpenWrt, pfSense, NAS, k3s nodes)

k3d/k3s -> optional lightweight clusters for CI/CD & observability

Collectors -> Nodes & workloads
Estimators -> Power & cost figures
Consolidator -> Proposed placements
Reporters -> Text / Markdown / AI narratives
```

Terraform codifies the base infrastructure (hypervisors, VLANs, storage pools). Ansible turns freshly provisioned nodes into firewalls, NAS appliances, or Kubernetes workers. Optional k3d clusters provide local sandboxes. The optimizer ingests runtime telemetry, feeds it into estimators, and generates actionable recommendations.

### Quick start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ranas-mukminov/homelab-cost-optimizer.git
   cd homelab-cost-optimizer
   ```
2. **Pick a blueprint** from `blueprints/terraform` and the matching Ansible playbook.
3. **Set variables** (domains, VLANs, power pricing) inside the blueprint `variables.tf` and `ansible/group_vars`.
4. **Provision with Terraform** and **configure with Ansible**.
5. **Install the optimizer**
   ```bash
   pip install -e optimizer/
   homelab-cost-optimizer --help
   ```
6. **Copy configs**
   ```bash
   cp config/electricity.example.yaml config/electricity.yaml
   cp config/optimizer.example.yaml config/optimizer.yaml
   ```
   Adjust the kWh price, node power profiles, and credentials.
7. **Collect and analyze**
   ```bash
   homelab-cost-optimizer collect --source proxmox --url https://pve.local --token $PVE_TOKEN --out data.json
   homelab-cost-optimizer analyze --inventory data.json --electricity config/electricity.yaml --out report.md
   homelab-cost-optimizer suggest --inventory data.json --scenario consolidate-low-util --out consolidate.md
   ```

### Blueprints catalog

* **`proxmox-homelab`** – Two or three Proxmox nodes, pfSense/OpenWrt edge, NAS VM/LXC, and a management jump host. Emphasizes VLAN separation, storage pools, and backup scheduling hooks.
* **`k3s-ci-monitoring`** – A lightweight K3s or k3d deployment wired with Git service + CI runners, ArgoCD, and Prometheus/Grafana monitoring. Includes ingress, TLS defaults, and optional longhorn storage references.
* **`micro-saas`** – Reverse proxy (Traefik), app container group, PostgreSQL with PITR backups, object storage sync placeholders, and a backup runner. Designed as a starter kit for hobby SaaS or SMB portals.

Variables are centralized, networks are explicit, and every Terraform module is designed as a transparent starting point—not an opaque black box.

### Cost optimizer

The optimizer’s data model tracks nodes, workloads, and power profiles. Collectors normalize information from Proxmox, libvirt, Docker, and Kubernetes. Power estimation combines idle wattage plus utilization-driven deltas. Cost estimation multiplies the energy profile by configurable tariffs. The heuristic consolidator tries to pack underutilized workloads while respecting CPU/RAM limits, producing “what-if” savings along with Markdown tables or AI-generated narratives.

CLI examples:

```bash
homelab-cost-optimizer collect --source docker --socket /var/run/docker.sock --out docker.json
homelab-cost-optimizer analyze --inventory docker.json --electricity config/electricity.yaml --out docker-report.md
homelab-cost-optimizer suggest --inventory docker.json --scenario rightsize --ai-report
```

### AI integration

* `blueprints/ai/blueprint_ai_adapter.py` accepts a hardware inventory + desired topology and asks a configured AI provider to suggest node roles, resource allocations, and Markdown explanations. Deterministic defaults exist; AI is optional.
* `optimizer/homelab_cost_optimizer/reporters/ai_reporter.py` converts raw numbers into human-friendly narratives, listing prioritized recommendations and comparing “before vs after” consolidation outcomes.
* Providers live in `ai_providers/` with a simple abstract base, an OpenAI example (requires `OPENAI_API_KEY`), and a deterministic mock provider for offline/tests.

### Testing and quality

* `pytest` – unit and integration coverage.
* `scripts/lint.sh` – Ruff, Black, YAML linting, and Terraform/Ansible formatting checks (auto-skipped if tooling is missing).
* `scripts/security_scan.sh` – `pip-audit` + `bandit` for dependency and code scanning.
* `scripts/perf_check.sh` – synthetic workload to ensure estimations stay performant.

### Legal and responsible use

* Operate strictly on infrastructure you own or manage with explicit authorization.
* Respect the API terms for Proxmox, libvirt, Docker, Kubernetes, and any cloud providers.
* Power and cost outputs are estimates for planning purposes, not financial advice or billing statements.
* Nothing in this repository bypasses licensing or security controls; stay compliant.

### Professional services – run-as-daemon.ru

> **Professional services by [run-as-daemon.ru](https://run-as-daemon.ru)**
>
> Maintained by a DevSecOps / SRE / FinOps engineer offering consulting for:
> * Blueprinting and automating homelab or SMB infrastructure.
> * Building resilient K3s/Kubernetes clusters with CI/CD and observability.
> * Optimizing infrastructure and power costs with tailored FinOps engagements.
>
> Reach out via the website for consulting, implementation, and ongoing support retainers.

### Contributing

Contributions are welcome! Please read `CONTRIBUTING.md`, open an issue describing your blueprint or feature idea, run `scripts/lint.sh` and `pytest`, and include documentation updates. We encourage blueprint submissions, cost-estimation improvements, and adapters for additional AI providers.

### License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

---

## Русский (кратко)

Репозиторий объединяет два инструмента: каталог IaC-блупринтов для домашнего/SMB-инфраструктуры и оптимизатор затрат, который собирает данные из Proxmox, libvirt, Docker и Kubernetes, оценивает энергопотребление и предлагает сценарии консолидации. Terraform + Ansible + k3d шаблоны помогают быстро поднять Proxmox + OpenWrt/pfSense + NAS, K3s кластер с CI/CD и мониторингом, домашний офис со VPN и бэкапами, а также минимальный micro-SaaS стек. CLI оптимизатора строит отчёты в Markdown или через AI и использует конфиги `config/*.yaml`. Используйте только на инфраструктуре, где у вас есть права доступа, соблюдайте условия API и помните, что расчёты энергопотребления являются приблизительными. За профессиональные услуги и поддержку обращайтесь на [run-as-daemon.ru](https://run-as-daemon.ru).

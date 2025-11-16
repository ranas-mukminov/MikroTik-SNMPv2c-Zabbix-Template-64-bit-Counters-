# Node Exporter Full Grafana Pack

> Production-ready Linux host observability stack built around rfmoz’s “Node Exporter Full” Grafana dashboard.

This repository streamlines the classic Grafana dashboard from https://grafana.com/grafana/dashboards/1860-node-exporter-full/ into a clone-and-run package. Prometheus, Grafana, node-exporter, alert rules, and the dashboard JSON are bundled so intermediate DevOps engineers can explore Linux host metrics in minutes.

## Features
- Turnkey Docker Compose stack for Prometheus, Grafana and node-exporter.
- Original Node Exporter Full dashboard JSON (revision 42) ready for import.
- Opinionated Prometheus scrape and alert configuration focused on host health.
- Sample alert rules for uptime, CPU, memory, disk and network anomalies.
- Clear guidance on required metrics, labels, and how to adapt to real fleets.
- Structured dashboard tour so teams know which panel solves which problem.

## Dashboard Sections at a Glance
- **Overview** – “Quick CPU / Mem / Disk” row with gauges for CPU busy, load, RAM, swap, root FS, total resources and uptime.
- **Basic Trends** – “Basic CPU / Mem / Net / Disk” timeseries that overlay utilization, RAM pressure, combined TX/RX throughput, and root filesystem usage trends.
- **Memory Deep Dive** – “Memory Meminfo” and “Memory Vmstat” rows covering committed memory, huge pages, swap churn, page faults, and cache/buffer dynamics.
- **System Health** – Rows for “System Timesync”, “Processes”, “System Misc”, “Hardware Misc”, and “Systemd” that expose NTP offset, run queue, interrupts, temperatures, voltages, entropy, and unit failures.
- **Storage** – “Storage Disk” (IOPS, throughput, await) and “Storage Filesystem” (capacity, inodes) views per block device and mount.
- **Network** – “Network Traffic”, “Sockstat”, and “Netstat” panels tracking interface throughput, packet errors, socket usage, and TCP connection states.
- **Collector Health** – “Node Exporter” row monitoring scrape duration, build info, and whether collectors expose errors.

## Quick Start
```bash
git clone https://github.com/your-org/node-exporter-full-stack.git
cd node-exporter-full-stack
docker compose up -d
open http://localhost:3000
# login admin / admin → Connections → Data sources → Prometheus (http://prometheus:9090)
# Dashboards → Import → Upload dashboard/node-exporter-full.json → choose Prometheus datasource
```

## Configuration
- Prometheus expects a `node` job that exposes standard node-exporter metrics such as `node_cpu_seconds_total`, `node_memory_MemAvailable_bytes`, `node_filesystem_*`, `node_network_*`, and `node_time_seconds`.
- Labels used throughout the dashboard: `job` (defaults to `node`), `instance` (host identifier), `device` for disks, `fstype` to suppress pseudo filesystems, and `interface` for NIC charts.
- To monitor real servers, add more `static_configs` (or service discovery blocks) under the `node` job in `prometheus/prometheus.yml`. Ensure each target matches the labels above.
- When running node-exporter on bare metal or VMs, use the host binaries or privileged container with `--path.rootfs` mounts so metrics reflect the actual system rather than the container.
- Grafana ships without pre-provisioned datasources to keep credentials out of the repo; create a Prometheus datasource pointing to `http://prometheus:9090` then import `dashboard/node-exporter-full.json`.

## Dashboard Tour

| Panel / Section | What it shows | How to use it / problems it finds |
| --- | --- | --- |
| Quick CPU / Mem / Disk | Gauges and stats for CPU busy %, load averages, RAM used, swap used, root filesystem %, total resources, uptime | Instant sanity check: spot overloaded CPUs (>85%), memory leaks, shrinking free disk or unexpected reboots. |
| Basic CPU / Mem / Net / Disk | Combined timeseries for CPU, memory, network throughput, and disk space trends | Correlate spikes during incidents and verify whether utilization is stable after changes or deployments. |
| Memory Meminfo & Vmstat | Committed memory vs limit, caches, buffers, huge pages, swap in/out, page faults | Determine if OOM events loom (commit charge), if caches can be reclaimed, or whether swap thrashing causes latency. |
| Storage Disk & Filesystem | Per-device IOPS, read/write bandwidth, await times, filesystem capacity and inode usage | Identify hot disks, failing volumes with high await, or filesystems close to full that may block deployments/logging. |
| Network Traffic | TX/RX throughput per interface with error/discard overlays plus Sockstat/Netstat panels | Catch NIC saturation, packet errors, SYN floods, or runaway socket consumption that depletes networking resources. |
| System Health Rows | Timesync offset, process counts, interrupts, context switches, temperatures, voltages, entropy, Systemd unit failures | Validate that hosts stay in sync, look for interrupt storms, hardware issues, entropy starvation, or failing systemd units. |
| Node Exporter | Exporter build info, scrape durations, `up` state | Troubleshoot missing data—if scrape duration grows or `up` drops to 0, check firewall, credentials or resource pressure. |

## Alerts
Sample alert rules (`alerts/node-exporter-alerts.yml`) cover:
- **NodeDown** – fires when Prometheus cannot scrape a host for 2 minutes.
- **NodeHighCpuSustained** – warns if average non-idle CPU stays above 85% for 5 minutes.
- **NodeMemoryPressure** – triggers when available memory stays below 10% for 5 minutes (indicates looming OOM).
- **NodeDiskSpaceLow** – alerts when filesystems have less than 15% free space (excluding tmpfs/overlay) for 10 minutes.
- **NodeFilesystemReadonly** – critical alert if any filesystem reports read-only state.
- **NodeNetworkErrorsBurst** – highlights recurring RX/TX errors, signaling faulty NICs, cabling, or driver issues.

Tune thresholds, severities, or label matches in `alerts/node-exporter-alerts.yml` to align with your SLA.

## Credits
- Original Grafana dashboard: **“Node Exporter Full”** by **rfmoz** (https://grafana.com/grafana/dashboards/1860-node-exporter-full/).  
  Please credit them whenever you share this package by adding a note such as: *“Dashboard derived from Node Exporter Full by rfmoz (grafana.com/dashboards/1860).”*
- node-exporter maintained by the Prometheus project.

If the upstream dashboard license is unclear on grafana.com, treat the JSON as reference material and follow the original author’s terms when redistributing.

## License
Code in this repository (compose stack, Prometheus config, alert rules, documentation) is offered under MIT.  
Dashboard JSON inherits the licensing of rfmoz’s original work; review the upstream terms before commercial redistribution.

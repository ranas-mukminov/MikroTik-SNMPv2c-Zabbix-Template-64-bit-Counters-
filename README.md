# MikroTik SNMP Zabbix Templates (Production-Ready v2.0)

**Professional-grade Zabbix 7.0+ templates for comprehensive MikroTik RouterOS monitoring**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zabbix: 7.0+](https://img.shields.io/badge/Zabbix-7.0+-red.svg)](https://www.zabbix.com)
[![RouterOS: 6.x/7.x](https://img.shields.io/badge/RouterOS-6.x%2F7.x-orange.svg)](https://mikrotik.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Available Templates](#available-templates)
- [Features](#features)
- [Quick Start](#quick-start)
- [Security Best Practices](#security-best-practices)
- [Detailed Configuration](#detailed-configuration)
- [Monitored Metrics](#monitored-metrics)
- [Triggers and Alerting](#triggers-and-alerting)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
- [Professional Support](#professional-support)
- [Contributing](#contributing)
- [Changelog](#changelog)

---

## 🎯 Overview

This repository provides **production-ready Zabbix monitoring templates** for MikroTik RouterOS devices with enterprise-level features:

- ✅ **Complete network visibility** - interfaces, routing protocols, hardware health
- ✅ **64-bit counters** - no counter wrapping on high-speed links (10G+)
- ✅ **Security-first approach** - SNMPv3 with encryption, secure defaults
- ✅ **Intelligent discovery** - automatic interface and routing protocol detection
- ✅ **Advanced preprocessing** - accurate rate calculations and unit conversions
- ✅ **Smart alerting** - trigger dependencies, hysteresis, severity levels
- ✅ **Capacity planning** - bandwidth utilization, resource trending
- ✅ **Broadcast storm detection** - network loop and misconfiguration alerts

---

## 📦 Available Templates

### 1. **Advanced SNMPv2c Template** (Recommended for most deployments)
**File:** [template_mikrotik_snmpv2c_advanced_zbx72.xml](template_mikrotik_snmpv2c_advanced_zbx72.xml)

- Full-featured monitoring with 64-bit counters
- CPU, memory, temperature, voltage monitoring
- OSPF and BGP protocol monitoring
- Interface errors, discards, and utilization tracking
- Graph prototypes for visualization
- **Use case:** Internal networks, trusted environments

⚠️ **Security Note:** SNMPv2c transmits community strings in plaintext. Use strong, unique community strings and restrict access by IP.

### 2. **Advanced SNMPv3 Template** (Recommended for production/WAN)
**File:** [template_mikrotik_snmpv3_advanced_zbx72.xml](template_mikrotik_snmpv3_advanced_zbx72.xml)

- All features of SNMPv2c template
- **Encrypted SNMP communication** (AES)
- **Authentication** (SHA/MD5)
- **User-based access control**
- No plaintext credentials
- **Use case:** Production environments, WAN monitoring, security-conscious deployments

### 3. **Basic SNMPv2c Template** (Legacy - for reference)
**File:** [template_mikrotik_snmpv2c_zbx72_uuid32.xml](template_mikrotik_snmpv2c_zbx72_uuid32.xml)

- Original basic template
- Interface monitoring only
- **Use case:** Testing, minimal deployments, compatibility reference

---

## 🚀 Features

### Network Monitoring
- 📡 **Automatic interface discovery** with smart filtering (excludes virtual/tunnel interfaces)
- 📊 **64-bit traffic counters** (ifHCInOctets/ifHCOutOctets) - supports 10G+ links
- 📈 **Bandwidth utilization** - real-time % calculation vs configured speed
- ⚠️ **Error and discard tracking** - detect physical layer issues and buffer overflows
- 🌐 **Broadcast/multicast monitoring** - storm detection and network loop alerts
- 🔄 **Interface status monitoring** - link up/down with value mapping

### Routing Protocol Monitoring
- 🦅 **OSPF neighbor discovery** - automatic adjacency monitoring
- 🌍 **BGP peer discovery** - session state and prefix tracking
- 📡 **Protocol state alerts** - detect routing failures instantly

### System Health Monitoring
- 🖥️ **CPU utilization** - multi-level thresholds (warning/critical)
- 💾 **Memory utilization** - calculated percentage with alerts
- 🌡️ **Temperature monitoring** - MikroTik-specific hardware sensors
- ⚡ **Voltage monitoring** - power supply health checks
- ⏱️ **Uptime tracking** - device restart detection
- 🔧 **RouterOS version** - inventory management

### Availability Monitoring
- 🏓 **ICMP ping checks** - basic reachability
- 📉 **Packet loss tracking** - latency and quality monitoring
- ⏱️ **Response time metrics** - performance tracking

### Visualization
- 📊 **Graph prototypes** - automatic graphs for all discovered interfaces
  - Traffic graphs (in/out bandwidth)
  - Utilization graphs (% of capacity)
  - Error and discard graphs
  - Broadcast/multicast graphs

### Advanced Features
- 🏷️ **Modern tagging** - Zabbix 7.0 tag structure (class, target, component)
- 🔗 **Trigger dependencies** - intelligent alert suppression
- ⏲️ **Hysteresis** - flapping prevention (link down requires 2-minute confirmation)
- 🎯 **Value mappings** - human-readable status values
- ⚙️ **Macro-based configuration** - easy per-host customization
- 📝 **Comprehensive descriptions** - every item and trigger documented

---

## ⚡ Quick Start

### Prerequisites
- Zabbix Server 7.0 or higher
- MikroTik device with RouterOS 6.x or 7.x
- SNMP enabled on MikroTik
- Network connectivity between Zabbix and MikroTik

### 5-Minute Setup (SNMPv2c)

#### Step 1: Configure MikroTik SNMP
```bash
# Connect to MikroTik via SSH or Winbox
/snmp
set enabled=yes
set contact="admin@example.com"
set location="DataCenter-1, Rack-A5"

# Create unique community string (change 'MySecureString123!' to your own!)
/snmp community
set [find default=yes] name="MySecureString123!" addresses=10.0.0.100/32

# Test SNMP from Zabbix server
# snmpwalk -v2c -c MySecureString123! <mikrotik-ip> system
```

#### Step 2: Import Zabbix Template
1. Go to **Zabbix UI → Configuration → Templates**
2. Click **Import**
3. Choose **template_mikrotik_snmpv2c_advanced_zbx72.xml**
4. Enable options:
   - ✅ Create new
   - ✅ Update existing
   - ✅ Delete missing
5. Click **Import**

#### Step 3: Create Host
1. Go to **Configuration → Hosts → Create host**
2. **Host name:** `mikrotik-router-01`
3. **Groups:** `Routers` (or create new)
4. **Interfaces:**
   - **Type:** SNMP
   - **IP address:** `192.168.1.1` (your MikroTik IP)
   - **Port:** `161`
   - **SNMP version:** `SNMPv2`
   - **Community:** `{$SNMP_COMMUNITY}` (macro, will be overridden)
5. **Templates:** Select `Template MikroTik SNMPv2c Advanced (Production)`
6. Go to **Macros** tab → **Host macros**
7. Add macro:
   - **Macro:** `{$SNMP_COMMUNITY}`
   - **Value:** `MySecureString123!` (your actual community string)
8. Click **Add**

#### Step 4: Verify
Wait 2-3 minutes, then check:
- **Monitoring → Latest data** - you should see CPU, memory, uptime, interfaces
- **Monitoring → Discovery** - interfaces should be discovered
- **Monitoring → Graphs** - traffic graphs should appear

### ✅ Post-Import Verification Checklist

1. **Run local static checks**
   ```bash
   ./tests/run_checks.sh
   ```
   - Ensures all XML templates are well-formed
   - Confirms UUID uniqueness and macro syntax
   - Safe to run before committing or opening a PR
2. **Confirm macro overrides**
   - `{$SNMP_COMMUNITY}` (SNMPv2c) or `{$SNMPV3_*}` (SNMPv3) must be set per host
   - Adjust threshold macros (`{$CPU.UTIL.WARN}`, `{$MEM.UTIL.CRIT}`, etc.) to match your SLA
3. **Inspect discovery output**
   - Interfaces should appear under **Monitoring → Discovery** within 30 minutes
   - Verify OSPF/BGP neighbors if those features are enabled on the router
4. **Spot-check hardware metrics**
   - Temperature, voltage, and uptime items should update at the polling interval
   - Unexpected `Unsupported item` errors usually indicate SNMP filters or firewall blocks
5. **Optional: live OID validation**
   - Use [`tests/test_oids.sh`](tests/test_oids.sh) against a lab router before production
   - Confirms RouterOS exposes all OIDs required by the templates

---

## 🔒 Security Best Practices

### SNMPv2c Security (if you must use it)

⚠️ **WARNING:** SNMPv2c sends community strings in **PLAINTEXT**. This is a security risk!

**Mitigation steps:**
1. **Use strong community strings**
   ```bash
   # Bad:  "public", "private", "community"
   # Good: "Zx9#mK2$pL7@vN3&qR8" (20+ random characters)
   ```

2. **Restrict by source IP**
   ```bash
   /snmp community
   set [find] addresses=10.0.0.100/32  # Only allow Zabbix server
   ```

3. **Use management VLAN**
   - Place MikroTik management interface on isolated VLAN
   - Restrict access with firewall rules

4. **Monitor for unauthorized access**
   ```bash
   /log print where topics~"snmp"
   ```

### SNMPv3 Security (RECOMMENDED)

✅ **SNMPv3 provides encryption and authentication**

#### Configure MikroTik for SNMPv3
```bash
/snmp
set enabled=yes

# Create SNMPv3 user with authentication and encryption
/snmp community
add name=zabbix_monitor \
    authentication-protocol=SHA1 \
    encryption-protocol=AES \
    authentication-password="YourStrongAuthPassword123!" \
    encryption-password="YourStrongPrivPassword456!" \
    addresses=10.0.0.100/32

# Disable SNMPv1/v2c if not needed
/snmp
set trap-version=3
```

#### Configure Zabbix Host for SNMPv3
1. Create host with **SNMP interface**
2. **SNMP version:** `SNMPv3`
3. **Context name:** (leave empty)
4. **Security name:** `zabbix_monitor`
5. **Security level:** `authPriv` (authentication + encryption)
6. **Authentication protocol:** `SHA`
7. **Authentication passphrase:** `YourStrongAuthPassword123!`
8. **Privacy protocol:** `AES`
9. **Privacy passphrase:** `YourStrongPrivPassword456!`

**OR** use macros (recommended for multiple hosts):
- `{$SNMPV3_USER}` = `zabbix_monitor`
- `{$SNMPV3_AUTH_PASSPHRASE}` = `YourStrongAuthPassword123!`
- `{$SNMPV3_PRIV_PASSPHRASE}` = `YourStrongPrivPassword456!`

---

## ⚙️ Detailed Configuration

### Template Macros Reference

All templates use macros for easy customization. Override at **host level** for specific devices or **template level** for global defaults.

#### SNMP Authentication
| Macro | Default | Description |
|-------|---------|-------------|
| `{$SNMP_COMMUNITY}` | `CHANGE_ME_SECURITY_RISK` | SNMPv2c community string (⚠️ change immediately!) |
| `{$SNMPV3_USER}` | `zabbix_monitor` | SNMPv3 username |
| `{$SNMPV3_AUTH_PASSPHRASE}` | `CHANGE_ME_AUTH_PASSWORD` | SNMPv3 auth password (min 8 chars) |
| `{$SNMPV3_PRIV_PASSPHRASE}` | `CHANGE_ME_PRIV_PASSWORD` | SNMPv3 encryption password (min 8 chars) |

#### Interface Discovery Filters
| Macro | Default | Description |
|-------|---------|-------------|
| `{$IF.LLD.FILTER.MATCH}` | `.*` | Include interfaces matching regex |
| `{$IF.LLD.FILTER.NOT_MATCHES}` | `(?i:loopback\|virtual\|vlan\|gre\|pppoe\|eoip\|6to4)` | Exclude virtual/tunnel interfaces |
| `{$IF.LLD.FILTER.ADMIN_STATUS}` | `^1$` | Only discover "up" interfaces (1=up, 2=down) |

#### Polling Intervals
| Macro | Default | Description |
|-------|---------|-------------|
| `{$IF.POLL.INTERVAL}` | `1m` | Interface metrics polling (use `30s` for critical links) |
| `{$IF.DISCOVERY.INTERVAL}` | `30m` | How often to rediscover interfaces |

#### Interface Thresholds
| Macro | Default | Description |
|-------|---------|-------------|
| `{$IF.ERRORS.MAX_DELTA}` | `1` | Max errors/sec before WARNING alert |
| `{$IF.DISCARDS.MAX_DELTA}` | `10` | Max discards/sec before WARNING alert |
| `{$IF.BROADCAST.MAX_PPS}` | `1000` | Max broadcast packets/sec (storm detection) |

#### CPU and Memory Thresholds
| Macro | Default | Description |
|-------|---------|-------------|
| `{$CPU.UTIL.WARN}` | `80` | CPU warning threshold (%) |
| `{$CPU.UTIL.CRIT}` | `90` | CPU critical threshold (%) |
| `{$MEM.UTIL.WARN}` | `85` | Memory warning threshold (%) |
| `{$MEM.UTIL.CRIT}` | `95` | Memory critical threshold (%) |

#### Hardware Health Thresholds
| Macro | Default | Description |
|-------|---------|-------------|
| `{$TEMP.MAX.WARN}` | `60` | Temperature warning (°C) |
| `{$TEMP.MAX.CRIT}` | `75` | Temperature critical (°C) |
| `{$VOLTAGE.MIN}` | `11` | Minimum voltage (V) - adjust for device |
| `{$VOLTAGE.MAX}` | `26` | Maximum voltage (V) - adjust for device |

#### ICMP Thresholds
| Macro | Default | Description |
|-------|---------|-------------|
| `{$ICMP.LOSS.WARN}` | `20` | Packet loss warning threshold (%) |

---

## 📊 Monitored Metrics

### Interface Metrics (per discovered interface)
- **Traffic:** Inbound/outbound bandwidth (bps, 64-bit counters)
- **Utilization:** Bandwidth usage as % of configured speed
- **Status:** Operational status (up/down with value mapping)
- **Errors:** Inbound/outbound error rate (errors/sec)
- **Discards:** Inbound/outbound discard rate (packets/sec) - QoS/buffer indicator
- **Broadcast:** Broadcast packet rate (storm detection)
- **Multicast:** Multicast packet rate
- **Speed:** Configured interface speed (Mbps)
- **Alias:** Interface description/alias

### System Metrics
- **CPU:** Utilization percentage
- **Memory:** Total, used, utilization percentage
- **Uptime:** System uptime in seconds
- **Description:** System description string
- **Name:** Device hostname (sysName)
- **Location:** Physical location (sysLocation)
- **Contact:** Administrator contact (sysContact)

### Hardware Health Metrics (MikroTik-specific)
- **Temperature:** System temperature (°C)
- **Voltage:** Power supply voltage (V)
- **RouterOS Version:** Installed RouterOS version
- **Serial Number:** Device serial number

### Routing Protocol Metrics

#### OSPF (discovered per neighbor)
- **State:** Neighbor state (down/init/twoWay/full)
- **Router ID:** Neighbor router ID

#### BGP (discovered per peer)
- **State:** Peer state (idle/connect/active/established)
- **Remote AS:** Peer autonomous system number
- **Received Messages:** Total messages from peer

### Availability Metrics
- **ICMP Ping:** Reachability (0/1)
- **Response Time:** ICMP round-trip time (seconds)
- **Packet Loss:** ICMP packet loss percentage

---

## 🚨 Triggers and Alerting

### Severity Levels
- 🔴 **HIGH** - Immediate action required (device down, critical resource exhaustion)
- 🟠 **AVERAGE** - Timely attention needed (interface down, routing issue)
- 🟡 **WARNING** - Monitor situation (high utilization, elevated errors)
- 🔵 **INFO** - Informational (device restarted)

### Availability Triggers
| Trigger | Severity | Condition | Dependencies |
|---------|----------|-----------|--------------|
| Device unreachable via ICMP | 🔴 HIGH | No ICMP response for 5 min | *None* (root cause) |
| High ICMP packet loss | 🟡 WARNING | >20% loss for 5 min | - |

### Interface Triggers
| Trigger | Severity | Condition | Dependencies |
|---------|----------|-----------|--------------|
| Interface is down | 🟠 AVERAGE | OperStatus=down for 2 min (hysteresis) | Device unreachable |
| Critical bandwidth utilization | 🔴 HIGH | >95% for 15 min | - |
| High bandwidth utilization | 🟡 WARNING | >80% for 15 min | - |
| High error rate | 🟡 WARNING | >1 error/sec for 5 min | - |
| High packet discard rate | 🟡 WARNING | >10 discards/sec for 5 min | - |
| Broadcast storm | 🟡 WARNING | >1000 broadcast pps for 5 min | - |

### System Triggers
| Trigger | Severity | Condition | Dependencies |
|---------|----------|-----------|--------------|
| Critical CPU utilization | 🔴 HIGH | >90% for 5 min | - |
| High CPU utilization | 🟡 WARNING | >80% for 5 min | - |
| Critical memory utilization | 🔴 HIGH | >95% for 5 min | - |
| High memory utilization | 🟡 WARNING | >85% for 5 min | - |
| Device has been restarted | 🔵 INFO | Uptime < 10 min | - |

### Hardware Triggers
| Trigger | Severity | Condition | Dependencies |
|---------|----------|-----------|--------------|
| Critical temperature | 🔴 HIGH | >75°C for 5 min | - |
| High temperature | 🟡 WARNING | >60°C for 5 min | - |
| Abnormal voltage | 🟠 AVERAGE | <11V or >26V for 5 min | - |

### Routing Protocol Triggers
| Trigger | Severity | Condition | Dependencies |
|---------|----------|-----------|--------------|
| OSPF neighbor not in Full state | 🟠 AVERAGE | State ≠ Full for 3 min | - |
| BGP peer not established | 🟠 AVERAGE | State ≠ Established for 5 min | - |

---

## 🎨 Customization

### Example: Monitor only ether1-ether5 interfaces

**Override macro at host level:**
```
{$IF.LLD.FILTER.MATCH} = ^ether[1-5]$
```

### Example: Include VLAN interfaces

**Override macro:**
```
{$IF.LLD.FILTER.NOT_MATCHES} = (?i:loopback|virtual|gre|pppoe)
```
(removed `vlan` from the exclusion list)

### Example: Monitor interfaces regardless of admin status

**Override macro:**
```
{$IF.LLD.FILTER.ADMIN_STATUS} = .*
```

### Example: Adjust for 24V devices (CCR series)

**Override macros:**
```
{$VOLTAGE.MIN} = 20
{$VOLTAGE.MAX} = 28
```

### Example: Poll critical WAN links every 30 seconds

**Create separate host or use host macro:**
```
{$IF.POLL.INTERVAL} = 30s
```

---

## 🔧 Troubleshooting

### No data from SNMP

**Check MikroTik SNMP configuration:**
```bash
/snmp print
# Ensure: enabled=yes

/snmp community print
# Ensure: correct community name, allowed IP includes Zabbix server
```

**Test SNMP from Zabbix server:**
```bash
# SNMPv2c test
snmpwalk -v2c -c YourCommunity <mikrotik-ip> system

# SNMPv3 test
snmpwalk -v3 -l authPriv -u zabbix_monitor \
  -a SHA -A "YourAuthPass" \
  -x AES -X "YourPrivPass" \
  <mikrotik-ip> system
```

**Check Zabbix host interface:**
- Correct IP address?
- Port 161?
- SNMP version matches MikroTik configuration?
- Community/credentials correct?

### Interfaces not discovered

**Check discovery filter macros:**
```bash
# On MikroTik, list all interfaces:
/interface print

# Check if names match your filter regex
```

**Force rediscovery:**
- Go to **Configuration → Hosts → [Your Host] → Discovery**
- Click **Execute now** on "Network interface discovery"

### High CPU on Zabbix server

**Reduce polling frequency for non-critical hosts:**
```
{$IF.POLL.INTERVAL} = 5m
{$IF.DISCOVERY.INTERVAL} = 1h
```

**Limit discovered interfaces:**
```
{$IF.LLD.FILTER.MATCH} = ^(ether|sfp).*
```

### False positive: Interface flapping alerts

**Increase hysteresis time (edit trigger):**
```
Current: net.if.status[{#IFINDEX}].count(2m,2)>1
Change to: net.if.status[{#IFINDEX}].count(5m,3)>2
```

### MikroTik doesn't support certain OIDs

**Some older RouterOS versions or devices may not support:**
- `ifHCInOctets` (64-bit counters) - upgrade RouterOS or use 32-bit version
- `hrProcessorLoad` (CPU) - try MikroTik-specific OID: `1.3.6.1.4.1.14988.1.1.3.1.0`
- OSPF/BGP MIBs - ensure routing packages installed and protocols enabled

---

## 💼 Examples

Detailed configuration examples are available in the [examples/](examples/) directory:

- **[mikrotik_snmp_config.rsc](examples/mikrotik_snmp_config.rsc)** - Complete MikroTik SNMP configuration script
- **[zabbix_host_config_example.md](examples/zabbix_host_config_example.md)** - Step-by-step Zabbix host setup
- **[dashboard_example.json](examples/dashboard_example.json)** - Pre-built Zabbix dashboard (import-ready)

---

## 🏢 Professional Support

Need help deploying these templates in your production environment?

### We offer:
- ✅ Custom template development for your specific MikroTik deployment
- ✅ Integration with existing monitoring infrastructure
- ✅ Performance optimization and troubleshooting
- ✅ Training for your IT team
- ✅ 24/7 monitoring service setup

**Contact:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-improvement`)
3. Test your changes thoroughly
4. Commit with clear messages (`git commit -m 'Add VRRP monitoring'`)
5. Push to your branch (`git push origin feature/amazing-improvement`)
6. Open a Pull Request

**Please ensure:**
- XML is valid (test with `xmllint --noout template.xml`)
- All UUIDs are unique
- Macros are documented
- Triggers include descriptions

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Latest: v2.0.0** (2025-01-XX)
- ✅ Complete rewrite with production-ready features
- ✅ Added SNMPv3 template with encryption
- ✅ Added CPU, memory, hardware health monitoring
- ✅ Added OSPF and BGP monitoring
- ✅ Added discard and broadcast/multicast tracking
- ✅ Added bandwidth utilization calculated items
- ✅ Added graph prototypes
- ✅ Improved security (no default "public" community)
- ✅ Added comprehensive documentation and examples

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- Zabbix community for monitoring best practices
- MikroTik for excellent SNMP support in RouterOS
- Network engineers who provided real-world feedback

---

## 📞 Support & Community

- **Issues:** [GitHub Issues](https://github.com/yourusername/mikrotik-zabbix-template/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/mikrotik-zabbix-template/discussions)
- **Professional Services:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

**Made with ❤️ for network engineers by network engineers**

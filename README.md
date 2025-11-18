# MikroTik SNMPv2c Zabbix Template (64-bit Counters)

Zabbix monitoring template for MikroTik RouterOS devices using SNMPv2c with 64-bit traffic counters.

**[English]** | [Русский](README.ru.md)

---

## Overview

This template provides comprehensive monitoring for MikroTik RouterOS devices through Zabbix. It is designed for network engineers, ISPs, and enterprise IT teams who need reliable SNMP-based monitoring with accurate traffic measurements.

**Why 64-bit counters matter:**

On high-speed links (1 Gbps and above), 32-bit SNMP counters can wrap around in minutes, causing incorrect traffic statistics and graphs. MikroTik devices support 64-bit counters (ifHCInOctets/ifHCOutOctets) which solve this problem by providing a much larger counter range. This template uses 64-bit counters by default and falls back to 32-bit only when the device does not support them.

---

## Features

### Interface Monitoring
- Automatic interface discovery with Low-Level Discovery (LLD)
- RX/TX traffic counters (64-bit: ifHCInOctets, ifHCOutOctets)
- Bandwidth utilization as percentage of configured speed
- Error and discard counters (inbound and outbound)
- Broadcast and multicast packet monitoring
- Operational and administrative status tracking
- Interface speed and alias information

### System Health
- System uptime monitoring
- CPU utilization with configurable thresholds
- Memory utilization (total, used, percentage)
- Hardware temperature monitoring (MikroTik-specific OID)
- Power supply voltage monitoring
- RouterOS version and serial number inventory

### Routing Protocols
- OSPF neighbor discovery and state monitoring
- BGP peer discovery and session state tracking

### Alerting
- Link down detection with hysteresis (prevents flapping alerts)
- High error rate alerts
- High CPU and memory utilization triggers
- Temperature and voltage threshold alerts
- Device unreachable alerts with ICMP monitoring

---

## Requirements

- **Zabbix Server:** 5.x, 6.x, or 7.x
- **MikroTik RouterOS:** 6.x or 7.x with SNMP enabled
- **SNMP Protocol:** SNMPv2c (template is configured for SNMPv2c; SNMPv3 can be used on the host side without template changes)
- **Network connectivity:** Zabbix server must be able to reach MikroTik on UDP port 161

---

## MikroTik SNMP Configuration

Enable SNMP on your MikroTik device and configure a community string:

```bash
/snmp
set enabled=yes contact="admin@example.com" location="DataCenter-A"

/snmp community
set [find default=yes] name="MySecureCommunity" addresses=10.0.0.100/32
```

**Security notes:**
- Always use a strong, unique community string—never use `public` or `private`
- Restrict SNMP access by source IP address (use `addresses=` parameter)
- Consider using SNMPv3 with authentication and encryption for production environments
- Place management interfaces on an isolated VLAN with firewall rules

Test SNMP access from your Zabbix server:

```bash
snmpwalk -v2c -c MySecureCommunity <mikrotik-ip> system
```

---

## Template Import

1. Log in to Zabbix web interface
2. Go to **Configuration → Templates**
3. Click **Import**
4. Select the template file: `template_mikrotik_snmpv2c_advanced_zbx72.xml`
5. Check the following options:
   - Create new
   - Update existing
   - Delete missing (if updating)
6. Click **Import**

After import, the template will appear as `Template MikroTik SNMPv2c Advanced (Production)` under **Templates/Network devices**.

> **⚠️ Mandatory security action:** The template intentionally ships with the placeholder `CHANGE_ME_SNMPV2C` for the `{$SNMP_COMMUNITY}` macro. Override this macro per host (or per secure host group) immediately after import—otherwise discovery and polling will fail, and you risk falling back to the insecure, guessable `public` string if someone reuses RouterOS defaults. For encrypted/authenticated monitoring prefer the bundled **RouterOS SNMPv3 template** (`template_mikrotik_snmpv3_advanced_zbx72.xml`).

---

## Linking Template to Host

1. Go to **Configuration → Hosts**
2. Click **Create host** or edit an existing host
3. Fill in the host details:
   - **Host name:** `mikrotik-router-01`
   - **Groups:** Select or create `Routers`
4. Add an **SNMP interface**:
   - **Type:** SNMP
   - **IP address:** (your MikroTik IP, e.g., `192.168.1.1`)
   - **Port:** `161`
   - **SNMP version:** SNMPv2
   - **SNMP community:** `{$SNMP_COMMUNITY}` (leave as macro)
5. Go to the **Templates** tab
6. Link the template: `Template MikroTik SNMPv2c Advanced (Production)`
7. Go to the **Macros** tab, select **Host macros**
8. Add or override the following macro:
   - **Macro:** `{$SNMP_COMMUNITY}`
   - **Value:** `MySecureCommunity` (the actual community string)
9. Click **Add** or **Update**

Within a few minutes, Zabbix will start collecting data. Check **Monitoring → Latest data** to verify.

### Host Inventory population

This template links several SNMP items to the Zabbix host inventory so key context is filled in automatically:

| Template item | SNMP source | Inventory field |
|---------------|-------------|-----------------|
| `system.descr[sysDescr]` | `SNMPv2-MIB::sysDescr.0` | **Type** |
| `system.name` *(advanced template)* | `SNMPv2-MIB::sysName.0` | **Name** |
| `system.location` *(advanced template)* | `SNMPv2-MIB::sysLocation.0` | **Location** |

To allow Zabbix to write these values, enable the host inventory and set the **Inventory mode** to **Automatic** (Configuration → Hosts → select the host → **Inventory** tab). Zabbix will then populate the above fields as soon as the associated items receive data.

---

## Macros & Customization

The template uses macros for flexible configuration. Override these macros at the host or template level as needed.

> **Why override `{$SNMP_COMMUNITY}` per host?** Using a single community across all routers (especially `public`) exposes your entire network inventory and configuration to anyone who can reach UDP/161. Set a unique, random string on each MikroTik (or at least per secure group) and mirror it in the host or group macro. Never leave RouterOS at the `public` default—attackers routinely scan for it, and it grants read access to routing tables, interface stats, and inventory data.

### SNMP Authentication
| Macro | Default | Description |
|-------|---------|-------------|
| `{$SNMP_COMMUNITY}` | `CHANGE_ME_SNMPV2C` | SNMPv2c community string (must be overridden per host/group) |

### Interface Discovery Filters
| Macro | Default | Description |
|-------|---------|-------------|
| `{$IF.LLD.FILTER.MATCH}` | `.*` | Regular expression to include interfaces |
| `{$IF.LLD.FILTER.NOT_MATCHES}` | `(?i:loopback\|virtual\|vlan\|gre\|pppoe\|eoip\|6to4)` | Regular expression to exclude virtual/tunnel interfaces |
| `{$IF.LLD.FILTER.ADMIN_STATUS}` | `^1$` | Only discover interfaces with admin status "up" (1=up, 2=down) |

### CPU and Memory Thresholds
| Macro | Default | Description |
|-------|---------|-------------|
| `{$CPU.UTIL.WARN}` | `80` | CPU utilization warning threshold (%) |
| `{$CPU.UTIL.CRIT}` | `90` | CPU utilization critical threshold (%) |
| `{$MEM.UTIL.WARN}` | `85` | Memory utilization warning threshold (%) |
| `{$MEM.UTIL.CRIT}` | `95` | Memory utilization critical threshold (%) |

### Examples

**Exclude VPN and tunnel interfaces from discovery:**

Set `{$IF.LLD.FILTER.NOT_MATCHES}` to:
```
(?i:loopback|virtual|vlan|gre|pppoe|eoip|6to4|wireguard|ovpn)
```

**Adjust CPU thresholds for a less critical device:**

Override at host level:
```
{$CPU.UTIL.WARN} = 90
{$CPU.UTIL.CRIT} = 95
```

**Monitor only specific interfaces (e.g., ether1-ether5):**

Set `{$IF.LLD.FILTER.MATCH}` to:
```
^ether[1-5]$
```

---

## 64-bit Counters Explanation

SNMP provides two sets of traffic counters:

- **32-bit counters** (ifInOctets, ifOutOctets): Maximum value is 4,294,967,295 bytes (~4 GB). On a 1 Gbps link running at full speed, these counters wrap around every 34 seconds.
- **64-bit counters** (ifHCInOctets, ifHCOutOctets): Maximum value is approximately 18 exabytes. These counters will not wrap around even on 10 Gbps or faster links.

When a counter wraps around, monitoring systems may report incorrect data (negative values, spikes, or gaps in graphs). This is why 64-bit counters are critical for accurate monitoring on high-speed networks.

This template is designed to use 64-bit counters by default. If a MikroTik device or interface does not support 64-bit counters (very old RouterOS versions), the template will fall back to 32-bit counters. For best results, ensure your RouterOS version is up to date (6.x or 7.x).

---

## Troubleshooting

### No data from host

**Possible causes:**
- SNMP is not enabled on MikroTik
- Incorrect community string in Zabbix host configuration
- Firewall blocking UDP port 161
- IP address restriction on MikroTik SNMP configuration

**How to check:**
1. Verify SNMP is enabled on MikroTik:
   ```bash
   /snmp print
   ```
2. Test SNMP connectivity from Zabbix server:
   ```bash
   snmpwalk -v2c -c YourCommunity <mikrotik-ip> system
   ```
3. Check Zabbix host interface settings (IP, port, community)
4. Review Zabbix server logs for SNMP timeout errors

### Interfaces not discovered

**Possible causes:**
- LLD filters exclude all interfaces
- Interfaces are administratively down
- SNMP does not expose interface data

**How to check:**
1. List all interfaces on MikroTik:
   ```bash
   /interface print
   ```
2. Adjust `{$IF.LLD.FILTER.NOT_MATCHES}` macro to include desired interfaces
3. Manually trigger discovery in Zabbix:
   **Configuration → Hosts → [Host] → Discovery → Execute now**

### Traffic spikes or weird values

**Possible causes:**
- Counter wrap-around (32-bit counters on fast links)
- Device reboot (counters reset to zero)
- Polling interval too long

**How to fix:**
- Ensure 64-bit counters are supported and in use
- Upgrade RouterOS if using an old version
- Reduce polling interval for critical interfaces (edit items or use `{$IF.POLL.INTERVAL}` macro)

### SNMP timeouts

**Possible causes:**
- High CPU load on MikroTik
- Network latency or packet loss
- SNMP request rate too high

**How to fix:**
- Increase SNMP timeout in Zabbix host interface settings
- Reduce polling frequency (increase item intervals)
- Check network connectivity and latency with `ping` and `traceroute`
- Verify MikroTik CPU utilization with `/system resource print`

---

## Roadmap

Planned improvements for future releases:

- Test and validate template on RouterOS v7.x latest stable releases
- Add more granular LLD filters for interface types (wired, wireless, bridge)
- Improve trigger hysteresis and alert dependencies to reduce false positives
- Create optional SNMPv3 configuration examples with authentication and encryption
- Develop sample Grafana dashboards for visualizing data collected by this template
- Add wireless client monitoring for MikroTik wireless access points

Contributions and suggestions are welcome. See the [Contributing](#contributing) section below.

---

## Local Testing

Structural checks for every `template_*.xml` file live under `tests/` and can be run with `pytest`. This is the same command the CI workflow executes on every pull request.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Make your changes and test them thoroughly
4. Commit your changes: `git commit -m "Add feature: description"`
5. Push to your branch: `git push origin feature/my-improvement`
6. Open a Pull Request

**Guidelines:**
- Keep template names and keys consistent with existing structure
- Avoid breaking changes without clear migration notes
- Test your changes on a real MikroTik device
- Document tested RouterOS and Zabbix versions in your PR description
- Ensure XML is valid before submitting (use `xmllint` or the test scripts in `tests/`)

---

## Maintainer and License

**Maintainer:** Ranas Mukminov  
**Website:** [run-as-daemon.ru](https://run-as-daemon.ru)

This project is open-source. See the repository for license details.

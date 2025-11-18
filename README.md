# MikroTik SNMP Zabbix Templates (64-bit Counters)

Production-ready Zabbix templates for MikroTik RouterOS with 64-bit interface counters, supporting SNMPv2c and SNMPv3.

English | [Русский](README.ru.md)

---

## About the Maintainer

**Ranas Mukminov** is a DevOps/SRE and network engineer specializing in:

- Monitoring and observability: Zabbix, Prometheus, Grafana, Loki
- Network monitoring: MikroTik, Cisco, Juniper, and other network equipment
- Automation and orchestration: Ansible, Docker, Kubernetes

**Contacts:**
- Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- GitHub: [ranas-mukminov](https://github.com/ranas-mukminov)
- Telegram: [@run_as_daemon](https://t.me/run_as_daemon)

---

## What This Repository Is

This repository provides Zabbix monitoring templates for MikroTik RouterOS devices with a focus on accurate traffic measurement using 64-bit interface counters. The templates support both SNMPv2c and SNMPv3 protocols and have been tested with modern Zabbix versions (7.x and 6.0 LTS).

**Key features:**

- 64-bit interface counters (ifHCInOctets/ifHCOutOctets) prevent counter wrapping on high-speed links
- Automatic interface discovery with flexible filtering
- System health monitoring: CPU, memory, temperature, voltage
- Network metrics: traffic, errors, discards, broadcast/multicast packets
- Routing protocol monitoring: OSPF neighbors, BGP peers
- Configurable thresholds via macros
- Comprehensive alerting with trigger hysteresis to reduce false positives

---

## Repository Structure

```text
.
├── template_mikrotik_snmpv2c_advanced_zbx72.xml
├── template_mikrotik_snmpv2c_zbx72_uuid32.xml
├── template_mikrotik_snmpv3_advanced_zbx72.xml
├── node-exporter-full-stack/
├── examples/
├── tests/
├── CHANGELOG.md
└── README.md / README.ru.md
```

**Available templates:**

| File                                         | Protocol | Zabbix | Notes                        |
| -------------------------------------------- | -------- | ------ | ---------------------------- |
| template_mikrotik_snmpv2c_advanced_zbx72.xml | SNMPv2c  | 7.2+   | Advanced template, 64-bit IF |
| template_mikrotik_snmpv2c_zbx72_uuid32.xml   | SNMPv2c  | 7.2+   | Basic template, UUID-based   |
| template_mikrotik_snmpv3_advanced_zbx72.xml  | SNMPv3   | 7.2+   | Advanced, secure SNMPv3      |

---

## Requirements

**Zabbix:**
- Server 7.2+ (also works with 7.x and 6.0 LTS with small adjustments if needed)

**MikroTik RouterOS:**
- Version 6.x or 7.x (7.x recommended for best feature support)

**SNMP:**
- SNMPv2c for 64-bit counters
- SNMPv3 support available via dedicated template

**Network:**
- Zabbix Server or Proxy must be able to reach MikroTik on UDP port 161

---

## Quick Start

### Enable SNMP on MikroTik (SNMPv2c)

Connect to your MikroTik device and configure SNMP:

```bash
/snmp
set enabled=yes contact="admin@example.com" location="DataCenter-A"

/snmp community
set [find default=yes] name="MySecureCommunity" addresses=10.0.0.100/32
```

Add a firewall rule to allow SNMP from your Zabbix server:

```bash
/ip firewall filter
add chain=input protocol=udp dst-port=161 src-address=10.0.0.100 \
    action=accept comment="Allow SNMP from Zabbix"
```

Test SNMP access from your Zabbix server:

```bash
snmpwalk -v2c -c MySecureCommunity <mikrotik-ip> system
```

### Import Template into Zabbix

1. Log in to Zabbix web interface
2. Navigate to **Configuration → Templates**
3. Click **Import**
4. Select the template file: `template_mikrotik_snmpv2c_advanced_zbx72.xml`
5. Enable the following import options:
   - Create new
   - Update existing
   - Delete missing (if updating an existing template)
6. Click **Import**

The template will appear as `Template MikroTik SNMPv2c Advanced (Production)` under **Templates/Network devices**.

### Link Template to MikroTik Host

1. Go to **Configuration → Hosts**
2. Click **Create host** or select an existing host
3. Configure host settings:
   - **Host name:** `mikrotik-router-01`
   - **Groups:** `Routers` (or create a new group)
4. Add an SNMP interface:
   - **Type:** SNMP
   - **IP address:** Your MikroTik IP (e.g., `192.168.1.1`)
   - **Port:** `161`
   - **SNMP version:** SNMPv2
   - **SNMP community:** `{$SNMP_COMMUNITY}` (leave as macro reference)
5. Switch to the **Templates** tab
6. Link the template: `Template MikroTik SNMPv2c Advanced (Production)`
7. Switch to the **Macros** tab and select **Host macros**
8. Override the SNMP community macro:
   - **Macro:** `{$SNMP_COMMUNITY}`
   - **Value:** `MySecureCommunity` (your actual community string)
9. Click **Add** or **Update**

Wait a few minutes for Zabbix to collect data, then verify in **Monitoring → Latest data** and check for any issues in **Monitoring → Problems**.

---

## What is Monitored

The templates collect comprehensive metrics from MikroTik devices:

**Device health:**
- System uptime
- CPU utilization
- Memory usage (total, used, free)
- Disk usage
- Hardware temperature (where available)
- Power supply voltage

**Network interfaces:**
- RX/TX traffic (inbound/outbound bytes and packets)
- Error counters (input/output errors)
- Discard counters (input/output discards)
- Interface operational and administrative status
- Interface descriptions and aliases
- Interface speed and duplex
- Bandwidth utilization percentage

**Additional metrics** (depending on RouterOS version and template):
- OSPF neighbor states
- BGP peer sessions
- ICMP ping response time and packet loss

The exact set of monitored items depends on your RouterOS version and the specific template you choose. You can inspect all items in Zabbix by viewing the template configuration.

---

## SNMPv3 (Recommended)

For production environments, SNMPv3 with authentication and privacy is strongly recommended over SNMPv2c.

### Configure SNMPv3 on MikroTik

Create an SNMPv3 user with authentication and privacy:

```bash
/snmp community
set [find default=yes] disabled=yes

/snmp
set enabled=yes engine-id=<your-engine-id> contact="admin@example.com"

/snmp user
add name=zabbix_user group=read auth-protocol=SHA1 auth-password="AuthPass123!" \
    encryption-protocol=AES encryption-password="PrivPass123!"
```

### Configure SNMPv3 in Zabbix

1. Import the SNMPv3 template: `template_mikrotik_snmpv3_advanced_zbx72.xml`
2. When configuring the host interface, select:
   - **SNMP version:** SNMPv3
   - **Context name:** (leave empty)
   - **Security name:** `zabbix_user`
   - **Security level:** authPriv
   - **Authentication protocol:** SHA
   - **Authentication passphrase:** `AuthPass123!`
   - **Privacy protocol:** AES
   - **Privacy passphrase:** `PrivPass123!`
3. Link the SNMPv3 template to the host

SNMPv3 encrypts SNMP traffic and prevents unauthorized access to your devices.

---

## Display & Value Mappings in Zabbix

To properly display collected data, configure value mappings and display settings in Zabbix.

### Interface Status Value Mapping

Create a value mapping for interface operational status:

1. Go to **Administration → General → Value mapping**
2. Click **Create value map**
3. Name: `IfOperStatus`
4. Add the following mappings:

   | Value | Mapped to        |
   | ----- | ---------------- |
   | 1     | up               |
   | 2     | down             |
   | 3     | testing          |
   | 4     | unknown          |
   | 5     | dormant          |
   | 6     | notPresent       |
   | 7     | lowerLayerDown   |

5. Save the value mapping

This mapping is used for items like `ifOperStatus[{#IFNAME}]` and `ifAdminStatus[{#IFNAME}]` to display interface states as readable text instead of numeric codes.

### Interface Speed Normalization

To display interface speeds in human-readable units:

1. Edit interface speed items in the template
2. Add a preprocessing step:
   - **Type:** Custom multiplier
   - **Parameters:** `0.000001` (converts bps to Mbps)
3. Set **Units** to `Mbps`
4. For bandwidth utilization items, use calculated items that reference macros:
   - `{$IF_UTIL_WARN}` for warning threshold (e.g., 80%)
   - `{$IF_UTIL_HIGH}` for high threshold (e.g., 90%)

### MikroTik Interface Type Mapping

Create a value mapping for MikroTik-specific interface types:

1. Go to **Administration → General → Value mapping**
2. Click **Create value map**
3. Name: `MikroTik.Interface.Type`
4. Add common mappings:

   | Value | Mapped to |
   | ----- | --------- |
   | 6     | ether     |
   | 24    | vlan      |
   | 53    | pppoe     |
   | 195   | lte       |

5. Extend this list as needed for other interface types

Apply this mapping to items like `mtIfType[{#IFNAME}]` if your template exposes interface type information.

### Traffic Graphs in Bits per Second

To display traffic graphs in bits per second instead of bytes:

1. Keep raw SNMP items collecting data in bytes (no change)
2. When creating or editing graphs:
   - Select the traffic items (inbound/outbound bytes)
   - Apply a **multiplier** of `8` to convert bytes to bits
   - Set **Y axis units** to `bit/s`
3. Alternatively, create calculated items that multiply byte counters by 8

This approach maintains raw byte data for accuracy while displaying familiar bit/s units in graphs.

---

## Troubleshooting

### No data from host

Check the following:
- Verify SNMP is enabled on MikroTik: `/snmp print`
- Test connectivity with snmpwalk from Zabbix server: `snmpwalk -v2c -c YourCommunity <mikrotik-ip> system`
- Confirm community string or SNMPv3 credentials are correct in Zabbix
- Check firewall rules on MikroTik and between Zabbix and MikroTik
- Review Zabbix server logs for SNMP timeout or authentication errors

### No interfaces discovered

Possible causes:
- LLD filters exclude the interfaces you want to monitor
- Interfaces are administratively disabled
- SNMPv2c and 64-bit counters are not available on the device

Solutions:
- Adjust `{$IF.LLD.FILTER.NOT_MATCHES}` macro to include desired interface types
- Set `{$IF.LLD.FILTER.ADMIN_STATUS}` to match both up and down interfaces if needed
- Manually trigger discovery: **Configuration → Hosts → [Host] → Discovery → Execute now**
- Verify interface availability with snmpwalk for IF-MIB

### Traffic spikes or incorrect values

Common causes:
- Counter wrapping (32-bit counters on high-speed links)
- Device reboot resets counters to zero
- Polling interval is too long
- Double polling from multiple Zabbix servers or proxies

Fixes:
- Ensure the template uses 64-bit counters (ifHCInOctets/ifHCOutOctets)
- Verify correct interface speed is detected
- Reduce polling interval for critical interfaces
- Check that only one Zabbix server/proxy is monitoring the device

### SNMP timeouts

Possible issues:
- High CPU load on MikroTik device
- Network latency or packet loss between Zabbix and MikroTik
- Too many SNMP requests at once (check max OIDs per request)
- Firewall or router limiting SNMP traffic

Solutions:
- Increase SNMP timeout in Zabbix host interface configuration
- Reduce polling frequency or distribute load across multiple proxies
- Check network path with ping and traceroute
- Verify MikroTik CPU usage: `/system resource print`
- Adjust bulk request settings in Zabbix if needed

---

## Roadmap

Planned improvements for future releases:

- Detailed metric documentation per template in `docs/` directory
- Example Grafana dashboards for MikroTik metrics (via Zabbix datasource)
- Additional RouterOS device profiles (CCR, CRS, hAP series)
- Continuous testing with new Zabbix and RouterOS releases
- Extended monitoring for wireless interfaces and client statistics
- QoS and queue monitoring templates

See [CHANGELOG.md](CHANGELOG.md) for version history and completed features.

---

## Contributing

Contributions are welcome! To contribute to this project:

1. Open an issue to discuss the change or feature
2. Fork the repository
3. Create a feature branch: `git checkout -b feature/my-improvement`
4. Make your changes and test them on a real MikroTik device
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/my-improvement`
7. Open a Pull Request

**Guidelines for contributors:**
- Do not change existing item keys without a strong reason (breaks existing deployments)
- Document tested Zabbix and RouterOS versions in the PR description
- Ensure XML templates are valid (use `xmllint` or run tests in `tests/`)
- Follow the existing template structure and naming conventions
- Update CHANGELOG.md with your changes

---

## License

This project is shared for personal and lab use with attribution to the maintainer.

For commercial use or deployment, contact the maintainer if you have questions.

**Maintainer:** Ranas Mukminov  
**Website:** [run-as-daemon.ru](https://run-as-daemon.ru)

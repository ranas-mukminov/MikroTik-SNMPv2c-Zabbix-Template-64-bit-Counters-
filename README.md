# MikroTik SNMP Zabbix Templates (64-bit Counters)

Production-ready Zabbix templates for MikroTik RouterOS devices with 64-bit interface counters, SNMPv2c and SNMPv3 support.

**English** | [Русский](README.ru.md)

---

## 👤 About the Maintainer

**Ranas Mukminov**  
DevOps / SRE / Network Engineer

- 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- 💼 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)
- 💬 Telegram: [Contact via website](https://run-as-daemon.ru)

---

## 📖 What is this Repository?

This repository provides **enterprise-grade Zabbix templates** for monitoring MikroTik RouterOS devices via SNMP. The templates focus on accurate network interface monitoring using **64-bit counters** (ifHC*) to prevent counter wraps on high-speed interfaces.

Key features:
- **64-bit interface counters** (ifHCInOctets, ifHCOutOctets) for accurate traffic measurement on 1G+ links
- **SNMPv2c and SNMPv3** template variants for different security requirements
- **Comprehensive monitoring**: system health (CPU, memory, temperature), interface metrics (traffic, errors, discards, status), and hardware inventory
- **Compatible with Zabbix 7.x and 6.0 LTS** with minimal adjustments
- **RouterOS 6.x and 7.x support** with MikroTik-specific OIDs

---

## 📁 Repository Structure

```
MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-/
├── template_mikrotik_snmpv2c_advanced_zbx72.xml    # Main SNMPv2c template (advanced)
├── template_mikrotik_snmpv2c_zbx72_uuid32.xml      # SNMPv2c template (UUID32 variant)
├── template_mikrotik_snmpv3_advanced_zbx72.xml     # SNMPv3 template (recommended)
├── examples/
│   ├── mikrotik_snmp_config.rsc                    # RouterOS SNMP configuration script
│   ├── zabbix_host_config_example.md               # Zabbix host setup guide
│   └── README.md                                    # Examples documentation
├── tests/                                           # Template validation tests
├── node-exporter-full-stack/                       # Optional Prometheus integration
├── CHANGELOG.md                                     # Version history
├── README.md                                        # This file
└── README.ru.md                                     # Russian documentation
```

### Available Templates

| File | Protocol | Zabbix Version | Description |
|------|----------|----------------|-------------|
| `template_mikrotik_snmpv2c_advanced_zbx72.xml` | SNMPv2c | 7.2+ | Full-featured template with system health, interface monitoring, hardware sensors |
| `template_mikrotik_snmpv2c_zbx72_uuid32.xml` | SNMPv2c | 7.2+ | Simplified template with UUID32 compatibility |
| `template_mikrotik_snmpv3_advanced_zbx72.xml` | SNMPv3 | 7.2+ | Secure template with authentication and encryption (recommended for production) |

---

## ⚙️ Requirements

### Zabbix Server
- **Zabbix 7.2+** (recommended)
- **Zabbix 6.0 LTS** (compatible with minor template adjustments)

### MikroTik RouterOS
- **RouterOS 7.x** (recommended)
- **RouterOS 6.x** (supported, but 7.x recommended for better SNMP stability)

### SNMP Configuration
- **SNMPv2c**: Simple community-based authentication (suitable for isolated networks)
- **SNMPv3**: Authentication (SHA/MD5) + encryption (AES/DES) - **recommended for production**
- SNMP configuration is done on the MikroTik device (host-side), templates remain the same

### Network Requirements
- UDP port **161** must be reachable from Zabbix server/proxy to MikroTik device
- Firewall rules on MikroTik should allow SNMP only from trusted Zabbix server IP

---

## 🚀 Quick Start

### Step 1: Enable SNMP on MikroTik

#### SNMPv2c Configuration (Basic)

Connect to your MikroTik via terminal and run:

```routeros
# Enable SNMP service
/snmp set enabled=yes contact="admin@example.com" location="DataCenter-1"

# Configure SNMP community with IP restriction
# SECURITY: Change "MySecureString123!" to a strong random string
# SECURITY: Change "10.0.0.100" to your Zabbix server IP
/snmp community
set [find default=yes] name="MySecureString123!" addresses=10.0.0.100/32 read-access=yes write-access=no

# Add firewall rule to restrict SNMP access
/ip firewall filter
add chain=input protocol=udp dst-port=161 src-address=10.0.0.100/32 action=accept comment="Allow SNMP from Zabbix"
add chain=input protocol=udp dst-port=161 action=drop comment="Drop all other SNMP"
```

**For complete configuration scripts**, see [`examples/mikrotik_snmp_config.rsc`](examples/mikrotik_snmp_config.rsc).

### Step 2: Import Template into Zabbix

1. Open Zabbix web interface
2. Navigate to **Configuration** → **Templates**
3. Click **Import** button
4. Choose the XML template file (e.g., `template_mikrotik_snmpv2c_advanced_zbx72.xml`)
5. Review import options and click **Import**
6. Confirm the template appears in the templates list

### Step 3: Link Template to MikroTik Host

1. Go to **Configuration** → **Hosts**
2. Create a new host or edit existing MikroTik host
3. Configure host parameters:
   - **Host name**: `mikrotik-router-01` (or your device name)
   - **Groups**: Create/select `MikroTik Routers` group
   - **Interfaces**: Add **SNMP** interface
     - **IP address**: Your MikroTik management IP
     - **Port**: 161
     - **SNMP version**: SNMPv2
     - **SNMP community**: `{$SNMP_COMMUNITY}` (or enter your community string)
4. Go to **Templates** tab
5. Click **Select** and choose the imported template
6. Click **Add** and then **Update**

### Step 4: Verify Data Collection

1. Wait 2-3 minutes for initial data collection
2. Navigate to **Monitoring** → **Latest data**
3. Filter by your MikroTik host
4. Check for interface traffic, system uptime, CPU, and memory metrics
5. Go to **Monitoring** → **Problems** to verify triggers are working

**Detailed configuration guide**: [`examples/zabbix_host_config_example.md`](examples/zabbix_host_config_example.md)

---

## 📊 What is Monitored

### System Health
- **Uptime**: Device uptime tracking with reboot detection
- **CPU**: Processor utilization percentage (warning at 70%, critical at 90%)
- **Memory**: Total, used, free memory with utilization percentage
- **Disk**: Storage usage (where applicable)
- **Temperature**: System temperature sensor (MikroTik-specific OID)
- **Voltage**: System voltage monitoring (MikroTik-specific OID)

### Network Interfaces (64-bit Counters)
- **Traffic**: Inbound/outbound octets (bytes) using ifHCInOctets/ifHCOutOctets
- **Bandwidth Utilization**: Calculated percentage of interface capacity
- **Interface Speed**: Configured speed (ifHighSpeed) for capacity planning
- **Operational Status**: up/down/testing/unknown/dormant/notPresent/lowerLayerDown
- **Administrative Status**: Configured admin state
- **Errors**: Inbound/outbound errors per interface
- **Discards**: Dropped packets due to buffer overflows
- **Broadcast/Multicast**: Storm detection with configurable thresholds

### Hardware Inventory
- **RouterOS Version**: Operating system version (auto-discovered)
- **Device Serial Number**: Hardware serial (MikroTik-specific OID)
- **System Name**: Configured hostname (sysName)
- **System Location**: Physical location (sysLocation)
- **System Contact**: Contact information (sysContact)

### Low-Level Discovery
- **Interface Discovery**: Automatic discovery of all network interfaces
- **Interface Filtering**: Exclude loopback, disabled, or specific interfaces via regex macros

---

## 🔐 SNMPv3 Configuration Example

SNMPv3 provides authentication and encryption, making it **recommended for production environments**.

### MikroTik Configuration

```routeros
# Enable SNMP service
/snmp set enabled=yes contact="admin@example.com" location="DataCenter-1" trap-version=3

# Create SNMPv3 user with authentication and encryption
# SECURITY: Change passwords to strong random strings (minimum 8 characters)
# SECURITY: Change "10.0.0.100" to your Zabbix server IP
/snmp community
add name=zabbix_monitor \
    authentication-protocol=SHA1 \
    encryption-protocol=AES \
    authentication-password="Your_Auth_Password_Min8Chars!" \
    encryption-password="Your_Priv_Password_Min8Chars!" \
    addresses=10.0.0.100/32 \
    read-access=yes \
    write-access=no

# Add firewall rule to restrict SNMP access
/ip firewall filter
add chain=input protocol=udp dst-port=161 src-address=10.0.0.100/32 action=accept comment="Allow SNMP from Zabbix"
add chain=input protocol=udp dst-port=161 action=drop comment="Drop all other SNMP"
```

### Zabbix Host Configuration

When creating the host in Zabbix:

1. **SNMP Interface Settings**:
   - **SNMP version**: SNMPv3
   - **Context name**: (leave empty)
   - **Security name**: `zabbix_monitor`
   - **Security level**: authPriv

2. **Authentication Settings**:
   - **Authentication protocol**: SHA
   - **Authentication passphrase**: `Your_Auth_Password_Min8Chars!`

3. **Privacy Settings**:
   - **Privacy protocol**: AES
   - **Privacy passphrase**: `Your_Priv_Password_Min8Chars!`

### Testing SNMPv3 from Zabbix Server

```bash
# Test SNMPv3 connection
snmpwalk -v3 -l authPriv \
  -u zabbix_monitor \
  -a SHA -A "Your_Auth_Password_Min8Chars!" \
  -x AES -X "Your_Priv_Password_Min8Chars!" \
  <mikrotik-ip> system

# Test specific OID (system uptime)
snmpget -v3 -l authPriv \
  -u zabbix_monitor \
  -a SHA -A "Your_Auth_Password_Min8Chars!" \
  -x AES -X "Your_Priv_Password_Min8Chars!" \
  <mikrotik-ip> SNMPv2-MIB::sysUpTime.0
```

---

## 🔧 Display & Value Mappings in Zabbix

Proper value mappings and preprocessing make metrics human-readable and actionable.

### Interface Operational Status Mapping

Create a value mapping for interface status:

**Value Map Name**: `IfOperStatus`

| Value | Mapped to |
|-------|-----------|
| 1 | up |
| 2 | down |
| 3 | testing |
| 4 | unknown |
| 5 | dormant |
| 6 | notPresent |
| 7 | lowerLayerDown |

**How to apply**:
1. Go to **Configuration** → **Templates** → Your template
2. Find item `ifOperStatus[{#IFNAME}]`
3. In item settings, set **Show value**: `IfOperStatus`
4. This also applies to `ifAdminStatus[{#IFNAME}]`

### Human-Readable Interface Speed

Convert interface speed from bps to Mbps:

**Item**: `ifHighSpeed[{#IFNAME}]`
- **Preprocessing**: Custom multiplier → `0.000001` (converts bps to Mbps)
- **Units**: `Mbps`
- **Value type**: Numeric (float)

Result: Interface speed displays as "1000 Mbps" instead of "1000000000"

### MikroTik Interface Type Mapping

Create a value mapping for MikroTik-specific interface types:

**Value Map Name**: `MikroTik.Interface.Type`

| Value | Mapped to |
|-------|-----------|
| 6 | ethernetCsmacd |
| 24 | softwareLoopback |
| 53 | propVirtual |
| 131 | tunnel |
| 135 | l2vlan |
| 136 | l3ipvlan |
| 244 | pppoe |

**Apply to item**: `ifType[{#IFNAME}]`

### Bandwidth Utilization Triggers

Use macros to define thresholds for interface utilization:

**Recommended Macros**:
- `{$IF_UTIL_WARN}` = `70` (Warning at 70% utilization)
- `{$IF_UTIL_HIGH}` = `90` (Critical at 90% utilization)
- `{$IF_ERROR_RATE_WARN}` = `1` (Warning on errors/discards per second)

**Example Trigger Expression** (Inbound utilization warning):
```
avg(/Template/ifHCInOctets[{#IFNAME}],5m) / ifHighSpeed[{#IFNAME}] * 8 * 100 > {$IF_UTIL_WARN}
```

**Example Trigger Expression** (Error rate warning):
```
rate(/Template/ifInErrors[{#IFNAME}],5m) > {$IF_ERROR_RATE_WARN}
```

### Preprocessing Pipeline Example

**Item**: Interface inbound traffic (bps)

1. **Change per second**: Convert cumulative counter to rate
2. **Custom multiplier**: `8` (convert bytes to bits)
3. **Units**: `bps`

**Item**: Percentage calculations

1. **Calculated item formula**: `(last(//ifHCInOctets[{#IFNAME}]) / last(//ifHighSpeed[{#IFNAME}])) * 100`
2. **Units**: `%`

### Host Macros for Customization

Define macros at host level to customize thresholds per device:

| Macro | Default | Description |
|-------|---------|-------------|
| `{$SNMP_COMMUNITY}` | `CHANGE_ME_SNMPV2C` | SNMPv2c community string |
| `{$CPU_UTIL_WARN}` | `70` | CPU utilization warning threshold (%) |
| `{$CPU_UTIL_CRIT}` | `90` | CPU utilization critical threshold (%) |
| `{$MEM_UTIL_WARN}` | `80` | Memory utilization warning threshold (%) |
| `{$MEM_UTIL_CRIT}` | `95` | Memory utilization critical threshold (%) |
| `{$TEMP_WARN}` | `60` | Temperature warning threshold (°C) |
| `{$TEMP_CRIT}` | `75` | Temperature critical threshold (°C) |
| `{$IF_UTIL_WARN}` | `70` | Interface utilization warning (%) |
| `{$IF_UTIL_HIGH}` | `90` | Interface utilization critical (%) |
| `{$IF_ERROR_RATE_WARN}` | `1` | Interface error rate warning (errors/sec) |
| `{$IFCONTROL}` | `1` | Interface discovery filter (1=enabled) |

**Override at host level**: Configuration → Hosts → Your host → Macros tab

---

## 🛠️ Troubleshooting

### No Data from Host

**Symptoms**: Items show "No data" or "Not supported"

**Solutions**:
1. **Test SNMP connectivity** from Zabbix server:
   ```bash
   snmpwalk -v2c -c YourCommunity <mikrotik-ip> system
   ```
2. **Check firewall rules** on MikroTik:
   ```routeros
   /ip firewall filter print where dst-port=161
   ```
3. **Verify SNMP is enabled** on MikroTik:
   ```routeros
   /snmp print
   ```
4. **Check SNMP community/credentials** match between MikroTik and Zabbix host settings

### Interfaces Not Discovered

**Symptoms**: Low-Level Discovery finds no interfaces or missing expected interfaces

**Solutions**:
1. **Check LLD rules**: Configuration → Templates → Discovery rules → Interface discovery
2. **Review interface filters**: Check macros like `{$IFCONTROL}`, `{$NET.IF.IFNAME.MATCHES}`, `{$NET.IF.IFNAME.NOT_MATCHES}`
3. **Verify SNMP version**: Ensure host SNMP version matches template expectations
4. **Test interface OID manually**:
   ```bash
   snmpwalk -v2c -c YourCommunity <mikrotik-ip> ifDescr
   ```
5. **Check RouterOS version**: Some older versions have limited SNMP support

### Traffic Spikes or Weird Values

**Symptoms**: Unrealistic traffic graphs, sudden spikes, or negative values

**Solutions**:
1. **Ensure 64-bit counters are used**: Templates use `ifHCInOctets`/`ifHCOutOctets` (64-bit) instead of `ifInOctets`/`ifOutOctets` (32-bit)
2. **Check for counter wraps**: 32-bit counters wrap at ~4GB on high-speed links
3. **Verify no overlapping templates**: Multiple templates collecting same metrics can cause conflicts
4. **Review preprocessing**: Ensure "Change per second" is applied to cumulative counters
5. **Check RouterOS SNMP agent**: Update to latest stable RouterOS if issues persist

### SNMP Timeouts

**Symptoms**: Frequent "SNMP timeout" errors in Zabbix

**Solutions**:
1. **Increase SNMP timeout**: Host → Interfaces → SNMP → Timeout (default 3s, try 5-10s)
2. **Check network latency**: High latency or packet loss affects SNMP response time
3. **Reduce polling frequency**: Adjust item intervals if device is under heavy load
4. **MikroTik CPU load**: High CPU usage on MikroTik can delay SNMP responses

### High CPU Usage on MikroTik

**Symptoms**: SNMP queries cause CPU spikes on MikroTik

**Solutions**:
1. **Increase item update intervals**: Change from 1m to 2m or 5m for less critical metrics
2. **Disable unneeded discovery rules**: Comment out unnecessary LLD rules
3. **Use SNMPv2c instead of v3** (if security permits): v3 encryption adds CPU overhead
4. **Update RouterOS**: Newer versions have improved SNMP performance

---

## 🗺️ Roadmap

### Planned Features
- [ ] Detailed metric documentation per template item
- [ ] Example Grafana dashboards for MikroTik visualization
- [ ] Extended SNMPv3 examples (different auth/priv combinations)
- [ ] RouterOS 8.x compatibility testing (when released)
- [ ] Multi-vendor SNMP template collection
- [ ] Zabbix 7.4+ LTS template optimization
- [ ] Integration with MikroTik API as alternative to SNMP
- [ ] Automated template validation CI/CD pipeline

### Under Consideration
- SNMP trap receiver configuration examples
- Wireless interface monitoring templates
- BGP/OSPF routing protocol monitoring
- Queue and QoS monitoring templates
- PPPoE server monitoring
- CAPsMAN wireless controller templates

**Suggestions welcome!** Open an issue to discuss new features or improvements.

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Update templates (XML files)
   - Add/improve documentation
   - Fix bugs or issues
4. **Test your changes**:
   - Import templates into test Zabbix instance
   - Verify monitoring works on test MikroTik device
   - Document tested versions (Zabbix X.Y, RouterOS Z.W)
5. **Commit with clear messages**: `git commit -m "Add: SNMPv3 example for RouterOS 7.x"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**: Describe your changes and testing environment

### Contribution Guidelines

- **Describe tested environment** in PR: Zabbix version, RouterOS version, device model
- **Follow existing template structure**: Keep naming conventions consistent
- **Update documentation**: If adding features, update README.md and README.ru.md
- **Security first**: Never commit real credentials or IP addresses
- **Keep it simple**: Prefer clarity over cleverness

### What to Contribute

- New template variants (different Zabbix versions, specialized use cases)
- Bug fixes for template items or triggers
- Documentation improvements (typos, clarity, translations)
- Example configurations and use cases
- Troubleshooting tips from real-world experience

---

## 📄 License

This project is provided for **personal and commercial use** without restriction.

**Conditions**:
- Use at your own risk; no warranties provided
- Attribution appreciated but not required
- Feel free to modify and distribute
- Not responsible for any issues arising from template usage

**Best Practices**:
- Always test templates in non-production environment first
- Backup your Zabbix configuration before importing new templates
- Review template items and triggers for your specific needs
- Keep templates updated with latest Zabbix and RouterOS versions

---

## 💬 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-/discussions)
- **Professional Services**: [run-as-daemon.ru](https://run-as-daemon.ru)

For professional consulting on Zabbix deployment, MikroTik network design, or enterprise monitoring solutions, visit [run-as-daemon.ru](https://run-as-daemon.ru).

---

**Made with ❤️ by [Ranas Mukminov](https://github.com/ranas-mukminov)**

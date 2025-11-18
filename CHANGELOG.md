# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 🧪 `tests/run_checks.sh` helper to run XML validation for all templates in one command

### Changed
- 📚 `README.md` now includes a post-import verification checklist referencing the new static checks
- 📚 `tests/README.md` documents how to run the aggregated validation script

## [2.0.0] - 2025-01-16

### 🎉 Major Release - Production-Ready Templates

This is a complete rewrite of the templates with enterprise-grade features and security improvements.

### Added

#### Security
- ✅ **SNMPv3 template** with authentication (SHA/MD5) and encryption (AES/DES)
- ✅ **Secure defaults**: Changed default community from "public" to "CHANGE_ME_SNMPV2C" to prevent accidental production deployment
- ✅ **Security documentation** with SNMPv2c mitigation strategies and SNMPv3 configuration guide

#### System Monitoring
- ✅ **CPU monitoring** - utilization percentage with warning/critical triggers
- ✅ **Memory monitoring** - total, used, and calculated utilization percentage
- ✅ **Hardware health monitoring**:
  - System temperature (MikroTik-specific OID)
  - System voltage (MikroTik-specific OID)
  - Temperature and voltage triggers
- ✅ **Inventory collection**:
  - RouterOS version (MikroTik-specific OID)
  - Device serial number (MikroTik-specific OID)
  - System name (sysName)
  - System location (sysLocation)
  - System contact (sysContact)

#### Network Monitoring
- ✅ **Packet discard monitoring** - ifInDiscards/ifOutDiscards for buffer overflow detection
- ✅ **Broadcast/multicast monitoring** - storm detection with configurable threshold
- ✅ **Bandwidth utilization** - calculated items showing % of interface capacity
- ✅ **Interface configured speed** - ifHighSpeed for capacity planning
- ✅ **Value mappings** for operational status (up/down/testing/etc.)

#### Routing Protocol Monitoring
- ✅ **OSPF neighbor discovery** - automatic adjacency monitoring
- ✅ **BGP peer discovery** - session state and prefix tracking
- ✅ **Protocol state triggers** - alerts for non-Full OSPF neighbors and non-Established BGP peers
- ✅ **Value mappings** for OSPF and BGP states

#### Availability Monitoring
- ✅ **ICMP ping monitoring** - basic reachability check
- ✅ **ICMP response time** - latency tracking
- ✅ **ICMP packet loss** - quality monitoring with configurable threshold

#### Visualization
- ✅ **Graph prototypes** for all discovered interfaces:
  - Traffic graphs (inbound/outbound bandwidth)
  - Bandwidth utilization graphs (percentage)
  - Errors and discards graphs
  - Broadcast/multicast traffic graphs

#### Configuration & Usability
- ✅ **Configurable polling intervals** via macros (`{$IF.POLL.INTERVAL}`, `{$IF.DISCOVERY.INTERVAL}`)
- ✅ **Comprehensive macro set** for all thresholds (CPU, memory, temperature, voltage, errors, discards, broadcast)
- ✅ **Modern tag structure** - updated to Zabbix 7.0 standards (class, target, component)
- ✅ **Trigger dependencies** - interface down triggers depend on ICMP ping to prevent alert storms
- ✅ **Hysteresis on triggers** - link down requires 2-minute confirmation to avoid flapping alerts
- ✅ **Manual close option** on persistent triggers
- ✅ **Detailed descriptions** on all items, triggers, and macros

#### Documentation
- ✅ **Comprehensive README.md** with:
  - Quick start guide (5-minute setup)
  - Security best practices (SNMPv2c and SNMPv3)
  - Complete macro reference table
  - Monitored metrics list
  - Trigger reference with severities
  - Troubleshooting guide
  - Customization examples
- ✅ **CHANGELOG.md** - this file
- ✅ **Example configurations**:
  - MikroTik SNMP configuration script
  - Zabbix host setup guide
  - Dashboard JSON template
- ✅ **Validation tests**:
  - XML validation script
  - OID testing script
  - README with testing guide
- ✅ **CI/CD pipeline** - GitHub Actions for automatic XML validation

#### Project Structure
- ✅ **.gitignore** for project cleanliness
- ✅ **examples/** directory with practical configuration samples
- ✅ **tests/** directory with validation scripts

### Changed

#### Template Structure
- 🔄 **Template group** changed from "Templates" to "Templates/Network devices" (Zabbix 7.0 best practice)
- 🔄 **Tag structure** updated from "Application" tags to modern "class/target/component" tags
- 🔄 **Discovery interval** default changed from 1h to 30m for better responsiveness
- 🔄 **Interface filter** enhanced to exclude more virtual interfaces (added eoip, 6to4)
- 🔄 **Error threshold** default remains 1 error/sec (conservative)
- 🔄 **History retention** standardized at 7d for metrics, 30d for status/text items

#### Triggers
- 🔄 **Interface down trigger** now includes:
  - Hysteresis (requires 2 status checks over 2 minutes)
  - Recovery expression for clean state transitions
  - Dependency on ICMP ping trigger
  - Manual close option
- 🔄 **Error rate trigger** now checks max(5m) instead of instantaneous values
- 🔄 **All resource triggers** use multi-level severity (warning at 80%, critical at 90%)

#### Macros
- 🔄 **`{$SNMP_COMMUNITY}`** default changed from "public" to "CHANGE_ME_SNMPV2C"
- 🔄 **Discovery filters** made more comprehensive and documented
- 🔄 **All thresholds** now configurable via macros (previously hardcoded)

### Fixed
- 🐛 **Counter wrapping** - ensured all bandwidth items use 64-bit counters (ifHCInOctets/ifHCOutOctets)
- 🐛 **Unit consistency** - all bandwidth metrics in bps, all memory metrics in bytes
- 🐛 **Value type corrections** - operational status changed from FLOAT to UNSIGNED
- 🐛 **Preprocessing order** - CHANGE_PER_SECOND before MULTIPLIER for accurate rate calculation
- 🐛 **Trends** disabled (trends=0) for text items and status items
- 🐛 **UUID uniqueness** - all UUIDs regenerated to ensure no conflicts

### Security

#### Breaking Changes
- ⚠️ **Default SNMP community changed** from "public" to "CHANGE_ME_SNMPV2C"
  - **Impact**: Templates will not work without explicitly configuring community string
  - **Rationale**: Prevents accidental production deployment with insecure defaults
  - **Migration**: Override `{$SNMP_COMMUNITY}` macro at host level with your actual community string

#### Recommendations
- 🔒 Use SNMPv3 template for production environments
- 🔒 Restrict SNMP access by source IP on MikroTik
- 🔒 Use strong, randomly generated community strings for SNMPv2c
- 🔒 Place monitoring on isolated management VLAN

### Deprecated
- ⚠️ **Original template** (template_mikrotik_snmpv2c_zbx72_uuid32.xml) is now "Legacy - Basic"
  - Still functional and maintained for compatibility
  - Recommended to migrate to Advanced template for production use

### Performance Improvements
- ⚡ **Reduced SNMP load** with optimized polling intervals
- ⚡ **Discovery efficiency** with smart filtering (fewer discovered items)
- ⚡ **Preprocessing** done on Zabbix server (reduces database writes)
- ⚡ **Calculated items** for bandwidth utilization (no additional SNMP polls)

---

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic interface discovery with 64-bit counters
- Inbound/outbound bandwidth monitoring
- Interface operational status monitoring
- Inbound/outbound error monitoring
- Interface alias and configured speed
- Basic triggers for interface down and high error rate
- System uptime and description items
- Smart interface filtering (exclude loopback, virtual, vlan, gre, pppoe)

### Features
- ✅ 64-bit counter support (ifHCInOctets, ifHCOutOctets)
- ✅ CHANGE_PER_SECOND preprocessing
- ✅ Byte to bit conversion (x8 multiplier)
- ✅ Macro-based SNMP community configuration
- ✅ Regex-based interface discovery filters
- ✅ Compatible with Zabbix 7.0+

---

## Version Comparison

| Feature | v1.0 (Basic) | v2.0 (Advanced) |
|---------|--------------|-----------------|
| Interface monitoring | ✅ | ✅ |
| 64-bit counters | ✅ | ✅ |
| CPU/Memory monitoring | ❌ | ✅ |
| Hardware health | ❌ | ✅ (temp/voltage) |
| Discards monitoring | ❌ | ✅ |
| Broadcast/multicast | ❌ | ✅ |
| Bandwidth utilization | ❌ | ✅ (calculated %) |
| OSPF monitoring | ❌ | ✅ |
| BGP monitoring | ❌ | ✅ |
| ICMP monitoring | ❌ | ✅ |
| Graph prototypes | ❌ | ✅ (4 per interface) |
| Value mappings | ❌ | ✅ (status, OSPF, BGP) |
| Trigger hysteresis | ❌ | ✅ |
| Trigger dependencies | ❌ | ✅ |
| SNMPv3 support | ❌ | ✅ (separate template) |
| Comprehensive docs | ❌ | ✅ |
| Security hardening | ❌ | ✅ |

---

## Upgrade Guide (v1.0 → v2.0)

### For Existing v1.0 Users

#### Option 1: Side-by-side deployment (Recommended)
1. Import v2.0 Advanced template (different template name, no conflicts)
2. Create new test host with v2.0 template
3. Verify all metrics collecting correctly
4. Migrate production hosts one by one
5. Remove v1.0 template when no longer used

#### Option 2: Direct upgrade (Advanced users)
1. Export your current v1.0 template configuration
2. Note all customized macros
3. Import v2.0 Advanced template with "Update existing" enabled
4. **IMPORTANT**: Configure `{$SNMP_COMMUNITY}` macro (default changed!)
5. Review new triggers and disable unwanted ones
6. Check discovery rules - some interfaces may newly appear due to filter changes

### Breaking Changes to Review
- Default SNMP community changed - **must configure macro**
- Template group changed - may affect permissions
- Additional items added - may increase database size
- ICMP items added - ensure Zabbix can ping devices
- New triggers - may generate new alerts

### Recommended Post-Upgrade Actions
1. Review and tune threshold macros for your environment
2. Create custom dashboards using new graph prototypes
3. Configure email/Slack notifications for new triggers
4. Document your macro customizations
5. Update monitoring runbooks

---

## Roadmap

### Planned for v2.1
- 🔮 QoS queue monitoring
- 🔮 Wireless interface discovery and metrics
- 🔮 PPPoE client/server monitoring
- 🔮 VPN tunnel monitoring (IPsec, L2TP, OpenVPN)
- 🔮 VRRP/CARP state monitoring
- 🔮 Firewall connection tracking
- 🔮 DHCP server statistics
- 🔮 NTP client monitoring

### Planned for v3.0
- 🔮 Zabbix HTTP agent items for RouterOS REST API
- 🔮 Active agent template (Zabbix agent on RouterOS via Container)
- 🔮 Pre-built dashboards (Network Overview, Capacity Planning, Troubleshooting)
- 🔮 Pre-configured alert escalations
- 🔮 Integration with external systems (Grafana, Prometheus exporter)

---

## Contributing

See [README.md](README.md#contributing) for contribution guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) file

---

**Questions?** Open an issue on GitHub or contact [run-as-daemon.ru](https://run-as-daemon.ru)

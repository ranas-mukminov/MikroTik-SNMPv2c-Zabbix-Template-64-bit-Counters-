# 📡 MikroTik SNMP Zabbix Templates (64-bit Counters)

[![Zabbix](https://img.shields.io/badge/Zabbix-7.2%2B-red?logo=zabbix)](https://www.zabbix.com/)
[![RouterOS](https://img.shields.io/badge/RouterOS-6.x%20%7C%207.x-blue?logo=mikrotik)](https://mikrotik.com/)
[![SNMP](https://img.shields.io/badge/SNMP-v2c%20%7C%20v3-green)](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol)
[![License](https://img.shields.io/badge/License-Custom-orange)](LICENSE)

Production-ready Zabbix templates for MikroTik RouterOS with 64-bit interface counters, supporting SNMPv2c and SNMPv3.

**English** | [Русский](README.ru.md)

---

## 🎯 Professional Deployment & Support

> **"Defense by design. Speed by default."**

Looking for enterprise-grade MikroTik monitoring deployment? Get **professional assistance** from experienced DevOps/SRE engineers specializing in network infrastructure monitoring.

### 🚀 Why Professional Services?

- ⚡ **Rapid Deployment** - Production-ready in days, not weeks
- 🎯 **Best Practices** - Battle-tested configurations from day one
- 🔒 **Security First** - SNMPv3, network segmentation, compliance-ready
- 📊 **Optimized Performance** - Fine-tuned for large-scale environments
- 🛠️ **Ongoing Support** - 24/7 monitoring and incident response

### 📞 Contact for Professional Services

- 🌐 Website: **[run-as-daemon.ru](https://run-as-daemon.ru)**
- 💬 Telegram: **[@run_as_daemon](https://t.me/run_as_daemon)**
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: **[@ranas-mukminov](https://github.com/ranas-mukminov)**

---

## 📖 Table of Contents

- [What This Repository Is](#-what-this-repository-is)
- [Quick Start](#-quick-start)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Requirements](#-requirements)
- [What is Monitored](#-what-is-monitored)
- [SNMPv3 Configuration](#-snmpv3-recommended)
- [Deployment Options](#-deployment-options)
- [Troubleshooting](#-troubleshooting)
- [Professional Services](#-professional-services)
- [Support Options](#-support-options-comparison)
- [Contributing](#-contributing)
- [Author & Professional Services](#-author--professional-services)

---

## 📋 Quick Start

Get up and running in 5 minutes! Follow these three simple steps:

### 1️⃣ Enable SNMP on MikroTik

```bash
/snmp set enabled=yes contact="admin@example.com" location="DataCenter"
/snmp community set [find default=yes] name="MySecureString" addresses=10.0.0.100/32
/ip firewall filter add chain=input protocol=udp dst-port=161 src-address=10.0.0.100 action=accept
```

### 2️⃣ Import Template in Zabbix

- Go to **Configuration → Templates → Import**
- Select `template_mikrotik_snmpv2c_advanced_zbx72.xml`
- Click **Import**

### 3️⃣ Add Host in Zabbix

- **Configuration → Hosts → Create host**
- Link template: `Template MikroTik SNMPv2c Advanced (Production)`
- Set macro `{$SNMP_COMMUNITY}` = `MySecureString`

✅ **Done!** Data collection starts in ~2 minutes.

📚 **Need more details?** See [QUICKSTART.md](QUICKSTART.md) or [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎯 What This Repository Is

This repository provides **enterprise-grade Zabbix monitoring templates** for MikroTik RouterOS devices with a focus on accurate traffic measurement using 64-bit interface counters. The templates support both SNMPv2c and SNMPv3 protocols and have been tested with modern Zabbix versions (7.x and 6.0 LTS).

### Why 64-bit Counters?

- ✅ **No Counter Wrapping** - 32-bit counters wrap at 4GB, causing data loss on high-speed links
- ✅ **Accurate Measurements** - Essential for 1Gbps+ interfaces
- ✅ **Production Ready** - Used in ISP and enterprise environments

---

## 🚀 Key Features

- ✅ **64-bit Interface Counters** - ifHCInOctets/ifHCOutOctets prevent counter wrapping on high-speed links
- ✅ **Automatic Interface Discovery** - Flexible filtering with customizable macros
- ✅ **System Health Monitoring** - CPU, memory, temperature, voltage, disk usage
- ✅ **Network Metrics** - Traffic, errors, discards, broadcast/multicast packets
- ✅ **Routing Protocol Monitoring** - OSPF neighbors, BGP peer sessions
- ✅ **Configurable Thresholds** - Easy customization via Zabbix macros
- ✅ **Smart Alerting** - Trigger hysteresis to reduce false positives
- ✅ **SNMPv2c & SNMPv3** - Support for both protocols (SNMPv3 recommended)
- ✅ **Production Tested** - Deployed in enterprise and service provider networks

---

## 🏗️ Tech Stack

### Monitoring Platform
- **Zabbix** 7.2+ (compatible with 7.x and 6.0 LTS)
- SNMP polling engine with 64-bit counter support
- Low-level discovery for dynamic interface monitoring
- Advanced trigger expressions with hysteresis

### Network Equipment
- **MikroTik RouterOS** 6.x / 7.x (7.x recommended)
- SNMPv2c and SNMPv3 support
- Standard IF-MIB (RFC 2863) compliance
- MikroTik-specific OIDs for extended metrics

### Protocols & Standards
- **SNMPv2c** - Simple, widely supported (community-based)
- **SNMPv3** - Secure with authentication and encryption
- **IF-MIB** - Industry-standard interface metrics
- **HC-RMON-MIB** - High-capacity 64-bit counters

---

## 📂 Repository Structure

```text
.
├── 📄 template_mikrotik_snmpv2c_advanced_zbx72.xml    # SNMPv2c Advanced (Recommended)
├── 📄 template_mikrotik_snmpv2c_zbx72_uuid32.xml      # SNMPv2c Basic
├── 📄 template_mikrotik_snmpv3_advanced_zbx72.xml     # SNMPv3 Secure
├── 📁 node-exporter-full-stack/                       # Additional monitoring stack
├── 📁 examples/                                        # Configuration examples
├── 📁 tests/                                           # Validation tests
├── 📝 README.md / README.ru.md                        # Documentation
├── 📝 QUICKSTART.md                                   # 3-step quick start guide
├── 📝 DEPLOYMENT.md                                   # Complete deployment guide
├── 📝 SECURITY.md                                     # Security best practices
├── 📝 CONTRIBUTING.md                                 # Contribution guidelines
├── 📝 CODE_OF_CONDUCT.md                              # Community guidelines
└── 📝 CHANGELOG.md                                    # Version history
```

### Available Templates

| File | Protocol | Zabbix | Features |
|------|----------|--------|----------|
| `template_mikrotik_snmpv2c_advanced_zbx72.xml` | SNMPv2c | 7.2+ | ⭐ **Recommended** - Advanced, 64-bit IF, BGP, OSPF |
| `template_mikrotik_snmpv2c_zbx72_uuid32.xml` | SNMPv2c | 7.2+ | Basic template, UUID-based |
| `template_mikrotik_snmpv3_advanced_zbx72.xml` | SNMPv3 | 7.2+ | 🔒 **Secure** - Advanced, encrypted, production-grade |

---

## ✅ Requirements

### Zabbix Server
- **Version:** 7.2 or higher (also works with 7.x and 6.0 LTS)
- **SNMP Support:** Enabled and configured
- **Resources:** Adequate poller processes for device count
- **Network:** Connectivity to MikroTik devices on UDP port 161

### MikroTik RouterOS
- **Version:** 6.x or 7.x (7.x recommended for best feature support)
- **SNMP:** Service enabled with proper configuration
- **Access:** Administrative permissions for configuration
- **Interfaces:** Support for 64-bit counters (most modern devices)

### Network
- **Connectivity:** Zabbix Server/Proxy → MikroTik UDP port 161
- **Latency:** < 100ms recommended for reliable polling
- **Security:** Firewall rules configured (see [SECURITY.md](SECURITY.md))

---

## 📊 What is Monitored

### 🖥️ Device Health

- **System Uptime** - Device availability tracking
- **CPU Utilization** - Processor load monitoring
- **Memory Usage** - RAM utilization (total, used, free)
- **Disk Usage** - Storage space monitoring
- **Hardware Temperature** - Thermal monitoring (where available)
- **Power Supply Voltage** - Power status monitoring

### 🌐 Network Interfaces

- **Traffic Metrics**
  - RX/TX traffic (inbound/outbound bytes and packets)
  - **64-bit counters** for high-capacity links
  - Bits per second calculations
  - Bandwidth utilization percentage

- **Error Counters**
  - Input/output errors
  - Input/output discards
  - Collision detection
  - Interface flaps

- **Interface Status**
  - Operational status (up/down)
  - Administrative status
  - Interface descriptions and aliases
  - Speed and duplex mode

- **Traffic Types**
  - Broadcast packets
  - Multicast packets
  - Unicast packets

### 🔀 Routing Protocols

- **OSPF Monitoring** - Neighbor states and adjacencies
- **BGP Monitoring** - Peer sessions and state tracking
- **Route Counting** - Active routes in routing table

### 🔌 Connectivity

- **ICMP Ping** - Response time and packet loss monitoring
- **Service Availability** - Device reachability alerts

> 📝 **Note:** Exact metric availability depends on your RouterOS version and the specific template used. Inspect the template in Zabbix for full details.

---

## 🔐 SNMPv3 (Recommended)

For production environments, **SNMPv3 with authentication and privacy is strongly recommended** over SNMPv2c.

### Why SNMPv3?

- 🔒 **Encryption** - SNMP traffic is encrypted (AES/DES)
- 🔑 **Authentication** - Prevents unauthorized access (SHA/MD5)
- 🛡️ **Security** - No plaintext community strings
- ✅ **Compliance** - Meets security standards (PCI-DSS, SOC2, etc.)

### Configure SNMPv3 on MikroTik

```bash
# Disable SNMPv2c community
/snmp community set [find default=yes] disabled=yes

# Configure SNMPv3
/snmp set enabled=yes engine-id=<your-engine-id> contact="admin@example.com"

# Create SNMPv3 user with strong security
/snmp user add name=zabbix_user group=read \
    auth-protocol=SHA256 auth-password="StrongAuthPass!2024" \
    encryption-protocol=AES encryption-password="StrongPrivPass!2024"
```

### Configure SNMPv3 in Zabbix

1. Import the SNMPv3 template: `template_mikrotik_snmpv3_advanced_zbx72.xml`
2. When configuring the host interface:
   - **SNMP version:** SNMPv3
   - **Security name:** `zabbix_user`
   - **Security level:** authPriv
   - **Authentication protocol:** SHA or SHA-256
   - **Authentication passphrase:** `StrongAuthPass!2024`
   - **Privacy protocol:** AES
   - **Privacy passphrase:** `StrongPrivPass!2024`
3. Link the SNMPv3 template to the host

📚 **Full security guide:** [SECURITY.md](SECURITY.md)

---

## 🚀 Deployment Options

### Option 1: Quick Deployment (5 minutes)

Perfect for testing or small deployments (1-10 devices).

✅ Manual configuration  
✅ Web UI-based setup  
✅ No automation required  

📖 **Guide:** [QUICKSTART.md](QUICKSTART.md)

---

### Option 2: Standard Deployment (1-2 hours)

Ideal for small to medium deployments (10-50 devices).

✅ Standardized configuration  
✅ Documentation and testing  
✅ Basic automation with scripts  

📖 **Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

### Option 3: Professional Deployment (1-3 days)

Best for large-scale or mission-critical deployments (50+ devices).

✅ Full automation with Ansible/API  
✅ High availability setup  
✅ Custom dashboards and reporting  
✅ Security hardening (SNMPv3, network segmentation)  
✅ Performance optimization  
✅ Team training and documentation  

📞 **Contact:** [run-as-daemon.ru](https://run-as-daemon.ru) for enterprise deployment

---

## 📝 Display & Value Mappings

To properly display collected data, configure value mappings in Zabbix.

### Interface Status Value Mapping

Create a value mapping for interface operational status:

1. Go to **Administration → General → Value mapping**
2. Click **Create value map**, Name: `IfOperStatus`
3. Add mappings:

| Value | Mapped to |
|-------|-----------|
| 1 | up |
| 2 | down |
| 3 | testing |
| 4 | unknown |
| 5 | dormant |
| 6 | notPresent |
| 7 | lowerLayerDown |

### Interface Speed Normalization

Display interface speeds in human-readable units:

1. Edit interface speed items in the template
2. Add preprocessing: **Custom multiplier** → `0.000001` (bps to Mbps)
3. Set **Units** to `Mbps`

### Traffic Graphs in Bits per Second

Display traffic in bits/s instead of bytes:

1. Keep raw SNMP items in bytes
2. When creating graphs, apply multiplier of `8` to convert bytes to bits
3. Set **Y axis units** to `bit/s`

---

## 🔧 Troubleshooting

### No data from host

**Check:**
```bash
snmpwalk -v2c -c YourCommunity <mikrotik-ip> system
```

**Common issues:**
- ❌ SNMP not enabled → `/snmp set enabled=yes` on MikroTik
- ❌ Wrong community → Verify `/snmp community print`
- ❌ Firewall blocking → Check firewall rules
- ❌ Network issue → Test with `ping`

### No interfaces discovered

**Solutions:**
- Adjust `{$IF.LLD.FILTER.NOT_MATCHES}` macro
- Manually trigger: **Configuration → Hosts → Discovery → Execute now**
- Verify interfaces: `/interface print` on MikroTik

### Traffic spikes or incorrect values

**Common causes:**
- Counter wrapping (use 64-bit counters)
- Device reboot (counters reset to zero)
- Polling interval too long
- Double polling from multiple servers

**Fixes:**
- Ensure template uses 64-bit counters (ifHC*)
- Verify correct interface speed detection
- Reduce polling interval for critical interfaces

### SNMP timeouts

**Solutions:**
- Increase SNMP timeout in Zabbix (Configuration → Hosts → Interface)
- Check MikroTik CPU: `/system resource print`
- Reduce polling frequency
- Use Zabbix proxies for distributed load

📚 **More troubleshooting:** [QUICKSTART.md](QUICKSTART.md#-quick-troubleshooting)

---

## 💼 Professional Services

### 🏗️ What We Offer

#### Infrastructure & Monitoring
- 📊 **Network Monitoring Setup** - Zabbix, Prometheus, Grafana deployment
- 🔧 **MikroTik Configuration** - RouterOS optimization and hardening
- 🌐 **High-Load Monitoring** - Scalable architectures for 100+ devices
- 🏢 **Enterprise Solutions** - Multi-site, high-availability setups

#### Security & Hardening
- 🔒 **SNMPv3 Migration** - Secure authentication and encryption
- 🛡️ **Network Hardening** - Firewall rules, access control, segmentation
- 📋 **Compliance** - PCI-DSS, ISO 27001, SOC2 readiness
- 🔐 **Security Audits** - Infrastructure and configuration review

#### Automation & DevOps
- 🤖 **Monitoring as Code** - Ansible, Terraform, API automation
- 🔄 **CI/CD Integration** - Automated template deployment
- 📦 **Infrastructure as Code** - Reproducible, version-controlled configs
- ⚙️ **Custom Integrations** - External systems and workflows

#### Training & Support
- 🎓 **Team Training** - Zabbix, MikroTik, monitoring best practices
- 📚 **Documentation** - Customized runbooks and procedures
- 🛠️ **24/7 Support** - Incident response and troubleshooting
- 💡 **Consulting** - Architecture design and optimization

### 🎯 Professional Deployment Recommendations

| Deployment Size | Recommended Approach | Timeline | Support Level |
|-----------------|---------------------|----------|---------------|
| 1-10 devices | Self-service with docs | 1-2 days | Community |
| 10-50 devices | Standard deployment | 1 week | Email support |
| 50-200 devices | Professional setup | 2-4 weeks | Dedicated support |
| 200+ devices | Enterprise solution | 1-3 months | 24/7 support |

---

## 📊 Support Options Comparison

| Feature | Community | Professional | Enterprise |
|---------|-----------|--------------|------------|
| **Documentation** | ✅ Public docs | ✅ + Custom docs | ✅ + Dedicated docs |
| **Deployment** | ⚙️ Self-service | 🚀 Assisted | 🏢 Fully managed |
| **Configuration** | 📖 Via docs | 🎯 Optimized | 💎 Custom tailored |
| **Response Time** | 🕐 Community (best effort) | ⏱️ 24-48 hours | ⚡ 1-4 hours (24/7) |
| **Security** | 🔓 Basic guidance | 🔒 SNMPv3 setup | 🛡️ Full hardening |
| **Automation** | ❌ Not included | ✅ Basic scripts | ✅ Full IaC |
| **Training** | ❌ Not included | ✅ 1-2 sessions | ✅ Comprehensive |
| **Updates** | 📦 Self-apply | 🔄 Assisted | 🔄 Managed |
| **Price** | Free | $$ Competitive | $$$ Enterprise |

### 📞 Contact for Professional Services

> **"Defense by design. Speed by default."**

- 🌐 Website: **[run-as-daemon.ru](https://run-as-daemon.ru)**
- 💬 Telegram: **[@run_as_daemon](https://t.me/run_as_daemon)**
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: **[@ranas-mukminov](https://github.com/ranas-mukminov)**

---

## 🤝 Contributing

Contributions are welcome! We appreciate bug reports, feature requests, and code contributions.

### How to Contribute

1. 🐛 **Report Bugs** - Open an issue with details
2. 💡 **Suggest Features** - Propose improvements
3. 🔧 **Submit PRs** - Fix bugs or add features
4. 📚 **Improve Docs** - Clarify or translate

### Contribution Guidelines

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before starting
- Follow existing code style and conventions
- Test your changes on real MikroTik devices
- Update documentation and CHANGELOG.md
- Do not change existing item keys without justification

📖 **Full guidelines:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 Code of Conduct

This project follows a Code of Conduct to ensure a welcoming and inclusive community.

- ✅ Be respectful and professional
- ✅ Provide constructive feedback
- ✅ Accept differences in opinion
- ❌ No harassment or discrimination

📖 **Full code:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## 🗺️ Roadmap

Planned improvements for future releases:

- 📖 **Detailed Metric Documentation** - Per-template metric guides
- 📊 **Grafana Dashboards** - Pre-built dashboards for Zabbix datasource
- 🔧 **Device Profiles** - CCR, CRS, hAP series-specific templates
- 🧪 **Automated Testing** - CI/CD for template validation
- 📡 **Wireless Monitoring** - Client statistics and signal strength
- ⚙️ **QoS & Queue Monitoring** - Traffic shaping metrics

See [CHANGELOG.md](CHANGELOG.md) for version history and completed features.

---

## 👨‍💻 Author & Professional Services

### About the Maintainer

**Ranas Mukminov** is a DevOps/SRE and network engineer with extensive experience in:

- 📊 **Monitoring & Observability** - Zabbix, Prometheus, Grafana, Loki, ELK
- 🌐 **Network Monitoring** - MikroTik, Cisco, Juniper, and other equipment
- 🤖 **Automation & Orchestration** - Ansible, Docker, Kubernetes, Terraform
- 🔒 **Security & Compliance** - Network hardening, secure architectures
- 🏗️ **Infrastructure Engineering** - High-availability, scalable systems

### Professional Experience

- ✅ Deployed monitoring for 100+ MikroTik devices in production
- ✅ ISP and enterprise network monitoring projects
- ✅ Custom Zabbix template development and optimization
- ✅ SNMPv3 migration and security hardening
- ✅ Training and consulting for monitoring teams

### Services & Expertise

🏗️ **Infrastructure & Monitoring**  
🔒 **Security & Network Hardening**  
⚙️ **MikroTik Configuration & Optimization**  
🌐 **Network Monitoring Setup** (Zabbix, Prometheus)  
🤖 **Automation** (Ansible, monitoring-as-code)  
📊 **High-Load Network Monitoring**  

### Get in Touch

> **"Defense by design. Speed by default."**

- 🌐 Website: **[run-as-daemon.ru](https://run-as-daemon.ru)**
- 💬 Telegram: **[@run_as_daemon](https://t.me/run_as_daemon)**
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: **[@ranas-mukminov](https://github.com/ranas-mukminov)**

---

## 📄 License

This project is shared for personal and lab use with attribution to the maintainer.

For commercial use or deployment in production, you are welcome to use these templates. If you need customization, professional support, or have questions, please contact the maintainer.

**Maintainer:** Ranas Mukminov  
**Website:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

## 🙏 Acknowledgments

- Thanks to the MikroTik and Zabbix communities for their support
- Contributors who have reported issues and suggested improvements
- Organizations using these templates in production

---

**⭐ If you find this project useful, please star it on GitHub!**

**🔗 Links:**
- [Quick Start Guide](QUICKSTART.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Security Best Practices](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)

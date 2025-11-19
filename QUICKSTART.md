# ⚡ Quick Start Guide

Get MikroTik SNMP monitoring up and running in 3 simple steps!

---

## 🚀 3-Step Deployment

### Step 1: Configure MikroTik (2 minutes)

```bash
# Connect to your MikroTik via SSH or terminal

# Enable SNMP
/snmp set enabled=yes contact="admin@example.com" location="DataCenter"

# Set community string (restrict to Zabbix IP)
/snmp community set [find default=yes] name="MySecureString" addresses=10.0.0.100/32

# Allow SNMP in firewall
/ip firewall filter add chain=input protocol=udp dst-port=161 \
    src-address=10.0.0.100 action=accept comment="Zabbix SNMP"
```

**Replace:**
- `MySecureString` - Your unique community string
- `10.0.0.100` - Your Zabbix server IP

### Step 2: Import Template in Zabbix (1 minute)

1. Download template: `template_mikrotik_snmpv2c_advanced_zbx72.xml`
2. In Zabbix UI: **Configuration → Templates → Import**
3. Select the XML file and click **Import**

### Step 3: Add Host in Zabbix (2 minutes)

1. Go to **Configuration → Hosts → Create host**
2. Fill in:
   - **Host name:** `mikrotik-01`
   - **Groups:** `Routers` (or create new)
3. Add SNMP interface:
   - **Type:** SNMP
   - **IP address:** Your MikroTik IP
   - **SNMP version:** SNMPv2
   - **SNMP community:** `{$SNMP_COMMUNITY}`
4. **Templates tab:** Link `Template MikroTik SNMPv2c Advanced (Production)`
5. **Macros tab:** Set `{$SNMP_COMMUNITY}` = `MySecureString`
6. Click **Add**

**Done!** ✅ Data collection starts in ~2 minutes.

---

## 🎯 Verify It's Working

### Quick Checks

1. **Test SNMP from Zabbix server:**
   ```bash
   snmpwalk -v2c -c MySecureString <mikrotik-ip> system
   ```
   Should return system information.

2. **Check Zabbix data collection:**
   - Go to **Monitoring → Latest data**
   - Filter by your host name
   - Verify data appears for CPU, Memory, Interfaces

3. **View interface discovery:**
   - **Monitoring → Latest data**
   - Filter by host and application "Interfaces"
   - Should see discovered interfaces with traffic data

---

## 🔍 Common Use Cases

### Use Case 1: Basic Router Monitoring

**Scenario:** Monitor a single edge router  
**Template:** `template_mikrotik_snmpv2c_advanced_zbx72.xml`

**Monitors:**
- ✅ System health (CPU, Memory, Uptime)
- ✅ Interface traffic (64-bit counters)
- ✅ Interface errors and discards
- ✅ Basic connectivity (ICMP ping)

**Setup time:** 5 minutes

### Use Case 2: ISP Core Network Monitoring

**Scenario:** Monitor multiple core routers with BGP  
**Template:** `template_mikrotik_snmpv2c_advanced_zbx72.xml`  
**Security:** Use SNMPv3 (`template_mikrotik_snmpv3_advanced_zbx72.xml`)

**Monitors:**
- ✅ All basic metrics
- ✅ BGP peer status
- ✅ OSPF neighbor states
- ✅ High-precision traffic (64-bit essential)

**Recommended:**
- Use Zabbix proxies for distributed monitoring
- Set up custom triggers for BGP/OSPF
- Create dedicated dashboards

**Setup time:** 15 minutes per device (after first)

### Use Case 3: Enterprise Branch Office Monitoring

**Scenario:** Monitor 50+ branch office routers  
**Approach:** Automated deployment with Zabbix API

**Monitors:**
- ✅ System health across all locations
- ✅ WAN interface performance
- ✅ VPN tunnel status (if applicable)
- ✅ Centralized alerting

**Recommended tools:**
- Ansible for MikroTik configuration
- Zabbix API for bulk host import
- Proxy servers per region

**Setup time:** 1 day for initial automation, then 2 minutes per device

### Use Case 4: Data Center Switch Monitoring

**Scenario:** Monitor CRS series switches  
**Template:** `template_mikrotik_snmpv2c_advanced_zbx72.xml`

**Monitors:**
- ✅ All switch ports (auto-discovery)
- ✅ Traffic per interface
- ✅ SFP module status (temperature, voltage)
- ✅ Power supply status

**Tuning:**
- Adjust discovery filters to exclude unused ports
- Set bandwidth utilization thresholds per port type
- Configure port-specific alerts

**Setup time:** 10 minutes

---

## 🛠️ Quick Troubleshooting

### No data from host

**Check:**
```bash
# From Zabbix server
snmpwalk -v2c -c YourCommunity <mikrotik-ip> system
```

**If fails:**
- ❌ SNMP not enabled → `/snmp set enabled=yes` on MikroTik
- ❌ Wrong community → Check `/snmp community print` on MikroTik
- ❌ Firewall blocking → Verify firewall rules on MikroTik
- ❌ Network issue → Check connectivity with `ping`

### Interfaces not discovered

**Solutions:**
- Manually trigger discovery: **Configuration → Hosts → Discovery → Execute now**
- Check discovery filters: Look at `{$IF.LLD.FILTER.MATCHES}` macro
- Verify interfaces are up: `/interface print` on MikroTik

### Wrong traffic values

**Common causes:**
- Using 32-bit counters on high-speed links
  - **Fix:** Use advanced template with 64-bit counters (ifHC*)
- Counter wrap on device reboot
  - **Fix:** Normal behavior, data corrects after next poll
- Incorrect interface speed
  - **Fix:** Zabbix auto-detects from SNMP, verify with `/interface print`

### SNMP timeouts

**Quick fixes:**
- Increase timeout in Zabbix host interface (default 3s → 5s)
- Check MikroTik CPU: `/system resource print`
- Reduce polling frequency if CPU is high
- Use Zabbix proxy closer to MikroTik devices

---

## 📊 Quick Customizations

### Adjust Warning Thresholds

**Via Host Macros:**
1. **Configuration → Hosts → [Your Host] → Macros**
2. Override:
   - `{$IF_UTIL_WARN}` = `80` (interface bandwidth warning %)
   - `{$IF_UTIL_HIGH}` = `90` (interface bandwidth critical %)
   - `{$CPU_UTIL_WARN}` = `75` (CPU warning %)
   - `{$MEMORY_UTIL_WARN}` = `85` (memory warning %)

### Filter Interfaces

**Example: Monitor only uplink ports**
1. **Configuration → Hosts → [Host] → Macros**
2. Add macro: `{$IF.LLD.FILTER.MATCHES}` = `^(ether1|sfp-sfpplus1)$`

**Example: Exclude management interfaces**
1. Add macro: `{$IF.LLD.FILTER.NOT_MATCHES}` = `^(ether10)$`

### Create Custom Dashboard

1. **Monitoring → Dashboards → Create dashboard**
2. Add widgets:
   - **Graph** → Interface traffic for critical links
   - **Problems** → Filtered by your host group
   - **Data overview** → CPU and Memory for all routers
   - **Map** → Network topology (if configured)

---

## 📈 Next Steps

After basic setup, consider:

1. **Security Hardening**
   - Migrate to SNMPv3 (see [SECURITY.md](SECURITY.md))
   - Implement network segmentation for monitoring

2. **Advanced Configuration**
   - Custom triggers for your specific use cases
   - Integration with external alerting (email, Slack, PagerDuty)
   - Custom scripts for automated remediation

3. **Optimization**
   - Fine-tune polling intervals
   - Optimize database performance
   - Implement data retention policies

4. **Scaling**
   - Deploy Zabbix proxies for distributed monitoring
   - Automate device onboarding with Zabbix API
   - Create standardized templates for device types

---

## 🏢 Need Professional Help?

Fast-track your deployment with expert assistance!

### Professional Services

- 🚀 **Rapid Deployment** - Get 100+ devices monitored in days
- 🎯 **Custom Configuration** - Tailored templates for your environment
- 🔧 **Optimization** - Fine-tuned for performance and accuracy
- 🎓 **Training** - Get your team up to speed quickly
- 🛠️ **Ongoing Support** - 24/7 monitoring and incident response

### Why Choose Professional Services?

> **"Defense by design. Speed by default."**

✅ Faster time to value  
✅ Best practices from day one  
✅ Avoid common pitfalls  
✅ Production-ready from start  

### Contact for Quick Professional Setup

- 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- 💬 Telegram: [@run_as_daemon](https://t.me/run_as_daemon)
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)

---

## 📚 More Documentation

- 📖 [Full README](README.md) - Complete documentation
- 🚀 [Deployment Guide](DEPLOYMENT.md) - Detailed deployment steps
- 🔒 [Security Guide](SECURITY.md) - Security best practices
- 🤝 [Contributing](CONTRIBUTING.md) - How to contribute

---

**Last Updated:** 2024  
**Maintainer:** Ranas Mukminov | [run-as-daemon.ru](https://run-as-daemon.ru)

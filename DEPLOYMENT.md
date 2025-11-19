# 🚀 Deployment Guide

Complete guide for deploying MikroTik SNMP monitoring templates in production environments.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [MikroTik Configuration](#mikrotik-configuration)
- [Zabbix Configuration](#zabbix-configuration)
- [Testing & Validation](#testing--validation)
- [Production Deployment](#production-deployment)
- [Professional Support](#professional-support)

---

## ✅ Prerequisites

### Required Components

**Zabbix Server:**
- Version 7.2 or higher (also compatible with 7.x and 6.0 LTS)
- SNMP support enabled
- Sufficient resources for monitoring load
- Network connectivity to MikroTik devices

**MikroTik RouterOS:**
- Version 6.x or 7.x (7.x recommended)
- SNMP service available
- Administrative access to configure SNMP
- Network connectivity to Zabbix server

**Network Requirements:**
- UDP port 161 accessible from Zabbix to MikroTik
- Low latency connection (< 100ms recommended)
- Reliable network path (minimal packet loss)

### Tools and Utilities

Install on your Zabbix server or management workstation:

```bash
# Debian/Ubuntu
apt-get update
apt-get install -y snmp snmp-mibs-downloader

# RHEL/CentOS/Rocky
yum install -y net-snmp net-snmp-utils

# Verify installation
snmpwalk --version
```

### Download Templates

Clone the repository or download the templates:

```bash
git clone https://github.com/ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-.git
cd MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-
```

Available templates:
- `template_mikrotik_snmpv2c_advanced_zbx72.xml` - SNMPv2c, advanced features
- `template_mikrotik_snmpv2c_zbx72_uuid32.xml` - SNMPv2c, basic
- `template_mikrotik_snmpv3_advanced_zbx72.xml` - SNMPv3, secure

---

## 🔧 MikroTik Configuration

### Step 1: Basic SNMP Configuration (SNMPv2c)

Connect to your MikroTik via SSH or terminal:

```bash
# Enable SNMP service
/snmp
set enabled=yes contact="network-admin@yourcompany.com" location="DataCenter-Primary"

# Configure SNMP community
/snmp community
set [find default=yes] name="YourSecureString123" addresses=10.0.0.100/32

# Alternative: Create new community
/snmp community
add name="YourSecureString123" addresses=10.0.0.100/32
```

**Important:**
- Replace `10.0.0.100` with your Zabbix server IP
- Use a strong, unique community string (not "public" or "private")
- Restrict access to specific IP addresses

### Step 2: Firewall Configuration

Add a firewall rule to allow SNMP from Zabbix:

```bash
/ip firewall filter
add chain=input protocol=udp dst-port=161 \
    src-address=10.0.0.100 \
    action=accept \
    comment="Allow SNMP from Zabbix Server" \
    place-before=0
```

For multiple Zabbix servers or proxies:

```bash
# Create address list
/ip firewall address-list
add list=zabbix-servers address=10.0.0.100 comment="Zabbix Primary"
add list=zabbix-servers address=10.0.0.101 comment="Zabbix Proxy 1"

# Firewall rule using address list
/ip firewall filter
add chain=input protocol=udp dst-port=161 \
    src-address-list=zabbix-servers \
    action=accept \
    comment="Allow SNMP from Zabbix Infrastructure"
```

### Step 3: SNMPv3 Configuration (Recommended for Production)

For enhanced security, configure SNMPv3:

```bash
# Disable SNMPv2c community
/snmp community
set [find default=yes] disabled=yes

# Configure SNMPv3
/snmp
set enabled=yes \
    engine-id=800000000100505400000001 \
    contact="security@yourcompany.com"

# Create SNMPv3 user
/snmp user
add name=zabbix-monitor \
    group=read \
    auth-protocol=SHA256 \
    auth-password="YourAuthPassword!2024" \
    encryption-protocol=AES \
    encryption-password="YourPrivPassword!2024"
```

**Security recommendations:**
- Use SHA-256 for authentication (SHA-1 minimum)
- Use AES for encryption
- Use strong, unique passwords (12+ characters)
- Different passwords for auth and encryption

### Step 4: Verify SNMP Configuration

On MikroTik, verify SNMP is running:

```bash
/snmp print
/snmp community print
# or for SNMPv3:
/snmp user print
```

Test from Zabbix server:

```bash
# Test SNMPv2c
snmpwalk -v2c -c YourSecureString123 192.168.1.1 system

# Test SNMPv3
snmpwalk -v3 -l authPriv \
    -u zabbix-monitor \
    -a SHA-256 -A "YourAuthPassword!2024" \
    -x AES -X "YourPrivPassword!2024" \
    192.168.1.1 system
```

Expected output should include system information (name, uptime, location, etc.).

---

## 🗄️ Zabbix Configuration

### Step 1: Import Template

1. Log in to Zabbix web interface
2. Navigate to **Configuration → Templates**
3. Click **Import** button
4. Click **Choose File** and select the template XML file
5. Configure import options:
   - ✅ Create new
   - ✅ Update existing
   - ✅ Delete missing (for template updates only)
6. Click **Import**
7. Verify the template appears in the templates list

### Step 2: Create Host Groups (Optional)

Organize your MikroTik devices:

1. Go to **Configuration → Host groups**
2. Click **Create host group**
3. Examples:
   - `MikroTik Routers`
   - `MikroTik Switches`
   - `Edge Routers`
   - `Core Switches`

### Step 3: Create Host

1. Navigate to **Configuration → Hosts**
2. Click **Create host**
3. Configure host settings:

**Host tab:**
- **Host name:** `mikrotik-edge-01` (unique identifier)
- **Visible name:** `Edge Router 01` (display name)
- **Groups:** Select appropriate host group(s)
- **Interfaces:**
  - Click **Add**
  - **Type:** SNMP
  - **IP address:** `192.168.1.1` (MikroTik IP)
  - **DNS name:** (optional, e.g., `router01.example.com`)
  - **Connect to:** IP
  - **Port:** `161`
  - **SNMP version:** SNMPv2 (or SNMPv3)
  - **SNMP community:** `{$SNMP_COMMUNITY}` (macro reference)
  - **Use bulk requests:** Yes (recommended for performance)
  - **Default:** Yes

For SNMPv3:
- **SNMP version:** SNMPv3
- **Context name:** (leave empty)
- **Security name:** `zabbix-monitor`
- **Security level:** authPriv
- **Authentication protocol:** SHA or SHA-256
- **Authentication passphrase:** `YourAuthPassword!2024`
- **Privacy protocol:** AES
- **Privacy passphrase:** `YourPrivPassword!2024`

**Templates tab:**
- Click **Select**
- Find and select: `Template MikroTik SNMPv2c Advanced (Production)`
- Click **Add**

**Macros tab:**
- **Inherited and host macros** (or **Host macros**)
- Override necessary macros:
  - `{$SNMP_COMMUNITY}` = `YourSecureString123` (for SNMPv2c)
  - `{$IF_UTIL_WARN}` = `80` (interface utilization warning, %)
  - `{$IF_UTIL_HIGH}` = `90` (interface utilization critical, %)
  - `{$CPU_UTIL_WARN}` = `80` (CPU warning threshold, %)
  - `{$CPU_UTIL_HIGH}` = `90` (CPU critical threshold, %)
  - `{$MEMORY_UTIL_WARN}` = `80` (Memory warning threshold, %)
  - `{$MEMORY_UTIL_HIGH}` = `90` (Memory critical threshold, %)

4. Click **Add** or **Update**

### Step 4: Configure Discovery Rules (Optional)

Adjust Low-Level Discovery (LLD) filters if needed:

1. Go to **Configuration → Hosts → [Your Host] → Discovery rules**
2. Select a discovery rule (e.g., "Network Interfaces Discovery")
3. Adjust filters via macros or LLD filters:
   - `{$IF.LLD.FILTER.MATCHES}` - Include interfaces matching pattern
   - `{$IF.LLD.FILTER.NOT_MATCHES}` - Exclude interfaces matching pattern
   - `{$IF.LLD.FILTER.ADMIN_STATUS}` - Filter by admin status (1=up)

Example: Monitor only ether and sfp interfaces:
- Override macro `{$IF.LLD.FILTER.MATCHES}` = `^(ether|sfp)`

---

## 🧪 Testing & Validation

### Initial Data Collection

1. Wait 2-5 minutes for initial data collection
2. Navigate to **Monitoring → Latest data**
3. Select your MikroTik host from the host filter
4. Verify data is being collected:
   - System uptime
   - CPU utilization
   - Memory usage
   - Interface discovery completed

### Verify Interface Discovery

1. Go to **Configuration → Hosts → [Your Host] → Discovery**
2. Click on "Network Interfaces Discovery" rule
3. Click **Execute now** to manually trigger discovery
4. Wait 30 seconds, then check **Monitoring → Latest data**
5. Filter by your host and application "Interfaces"
6. Verify interfaces are discovered and collecting data

### Test Triggers

1. Navigate to **Monitoring → Problems**
2. Check for any new problems related to your host
3. If no problems, test a trigger:
   - Temporarily lower a threshold via macro
   - Or simulate a condition (e.g., shut down an interface on MikroTik)
4. Verify trigger activates within expected time

### Check Graphs

1. Go to **Monitoring → Hosts → Graphs**
2. Select your MikroTik host
3. View graphs for:
   - CPU utilization
   - Memory usage
   - Interface traffic (should show in bits/sec)
4. Verify graphs display data correctly

### Performance Validation

Monitor Zabbix server performance:

```bash
# Check Zabbix server internal items
# In Zabbix UI: Monitoring → Latest data → Host: Zabbix Server
```

Look for:
- Poller processes utilization
- SNMP poller busy %
- Queue of items to be collected

If queue is growing or pollers are 100% busy, consider:
- Increasing poller processes in `zabbix_server.conf`
- Using Zabbix proxies for distributed monitoring
- Adjusting polling intervals

---

## 🚀 Production Deployment

### Pre-Deployment Checklist

- [ ] Templates tested in lab environment
- [ ] SNMP configuration validated on test devices
- [ ] Firewall rules tested and documented
- [ ] Monitoring thresholds reviewed and approved
- [ ] Alerting actions configured in Zabbix
- [ ] Escalation procedures documented
- [ ] Team trained on new monitoring
- [ ] Rollback plan prepared

### Deployment Strategy

**Option 1: Phased Rollout**
1. Start with non-critical edge devices
2. Monitor for 24-48 hours
3. Deploy to secondary infrastructure
4. Monitor for 1 week
5. Deploy to critical core infrastructure

**Option 2: Pilot Program**
1. Select 5-10 representative devices
2. Deploy and monitor for 2 weeks
3. Gather feedback from NOC team
4. Adjust thresholds and filters
5. Full deployment after validation

### Post-Deployment Tasks

**Week 1:**
- [ ] Monitor data collection daily
- [ ] Review triggered alerts
- [ ] Adjust thresholds based on baselines
- [ ] Document false positives
- [ ] Train additional team members

**Week 2-4:**
- [ ] Analyze historical data
- [ ] Create custom dashboards
- [ ] Configure additional alerting actions
- [ ] Document troubleshooting procedures
- [ ] Conduct team retrospective

### Maintenance

**Monthly:**
- Review trigger frequency and adjust thresholds
- Check for template updates
- Validate discovery rules are functioning
- Review and clean up obsolete items

**Quarterly:**
- Update templates to latest version
- Review and optimize polling intervals
- Conduct security audit of SNMP access
- Update documentation

**Annually:**
- Migrate to SNMPv3 if not already using
- Review and optimize Zabbix database
- Conduct full disaster recovery test
- Plan for Zabbix version upgrades

---

## 🏢 Professional Support

Need assistance with deployment or optimization?

### Deployment Services

- 🏗️ **Infrastructure Design**
  - Monitoring architecture planning
  - SNMP security design
  - High-availability setup

- ⚙️ **Implementation**
  - Template customization
  - Bulk device onboarding
  - Integration with existing systems

- 🎯 **Optimization**
  - Performance tuning
  - Threshold calibration
  - Custom alerting workflows

- 🎓 **Training**
  - Team onboarding
  - Best practices workshops
  - Troubleshooting training

- 🛠️ **Ongoing Support**
  - Managed monitoring services
  - 24/7 incident response
  - Regular health checks

### Why Choose Professional Services?

> **"Defense by design. Speed by default."**

✅ **Experience**
- Years of MikroTik and Zabbix expertise
- Proven deployment methodologies
- Battle-tested configurations

✅ **Efficiency**
- Faster deployment (days vs. weeks)
- Avoid common pitfalls
- Best practices from day one

✅ **Reliability**
- Production-ready configurations
- Comprehensive testing
- Ongoing support

### Contact for Professional Deployment Support

- 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- 💬 Telegram: [@run_as_daemon](https://t.me/run_as_daemon)
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)

---

## 📚 Additional Resources

- [Main README](README.md) - Overview and quick start
- [QUICKSTART.md](QUICKSTART.md) - 3-step deployment guide
- [SECURITY.md](SECURITY.md) - Security best practices
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history

---

**Last Updated:** 2024  
**Maintainer:** Ranas Mukminov | [run-as-daemon.ru](https://run-as-daemon.ru)

# Zabbix Host Configuration Example

This guide provides step-by-step instructions for configuring a MikroTik host in Zabbix using the Advanced templates.

---

## Table of Contents

- [SNMPv2c Configuration](#snmpv2c-configuration)
- [SNMPv3 Configuration (Recommended)](#snmpv3-configuration-recommended)
- [Host Macro Customization](#host-macro-customization)
- [Verification Steps](#verification-steps)
- [Common Issues](#common-issues)

---

## SNMPv2c Configuration

### Step 1: Import Template

1. Navigate to **Data collection → Templates**
2. Click **Import**
3. Select `template_mikrotik_snmpv2c_advanced_zbx72.xml`
4. Import options:
   - ✅ **Create new**
   - ✅ **Update existing**
   - ✅ **Delete missing**
5. Click **Import**
6. Verify template appears in list as **Template MikroTik SNMPv2c Advanced (Production)**

### Step 2: Create Host

1. Navigate to **Data collection → Hosts**
2. Click **Create host** (top right)
3. **Host** tab configuration:

| Field | Value | Notes |
|-------|-------|-------|
| **Host name** | `mikrotik-gw-01` | Use DNS name or descriptive identifier |
| **Visible name** | `MikroTik Gateway 01 (192.168.1.1)` | Human-readable name for UI |
| **Templates** | `Template MikroTik SNMPv2c Advanced (Production)` | Select from dropdown |
| **Host groups** | `Routers` or `Network devices` | Create if doesn't exist |
| **Description** | `Main gateway router - Building A` | Optional, for documentation |

4. **Interfaces** section:
   - Click **Add** → **SNMP**

| Field | Value | Notes |
|-------|-------|-------|
| **IP address** | `192.168.1.1` | MikroTik management IP |
| **DNS name** | `gw01.example.com` | Optional, leave empty if using IP |
| **Connect to** | `IP` | Or `DNS` if you provided DNS name |
| **Port** | `161` | Standard SNMP port |
| **SNMP version** | `SNMPv2` | For SNMPv2c |
| **SNMP community** | `{$SNMP_COMMUNITY}` | Use macro (will override below) |

5. Don't click Add yet - continue to Macros tab

### Step 3: Configure Host Macros

1. Click **Macros** tab
2. Click **Add** in **Host macros** section
3. Configure SNMP community:

| Macro | Value | Description |
|-------|-------|-------------|
| `{$SNMP_COMMUNITY}` | `YourSecureString123!` | **Must match MikroTik config** |

4. **Optional**: Customize thresholds for this specific host:

| Macro | Default | Suggested Override | Use Case |
|-------|---------|-------------------|----------|
| `{$CPU.UTIL.WARN}` | 80 | 70 | Lower threshold for critical routers |
| `{$CPU.UTIL.CRIT}` | 90 | 85 | Lower threshold for critical routers |
| `{$IF.POLL.INTERVAL}` | 1m | 30s | High-frequency monitoring for WAN links |
| `{$TEMP.MAX.WARN}` | 60 | 50 | Cooler environment or sensitive hardware |
| `{$IF.LLD.FILTER.MATCH}` | `.*` | `^ether[1-8]$` | Only monitor specific interfaces |
| `{$VOLTAGE.MIN}` | 11 | 20 | For 24V devices (CCR series) |
| `{$VOLTAGE.MAX}` | 26 | 28 | For 24V devices (CCR series) |

5. Click **Add** to create the host

### Step 4: Verify Configuration

Wait **2-3 minutes** for initial data collection, then:

1. **Check latest data:**
   - **Monitoring → Latest data**
   - Filter by host: `mikrotik-gw-01`
   - You should see:
     - ✅ ICMP ping = 1 (reachable)
     - ✅ System uptime (value in seconds)
     - ✅ CPU utilization (percentage)
     - ✅ Memory utilization (percentage)
     - ✅ Temperature (if supported)

2. **Check discovery:**
   - **Data collection → Hosts → [Your Host] → Discovery**
   - Click **Network interface discovery**
   - Status should show discovered interfaces (e.g., 5-10 interfaces)

3. **Check triggers:**
   - **Monitoring → Problems**
   - Filter by host
   - Should be empty (or only expected alerts)

---

## SNMPv3 Configuration (Recommended)

### Step 1: Import Template

1. Navigate to **Data collection → Templates**
2. Click **Import**
3. Select `template_mikrotik_snmpv3_advanced_zbx72.xml`
4. Import with same options as SNMPv2c
5. Verify template: **Template MikroTik SNMPv3 Advanced (Production - Secure)**

### Step 2: Create Host

Follow same steps as SNMPv2c, but with **different SNMP interface configuration**:

**Interfaces** section - SNMP configuration:

| Field | Value | Notes |
|-------|-------|-------|
| **IP address** | `192.168.1.1` | MikroTik management IP |
| **Port** | `161` | Standard SNMP port |
| **SNMP version** | `SNMPv3` | **Important: Select SNMPv3** |
| **Context name** | *(leave empty)* | Not needed for MikroTik |
| **Security name** | `{$SNMPV3_USER}` | Use macro |
| **Security level** | `authPriv` | **Recommended** (auth + encryption) |
| **Authentication protocol** | `SHA` | **Recommended** (or SHA224/SHA256/SHA384/SHA512 if available) |
| **Authentication passphrase** | `{$SNMPV3_AUTH_PASSPHRASE}` | Use macro |
| **Privacy protocol** | `AES128` | **Recommended** (or AES192/AES256 if available) |
| **Privacy passphrase** | `{$SNMPV3_PRIV_PASSPHRASE}` | Use macro |

### Step 3: Configure Host Macros (SNMPv3)

**Required macros:**

| Macro | Value | Description |
|-------|-------|-------------|
| `{$SNMPV3_USER}` | `zabbix_monitor` | **Must match MikroTik config** |
| `{$SNMPV3_AUTH_PASSPHRASE}` | `YourAuthPass123!` | **Min 8 chars, must match MikroTik** |
| `{$SNMPV3_PRIV_PASSPHRASE}` | `YourPrivPass456!` | **Min 8 chars, must match MikroTik** |

**Optional macros:** Same as SNMPv2c (CPU thresholds, polling intervals, etc.)

### Step 4: Verify Configuration

Same verification steps as SNMPv2c.

---

## Host Macro Customization

### Example 1: Core Router (High Availability Requirements)

```
Host: mikrotik-core-01
Macros:
  {$SNMP_COMMUNITY} = StrongRandomString987!
  {$CPU.UTIL.WARN} = 70            # Lower threshold for early warning
  {$CPU.UTIL.CRIT} = 85            # Lower critical threshold
  {$MEM.UTIL.WARN} = 80            # Lower memory warning
  {$IF.POLL.INTERVAL} = 30s        # Poll critical interfaces every 30s
  {$ICMP.LOSS.WARN} = 5            # Alert on minimal packet loss
  {$IF.LLD.FILTER.MATCH} = ^(ether|sfp).*  # Only physical interfaces
```

### Example 2: Edge Router (Standard Monitoring)

```
Host: mikrotik-edge-05
Macros:
  {$SNMP_COMMUNITY} = AnotherSecureString456!
  # Use all default thresholds (no overrides needed)
```

### Example 3: Branch Office Router (Reduced Monitoring)

```
Host: mikrotik-branch-12
Macros:
  {$SNMP_COMMUNITY} = BranchSecureString789!
  {$IF.POLL.INTERVAL} = 5m         # Reduce polling frequency
  {$IF.DISCOVERY.INTERVAL} = 2h    # Reduce discovery frequency
  {$IF.LLD.FILTER.MATCH} = ^ether1$  # Only monitor WAN interface
```

### Example 4: CCR Router (24V Power Supply)

```
Host: mikrotik-ccr-01
Macros:
  {$SNMP_COMMUNITY} = CCRSecureString321!
  {$VOLTAGE.MIN} = 20              # 24V device minimum
  {$VOLTAGE.MAX} = 28              # 24V device maximum
```

### Example 5: Wireless AP (Include VLAN Interfaces)

```
Host: mikrotik-ap-03
Macros:
  {$SNMP_COMMUNITY} = APSecureString654!
  {$IF.LLD.FILTER.NOT_MATCHES} = (?i:loopback|virtual)  # Allow VLANs
  {$IF.LLD.FILTER.ADMIN_STATUS} = .*  # Monitor all admin states
```

---

## Verification Steps

### 1. Test SNMP from Zabbix Server

**For SNMPv2c:**
```bash
# From Zabbix server, test SNMP connectivity
snmpwalk -v2c -c YourSecureString123! 192.168.1.1 system

# Expected output:
# SNMPv2-MIB::sysDescr.0 = STRING: RouterOS RB3011
# SNMPv2-MIB::sysObjectID.0 = OID: ...
# SNMPv2-MIB::sysUpTime.0 = Timeticks: ...
```

**For SNMPv3:**
```bash
# From Zabbix server, test SNMPv3 connectivity
snmpwalk -v3 -l authPriv \
  -u zabbix_monitor \
  -a SHA -A "YourAuthPass123!" \
  -x AES -X "YourPrivPass456!" \
  192.168.1.1 system

# Expected output: Same as SNMPv2c
```

### 2. Check Zabbix Server Logs

```bash
# Check Zabbix server logs for SNMP errors
tail -f /var/log/zabbix/zabbix_server.log | grep -i snmp

# Look for errors like:
# - "Timeout while connecting" → Check firewall, MikroTik SNMP enabled
# - "No Such Instance" → Check if OID is supported on your RouterOS version
# - "Authentication failure" → Check SNMPv3 credentials
```

### 3. Force Discovery Execution

1. Navigate to **Data collection → Hosts → [Your Host] → Discovery**
2. Find **Network interface discovery**
3. Click **Execute now**
4. Refresh page after 30 seconds
5. Check **Last check** column - should show recent timestamp

### 4. Verify Interface Discovery Results

1. Navigate to **Monitoring → Latest data**
2. Filter: **Hosts** = `mikrotik-gw-01`, **Name** = `Inbound bandwidth`
3. You should see multiple items, one per interface:
   - `ether1: Inbound bandwidth`
   - `ether2: Inbound bandwidth`
   - `sfp1: Inbound bandwidth`
   - etc.

### 5. Check Graphs

1. Navigate to **Monitoring → Hosts → [Your Host] → Graphs**
2. You should see automatically created graphs:
   - `ether1: Traffic`
   - `ether1: Bandwidth utilization`
   - `ether1: Errors and discards`
   - etc.

---

## Common Issues

### Issue 1: "SNMP timeout" in Zabbix

**Possible causes:**
- ❌ MikroTik SNMP not enabled
- ❌ Firewall blocking UDP 161
- ❌ Wrong IP address
- ❌ Wrong community string / SNMPv3 credentials

**Solutions:**
1. Check MikroTik SNMP: `/snmp print` → Ensure `enabled=yes`
2. Check MikroTik firewall: `/ip firewall filter print where dst-port=161`
3. Test from Zabbix server: `snmpwalk -v2c -c <community> <mikrotik-ip> system`
4. Check Zabbix host interface configuration

### Issue 2: No interfaces discovered

**Possible causes:**
- ❌ Discovery filters too restrictive
- ❌ Interfaces in "down" admin state
- ❌ Interface names don't match regex

**Solutions:**
1. Check MikroTik interfaces: `/interface print`
2. Temporarily disable filters:
   - `{$IF.LLD.FILTER.MATCH}` = `.*`
   - `{$IF.LLD.FILTER.NOT_MATCHES}` = (leave empty or set to `NONE`)
   - `{$IF.LLD.FILTER.ADMIN_STATUS}` = `.*`
3. Force discovery: **Execute now**
4. Check Zabbix logs for discovery data

### Issue 3: CPU/Memory items not supported

**Possible causes:**
- ❌ Old RouterOS version
- ❌ Device doesn't support HOST-RESOURCES-MIB

**Solutions:**
1. Update RouterOS to latest stable version
2. Try MikroTik-specific OIDs:
   - CPU: `1.3.6.1.4.1.14988.1.1.3.1.0`
   - Memory: Check MikroTik documentation
3. Disable unsupported items in template

### Issue 4: Temperature/Voltage items not supported

**Possible causes:**
- ❌ Device model doesn't have sensors (e.g., some hEX models)
- ❌ Older RouterOS version

**Solutions:**
1. Check device specifications
2. Disable temperature/voltage items if not supported:
   - **Data collection → Hosts → [Host] → Items**
   - Filter by "temperature" or "voltage"
   - Disable items (don't delete - template will recreate)

### Issue 5: OSPF/BGP discovery not working

**Possible causes:**
- ❌ OSPF/BGP not configured on MikroTik
- ❌ Routing package not installed
- ❌ SNMP doesn't support routing MIBs on this device

**Solutions:**
1. Check if OSPF/BGP is running: `/routing ospf neighbor print` or `/routing bgp peer print`
2. Check if routing package installed: `/system package print`
3. Test OSPF/BGP MIBs from Zabbix server:
   ```bash
   snmpwalk -v2c -c <community> <mikrotik-ip> OSPF-MIB::ospfNbrTable
   snmpwalk -v2c -c <community> <mikrotik-ip> BGP4-MIB::bgpPeerTable
   ```
4. Disable OSPF/BGP discovery if not needed

### Issue 6: Too many alerts after deployment

**Solutions:**
1. Review and adjust threshold macros
2. Use trigger dependencies (already configured)
3. Temporarily disable non-critical triggers
4. Set up maintenance periods during testing
5. Configure alert severity filters in notifications

### Issue 7: High Zabbix database growth

**Solutions:**
1. Reduce polling intervals for non-critical hosts
2. Reduce history/trend retention:
   - **Administration → Housekeeping**
   - Adjust retention periods
3. Limit discovered interfaces with filters
4. Use Zabbix partitioning (advanced)

---

## Next Steps

After successful configuration:

1. ✅ **Create custom dashboards** - visualize key metrics
2. ✅ **Configure notifications** - email/Slack alerts for triggers
3. ✅ **Set up maintenance windows** - suppress alerts during planned work
4. ✅ **Document customizations** - record macro overrides
5. ✅ **Create runbooks** - procedures for common alerts
6. ✅ **Regular reviews** - tune thresholds based on actual behavior
7. ✅ **Backup Zabbix config** - export templates and host configs

---

## Resources

- **MikroTik Wiki:** https://wiki.mikrotik.com/wiki/Manual:SNMP
- **Zabbix Documentation:** https://www.zabbix.com/documentation/current/
- **SNMP MIB Browser:** https://www.ireasoning.com/mibbrowser.shtml (for testing OIDs)
- **Project Repository:** [Link to your GitHub repo]

---

**Questions?** Check [Troubleshooting](../README.md#troubleshooting) in main README or open an issue.

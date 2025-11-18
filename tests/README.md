# Tests Directory

This directory contains validation and testing scripts for the MikroTik Zabbix templates.

---

## 📁 Files

### [run_checks.sh](run_checks.sh)
**Convenience wrapper to execute all static checks locally**

**Features:**
- ✅ Runs `validate_xml.py --all` against every template in one command
- ✅ Uses the system `python3` (override via `PYTHON_BIN=/path/to/python`)
- ✅ Exits with non-zero status when validation fails (CI-friendly)

**Usage:**
```bash
chmod +x run_checks.sh
./run_checks.sh

# or force a different interpreter
PYTHON_BIN=python3.11 ./run_checks.sh
```

---

### [validate_xml.py](validate_xml.py)
**Python script to validate Zabbix template XML files**

**Features:**
- ✅ XML well-formedness check
- ✅ UUID uniqueness validation
- ✅ Required elements presence check
- ✅ Macro syntax validation
- ✅ Item key syntax validation
- ✅ SNMP OID format validation
- ✅ Trigger expression validation
- ✅ Security issue detection (default passwords)

**Requirements:**
- Python 3.6+
- Standard library only (no external dependencies)

**Usage:**
```bash
# Validate single template
python3 validate_xml.py ../template_mikrotik_snmpv2c_advanced_zbx72.xml

# Validate all XML files in parent directory
python3 validate_xml.py --all
```

**Output:**
```
╔════════════════════════════════════════════════════════════════════╗
║  Zabbix Template XML Validator                                    ║
╚════════════════════════════════════════════════════════════════════╝

Validating: template_mikrotik_snmpv2c_advanced_zbx72.xml
======================================================================

Information:
  ✓ XML is well-formed
  ✓ Export version: 7.0
  ✓ Template uuid: 8a9b7c6d5e4f3a2b1c0d9e8f7a6b5c4d
  ✓ All 150 UUIDs are unique
  ✓ Found 35 items/item prototypes

Warnings (2):
  ⚠ Item 'CPU utilization' may need CHANGE_PER_SECOND preprocessing
  ⚠ No OSPF discovery found

✓ VALIDATION PASSED WITH WARNINGS
```

---

### [test_oids.sh](test_oids.sh)
**Bash script to test SNMP OIDs against a real MikroTik device**

**Features:**
- ✅ Tests all OIDs used in templates
- ✅ Supports SNMPv2c and SNMPv3
- ✅ Color-coded output (pass/fail/N/A)
- ✅ Detects unsupported features
- ✅ Provides troubleshooting suggestions

**Requirements:**
- `snmpget` and `snmpwalk` commands (net-snmp package)
- Network access to MikroTik device
- SNMP enabled on MikroTik

**Installation (if snmpget not found):**
```bash
# Debian/Ubuntu
sudo apt-get install snmp snmp-mibs-downloader

# RHEL/CentOS
sudo yum install net-snmp-utils

# macOS
brew install net-snmp
```

**Usage:**
```bash
# Make script executable
chmod +x test_oids.sh

# Test with SNMPv2c
./test_oids.sh 192.168.1.1 MySecureString v2c

# Test with SNMPv3 (edit credentials in script first!)
./test_oids.sh 192.168.1.1 zabbix_monitor v3
```

**Before using SNMPv3:** Edit the script and update these variables:
```bash
SNMPV3_USER="zabbix_monitor"
SNMPV3_AUTH_PASS="YourAuthPassword"
SNMPV3_PRIV_PASS="YourPrivPassword"
```

**Output:**
```
╔════════════════════════════════════════════════════════════════════╗
║  MikroTik SNMP OID Tester                                         ║
╚════════════════════════════════════════════════════════════════════╝

Target:  192.168.1.1
Version: SNMPv2c

━━━ Basic System Information ━━━
  System Description                                 ✓ OK (RouterOS RB3011)
  System Uptime                                      ✓ OK (1234567)
  System Name                                        ✓ OK (mikrotik-gw-01)

━━━ CPU and Memory ━━━
  CPU Load                                           ✓ OK (25)
  Total Memory                                       ✓ OK (524288)

━━━ MikroTik-Specific Hardware Health ━━━
  System Temperature                                 ✓ OK (450)
  System Voltage                                     ✓ OK (240)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total tests: 26
Passed:      24
Failed:      2
Success rate: 92%

✓ All critical OIDs are supported!
```

---

## 🚀 Quick Start

### Validate Templates Before Deployment

```bash
# Navigate to tests directory
cd tests

# Validate all templates
python3 validate_xml.py --all
```

### Test Against Real Device

```bash
# Navigate to tests directory
cd tests

# Configure MikroTik first (see examples/mikrotik_snmp_config.rsc)

# Test OID support
./test_oids.sh 192.168.1.1 YourCommunityString v2c
```

---

## 🔍 Validation Checklist

Before deploying templates to production:

- [ ] Run `validate_xml.py --all` - ensure no errors
- [ ] Run `test_oids.sh` on representative device - ensure >90% pass rate
- [ ] Check unsupported OIDs and plan to disable those items
- [ ] Test template import in non-production Zabbix
- [ ] Verify discovery works on test device
- [ ] Check that graphs are generated
- [ ] Test trigger firing with simulated conditions

---

## 🐛 Troubleshooting

### validate_xml.py Issues

**Problem:** `ModuleNotFoundError: No module named 'xml'`
```bash
# This shouldn't happen (xml.etree is in standard library)
# Try reinstalling Python 3
```

**Problem:** "Duplicate UUID" errors
```bash
# UUIDs must be unique across the template
# Regenerate UUIDs with:
import uuid
print(uuid.uuid4().hex)
```

**Problem:** "Security risk: Macro uses default 'public' value"
```bash
# This is intentional for security
# The default community is now "CHANGE_ME_SECURITY_RISK"
# Override with secure value at host level
```

---

### test_oids.sh Issues

**Problem:** `snmpget: command not found`
```bash
# Install SNMP tools:
sudo apt-get install snmp  # Debian/Ubuntu
sudo yum install net-snmp-utils  # RHEL/CentOS
```

**Problem:** "Timeout" errors on all OIDs
```bash
# Check SNMP connectivity:
1. Ping MikroTik: ping 192.168.1.1
2. Check SNMP enabled: /snmp print (on MikroTik)
3. Check firewall: /ip firewall filter print where dst-port=161
4. Test from Zabbix server, not your workstation
```

**Problem:** "Authentication failure" (SNMPv3)
```bash
# Edit test_oids.sh and update these variables:
SNMPV3_USER="your_username"
SNMPV3_AUTH_PASS="your_auth_password"
SNMPV3_PRIV_PASS="your_priv_password"

# Must match MikroTik configuration exactly
```

**Problem:** Many "No Such Object" errors
```bash
# Possible causes:
1. Old RouterOS version - upgrade to latest stable
2. Device model doesn't support certain OIDs
3. Features not enabled (OSPF/BGP)

# Check RouterOS version:
# /system resource print

# Acceptable: 4-5 failures for optional features
# Concerning: >10 failures indicate compatibility issues
```

---

## 📝 Interpreting Test Results

### XML Validation Results

| Result | Meaning | Action |
|--------|---------|--------|
| ✓ VALIDATION PASSED | No issues found | Safe to use |
| ⚠ VALIDATION PASSED WITH WARNINGS | Minor issues | Review warnings, usually safe |
| ✗ VALIDATION FAILED | Critical errors | Fix before deploying |

### OID Test Results

| Symbol | Meaning | Description |
|--------|---------|-------------|
| ✓ OK | OID supported | Full functionality |
| ✗ FAIL | OID not supported | Feature unavailable |
| ⊗ N/A | Optional feature | Not configured (OK) |

**Success Rate Interpretation:**
- **100%** - Perfect, all features supported
- **90-99%** - Excellent, only optional features missing
- **80-89%** - Good, some hardware features unavailable
- **<80%** - Investigate, may indicate configuration issues

---

## 🔧 Advanced Testing

### Test Discovery Rules

```bash
# Test interface discovery
snmpwalk -v2c -c YourCommunity 192.168.1.1 IF-MIB::ifDescr
snmpwalk -v2c -c YourCommunity 192.168.1.1 IF-MIB::ifIndex

# Test OSPF neighbor discovery
snmpwalk -v2c -c YourCommunity 192.168.1.1 OSPF-MIB::ospfNbrIpAddr

# Test BGP peer discovery
snmpwalk -v2c -c YourCommunity 192.168.1.1 BGP4-MIB::bgpPeerRemoteAddr
```

### Test 64-bit Counters

```bash
# Verify device supports 64-bit counters (required for 10G+ links)
snmpget -v2c -c YourCommunity 192.168.1.1 IF-MIB::ifHCInOctets.1
snmpget -v2c -c YourCommunity 192.168.1.1 IF-MIB::ifHCOutOctets.1

# Should return Counter64 values, not "No Such Object"
```

### Test MikroTik-Specific OIDs

```bash
# CPU (MikroTik MIB)
snmpget -v2c -c YourCommunity 192.168.1.1 1.3.6.1.4.1.14988.1.1.3.1.0

# Temperature
snmpget -v2c -c YourCommunity 192.168.1.1 1.3.6.1.4.1.14988.1.1.3.10.0

# Voltage
snmpget -v2c -c YourCommunity 192.168.1.1 1.3.6.1.4.1.14988.1.1.3.8.0
```

---

## 🤝 Contributing

Found a bug in validation scripts? Have an improvement?

1. Test your changes
2. Update this README if adding new scripts
3. Submit a Pull Request

---

## 📄 License

These testing scripts are part of the MikroTik Zabbix Template project.
MIT License - see [../LICENSE](../LICENSE)

---

**Questions?** See main [README](../README.md) or open an issue on GitHub.

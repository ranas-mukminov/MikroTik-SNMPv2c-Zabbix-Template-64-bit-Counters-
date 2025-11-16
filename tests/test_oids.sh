#!/bin/bash
#
# SNMP OID Tester for MikroTik Devices
#
# This script tests all SNMP OIDs used in the Zabbix templates
# against a real MikroTik device.
#
# Usage:
#   ./test_oids.sh <mikrotik-ip> <community-or-user> [v2c|v3]
#
# Examples:
#   ./test_oids.sh 192.168.1.1 MySecureString v2c
#   ./test_oids.sh 192.168.1.1 zabbix_monitor v3
#

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <mikrotik-ip> <community-or-user> [v2c|v3]"
    echo ""
    echo "Examples:"
    echo "  $0 192.168.1.1 MySecureString v2c"
    echo "  $0 192.168.1.1 zabbix_monitor v3"
    exit 1
fi

MIKROTIK_IP=$1
AUTH_STRING=$2
SNMP_VERSION=${3:-v2c}

# SNMPv3 credentials (edit these if using SNMPv3)
SNMPV3_USER="zabbix_monitor"
SNMPV3_AUTH_PASS="ChangeMe_AuthPass_Min8Chars!"
SNMPV3_PRIV_PASS="ChangeMe_PrivPass_Min8Chars!"

# Check if snmpget is installed
if ! command -v snmpget &> /dev/null; then
    echo -e "${RED}Error: snmpget command not found${NC}"
    echo "Install: sudo apt-get install snmp  (Debian/Ubuntu)"
    echo "         sudo yum install net-snmp-utils  (RHEL/CentOS)"
    exit 1
fi

# Function to test OID
test_oid() {
    local oid=$1
    local description=$2
    local expected_type=$3

    printf "  %-50s " "$description"

    if [ "$SNMP_VERSION" == "v3" ]; then
        result=$(snmpget -v3 -l authPriv \
            -u "$SNMPV3_USER" \
            -a SHA -A "$SNMPV3_AUTH_PASS" \
            -x AES -X "$SNMPV3_PRIV_PASS" \
            -Oqv -t 5 "$MIKROTIK_IP" "$oid" 2>&1)
    else
        result=$(snmpget -v2c -c "$AUTH_STRING" -Oqv -t 5 "$MIKROTIK_IP" "$oid" 2>&1)
    fi

    if [ $? -eq 0 ] && [ -n "$result" ] && [[ ! "$result" =~ "No Such" ]]; then
        echo -e "${GREEN}✓ OK${NC} ($result)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} ($result)"
        return 1
    fi
}

# Print header
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  MikroTik SNMP OID Tester                                         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Target:  ${YELLOW}$MIKROTIK_IP${NC}"
echo -e "Version: ${YELLOW}SNMP$SNMP_VERSION${NC}"
echo ""

passed=0
failed=0

# ============================================================================
# Basic System OIDs
# ============================================================================
echo -e "${BLUE}━━━ Basic System Information ━━━${NC}"

test_oid "SNMPv2-MIB::sysDescr.0" "System Description" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "SNMPv2-MIB::sysUpTime.0" "System Uptime" "Timeticks"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "SNMPv2-MIB::sysName.0" "System Name" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "SNMPv2-MIB::sysLocation.0" "System Location" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "SNMPv2-MIB::sysContact.0" "System Contact" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

# ============================================================================
# CPU and Memory OIDs
# ============================================================================
echo ""
echo -e "${BLUE}━━━ CPU and Memory ━━━${NC}"

test_oid "HOST-RESOURCES-MIB::hrProcessorLoad.1" "CPU Load" "INTEGER"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "HOST-RESOURCES-MIB::hrMemorySize.0" "Total Memory" "INTEGER"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "HOST-RESOURCES-MIB::hrStorageUsed.1" "Used Memory" "INTEGER"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

# ============================================================================
# MikroTik-Specific OIDs
# ============================================================================
echo ""
echo -e "${BLUE}━━━ MikroTik-Specific Hardware Health ━━━${NC}"

test_oid "1.3.6.1.4.1.14988.1.1.3.10.0" "System Temperature" "INTEGER"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "1.3.6.1.4.1.14988.1.1.3.8.0" "System Voltage" "INTEGER"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "1.3.6.1.4.1.14988.1.1.4.4.0" "RouterOS Version" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "1.3.6.1.4.1.14988.1.1.7.3.0" "Serial Number" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

# ============================================================================
# Interface OIDs (testing with index 1)
# ============================================================================
echo ""
echo -e "${BLUE}━━━ Interface Metrics (testing ifIndex=1) ━━━${NC}"

test_oid "IF-MIB::ifDescr.1" "Interface Description" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifOperStatus.1" "Interface Operational Status" "INTEGER"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifHCInOctets.1" "Inbound Octets (64-bit)" "Counter64"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifHCOutOctets.1" "Outbound Octets (64-bit)" "Counter64"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifInErrors.1" "Inbound Errors" "Counter32"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifOutErrors.1" "Outbound Errors" "Counter32"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifInDiscards.1" "Inbound Discards" "Counter32"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifOutDiscards.1" "Outbound Discards" "Counter32"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifHCInBroadcastPkts.1" "Inbound Broadcast Packets" "Counter64"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifHCInMulticastPkts.1" "Inbound Multicast Packets" "Counter64"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifHighSpeed.1" "Interface Speed (Mbps)" "Gauge32"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

test_oid "IF-MIB::ifAlias.1" "Interface Alias" "STRING"
[ $? -eq 0 ] && ((passed++)) || ((failed++))

# ============================================================================
# Routing Protocol OIDs (optional - may not be configured)
# ============================================================================
echo ""
echo -e "${BLUE}━━━ Routing Protocols (optional - may fail if not configured) ━━━${NC}"

printf "  %-50s " "OSPF Neighbors"
if [ "$SNMP_VERSION" == "v3" ]; then
    ospf_result=$(snmpwalk -v3 -l authPriv \
        -u "$SNMPV3_USER" \
        -a SHA -A "$SNMPV3_AUTH_PASS" \
        -x AES -X "$SNMPV3_PRIV_PASS" \
        -Oqv -t 5 "$MIKROTIK_IP" OSPF-MIB::ospfNbrIpAddr 2>&1 | head -1)
else
    ospf_result=$(snmpwalk -v2c -c "$AUTH_STRING" -Oqv -t 5 "$MIKROTIK_IP" OSPF-MIB::ospfNbrIpAddr 2>&1 | head -1)
fi

if [[ "$ospf_result" =~ "No Such" ]] || [ -z "$ospf_result" ]; then
    echo -e "${YELLOW}⊗ N/A${NC} (OSPF not configured or not supported)"
else
    echo -e "${GREEN}✓ OK${NC} (Found: $ospf_result)"
fi

printf "  %-50s " "BGP Peers"
if [ "$SNMP_VERSION" == "v3" ]; then
    bgp_result=$(snmpwalk -v3 -l authPriv \
        -u "$SNMPV3_USER" \
        -a SHA -A "$SNMPV3_AUTH_PASS" \
        -x AES -X "$SNMPV3_PRIV_PASS" \
        -Oqv -t 5 "$MIKROTIK_IP" BGP4-MIB::bgpPeerRemoteAddr 2>&1 | head -1)
else
    bgp_result=$(snmpwalk -v2c -c "$AUTH_STRING" -Oqv -t 5 "$MIKROTIK_IP" BGP4-MIB::bgpPeerRemoteAddr 2>&1 | head -1)
fi

if [[ "$bgp_result" =~ "No Such" ]] || [ -z "$bgp_result" ]; then
    echo -e "${YELLOW}⊗ N/A${NC} (BGP not configured or not supported)"
else
    echo -e "${GREEN}✓ OK${NC} (Found: $bgp_result)"
fi

# ============================================================================
# Summary
# ============================================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

total=$((passed + failed))
percentage=$((passed * 100 / total))

echo -e "Total tests: ${BLUE}$total${NC}"
echo -e "Passed:      ${GREEN}$passed${NC}"
echo -e "Failed:      ${RED}$failed${NC}"
echo -e "Success rate: ${YELLOW}$percentage%${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✓ All critical OIDs are supported!${NC}"
    echo ""
    echo "Your MikroTik device is fully compatible with the Zabbix templates."
    exit 0
elif [ $failed -le 4 ]; then
    echo -e "${YELLOW}⚠ Some optional OIDs are not supported${NC}"
    echo ""
    echo "Your device is compatible, but some features may not work:"
    echo "  - Temperature/Voltage monitoring (device-specific)"
    echo "  - OSPF/BGP monitoring (requires routing configuration)"
    echo ""
    echo "You can disable unsupported items in Zabbix after template import."
    exit 0
else
    echo -e "${RED}✗ Many OIDs are not supported${NC}"
    echo ""
    echo "Possible causes:"
    echo "  1. SNMP is not enabled on MikroTik"
    echo "  2. Wrong community string or SNMPv3 credentials"
    echo "  3. Firewall blocking SNMP requests"
    echo "  4. Old RouterOS version (upgrade recommended)"
    echo ""
    echo "Troubleshooting:"
    echo "  - Check MikroTik: /snmp print"
    echo "  - Check firewall: /ip firewall filter print where dst-port=161"
    echo "  - Update RouterOS to latest stable version"
    exit 1
fi

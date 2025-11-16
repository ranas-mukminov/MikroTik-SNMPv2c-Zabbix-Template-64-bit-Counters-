# MikroTik SNMP Configuration Script
# Compatible with RouterOS 6.x and 7.x
#
# This script configures SNMP on MikroTik for Zabbix monitoring
# Choose ONE configuration method: SNMPv2c OR SNMPv3 (recommended)
#
# BEFORE RUNNING:
# 1. Replace IP addresses with your Zabbix server IP
# 2. Replace passwords/community strings with strong values
# 3. Test configuration before deploying to production

# ============================================================================
# OPTION 1: SNMPv2c Configuration (Basic - for internal networks)
# ============================================================================

# Enable SNMP service
/snmp
set enabled=yes \
    contact="Network Admin <admin@example.com>" \
    location="DataCenter-1, Rack-A5, Position-2U" \
    trap-version=2 \
    trap-community=public \
    trap-generators=""

# Configure SNMPv2c community with IP restriction
# SECURITY: Change "MySecureString123!" to a strong random string
# SECURITY: Change "10.0.0.100/32" to your Zabbix server IP
/snmp community
set [find default=yes] \
    name="MySecureString123!" \
    addresses=10.0.0.100/32 \
    read-access=yes \
    write-access=no

# Alternative: Create new community (if default was removed)
# /snmp community
# add name="MySecureString123!" \
#     addresses=10.0.0.100/32 \
#     read-access=yes \
#     write-access=no

# ============================================================================
# OPTION 2: SNMPv3 Configuration (RECOMMENDED - for production)
# ============================================================================

# Enable SNMP service
/snmp
set enabled=yes \
    contact="Network Admin <admin@example.com>" \
    location="DataCenter-1, Rack-A5, Position-2U" \
    trap-version=3

# Create SNMPv3 user with authentication and encryption
# SECURITY: Change passwords to strong random strings (min 8 characters)
# SECURITY: Change "10.0.0.100/32" to your Zabbix server IP
/snmp community
add name=zabbix_monitor \
    authentication-protocol=SHA1 \
    encryption-protocol=AES \
    authentication-password="ChangeMe_AuthPass_Min8Chars!" \
    encryption-password="ChangeMe_PrivPass_Min8Chars!" \
    addresses=10.0.0.100/32 \
    read-access=yes \
    write-access=no

# Optional: Disable SNMPv1/v2c for maximum security
# (Only do this after confirming SNMPv3 works!)
# /snmp community
# remove [find name!="zabbix_monitor"]

# ============================================================================
# Optional: Configure SNMP Traps (Zabbix can receive SNMP traps)
# ============================================================================

# Set trap target (Zabbix server)
# /snmp
# set trap-target=10.0.0.100 \
#     trap-community=MyTrapCommunity \
#     trap-version=2

# Enable trap generators (optional)
# /snmp
# set trap-generators=interfaces,start-trap

# ============================================================================
# Firewall Configuration (IMPORTANT for Security)
# ============================================================================

# Add firewall rule to restrict SNMP access to Zabbix server only
# Adjust interface name and IP ranges for your environment

# For INPUT chain (SNMP to router itself)
/ip firewall filter
add chain=input \
    protocol=udp \
    dst-port=161 \
    src-address=10.0.0.100/32 \
    action=accept \
    comment="Allow SNMP from Zabbix server" \
    place-before=0

# Drop all other SNMP requests (add after above rule)
/ip firewall filter
add chain=input \
    protocol=udp \
    dst-port=161 \
    action=drop \
    comment="Drop all other SNMP requests" \
    place-before=1

# ============================================================================
# Verification Commands
# ============================================================================

# Check SNMP status
# /snmp print

# Check SNMP communities
# /snmp community print detail

# Check firewall rules
# /ip firewall filter print where dst-port=161

# Monitor SNMP logs
# /log print where topics~"snmp"

# ============================================================================
# Testing from Zabbix Server
# ============================================================================

# Test SNMPv2c (run from Zabbix server):
# snmpwalk -v2c -c MySecureString123! <mikrotik-ip> system
# snmpget -v2c -c MySecureString123! <mikrotik-ip> SNMPv2-MIB::sysUpTime.0

# Test SNMPv3 (run from Zabbix server):
# snmpwalk -v3 -l authPriv \
#   -u zabbix_monitor \
#   -a SHA -A "ChangeMe_AuthPass_Min8Chars!" \
#   -x AES -X "ChangeMe_PrivPass_Min8Chars!" \
#   <mikrotik-ip> system

# ============================================================================
# Advanced: CPU Monitoring via MikroTik-specific OID
# ============================================================================

# Some RouterOS versions support CPU monitoring via:
# OID: 1.3.6.1.4.1.14988.1.1.3.1.0 (mtxrHlProcessorUsage)
#
# Test from Zabbix server:
# snmpget -v2c -c MySecureString123! <mikrotik-ip> 1.3.6.1.4.1.14988.1.1.3.1.0

# ============================================================================
# Troubleshooting
# ============================================================================

# Problem: No SNMP response
# Solution 1: Check if SNMP is enabled
#   /snmp print
#
# Solution 2: Check firewall rules
#   /ip firewall filter print where chain=input and dst-port=161
#
# Solution 3: Check source IP restriction
#   /snmp community print
#
# Solution 4: Check logs for errors
#   /log print where topics~"snmp"

# Problem: "Timeout" errors from Zabbix
# Solution 1: Check network connectivity
#   /tool flood-ping <zabbix-ip> count=10
#
# Solution 2: Increase SNMP timeout on MikroTik (if needed)
#   /snmp set engine-id-suffix=

# Problem: Partial data (some OIDs work, others don't)
# Solution 1: Update RouterOS to latest stable version
# Solution 2: Check if specific MIBs are supported on your device
# Solution 3: Enable additional features (routing packages for OSPF/BGP MIBs)

# ============================================================================
# Security Best Practices
# ============================================================================

# 1. Use SNMPv3 with authentication and encryption
# 2. Restrict SNMP access by source IP (Zabbix server only)
# 3. Use strong, random passwords/community strings (20+ characters)
# 4. Disable write access (read-access=yes, write-access=no)
# 5. Place management interface on isolated VLAN
# 6. Use firewall rules to drop unwanted SNMP requests
# 7. Monitor SNMP logs for unauthorized access attempts
# 8. Regularly update RouterOS to patch security vulnerabilities
# 9. Never use default community strings (public, private)
# 10. Document your SNMP configuration in change management system

# ============================================================================
# Backup and Restore
# ============================================================================

# Export SNMP configuration
# /snmp export file=snmp-config

# Import SNMP configuration
# /import snmp-config.rsc

# ============================================================================
# End of Configuration Script
# ============================================================================

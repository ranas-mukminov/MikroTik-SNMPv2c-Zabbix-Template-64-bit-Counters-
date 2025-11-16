# Examples Directory

This directory contains practical examples and configuration templates for deploying MikroTik SNMP monitoring in Zabbix.

## 📁 Files

### [mikrotik_snmp_config.rsc](mikrotik_snmp_config.rsc)
**Complete MikroTik RouterOS configuration script**

- SNMPv2c configuration with security best practices
- SNMPv3 configuration (recommended for production)
- Firewall rules to restrict SNMP access
- Verification commands
- Troubleshooting guide

**Usage:**
```bash
# Copy-paste sections into MikroTik terminal, OR
# Upload file and import:
/import mikrotik_snmp_config.rsc
```

**Important:** Edit the following before using:
- Replace `10.0.0.100/32` with your Zabbix server IP
- Replace `MySecureString123!` with a strong random string (SNMPv2c)
- Replace `ChangeMe_AuthPass_Min8Chars!` with strong password (SNMPv3)
- Replace `ChangeMe_PrivPass_Min8Chars!` with strong password (SNMPv3)
- Update contact and location information

---

### [zabbix_host_config_example.md](zabbix_host_config_example.md)
**Step-by-step Zabbix host configuration guide**

- SNMPv2c host setup with screenshots descriptions
- SNMPv3 host setup (recommended)
- Host macro customization examples
- Verification steps
- Common issues and solutions

**Covers:**
- Template import
- Host creation
- Interface configuration (SNMP)
- Macro configuration
- Discovery verification
- Troubleshooting

**Use cases included:**
1. Core router (high availability)
2. Edge router (standard monitoring)
3. Branch office (reduced monitoring)
4. CCR router (24V power)
5. Wireless AP (VLAN interfaces)

---

## 🚀 Quick Start

### For MikroTik Configuration:
1. Open [mikrotik_snmp_config.rsc](mikrotik_snmp_config.rsc)
2. Choose SNMPv2c OR SNMPv3 section
3. Edit IP addresses and passwords
4. Copy-paste into MikroTik terminal
5. Test with `snmpwalk` from Zabbix server

### For Zabbix Configuration:
1. Read [zabbix_host_config_example.md](zabbix_host_config_example.md)
2. Follow step-by-step instructions
3. Use macro examples for customization
4. Verify with "Latest data" in Zabbix

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Changed default SNMP community/passwords
- [ ] Restricted SNMP access by IP address
- [ ] Configured firewall rules on MikroTik
- [ ] Using SNMPv3 with authentication and encryption (recommended)
- [ ] Tested SNMP connectivity from Zabbix server
- [ ] Verified no plaintext passwords in configs
- [ ] Documented credentials in password manager
- [ ] Set up monitoring for unauthorized SNMP access

---

## 📚 Additional Resources

### MikroTik Documentation
- [SNMP Configuration Manual](https://wiki.mikrotik.com/wiki/Manual:SNMP)
- [Firewall Configuration](https://wiki.mikrotik.com/wiki/Manual:IP/Firewall/Filter)
- [RouterOS Scripting](https://wiki.mikrotik.com/wiki/Manual:Scripting)

### Zabbix Documentation
- [SNMP Monitoring](https://www.zabbix.com/documentation/current/manual/config/items/itemtypes/snmp)
- [Low-Level Discovery](https://www.zabbix.com/documentation/current/manual/discovery/low_level_discovery)
- [Macros](https://www.zabbix.com/documentation/current/manual/config/macros)

### SNMP Tools
- **snmpwalk** - Command-line SNMP browser (most Linux distributions)
- **iReasoning MIB Browser** - GUI SNMP tool for Windows/Mac/Linux
- **Paessler SNMP Tester** - Free SNMP testing tool

---

## 🤝 Contributing

Have a useful configuration example? Please contribute:

1. Create a new `.rsc` or `.md` file
2. Follow the existing format and documentation style
3. Include security warnings where appropriate
4. Test your example before submitting
5. Submit a Pull Request

---

## ⚠️ Disclaimer

These examples are provided as templates and must be customized for your specific environment. Always test in a non-production environment first. The authors are not responsible for any issues arising from the use of these configurations.

---

**Need help?** Check the main [README](../README.md) or open an issue on GitHub.

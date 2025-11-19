# 🔒 Security Policy

## Reporting a Vulnerability

We take the security of MikroTik SNMP monitoring templates seriously. If you discover a security vulnerability in these templates, please report it responsibly.

### How to Report

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Contact us directly through:
   - 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
   - 💬 Telegram: [@run_as_daemon](https://t.me/run_as_daemon)
   - 🐙 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)

### What to Include

When reporting a vulnerability, please include:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if available)
- Your contact information

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 1 week
- **Fix Timeline:** Depends on severity, typically within 2-4 weeks

---

## 🛡️ Best Practices for Secure SNMP Monitoring

### General Security Recommendations

1. **Use SNMPv3** whenever possible
   - SNMPv2c transmits community strings in plaintext
   - SNMPv3 provides authentication and encryption

2. **Restrict SNMP Access**
   - Configure firewall rules to allow SNMP only from trusted sources
   - Use specific IP addresses, not network ranges
   - Limit SNMP access to management VLANs

3. **Strong Community Strings** (SNMPv2c)
   - Never use default community strings like "public" or "private"
   - Use complex, randomly generated strings (20+ characters)
   - Use different community strings for different devices or groups

4. **Regular Security Audits**
   - Review SNMP access logs regularly
   - Monitor for unauthorized SNMP queries
   - Update templates and Zabbix regularly

5. **Principle of Least Privilege**
   - Use read-only SNMP access for monitoring
   - Avoid SNMP write access unless absolutely necessary
   - Create separate SNMP users for different monitoring systems

---

## 🔐 SNMPv3 Security Configuration

### Recommended SNMPv3 Settings

**Authentication:**
- **Protocol:** SHA-256 (preferred) or SHA-1 (minimum)
- **Password:** Minimum 12 characters, complex
- Never use: MD5 (deprecated, insecure)

**Privacy (Encryption):**
- **Protocol:** AES-256 (preferred) or AES-128 (minimum)
- **Password:** Different from authentication password
- Never use: DES (deprecated, insecure)

### MikroTik SNMPv3 Configuration Example

```bash
# Disable SNMPv2c community
/snmp community
set [find default=yes] disabled=yes

# Configure SNMPv3
/snmp
set enabled=yes contact="security@example.com" location="Secure-DC"

# Create SNMPv3 user with strong security
/snmp user
add name=zabbix-monitor group=read \
    auth-protocol=SHA256 auth-password="StrongAuthPass!2024#Monitoring" \
    encryption-protocol=AES encryption-password="StrongPrivPass!2024#Secure"
```

### Zabbix SNMPv3 Configuration

When configuring SNMPv3 in Zabbix:
- **Security Level:** authPriv (authentication + encryption)
- **Authentication Protocol:** SHA or SHA-256
- **Privacy Protocol:** AES or AES-256
- Store credentials in Zabbix macros, not in plain text

---

## 🚨 Known Security Considerations

### Template-Specific Security Notes

1. **No Credentials in Templates**
   - These templates do not contain hardcoded credentials
   - SNMP community strings are referenced via macros
   - Always override default macro values

2. **Discovery Filters**
   - Low-level discovery rules filter interfaces by type
   - Review and customize filters for your environment
   - Avoid exposing sensitive interface names

3. **Monitoring Data Privacy**
   - SNMP metrics may contain sensitive network information
   - Secure your Zabbix server and database
   - Implement access controls for Zabbix dashboards

4. **Template Updates**
   - Check [CHANGELOG.md](CHANGELOG.md) for security-related updates
   - Review template changes before importing
   - Test updates in a non-production environment first

---

## 🏢 Professional Security Services

Need help securing your monitoring infrastructure?

### Our Security Services

- 🔒 **Security Hardening**
  - SNMPv3 migration and configuration
  - Firewall rules and access control setup
  - Network segmentation for monitoring traffic

- 🛡️ **Security Audits**
  - SNMP configuration review
  - Monitoring infrastructure assessment
  - Compliance verification (PCI-DSS, ISO 27001)

- 📋 **Security Best Practices Implementation**
  - Secure monitoring architecture design
  - Credential management and rotation
  - Encrypted communication setup

- 🎓 **Security Training**
  - SNMPv3 configuration workshops
  - Secure monitoring best practices
  - Incident response for monitoring systems

### Contact for Professional Security Support

> **"Defense by design. Speed by default."**

- 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- 💬 Telegram: [@run_as_daemon](https://t.me/run_as_daemon)
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)

---

## 📚 Additional Security Resources

- [SNMP Best Practices (NIST)](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-40r3.pdf)
- [MikroTik Security Documentation](https://help.mikrotik.com/docs/display/ROS/Security)
- [Zabbix Security Best Practices](https://www.zabbix.com/documentation/current/en/manual/installation/requirements/best_practices)

---

**Last Updated:** 2024  
**Maintainer:** Ranas Mukminov | [run-as-daemon.ru](https://run-as-daemon.ru)

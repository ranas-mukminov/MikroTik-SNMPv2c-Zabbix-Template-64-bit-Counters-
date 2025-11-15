# MikroTik SNMPv2c Zabbix Template (64-bit Counters)

This repository provides a Zabbix 7.0+ ready template for MikroTik routers that focuses on reliable SNMPv2c polling using 64-bit c
ounters, best-practice preprocessing and automatic interface discovery.

## Features

- 📡 SNMPv2c template with configurable community macro (`{$SNMP_COMMUNITY}`)
- 🔍 Interface low-level discovery (LLD) for physical and logical ports (loopbacks/virtual links excluded by default)
- 📈 64-bit inbound/outbound bandwidth converted to bits per second with change-per-second preprocessing
- 🚨 Trigger prototype to alert when an interface operational status transitions to *down*
- 🧮 Error rate monitoring for inbound/outbound errors (per-second delta)
- 🧾 System uptime (converted from timeticks) and descriptive inventory information
- ✅ Compatible with Zabbix 7.0+ and uses stable 32-character UUIDs

## Import instructions

1. Go to **Configuration → Templates** in Zabbix.
2. Click **Import**.
3. Select `template_mikrotik_snmpv2c_zbx72_uuid32.xml` from this repository.
4. ✅ Enable "Create missing" and "Update existing".
5. Import — done!

## Customisation tips

- Override `{$SNMP_COMMUNITY}` per host to match your MikroTik SNMPv2c community string.
- Adjust the discovery rule filter regex if you need to include (or exclude) additional interface types.
- Tune polling intervals on the prototypes when monitoring very high-throughput links to match your retention needs.

## Помощь в настройке MikroTik для организаций

Если вам требуется профессиональная помощь в настройке MikroTik для вашей организации, вы можете обратиться ко мне напрямую на с
айте [run-as-daemon.ru](https://run-as-daemon.ru).

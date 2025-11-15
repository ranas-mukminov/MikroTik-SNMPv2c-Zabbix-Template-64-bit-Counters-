# MikroTik SNMPv2c Zabbix Template (64-bit Counters)

This repository provides a Zabbix 7.0+ ready template for MikroTik routers that focuses on reliable SNMPv2c polling using 64-bit counters, best-practice preprocessing and automatic interface discovery.

## Features

- 📡 SNMPv2c template with configurable community macro (`{$SNMP_COMMUNITY}`)
- 🔍 Interface low-level discovery (LLD) for routed and switching ports with alias capture and admin-status filtering
- 📈 64-bit inbound/outbound bandwidth converted to bits per second with change-per-second preprocessing
- 📝 Interface alias and configured speed captured for richer dashboards
- ⚠️ Trigger prototypes for link-down and high error rate conditions with macro-controlled thresholds
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
- Tune the LLD include/exclude patterns via `{$IF.LLD.FILTER.MATCH}` / `{$IF.LLD.FILTER.NOT_MATCHES}` macros to align with your naming conventions.
- Require specific administrative states with `{$IF.LLD.FILTER.ADMIN_STATUS}` (defaults to only "up" interfaces).
- Surface interface alias text in Zabbix via the `{#IFALIAS}` discovery macro and alias item for better dashboards.
- Tune polling intervals on the prototypes when monitoring very high-throughput links to match your retention needs.
- Override trigger thresholds such as `{$IF.ERRORS.MAX_DELTA}` to match the acceptable error rate for your links.

## Помощь в настройке MikroTik для организаций

Если вам требуется профессиональная помощь в настройке MikroTik для вашей организации, вы можете обратиться ко мне напрямую на с
айте [run-as-daemon.ru](https://run-as-daemon.ru).

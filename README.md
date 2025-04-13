# MikroTik SNMPv2c Zabbix Template (64-bit Counters)

This is a minimal and clean Zabbix 7.2+ compatible template for monitoring MikroTik routers via SNMPv2c using 64-bit traffic counters.

## Features

- 📡 SNMPv2c support
- 📥 64-bit traffic input counter: `ifHCInOctets`
- ✅ Compatible with Zabbix 7.2+
- 🔐 Proper UUID formatting for import
- 🧩 Template group: `Templates`

## Import instructions

1. Go to **Configuration → Templates** in Zabbix
2. Click **Import**
3. Select `template_mikrotik_snmpv2c_zbx72_uuid32.xml`
4. ✅ Enable "Create missing" and "Update existing"
5. Import — done!

## Future improvements (coming soon or PR welcome)

- Outbound traffic monitoring (`ifHCOutOctets`)
- Interface discovery (LLD)
- Link/CRC status
- Graphs and triggers

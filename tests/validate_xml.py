#!/usr/bin/env python3
"""
Zabbix Template XML Validator

This script validates Zabbix template XML files for:
- Well-formed XML structure
- Unique UUIDs
- Required elements presence
- Macro syntax
- Item key syntax
- OID format

Usage:
    python3 validate_xml.py ../template_mikrotik_snmpv2c_advanced_zbx72.xml
    python3 validate_xml.py --all  # Validate all XML files in parent directory
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class TemplateValidator:
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.tree = None
        self.root = None
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def validate(self) -> bool:
        """Run all validations and return success status"""
        print(f"\n{BLUE}Validating: {os.path.basename(self.xml_path)}{RESET}")
        print("=" * 70)

        # Step 1: Parse XML
        if not self._parse_xml():
            return False

        # Step 2: Validate structure
        self._validate_version()
        self._validate_template_metadata()

        # Step 3: Validate UUIDs
        self._validate_uuids()

        # Step 4: Validate items
        self._validate_items()

        # Step 5: Validate macros
        self._validate_macros()

        # Step 6: Validate triggers
        self._validate_triggers()

        # Step 7: Validate value maps
        self._validate_value_maps()

        # Print results
        self._print_results()

        return len(self.errors) == 0

    def _parse_xml(self) -> bool:
        """Parse and validate XML structure"""
        try:
            self.tree = ET.parse(self.xml_path)
            self.root = self.tree.getroot()
            self.info.append("✓ XML is well-formed")
            return True
        except ET.ParseError as e:
            self.errors.append(f"XML parse error: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.xml_path}")
            return False

    def _validate_version(self):
        """Validate Zabbix export version"""
        version = self.root.get("version")
        if not version:
            self.errors.append("Missing zabbix_export version attribute")
        elif version != "7.0":
            self.warnings.append(f"Export version is {version}, expected 7.0")
        else:
            self.info.append(f"✓ Export version: {version}")

    def _validate_template_metadata(self):
        """Validate template metadata"""
        template = self.root.find(".//template")
        if template is None:
            self.errors.append("No template element found")
            return

        # Check required fields
        required_fields = ["uuid", "template", "name"]
        for field in required_fields:
            elem = template.find(field)
            if elem is None or not elem.text:
                self.errors.append(f"Template missing required field: {field}")
            else:
                self.info.append(f"✓ Template {field}: {elem.text}")

        # Check template group
        group = template.find(".//group/name")
        if group is not None:
            self.info.append(f"✓ Template group: {group.text}")
            if "Templates/Network" not in group.text:
                self.warnings.append(
                    "Template group should be 'Templates/Network devices' for Zabbix 7.0"
                )

    def _validate_uuids(self):
        """Validate UUID uniqueness and format"""
        uuids = defaultdict(list)
        uuid_pattern = re.compile(r"^[a-f0-9]{32}$")

        # Collect all UUIDs
        for elem in self.root.iter():
            if elem.tag == "uuid" and elem.text:
                uuid = elem.text.strip()

                # Check format
                if not uuid_pattern.match(uuid):
                    self.errors.append(f"Invalid UUID format: {uuid}")

                # Track duplicates
                parent = self._get_element_path(elem)
                uuids[uuid].append(parent)

        # Check for duplicates
        duplicates = {uuid: paths for uuid, paths in uuids.items() if len(paths) > 1}
        if duplicates:
            for uuid, paths in duplicates.items():
                self.errors.append(f"Duplicate UUID {uuid} found in: {', '.join(paths)}")
        else:
            self.info.append(f"✓ All {len(uuids)} UUIDs are unique")

    def _validate_items(self):
        """Validate item definitions"""
        items = self.root.findall(".//item") + self.root.findall(".//item_prototype")

        if not items:
            self.warnings.append("No items found in template")
            return

        self.info.append(f"✓ Found {len(items)} items/item prototypes")

        for item in items:
            name = item.find("name")
            key = item.find("key")
            item_type = item.find("type")

            # Validate item has name and key
            if name is None or not name.text:
                self.errors.append("Item missing name")
            if key is None or not key.text:
                self.errors.append(
                    f"Item '{name.text if name is not None else 'unknown'}' missing key"
                )
                continue

            key_text = key.text

            # Validate SNMP items have OID
            if item_type is not None and item_type.text == "SNMP_AGENT":
                oid = item.find("snmp_oid")
                if oid is None or not oid.text:
                    self.errors.append(f"SNMP item '{name.text}' missing snmp_oid")
                else:
                    self._validate_oid(oid.text, name.text)

            # Validate key syntax
            if not self._validate_item_key(key_text):
                self.errors.append(f"Invalid item key syntax: {key_text}")

            # Check for preprocessing on CHANGE_PER_SECOND items
            if "bandwidth" in key_text or "error" in key_text or "discard" in key_text:
                preprocessing = item.find(".//preprocessing")
                if preprocessing is None:
                    item_name = name.text if name is not None and name.text else "unknown"
                    self.warnings.append(
                        f"Item '{item_name}' may need CHANGE_PER_SECOND preprocessing"
                    )

    def _validate_oid(self, oid: str, item_name: str):
        """Validate SNMP OID format"""
        # OID can be numeric (1.3.6.1...) or MIB name (IF-MIB::ifIndex)
        numeric_oid_pattern = re.compile(r"^\.?\d+(\.\d+)*$")
        mib_oid_pattern = re.compile(r"^[A-Z][A-Z0-9-]*::[a-zA-Z][a-zA-Z0-9]*")

        if not (numeric_oid_pattern.match(oid) or mib_oid_pattern.match(oid) or "discovery" in oid):
            self.warnings.append(f"Unusual OID format in '{item_name}': {oid}")

    def _validate_item_key(self, key: str) -> bool:
        """Validate item key syntax"""
        # Basic validation: key[params]
        key_pattern = re.compile(r"^[a-zA-Z0-9._-]+(\[.*\])?$")
        return bool(key_pattern.match(key))

    def _validate_macros(self):
        """Validate macro definitions"""
        # Only get macros from template/macros section, not from LLD filters
        macros = self.root.findall(".//template/macros/macro")

        if not macros:
            self.warnings.append("No macros found in template")
            return

        self.info.append(f"✓ Found {len(macros)} macros")

        required_macros = {
            "SNMPv2c": ["{$SNMP_COMMUNITY}"],
            "SNMPv3": ["{$SNMPV3_USER}", "{$SNMPV3_AUTH_PASSPHRASE}", "{$SNMPV3_PRIV_PASSPHRASE}"],
        }

        macro_names = []
        for macro in macros:
            name = macro.find("macro")
            value = macro.find("value")

            if name is None or not name.text:
                self.errors.append("Macro missing name")
                continue

            macro_names.append(name.text)

            # Check macro syntax
            if not (name.text.startswith("{$") and name.text.endswith("}")):
                self.errors.append(f"Invalid macro syntax: {name.text}")

            # Check for security issues
            if value is not None and value.text:
                if "public" in value.text.lower() and "COMMUNITY" in name.text:
                    self.errors.append(
                        f"Security risk: Macro {name.text} uses default 'public' value"
                    )

        # Check for required macros (either SNMPv2c or SNMPv3)
        has_v2_macros = all(m in macro_names for m in required_macros["SNMPv2c"])
        has_v3_macros = all(m in macro_names for m in required_macros["SNMPv3"])

        if not (has_v2_macros or has_v3_macros):
            self.warnings.append("Template missing expected SNMP authentication macros")

    def _validate_triggers(self):
        """Validate trigger definitions"""
        triggers = self.root.findall(".//trigger") + self.root.findall(".//trigger_prototype")

        if not triggers:
            self.warnings.append("No triggers found in template")
            return

        self.info.append(f"✓ Found {len(triggers)} triggers/trigger prototypes")

        for trigger in triggers:
            name = trigger.find("name")
            expression = trigger.find("expression")
            priority = trigger.find("priority")

            if name is None or not name.text:
                self.errors.append("Trigger missing name")

            if expression is None or not expression.text:
                self.errors.append(
                    f"Trigger '{name.text if name else 'unknown'}' missing expression"
                )

            if priority is None or not priority.text:
                self.warnings.append(
                    f"Trigger '{name.text if name else 'unknown'}' missing priority"
                )

    def _validate_value_maps(self):
        """Validate value map definitions"""
        value_maps = self.root.findall(".//value_map")

        if value_maps:
            self.info.append(f"✓ Found {len(value_maps)} value maps")

            for vm in value_maps:
                name = vm.find("name")
                mappings = vm.findall(".//mapping")

                if name is None or not name.text:
                    self.errors.append("Value map missing name")
                elif not mappings:
                    self.warnings.append(f"Value map '{name.text}' has no mappings")

    def _get_element_path(self, elem) -> str:
        """Get descriptive path for an element"""
        parent = elem.getparent() if hasattr(elem, "getparent") else None
        if parent is not None:
            name_elem = parent.find("name")
            if name_elem is not None and name_elem.text:
                return name_elem.text
        return elem.tag

    def _print_results(self):
        """Print validation results"""
        print()

        # Print info
        if self.info:
            print(f"{BLUE}Information:{RESET}")
            for msg in self.info:
                print(f"  {msg}")
            print()

        # Print warnings
        if self.warnings:
            print(f"{YELLOW}Warnings ({len(self.warnings)}):{RESET}")
            for msg in self.warnings:
                print(f"  ⚠ {msg}")
            print()

        # Print errors
        if self.errors:
            print(f"{RED}Errors ({len(self.errors)}):{RESET}")
            for msg in self.errors:
                print(f"  ✗ {msg}")
            print()

        # Print summary
        if self.errors:
            print(f"{RED}✗ VALIDATION FAILED{RESET}")
            return False
        elif self.warnings:
            print(f"{YELLOW}⚠ VALIDATION PASSED WITH WARNINGS{RESET}")
            return True
        else:
            print(f"{GREEN}✓ VALIDATION PASSED{RESET}")
            return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_xml.py <template.xml>")
        print("       python3 validate_xml.py --all")
        sys.exit(1)

    files_to_validate = []

    if sys.argv[1] == "--all":
        # Find all XML files in parent directory
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for file in os.listdir(parent_dir):
            if file.endswith(".xml"):
                files_to_validate.append(os.path.join(parent_dir, file))
    else:
        files_to_validate = sys.argv[1:]

    if not files_to_validate:
        print("No XML files found to validate")
        sys.exit(1)

    print(f"\n{BLUE}╔════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║  Zabbix Template XML Validator                                    ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════════════════════╝{RESET}")

    all_passed = True
    results = {}

    for xml_file in files_to_validate:
        validator = TemplateValidator(xml_file)
        passed = validator.validate()
        results[xml_file] = passed
        all_passed = all_passed and passed

    # Print summary
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}Summary:{RESET}")
    print()

    for xml_file, passed in results.items():
        status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
        print(f"  {status}  {os.path.basename(xml_file)}")

    print()
    if all_passed:
        print(f"{GREEN}All validations passed!{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}Some validations failed!{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Validation tests for MikroTik Zabbix templates."""
from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_GLOB = "template_*.xml"
TEMPLATE_PATHS = sorted(REPO_ROOT.glob(TEMPLATE_GLOB))

# Macros that every template relies on for interface discovery logic.
BASE_REQUIRED_MACROS = {
    "{$IF.LLD.FILTER.MATCH}",
    "{$IF.LLD.FILTER.NOT_MATCHES}",
    "{$IF.LLD.FILTER.ADMIN_STATUS}",
    "{$IF.ERRORS.MAX_DELTA}",
}

SNMPV2_REQUIRED_MACROS = {"{$SNMP_COMMUNITY}"}
SNMPV3_REQUIRED_MACROS = {
    "{$SNMPV3_USER}",
    "{$SNMPV3_AUTH_PROTOCOL}",
    "{$SNMPV3_AUTH_PASSPHRASE}",
    "{$SNMPV3_PRIV_PROTOCOL}",
    "{$SNMPV3_PRIV_PASSPHRASE}",
    "{$SNMPV3_SECURITY_LEVEL}",
}


def _load_template(path: Path) -> ET.Element:
    """Parse a template XML file and return the root element."""
    tree = ET.parse(path)
    return tree.getroot()


@pytest.mark.parametrize("template_path", TEMPLATE_PATHS, ids=lambda p: p.name)
def test_template_structure(template_path: Path) -> None:
    """Ensure each template has the expected structural nodes."""
    root = _load_template(template_path)
    assert root.tag == "zabbix_export", "Template must be wrapped in <zabbix_export>"

    templates = root.find("templates")
    assert templates is not None, "Missing <templates> node"

    template_nodes = templates.findall("template")
    assert template_nodes, "Template list should contain at least one <template> entry"

    # Basic sanity checks for human-facing metadata
    for template in template_nodes:
        assert template.findtext("name"), "Template entries must declare a <name>"
        assert template.findtext("description"), "Template entries must include a <description>"


@pytest.mark.parametrize("template_path", TEMPLATE_PATHS, ids=lambda p: p.name)
def test_template_macros(template_path: Path) -> None:
    """Validate that critical macros are declared in every template variant."""
    root = _load_template(template_path)
    macros_node = root.find(".//template/macros")
    assert macros_node is not None, "Templates should define a <macros> block"

    defined_macros = {macro.findtext("macro") for macro in macros_node.findall("macro")}

    missing = sorted(BASE_REQUIRED_MACROS - defined_macros)
    assert not missing, f"Missing base macros: {', '.join(missing)}"

    filename = template_path.name.lower()
    if "snmpv3" in filename:
        missing = sorted(SNMPV3_REQUIRED_MACROS - defined_macros)
        assert not missing, f"Missing SNMPv3 macros: {', '.join(missing)}"
    else:
        missing = sorted(SNMPV2_REQUIRED_MACROS - defined_macros)
        assert not missing, f"Missing SNMPv2c macros: {', '.join(missing)}"

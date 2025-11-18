"""Pytest-based structural checks for Zabbix template exports."""
from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATTERN = "template_*.xml"

# Macros that every template should provide to keep interface discovery configurable.
BASE_REQUIRED_MACROS = {
    "{$IF.LLD.FILTER.MATCH}",
    "{$IF.LLD.FILTER.NOT_MATCHES}",
    "{$IF.LLD.FILTER.ADMIN_STATUS}",
    "{$IF.ERRORS.MAX_DELTA}",
}

# Additional macro requirements derived from the security guidance in README.md
# and the supported SNMP authentication modes.
REQUIRED_MACROS_BY_KEYWORD = {
    "snmpv2c": {
        "{$SNMP_COMMUNITY}",
    },
    "snmpv3": {
        "{$SNMPV3_USER}",
        "{$SNMPV3_AUTH_PROTOCOL}",
        "{$SNMPV3_AUTH_PASSPHRASE}",
        "{$SNMPV3_PRIV_PROTOCOL}",
        "{$SNMPV3_PRIV_PASSPHRASE}",
        "{$SNMPV3_SECURITY_LEVEL}",
    },
}


def _template_files() -> list[Path]:
    files = sorted(REPO_ROOT.glob(TEMPLATE_PATTERN))
    if not files:
        pytest.fail(f"No files matching {TEMPLATE_PATTERN!r} were found at {REPO_ROOT}.")
    return files


def _text(element: ET.Element, tag: str, filename: str) -> str:
    child = element.find(tag)
    assert child is not None, f"{filename}: missing <{tag}> element"
    text = (child.text or "").strip()
    assert text, f"{filename}: <{tag}> must not be empty"
    return text


def _macros_from(template_el: ET.Element) -> set[str]:
    macros: set[str] = set()
    for macro_entry in template_el.findall("./macros/macro"):
        name = (macro_entry.findtext("macro") or "").strip()
        if name:
            macros.add(name)
    return macros


def _required_macros(path: Path) -> set[str]:
    required = set(BASE_REQUIRED_MACROS)
    lower_name = path.name.lower()
    for keyword, macros in REQUIRED_MACROS_BY_KEYWORD.items():
        if keyword in lower_name:
            required.update(macros)
    return required


@pytest.mark.parametrize("template_path", _template_files())
def test_template_structure(template_path: Path) -> None:
    """Ensure each template can be parsed and has the expected metadata/macros."""

    try:
        tree = ET.parse(template_path)
    except ET.ParseError as exc:  # pragma: no cover - pytest displays failure context
        pytest.fail(f"Failed to parse {template_path.name}: {exc}")

    root = tree.getroot()
    assert root.tag == "zabbix_export", f"{template_path.name}: unexpected root tag {root.tag!r}"

    templates = root.findall("./templates/template")
    assert templates, f"{template_path.name}: no <template> elements found"

    required_macros = _required_macros(template_path)

    for template_el in templates:
        _text(template_el, "uuid", template_path.name)
        _text(template_el, "template", template_path.name)
        _text(template_el, "name", template_path.name)

        macros = _macros_from(template_el)
        assert macros, f"{template_path.name}: at least one macro must be defined"

        missing = required_macros - macros
        assert not missing, (
            f"{template_path.name}: missing required macros {sorted(missing)} "
            f"(expected {sorted(required_macros)})"
        )

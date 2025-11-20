from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - fallback when PyYAML is unavailable
    yaml = None  # type: ignore[assignment]


def load_yaml(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    text = file_path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text) or {}
    return _simple_yaml(text)


def _simple_yaml(text: str) -> dict[str, Any]:
    """Very small YAML subset parser for key/value pairs."""

    data: dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = _coerce(value.strip())
    return data


def _coerce(value: str) -> Any:
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value

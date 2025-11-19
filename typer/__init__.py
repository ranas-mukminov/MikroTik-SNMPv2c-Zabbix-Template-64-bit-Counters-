from __future__ import annotations

import inspect
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List


class BadParameter(Exception):
    """Raised when CLI arguments are invalid."""


@dataclass
class OptionInfo:
    default: Any
    help: str = ""
    case_sensitive: bool = True


def Option(default: Any = inspect._empty, **kwargs: Any) -> OptionInfo:
    return OptionInfo(default=default, **kwargs)


class Typer:
    def __init__(self, help: str | None = None) -> None:
        self.help = help or ""
        self._commands: Dict[str, Callable[..., Any]] = {}

    def command(self, name: str | None = None):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            cmd_name = (name or func.__name__).replace("_", "-")
            self._commands[cmd_name] = func
            return func

        return decorator

    def __call__(self) -> None:
        self._run_cli(sys.argv[1:])

    def _run_cli(self, args: List[str]) -> None:
        if not args:
            raise SystemExit(0)
        command_name = args[0]
        func = self._commands.get(command_name)
        if not func:
            raise SystemExit(f"Unknown command: {command_name}")
        try:
            kwargs = self._parse_args(func, args[1:])
            func(**kwargs)
        except BadParameter as exc:  # pragma: no cover - exercised via CLI
            raise SystemExit(f"Error: {exc}") from exc

    def _parse_args(self, func: Callable[..., Any], tokens: List[str]) -> Dict[str, Any]:
        sig = inspect.signature(func)
        kwargs: Dict[str, Any] = {}
        idx = 0
        while idx < len(tokens):
            token = tokens[idx]
            if not token.startswith("--"):
                raise BadParameter(f"Unexpected argument: {token}")
            key = token[2:].replace("-", "_")
            idx += 1
            param = sig.parameters.get(key)
            if param is None:
                raise BadParameter(f"Unknown option: --{key}")
            default = param.default
            option_info = default if isinstance(default, OptionInfo) else None
            default_value = option_info.default if option_info else default
            annotation = param.annotation
            if annotation is bool or isinstance(default_value, bool):
                kwargs[key] = True
                continue
            if idx >= len(tokens):
                raise BadParameter(f"Missing value for --{key}")
            value = self._convert(tokens[idx], annotation)
            idx += 1
            kwargs[key] = value
        for name, param in sig.parameters.items():
            if name in kwargs:
                continue
            default = param.default
            option_info = default if isinstance(default, OptionInfo) else None
            default_value = option_info.default if option_info else default
            if default_value is inspect._empty:
                raise BadParameter(f"Missing required option --{name.replace('_', '-')}")
            kwargs[name] = default_value
        return kwargs

    def _convert(self, value: str, annotation: Any) -> Any:
        if annotation in (inspect._empty, str, Any):
            return value
        if annotation is Path:
            return Path(value)
        if annotation is int:
            return int(value)
        if annotation is float:
            return float(value)
        if annotation is bool:
            return value.lower() in {"1", "true", "yes", "on"}
        return value


from . import testing  # noqa: E402  # pylint: disable=wrong-import-position

__all__ = ["Typer", "Option", "BadParameter", "testing", "echo"]


def echo(message: str) -> None:
    print(message)

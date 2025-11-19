from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Any, List
import contextlib


@dataclass
class Result:
    exit_code: int
    stdout: str
    stderr: str
    exception: Exception | None = None


class CliRunner:
    def invoke(self, app, args: List[str]):
        stdout = StringIO()
        stderr = StringIO()
        exit_code = 0
        exc: Exception | None = None
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                app._run_cli([str(arg) for arg in args])  # type: ignore[attr-defined]
        except SystemExit as sys_exit:
            exit_code = sys_exit.code if isinstance(sys_exit.code, int) else 1
        except Exception as error:  # pragma: no cover - debugging helper
            exit_code = 1
            exc = error
        return Result(exit_code=exit_code, stdout=stdout.getvalue(), stderr=stderr.getvalue(), exception=exc)

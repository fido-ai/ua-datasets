"""Lightweight shim for Python <3.11 environments expecting stdlib 'tomllib'.

If running on Python 3.11+ the real stdlib 'tomllib' should be preferred and
this module will typically be ignored (because the stdlib shadows it).

For Python 3.10, ensure 'tomli' is installed (declared as an optional
compat dependency). This shim exposes the minimal public surface used by
most tooling: 'load' and 'loads'.
"""
from __future__ import annotations

try:  # pragma: no cover - environment dependent
    import tomli as _tomli  # type: ignore
except ModuleNotFoundError as exc:  # pragma: no cover - only on missing tomli
    raise ModuleNotFoundError(
        "tomllib shim requires 'tomli' on Python <3.11. Install with 'pip install tomli'."
    ) from exc

__all__ = ["load", "loads"]


def loads(s: str, /):  # type: ignore[override]
    return _tomli.loads(s)


def load(fp, /):  # type: ignore[override]
    return _tomli.load(fp)

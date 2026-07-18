"""Opaque payload helpers for port adapters.

Application and Studio ports exchange opaque ``dict`` summaries so that
consumers never couple to concrete DTO types across bounded contexts.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


def to_opaque(value: Any) -> Any:
    """Convert snapshots / dataclasses / enums into JSON-friendly opaque data."""
    if value is None:
        return None
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {k: to_opaque(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): to_opaque(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [to_opaque(v) for v in value]
    if isinstance(value, str | int | float | bool):
        return value
    if hasattr(value, "__dict__") and not isinstance(value, type):
        return {
            k: to_opaque(v)
            for k, v in vars(value).items()
            if not k.startswith("_")
        }
    return str(value)


def opaque_dict(value: Any) -> dict[str, Any]:
    """Require a mapping payload; wrap scalars under ``value`` when needed."""
    converted = to_opaque(value)
    if isinstance(converted, dict):
        return dict(converted)
    return {"value": converted}

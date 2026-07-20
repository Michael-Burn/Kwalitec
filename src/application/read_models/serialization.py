"""Serialize immutable read models into dashboard JSON mappings.

Presentation concern only — no educational interpretation.
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any


def to_dashboard_json(read_model: Any) -> dict[str, Any]:
    """Convert a frozen read-model dataclass into a JSON-ready mapping.

    Args:
        read_model: An immutable read-model instance (frozen dataclass).

    Returns:
        A plain ``dict`` suitable for ``jsonify`` / dashboard API responses.
        Nested tuples become lists so the payload is JSON-native.

    Raises:
        TypeError: If ``read_model`` is not a dataclass instance.
    """
    if not is_dataclass(read_model) or isinstance(read_model, type):
        raise TypeError("read_model must be a dataclass instance")
    result = _to_json_value(read_model)
    if not isinstance(result, dict):
        raise TypeError("read_model serialization must produce a mapping")
    return result


def _to_json_value(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {f.name: _to_json_value(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, tuple | list):
        return [_to_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_json_value(item) for key, item in value.items()}
    return value

"""DTO ↔ SQLAlchemy model column translation helpers.

Converts nested persistence DTOs to JSON-friendly column values and back.
No educational behaviour.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, fields, is_dataclass
from datetime import UTC, datetime
from types import UnionType
from typing import Any, Union, get_args, get_origin, get_type_hints


def column_values_from_dto(dto: Any) -> dict[str, Any]:
    """Flatten a persistence DTO into SQLAlchemy column kwargs (JSON-safe)."""
    if not is_dataclass(dto):
        raise TypeError(f"expected dataclass DTO, got {type(dto)!r}")
    return asdict(dto)


def dto_from_column_values(dto_cls: type[Any], values: Mapping[str, Any]) -> Any:
    """Rebuild a persistence DTO from model/JSON column values."""
    if not is_dataclass(dto_cls):
        raise TypeError(f"expected dataclass type, got {dto_cls!r}")
    hints = get_type_hints(dto_cls)
    kwargs: dict[str, Any] = {}
    for field in fields(dto_cls):
        kwargs[field.name] = _coerce(hints[field.name], values[field.name])
    return dto_cls(**kwargs)


def model_from_dto(model_cls: type[Any], dto: Any) -> Any:
    """Construct a SQLAlchemy model instance from a persistence DTO."""
    return model_cls(**column_values_from_dto(dto))


def dto_from_model(dto_cls: type[Any], model: Any) -> Any:
    """Build a persistence DTO from a SQLAlchemy model row."""
    values = {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
    }
    return dto_from_column_values(dto_cls, values)


def _coerce(annotation: Any, raw: Any) -> Any:
    if raw is None:
        return None

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is Union or origin is UnionType:
        non_none = [arg for arg in args if arg is not type(None)]
        if len(non_none) == 1:
            return _coerce(non_none[0], raw)
        for arg in non_none:
            try:
                return _coerce(arg, raw)
            except (TypeError, ValueError, KeyError):
                continue
        raise TypeError(f"cannot coerce {raw!r} to {annotation!r}")

    if origin is tuple:
        inner = args[0] if args else Any
        if not isinstance(raw, list | tuple):
            raise TypeError(
                f"expected list/tuple for {annotation!r}, got {type(raw)!r}"
            )
        return tuple(_coerce(inner, item) for item in raw)

    if origin is list:
        inner = args[0] if args else Any
        if not isinstance(raw, list | tuple):
            raise TypeError(f"expected list for {annotation!r}, got {type(raw)!r}")
        return [_coerce(inner, item) for item in raw]

    if is_dataclass(annotation):
        if not isinstance(raw, Mapping):
            raise TypeError(
                f"expected mapping for {annotation!r}, got {type(raw)!r}"
            )
        return dto_from_column_values(annotation, raw)

    if annotation is datetime and isinstance(raw, datetime):
        # SQLite (and some drivers) return naive UTC timestamps. Domain and
        # DTO equality require timezone-aware UTC datetimes.
        if raw.tzinfo is None:
            return raw.replace(tzinfo=UTC)
        return raw.astimezone(UTC)

    return raw

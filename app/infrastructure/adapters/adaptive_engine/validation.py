"""Input validation for Adaptive Input Assembler (MS-003 A1).

Validates collected / normalized Adaptive inputs. Does not repair or estimate
missing educational values.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.adaptive_engine.collectors import CollectorResult
from app.infrastructure.adapters.adaptive_engine.provenance import (
    AVAILABILITY_STATUSES,
    AVAILABILITY_UNAVAILABLE,
    INPUT_FIELD_NAMES,
    FieldProvenance,
)


class AdaptiveInputValidationError(ValueError):
    """Raised when assembled Adaptive inputs violate contract rules."""


def validate_student_id(student_id: str) -> str:
    """Return stripped non-empty student_id or raise."""
    sid = (student_id or "").strip()
    if not sid:
        raise AdaptiveInputValidationError("student_id must be a non-empty string")
    return sid


def validate_as_of(as_of: str | None) -> str | None:
    """Validate optional as_of clock (ISO string or None — never auto-generated)."""
    if as_of is None:
        return None
    if not isinstance(as_of, str):
        raise AdaptiveInputValidationError("as_of must be an ISO string or None")
    text = as_of.strip()
    return text or None


def validate_collector_result(result: CollectorResult, *, field_name: str) -> None:
    """Validate a single collector result contract."""
    if not isinstance(result, CollectorResult):
        raise AdaptiveInputValidationError(
            f"{field_name}: collector must return CollectorResult"
        )
    if not result.source_service or not result.source_entity:
        raise AdaptiveInputValidationError(
            f"{field_name}: source_service and source_entity are required"
        )
    if not result.available and not (result.unavailable_reason or "").strip():
        raise AdaptiveInputValidationError(
            f"{field_name}: unavailable_reason required when unavailable"
        )


def validate_provenance_map(
    field_provenance: Mapping[str, Any],
    *,
    required_fields: tuple[str, ...] = INPUT_FIELD_NAMES,
) -> None:
    """Ensure every Adaptive input field exposes complete provenance."""
    for name in required_fields:
        if name not in field_provenance:
            raise AdaptiveInputValidationError(
                f"field_provenance missing entry for {name}"
            )
        entry = field_provenance[name]
        if isinstance(entry, FieldProvenance):
            payload = entry.to_canonical_dict()
        elif isinstance(entry, Mapping):
            payload = dict(entry)
        else:
            raise AdaptiveInputValidationError(
                f"field_provenance[{name}] must be a mapping"
            )
        for key in (
            "source_service",
            "source_entity",
            "collected_at",
            "availability",
        ):
            if key not in payload:
                raise AdaptiveInputValidationError(
                    f"field_provenance[{name}] missing {key}"
                )
        availability = str(payload.get("availability") or "").strip().lower()
        if availability not in AVAILABILITY_STATUSES:
            raise AdaptiveInputValidationError(
                f"field_provenance[{name}] invalid availability"
            )
        if availability == AVAILABILITY_UNAVAILABLE and not str(
            payload.get("unavailable_reason") or ""
        ).strip():
            raise AdaptiveInputValidationError(
                f"field_provenance[{name}] unavailable without reason"
            )


def validate_unavailable_payload_empty(
    *,
    field_name: str,
    availability: str,
    payload: Any,
) -> None:
    """Unavailable fields must not carry invented educational payloads."""
    if availability != AVAILABILITY_UNAVAILABLE:
        return
    if payload in (None, "", {}, []):
        return
    if isinstance(payload, Mapping) and not payload:
        return
    if isinstance(payload, list | tuple) and not payload:
        return
    # Allow empty structured shells only.
    if isinstance(payload, Mapping):
        material = {
            k: v
            for k, v in payload.items()
            if k
            not in {
                "attempt_count",
                "authorised_count",
                "attempts",
                "history",
                "history_count",
                "today",
                "leaves",
                "leaf_count",
                "overall",
                "coverage",
                "review_backlog",
            }
            and v not in (None, "", {}, [], 0)
        }
        empty_ok = not material and all(
            (not v) if isinstance(v, list | dict) else v in (None, "", 0, False)
            for k, v in payload.items()
            if k
            in {
                "attempts",
                "history",
                "leaves",
                "overall",
                "coverage",
                "review_backlog",
                "today",
            }
        )
        if empty_ok:
            return
    raise AdaptiveInputValidationError(
        f"{field_name}: unavailable fields must not carry educational payloads"
    )


def validate_no_estimation_markers(payload: Any, *, field_name: str) -> None:
    """Reject payloads that claim estimated / inferred educational values."""
    forbidden_keys = {
        "estimated",
        "inferred",
        "fabricated",
        "guessed_score",
        "synthetic",
    }

    def _walk(node: Any, path: str) -> None:
        if isinstance(node, Mapping):
            for key, value in node.items():
                key_l = str(key).lower()
                if key_l in forbidden_keys:
                    raise AdaptiveInputValidationError(
                        f"{field_name}: forbidden estimation key at {path}.{key}"
                    )
                _walk(value, f"{path}.{key}")
        elif isinstance(node, list | tuple):
            for idx, item in enumerate(node):
                _walk(item, f"{path}[{idx}]")

    _walk(payload, field_name)


def assert_available_status(availability: str) -> str:
    status = (availability or "").strip().lower()
    if status not in AVAILABILITY_STATUSES:
        raise AdaptiveInputValidationError(f"invalid availability: {availability!r}")
    return status

"""Validation for Twin Facet Synthesis (MS-004 T1).

Validates Runtime A evidence and synthesised facet contracts. Does not repair
or estimate missing educational values.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    TWIN_FACET_NAMES,
    TwinProvenance,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FACET_SYNTHESIS_ORDER,
)


class TwinFacetValidationError(ValueError):
    """Raised when Twin facet synthesis inputs or outputs violate contracts."""


def validate_student_id(student_id: str) -> str:
    """Return stripped non-empty student_id or raise."""
    sid = (student_id or "").strip()
    if not sid:
        raise TwinFacetValidationError("student_id must be a non-empty string")
    return sid


def validate_as_of(as_of: str | None) -> str | None:
    """Validate optional as_of clock (ISO string or None — never auto-generated)."""
    if as_of is None:
        return None
    if not isinstance(as_of, str):
        raise TwinFacetValidationError("as_of must be an ISO string or None")
    text = as_of.strip()
    return text or None


def validate_facet_provenance_map(
    field_provenance: Mapping[str, Any],
    *,
    required_facets: tuple[str, ...] = FACET_SYNTHESIS_ORDER,
) -> None:
    """Ensure every Twin facet exposes complete provenance."""
    for name in required_facets:
        if name not in field_provenance:
            raise TwinFacetValidationError(
                f"field_provenance missing entry for {name}"
            )
        entry = field_provenance[name]
        if isinstance(entry, TwinProvenance):
            payload = entry.to_canonical_dict()
        elif isinstance(entry, Mapping):
            payload = dict(entry)
        else:
            raise TwinFacetValidationError(
                f"field_provenance[{name}] must be a mapping"
            )
        for key in (
            "source_service",
            "source_entity",
            "collected_at",
            "availability",
            "unavailable_reason",
        ):
            if key not in payload:
                raise TwinFacetValidationError(
                    f"field_provenance[{name}] missing {key}"
                )
        availability = str(payload.get("availability") or "").strip().lower()
        if availability not in {
            AVAILABILITY_AVAILABLE,
            AVAILABILITY_UNAVAILABLE,
        }:
            raise TwinFacetValidationError(
                f"field_provenance[{name}] invalid availability"
            )
        if availability == AVAILABILITY_UNAVAILABLE and not str(
            payload.get("unavailable_reason") or ""
        ).strip():
            raise TwinFacetValidationError(
                f"field_provenance[{name}] unavailable without reason"
            )


def validate_unavailable_facet_empty(
    *,
    facet_name: str,
    availability: str,
    evidence_refs: tuple[str, ...] | list[str],
    material_values: Mapping[str, Any],
) -> None:
    """Unavailable facets must not carry invented material educational values."""
    if availability != AVAILABILITY_UNAVAILABLE:
        return
    if evidence_refs:
        raise TwinFacetValidationError(
            f"{facet_name}: unavailable facet must not cite evidence_refs"
        )
    for key, value in material_values.items():
        if value in (None, "", (), [], {}):
            continue
        raise TwinFacetValidationError(
            f"{facet_name}: unavailable facet must not set material field {key}"
        )


def validate_no_facet_cross_dependency(
    builder_source_fields: Mapping[str, set[str]],
) -> None:
    """Guardrail: builders may only declare Runtime A / empty deps — never facets."""
    for builder_name, deps in builder_source_fields.items():
        illegal = set(deps) & set(TWIN_FACET_NAMES)
        if illegal:
            raise TwinFacetValidationError(
                f"{builder_name} must not depend on facets {sorted(illegal)}"
            )


def validate_no_estimation_markers(payload: Any, *, field_name: str) -> None:
    """Reject payloads that advertise fabricated / estimated Twin values."""
    banned = ("estimated", "fabricated", "inferred_missing", "demo_seed")
    text = str(payload).lower()
    for token in banned:
        if token in text:
            raise TwinFacetValidationError(
                f"{field_name}: forbidden estimation marker {token!r}"
            )

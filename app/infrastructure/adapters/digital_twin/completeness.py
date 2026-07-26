"""Structural completeness evaluation for Twin Snapshots (MS-004 T2).

Evaluates only whether the seven Twin facets are present or explicitly
unavailable. Does not estimate, score, or invent missing educational values.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    COMPLETENESS_COMPLETE,
    COMPLETENESS_EMPTY,
    COMPLETENESS_PARTIAL,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    UnavailableSummary,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FACET_SYNTHESIS_ORDER,
)


def _facet_availability(
    profile: TwinProfile,
    field_provenance: Mapping[str, Any],
    facet_name: str,
) -> str:
    """Resolve structural availability for one facet (provenance preferred)."""
    entry = field_provenance.get(facet_name)
    if isinstance(entry, TwinProvenance):
        availability = (entry.availability or "").strip().lower()
        if availability in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE}:
            return availability
    elif isinstance(entry, Mapping):
        availability = str(entry.get("availability") or "").strip().lower()
        if availability in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE}:
            return availability

    facet = getattr(profile, facet_name, None)
    if facet is None:
        return AVAILABILITY_UNAVAILABLE
    availability = str(getattr(facet, "availability", "") or "").strip().lower()
    if availability == AVAILABILITY_AVAILABLE:
        return AVAILABILITY_AVAILABLE
    return AVAILABILITY_UNAVAILABLE


def _facet_unavailable_reason(
    profile: TwinProfile,
    field_provenance: Mapping[str, Any],
    facet_name: str,
) -> str:
    entry = field_provenance.get(facet_name)
    if isinstance(entry, TwinProvenance):
        reason = (entry.unavailable_reason or "").strip()
        if reason:
            return reason
    elif isinstance(entry, Mapping):
        reason = str(entry.get("unavailable_reason") or "").strip()
        if reason:
            return reason
    facet = getattr(profile, facet_name, None)
    if facet is None:
        return "UNAVAILABLE"
    return str(getattr(facet, "unavailable_reason", "") or "").strip() or (
        "UNAVAILABLE"
    )


class CompletenessEvaluator:
    """Compute structural TwinSnapshot completeness from facets + provenance."""

    def evaluate(
        self,
        profile: TwinProfile,
        field_provenance: Mapping[str, Any] | None = None,
    ) -> TwinCompleteness:
        """Return structural completeness (score always None — no estimation)."""
        provenance = field_provenance or {}
        present: list[str] = []
        unavailable: list[str] = []
        for name in FACET_SYNTHESIS_ORDER:
            if _facet_availability(profile, provenance, name) == (
                AVAILABILITY_AVAILABLE
            ):
                present.append(name)
            else:
                unavailable.append(name)

        present_t = tuple(present)
        unavailable_t = tuple(unavailable)
        if not present_t:
            status = COMPLETENESS_EMPTY
        elif not unavailable_t:
            status = COMPLETENESS_COMPLETE
        else:
            status = COMPLETENESS_PARTIAL

        return TwinCompleteness(
            score=None,
            facets_present=present_t,
            facets_unavailable=unavailable_t,
            status=status,
            summary=(
                f"status={status};present={len(present_t)};"
                f"unavailable={len(unavailable_t)}"
            ),
        )

    def unavailable_summary(
        self,
        profile: TwinProfile,
        field_provenance: Mapping[str, Any] | None = None,
        *,
        completeness: TwinCompleteness | None = None,
    ) -> UnavailableSummary:
        """Build an explicit unavailable summary (facets + reasons only)."""
        provenance = field_provenance or {}
        resolved = completeness or self.evaluate(profile, provenance)
        reasons: dict[str, str] = {}
        for name in resolved.facets_unavailable:
            reasons[name] = _facet_unavailable_reason(profile, provenance, name)
        facets = resolved.facets_unavailable
        if not facets:
            summary = "all_facets_available"
        else:
            summary = (
                f"unavailable={len(facets)};"
                f"reasons={','.join(sorted(set(reasons.values())))}"
            )
        return UnavailableSummary(
            facets=facets,
            reasons=reasons,
            summary=summary,
        )

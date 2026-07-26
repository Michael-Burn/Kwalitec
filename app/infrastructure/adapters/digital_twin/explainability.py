"""Twin Explainability (MS-004 T3).

Produces deterministic FacetExplanation / SnapshotExplanation values from
immutable TwinSnapshots and authoritative Runtime A provenance. No
persistence, Adaptive integration, Experience cutover, Runtime A writes,
or UI changes.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_COGNITIVE_LOAD,
    FACET_CONFIDENCE_TREND,
    FACET_CONSISTENCY,
    FACET_LEARNING_RHYTHM,
    FACET_PERSISTENCE,
    FACET_REVISION_BEHAVIOUR,
    FACET_SESSION_HABITS,
    TWIN_FACET_NAMES,
    FacetExplanation,
    SnapshotExplanation,
    TwinProvenance,
    TwinSnapshot,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FACET_RUNTIME_A_FIELDS,
    FACET_SYNTHESIS_ORDER,
    expand_facet_provenance,
    expand_snapshot_provenance,
)
from app.infrastructure.adapters.digital_twin.validation import (
    TwinFacetValidationError,
)

# Explainability construction version (rules for explanation text / refs).
EXPLAINABILITY_VERSION = "t3.0"
RULE_VERSION = "t3.0"

# Registered rule / model ids (DIGITAL_TWIN_EXPLAINABILITY.md registry).
FACET_RULE_CATALOGUE: Mapping[str, tuple[str, str]] = {
    FACET_LEARNING_RHYTHM: (
        "twin.structure.learning_rhythm",
        "Surface study-attempt duration / cadence structure from Runtime A",
    ),
    FACET_CONSISTENCY: (
        "twin.structure.consistency",
        "Surface mission completion / miss structure from Runtime A",
    ),
    FACET_PERSISTENCE: (
        "twin.structure.persistence",
        "Surface topic-progress continuity structure from Runtime A",
    ),
    FACET_REVISION_BEHAVIOUR: (
        "twin.structure.revision_behaviour",
        "Surface revision-count structure from Runtime A topic progress",
    ),
    FACET_CONFIDENCE_TREND: (
        "twin.structure.confidence_trend",
        "Surface confidence before/after attempt structure from Runtime A",
    ),
    FACET_SESSION_HABITS: (
        "twin.structure.session_habits",
        "Surface mission + attempt habit structure from Runtime A",
    ),
    FACET_COGNITIVE_LOAD: (
        "twin.structure.cognitive_load_indicators",
        "Surface duration / preferred-session load indicators from Runtime A",
    ),
}

RULE_SPARSE_OR_UNAVAILABLE = (
    "twin.insight.sparse_evidence",
    "Honest unavailable / sparse narrative — no estimation",
)

assert frozenset(FACET_RULE_CATALOGUE) == TWIN_FACET_NAMES


class TwinExplainabilityValidationError(TwinFacetValidationError):
    """Raised when Twin explainability inputs violate contracts."""


def _provenance_dict(
    entry: TwinProvenance | Mapping[str, Any] | None,
) -> dict[str, Any]:
    if entry is None:
        return {}
    if isinstance(entry, TwinProvenance):
        return entry.to_canonical_dict()
    return dict(entry)


def _facet_obj(snapshot: TwinSnapshot, facet_name: str) -> Any:
    facet = getattr(snapshot.profile, facet_name, None)
    if facet is None:
        raise TwinExplainabilityValidationError(
            f"TwinSnapshot missing facet: {facet_name}"
        )
    return facet


def _facet_availability(
    snapshot: TwinSnapshot,
    facet_name: str,
) -> str:
    entry = _provenance_dict(snapshot.field_provenance.get(facet_name))
    availability = str(entry.get("availability") or "").strip().lower()
    if availability in {AVAILABILITY_AVAILABLE, AVAILABILITY_UNAVAILABLE}:
        return availability
    facet = _facet_obj(snapshot, facet_name)
    availability = str(getattr(facet, "availability", "") or "").strip().lower()
    if availability == AVAILABILITY_AVAILABLE:
        return AVAILABILITY_AVAILABLE
    return AVAILABILITY_UNAVAILABLE


def _facet_unavailable_reason(snapshot: TwinSnapshot, facet_name: str) -> str:
    entry = _provenance_dict(snapshot.field_provenance.get(facet_name))
    reason = str(entry.get("unavailable_reason") or "").strip()
    if reason:
        return reason
    facet = _facet_obj(snapshot, facet_name)
    return str(getattr(facet, "unavailable_reason", "") or "").strip()


def _facet_evidence_refs(snapshot: TwinSnapshot, facet_name: str) -> tuple[str, ...]:
    facet = _facet_obj(snapshot, facet_name)
    refs = getattr(facet, "evidence_refs", ()) or ()
    return tuple(str(item) for item in refs)


def _contributing_runtime_a_evidence(
    snapshot: TwinSnapshot,
    facet_name: str,
    *,
    availability: str,
) -> tuple[str, ...]:
    """List contributing Runtime A evidence without inventing ids.

    Includes:
    - declared Runtime A field names the facet builder consumes
    - facet ``evidence_refs`` only when the facet is available
    """
    fields = FACET_RUNTIME_A_FIELDS.get(facet_name, ())
    tokens: list[str] = [f"runtime_a_field:{name}" for name in fields]
    if availability == AVAILABILITY_AVAILABLE:
        for ref in _facet_evidence_refs(snapshot, facet_name):
            if ref and ref not in tokens:
                tokens.append(ref)
    return tuple(tokens)


def _rule_for_facet(facet_name: str, *, availability: str) -> tuple[str, str, str]:
    if availability != AVAILABILITY_AVAILABLE:
        rule_id, description = RULE_SPARSE_OR_UNAVAILABLE
        return rule_id, RULE_VERSION, description
    rule_id, description = FACET_RULE_CATALOGUE[facet_name]
    return rule_id, RULE_VERSION, description


def _derivation_summary(
    snapshot: TwinSnapshot,
    facet_name: str,
    *,
    availability: str,
) -> str:
    """Plain-language derivation summary — documents existing facet fields only."""
    if availability != AVAILABILITY_AVAILABLE:
        reason = _facet_unavailable_reason(snapshot, facet_name) or "UNAVAILABLE"
        return (
            f"Facet {facet_name} unavailable; no derivation performed. "
            f"reason={reason}"
        )

    facet = _facet_obj(snapshot, facet_name)
    label = str(getattr(facet, "label", "") or "").strip()
    note_keys = (
        "cadence_note",
        "adherence_note",
        "continuity_note",
        "revision_note",
        "trend_note",
        "habits_note",
        "load_note",
    )
    note = ""
    for key in note_keys:
        value = getattr(facet, key, None)
        if value:
            note = str(value).strip()
            break
    refs = _facet_evidence_refs(snapshot, facet_name)
    fields = FACET_RUNTIME_A_FIELDS.get(facet_name, ())
    parts = [
        f"Derived {facet_name} from Runtime A fields "
        f"[{','.join(fields)}]",
    ]
    if label:
        parts.append(f"label={label}")
    if note:
        parts.append(f"note={note}")
    typical = getattr(facet, "typical_session_minutes", None)
    if typical is not None:
        parts.append(f"typical_session_minutes={typical}")
    parts.append(f"evidence_refs_count={len(refs)}")
    return "; ".join(parts)


def _completeness_reasoning(
    snapshot: TwinSnapshot,
    facet_name: str,
    *,
    availability: str,
) -> str:
    status = (snapshot.completeness.status or "").strip() or "unknown"
    present = facet_name in snapshot.completeness.facets_present
    unavailable = facet_name in snapshot.completeness.facets_unavailable
    if availability == AVAILABILITY_AVAILABLE:
        return (
            f"Facet {facet_name} is available and "
            f"{'is' if present else 'is not'} listed in "
            f"completeness.facets_present; snapshot status={status}"
        )
    return (
        f"Facet {facet_name} is unavailable and "
        f"{'is' if unavailable else 'is not'} listed in "
        f"completeness.facets_unavailable; snapshot status={status}"
    )


class FacetExplanationBuilder:
    """Build a deterministic FacetExplanation from a TwinSnapshot facet."""

    def build(
        self,
        snapshot: TwinSnapshot,
        facet_name: str,
    ) -> FacetExplanation:
        name = (facet_name or "").strip()
        if name not in TWIN_FACET_NAMES:
            raise TwinExplainabilityValidationError(
                f"Unknown Twin facet: {facet_name!r}"
            )
        availability = _facet_availability(snapshot, name)
        expansion = expand_facet_provenance(
            name,
            snapshot.field_provenance.get(name),
        )
        rule_id, rule_version, rule_description = _rule_for_facet(
            name, availability=availability
        )
        unavailable_reasoning = ""
        if availability != AVAILABILITY_AVAILABLE:
            unavailable_reasoning = (
                _facet_unavailable_reason(snapshot, name) or "UNAVAILABLE"
            )
        return FacetExplanation(
            facet_name=name,
            availability=availability,
            contributing_runtime_a_evidence=_contributing_runtime_a_evidence(
                snapshot, name, availability=availability
            ),
            derivation_summary=_derivation_summary(
                snapshot, name, availability=availability
            ),
            completeness_reasoning=_completeness_reasoning(
                snapshot, name, availability=availability
            ),
            unavailable_reasoning=unavailable_reasoning,
            provenance_refs=(expansion.reference,),
            rule_or_model_id=rule_id,
            rule_version=rule_version,
            rule_description=rule_description,
        )


class SnapshotExplanationBuilder:
    """Aggregate facet explanations into a SnapshotExplanation."""

    def __init__(
        self,
        *,
        facet_builder: FacetExplanationBuilder | None = None,
        explainability_version: str = EXPLAINABILITY_VERSION,
    ) -> None:
        self._facet_builder = facet_builder or FacetExplanationBuilder()
        self._explainability_version = explainability_version

    def build(self, snapshot: TwinSnapshot) -> SnapshotExplanation:
        if not isinstance(snapshot, TwinSnapshot):
            raise TwinExplainabilityValidationError(
                "snapshot must be a TwinSnapshot"
            )

        facet_explanations = tuple(
            self._facet_builder.build(snapshot, name)
            for name in FACET_SYNTHESIS_ORDER
        )
        expansions = expand_snapshot_provenance(
            snapshot.field_provenance,
            root=snapshot.provenance,
        )
        provenance_refs = tuple(item.reference for item in expansions)

        completeness = snapshot.completeness
        overall = (
            f"status={completeness.status or 'unknown'};"
            f"present={len(completeness.facets_present)};"
            f"unavailable={len(completeness.facets_unavailable)};"
            f"score={'none' if completeness.score is None else completeness.score}"
        )
        if completeness.summary:
            overall = f"{overall};summary={completeness.summary}"

        unavailable = snapshot.unavailable_summary
        if not unavailable.facets:
            unavailable_text = "all_facets_available"
        else:
            reason_parts = [
                f"{name}={unavailable.reasons.get(name, 'UNAVAILABLE')}"
                for name in unavailable.facets
            ]
            unavailable_text = (
                f"unavailable_count={len(unavailable.facets)};"
                + ";".join(reason_parts)
            )
            if unavailable.summary:
                unavailable_text = (
                    f"{unavailable_text};summary={unavailable.summary}"
                )

        provenance_summary = snapshot.provenance_summary
        evidence_ref_total = sum(
            len(item.contributing_runtime_a_evidence)
            for item in facet_explanations
            if item.availability == AVAILABILITY_AVAILABLE
        )
        coverage = (
            f"available_facets={len(completeness.facets_present)}/"
            f"{len(FACET_SYNTHESIS_ORDER)};"
            f"contributing_sources="
            f"[{','.join(provenance_summary.contributing_runtime_a_sources)}];"
            f"evidence_window="
            f"{provenance_summary.evidence_window_start or ''}.."
            f"{provenance_summary.evidence_window_end or ''};"
            f"contributing_evidence_tokens={evidence_ref_total};"
            f"unavailable_inputs="
            f"[{','.join(provenance_summary.unavailable_inputs)}]"
        )

        return SnapshotExplanation(
            twin_id=snapshot.twin_id,
            student_id=snapshot.profile.student_id,
            generated_at=snapshot.generated_at,
            explainability_version=self._explainability_version,
            overall_completeness_explanation=overall,
            unavailable_summary_explanation=unavailable_text,
            evidence_coverage_summary=coverage,
            facet_explanations=facet_explanations,
            provenance_refs=provenance_refs,
        )


class TwinExplainabilityService:
    """Produce deterministic Twin explanations from TwinSnapshots (MS-004 T3).

    Rules:
    - MAY expand provenance and document existing snapshot / facet fields
    - MUST NOT invent evidence, estimate missing facets, persist snapshots,
      write Runtime A, call Adaptive paths, or cut over Experience TwinPort
    - Identical TwinSnapshot material inputs → identical explanations
    """

    SERVICE_ID = "twin_explainability"
    SERVICE_VERSION = "1.0.0-t3"

    def __init__(
        self,
        *,
        enabled: bool = True,
        facet_builder: FacetExplanationBuilder | None = None,
        snapshot_builder: SnapshotExplanationBuilder | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._facet_builder = facet_builder or FacetExplanationBuilder()
        self._snapshot_builder = snapshot_builder or SnapshotExplanationBuilder(
            facet_builder=self._facet_builder,
        )

    @property
    def service_id(self) -> str:
        return self.SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def explain_facet(
        self,
        snapshot: TwinSnapshot,
        facet_name: str,
    ) -> FacetExplanation:
        """Explain one Twin facet from an assembled TwinSnapshot."""
        if not self._enabled:
            raise TwinExplainabilityValidationError(
                "TwinExplainabilityService is disabled (feature flag OFF)"
            )
        if not isinstance(snapshot, TwinSnapshot):
            raise TwinExplainabilityValidationError(
                "snapshot must be a TwinSnapshot"
            )
        return self._facet_builder.build(snapshot, facet_name)

    def explain_snapshot(self, snapshot: TwinSnapshot) -> SnapshotExplanation:
        """Explain a TwinSnapshot including all seven facet explanations."""
        if not self._enabled:
            raise TwinExplainabilityValidationError(
                "TwinExplainabilityService is disabled (feature flag OFF)"
            )
        return self._snapshot_builder.build(snapshot)


def build_twin_explainability_service(
    *,
    enabled: bool,
) -> TwinExplainabilityService | None:
    """DI helper — construct TwinExplainabilityService only when the flag is on."""
    if not enabled:
        return None
    return TwinExplainabilityService(enabled=True)


__all__ = [
    "EXPLAINABILITY_VERSION",
    "FACET_RULE_CATALOGUE",
    "RULE_VERSION",
    "FacetExplanationBuilder",
    "SnapshotExplanationBuilder",
    "TwinExplainabilityService",
    "TwinExplainabilityValidationError",
    "build_twin_explainability_service",
]

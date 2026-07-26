"""Evidence Collector (MS-006 E1).

Read-only intake: freeze ObservedEvent / EvidenceContext / upstream reference
payloads into CollectedObservation. Never mutates inputs, estimates facts,
scores outcomes, or writes educational state.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    CLAIM_LEARNING_SIGNAL,
    CLAIM_ORGANISATION,
    CLASS_ADVICE_EVENT,
    CLASS_DELIVERY_EVENT,
    CLASS_FACT_EVENT,
    CLASS_INTERPRETATION_EVENT,
    CLASS_ORCHESTRATION_EVENT,
    REF_KIND_ADAPTIVE,
    REF_KIND_EXPERIENCE,
    REF_KIND_RUNTIME_A,
    REF_KIND_STRATEGY,
    REF_KIND_TWIN,
    EvidenceContext,
    ObservationRef,
    ObservedEvent,
    serialize_canonical,
)
from app.infrastructure.adapters.evidence_platform.provenance import (
    REASON_ADAPTIVE_UNAVAILABLE,
    REASON_EXPERIENCE_UNAVAILABLE,
    REASON_RUNTIME_A_UNAVAILABLE,
    REASON_STRATEGY_UNAVAILABLE,
    REASON_TWIN_UNAVAILABLE,
    SOURCE_SERVICE_ADAPTIVE,
    SOURCE_SERVICE_EXPERIENCE,
    SOURCE_SERVICE_RUNTIME_A,
    SOURCE_SERVICE_STRATEGY,
    SOURCE_SERVICE_TWIN,
    block_provenance,
    freeze_provenance_map,
)
from app.infrastructure.adapters.evidence_platform.validation import (
    EvidenceValidationError,
    EvidenceValidator,
)

# Map common event type tokens → evidence class (structural, not interpretive).
_EVENT_TYPE_CLASS: dict[str, str] = {
    "mission_completed": CLASS_FACT_EVENT,
    "mission_abandoned": CLASS_FACT_EVENT,
    "study_attempt": CLASS_FACT_EVENT,
    "evidence_accepted": CLASS_FACT_EVENT,
    "progress_delta": CLASS_FACT_EVENT,
    "runtime_a": CLASS_FACT_EVENT,
    "experience_served": CLASS_DELIVERY_EVENT,
    "experience_delivery": CLASS_DELIVERY_EVENT,
    "delivery": CLASS_DELIVERY_EVENT,
    "adaptive_recommendation": CLASS_ADVICE_EVENT,
    "adaptive_decision": CLASS_ADVICE_EVENT,
    "advice": CLASS_ADVICE_EVENT,
    "strategy_projection": CLASS_ORCHESTRATION_EVENT,
    "strategy_intervention": CLASS_ORCHESTRATION_EVENT,
    "orchestration": CLASS_ORCHESTRATION_EVENT,
    "twin_snapshot": CLASS_INTERPRETATION_EVENT,
    "twin_facet": CLASS_INTERPRETATION_EVENT,
    "interpretation": CLASS_INTERPRETATION_EVENT,
}


@dataclass(frozen=True)
class CollectedObservation:
    """Immutable frozen observation after E1 collection (pre-assembly)."""

    student_id: str
    event_type: str = ""
    evidence_class: str = ""
    claim_boundary: str = ""
    observed_at: str | None = None
    ingested_at: str | None = None
    as_of: str | None = None
    source_refs: tuple[ObservationRef, ...] = ()
    payload_summary: Mapping[str, Any] = field(default_factory=dict)
    field_provenance: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(self, "event_type", (self.event_type or "").strip())
        object.__setattr__(
            self, "evidence_class", (self.evidence_class or "").strip().upper()
        )
        object.__setattr__(
            self, "claim_boundary", (self.claim_boundary or "").strip().lower()
        )
        object.__setattr__(self, "source_refs", tuple(self.source_refs or ()))
        object.__setattr__(
            self,
            "payload_summary",
            MappingProxyType(dict(self.payload_summary or {})),
        )
        object.__setattr__(
            self, "field_provenance", freeze_provenance_map(self.field_provenance)
        )
        object.__setattr__(self, "limitations", tuple(self.limitations or ()))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "claim_boundary": self.claim_boundary,
            "evidence_class": self.evidence_class,
            "event_type": self.event_type,
            "field_provenance": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(self.field_provenance.items())
            },
            "ingested_at": self.ingested_at,
            "limitations": list(self.limitations),
            "observed_at": self.observed_at,
            "payload_summary": dict(self.payload_summary),
            "source_refs": [ref.to_canonical_dict() for ref in self.source_refs],
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


class EvidenceCollector:
    """Collect and freeze observational inputs into CollectedObservation.

    Rules:
    - MAY freeze ObservedEvent / EvidenceContext / reference payloads
    - MUST NOT mutate inputs, estimate missing facts, score, or write Runtime A /
      Twin / Adaptive / Strategy / Experience educational state
    """

    COLLECTOR_ID = "evidence_collector"
    COLLECTOR_VERSION = "1.0.0-e1"

    def __init__(
        self,
        *,
        validator: EvidenceValidator | None = None,
        enabled: bool = True,
    ) -> None:
        self._validator = validator or EvidenceValidator()
        self._enabled = bool(enabled)

    @property
    def collector_id(self) -> str:
        return self.COLLECTOR_ID

    @property
    def collector_version(self) -> str:
        return self.COLLECTOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def collect(
        self,
        event: ObservedEvent | EvidenceContext | Mapping[str, Any],
    ) -> CollectedObservation:
        """Freeze an observed event / context into CollectedObservation.

        Identical material inputs → identical CollectedObservation.serialize().
        """
        if not self._enabled:
            raise EvidenceValidationError(
                "EvidenceCollector is disabled (feature flag OFF)"
            )

        if isinstance(event, ObservedEvent):
            return self._collect_observed_event(event)
        if isinstance(event, EvidenceContext):
            return self._collect_context(event)
        if isinstance(event, Mapping):
            return self._collect_observed_event(_mapping_to_observed_event(event))
        raise EvidenceValidationError(
            "event must be ObservedEvent, EvidenceContext, or mapping"
        )

    def _collect_observed_event(self, event: ObservedEvent) -> CollectedObservation:
        validated = self._validator.validate_observed_event(event)
        # Deep-freeze upstream blocks without aliasing caller mappings.
        runtime_a = _deep_copy_mapping(validated.runtime_a)
        experience = _deep_copy_mapping(validated.experience)
        strategy = _deep_copy_mapping(validated.strategy)
        adaptive = _deep_copy_mapping(validated.adaptive)
        twin = _deep_copy_mapping(validated.twin)
        payload_summary = _deep_copy_mapping(validated.payload_summary)

        clock = (
            self._validator.validate_clock(validated.as_of, label="as_of")
            or self._validator.validate_clock(
                validated.observed_at, label="observed_at"
            )
            or self._validator.validate_clock(
                validated.ingested_at, label="ingested_at"
            )
        )
        observed_at = self._validator.validate_clock(
            validated.observed_at, label="observed_at"
        )
        ingested_at = self._validator.validate_clock(
            validated.ingested_at, label="ingested_at"
        )
        # Preserve both clocks; when only one provided, mirror for determinism.
        if observed_at is None and ingested_at is not None:
            observed_at = ingested_at
        if ingested_at is None and observed_at is not None:
            ingested_at = observed_at
        if observed_at is None and clock is not None:
            observed_at = clock
            ingested_at = clock

        refs = list(validated.source_refs)
        field_provenance: dict[str, Any] = {}
        limitations: list[str] = list(validated.limitations)

        runtime_refs, runtime_available = _refs_from_runtime_a(
            runtime_a,
            student_id=validated.student_id,
            observed_at=observed_at,
            as_of=clock,
            claim_boundary=validated.claim_boundary or CLAIM_ORGANISATION,
        )
        refs.extend(runtime_refs)
        field_provenance["runtime_a"] = block_provenance(
            available=runtime_available,
            source_service=SOURCE_SERVICE_RUNTIME_A,
            source_entity="educational_event",
            collected_at=clock,
            unavailable_reason=""
            if runtime_available
            else REASON_RUNTIME_A_UNAVAILABLE,
        )
        if not runtime_available and not validated.source_refs:
            limitations.append(REASON_RUNTIME_A_UNAVAILABLE)

        experience_refs, experience_available = _refs_from_block(
            experience,
            ref_kind=REF_KIND_EXPERIENCE,
            default_entity="ExperienceDelivery",
            student_id=validated.student_id,
            observed_at=observed_at,
            as_of=clock,
            claim_boundary=validated.claim_boundary or CLAIM_ORGANISATION,
            id_keys=("delivery_id", "projection_id", "entity_id", "id"),
        )
        refs.extend(experience_refs)
        field_provenance["experience"] = block_provenance(
            available=experience_available,
            source_service=SOURCE_SERVICE_EXPERIENCE,
            source_entity="ExperienceDelivery",
            collected_at=clock,
            unavailable_reason=""
            if experience_available
            else REASON_EXPERIENCE_UNAVAILABLE,
        )

        strategy_refs, strategy_available = _refs_from_block(
            strategy,
            ref_kind=REF_KIND_STRATEGY,
            default_entity="StrategyProjection",
            student_id=validated.student_id,
            observed_at=observed_at,
            as_of=clock,
            claim_boundary=validated.claim_boundary or CLAIM_ORGANISATION,
            id_keys=(
                "intervention_id",
                "projection_id",
                "strategy_trace_id",
                "entity_id",
                "id",
            ),
        )
        refs.extend(strategy_refs)
        field_provenance["strategy"] = block_provenance(
            available=strategy_available,
            source_service=SOURCE_SERVICE_STRATEGY,
            source_entity="StrategyProjection",
            collected_at=clock,
            unavailable_reason=""
            if strategy_available
            else REASON_STRATEGY_UNAVAILABLE,
        )

        adaptive_refs, adaptive_available = _refs_from_block(
            adaptive,
            ref_kind=REF_KIND_ADAPTIVE,
            default_entity="AdaptiveDecisionRecord",
            student_id=validated.student_id,
            observed_at=observed_at,
            as_of=clock,
            claim_boundary=validated.claim_boundary or CLAIM_LEARNING_SIGNAL,
            id_keys=(
                "decision_id",
                "recommendation_id",
                "adaptive_recommendation_ref",
                "entity_id",
                "id",
            ),
        )
        refs.extend(adaptive_refs)
        field_provenance["adaptive"] = block_provenance(
            available=adaptive_available,
            source_service=SOURCE_SERVICE_ADAPTIVE,
            source_entity="AdaptiveDecisionRecord",
            collected_at=clock,
            unavailable_reason=""
            if adaptive_available
            else REASON_ADAPTIVE_UNAVAILABLE,
        )

        twin_refs, twin_available = _refs_from_block(
            twin,
            ref_kind=REF_KIND_TWIN,
            default_entity="TwinSnapshot",
            student_id=validated.student_id,
            observed_at=observed_at,
            as_of=clock,
            claim_boundary=validated.claim_boundary or CLAIM_ORGANISATION,
            id_keys=(
                "twin_id",
                "snapshot_id",
                "snapshot_version",
                "entity_id",
                "id",
            ),
        )
        refs.extend(twin_refs)
        field_provenance["twin"] = block_provenance(
            available=twin_available,
            source_service=SOURCE_SERVICE_TWIN,
            source_entity="TwinSnapshot",
            collected_at=clock,
            unavailable_reason="" if twin_available else REASON_TWIN_UNAVAILABLE,
        )

        # Deduplicate refs by canonical serialize while preserving order.
        unique_refs = _dedupe_refs(refs)
        scoped_refs = self._validator.validate_source_refs(
            unique_refs, student_id=validated.student_id
        )

        evidence_class = (
            validated.evidence_class
            or _infer_evidence_class(validated.event_type, scoped_refs)
        )
        claim_boundary = validated.claim_boundary or _default_claim_boundary(
            evidence_class
        )
        event_type = validated.event_type or evidence_class.lower()

        summary = dict(payload_summary)
        if "event_type" not in summary and event_type:
            summary["event_type"] = event_type
        # Strip raw educational answer bodies — refs only.
        summary.pop("raw_answer", None)
        summary.pop("raw_answers", None)

        return CollectedObservation(
            student_id=validated.student_id,
            event_type=event_type,
            evidence_class=evidence_class,
            claim_boundary=claim_boundary,
            observed_at=observed_at,
            ingested_at=ingested_at,
            as_of=clock,
            source_refs=scoped_refs,
            payload_summary=summary,
            field_provenance=field_provenance,
            limitations=tuple(dict.fromkeys(limitations)),
        )

    def _collect_context(self, context: EvidenceContext) -> CollectedObservation:
        validated = self._validator.validate_evidence_context(context)
        clock = self._validator.validate_clock(validated.as_of, label="as_of")
        refs = self._validator.validate_source_refs(
            validated.source_refs, student_id=validated.student_id
        )
        evidence_class = validated.evidence_class or _infer_evidence_class("", refs)
        claim_boundary = validated.claim_boundary or _default_claim_boundary(
            evidence_class
        )
        runtime_present = any(ref.ref_kind == REF_KIND_RUNTIME_A for ref in refs)
        field_provenance = {
            "runtime_a": block_provenance(
                available=runtime_present,
                source_service=SOURCE_SERVICE_RUNTIME_A
                if runtime_present
                else SOURCE_SERVICE_RUNTIME_A,
                source_entity="ObservationRef",
                collected_at=clock,
                unavailable_reason=""
                if runtime_present
                else REASON_RUNTIME_A_UNAVAILABLE,
            ),
            **{
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in validated.field_provenance.items()
            },
        }
        limitations = list(validated.limitations)
        if not runtime_present and evidence_class == CLASS_FACT_EVENT:
            limitations.append(REASON_RUNTIME_A_UNAVAILABLE)
        return CollectedObservation(
            student_id=validated.student_id,
            event_type=evidence_class.lower() if evidence_class else "",
            evidence_class=evidence_class,
            claim_boundary=claim_boundary,
            observed_at=clock,
            ingested_at=clock,
            as_of=clock,
            source_refs=refs,
            payload_summary={},
            field_provenance=field_provenance,
            limitations=tuple(dict.fromkeys(limitations)),
        )


def build_evidence_collector(
    *,
    enabled: bool,
    validator: EvidenceValidator | None = None,
) -> EvidenceCollector | None:
    """DI helper — construct EvidenceCollector only when the flag is on."""
    if not enabled:
        return None
    return EvidenceCollector(validator=validator, enabled=True)


def _mapping_to_observed_event(value: Mapping[str, Any]) -> ObservedEvent:
    payload = _deep_copy_mapping(value)
    raw_refs = payload.pop("source_refs", ()) or ()
    refs: list[ObservationRef] = []
    for item in raw_refs:
        if isinstance(item, ObservationRef):
            refs.append(item)
        elif isinstance(item, Mapping):
            refs.append(
                ObservationRef(
                    ref_kind=str(item.get("ref_kind") or ""),
                    entity_kind=str(item.get("entity_kind") or ""),
                    entity_id=str(item.get("entity_id") or ""),
                    fingerprint=str(item.get("fingerprint") or ""),
                    observed_at=item.get("observed_at"),
                    as_of=item.get("as_of"),
                    student_id=str(item.get("student_id") or ""),
                    claim_boundary=str(item.get("claim_boundary") or ""),
                )
            )
        else:
            raise EvidenceValidationError(
                "source_refs must contain ObservationRef or mappings"
            )
    return ObservedEvent(
        student_id=str(payload.get("student_id") or ""),
        event_type=str(payload.get("event_type") or ""),
        observed_at=payload.get("observed_at"),
        ingested_at=payload.get("ingested_at"),
        as_of=payload.get("as_of"),
        claim_boundary=str(payload.get("claim_boundary") or ""),
        evidence_class=str(payload.get("evidence_class") or ""),
        source_refs=tuple(refs),
        runtime_a=dict(payload.get("runtime_a") or {}),
        experience=dict(payload.get("experience") or {}),
        strategy=dict(payload.get("strategy") or {}),
        adaptive=dict(payload.get("adaptive") or {}),
        twin=dict(payload.get("twin") or {}),
        payload_summary=dict(payload.get("payload_summary") or {}),
        limitations=tuple(payload.get("limitations") or ()),
    )


def _deep_copy_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    """Recursively copy mappings / sequences without aliasing the original."""
    if value is None:
        return {}
    if hasattr(value, "to_canonical_dict"):
        payload = value.to_canonical_dict()
        if not isinstance(payload, dict):
            raise EvidenceValidationError(
                "input to_canonical_dict() must return a mapping"
            )
        return _deep_copy_mapping(payload)
    result: dict[str, Any] = {}
    for key, item in value.items():
        result[str(key)] = _deep_copy_value(item)
    return result


def _deep_copy_value(value: Any) -> Any:
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, Mapping):
        return _deep_copy_mapping(value)
    if isinstance(value, list | tuple):
        return [_deep_copy_value(item) for item in value]
    if hasattr(value, "to_canonical_dict"):
        return _deep_copy_value(value.to_canonical_dict())
    raise EvidenceValidationError(
        f"unsupported evidence collection value type: {type(value)!r}"
    )


def _refs_from_runtime_a(
    payload: Mapping[str, Any],
    *,
    student_id: str,
    observed_at: str | None,
    as_of: str | None,
    claim_boundary: str,
) -> tuple[list[ObservationRef], bool]:
    if not payload:
        return [], False
    refs: list[ObservationRef] = []
    mission = payload.get("mission")
    if isinstance(mission, Mapping):
        mission_id = str(
            mission.get("mission_id") or mission.get("id") or ""
        ).strip()
        if mission_id:
            refs.append(
                ObservationRef(
                    ref_kind=REF_KIND_RUNTIME_A,
                    entity_kind="Mission",
                    entity_id=mission_id,
                    fingerprint=_fingerprint({"mission": dict(mission)}),
                    observed_at=observed_at,
                    as_of=as_of,
                    student_id=student_id,
                    claim_boundary=claim_boundary or CLAIM_ORGANISATION,
                )
            )
    attempt = payload.get("study_attempt") or payload.get("attempt")
    if isinstance(attempt, Mapping):
        attempt_id = str(attempt.get("attempt_id") or attempt.get("id") or "").strip()
        if attempt_id:
            refs.append(
                ObservationRef(
                    ref_kind=REF_KIND_RUNTIME_A,
                    entity_kind="StudyAttempt",
                    entity_id=attempt_id,
                    fingerprint=_fingerprint({"attempt": dict(attempt)}),
                    observed_at=observed_at,
                    as_of=as_of,
                    student_id=student_id,
                    claim_boundary=claim_boundary or CLAIM_LEARNING_SIGNAL,
                )
            )
    evidence_id = str(payload.get("evidence_id") or "").strip()
    if evidence_id:
        refs.append(
            ObservationRef(
                ref_kind=REF_KIND_RUNTIME_A,
                entity_kind="Evidence",
                entity_id=evidence_id,
                fingerprint=_fingerprint({"evidence_id": evidence_id}),
                observed_at=observed_at,
                as_of=as_of,
                student_id=student_id,
                claim_boundary=claim_boundary or CLAIM_LEARNING_SIGNAL,
            )
        )
    event_id = str(payload.get("event_id") or payload.get("entity_id") or "").strip()
    if event_id and not refs:
        refs.append(
            ObservationRef(
                ref_kind=REF_KIND_RUNTIME_A,
                entity_kind=str(payload.get("entity_kind") or "EducationalEvent"),
                entity_id=event_id,
                fingerprint=_fingerprint(dict(payload)),
                observed_at=observed_at,
                as_of=as_of,
                student_id=student_id,
                claim_boundary=claim_boundary or CLAIM_ORGANISATION,
            )
        )
    if not refs and payload:
        # Honest reference when payload present but no id — fingerprint only.
        refs.append(
            ObservationRef(
                ref_kind=REF_KIND_RUNTIME_A,
                entity_kind=str(payload.get("entity_kind") or "EducationalEvent"),
                entity_id="",
                fingerprint=_fingerprint(dict(payload)),
                observed_at=observed_at,
                as_of=as_of,
                student_id=student_id,
                claim_boundary=claim_boundary or CLAIM_ORGANISATION,
            )
        )
    return refs, True


def _refs_from_block(
    payload: Mapping[str, Any],
    *,
    ref_kind: str,
    default_entity: str,
    student_id: str,
    observed_at: str | None,
    as_of: str | None,
    claim_boundary: str,
    id_keys: tuple[str, ...],
) -> tuple[list[ObservationRef], bool]:
    if not payload:
        return [], False
    entity_id = ""
    for key in id_keys:
        candidate = str(payload.get(key) or "").strip()
        if candidate:
            entity_id = candidate
            break
    entity_kind = str(payload.get("entity_kind") or default_entity).strip()
    refs = [
        ObservationRef(
            ref_kind=ref_kind,
            entity_kind=entity_kind,
            entity_id=entity_id,
            fingerprint=_fingerprint(dict(payload)),
            observed_at=observed_at,
            as_of=as_of,
            student_id=student_id,
            claim_boundary=claim_boundary,
        )
    ]
    return refs, True


def _fingerprint(payload: Mapping[str, Any]) -> str:
    digest = hashlib.sha256(
        serialize_canonical(dict(payload)).encode("utf-8")
    ).hexdigest()
    return digest[:32]


def _dedupe_refs(refs: list[ObservationRef]) -> list[ObservationRef]:
    seen: set[str] = set()
    unique: list[ObservationRef] = []
    for ref in refs:
        key = ref.serialize()
        if key in seen:
            continue
        seen.add(key)
        unique.append(ref)
    return unique


def _infer_evidence_class(
    event_type: str, refs: tuple[ObservationRef, ...] | list[ObservationRef]
) -> str:
    token = (event_type or "").strip().lower()
    if token in _EVENT_TYPE_CLASS:
        return _EVENT_TYPE_CLASS[token]
    for ref in refs:
        if ref.ref_kind == REF_KIND_RUNTIME_A:
            return CLASS_FACT_EVENT
        if ref.ref_kind == REF_KIND_EXPERIENCE:
            return CLASS_DELIVERY_EVENT
        if ref.ref_kind == REF_KIND_ADAPTIVE:
            return CLASS_ADVICE_EVENT
        if ref.ref_kind == REF_KIND_STRATEGY:
            return CLASS_ORCHESTRATION_EVENT
        if ref.ref_kind == REF_KIND_TWIN:
            return CLASS_INTERPRETATION_EVENT
    return CLASS_FACT_EVENT if refs else ""


def _default_claim_boundary(evidence_class: str) -> str:
    if evidence_class in {CLASS_FACT_EVENT, CLASS_DELIVERY_EVENT}:
        return CLAIM_ORGANISATION
    if evidence_class == CLASS_ADVICE_EVENT:
        return CLAIM_LEARNING_SIGNAL
    if evidence_class == CLASS_INTERPRETATION_EVENT:
        return CLAIM_ORGANISATION
    if evidence_class == CLASS_ORCHESTRATION_EVENT:
        return CLAIM_ORGANISATION
    return CLAIM_ORGANISATION if evidence_class else ""


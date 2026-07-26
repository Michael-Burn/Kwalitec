"""Twin Facet Assembler (MS-004 T1).

Collects authoritative Runtime A educational data and synthesises immutable
learner facets. Performs collection, validation, facet building, and
provenance annotation only — no snapshot persistence, Adaptive integration,
Experience cutover, or educational writes.
"""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from app.infrastructure.adapters.adaptive_engine.collectors import (
    CollectorResult,
    RuntimeACollector,
    build_default_collectors,
    read_active_study_plan,
)
from app.infrastructure.adapters.adaptive_engine.normalization import (
    normalize_curriculum,
    normalize_evidence,
    normalize_lifecycle_stage,
    normalize_mission,
    normalize_readiness,
    normalize_student_goals,
    normalize_study_attempts,
    normalize_topic_progress,
)
from app.infrastructure.adapters.digital_twin.builders import (
    FacetBuilder,
    default_facet_builders,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_COGNITIVE_LOAD,
    FACET_CONFIDENCE_TREND,
    FACET_CONSISTENCY,
    FACET_LEARNING_RHYTHM,
    FACET_PERSISTENCE,
    FACET_REVISION_BEHAVIOUR,
    FACET_SESSION_HABITS,
    CognitiveLoadIndicatorsFacet,
    ConfidenceTrendFacet,
    ConsistencyFacet,
    LearningRhythmFacet,
    PersistenceFacet,
    RevisionBehaviourFacet,
    SessionHabitsFacet,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    serialize_canonical,
)
from app.infrastructure.adapters.digital_twin.evidence import TwinRuntimeEvidence
from app.infrastructure.adapters.digital_twin.provenance import (
    FACET_SYNTHESIS_ORDER,
    FIELD_CURRICULUM,
    FIELD_EVIDENCE,
    FIELD_LIFECYCLE_STAGE,
    FIELD_MISSION,
    FIELD_READINESS,
    FIELD_STUDENT_GOALS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_TOPIC_PROGRESS,
    KIND_RUNTIME_A_DERIVED,
    REASON_INVALID_STUDENT_ID,
    RUNTIME_A_FIELD_NAMES,
    SOURCE_SERVICE_TWIN_FACET,
    freeze_provenance_map,
    unavailable_facet_provenance,
)
from app.infrastructure.adapters.digital_twin.validation import (
    TwinFacetValidationError,
    validate_as_of,
    validate_facet_provenance_map,
    validate_no_estimation_markers,
    validate_no_facet_cross_dependency,
    validate_student_id,
)

logger = logging.getLogger(__name__)

FACET_PROFILE_VERSION = "t1.0"


@dataclass(frozen=True)
class TwinFacetBundle:
    """Immutable result of Twin Facet Synthesis (not a TwinSnapshot).

    T1 stops at facets. Snapshot persistence / lifecycle is T2.
    """

    student_id: str
    as_of: str | None
    profile: TwinProfile
    field_provenance: Mapping[str, Any] = field(default_factory=dict)
    completeness: TwinCompleteness = field(default_factory=TwinCompleteness)
    source_evidence_version: str = ""
    profile_version: str = FACET_PROFILE_VERSION
    authority: str = AUTHORITY_DIGITAL_TWIN

    def __post_init__(self) -> None:
        if not isinstance(self.profile, TwinProfile):
            raise TypeError("profile must be a TwinProfile")
        if not isinstance(self.completeness, TwinCompleteness):
            raise TypeError("completeness must be a TwinCompleteness")
        object.__setattr__(
            self, "field_provenance", freeze_provenance_map(self.field_provenance)
        )
        object.__setattr__(self, "student_id", (self.student_id or "").strip())

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "authority": self.authority,
            "completeness": self.completeness.to_canonical_dict(),
            "field_provenance": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(self.field_provenance.items())
            },
            "profile": self.profile.to_canonical_dict(),
            "profile_version": self.profile_version,
            "source_evidence_version": self.source_evidence_version,
            "student_id": self.student_id,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


class TwinFacetAssembler:
    """Assemble Twin facets from Runtime A collectors.

    Rules:
    - MAY collect Runtime A, validate, build facets, annotate provenance
    - MUST NOT estimate missing values, persist snapshots, call Adaptive
      decision paths, write Runtime A, or cut over Experience TwinPort
    - Facets must not depend on other derived facets
    """

    ASSEMBLER_ID = "twin_facet_assembler"
    ASSEMBLER_VERSION = "1.0.0-t1"

    def __init__(
        self,
        *,
        collectors: dict[str, RuntimeACollector] | None = None,
        builders: tuple[FacetBuilder, ...] | None = None,
        study_plan_service: Any | None = None,
        enabled: bool = True,
    ) -> None:
        self._collectors = collectors or build_default_collectors()
        self._builders = builders or default_facet_builders()
        self._study_plan_service = study_plan_service
        self._enabled = bool(enabled)
        validate_no_facet_cross_dependency(
            {
                builder.facet_name: set(builder.source_fields)
                for builder in self._builders
            }
        )

    @property
    def assembler_id(self) -> str:
        return self.ASSEMBLER_ID

    @property
    def assembler_version(self) -> str:
        return self.ASSEMBLER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def collect_evidence(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
    ) -> TwinRuntimeEvidence:
        """Collect immutable Runtime A evidence without synthesising facets.

        Used by EP-001.1 Foundation and by ``assemble`` so collection runs once.
        """
        if not self._enabled:
            raise TwinFacetValidationError(
                "TwinFacetAssembler is disabled (feature flag OFF)"
            )

        clock = validate_as_of(as_of)
        try:
            sid = validate_student_id(student_id)
            user_id = self._parse_user_id(sid)
        except TwinFacetValidationError:
            return TwinRuntimeEvidence(
                student_id=(student_id or "").strip() or "invalid",
                as_of=clock,
            )

        context = self._build_context(user_id)
        results: dict[str, CollectorResult] = {}
        for field_name in RUNTIME_A_FIELD_NAMES:
            collector = self._collectors.get(field_name)
            if collector is None:
                empty: Any = (
                    []
                    if field_name
                    in {FIELD_TOPIC_PROGRESS, FIELD_STUDY_ATTEMPTS}
                    else {}
                )
                if field_name == FIELD_LIFECYCLE_STAGE:
                    empty = ""
                results[field_name] = CollectorResult(
                    available=False,
                    payload=empty,
                    source_service=SOURCE_SERVICE_TWIN_FACET,
                    source_entity=field_name,
                    unavailable_reason="UNAVAILABLE",
                )
                continue
            result = collector.collect(user_id, as_of=clock, context=context)
            results[field_name] = result

        return self._build_evidence(
            student_id=sid,
            as_of=clock,
            results=results,
        )

    def assemble(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
    ) -> TwinFacetBundle:
        """Collect Runtime A evidence and synthesise Twin facets.

        Identical Runtime A inputs + identical ``as_of`` yield identical
        TwinFacetBundle serializations (deterministic).
        """
        if not self._enabled:
            raise TwinFacetValidationError(
                "TwinFacetAssembler is disabled (feature flag OFF)"
            )

        clock = validate_as_of(as_of)
        collected_at = clock
        try:
            validate_student_id(student_id)
        except TwinFacetValidationError:
            return self._unavailable_identity_bundle(
                student_id=(student_id or "").strip() or "invalid",
                as_of=clock,
                collected_at=collected_at,
            )

        evidence = self.collect_evidence(student_id, as_of=clock)
        return self._synthesise(
            evidence=evidence,
            collected_at=collected_at,
        )

    def synthesise_from_evidence(
        self,
        evidence: TwinRuntimeEvidence,
        *,
        collected_at: str | None = None,
    ) -> TwinFacetBundle:
        """Synthesise facets from a pre-built Runtime A evidence bag (tests)."""
        if not self._enabled:
            raise TwinFacetValidationError(
                "TwinFacetAssembler is disabled (feature flag OFF)"
            )
        clock = validate_as_of(evidence.as_of)
        return self._synthesise(
            evidence=TwinRuntimeEvidence(
                student_id=evidence.student_id,
                as_of=clock,
                evidence=dict(evidence.evidence),
                topic_progress=tuple(dict(r) for r in evidence.topic_progress),
                study_attempts=tuple(dict(r) for r in evidence.study_attempts),
                mission=dict(evidence.mission),
                readiness=dict(evidence.readiness),
                curriculum=dict(evidence.curriculum),
                student_goals=dict(evidence.student_goals),
                lifecycle_stage=evidence.lifecycle_stage,
                field_available=dict(evidence.field_available),
                field_reasons=dict(evidence.field_reasons),
                field_sources={
                    k: dict(v) for k, v in evidence.field_sources.items()
                },
            ),
            collected_at=collected_at if collected_at is not None else clock,
        )

    def _synthesise(
        self,
        *,
        evidence: TwinRuntimeEvidence,
        collected_at: str | None,
    ) -> TwinFacetBundle:
        validate_no_estimation_markers(
            evidence.to_canonical_dict(), field_name="runtime_a_evidence"
        )
        built: dict[str, Any] = {}
        provenance: dict[str, TwinProvenance] = {}
        for builder in self._builders:
            result = builder.build(evidence, collected_at=collected_at)
            built[result.facet_name] = result.facet
            provenance[result.facet_name] = result.provenance

        # Ensure every facet name is present even if a custom builder set omits one.
        for name in FACET_SYNTHESIS_ORDER:
            if name in built:
                continue
            built[name] = self._empty_unavailable_facet(name)
            provenance[name] = unavailable_facet_provenance(
                source_service=SOURCE_SERVICE_TWIN_FACET,
                source_entity=name,
                collected_at=collected_at,
                reason="UNAVAILABLE",
                kind=KIND_RUNTIME_A_DERIVED,
            )

        present = tuple(
            name
            for name in FACET_SYNTHESIS_ORDER
            if provenance[name].availability == AVAILABILITY_AVAILABLE
        )
        unavailable = tuple(
            name
            for name in FACET_SYNTHESIS_ORDER
            if provenance[name].availability == AVAILABILITY_UNAVAILABLE
        )
        limitations = tuple(
            provenance[name].unavailable_reason
            for name in unavailable
            if provenance[name].unavailable_reason
        )
        # Deduplicate limitation codes deterministically.
        limitation_codes = tuple(sorted(set(limitations)))

        profile = TwinProfile(
            student_id=evidence.student_id,
            learning_rhythm=built[FACET_LEARNING_RHYTHM],
            consistency=built[FACET_CONSISTENCY],
            persistence=built[FACET_PERSISTENCE],
            revision_behaviour=built[FACET_REVISION_BEHAVIOUR],
            confidence_trend=built[FACET_CONFIDENCE_TREND],
            session_habits=built[FACET_SESSION_HABITS],
            cognitive_load_indicators=built[FACET_COGNITIVE_LOAD],
            limitations_codes=limitation_codes,
            limitations_summary=(
                "Twin facet synthesis from Runtime A"
                if present
                else "No Twin facets available from Runtime A evidence"
            ),
        )
        completeness = TwinCompleteness(
            score=None,
            facets_present=present,
            facets_unavailable=unavailable,
            summary=(
                f"present={len(present)};unavailable={len(unavailable)}"
            ),
        )
        validate_facet_provenance_map(provenance)
        evidence_version = self._evidence_version(evidence)
        return TwinFacetBundle(
            student_id=evidence.student_id,
            as_of=evidence.as_of,
            profile=profile,
            field_provenance=provenance,
            completeness=completeness,
            source_evidence_version=evidence_version,
            profile_version=FACET_PROFILE_VERSION,
            authority=AUTHORITY_DIGITAL_TWIN,
        )

    def _build_evidence(
        self,
        *,
        student_id: str,
        as_of: str | None,
        results: dict[str, CollectorResult],
    ) -> TwinRuntimeEvidence:
        field_available: dict[str, bool] = {}
        field_reasons: dict[str, str] = {}
        field_sources: dict[str, dict[str, str]] = {}

        def _register(name: str, result: CollectorResult) -> None:
            field_available[name] = bool(result.available)
            field_reasons[name] = (
                "" if result.available else (result.unavailable_reason or "")
            )
            field_sources[name] = {
                "source_service": result.source_service,
                "source_entity": result.source_entity,
            }

        evidence_result = results[FIELD_EVIDENCE]
        _register(FIELD_EVIDENCE, evidence_result)
        evidence_payload = (
            normalize_evidence(evidence_result.payload)
            if evidence_result.available
            else {}
        )

        progress_result = results[FIELD_TOPIC_PROGRESS]
        _register(FIELD_TOPIC_PROGRESS, progress_result)
        topic_progress = (
            normalize_topic_progress(progress_result.payload)
            if progress_result.available
            else []
        )

        attempts_result = results[FIELD_STUDY_ATTEMPTS]
        _register(FIELD_STUDY_ATTEMPTS, attempts_result)
        study_attempts = (
            normalize_study_attempts(attempts_result.payload)
            if attempts_result.available
            else []
        )

        mission_result = results[FIELD_MISSION]
        _register(FIELD_MISSION, mission_result)
        mission = (
            normalize_mission(mission_result.payload)
            if mission_result.available
            else {}
        )

        readiness_result = results[FIELD_READINESS]
        _register(FIELD_READINESS, readiness_result)
        readiness = (
            normalize_readiness(readiness_result.payload)
            if readiness_result.available
            else {}
        )

        curriculum_result = results[FIELD_CURRICULUM]
        _register(FIELD_CURRICULUM, curriculum_result)
        curriculum = (
            normalize_curriculum(curriculum_result.payload)
            if curriculum_result.available
            else {}
        )

        goals_result = results[FIELD_STUDENT_GOALS]
        _register(FIELD_STUDENT_GOALS, goals_result)
        student_goals = (
            normalize_student_goals(goals_result.payload)
            if goals_result.available
            else {}
        )

        lifecycle_result = results[FIELD_LIFECYCLE_STAGE]
        _register(FIELD_LIFECYCLE_STAGE, lifecycle_result)
        lifecycle_stage = (
            normalize_lifecycle_stage(lifecycle_result.payload)
            if lifecycle_result.available
            else ""
        )

        return TwinRuntimeEvidence(
            student_id=student_id,
            as_of=as_of,
            evidence=evidence_payload,
            topic_progress=tuple(topic_progress),
            study_attempts=tuple(study_attempts),
            mission=mission,
            readiness=readiness,
            curriculum=curriculum,
            student_goals=student_goals,
            lifecycle_stage=lifecycle_stage,
            field_available=field_available,
            field_reasons=field_reasons,
            field_sources=field_sources,
        )

    def _build_context(self, user_id: int) -> dict[str, Any]:
        """Load shared read-only context (active plan) once."""
        plan = None
        try:
            if self._study_plan_service is not None:
                plan = self._study_plan_service.read_active_plan(user_id)
            else:
                plan = read_active_study_plan(user_id)
        except Exception:  # noqa: BLE001
            logger.debug(
                "active plan lookup failed user_id=%s", user_id, exc_info=True
            )
            plan = None
        context: dict[str, Any] = {"active_plan": plan}
        if plan is not None:
            context["study_plan_id"] = plan.id
        return context

    @staticmethod
    def _parse_user_id(student_id: str) -> int:
        try:
            return int(student_id)
        except (TypeError, ValueError) as exc:
            raise TwinFacetValidationError(
                "student_id must be a numeric Runtime A user id"
            ) from exc

    @staticmethod
    def _evidence_version(evidence: TwinRuntimeEvidence) -> str:
        payload = serialize_canonical(evidence.to_canonical_dict())
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return f"runtime_a:{digest[:16]}"

    def _unavailable_identity_bundle(
        self,
        *,
        student_id: str,
        as_of: str | None,
        collected_at: str | None,
    ) -> TwinFacetBundle:
        provenance = {
            name: unavailable_facet_provenance(
                source_service=SOURCE_SERVICE_TWIN_FACET,
                source_entity=name,
                collected_at=collected_at,
                reason=REASON_INVALID_STUDENT_ID,
            )
            for name in FACET_SYNTHESIS_ORDER
        }
        profile = TwinProfile(
            student_id=student_id,
            learning_rhythm=LearningRhythmFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            consistency=ConsistencyFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            persistence=PersistenceFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            revision_behaviour=RevisionBehaviourFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            confidence_trend=ConfidenceTrendFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            session_habits=SessionHabitsFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            cognitive_load_indicators=CognitiveLoadIndicatorsFacet(
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=REASON_INVALID_STUDENT_ID,
            ),
            limitations_codes=(REASON_INVALID_STUDENT_ID,),
            limitations_summary="Invalid student_id — Twin facets unavailable",
        )
        return TwinFacetBundle(
            student_id=student_id,
            as_of=as_of,
            profile=profile,
            field_provenance=provenance,
            completeness=TwinCompleteness(
                score=None,
                facets_present=(),
                facets_unavailable=FACET_SYNTHESIS_ORDER,
                summary="present=0;unavailable=7",
            ),
            source_evidence_version="",
            authority=AUTHORITY_RUNTIME_A,
        )

    @staticmethod
    def _empty_unavailable_facet(name: str) -> Any:
        mapping = {
            FACET_LEARNING_RHYTHM: LearningRhythmFacet,
            FACET_CONSISTENCY: ConsistencyFacet,
            FACET_PERSISTENCE: PersistenceFacet,
            FACET_REVISION_BEHAVIOUR: RevisionBehaviourFacet,
            FACET_CONFIDENCE_TREND: ConfidenceTrendFacet,
            FACET_SESSION_HABITS: SessionHabitsFacet,
            FACET_COGNITIVE_LOAD: CognitiveLoadIndicatorsFacet,
        }
        cls = mapping[name]
        return cls(
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="UNAVAILABLE",
        )


def build_twin_facet_assembler(
    *,
    enabled: bool,
    collectors: dict[str, RuntimeACollector] | None = None,
    builders: tuple[FacetBuilder, ...] | None = None,
    study_plan_service: Any | None = None,
) -> TwinFacetAssembler | None:
    """DI helper — construct TwinFacetAssembler only when the flag is on."""
    if not enabled:
        return None
    return TwinFacetAssembler(
        collectors=collectors,
        builders=builders,
        study_plan_service=study_plan_service,
        enabled=True,
    )

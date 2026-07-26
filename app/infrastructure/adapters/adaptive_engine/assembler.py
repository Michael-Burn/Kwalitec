"""Adaptive Input Assembler (MS-003 A1; MS-004 T4 Twin consumption).

Gathers authoritative Runtime A educational data into immutable
AdaptiveInputBundles. Optionally attaches read-only TwinSnapshot enrichment
via TwinInputAdapter when Digital Twin is enabled. Performs collection,
validation, normalization, and provenance annotation only — no adaptive
reasoning, scoring, ranking, Twin synthesis, or Twin persistence.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from app.infrastructure.adapters.adaptive_engine.collectors import (
    CollectorResult,
    RuntimeACollector,
    build_default_collectors,
    read_active_study_plan,
)
from app.infrastructure.adapters.adaptive_engine.contracts import (
    AUTHORITY_RUNTIME_A,
    AdaptiveInputBundle,
)

if TYPE_CHECKING:
    from app.infrastructure.adapters.adaptive_engine.twin_input import TwinInputAdapter
    from app.infrastructure.adapters.digital_twin.contracts import (
        SnapshotExplanation,
        TwinSnapshot,
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
from app.infrastructure.adapters.adaptive_engine.provenance import (
    FIELD_CURRICULUM,
    FIELD_EVIDENCE,
    FIELD_LIFECYCLE_STAGE,
    FIELD_MISSION,
    FIELD_READINESS,
    FIELD_STUDENT_GOALS,
    FIELD_STUDY_ATTEMPTS,
    FIELD_TOPIC_PROGRESS,
    INPUT_FIELD_NAMES,
    REASON_INVALID_STUDENT_ID,
    FieldProvenance,
    available_provenance,
    unavailable_provenance,
)
from app.infrastructure.adapters.adaptive_engine.validation import (
    AdaptiveInputValidationError,
    validate_as_of,
    validate_collector_result,
    validate_no_estimation_markers,
    validate_provenance_map,
    validate_student_id,
    validate_unavailable_payload_empty,
)

logger = logging.getLogger(__name__)


class AdaptiveInputAssembler:
    """Assemble AdaptiveInputBundle from Runtime A collectors (+ optional Twin).

    Rules:
    - MAY collect, normalize, validate, annotate provenance
    - MAY attach TwinSnapshot enrichment via TwinInputAdapter (read-only)
    - MUST NOT estimate missing values, infer educational state beyond
      pass-through, rank recommendations, score topics, mutate Runtime A,
      synthesise Twin, or persist Twin data
    """

    ASSEMBLER_ID = "adaptive_input_assembler"
    ASSEMBLER_VERSION = "1.1.0-t4"

    def __init__(
        self,
        *,
        collectors: dict[str, RuntimeACollector] | None = None,
        study_plan_service: Any | None = None,
        twin_input: TwinInputAdapter | None = None,
        enabled: bool = True,
    ) -> None:
        self._collectors = collectors or build_default_collectors()
        self._study_plan_service = study_plan_service
        self._twin_input = twin_input
        self._enabled = bool(enabled)

    @property
    def assembler_id(self) -> str:
        return self.ASSEMBLER_ID

    @property
    def assembler_version(self) -> str:
        return self.ASSEMBLER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def twin_input(self) -> TwinInputAdapter | None:
        return self._twin_input

    def assemble(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        twin_snapshot: TwinSnapshot | None = None,
        twin_explanation: SnapshotExplanation | None = None,
    ) -> AdaptiveInputBundle:
        """Collect, validate, and normalize Runtime A inputs into a bundle.

        Optional TwinSnapshot enrichment is attached when ``twin_input`` is
        wired (KWALITEC_DIGITAL_TWIN). Twin absence fail-opens to unavailable
        Twin attachment — Runtime A fields remain authoritative.

        Identical Runtime A inputs + identical ``as_of`` (+ identical Twin
        attachment when present) yield identical AdaptiveInputBundle
        serializations (deterministic).
        """
        if not self._enabled:
            raise AdaptiveInputValidationError(
                "AdaptiveInputAssembler is disabled (feature flag OFF)"
            )

        clock = validate_as_of(as_of)
        collected_at = clock or ""
        try:
            sid = validate_student_id(student_id)
            user_id = self._parse_user_id(sid)
        except AdaptiveInputValidationError:
            # Explicit unavailable contract for invalid identity.
            return self._maybe_attach_twin(
                self._unavailable_identity_bundle(
                    student_id=(student_id or "").strip() or "invalid",
                    as_of=as_of,
                    collected_at=collected_at,
                ),
                twin_snapshot=twin_snapshot,
                twin_explanation=twin_explanation,
                collected_at=collected_at,
            )

        context = self._build_context(user_id)

        results: dict[str, CollectorResult] = {}
        for field_name in INPUT_FIELD_NAMES:
            collector = self._collectors.get(field_name)
            if collector is None:
                results[field_name] = CollectorResult(
                    available=False,
                    payload={} if field_name not in {
                        FIELD_TOPIC_PROGRESS,
                        FIELD_STUDY_ATTEMPTS,
                    } else [],
                    source_service="adaptive_input_assembler",
                    source_entity=field_name,
                    unavailable_reason="UNAVAILABLE",
                )
                continue
            result = collector.collect(user_id, as_of=clock, context=context)
            validate_collector_result(result, field_name=field_name)
            results[field_name] = result

        bundle = self._build_bundle(
            student_id=sid,
            as_of=clock,
            collected_at=collected_at,
            results=results,
        )
        return self._maybe_attach_twin(
            bundle,
            twin_snapshot=twin_snapshot,
            twin_explanation=twin_explanation,
            collected_at=collected_at,
        )

    def _maybe_attach_twin(
        self,
        bundle: AdaptiveInputBundle,
        *,
        twin_snapshot: TwinSnapshot | None,
        twin_explanation: SnapshotExplanation | None,
        collected_at: str,
    ) -> AdaptiveInputBundle:
        """Attach Twin enrichment when TwinInputAdapter is wired; else unchanged."""
        if self._twin_input is None:
            return bundle
        return self._twin_input.enrich_bundle(
            bundle,
            snapshot=twin_snapshot,
            explanation=twin_explanation,
            collected_at=collected_at,
        )

    def _build_context(self, user_id: int) -> dict[str, Any]:
        """Load shared read-only context (active plan) once.

        Prefer injected test doubles exposing ``read_active_plan``; otherwise
        use the package ORM read helper (never a StudyPlanService path that
        may self-heal curriculum binding and commit).
        """
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
            raise AdaptiveInputValidationError(
                "student_id must be a numeric Runtime A user id"
            ) from exc
    def _build_bundle(
        self,
        *,
        student_id: str,
        as_of: str | None,
        collected_at: str,
        results: dict[str, CollectorResult],
    ) -> AdaptiveInputBundle:
        provenance: dict[str, FieldProvenance] = {}
        authority_tags: list[str] = [AUTHORITY_RUNTIME_A]

        def _prov(field_name: str, result: CollectorResult) -> FieldProvenance:
            if result.available:
                entry = available_provenance(
                    source_service=result.source_service,
                    source_entity=result.source_entity,
                    collected_at=collected_at,
                )
            else:
                entry = unavailable_provenance(
                    source_service=result.source_service,
                    source_entity=result.source_entity,
                    collected_at=collected_at,
                    reason=result.unavailable_reason,
                )
            provenance[field_name] = entry
            if result.source_service and result.source_service not in authority_tags:
                authority_tags.append(result.source_service)
            return entry

        evidence_result = results[FIELD_EVIDENCE]
        evidence_prov = _prov(FIELD_EVIDENCE, evidence_result)
        evidence = (
            normalize_evidence(evidence_result.payload)
            if evidence_result.available
            else {}
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_EVIDENCE,
            availability=evidence_prov.availability,
            payload=evidence,
        )
        validate_no_estimation_markers(evidence, field_name=FIELD_EVIDENCE)

        progress_result = results[FIELD_TOPIC_PROGRESS]
        progress_prov = _prov(FIELD_TOPIC_PROGRESS, progress_result)
        topic_progress = (
            normalize_topic_progress(progress_result.payload)
            if progress_result.available
            else []
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_TOPIC_PROGRESS,
            availability=progress_prov.availability,
            payload=topic_progress,
        )
        validate_no_estimation_markers(
            topic_progress, field_name=FIELD_TOPIC_PROGRESS
        )

        attempts_result = results[FIELD_STUDY_ATTEMPTS]
        attempts_prov = _prov(FIELD_STUDY_ATTEMPTS, attempts_result)
        study_attempts = (
            normalize_study_attempts(attempts_result.payload)
            if attempts_result.available
            else []
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_STUDY_ATTEMPTS,
            availability=attempts_prov.availability,
            payload=study_attempts,
        )
        validate_no_estimation_markers(
            study_attempts, field_name=FIELD_STUDY_ATTEMPTS
        )

        mission_result = results[FIELD_MISSION]
        mission_prov = _prov(FIELD_MISSION, mission_result)
        mission = (
            normalize_mission(mission_result.payload)
            if mission_result.available
            else {}
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_MISSION,
            availability=mission_prov.availability,
            payload=mission,
        )
        validate_no_estimation_markers(mission, field_name=FIELD_MISSION)

        readiness_result = results[FIELD_READINESS]
        readiness_prov = _prov(FIELD_READINESS, readiness_result)
        readiness = (
            normalize_readiness(readiness_result.payload)
            if readiness_result.available
            else {}
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_READINESS,
            availability=readiness_prov.availability,
            payload=readiness,
        )
        validate_no_estimation_markers(readiness, field_name=FIELD_READINESS)

        curriculum_result = results[FIELD_CURRICULUM]
        curriculum_prov = _prov(FIELD_CURRICULUM, curriculum_result)
        curriculum = (
            normalize_curriculum(curriculum_result.payload)
            if curriculum_result.available
            else {}
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_CURRICULUM,
            availability=curriculum_prov.availability,
            payload=curriculum,
        )
        validate_no_estimation_markers(curriculum, field_name=FIELD_CURRICULUM)

        goals_result = results[FIELD_STUDENT_GOALS]
        goals_prov = _prov(FIELD_STUDENT_GOALS, goals_result)
        student_goals = (
            normalize_student_goals(goals_result.payload)
            if goals_result.available
            else {}
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_STUDENT_GOALS,
            availability=goals_prov.availability,
            payload=student_goals,
        )
        validate_no_estimation_markers(
            student_goals, field_name=FIELD_STUDENT_GOALS
        )

        lifecycle_result = results[FIELD_LIFECYCLE_STAGE]
        lifecycle_prov = _prov(FIELD_LIFECYCLE_STAGE, lifecycle_result)
        lifecycle_stage = (
            normalize_lifecycle_stage(lifecycle_result.payload)
            if lifecycle_result.available
            else ""
        )
        validate_unavailable_payload_empty(
            field_name=FIELD_LIFECYCLE_STAGE,
            availability=lifecycle_prov.availability,
            payload={"stage": lifecycle_stage} if lifecycle_stage else {},
        )

        validate_provenance_map(provenance)
        # Stable authority tag order.
        ordered_tags = tuple(
            sorted(set(authority_tags), key=lambda t: (t != AUTHORITY_RUNTIME_A, t))
        )

        return AdaptiveInputBundle(
            student_id=student_id,
            as_of=as_of,
            evidence=evidence,
            topic_progress=tuple(topic_progress),
            study_attempts=tuple(study_attempts),
            readiness=readiness,
            mission=mission,
            curriculum=curriculum,
            student_goals=student_goals,
            authority_tags=ordered_tags,
            lifecycle_stage=lifecycle_stage,
            field_provenance=provenance,
        )

    def _unavailable_identity_bundle(
        self,
        *,
        student_id: str,
        as_of: str | None,
        collected_at: str,
    ) -> AdaptiveInputBundle:
        """Return a fully unavailable bundle for invalid student identity."""
        provenance = {
            name: unavailable_provenance(
                source_service="adaptive_input_assembler",
                source_entity=name,
                collected_at=collected_at,
                reason=REASON_INVALID_STUDENT_ID,
            )
            for name in INPUT_FIELD_NAMES
        }
        return AdaptiveInputBundle(
            student_id=student_id or "invalid",
            as_of=validate_as_of(as_of),
            evidence={},
            topic_progress=(),
            study_attempts=(),
            readiness={},
            mission={},
            curriculum={},
            student_goals={},
            authority_tags=(AUTHORITY_RUNTIME_A,),
            lifecycle_stage="",
            field_provenance=provenance,
        )


def build_adaptive_input_assembler(
    *,
    enabled: bool,
    collectors: dict[str, RuntimeACollector] | None = None,
    study_plan_service: Any | None = None,
    twin_input: TwinInputAdapter | None = None,
) -> AdaptiveInputAssembler | None:
    """DI helper — construct AdaptiveInputAssembler only when the flag is on."""
    if not enabled:
        return None
    return AdaptiveInputAssembler(
        collectors=collectors,
        study_plan_service=study_plan_service,
        twin_input=twin_input,
        enabled=True,
    )

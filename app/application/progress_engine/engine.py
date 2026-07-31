"""Progress Engine — sole curriculum progression AUTHORITY (SR-003).

Integrates Accepted educational evidence decisions, mission completion
signals, curriculum structure, and optional Twin estimates into one
Study Progress truth.

MUST NOT evaluate evidence, update Twin, run sessions, teach, or generate
evidence. EducationalEvidenceAuthority remains sole Evidence Authority;
StudentTwinEngine remains sole learner estimation AUTHORITY;
LearningSessionRuntime remains sole Session AUTHORITY.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.progress_engine.dto import (
    CoverageAdvanceDecision,
    CurriculumPosition,
    MissionCompositionInputs,
    ProgressProjection,
    StudyProgress,
    TwinEstimateInput,
)
from app.application.progress_engine.exceptions import DuplicateProgressWriter
from app.domain.educational_runtime_engine.events import EducationalEventRecord
from app.domain.educational_runtime_engine.progress import (
    DerivedProgress,
    ProgressModelSpec,
    ProgressTopicSpec,
    derive_progress,
)

logger = logging.getLogger(__name__)

# Process-scoped sole-writer registry (tests + runtime assert singularity).
_REGISTERED_WRITER: str | None = None

# Weak-topic threshold for optional Twin annotation (projection only).
_WEAK_MASTERY_THRESHOLD = 0.45


def register_progress_writer(writer_id: str) -> None:
    """Register the sole progress writer identity.

    Raises DuplicateProgressWriter when a second distinct writer registers
    while SR_PROGRESS_SINGULARITY is conceptually active in-process.
    """
    global _REGISTERED_WRITER
    wid = str(writer_id).strip()
    if not wid:
        raise ValueError("writer_id required")
    if _REGISTERED_WRITER is not None and _REGISTERED_WRITER != wid:
        raise DuplicateProgressWriter(
            f"progress writer already registered as {_REGISTERED_WRITER!r}; "
            f"refusing second writer {wid!r}"
        )
    _REGISTERED_WRITER = wid


def clear_progress_writer_registry() -> None:
    """Test / rollback helper — clear sole-writer registry."""
    global _REGISTERED_WRITER
    _REGISTERED_WRITER = None


def registered_progress_writer() -> str | None:
    return _REGISTERED_WRITER


class ProgressEngine:
    """Singular Progress Authority for curriculum coverage and position.

    Consumes Authority-accepted evidence columns and curriculum structure.
    Twin estimates are optional projection inputs only.
    """

    AUTHORITY_ID = "progress_engine"
    AUTHORITY_VERSION = "1.0.0"
    WEAK_MASTERY_THRESHOLD = _WEAK_MASTERY_THRESHOLD

    def __init__(
        self,
        *,
        flag_resolver: Callable[[], Any] | None = None,
    ) -> None:
        self._flag_resolver = flag_resolver or resolve_v2_feature_flags

    def singularity_enabled(self) -> bool:
        flags = self._flag_resolver()
        return bool(getattr(flags, "SR_PROGRESS_SINGULARITY", False))

    def claim_sole_writer(self, writer_id: str = AUTHORITY_ID) -> None:
        """Register this engine as the sole progress writer (singularity ON)."""
        register_progress_writer(writer_id)

    # ── Advance gate (trusts Evidence Authority; never re-evaluates) ─────

    def authorise_coverage_advance(
        self,
        *,
        may_advance_progress: bool,
        evidence_disposition: str | None = None,
        may_complete_mission: bool | None = None,
        topic_id: str | None = None,
        package_id: str | None = None,
        mission_instance_id: str | None = None,
    ) -> CoverageAdvanceDecision:
        """Decide whether coverage may advance for one sitting.

        Rejected evidence and Authority denials are ignored (no advance).
        Does not inspect observation payloads or regrade packages.
        """
        disposition = (evidence_disposition or "").strip().lower() or None
        if disposition == "rejected":
            return CoverageAdvanceDecision(
                may_advance=False,
                reason="rejected_evidence_ignored",
                evidence_disposition=disposition,
                topic_id=topic_id,
                package_id=package_id,
                mission_instance_id=mission_instance_id,
            )
        if may_complete_mission is False:
            return CoverageAdvanceDecision(
                may_advance=False,
                reason="mission_completion_not_authorised",
                evidence_disposition=disposition,
                topic_id=topic_id,
                package_id=package_id,
                mission_instance_id=mission_instance_id,
            )
        if not may_advance_progress:
            return CoverageAdvanceDecision(
                may_advance=False,
                reason="authority_denied_progress_advance",
                evidence_disposition=disposition,
                topic_id=topic_id,
                package_id=package_id,
                mission_instance_id=mission_instance_id,
            )
        return CoverageAdvanceDecision(
            may_advance=True,
            reason="authority_accepted_coverage_advance",
            evidence_disposition=disposition,
            topic_id=topic_id,
            package_id=package_id,
            mission_instance_id=mission_instance_id,
        )

    def authorise_from_validation(
        self,
        validation: Any,
        *,
        topic_id: str | None = None,
        package_id: str | None = None,
        mission_instance_id: str | None = None,
    ) -> CoverageAdvanceDecision:
        """Authorise from an EvidenceValidationResult (or duck-typed equivalent)."""
        if validation is None:
            return CoverageAdvanceDecision(
                may_advance=False,
                reason="missing_validation",
                topic_id=topic_id,
                package_id=package_id,
                mission_instance_id=mission_instance_id,
            )
        disposition = getattr(validation, "disposition", None)
        disposition_value = (
            disposition.value if hasattr(disposition, "value") else disposition
        )
        return self.authorise_coverage_advance(
            may_advance_progress=bool(
                getattr(validation, "may_advance_progress", False)
            ),
            evidence_disposition=(
                str(disposition_value) if disposition_value is not None else None
            ),
            may_complete_mission=bool(
                getattr(validation, "may_complete_mission", False)
            ),
            topic_id=topic_id,
            package_id=package_id,
            mission_instance_id=mission_instance_id,
        )

    # ── Derive Study Progress ────────────────────────────────────────────

    def derive_study_progress(
        self,
        progress_model: ProgressModelSpec,
        events: tuple[EducationalEventRecord, ...] | list[EducationalEventRecord],
        *,
        twin_estimates: TwinEstimateInput | None = None,
    ) -> StudyProgress:
        """Derive singular Study Progress from events + curriculum structure.

        Twin estimates are optional. Coverage is deterministic from
        TOPIC_COMPLETED events alone.
        """
        derived = derive_progress(progress_model, events)
        twin = twin_estimates or TwinEstimateInput.absent()
        return self._assemble(progress_model, derived, twin)

    def from_derived(
        self,
        progress_model: ProgressModelSpec,
        derived: DerivedProgress,
        *,
        twin_estimates: TwinEstimateInput | None = None,
    ) -> StudyProgress:
        """Assemble Study Progress from an already-derived coverage snapshot."""
        twin = twin_estimates or TwinEstimateInput.absent()
        return self._assemble(progress_model, derived, twin)

    def curriculum_position(
        self,
        progress_model: ProgressModelSpec,
        events: tuple[EducationalEventRecord, ...] | list[EducationalEventRecord],
    ) -> CurriculumPosition:
        """Compute unique curriculum position (current topic is singular)."""
        study = self.derive_study_progress(progress_model, events)
        return study.position

    def progress_projection(
        self,
        study_progress: StudyProgress,
        *,
        twin_estimates: TwinEstimateInput | None = None,
    ) -> ProgressProjection:
        """Expose progress projections; Twin absence is fully supported."""
        twin = twin_estimates or TwinEstimateInput.absent()
        return self._build_projection(study_progress.incomplete_topic_ids, twin)

    def mission_composition_inputs(
        self,
        study_progress: StudyProgress,
    ) -> MissionCompositionInputs:
        """Provide Progress inputs for tomorrow's mission composition."""
        return MissionCompositionInputs(
            curriculum_identity=study_progress.curriculum_identity,
            current_topic_id=study_progress.current_topic_id,
            completed_topic_ids=study_progress.completed_topic_ids,
            remaining_topic_ids=study_progress.incomplete_topic_ids,
            coverage_ratio=study_progress.coverage_ratio,
            journey_stage=study_progress.journey_stage,
            syllabus_complete=study_progress.syllabus_complete,
            weak_topic_ids=study_progress.projection.weak_topic_ids,
            twin_present=study_progress.projection.twin_present,
        )

    # ── Internals ────────────────────────────────────────────────────────

    def _assemble(
        self,
        progress_model: ProgressModelSpec,
        derived: DerivedProgress,
        twin: TwinEstimateInput,
    ) -> StudyProgress:
        topic_specs = {t.topic_id: t for t in progress_model.topics}
        completed_objectives, remaining_objectives = _objective_rollups(
            topic_specs=topic_specs,
            topic_ids=derived.topic_ids,
            completed_topic_ids=derived.completed_topic_ids,
        )
        position = _position_from_derived(derived)
        projection = self._build_projection(derived.incomplete_topic_ids, twin)
        return StudyProgress(
            curriculum_identity=derived.curriculum_identity,
            topic_ids=derived.topic_ids,
            completed_topic_ids=derived.completed_topic_ids,
            incomplete_topic_ids=derived.incomplete_topic_ids,
            current_topic_id=derived.current_topic_id,
            coverage_ratio=derived.coverage_ratio,
            journey_stage=derived.journey_stage.value,
            syllabus_complete=derived.syllabus_complete,
            completed_objective_ids=completed_objectives,
            remaining_objective_ids=remaining_objectives,
            position=position,
            projection=projection,
            twin_estimates_applied=twin.is_present(),
            authority=self.AUTHORITY_ID,
        )

    def _build_projection(
        self,
        remaining_topic_ids: tuple[str, ...],
        twin: TwinEstimateInput,
    ) -> ProgressProjection:
        next_topic = remaining_topic_ids[0] if remaining_topic_ids else None
        if not twin.is_present():
            return ProgressProjection(
                remaining_topic_ids=remaining_topic_ids,
                next_topic_id=next_topic,
                estimated_topics_remaining=len(remaining_topic_ids),
                twin_present=False,
                twin_annotated_remaining=(),
                weak_topic_ids=(),
                overall_estimated_mastery=None,
                overall_estimated_knowledge=None,
                projection_basis="coverage_only",
            )

        annotated: list[dict[str, Any]] = []
        weak: list[str] = []
        for topic_id in remaining_topic_ids:
            mastery = twin.estimated_mastery.get(topic_id)
            knowledge = twin.estimated_knowledge.get(topic_id)
            entry: dict[str, Any] = {"topic_id": topic_id}
            if mastery is not None:
                entry["estimated_mastery"] = mastery
                if mastery < self.WEAK_MASTERY_THRESHOLD:
                    weak.append(topic_id)
                    entry["weak"] = True
            if knowledge is not None:
                entry["estimated_knowledge"] = knowledge
            annotated.append(entry)

        return ProgressProjection(
            remaining_topic_ids=remaining_topic_ids,
            next_topic_id=next_topic,
            estimated_topics_remaining=len(remaining_topic_ids),
            twin_present=True,
            twin_annotated_remaining=tuple(annotated),
            weak_topic_ids=tuple(weak),
            overall_estimated_mastery=twin.overall_mastery,
            overall_estimated_knowledge=twin.overall_knowledge,
            projection_basis="coverage_plus_optional_twin",
        )


def _position_from_derived(derived: DerivedProgress) -> CurriculumPosition:
    index: int | None = None
    if derived.current_topic_id is not None:
        try:
            index = derived.topic_ids.index(derived.current_topic_id)
        except ValueError:
            index = None
    return CurriculumPosition(
        curriculum_identity=derived.curriculum_identity,
        current_topic_id=derived.current_topic_id,
        current_topic_index=index,
        topic_count=len(derived.topic_ids),
        completed_count=len(derived.completed_topic_ids),
        remaining_count=len(derived.incomplete_topic_ids),
        coverage_ratio=derived.coverage_ratio,
        journey_stage=derived.journey_stage.value,
        syllabus_complete=derived.syllabus_complete,
    )


def _objective_rollups(
    *,
    topic_specs: dict[str, ProgressTopicSpec],
    topic_ids: tuple[str, ...],
    completed_topic_ids: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    completed_set = set(completed_topic_ids)
    completed_objectives: list[str] = []
    remaining_objectives: list[str] = []
    seen_completed: set[str] = set()
    seen_remaining: set[str] = set()
    for topic_id in topic_ids:
        spec = topic_specs.get(topic_id)
        objectives = spec.objective_ids if spec is not None else ()
        if topic_id in completed_set:
            for oid in objectives:
                if oid not in seen_completed:
                    seen_completed.add(oid)
                    completed_objectives.append(oid)
        else:
            for oid in objectives:
                if oid not in seen_remaining:
                    seen_remaining.add(oid)
                    remaining_objectives.append(oid)
    return tuple(completed_objectives), tuple(remaining_objectives)

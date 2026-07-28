"""MissionPlanningService — plan study missions from validated Twin decisions.

Pipeline:
  EducationalDecisionSet (+ Twin)
    → MissionPlanningStarted
    → CandidateBuilder
    → PlanningBatch
    → PlanningValidator
    → StudyMissionPlan + MissionGenerated / MissionPlanningSkipped
    → MissionPlanningCompleted
    → PlanningPersistenceService
    → STOP

Does not modify Twin belief, Learning Graph, Tutor, Assessment, or Reasoning.
Does not interpret assessment evidence. Never invents missing learner state.
Uses existing Adaptive Mission prioritisation scoring only.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.mission_engine.planning.candidate_builder import CandidateBuilder
from app.application.mission_engine.planning.persistence import (
    PlanningPersistenceService,
)
from app.application.mission_engine.planning.validator import PlanningValidator
from app.application.mission_engine.planning.versions import PLANNING_VERSION
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.mission.planning.batch import PlanningBatch
from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.context import PlanningContext
from app.domain.mission.planning.events import (
    MissionGenerated,
    MissionPlanningCompleted,
    MissionPlanningSkipped,
    MissionPlanningStarted,
)
from app.domain.mission.planning.plan import StudyMissionPlan
from app.domain.mission.planning.result import PlanningEvent, PlanningResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


class MissionPlanningService:
    """Deterministic Twin → Mission planning (AP-002D5)."""

    def __init__(
        self,
        *,
        persistence: PlanningPersistenceService | None = None,
        validator: PlanningValidator | None = None,
    ) -> None:
        self._persistence = persistence or PlanningPersistenceService()
        self._validator = validator

    @property
    def persistence(self) -> PlanningPersistenceService:
        return self._persistence

    def plan(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        learning_graph: LearningGraph | None = None,
        available_minutes: int = 45,
        curriculum_position: str = "",
        planned_at: datetime | None = None,
        persist: bool = True,
        allow_idempotent_skip: bool = True,
    ) -> PlanningResult:
        """Plan a study mission from validated Twin decisions.

        Args:
            twin: Authoritative learner Twin after belief update.
            decision_set: Validated educational decisions to consume.
            learning_graph: Optional Graph for recovery-path structure only.
            available_minutes: Existing workload constraint (planning budget).
            curriculum_position: Optional current curriculum entity id.
            planned_at: Deterministic timestamp for replay.
            persist: Persist into the planning ledger when True.
            allow_idempotent_skip: When True, duplicate request/candidate ids
                emit MissionPlanningSkipped instead of raising.

        Returns:
            PlanningResult with batch, study mission plan, and factual events.
        """
        self._assert_twin_version(twin)
        when = planned_at or datetime.now(UTC).replace(tzinfo=None)
        context = PlanningContext(
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            reasoning_request_id=decision_set.context.reasoning_request_id,
            evidence_bundle_id=decision_set.context.evidence_bundle_id,
            session_id=decision_set.context.session_id,
            correlation_id=decision_set.context.correlation_id,
            planning_version=PLANNING_VERSION,
            decision_version=decision_set.decision_version,
            twin_version=twin.version,
            decision_set_id=decision_set.set_id,
            available_minutes=available_minutes,
            curriculum_position=curriculum_position or "",
        )

        events: list[PlanningEvent] = [
            MissionPlanningStarted(
                event_id=(
                    f"ev-start:{context.mission_request_id}:{PLANNING_VERSION}"
                ),
                twin_id=twin.twin_id,
                decision_set_id=decision_set.set_id,
                mission_request_id=context.mission_request_id,
                occurred_at=when,
                planning_version=PLANNING_VERSION,
            )
        ]

        existing_requests = self._persistence.existing_request_ids(
            twin_id=twin.twin_id
        )
        existing_candidates = self._persistence.existing_candidate_ids(
            twin_id=twin.twin_id
        )

        if context.mission_request_id in existing_requests:
            if not allow_idempotent_skip:
                from app.domain.mission.planning.errors import DuplicateMissionRequest

                raise DuplicateMissionRequest(
                    f"duplicate mission request: {context.mission_request_id!r}"
                )
            events.append(
                MissionPlanningSkipped(
                    event_id=(
                        f"ev-skip-req:{context.mission_request_id}:{PLANNING_VERSION}"
                    ),
                    twin_id=twin.twin_id,
                    decision_id=decision_set.decision_ids[0]
                    if decision_set.decision_ids
                    else decision_set.set_id,
                    reason_code="duplicate_mission_request",
                    occurred_at=when,
                    planning_version=PLANNING_VERSION,
                    plan_id=f"smp-dup:{context.mission_request_id}",
                )
            )
            empty_plan = self._empty_plan(
                twin=twin,
                context=context,
                when=when,
                prior_plan_ids=tuple(
                    self._persistence.version_history(twin_id=twin.twin_id)
                ),
                validation_summary="Duplicate mission request — planning skipped.",
            )
            events.append(
                self._completed_event(
                    twin=twin,
                    context=context,
                    plan=empty_plan,
                    candidate_count=0,
                    skipped_count=1,
                    when=when,
                )
            )
            result = PlanningResult(
                context=context,
                batch=PlanningBatch(
                    batch_id=f"mpb-dup:{context.mission_request_id}",
                    candidates=(),
                    context=context,
                    planning_version=PLANNING_VERSION,
                    skipped_decision_ids=tuple(decision_set.decision_ids),
                ),
                study_mission_plan=empty_plan,
                planned_at=when,
                events=tuple(events),
            )
            return result if not persist else self._persistence.persist(result)

        if learning_graph is not None and learning_graph.twin_id != twin.twin_id:
            from app.domain.mission.planning.errors import PlanningRejected

            raise PlanningRejected(
                f"graph twin_id {learning_graph.twin_id!r} does not match Twin "
                f"{twin.twin_id!r}"
            )

        builder = CandidateBuilder(
            context=context,
            twin=twin,
            learning_graph=learning_graph,
            created_at=when,
        )

        candidates: list[MissionCandidateProjection] = []
        skipped_decision_ids: list[str] = []

        for decision in decision_set.decisions:
            built = builder.build_from_decision(decision)
            if not built:
                skipped_decision_ids.append(decision.decision_id)
                events.append(
                    MissionPlanningSkipped(
                        event_id=(
                            f"ev-skip:{decision.decision_id}:{PLANNING_VERSION}"
                        ),
                        twin_id=twin.twin_id,
                        decision_id=decision.decision_id,
                        reason_code="non_plannable_decision",
                        occurred_at=when,
                        planning_version=PLANNING_VERSION,
                    )
                )
                continue

            for cand in built:
                if cand.candidate_id in existing_candidates:
                    if allow_idempotent_skip:
                        events.append(
                            MissionPlanningSkipped(
                                event_id=(
                                    f"ev-skip:{cand.candidate_id}:{PLANNING_VERSION}"
                                ),
                                twin_id=twin.twin_id,
                                decision_id=decision.decision_id,
                                reason_code="duplicate_candidate",
                                occurred_at=when,
                                planning_version=PLANNING_VERSION,
                                candidate_id=cand.candidate_id,
                            )
                        )
                        if decision.decision_id not in skipped_decision_ids:
                            skipped_decision_ids.append(decision.decision_id)
                        continue
                    from app.domain.mission.planning.errors import (
                        DuplicateMissionRequest,
                    )

                    raise DuplicateMissionRequest(
                        f"candidate already planned: {cand.candidate_id!r}"
                    )
                candidates.append(cand)

        ranked = tuple(
            sorted(
                candidates,
                key=lambda c: (-c.priority_score, c.concept_id, c.candidate_id),
            )
        )
        selected = ranked[0] if ranked else None

        batch = PlanningBatch(
            batch_id=(
                f"mpb:{context.reasoning_request_id}:"
                f"{context.evidence_bundle_id}:{context.twin_version}"
            ),
            candidates=ranked,
            context=context,
            planning_version=PLANNING_VERSION,
            skipped_decision_ids=tuple(skipped_decision_ids),
        )

        validator = self._validator or PlanningValidator(
            existing_request_ids=() if allow_idempotent_skip else existing_requests,
            existing_candidate_ids=(
                () if allow_idempotent_skip else existing_candidates
            ),
        )
        validated = validator.validate(batch)

        plan = self._build_plan(
            twin=twin,
            context=context,
            ranked=validated.candidates,
            selected=selected,
            when=when,
            prior_plan_ids=tuple(
                self._persistence.version_history(twin_id=twin.twin_id)
            ),
            decision_set=decision_set,
        )

        if selected is not None:
            events.append(
                MissionGenerated(
                    event_id=f"ev-gen:{plan.plan_id}:{PLANNING_VERSION}",
                    plan_id=plan.plan_id,
                    mission_id=plan.mission_id,
                    twin_id=twin.twin_id,
                    decision_id=selected.decision_id,
                    concept_id=selected.concept_id,
                    occurred_at=when,
                    planning_version=PLANNING_VERSION,
                )
            )
        elif not skipped_decision_ids and not decision_set.decisions:
            events.append(
                MissionPlanningSkipped(
                    event_id=f"ev-skip-empty:{context.mission_request_id}",
                    twin_id=twin.twin_id,
                    decision_id=decision_set.set_id,
                    reason_code="empty_decision_set",
                    occurred_at=when,
                    planning_version=PLANNING_VERSION,
                    plan_id=plan.plan_id,
                )
            )

        events.append(
            self._completed_event(
                twin=twin,
                context=context,
                plan=plan,
                candidate_count=len(validated),
                skipped_count=len(skipped_decision_ids),
                when=when,
            )
        )

        result = PlanningResult(
            context=context,
            batch=validated,
            study_mission_plan=plan,
            planned_at=when,
            events=tuple(events),
        )
        if persist:
            return self._persistence.persist(result)
        return result

    def replay(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        learning_graph: LearningGraph | None = None,
        available_minutes: int = 45,
        curriculum_position: str = "",
        planned_at: datetime | None = None,
    ) -> PlanningResult:
        """Replay planning into a fresh store (determinism / audit)."""
        replay_service = MissionPlanningService(
            persistence=self._persistence.clone_empty(),
            validator=self._validator,
        )
        return replay_service.plan(
            twin,
            decision_set,
            learning_graph=learning_graph,
            available_minutes=available_minutes,
            curriculum_position=curriculum_position,
            planned_at=planned_at,
            persist=True,
            allow_idempotent_skip=True,
        )

    def plan_snapshot(self, *, twin_id: str) -> dict:
        """Deterministic ledger snapshot for identical-Twin identical-Mission checks."""
        return self._persistence.snapshot(twin_id=twin_id)

    @staticmethod
    def _assert_twin_version(twin: StudentDigitalTwin) -> None:
        if twin is None:
            from app.domain.mission.planning.errors import MissingLearnerState

            raise MissingLearnerState("Twin is required for mission planning")
        if getattr(twin, "version", 0) < 1:
            from app.domain.mission.planning.errors import UnknownTwinVersion

            raise UnknownTwinVersion(f"unknown twin version: {twin.version!r}")

    def _build_plan(
        self,
        *,
        twin: StudentDigitalTwin,
        context: PlanningContext,
        ranked: tuple[MissionCandidateProjection, ...],
        selected: MissionCandidateProjection | None,
        when: datetime,
        prior_plan_ids: tuple[str, ...],
        decision_set: EducationalDecisionSet,
    ) -> StudyMissionPlan:
        plan_id = (
            f"smp:{context.reasoning_request_id}:"
            f"{context.evidence_bundle_id}:v{context.twin_version}"
        )
        if selected is None:
            return self._empty_plan(
                twin=twin,
                context=context,
                when=when,
                prior_plan_ids=prior_plan_ids,
                validation_summary=(
                    "No plannable Twin decisions — mission generation skipped."
                ),
                plan_id=plan_id,
            )

        mission_id = (
            f"sm:{twin.twin_id}:{selected.concept_id}:"
            f"{context.evidence_bundle_id}:v{context.twin_version}"
        )
        goal = f"Today: strengthen {selected.concept_title}"
        explanation = selected.priority_explanation or (
            "Deterministic priority from Twin decisions and Learning Graph structure."
        )
        return StudyMissionPlan(
            plan_id=plan_id,
            mission_id=mission_id,
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            context=context,
            selected_candidate=selected,
            ranked_candidates=ranked,
            planning_version=PLANNING_VERSION,
            twin_version=twin.version,
            created_at=when,
            goal=goal,
            educational_explanation=explanation,
            concept_ids=tuple(c.concept_id for c in ranked),
            decision_ids=tuple(decision_set.decision_ids),
            prior_plan_ids=prior_plan_ids,
            validation_passed=True,
            validation_summary="Planning validation passed.",
            provenance={
                "decision_set_id": decision_set.set_id,
                "decision_ids": list(decision_set.decision_ids),
                "evidence_bundle_id": context.evidence_bundle_id,
                "reasoning_request_id": context.reasoning_request_id,
                "assessment_session_id": context.session_id,
                "correlation_id": context.correlation_id,
                "twin_version": twin.version,
                "planning_version": PLANNING_VERSION,
                "selected_candidate_id": selected.candidate_id,
                "selected_decision_id": selected.decision_id,
                "available_minutes": context.available_minutes,
                "curriculum_position": context.curriculum_position,
            },
        )

    @staticmethod
    def _empty_plan(
        *,
        twin: StudentDigitalTwin,
        context: PlanningContext,
        when: datetime,
        prior_plan_ids: tuple[str, ...],
        validation_summary: str,
        plan_id: str | None = None,
    ) -> StudyMissionPlan:
        resolved_plan_id = plan_id or (
            f"smp:{context.reasoning_request_id}:"
            f"{context.evidence_bundle_id}:v{context.twin_version}"
        )
        return StudyMissionPlan(
            plan_id=resolved_plan_id,
            mission_id="",
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            context=context,
            selected_candidate=None,
            ranked_candidates=(),
            planning_version=PLANNING_VERSION,
            twin_version=twin.version,
            created_at=when,
            goal="",
            educational_explanation=validation_summary,
            prior_plan_ids=prior_plan_ids,
            validation_passed=True,
            validation_summary=validation_summary,
            provenance={
                "decision_set_id": context.decision_set_id,
                "evidence_bundle_id": context.evidence_bundle_id,
                "reasoning_request_id": context.reasoning_request_id,
                "twin_version": twin.version,
                "planning_version": PLANNING_VERSION,
            },
        )

    @staticmethod
    def _completed_event(
        *,
        twin: StudentDigitalTwin,
        context: PlanningContext,
        plan: StudyMissionPlan,
        candidate_count: int,
        skipped_count: int,
        when: datetime,
    ) -> MissionPlanningCompleted:
        return MissionPlanningCompleted(
            event_id=f"ev-done:{plan.plan_id}:{PLANNING_VERSION}",
            twin_id=twin.twin_id,
            decision_set_id=context.decision_set_id,
            mission_request_id=context.mission_request_id,
            plan_id=plan.plan_id,
            candidate_count=candidate_count,
            skipped_count=skipped_count,
            occurred_at=when,
            planning_version=PLANNING_VERSION,
        )

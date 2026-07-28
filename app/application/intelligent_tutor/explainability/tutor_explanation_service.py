"""TutorExplanationService — explain validated educational provenance.

Pipeline:
  EducationalDecisionSet (+ Twin) (+ optional StudyMissionPlan / Graph)
    → TutorExplanationRequested
    → ExplanationBuilder
    → ExplanationValidator
    → TutorExplanationGenerated / TutorExplanationUnavailable
    → ExplanationPersistenceService
    → STOP

Does not modify Twin belief, Learning Graph, Mission plans, Assessment,
or Reasoning. Never invents missing educational conclusions.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from app.application.intelligent_tutor.explainability.explanation_builder import (
    ExplanationBuilder,
)
from app.application.intelligent_tutor.explainability.persistence import (
    ExplanationPersistenceService,
)
from app.application.intelligent_tutor.explainability.validator import (
    ExplanationValidator,
)
from app.application.intelligent_tutor.explainability.versions import (
    EXPLANATION_VERSION,
    SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION,
)
from app.domain.intelligent_tutor.explainability.context import ExplanationContext
from app.domain.intelligent_tutor.explainability.events import (
    TutorExplanationGenerated,
    TutorExplanationRequested,
    TutorExplanationUnavailable,
)
from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation
from app.domain.intelligent_tutor.explainability.result import (
    ExplanationEvent,
    ExplanationResult,
)
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.mission.planning.plan import StudyMissionPlan
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


class TutorExplanationService:
    """Deterministic Twin / Decision / Mission → Tutor explanation (AP-002D6)."""

    def __init__(
        self,
        *,
        persistence: ExplanationPersistenceService | None = None,
        validator: ExplanationValidator | None = None,
    ) -> None:
        self._persistence = persistence or ExplanationPersistenceService()
        self._validator = validator

    @property
    def persistence(self) -> ExplanationPersistenceService:
        return self._persistence

    def explain(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        study_mission_plan: StudyMissionPlan | None = None,
        learning_graph: LearningGraph | None = None,
        explained_at: datetime | None = None,
        persist: bool = True,
        allow_idempotent_skip: bool = True,
    ) -> ExplanationResult:
        """Generate a fully traceable Tutor explanation.

        Args:
            twin: Authoritative learner Twin after belief update.
            decision_set: Validated educational decisions to narrate.
            study_mission_plan: Optional StudyMissionPlan to explain selection.
            learning_graph: Optional Graph for structural concept relationships.
            explained_at: Deterministic timestamp for replay.
            persist: Persist into the explanation ledger when True.
            allow_idempotent_skip: When True, duplicate request ids emit
                TutorExplanationUnavailable instead of raising.

        Returns:
            ExplanationResult with TutorExplanation and factual events.
        """
        self._assert_inputs(twin, decision_set, study_mission_plan, learning_graph)
        when = explained_at or datetime.now(UTC).replace(tzinfo=None)
        context = self._build_context(twin, decision_set, study_mission_plan)

        events: list[ExplanationEvent] = [
            TutorExplanationRequested(
                event_id=(
                    f"ev-xreq:{context.explanation_request_id}:{EXPLANATION_VERSION}"
                ),
                twin_id=twin.twin_id,
                decision_set_id=decision_set.set_id,
                explanation_request_id=context.explanation_request_id,
                occurred_at=when,
                explanation_version=EXPLANATION_VERSION,
            )
        ]

        existing_requests = self._persistence.existing_request_ids(
            twin_id=twin.twin_id
        )
        if context.explanation_request_id in existing_requests:
            if not allow_idempotent_skip:
                from app.domain.intelligent_tutor.explainability.errors import (
                    DuplicateExplanationRequest,
                )

                raise DuplicateExplanationRequest(
                    f"duplicate explanation request: "
                    f"{context.explanation_request_id!r}"
                )
            unavailable = self._duplicate_unavailable(
                twin=twin, context=context, decision_set=decision_set, when=when
            )
            events.append(
                TutorExplanationUnavailable(
                    event_id=(
                        f"ev-xunavail-dup:{context.explanation_request_id}:"
                        f"{EXPLANATION_VERSION}"
                    ),
                    twin_id=twin.twin_id,
                    decision_set_id=decision_set.set_id,
                    reason_code="duplicate_explanation_request",
                    occurred_at=when,
                    explanation_version=EXPLANATION_VERSION,
                    explanation_id=unavailable.explanation_id,
                    explanation_request_id=context.explanation_request_id,
                )
            )
            result = ExplanationResult(
                context=context,
                explanation=unavailable,
                explained_at=when,
                events=tuple(events),
            )
            return result if not persist else self._persistence.persist(result)

        builder = ExplanationBuilder(
            context=context,
            twin=twin,
            decision_set=decision_set,
            study_mission_plan=study_mission_plan,
            learning_graph=learning_graph,
            created_at=when,
        )
        built = builder.build()

        validator = self._validator or ExplanationValidator(
            existing_request_ids=() if allow_idempotent_skip else existing_requests,
            expected_twin_version=twin.version,
            expected_planning_version=(
                study_mission_plan.planning_version if study_mission_plan else None
            ),
        )

        if built.available:
            validated = validator.validate(built)
            validated = replace(
                validated,
                validation_summary="Explanation validation passed.",
            )
            events.append(
                TutorExplanationGenerated(
                    event_id=(
                        f"ev-xgen:{validated.explanation_id}:{EXPLANATION_VERSION}"
                    ),
                    explanation_id=validated.explanation_id,
                    twin_id=twin.twin_id,
                    decision_set_id=decision_set.set_id,
                    section_count=len(validated),
                    occurred_at=when,
                    explanation_version=EXPLANATION_VERSION,
                    mission_plan_id=validated.mission_plan_id,
                )
            )
            explanation = validated
        else:
            # Unavailable explanations skip section provenance validation but
            # still require supported contract / twin version.
            if built.explanation_version != EXPLANATION_VERSION:
                from app.domain.intelligent_tutor.explainability.errors import (
                    UnsupportedExplanationContract,
                )

                raise UnsupportedExplanationContract(
                    f"unsupported explanation version: {built.explanation_version!r}"
                )
            events.append(
                TutorExplanationUnavailable(
                    event_id=(
                        f"ev-xunavail:{built.explanation_id}:{EXPLANATION_VERSION}"
                    ),
                    twin_id=twin.twin_id,
                    decision_set_id=decision_set.set_id,
                    reason_code=str(
                        built.provenance.get("reason_code", "insufficient_provenance")
                    ),
                    occurred_at=when,
                    explanation_version=EXPLANATION_VERSION,
                    explanation_id=built.explanation_id,
                    explanation_request_id=context.explanation_request_id,
                )
            )
            explanation = built

        result = ExplanationResult(
            context=context,
            explanation=explanation,
            explained_at=when,
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
        study_mission_plan: StudyMissionPlan | None = None,
        learning_graph: LearningGraph | None = None,
        explained_at: datetime | None = None,
    ) -> ExplanationResult:
        """Replay explanation into a fresh store (determinism / audit)."""
        replay_service = TutorExplanationService(
            persistence=self._persistence.clone_empty(),
            validator=self._validator,
        )
        return replay_service.explain(
            twin,
            decision_set,
            study_mission_plan=study_mission_plan,
            learning_graph=learning_graph,
            explained_at=explained_at,
            persist=True,
            allow_idempotent_skip=True,
        )

    def explanation_snapshot(self, *, twin_id: str) -> dict:
        """Deterministic ledger snapshot for identical-input checks."""
        return self._persistence.snapshot(twin_id=twin_id)

    @staticmethod
    def _assert_inputs(
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        study_mission_plan: StudyMissionPlan | None,
        learning_graph: LearningGraph | None,
    ) -> None:
        if twin is None:
            from app.domain.intelligent_tutor.explainability.errors import (
                MissingExplanationInput,
            )

            raise MissingExplanationInput("Twin is required for Tutor explanation")
        if getattr(twin, "version", 0) < 1:
            from app.domain.intelligent_tutor.explainability.errors import (
                UnknownTwinVersion,
            )

            raise UnknownTwinVersion(f"unknown twin version: {twin.version!r}")
        if decision_set is None:
            from app.domain.intelligent_tutor.explainability.errors import (
                MissingExplanationInput,
            )

            raise MissingExplanationInput("EducationalDecisionSet is required")
        if decision_set.context.twin_id != twin.twin_id:
            from app.domain.intelligent_tutor.explainability.errors import (
                ExplanationRejected,
            )

            raise ExplanationRejected(
                f"decision set twin_id {decision_set.context.twin_id!r} does not "
                f"match Twin {twin.twin_id!r}"
            )
        if study_mission_plan is not None:
            if study_mission_plan.twin_id != twin.twin_id:
                from app.domain.intelligent_tutor.explainability.errors import (
                    ExplanationRejected,
                )

                raise ExplanationRejected(
                    f"mission plan twin_id {study_mission_plan.twin_id!r} does not "
                    f"match Twin {twin.twin_id!r}"
                )
            if study_mission_plan.twin_version != twin.version:
                from app.domain.intelligent_tutor.explainability.errors import (
                    TwinVersionMismatch,
                )

                raise TwinVersionMismatch(
                    f"mission plan twin_version {study_mission_plan.twin_version} "
                    f"does not match Twin {twin.version}"
                )
            if (
                study_mission_plan.planning_version
                not in SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION
            ):
                from app.domain.intelligent_tutor.explainability.errors import (
                    MissionVersionMismatch,
                )

                raise MissionVersionMismatch(
                    f"unsupported mission planning version: "
                    f"{study_mission_plan.planning_version!r}"
                )
        if learning_graph is not None and learning_graph.twin_id != twin.twin_id:
            from app.domain.intelligent_tutor.explainability.errors import (
                ExplanationRejected,
            )

            raise ExplanationRejected(
                f"graph twin_id {learning_graph.twin_id!r} does not match Twin "
                f"{twin.twin_id!r}"
            )

    @staticmethod
    def _build_context(
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        study_mission_plan: StudyMissionPlan | None,
    ) -> ExplanationContext:
        plan_id = study_mission_plan.plan_id if study_mission_plan else ""
        mission_id = study_mission_plan.mission_id if study_mission_plan else ""
        planning_version = (
            study_mission_plan.planning_version if study_mission_plan else ""
        )
        return ExplanationContext(
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            reasoning_request_id=decision_set.context.reasoning_request_id,
            evidence_bundle_id=decision_set.context.evidence_bundle_id,
            session_id=decision_set.context.session_id,
            correlation_id=decision_set.context.correlation_id,
            explanation_version=EXPLANATION_VERSION,
            decision_version=decision_set.decision_version,
            twin_version=twin.version,
            decision_set_id=decision_set.set_id,
            mission_plan_id=plan_id,
            mission_id=mission_id,
            planning_version=planning_version,
        )

    @staticmethod
    def _duplicate_unavailable(
        *,
        twin: StudentDigitalTwin,
        context: ExplanationContext,
        decision_set: EducationalDecisionSet,
        when: datetime,
    ) -> TutorExplanation:
        summary = (
            "Duplicate explanation request — narration skipped. "
            "No new educational claim was fabricated."
        )
        return TutorExplanation(
            explanation_id=(
                f"tex-dup:{context.explanation_request_id}:{EXPLANATION_VERSION}"
            ),
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            context=context,
            sections=(),
            explanation_version=EXPLANATION_VERSION,
            twin_version=twin.version,
            created_at=when,
            summary=summary,
            decision_ids=tuple(decision_set.decision_ids),
            mission_plan_id=context.mission_plan_id,
            mission_id=context.mission_id,
            uncertainty_notes=("duplicate_explanation_request",),
            validation_passed=True,
            validation_summary=summary,
            available=False,
            provenance={
                "decision_set_id": decision_set.set_id,
                "reason_code": "duplicate_explanation_request",
                "explanation_version": EXPLANATION_VERSION,
                "twin_version": twin.version,
            },
        )

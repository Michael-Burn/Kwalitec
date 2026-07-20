"""ExplanationBuilder — deterministic EducationalExplanation from Educational OS.

Architecture Source
    EDU-005 Educational Explainability Engine
    EDUCATIONAL_EXPLAINABILITY_STANDARD.md (EIP-003)
Concept
    Explanation Builder

Rules
    No AI. No prompting. No randomness.
    No persistence. No wall-clock dependence.
    Same Educational OS outputs always yield the same EducationalExplanation.
    Educational decisions are narrated, never modified.
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability.decision_trace import DecisionTrace, TraceStep
from domain.explainability.educational_explanation import EducationalExplanation
from domain.explainability.enums import (
    DecisionStage,
    EvidenceSourceKind,
    ExplanationSectionKind,
)
from domain.explainability.evidence_reference import EvidenceReference
from domain.explainability.explanation_section import ExplanationSection
from domain.explainability.ids import (
    DecisionTraceId,
    EducationalExplanationId,
    EvidenceReferenceId,
    ExplanationSectionId,
)
from domain.mission_generation.mission_specification import MissionSpecification
from domain.progress_evaluation.progress_report import ProgressReport
from domain.recommendation.enums import RecommendationCategory
from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from domain.study_planning.study_plan import StudyPlan

_CATEGORY_NEXT_LABEL: dict[RecommendationCategory, str] = {
    RecommendationCategory.CONTINUE_MISSION: (
        "Continue the current mission sitting"
    ),
    RecommendationCategory.REVIEW_PREVIOUS_TOPIC: (
        "Review the previous topic before advancing"
    ),
    RecommendationCategory.INCREASE_DIFFICULTY: (
        "Increase instructional challenge carefully"
    ),
    RecommendationCategory.REDUCE_COGNITIVE_LOAD: (
        "Reduce cognitive load to stabilise understanding"
    ),
    RecommendationCategory.REPEAT_ASSESSMENT: (
        "Repeat assessment to calibrate confidence"
    ),
    RecommendationCategory.SCHEDULE_REVISION: (
        "Schedule spaced revision for retention"
    ),
    RecommendationCategory.REVISIT_PREREQUISITES: (
        "Revisit prerequisites blocking progress"
    ),
    RecommendationCategory.PAUSE_FOR_CONSOLIDATION: (
        "Pause advancement to consolidate recent learning"
    ),
}

_SECTION_TITLES: dict[ExplanationSectionKind, str] = {
    ExplanationSectionKind.OBSERVED_FACTS: "What we know",
    ExplanationSectionKind.ESTIMATES: "What we estimate",
    ExplanationSectionKind.WHY: "Why this guidance",
    ExplanationSectionKind.NEXT_ACTION: "What to do next",
}


class ExplanationBuilder:
    """Pure domain service that builds EducationalExplanation projections.

    Building is fully deterministic and educational. Decisions remain owned by
    Educational OS engines. This builder narrates authorised state into the
    four-question explainability contract — it never invents mastery or
    mutates recommendations.
    """

    @classmethod
    def build(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> EducationalExplanation:
        """Build an EducationalExplanation from Educational OS outputs.

        Args:
            mission: Current MissionSpecification being explained.
            study_plan: Active StudyPlan providing schedule context.
            progress: ProgressReport with trends and intervention signals.
            recommendations: RecommendationSpecification whose primary decision
                is explained.

        Returns:
            Immutable EducationalExplanation with sections, decision trace,
            and evidence references.

        Raises:
            EducationalInvariantViolation: When inputs are inconsistent.
        """
        cls._assert_inputs(mission, study_plan, progress, recommendations)

        evidence = cls._build_evidence(
            mission, study_plan, progress, recommendations
        )
        sections = cls._build_sections(
            mission=mission,
            study_plan=study_plan,
            progress=progress,
            recommendations=recommendations,
            evidence=evidence,
        )
        decision_trace = cls._build_decision_trace(
            mission, study_plan, progress, recommendations
        )
        explanation_id = cls._explanation_id(
            mission, study_plan, progress, recommendations
        )
        summary = cls._build_summary(mission, recommendations)

        return EducationalExplanation(
            explanation_id=explanation_id,
            student_id=mission.student_id,
            sections=sections,
            decision_trace=decision_trace,
            evidence_references=evidence,
            summary=summary,
            mission_id=mission.mission_id,
            plan_id=study_plan.plan_id,
            progress_report_id=progress.report_id,
            recommendation_specification_id=recommendations.specification_id,
        )

    # --- validation ---------------------------------------------------------

    @staticmethod
    def _assert_inputs(
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> None:
        if not isinstance(mission, MissionSpecification):
            raise EducationalInvariantViolation(
                "mission must be a MissionSpecification",
                invariant="ExplanationBuilder.mission.type",
            )
        if not isinstance(study_plan, StudyPlan):
            raise EducationalInvariantViolation(
                "study_plan must be a StudyPlan",
                invariant="ExplanationBuilder.study_plan.type",
            )
        if not isinstance(progress, ProgressReport):
            raise EducationalInvariantViolation(
                "progress must be a ProgressReport",
                invariant="ExplanationBuilder.progress.type",
            )
        if not isinstance(recommendations, RecommendationSpecification):
            raise EducationalInvariantViolation(
                "recommendations must be a RecommendationSpecification",
                invariant="ExplanationBuilder.recommendations.type",
            )
        student_id = mission.student_id
        for name, value in (
            ("study_plan", study_plan.student_id),
            ("progress", progress.student_id),
            ("recommendations", recommendations.student_id),
        ):
            if value != student_id:
                raise EducationalInvariantViolation(
                    f"{name} student_id must match mission student_id",
                    invariant="ExplanationBuilder.student_id.align",
                )
        if recommendations.mission_id != mission.mission_id:
            raise EducationalInvariantViolation(
                "recommendations.mission_id must match mission.mission_id",
                invariant="ExplanationBuilder.mission_id.align",
            )
        if recommendations.plan_id != study_plan.plan_id:
            raise EducationalInvariantViolation(
                "recommendations.plan_id must match study_plan.plan_id",
                invariant="ExplanationBuilder.plan_id.align",
            )
        if recommendations.progress_report_id != progress.report_id:
            raise EducationalInvariantViolation(
                "recommendations.progress_report_id must match progress.report_id",
                invariant="ExplanationBuilder.progress_report_id.align",
            )
        if mission.mission_id not in study_plan.mission_ids:
            raise EducationalInvariantViolation(
                "mission must belong to study_plan.mission_ids",
                invariant="ExplanationBuilder.mission.in_plan",
            )
        if study_plan.plan_id not in progress.plan_ids:
            raise EducationalInvariantViolation(
                "progress report must reference the provided study plan",
                invariant="ExplanationBuilder.progress.plan_link",
            )

    # --- evidence -----------------------------------------------------------

    @classmethod
    def _build_evidence(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> tuple[EvidenceReference, ...]:
        primary = recommendations.primary
        refs: list[EvidenceReference] = [
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{mission.mission_id.value}-mission"
                ),
                source_kind=EvidenceSourceKind.MISSION,
                source_id=mission.mission_id.value,
                statement=(
                    f"Mission objective: {mission.objective.statement}"
                ),
                sequence=1,
                code="mission_objective",
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{study_plan.plan_id.value}-plan"
                ),
                source_kind=EvidenceSourceKind.STUDY_PLAN,
                source_id=study_plan.plan_id.value,
                statement=(
                    "Study plan schedules "
                    f"{study_plan.estimated_completion.session_count} "
                    "session(s) across "
                    f"{len(study_plan.mission_ids)} mission(s)."
                ),
                sequence=2,
                code="study_plan_schedule",
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{progress.report_id.value}-progress"
                ),
                source_kind=EvidenceSourceKind.PROGRESS,
                source_id=progress.report_id.value,
                statement=(
                    f"Progress shows mastery trend "
                    f"{progress.mastery_trend.direction.value} and stability "
                    f"{progress.knowledge_stability.value}."
                ),
                sequence=3,
                code="progress_trends",
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{primary.recommendation_id.value}-recommendation"
                ),
                source_kind=EvidenceSourceKind.RECOMMENDATION,
                source_id=primary.recommendation_id.value,
                statement=primary.reason.statement,
                sequence=4,
                code=primary.reason.code.value,
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{mission.twin_id.value}-twin"
                ),
                source_kind=EvidenceSourceKind.TWIN,
                source_id=mission.twin_id.value,
                statement=(
                    "Digital Twin identity anchors mission and recommendation "
                    "lineage for this explanation."
                ),
                sequence=5,
                code="twin_lineage",
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{mission.diagnosis_id.value}-diagnosis"
                ),
                source_kind=EvidenceSourceKind.DIAGNOSIS,
                source_id=mission.diagnosis_id.value,
                statement=(
                    f"Mission diagnosis type "
                    f"{mission.objective.diagnosis_type.value} shaped the "
                    "educational aim of this sitting."
                ),
                sequence=6,
                code="diagnosis_type",
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{mission.priority_id.value}-priority"
                ),
                source_kind=EvidenceSourceKind.PRIORITY,
                source_id=mission.priority_id.value,
                statement=(
                    "Educational priority lineage is preserved from mission "
                    "through recommendation."
                ),
                sequence=7,
                code="priority_lineage",
            ),
            EvidenceReference(
                reference_id=EvidenceReferenceId(
                    f"eref-{mission.strategy_id.value}-strategy"
                ),
                source_kind=EvidenceSourceKind.STRATEGY,
                source_id=mission.strategy_id.value,
                statement=(
                    f"Teaching strategy "
                    f"{mission.objective.primary_strategy.value} informs "
                    "how the mission pursues its educational aim."
                ),
                sequence=8,
                code="strategy_type",
            ),
        ]
        return tuple(refs)

    # --- sections -----------------------------------------------------------

    @classmethod
    def _build_sections(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
        evidence: tuple[EvidenceReference, ...],
    ) -> tuple[ExplanationSection, ...]:
        by_kind = {item.source_kind: item for item in evidence}
        primary = recommendations.primary
        next_label = _CATEGORY_NEXT_LABEL[primary.category]

        observed_body = (
            f"Today's mission focuses on: {mission.objective.statement}. "
            f"Planned sitting length is {mission.duration.planned_minutes} "
            f"minute(s). The study plan includes "
            f"{study_plan.estimated_completion.session_count} session(s) for "
            f"{len(study_plan.mission_ids)} mission(s). "
            f"{len(progress.mission_ids)} completed mission(s) appear in the "
            "progress report."
        )
        estimates_body = (
            f"Estimated mastery trend: {progress.mastery_trend.direction.value}. "
            f"Estimated confidence trend: "
            f"{progress.confidence_trend.direction.value}. "
            f"Estimated knowledge stability: "
            f"{progress.knowledge_stability.value}. "
            f"Estimated learning velocity: {progress.learning_velocity.band.value}. "
            f"Estimated revision effectiveness: "
            f"{progress.revision_effectiveness.band.value}. "
            "These are estimates — not validated mastery claims."
        )
        why_body = (
            f"{primary.reason.statement} "
            f"Mission rationale: {mission.educational_rationale} "
            f"Progress explanation: {progress.educational_explanation}"
        )
        next_body = (
            f"{next_label}. Expected outcome: {primary.expected_outcome} "
            "This guidance is educational advice — it does not replace "
            "Today's Mission authority."
        )

        sections = (
            ExplanationSection(
                section_id=ExplanationSectionId(
                    f"sec-{mission.mission_id.value}-observed"
                ),
                kind=ExplanationSectionKind.OBSERVED_FACTS,
                title=_SECTION_TITLES[ExplanationSectionKind.OBSERVED_FACTS],
                body=observed_body,
                sequence=1,
                evidence_reference_ids=(
                    by_kind[EvidenceSourceKind.MISSION].reference_id,
                    by_kind[EvidenceSourceKind.STUDY_PLAN].reference_id,
                    by_kind[EvidenceSourceKind.PROGRESS].reference_id,
                ),
            ),
            ExplanationSection(
                section_id=ExplanationSectionId(
                    f"sec-{mission.mission_id.value}-estimates"
                ),
                kind=ExplanationSectionKind.ESTIMATES,
                title=_SECTION_TITLES[ExplanationSectionKind.ESTIMATES],
                body=estimates_body,
                sequence=2,
                evidence_reference_ids=(
                    by_kind[EvidenceSourceKind.PROGRESS].reference_id,
                    by_kind[EvidenceSourceKind.TWIN].reference_id,
                ),
            ),
            ExplanationSection(
                section_id=ExplanationSectionId(
                    f"sec-{mission.mission_id.value}-why"
                ),
                kind=ExplanationSectionKind.WHY,
                title=_SECTION_TITLES[ExplanationSectionKind.WHY],
                body=why_body,
                sequence=3,
                evidence_reference_ids=(
                    by_kind[EvidenceSourceKind.RECOMMENDATION].reference_id,
                    by_kind[EvidenceSourceKind.DIAGNOSIS].reference_id,
                    by_kind[EvidenceSourceKind.STRATEGY].reference_id,
                    by_kind[EvidenceSourceKind.PRIORITY].reference_id,
                ),
            ),
            ExplanationSection(
                section_id=ExplanationSectionId(
                    f"sec-{mission.mission_id.value}-next"
                ),
                kind=ExplanationSectionKind.NEXT_ACTION,
                title=_SECTION_TITLES[ExplanationSectionKind.NEXT_ACTION],
                body=next_body,
                sequence=4,
                evidence_reference_ids=(
                    by_kind[EvidenceSourceKind.RECOMMENDATION].reference_id,
                    by_kind[EvidenceSourceKind.MISSION].reference_id,
                ),
            ),
        )
        return sections

    # --- decision trace -----------------------------------------------------

    @classmethod
    def _build_decision_trace(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> DecisionTrace:
        primary = recommendations.primary
        steps = (
            TraceStep(
                stage=DecisionStage.MISSION,
                source_id=mission.mission_id.value,
                summary=(
                    f"Mission generated for objective: "
                    f"{mission.objective.statement}"
                ),
                sequence=1,
                reason_codes=(
                    mission.objective.diagnosis_type.value,
                    mission.objective.primary_strategy.value,
                ),
            ),
            TraceStep(
                stage=DecisionStage.STUDY_PLAN,
                source_id=study_plan.plan_id.value,
                summary=(
                    f"Study plan scheduled "
                    f"{study_plan.estimated_completion.session_count} "
                    f"session(s) with "
                    f"{len(study_plan.review_windows)} review window(s)."
                ),
                sequence=2,
                reason_codes=(study_plan.priority_id.value,),
            ),
            TraceStep(
                stage=DecisionStage.PROGRESS,
                source_id=progress.report_id.value,
                summary=(
                    f"Progress evaluated with mastery "
                    f"{progress.mastery_trend.direction.value} and "
                    f"intervention required="
                    f"{str(progress.intervention_signal.required).lower()}."
                ),
                sequence=3,
                reason_codes=(
                    progress.mastery_trend.direction.value,
                    progress.knowledge_stability.value,
                    progress.intervention_signal.urgency.value,
                ),
            ),
            TraceStep(
                stage=DecisionStage.RECOMMENDATION,
                source_id=primary.recommendation_id.value,
                summary=(
                    f"Primary recommendation selected: "
                    f"{primary.category.value} "
                    f"({primary.priority.band.value} priority)."
                ),
                sequence=4,
                reason_codes=(
                    primary.reason.code.value,
                    primary.category.value,
                    *(item.code.value for item in primary.supporting_evidence),
                ),
            ),
        )
        chain_summary = (
            f"Decision chain for student {mission.student_id}: "
            f"mission → study plan → progress → recommendation "
            f"({primary.category.value})."
        )
        return DecisionTrace(
            trace_id=DecisionTraceId(
                f"trace-{mission.mission_id.value}"
                f"-{recommendations.specification_id.value}"
            ),
            steps=steps,
            primary_decision=primary.category.value,
            chain_summary=chain_summary,
        )

    # --- summary / identity -------------------------------------------------

    @staticmethod
    def _explanation_id(
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> EducationalExplanationId:
        return EducationalExplanationId(
            f"expl-{mission.mission_id.value}-{study_plan.plan_id.value}"
            f"-{progress.report_id.value}"
            f"-{recommendations.specification_id.value}"
        )

    @staticmethod
    def _build_summary(
        mission: MissionSpecification,
        recommendations: RecommendationSpecification,
    ) -> str:
        primary = recommendations.primary
        next_label = _CATEGORY_NEXT_LABEL[primary.category]
        return (
            f"Educational explanation for student {mission.student_id}: "
            f"mission {mission.mission_id.value} leads to "
            f"{primary.category.value} — {next_label}."
        )

"""ExplanationBuilder — narrate validated educational provenance only.

Never reasons. Never predicts. Never estimates mastery independently.
Never consumes assessment responses, evidence bundles, or observations as
authority — only validated Decision / Twin / Mission / Graph identifiers.
"""

from __future__ import annotations

from datetime import datetime

from app.application.intelligent_tutor.explainability.versions import (
    EXPLANATION_PROVENANCE_PREFIX,
    EXPLANATION_VERSION,
)
from app.domain.intelligent_tutor.explainability.context import ExplanationContext
from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation
from app.domain.intelligent_tutor.explainability.reference import ExplanationReference
from app.domain.intelligent_tutor.explainability.section import (
    ConceptExplanation,
    DecisionExplanation,
    EvidenceExplanation,
    ExplanationSection,
    ExplanationSectionKind,
    LearningObjectiveExplanation,
    MissionExplanation,
)
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.mission.planning.plan import StudyMissionPlan
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin

_SOFT_CATEGORIES = frozenset(
    {
        DecisionCategory.UNCERTAINTY_PRESERVED,
        DecisionCategory.PROVENANCE_RECORDED,
    }
)


class ExplanationBuilder:
    """Build deterministic TutorExplanation sections from validated inputs."""

    def __init__(
        self,
        *,
        context: ExplanationContext,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        study_mission_plan: StudyMissionPlan | None = None,
        learning_graph: LearningGraph | None = None,
        created_at: datetime,
    ) -> None:
        self._context = context
        self._twin = twin
        self._decision_set = decision_set
        self._plan = study_mission_plan
        self._graph = learning_graph
        self._created_at = created_at

    def build(self) -> TutorExplanation:
        """Assemble a fully traceable TutorExplanation (or unavailable shell)."""
        sections: list[ExplanationSection] = []
        uncertainty_notes: list[str] = []
        concept_ids: list[str] = []
        lo_ids: list[str] = []
        decision_ids = list(self._decision_set.decision_ids)

        if not self._decision_set.decisions:
            uncertainty_notes.append(
                "No validated educational decisions were available to explain."
            )
            return self._unavailable(
                reason="empty_decision_set",
                uncertainty_notes=tuple(uncertainty_notes),
            )

        # Prefer an actionable decision as the primary provenance anchor.
        primary = self._primary_decision()
        if primary is None:
            uncertainty_notes.append(
                "Only soft decisions were present; educational conclusions remain "
                "uncertain and are not restated as mastery."
            )
            soft = self._decision_set.decisions[0]
            sections.append(self._decision_section(soft, index=0))
            sections.append(self._evidence_section(soft, index=0))
            sections.append(
                self._uncertainty_section(
                    soft,
                    notes=tuple(uncertainty_notes),
                    index=0,
                )
            )
            return self._assemble(
                sections=tuple(sections),
                summary=(
                    "Evidence was recorded, but no firm educational conclusion is "
                    "available to explain yet."
                ),
                decision_ids=decision_ids,
                concept_ids=(),
                learning_objective_ids=(),
                uncertainty_notes=tuple(uncertainty_notes),
                available=True,
            )

        sections.append(self._decision_section(primary, index=0))
        sections.append(self._evidence_section(primary, index=0))

        concept = self._concept_id(primary)
        if concept:
            related = self._related_concepts(concept)
            sections.append(
                self._concept_section(
                    primary, concept_id=concept, related=related, index=0
                )
            )
            concept_ids.append(concept)
            concept_ids.extend(c for c in related if c not in concept_ids)

        lo = self._learning_objective_id(primary)
        if lo:
            sections.append(self._lo_section(primary, lo_id=lo, index=0))
            lo_ids.append(lo)

        if self._plan is not None and (self._plan.mission_id or "").strip():
            sections.append(self._mission_section(primary, index=0))
            for cid in self._plan.concept_ids:
                if cid and cid not in concept_ids:
                    concept_ids.append(cid)

        for index, decision in enumerate(self._decision_set.decisions):
            if decision.decision_id == primary.decision_id:
                continue
            if decision.category in _SOFT_CATEGORIES:
                note = (
                    f"Decision {decision.decision_id} preserved uncertainty "
                    f"({decision.category.value}); no mastery claim is made."
                )
                uncertainty_notes.append(note)
                sections.append(
                    self._uncertainty_section(decision, notes=(note,), index=index)
                )
            else:
                sections.append(self._decision_section(decision, index=index))
                cid = self._concept_id(decision)
                if cid and cid not in concept_ids:
                    concept_ids.append(cid)

        if not uncertainty_notes and any(
            d.category in _SOFT_CATEGORIES for d in self._decision_set.decisions
        ):
            uncertainty_notes.append(
                "Some decisions preserved uncertainty; explanations under-claim "
                "rather than invent confidence."
            )

        summary = self._summary(primary=primary, concept_ids=tuple(concept_ids))
        return self._assemble(
            sections=tuple(sections),
            summary=summary,
            decision_ids=decision_ids,
            concept_ids=tuple(concept_ids),
            learning_objective_ids=tuple(lo_ids),
            uncertainty_notes=tuple(uncertainty_notes),
            available=True,
        )

    def _primary_decision(self) -> EducationalDecision | None:
        plan_decision_ids = set(self._plan.decision_ids) if self._plan else set()
        if self._plan and self._plan.selected_candidate is not None:
            selected_id = self._plan.selected_candidate.decision_id
            for decision in self._decision_set.decisions:
                if decision.decision_id == selected_id:
                    return decision
        for decision in self._decision_set.decisions:
            if decision.category not in _SOFT_CATEGORIES:
                if not plan_decision_ids or decision.decision_id in plan_decision_ids:
                    return decision
        for decision in self._decision_set.decisions:
            if decision.category not in _SOFT_CATEGORIES:
                return decision
        return None

    def _summary(
        self,
        *,
        primary: EducationalDecision,
        concept_ids: tuple[str, ...],
    ) -> str:
        concept = concept_ids[0] if concept_ids else self._concept_id(primary)
        if self._plan is not None and self._plan.goal:
            base = (
                f"Today's mission was selected from validated Twin decisions"
                f"{f' involving {concept}' if concept else ''}."
            )
            if self._plan.educational_explanation:
                return f"{base} {self._plan.educational_explanation}"
            return base
        reason = (primary.reason.summary or "").strip()
        if reason and concept:
            return f"{reason} (concept {concept})."
        if reason:
            return reason
        if concept:
            return (
                f"This explanation is grounded in validated educational decisions "
                f"for {concept}."
            )
        return (
            "This explanation is grounded in validated educational decisions "
            "and approved provenance."
        )

    def _decision_section(
        self, decision: EducationalDecision, *, index: int
    ) -> DecisionExplanation:
        ref = self._reference(decision, section_suffix=f"decision-{index}")
        body = (
            f"Decision {decision.decision_id} "
            f"({decision.category.value}): {decision.reason.summary}. "
            f"This statement narrates a validated educational decision; "
            f"it does not re-score mastery or invent a new recommendation."
        )
        return DecisionExplanation(
            section_id=f"sec-decision:{decision.decision_id}",
            kind=ExplanationSectionKind.DECISION,
            title="Educational decision",
            body=body,
            reference=ref,
            concept_ids=tuple(
                c for c in (self._concept_id(decision),) if c
            ),
            learning_objective_ids=tuple(
                lo for lo in (self._learning_objective_id(decision),) if lo
            ),
            decision_ids=(decision.decision_id,),
            decision_category=decision.category.value,
            decision_summary=decision.reason.summary,
            provenance=self._section_provenance(decision, ref),
        )

    def _evidence_section(
        self, decision: EducationalDecision, *, index: int
    ) -> EvidenceExplanation:
        ref = self._reference(decision, section_suffix=f"evidence-{index}")
        obs = ref.educational_observation_ids
        body = (
            f"Evidence bundle {ref.evidence_bundle_id} contributed "
            f"{len(obs)} educational observation id(s) "
            f"({', '.join(obs)}). "
            f"Reasoning request {ref.reasoning_request_id} and correlation "
            f"{ref.correlation_id} anchor this narration. "
            f"Raw assessment responses are not consumed by the Tutor."
        )
        return EvidenceExplanation(
            section_id=f"sec-evidence:{decision.decision_id}",
            kind=ExplanationSectionKind.EVIDENCE,
            title="Evidence contribution",
            body=body,
            reference=ref,
            decision_ids=(decision.decision_id,),
            observation_count=len(obs),
            provenance=self._section_provenance(decision, ref),
        )

    def _concept_section(
        self,
        decision: EducationalDecision,
        *,
        concept_id: str,
        related: tuple[str, ...],
        index: int,
    ) -> ConceptExplanation:
        ref = self._reference(
            decision,
            section_suffix=f"concept-{index}",
            concept=concept_id,
        )
        related_text = (
            f" Related Learning Graph concepts: {', '.join(related)}."
            if related
            else ""
        )
        body = (
            f"Concept {concept_id} influenced this explanation via validated "
            f"Twin decisions.{related_text} "
            f"Graph relationships are structural only — not mastery authority."
        )
        return ConceptExplanation(
            section_id=f"sec-concept:{decision.decision_id}:{concept_id}",
            kind=ExplanationSectionKind.CONCEPT,
            title="Concepts involved",
            body=body,
            reference=ref,
            concept_ids=(concept_id, *related),
            decision_ids=(decision.decision_id,),
            primary_concept_id=concept_id,
            related_concept_ids=related,
            provenance=self._section_provenance(decision, ref),
        )

    def _lo_section(
        self,
        decision: EducationalDecision,
        *,
        lo_id: str,
        index: int,
    ) -> LearningObjectiveExplanation:
        ref = self._reference(
            decision,
            section_suffix=f"lo-{index}",
            learning_objective=lo_id,
        )
        body = (
            f"Learning objective {lo_id} is referenced by decision "
            f"{decision.decision_id}. The Tutor does not invent objectives."
        )
        return LearningObjectiveExplanation(
            section_id=f"sec-lo:{decision.decision_id}:{lo_id}",
            kind=ExplanationSectionKind.LEARNING_OBJECTIVE,
            title="Learning objectives",
            body=body,
            reference=ref,
            learning_objective_ids=(lo_id,),
            decision_ids=(decision.decision_id,),
            primary_learning_objective_id=lo_id,
            provenance=self._section_provenance(decision, ref),
        )

    def _mission_section(
        self, decision: EducationalDecision, *, index: int
    ) -> MissionExplanation:
        assert self._plan is not None
        ref = self._reference(
            decision,
            section_suffix=f"mission-{index}",
            concept=self._concept_id(decision),
            learning_objective=self._learning_objective_id(decision),
        )
        goal = self._plan.goal or self._plan.educational_explanation or "study mission"
        body = (
            f"Mission plan {self._plan.plan_id} "
            f"(mission {self._plan.mission_id}) was selected because validated "
            f"Twin decisions supported: {goal}. "
            f"Planning version {self._plan.planning_version}; "
            f"twin version {self._plan.twin_version}. "
            f"The Tutor does not re-plan or invent mission priority."
        )
        return MissionExplanation(
            section_id=f"sec-mission:{self._plan.plan_id}",
            kind=ExplanationSectionKind.MISSION,
            title="Why this mission",
            body=body,
            reference=ref,
            concept_ids=tuple(self._plan.concept_ids),
            decision_ids=tuple(self._plan.decision_ids or (decision.decision_id,)),
            mission_plan_id=self._plan.plan_id,
            mission_id=self._plan.mission_id,
            mission_goal=self._plan.goal,
            provenance=self._section_provenance(decision, ref),
        )

    def _uncertainty_section(
        self,
        decision: EducationalDecision,
        *,
        notes: tuple[str, ...],
        index: int,
    ) -> ExplanationSection:
        ref = self._reference(decision, section_suffix=f"uncertainty-{index}")
        body = " ".join(notes) if notes else (
            "Provenance is insufficient for a firm educational claim; "
            "uncertainty is stated explicitly rather than fabricated."
        )
        return ExplanationSection(
            section_id=f"sec-uncertainty:{decision.decision_id}:{index}",
            kind=ExplanationSectionKind.UNCERTAINTY,
            title="What remains uncertain",
            body=body,
            reference=ref,
            decision_ids=(decision.decision_id,),
            uncertainty_notes=notes,
            provenance=self._section_provenance(decision, ref),
        )

    def _related_concepts(self, primary: str) -> tuple[str, ...]:
        if self._graph is None or not primary:
            return ()
        related: list[str] = []
        for node in self._graph.nodes:
            cid = getattr(node, "concept_id", "") or ""
            if cid and cid != primary and cid not in related:
                related.append(cid)
            if len(related) >= 4:
                break
        return tuple(related)

    def _reference(
        self,
        decision: EducationalDecision,
        *,
        section_suffix: str,
        concept: str = "",
        learning_objective: str = "",
    ) -> ExplanationReference:
        ref = decision.reference
        return ExplanationReference(
            decision_id=decision.decision_id,
            decision_version=decision.decision_version,
            twin_version=self._context.twin_version,
            evidence_bundle_id=ref.evidence_bundle_id,
            educational_observation_ids=ref.educational_observation_ids,
            reasoning_request_id=ref.reasoning_request_id,
            assessment_session_id=ref.assessment_session_id,
            correlation_id=ref.correlation_id,
            explanation_version=EXPLANATION_VERSION,
            twin_id=self._twin.twin_id,
            learning_objective=learning_objective
            or self._learning_objective_id(decision),
            concept=concept or self._concept_id(decision),
            mission_plan_id=self._context.mission_plan_id,
            mission_id=self._context.mission_id,
            section_id=section_suffix,
        )

    def _section_provenance(
        self, decision: EducationalDecision, ref: ExplanationReference
    ) -> dict:
        return {
            "decision_id": ref.decision_id,
            "decision_version": ref.decision_version,
            "twin_version": ref.twin_version,
            "evidence_bundle_id": ref.evidence_bundle_id,
            "educational_observation_ids": list(ref.educational_observation_ids),
            "reasoning_request_id": ref.reasoning_request_id,
            "assessment_session_id": ref.assessment_session_id,
            "correlation_id": ref.correlation_id,
            "explanation_version": ref.explanation_version,
            "learning_objective": ref.learning_objective,
            "concept": ref.concept,
            "mission_plan_id": ref.mission_plan_id,
            "mission_id": ref.mission_id,
            "provenance_prefix": EXPLANATION_PROVENANCE_PREFIX,
            "decision_category": decision.category.value,
        }

    @staticmethod
    def _concept_id(decision: EducationalDecision) -> str:
        return (
            (decision.reference.concept_reference or "").strip()
            or (decision.subject_ref or "").strip()
        )

    @staticmethod
    def _learning_objective_id(decision: EducationalDecision) -> str:
        return (decision.reference.learning_objective_reference or "").strip()

    def _assemble(
        self,
        *,
        sections: tuple[ExplanationSection, ...],
        summary: str,
        decision_ids: list[str],
        concept_ids: tuple[str, ...],
        learning_objective_ids: tuple[str, ...],
        uncertainty_notes: tuple[str, ...],
        available: bool,
    ) -> TutorExplanation:
        explanation_id = (
            f"tex:{self._context.reasoning_request_id}:"
            f"{self._context.evidence_bundle_id}:v{self._context.twin_version}"
            f":{self._context.mission_plan_id or 'no-plan'}"
        )
        return TutorExplanation(
            explanation_id=explanation_id,
            twin_id=self._twin.twin_id,
            student_id=self._twin.student.student_id,
            context=self._context,
            sections=sections,
            explanation_version=EXPLANATION_VERSION,
            twin_version=self._twin.version,
            created_at=self._created_at,
            summary=summary,
            decision_ids=tuple(decision_ids),
            concept_ids=concept_ids,
            learning_objective_ids=learning_objective_ids,
            mission_plan_id=self._context.mission_plan_id,
            mission_id=self._context.mission_id,
            uncertainty_notes=uncertainty_notes,
            validation_passed=True,
            validation_summary="Explanation validation pending.",
            available=available,
            provenance={
                "decision_set_id": self._decision_set.set_id,
                "decision_ids": list(decision_ids),
                "evidence_bundle_id": self._context.evidence_bundle_id,
                "reasoning_request_id": self._context.reasoning_request_id,
                "assessment_session_id": self._context.session_id,
                "correlation_id": self._context.correlation_id,
                "twin_version": self._twin.version,
                "explanation_version": EXPLANATION_VERSION,
                "mission_plan_id": self._context.mission_plan_id,
                "mission_id": self._context.mission_id,
                "planning_version": self._context.planning_version,
                "provenance_prefix": EXPLANATION_PROVENANCE_PREFIX,
            },
        )

    def _unavailable(
        self,
        *,
        reason: str,
        uncertainty_notes: tuple[str, ...],
    ) -> TutorExplanation:
        explanation_id = (
            f"tex-unavail:{self._context.reasoning_request_id}:"
            f"{self._context.evidence_bundle_id}:v{self._context.twin_version}"
        )
        summary = (
            "A Tutor explanation is unavailable because educational provenance "
            f"is insufficient ({reason}). No claim was fabricated."
        )
        return TutorExplanation(
            explanation_id=explanation_id,
            twin_id=self._twin.twin_id,
            student_id=self._twin.student.student_id,
            context=self._context,
            sections=(),
            explanation_version=EXPLANATION_VERSION,
            twin_version=self._twin.version,
            created_at=self._created_at,
            summary=summary,
            uncertainty_notes=uncertainty_notes,
            validation_passed=True,
            validation_summary=summary,
            available=False,
            mission_plan_id=self._context.mission_plan_id,
            mission_id=self._context.mission_id,
            provenance={
                "decision_set_id": self._decision_set.set_id,
                "evidence_bundle_id": self._context.evidence_bundle_id,
                "reasoning_request_id": self._context.reasoning_request_id,
                "reason_code": reason,
                "twin_version": self._twin.version,
                "explanation_version": EXPLANATION_VERSION,
                "provenance_prefix": EXPLANATION_PROVENANCE_PREFIX,
            },
        )

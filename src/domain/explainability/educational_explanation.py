"""EducationalExplanation — deterministic explanation of educational decisions.

Architecture Source
    EDU-005 Educational Explainability Engine
    EDUCATIONAL_EXPLAINABILITY_STANDARD.md (EIP-003)
Concept
    Educational Explanation
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability.decision_trace import DecisionTrace
from domain.explainability.enums import ExplanationSectionKind
from domain.explainability.evidence_reference import EvidenceReference
from domain.explainability.explanation_section import ExplanationSection
from domain.explainability.ids import EducationalExplanationId
from domain.mission_generation.ids import MissionSpecificationId
from domain.progress_evaluation.ids import ProgressReportId
from domain.recommendation.ids import RecommendationSpecificationId
from domain.study_planning.ids import StudyPlanId

_REQUIRED_SECTION_KINDS = (
    ExplanationSectionKind.OBSERVED_FACTS,
    ExplanationSectionKind.ESTIMATES,
    ExplanationSectionKind.WHY,
    ExplanationSectionKind.NEXT_ACTION,
)


@dataclass(frozen=True, slots=True)
class EducationalExplanation(EducationalValueObject):
    """Fully explainable projection of why educational decisions were made.

    An EducationalExplanation is part of the educational model: ordered
    four-question sections, a decision trace, and evidence references derived
    from MissionSpecification, StudyPlan, ProgressReport, and
    RecommendationSpecification. Pure domain — no AI, persistence, or UI.
    """

    explanation_id: EducationalExplanationId
    student_id: str
    sections: tuple[ExplanationSection, ...]
    decision_trace: DecisionTrace
    evidence_references: tuple[EvidenceReference, ...]
    summary: str
    mission_id: MissionSpecificationId
    plan_id: StudyPlanId
    progress_report_id: ProgressReportId
    recommendation_specification_id: RecommendationSpecificationId

    def _validate(self) -> None:
        if not isinstance(self.explanation_id, EducationalExplanationId):
            raise EducationalInvariantViolation(
                "explanation_id must be an EducationalExplanationId",
                invariant="EducationalExplanation.explanation_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.sections, tuple) or not self.sections:
            raise EducationalInvariantViolation(
                "sections must be a non-empty tuple",
                invariant="EducationalExplanation.sections.min_one",
            )
        seen_section_ids: set[str] = set()
        seen_kinds: set[ExplanationSectionKind] = set()
        expected = 1
        for section in self.sections:
            if not isinstance(section, ExplanationSection):
                raise EducationalInvariantViolation(
                    "sections must contain ExplanationSection values",
                    invariant="EducationalExplanation.sections.item_type",
                )
            if section.section_id.value in seen_section_ids:
                raise EducationalInvariantViolation(
                    "section identities must be unique",
                    invariant="EducationalExplanation.sections.unique",
                )
            seen_section_ids.add(section.section_id.value)
            if section.kind in seen_kinds:
                raise EducationalInvariantViolation(
                    "each ExplanationSectionKind may appear at most once",
                    invariant="EducationalExplanation.sections.unique_kind",
                )
            seen_kinds.add(section.kind)
            if section.sequence != expected:
                raise EducationalInvariantViolation(
                    "section sequences must be contiguous from 1",
                    invariant="EducationalExplanation.sections.contiguous",
                )
            expected += 1
        for kind in _REQUIRED_SECTION_KINDS:
            if kind not in seen_kinds:
                raise EducationalInvariantViolation(
                    f"explanation must include {kind.value} section",
                    invariant="EducationalExplanation.sections.required",
                )
        if not isinstance(self.decision_trace, DecisionTrace):
            raise EducationalInvariantViolation(
                "decision_trace must be a DecisionTrace",
                invariant="EducationalExplanation.decision_trace.type",
            )
        if (
            not isinstance(self.evidence_references, tuple)
            or not self.evidence_references
        ):
            raise EducationalInvariantViolation(
                "evidence_references must be a non-empty tuple",
                invariant="EducationalExplanation.evidence_references.min_one",
            )
        seen_refs: set[str] = set()
        for reference in self.evidence_references:
            if not isinstance(reference, EvidenceReference):
                raise EducationalInvariantViolation(
                    "evidence_references must contain EvidenceReference values",
                    invariant="EducationalExplanation.evidence_references.item_type",
                )
            if reference.reference_id.value in seen_refs:
                raise EducationalInvariantViolation(
                    "evidence reference identities must be unique",
                    invariant="EducationalExplanation.evidence_references.unique",
                )
            seen_refs.add(reference.reference_id.value)
        known_ref_ids = {ref.reference_id for ref in self.evidence_references}
        for section in self.sections:
            for reference_id in section.evidence_reference_ids:
                if reference_id not in known_ref_ids:
                    raise EducationalInvariantViolation(
                        "section evidence_reference_ids must exist on the explanation",
                        invariant="EducationalExplanation.sections.evidence_link",
                    )
        object.__setattr__(
            self,
            "summary",
            require_non_empty_text(self.summary, "summary"),
        )
        if len(self.summary) < 24:
            raise EducationalInvariantViolation(
                "summary must be educationally substantive",
                invariant="EducationalExplanation.summary.substantive",
            )
        for name, value, expected_type in (
            ("mission_id", self.mission_id, MissionSpecificationId),
            ("plan_id", self.plan_id, StudyPlanId),
            ("progress_report_id", self.progress_report_id, ProgressReportId),
            (
                "recommendation_specification_id",
                self.recommendation_specification_id,
                RecommendationSpecificationId,
            ),
        ):
            if not isinstance(value, expected_type):
                raise EducationalInvariantViolation(
                    f"{name} must be a {expected_type.__name__}",
                    invariant=f"EducationalExplanation.{name}.type",
                )

    def section_count(self) -> int:
        return len(self.sections)

    def evidence_count(self) -> int:
        return len(self.evidence_references)

    def section_for(self, kind: ExplanationSectionKind) -> ExplanationSection | None:
        for section in self.sections:
            if section.kind is kind:
                return section
        return None

    def has_section_kind(self, kind: ExplanationSectionKind) -> bool:
        return any(section.kind is kind for section in self.sections)

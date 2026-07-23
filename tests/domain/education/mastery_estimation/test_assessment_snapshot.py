"""Unit tests for AssessmentSnapshot."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.ids import AssessmentId
from domain.education.mastery_estimation.value_objects.assessment_snapshot import (
    AssessmentSnapshot,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.mastery_estimation.value_objects.learning_stability import (
    LearningStability,
)
from domain.education.mastery_estimation.value_objects.mastery_confidence import (
    MasteryConfidence,
)
from domain.education.mastery_estimation.value_objects.mastery_score import (
    MasteryScore,
)

AS_OF = datetime(2026, 7, 21, 12, 0, 0, tzinfo=UTC)


def _minimal_kwargs() -> dict:
    return {
        "assessment_id": AssessmentId("assessment-1"),
        "student_id": "student-001",
        "overall_mastery": MasteryScore.not_assessed(),
        "overall_confidence": MasteryConfidence.zero(),
        "overall_stability": LearningStability.insufficient_data(),
        "subject_assessments": (),
        "knowledge_gaps": (),
        "supporting_evidence": (),
        "reasons": (),
        "assessed_at": AS_OF,
    }


class TestAssessmentSnapshot:
    def test_construction_with_empty_collections(self) -> None:
        snapshot = AssessmentSnapshot(**_minimal_kwargs())
        assert snapshot.subject_count() == 0
        assert snapshot.knowledge_gap_count() == 0
        assert snapshot.weak_prerequisites() == ()

    def test_rejects_blank_student_id(self) -> None:
        kwargs = _minimal_kwargs()
        kwargs["student_id"] = "   "
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**kwargs)

    def test_rejects_wrong_assessment_id_type(self) -> None:
        kwargs = _minimal_kwargs()
        kwargs["assessment_id"] = "not-an-id"
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**kwargs)

    def test_rejects_wrong_knowledge_gap_member_type(self) -> None:
        kwargs = _minimal_kwargs()
        kwargs["knowledge_gaps"] = ("not-a-gap",)
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**kwargs)

    def test_rejects_non_datetime_assessed_at(self) -> None:
        kwargs = _minimal_kwargs()
        kwargs["assessed_at"] = "2026-07-21"
        with pytest.raises(EducationalInvariantViolation):
            AssessmentSnapshot(**kwargs)

    def test_weak_prerequisites_filters_by_kind(self) -> None:
        from domain.education.knowledge_graph.value_objects.dependency_strength import (
            DependencyStrength,
        )
        from domain.education.mastery_estimation.enums import (
            KnowledgeGapKind,
            KnowledgeGapSeverity,
        )
        from domain.education.mastery_estimation.ids import CompetencyId

        prereq_gap = KnowledgeGap(
            competency_id=CompetencyId("prereq"),
            kind=KnowledgeGapKind.WEAK_PREREQUISITE,
            severity=KnowledgeGapSeverity.SEVERE,
            mastery_score=MasteryScore(magnitude=0.1, evidence_count=1),
            related_competency_id=CompetencyId("dependent"),
            dependency_strength=DependencyStrength.critical(),
        )
        direct_gap = KnowledgeGap(
            competency_id=CompetencyId("dependent"),
            kind=KnowledgeGapKind.WEAK_EVIDENCE,
            severity=KnowledgeGapSeverity.MINOR,
            mastery_score=MasteryScore(magnitude=0.4, evidence_count=1),
        )
        kwargs = _minimal_kwargs()
        kwargs["knowledge_gaps"] = (prereq_gap, direct_gap)
        snapshot = AssessmentSnapshot(**kwargs)
        assert snapshot.weak_prerequisites() == (prereq_gap,)
        assert snapshot.knowledge_gap_count() == 2

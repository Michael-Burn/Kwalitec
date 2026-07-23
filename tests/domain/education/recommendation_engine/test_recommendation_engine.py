"""Unit tests for the RecommendationEngine — core decision surface."""

from __future__ import annotations

from datetime import UTC, datetime

from domain.education.mastery_estimation.enums import LearningStabilityBand
from domain.education.recommendation_engine import (
    CompetencyId,
    RecommendationCategory,
    RecommendationEngine,
    RecommendationReasonCode,
    RecommendationSetId,
    SubjectId,
)
from tests.domain.education.recommendation_engine.conftest import (
    COMPETENCY_LINEAR_EQUATIONS,
    COMPETENCY_QUADRATIC_EQUATIONS,
    STUDENT_ID,
    SUBJECT_ALGEBRA,
    contradictory_reason,
    make_competency_assessment,
    make_knowledge_graph,
    make_mastery_assessment,
    make_prerequisite_gap,
    make_question_evidence,
    make_student_state,
)

AS_OF = datetime(2026, 7, 23, 12, 0, 0, tzinfo=UTC)


def test_recommend_is_deterministic(set_id: RecommendationSetId) -> None:
    state = make_student_state(
        competency_ids=(COMPETENCY_LINEAR_EQUATIONS, COMPETENCY_QUADRATIC_EQUATIONS)
    )
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.35,
                confidence_magnitude=0.7,
            ),
            make_competency_assessment(
                competency_id=COMPETENCY_QUADRATIC_EQUATIONS,
                mastery_magnitude=0.2,
                confidence_magnitude=0.3,
                gaps=(make_prerequisite_gap(),),
            ),
        ),
        assessed_at=AS_OF,
    )
    evidence = (
        make_question_evidence(
            evidence_id="e1", is_correct=False, occurred_at=AS_OF
        ),
    )
    graph = make_knowledge_graph(
        edges=((COMPETENCY_LINEAR_EQUATIONS, COMPETENCY_QUADRATIC_EQUATIONS, None),)
    )

    first = RecommendationEngine.recommend(
        state,
        assessment,
        evidence,
        graph,
        set_id=set_id,
        recommended_at=AS_OF,
    )
    second = RecommendationEngine.recommend(
        state,
        assessment,
        evidence,
        graph,
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert first == second
    assert [r.recommendation_id for r in first.recommendations] == [
        r.recommendation_id for r in second.recommendations
    ]


def test_weak_prerequisite_recommends_study_first(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state(
        competency_ids=(COMPETENCY_LINEAR_EQUATIONS, COMPETENCY_QUADRATIC_EQUATIONS)
    )
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                competency_id=COMPETENCY_QUADRATIC_EQUATIONS,
                mastery_magnitude=0.4,
                confidence_magnitude=0.5,
                gaps=(make_prerequisite_gap(),),
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    categories = {r.category for r in result.recommendations}
    assert RecommendationCategory.STUDY_PREREQUISITE in categories
    assert RecommendationCategory.DELAY_ADVANCED_TOPIC in categories
    study = next(
        r
        for r in result.recommendations
        if r.category is RecommendationCategory.STUDY_PREREQUISITE
    )
    assert study.target.competency_id == CompetencyId(COMPETENCY_LINEAR_EQUATIONS)
    assert result.has_blocking_constraints()


def test_low_mastery_high_confidence_reinforcement(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.4,
                confidence_magnitude=0.8,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert any(
        r.category is RecommendationCategory.STRENGTHEN_WEAK_AREA
        for r in result.recommendations
    )


def test_low_mastery_low_confidence_foundation(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.05,
                evidence_count=1,
                confidence_magnitude=0.15,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert any(
        r.category is RecommendationCategory.REVISIT_FOUNDATION
        for r in result.recommendations
    )


def test_stable_high_mastery_maintenance_and_reduce_revision(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.95,
                evidence_count=6,
                confidence_magnitude=0.85,
                stability_band=LearningStabilityBand.STABLE,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    categories = {r.category for r in result.recommendations}
    assert RecommendationCategory.MAINTAIN_MASTERY in categories
    assert RecommendationCategory.REDUCE_REVISION_FREQUENCY in categories


def test_contradictory_evidence_review(set_id: RecommendationSetId) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.55,
                contradiction_ratio=0.6,
                reasons=(contradictory_reason(),),
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    review = next(
        r
        for r in result.recommendations
        if r.category is RecommendationCategory.REVIEW_CONCEPT
    )
    assert (
        review.explanation.primary_reason_code
        is RecommendationReasonCode.CONTRADICTORY_EVIDENCE
    )


def test_continue_current_mission(set_id: RecommendationSetId) -> None:
    state = make_student_state(with_mission=True)
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.7,
                evidence_count=4,
                confidence_magnitude=0.65,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert any(
        r.category is RecommendationCategory.CONTINUE_CURRENT_MISSION
        for r in result.recommendations
    )


def test_attempt_checkpoint_when_secure(set_id: RecommendationSetId) -> None:
    state = make_student_state(with_checkpoint=True)
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.9,
                evidence_count=5,
                confidence_magnitude=0.8,
                stability_band=LearningStabilityBand.STABLE,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert any(
        r.category is RecommendationCategory.ATTEMPT_CHECKPOINT
        for r in result.recommendations
    )


def test_prepare_assessment_when_checkpoint_but_weak(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state(with_checkpoint=True)
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.35,
                confidence_magnitude=0.3,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert any(
        r.category is RecommendationCategory.PREPARE_ASSESSMENT
        for r in result.recommendations
    )


def test_recommend_for_subject_scopes(
    set_id: RecommendationSetId, subject_id: SubjectId
) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(assessed_at=AS_OF)
    result = RecommendationEngine.recommend_for_subject(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        subject_id=subject_id,
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert result.student_id == STUDENT_ID
    for recommendation in result.recommendations:
        assert recommendation.target.subject_id == subject_id


def test_recommend_for_unknown_subject_empty(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(assessed_at=AS_OF)
    result = RecommendationEngine.recommend_for_subject(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        subject_id=SubjectId("unknown-subject"),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert result.is_empty()


def test_recommend_for_competency(
    set_id: RecommendationSetId, competency_id: CompetencyId
) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.4,
                confidence_magnitude=0.75,
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend_for_competency(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        competency_id=competency_id,
        set_id=set_id,
        recommended_at=AS_OF,
    )
    assert not result.is_empty()
    assert all(
        r.target.competency_id == competency_id
        or r.category is RecommendationCategory.STUDY_PREREQUISITE
        for r in result.recommendations
    )


def test_rank_and_prioritise_and_highest_impact(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state(
        competency_ids=(COMPETENCY_LINEAR_EQUATIONS, COMPETENCY_QUADRATIC_EQUATIONS)
    )
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.2,
                confidence_magnitude=0.2,
            ),
            make_competency_assessment(
                competency_id=COMPETENCY_QUADRATIC_EQUATIONS,
                mastery_magnitude=0.3,
                gaps=(make_prerequisite_gap(),),
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    ranked = RecommendationEngine.rank(result.recommendations)
    prioritised = RecommendationEngine.prioritise(result.recommendations)
    assert ranked == prioritised
    high = RecommendationEngine.identify_highest_impact_actions(result, limit=2)
    assert len(high) <= 2
    assert all(r.impact.magnitude >= 0.67 for r in high)


def test_generate_reasoning_and_snapshot(set_id: RecommendationSetId) -> None:
    explanation = RecommendationEngine.generate_reasoning(
        RecommendationCategory.FOCUS_COMPETENCY,
        subject_id=SubjectId(SUBJECT_ALGEBRA),
        competency_id=CompetencyId(COMPETENCY_LINEAR_EQUATIONS),
        detail=0.33,
    )
    assert (
        explanation.primary_reason_code
        is RecommendationReasonCode.LOW_MASTERY_LOW_CONFIDENCE
    )

    state = make_student_state()
    assessment = make_mastery_assessment(assessed_at=AS_OF)
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    snapshot = RecommendationEngine.produce_snapshot(result)
    assert snapshot.set_id == set_id
    assert snapshot.recommendation_count() == result.recommendation_count()


def test_engine_does_not_mutate_inputs(set_id: RecommendationSetId) -> None:
    state = make_student_state()
    assessment = make_mastery_assessment(assessed_at=AS_OF)
    graph = make_knowledge_graph()
    before_subjects = len(state.subject_states)
    before_gaps = len(assessment.knowledge_gaps)
    before_nodes = len(graph.nodes) if hasattr(graph, "nodes") else None

    RecommendationEngine.recommend(
        state,
        assessment,
        (),
        graph,
        set_id=set_id,
        recommended_at=AS_OF,
    )

    assert len(state.subject_states) == before_subjects
    assert len(assessment.knowledge_gaps) == before_gaps
    if before_nodes is not None:
        assert len(graph.nodes) == before_nodes


def test_recommendations_are_priority_ordered(
    set_id: RecommendationSetId,
) -> None:
    state = make_student_state(
        competency_ids=(COMPETENCY_LINEAR_EQUATIONS, COMPETENCY_QUADRATIC_EQUATIONS),
        with_mission=True,
    )
    assessment = make_mastery_assessment(
        competencies=(
            make_competency_assessment(
                mastery_magnitude=0.95,
                evidence_count=5,
                confidence_magnitude=0.9,
                stability_band=LearningStabilityBand.STABLE,
            ),
            make_competency_assessment(
                competency_id=COMPETENCY_QUADRATIC_EQUATIONS,
                mastery_magnitude=0.25,
                gaps=(make_prerequisite_gap(),),
            ),
        ),
        assessed_at=AS_OF,
    )
    result = RecommendationEngine.recommend(
        state,
        assessment,
        (),
        make_knowledge_graph(),
        set_id=set_id,
        recommended_at=AS_OF,
    )
    priorities = [r.priority.magnitude for r in result.recommendations]
    assert priorities == sorted(priorities, reverse=True)
    assert result.recommendations[0].ordering.rank == 1

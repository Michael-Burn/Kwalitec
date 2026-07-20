"""Policy tests for Evidence Interpretation domain."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    ClusteringPolicy,
    InterpretationStatus,
    InterpretationValidationPolicy,
    PatternKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from tests.domain.education.evidence_interpretation.conftest import (
    CONCEPT_SELECT,
    EPISODE_001,
    EVIDENCE_001,
    EVIDENCE_002,
    KNOWN_CONCEPTS,
    KNOWN_EPISODES,
    KNOWN_EVIDENCE,
    make_cluster,
    make_confidence,
    make_context,
    make_pattern,
    make_summary,
)


def test_validation_assert_student_id() -> None:
    assert InterpretationValidationPolicy.assert_student_id("ada") == "ada"
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_student_id("  ")


def test_validation_assert_context() -> None:
    ctx = make_context()
    assert InterpretationValidationPolicy.assert_context(ctx) is ctx
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_context("ctx")  # type: ignore[arg-type]


def test_validation_assert_confidence_and_summary() -> None:
    conf = make_confidence()
    summary = make_summary()
    assert InterpretationValidationPolicy.assert_confidence(conf) is conf
    assert InterpretationValidationPolicy.assert_summary(summary) is summary


def test_validation_assert_mutable() -> None:
    InterpretationValidationPolicy.assert_mutable(
        InterpretationStatus.ACTIVE, action="revise"
    )
    InterpretationValidationPolicy.assert_mutable(
        InterpretationStatus.REVISED, action="revise"
    )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_mutable(
            InterpretationStatus.INVALIDATED, action="revise"
        )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_mutable(
            InterpretationStatus.MERGED, action="revise"
        )


def test_validation_known_sets() -> None:
    InterpretationValidationPolicy.assert_known_concepts(
        KNOWN_CONCEPTS, {CONCEPT_SELECT}
    )
    InterpretationValidationPolicy.assert_known_episodes(KNOWN_EPISODES, {EPISODE_001})
    InterpretationValidationPolicy.assert_known_evidence(
        KNOWN_EVIDENCE, {EVIDENCE_001, EVIDENCE_002}
    )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_known_concepts(
            KNOWN_CONCEPTS, {ConceptId("missing")}
        )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_known_episodes(
            KNOWN_EPISODES, {LearningEpisodeId("missing")}
        )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_known_evidence(
            KNOWN_EVIDENCE, {EvidenceId("missing")}
        )


def test_validation_collect_references() -> None:
    clusters = (make_cluster(),)
    patterns = (make_pattern(),)
    ctx = make_context()
    concepts = InterpretationValidationPolicy.collect_referenced_concept_ids(
        clusters, patterns, ctx, ()
    )
    assert CONCEPT_SELECT in concepts
    episodes = InterpretationValidationPolicy.collect_referenced_episode_ids(
        clusters, patterns, ctx, ()
    )
    assert EPISODE_001 in episodes


def test_clustering_assert_consistent_ok() -> None:
    ClusteringPolicy.assert_consistent(
        (make_cluster(),),
        (make_pattern(),),
        make_confidence(),
    )


def test_clustering_merge_compatible() -> None:
    ClusteringPolicy.assert_merge_compatible("a", "a")
    with pytest.raises(EducationalInvariantViolation):
        ClusteringPolicy.assert_merge_compatible("a", "b")


@pytest.mark.parametrize(
    "kind",
    [
        PatternKind.REPEATED_RETRIEVAL_FAILURE,
        PatternKind.REPEATED_TRANSFER_FAILURE,
        PatternKind.REPEATED_MISCONCEPTION_INDICATOR,
        PatternKind.REPEATED_PROCEDURAL_ERROR,
    ],
)
def test_clustering_size_for_repeated_kinds(kind: PatternKind) -> None:
    with pytest.raises(EducationalInvariantViolation):
        ClusteringPolicy.assert_cluster_size_for_patterns(
            (make_cluster(evidence_ids=(EVIDENCE_001,)),),
            (
                make_pattern(
                    kind=kind,
                    description=f"{kind.value} needs size",
                    evidence_ids=(EVIDENCE_001, EVIDENCE_002),
                ),
            ),
        )


def test_soft_ceiling_policy() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ClusteringPolicy.assert_confidence_consistent_with_patterns(
            make_confidence(ConfidenceLevel.VERY_HIGH),
            (
                make_pattern(
                    kind=PatternKind.REPEATED_CONFIDENCE_MISMATCH,
                    description="Felt high, scored low repeatedly",
                ),
            ),
        )


def test_assert_pattern_not_duplicate() -> None:
    existing = [make_pattern()]
    InterpretationValidationPolicy.assert_pattern_not_duplicate(
        existing,
        make_pattern(
            pattern_id="new",
            kind=PatternKind.TREND_STABILITY,
            description="Different",
            evidence_ids=(EVIDENCE_001,),
            occurrence_count=1,
        ),
    )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_pattern_not_duplicate(
            existing, make_pattern(pattern_id="other-id")
        )


def test_assert_status() -> None:
    for status in InterpretationStatus:
        assert InterpretationValidationPolicy.assert_status(status) is status
    with pytest.raises(EducationalInvariantViolation):
        InterpretationValidationPolicy.assert_status("active")  # type: ignore[arg-type]


def test_assert_references_evidence() -> None:
    ids = InterpretationValidationPolicy.assert_references_evidence(
        (make_cluster(),),
        (make_pattern(),),
    )
    assert EVIDENCE_001 in ids

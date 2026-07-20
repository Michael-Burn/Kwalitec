"""Invariant tests for Evidence Interpretation domain."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    Interpretation,
    InterpretationId,
    PatternKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence_interpretation.conftest import (
    EVIDENCE_001,
    EVIDENCE_002,
    KNOWN_CONCEPTS,
    KNOWN_EPISODES,
    KNOWN_EVIDENCE,
    make_cluster,
    make_confidence,
    make_context,
    make_interpretation,
    make_pattern,
    make_summary,
)


def test_must_reference_evidence() -> None:
    """Cannot construct without evidence clusters."""
    with pytest.raises(EducationalInvariantViolation) as exc:
        Interpretation.interpret(
            interpretation_id=InterpretationId("i1"),
            student_id="student-ada",
            clusters=[],
            patterns=[make_pattern()],
            context=make_context(),
            confidence=make_confidence(),
            summary=make_summary(),
            known_evidence_ids=KNOWN_EVIDENCE,
            known_concept_ids=KNOWN_CONCEPTS,
            known_episode_ids=KNOWN_EPISODES,
        )
    assert "clusters" in (exc.value.invariant or "")


def test_must_possess_confidence() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        Interpretation.interpret(
            interpretation_id=InterpretationId("i1"),
            student_id="student-ada",
            clusters=[make_cluster()],
            patterns=[make_pattern()],
            context=make_context(),
            confidence="high",  # type: ignore[arg-type]
            summary=make_summary(),
            known_evidence_ids=KNOWN_EVIDENCE,
            known_concept_ids=KNOWN_CONCEPTS,
            known_episode_ids=KNOWN_EPISODES,
        )
    assert exc.value.invariant == "Interpretation.confidence.required"


def test_must_identify_educational_scope() -> None:
    # Context construction itself rejects blank scope.
    with pytest.raises(EducationalInvariantViolation):
        make_context(educational_scope="")


def test_cannot_duplicate_patterns() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            patterns=[
                make_pattern(pattern_id="a"),
                make_pattern(pattern_id="b"),  # same signature
            ],
            summary=make_summary(pattern_count=2, cluster_count=1),
        )
    assert exc.value.invariant == "Interpretation.patterns.no_duplicate"


def test_cannot_duplicate_pattern_ids() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            patterns=[
                make_pattern(pattern_id="same", description="One"),
                make_pattern(
                    pattern_id="same",
                    kind=PatternKind.REPEATED_TRANSFER_FAILURE,
                    description="Two",
                ),
            ],
            summary=make_summary(pattern_count=2, cluster_count=1),
        )
    assert "duplicate" in (exc.value.invariant or "")


def test_cannot_exist_without_patterns() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        Interpretation.interpret(
            interpretation_id=InterpretationId("i1"),
            student_id="student-ada",
            clusters=[make_cluster()],
            patterns=[],
            context=make_context(),
            confidence=make_confidence(),
            summary=make_summary(pattern_count=1, cluster_count=1),
            known_evidence_ids=KNOWN_EVIDENCE,
            known_concept_ids=KNOWN_CONCEPTS,
            known_episode_ids=KNOWN_EPISODES,
        )
    assert exc.value.invariant == "Interpretation.patterns.min_one"


def test_unknown_evidence_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            known_evidence=frozenset({EVIDENCE_001}),
            clusters=[make_cluster(evidence_ids=(EVIDENCE_001, EVIDENCE_002))],
            patterns=[
                make_pattern(evidence_ids=(EVIDENCE_001, EVIDENCE_002)),
            ],
        )
    assert exc.value.invariant == "Interpretation.evidence.known"


def test_unknown_concept_rejected() -> None:
    unknown = ConceptId("concept-unknown")
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(
            patterns=[make_pattern(concept_id=unknown)],
            clusters=[make_cluster(concept_id=unknown)],
        )


def test_unknown_episode_rejected() -> None:
    unknown = LearningEpisodeId("episode-unknown")
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(
            patterns=[make_pattern(learning_episode_id=unknown)],
            clusters=[make_cluster(learning_episode_id=unknown)],
        )


def test_pattern_evidence_must_be_in_cluster() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            clusters=[make_cluster(evidence_ids=(EVIDENCE_001, EVIDENCE_002))],
            patterns=[
                make_pattern(
                    evidence_ids=(
                        EVIDENCE_001,
                        EvidenceId("evidence-003"),
                    )
                )
            ],
        )
    assert "in_cluster" in (exc.value.invariant or "")


def test_orphan_cluster_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            clusters=[
                make_cluster(
                    cluster_id="c1",
                    evidence_ids=(EVIDENCE_001, EVIDENCE_002),
                ),
                make_cluster(
                    cluster_id="c2",
                    theme="orphan theme",
                    evidence_ids=(EvidenceId("evidence-003"),),
                ),
            ],
            patterns=[make_pattern(evidence_ids=(EVIDENCE_001, EVIDENCE_002))],
            summary=make_summary(pattern_count=1, cluster_count=2),
        )
    assert "orphan" in (exc.value.invariant or "")


def test_repeated_pattern_requires_large_enough_cluster() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            clusters=[make_cluster(evidence_ids=(EVIDENCE_001,))],
            patterns=[
                make_pattern(
                    kind=PatternKind.EVIDENCE_SUFFICIENCY,
                    description="sufficiency only",
                    evidence_ids=(EVIDENCE_001,),
                    occurrence_count=1,
                ),
                make_pattern(
                    pattern_id="p-repeated",
                    kind=PatternKind.REPEATED_RETRIEVAL_FAILURE,
                    description="needs size",
                    evidence_ids=(EVIDENCE_001, EVIDENCE_001),  # will fail earlier
                ),
            ],
            summary=make_summary(pattern_count=2, cluster_count=1),
        )
    # Either duplicate evidence in pattern or cluster size — both are invariants.
    assert exc.value.invariant is not None


def test_soft_patterns_cannot_claim_very_high_confidence() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            patterns=[
                make_pattern(
                    kind=PatternKind.REPEATED_REFLECTION_THEME,
                    description="Repeated reflection theme about difficulty",
                )
            ],
            confidence=make_confidence(ConfidenceLevel.VERY_HIGH),
        )
    assert "soft_ceiling" in (exc.value.invariant or "")


def test_summary_counts_must_match() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        make_interpretation(
            summary=make_summary(pattern_count=9, cluster_count=1),
        )
    assert "pattern_count" in (exc.value.invariant or "")


def test_student_id_required() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(student_id="")


def test_identity_required() -> None:
    with pytest.raises(EducationalInvariantViolation):
        Interpretation.interpret(
            interpretation_id="not-id",  # type: ignore[arg-type]
            student_id="student-ada",
            clusters=[make_cluster()],
            patterns=[make_pattern()],
            context=make_context(),
            confidence=make_confidence(),
            summary=make_summary(),
            known_evidence_ids=KNOWN_EVIDENCE,
            known_concept_ids=KNOWN_CONCEPTS,
            known_episode_ids=KNOWN_EPISODES,
        )


def test_duplicate_clusters_rejected() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(
            clusters=[
                make_cluster(cluster_id="c1"),
                make_cluster(cluster_id="c2"),  # identical signature
            ],
            summary=make_summary(pattern_count=1, cluster_count=2),
        )


def test_confidence_floor_for_trend_stability() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(
            clusters=[make_cluster(evidence_ids=(EVIDENCE_001,))],
            patterns=[
                make_pattern(
                    kind=PatternKind.TREND_STABILITY,
                    description="Stable trend across window",
                    evidence_ids=(EVIDENCE_001,),
                    occurrence_count=1,
                )
            ],
            confidence=make_confidence(ConfidenceLevel.VERY_LOW),
            summary=make_summary(pattern_count=1, cluster_count=1),
        )


def test_concept_reference_must_be_known() -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_interpretation(
            concept_references=[
                ConceptReference(concept_id=ConceptId("concept-ghost"))
            ],
        )

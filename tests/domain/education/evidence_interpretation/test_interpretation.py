"""Interpretation aggregate behaviour tests."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    Interpretation,
    InterpretationCreated,
    InterpretationId,
    InterpretationStatus,
    PatternKind,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence_interpretation.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    EPISODE_002,
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
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


def test_interpret_creates_active_with_event() -> None:
    interp = make_interpretation()
    assert interp.is_active()
    assert interp.pattern_count() == 1
    assert interp.cluster_count() == 1
    events = interp.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], InterpretationCreated)
    assert events[0].pattern_count == 1
    assert interp.pull_events() == []


def test_interpret_identity_and_repr() -> None:
    interp = make_interpretation(interpretation_id="interp-xyz")
    assert interp.interpretation_id == InterpretationId("interp-xyz")
    assert "interp-xyz" in repr(interp)
    assert interp == make_interpretation(interpretation_id="interp-xyz")
    assert hash(interp) == hash(make_interpretation(interpretation_id="interp-xyz"))


def test_has_concept_episode_evidence() -> None:
    interp = make_interpretation()
    assert interp.has_concept(CONCEPT_SELECT)
    assert interp.has_learning_episode(EPISODE_001)
    assert interp.has_evidence(EVIDENCE_001)
    assert not interp.has_evidence(EvidenceId("evidence-missing"))


def test_patterns_of_kind() -> None:
    interp = make_interpretation()
    found = interp.patterns_of_kind(PatternKind.REPEATED_RETRIEVAL_FAILURE)
    assert len(found) == 1
    assert interp.patterns_of_kind(PatternKind.TREND_STABILITY) == ()


def test_revise_patterns_and_status() -> None:
    interp = make_interpretation()
    interp.pull_events()
    new_pattern = make_pattern(
        pattern_id="pattern-rev",
        kind=PatternKind.REPEATED_TRANSFER_FAILURE,
        description="Revised transfer failure pattern",
        evidence_ids=(EVIDENCE_001, EVIDENCE_002),
    )
    interp.revise(
        patterns=[new_pattern],
        summary=make_summary(
            text="Revised observational summary of transfer failures",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert interp.is_revised()
    assert interp.patterns[0].kind is PatternKind.REPEATED_TRANSFER_FAILURE


def test_revise_confidence() -> None:
    interp = make_interpretation()
    interp.revise(confidence=make_confidence(ConfidenceLevel.MEDIUM, ratio=0.55))
    assert interp.confidence.level is ConfidenceLevel.MEDIUM
    assert interp.is_revised()


def test_invalidate() -> None:
    interp = make_interpretation()
    interp.invalidate("signal provenance disputed")
    assert interp.is_invalidated()
    assert interp.invalidation_reason == "signal provenance disputed"
    with pytest.raises(EducationalInvariantViolation):
        interp.revise(confidence=make_confidence())


def test_merge_absorbs_patterns() -> None:
    primary = make_interpretation(interpretation_id="primary")
    other = make_interpretation(
        interpretation_id="other",
        clusters=[
            make_cluster(
                cluster_id="cluster-other",
                theme="transfer failures",
                evidence_ids=(EVIDENCE_001, EVIDENCE_003),
            )
        ],
        patterns=[
            make_pattern(
                pattern_id="pattern-other",
                kind=PatternKind.REPEATED_TRANSFER_FAILURE,
                description="Repeated transfer failures",
                evidence_ids=(EVIDENCE_001, EVIDENCE_003),
            )
        ],
        summary=make_summary(
            text="Observed repeated transfer failures",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    primary.merge(other)
    assert primary.pattern_count() == 2
    assert primary.cluster_count() == 2
    assert other.is_merged()
    with pytest.raises(EducationalInvariantViolation):
        other.invalidate("already merged")


def test_merge_rejects_self() -> None:
    interp = make_interpretation()
    with pytest.raises(EducationalInvariantViolation):
        interp.merge(interp)


def test_merge_rejects_different_student() -> None:
    primary = make_interpretation(student_id="student-a")
    other = make_interpretation(
        interpretation_id="other",
        student_id="student-b",
        patterns=[
            make_pattern(
                pattern_id="p-other",
                description="Other student pattern",
            )
        ],
    )
    with pytest.raises(EducationalInvariantViolation):
        primary.merge(other)


def test_merge_rejects_duplicate_pattern_signature() -> None:
    primary = make_interpretation(interpretation_id="primary")
    other = make_interpretation(
        interpretation_id="other",
        clusters=[
            make_cluster(cluster_id="cluster-other", theme="other theme")
        ],
        patterns=[
            make_pattern(
                pattern_id="pattern-other",
                # same signature as primary default pattern
            )
        ],
    )
    with pytest.raises(EducationalInvariantViolation):
        primary.merge(other)


def test_cannot_mutate_invalidated() -> None:
    interp = make_interpretation()
    interp.invalidate("void")
    with pytest.raises(EducationalInvariantViolation):
        interp.merge(make_interpretation(interpretation_id="other"))


def test_referenced_evidence_ids() -> None:
    interp = make_interpretation()
    ids = interp.referenced_evidence_ids()
    assert EVIDENCE_001 in ids
    assert EVIDENCE_002 in ids


def test_equality_by_identity() -> None:
    a = make_interpretation(interpretation_id="same")
    b = make_interpretation(interpretation_id="same")
    c = make_interpretation(interpretation_id="different")
    assert a == b
    assert a != c


def test_constructor_without_event() -> None:
    interp = Interpretation(
        interpretation_id=InterpretationId("interp-quiet"),
        student_id="student-ada",
        clusters=[make_cluster()],
        patterns=[make_pattern()],
        context=make_context(),
        confidence=make_confidence(),
        summary=make_summary(),
        known_evidence_ids=KNOWN_EVIDENCE,
        known_concept_ids=KNOWN_CONCEPTS,
        known_episode_ids=KNOWN_EPISODES,
        concept_references=[ConceptReference(concept_id=CONCEPT_SELECT)],
        learning_episode_ids=[EPISODE_001],
        _record_created=False,
    )
    assert interp.pull_events() == []
    assert interp.status is InterpretationStatus.ACTIVE


def test_revise_context() -> None:
    interp = make_interpretation()
    new_ctx = make_context(
        context_id="ctx-rev",
        educational_scope="Ultimate mortality scope",
        concepts=(ConceptReference(concept_id=CONCEPT_ULTIMATE),),
        episodes=(EPISODE_002,),
    )
    # Need known concepts to include ultimate which is already in KNOWN_CONCEPTS
    interp.revise(
        context=new_ctx,
        patterns=[
            make_pattern(
                concept_id=CONCEPT_ULTIMATE,
                learning_episode_id=EPISODE_002,
                description="Pattern on ultimate mortality",
            )
        ],
        clusters=[
            make_cluster(
                concept_id=CONCEPT_ULTIMATE,
                learning_episode_id=EPISODE_002,
                theme="ultimate retrieval",
            )
        ],
        summary=make_summary(
            text="Observed patterns on ultimate mortality",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    assert interp.context.educational_scope.startswith("Ultimate")
    assert interp.has_concept(CONCEPT_ULTIMATE)


def test_merge_expands_concept_and_episode_refs() -> None:
    primary = make_interpretation(interpretation_id="primary")
    other = make_interpretation(
        interpretation_id="other",
        clusters=[
            make_cluster(
                cluster_id="c-ult",
                theme="ultimate",
                concept_id=CONCEPT_ULTIMATE,
                learning_episode_id=EPISODE_002,
                evidence_ids=(EVIDENCE_002, EVIDENCE_003),
            )
        ],
        patterns=[
            make_pattern(
                pattern_id="p-ult",
                kind=PatternKind.REPEATED_PROCEDURAL_ERROR,
                description="Repeated procedural errors on ultimate",
                concept_id=CONCEPT_ULTIMATE,
                learning_episode_id=EPISODE_002,
                evidence_ids=(EVIDENCE_002, EVIDENCE_003),
            )
        ],
        context=make_context(
            concepts=(ConceptReference(concept_id=CONCEPT_ULTIMATE),),
            episodes=(EPISODE_002,),
        ),
        concept_references=[ConceptReference(concept_id=CONCEPT_ULTIMATE)],
        learning_episode_ids=[EPISODE_002],
        summary=make_summary(
            text="Observed repeated procedural errors",
            pattern_count=1,
            cluster_count=1,
        ),
    )
    primary.merge(other)
    assert primary.has_concept(CONCEPT_ULTIMATE)
    assert primary.has_learning_episode(EPISODE_002)

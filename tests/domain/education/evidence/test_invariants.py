"""Invariant enforcement tests for EvidenceRecord."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    EvidenceContext,
    EvidenceContextId,
    EvidenceRecord,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    KNOWN_CONCEPTS,
    KNOWN_EPISODES,
    make_confidence,
    make_context,
    make_item,
    make_record,
    make_source,
    make_strength,
    make_timestamp,
)


class TestRequiredConstituents:
    def test_requires_at_least_one_item(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceRecord.record(
                evidence_id=EvidenceId("e1"),
                student_id="student-ada",
                items=[],
                source=make_source(),
                context=make_context(),
                confidence=make_confidence(),
                strength=make_strength(),
                timestamp=make_timestamp(),
                known_concept_ids=KNOWN_CONCEPTS,
                known_episode_ids=KNOWN_EPISODES,
            )
        assert exc.value.invariant == "EvidenceRecord.items.min_one"

    def test_requires_source(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceRecord.record(
                evidence_id=EvidenceId("e1"),
                student_id="student-ada",
                items=[make_item()],
                source=None,  # type: ignore[arg-type]
                context=make_context(),
                confidence=make_confidence(),
                strength=make_strength(),
                timestamp=make_timestamp(),
                known_concept_ids=KNOWN_CONCEPTS,
                known_episode_ids=KNOWN_EPISODES,
            )

    def test_requires_context(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceRecord.record(
                evidence_id=EvidenceId("e1"),
                student_id="student-ada",
                items=[make_item()],
                source=make_source(),
                context=None,  # type: ignore[arg-type]
                confidence=make_confidence(),
                strength=make_strength(),
                timestamp=make_timestamp(),
                known_concept_ids=KNOWN_CONCEPTS,
                known_episode_ids=KNOWN_EPISODES,
            )

    def test_requires_confidence(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceRecord.record(
                evidence_id=EvidenceId("e1"),
                student_id="student-ada",
                items=[make_item()],
                source=make_source(),
                context=make_context(),
                confidence=None,  # type: ignore[arg-type]
                strength=make_strength(),
                timestamp=make_timestamp(),
                known_concept_ids=KNOWN_CONCEPTS,
                known_episode_ids=KNOWN_EPISODES,
            )

    def test_requires_timestamp(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceRecord.record(
                evidence_id=EvidenceId("e1"),
                student_id="student-ada",
                items=[make_item()],
                source=make_source(),
                context=make_context(),
                confidence=make_confidence(),
                strength=make_strength(),
                timestamp=None,  # type: ignore[arg-type]
                known_concept_ids=KNOWN_CONCEPTS,
                known_episode_ids=KNOWN_EPISODES,
            )


class TestDuplicatePrevention:
    def test_identical_items_rejected_at_record(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            make_record(
                items=[
                    make_item(item_id="a", observation="Same outcome"),
                    make_item(item_id="b", observation="Same outcome"),
                ]
            )
        assert exc.value.invariant == "EvidenceRecord.items.no_identical_duplicate"

    def test_add_item_rejects_identical(self) -> None:
        record = make_record()
        with pytest.raises(EducationalInvariantViolation):
            record.add_item(
                make_item(
                    item_id="item-002",
                    observation=record.items[0].observation,
                )
            )

    def test_merge_rejects_identical(self) -> None:
        primary = make_record(evidence_id="ev-a")
        other = make_record(evidence_id="ev-b")
        with pytest.raises(EducationalInvariantViolation):
            primary.merge(other)


class TestUnknownReferences:
    def test_unknown_concept_on_item_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            make_record(
                items=[
                    make_item(concept_id=ConceptId("concept-not-known")),
                ],
                context=EvidenceContext(
                    context_id=EvidenceContextId("ctx"),
                    situation="Probe without concepts",
                ),
                concept_references=[],
                known_concepts=frozenset({CONCEPT_SELECT}),
            )
        assert exc.value.invariant == "EvidenceRecord.concepts.known"

    def test_unknown_episode_on_item_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            make_record(
                items=[
                    make_item(learning_episode_id=LearningEpisodeId("episode-ghost")),
                ],
                context=EvidenceContext(
                    context_id=EvidenceContextId("ctx"),
                    situation="Probe",
                    concept_references=(
                        ConceptReference(concept_id=CONCEPT_SELECT),
                    ),
                ),
                learning_episode_ids=[],
                known_episodes=frozenset({EPISODE_001}),
            )
        assert exc.value.invariant == "EvidenceRecord.episodes.known"

    def test_unknown_concept_on_context_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            make_record(
                items=[make_item(concept_id=None, learning_episode_id=None)],
                context=make_context(
                    concepts=(
                        ConceptReference(concept_id=ConceptId("concept-ghost")),
                    ),
                    episodes=(),
                ),
                concept_references=[],
                learning_episode_ids=[],
                known_concepts=frozenset({CONCEPT_SELECT}),
                known_episodes=frozenset(),
            )

    def test_amend_rejects_unknown_concept(self) -> None:
        record = make_record()
        with pytest.raises(EducationalInvariantViolation):
            record.amend(
                items=[
                    make_item(
                        item_id="new",
                        concept_id=ConceptId("concept-ghost"),
                        observation="New observation",
                    )
                ]
            )


class TestBehaviourGuards:
    def test_cannot_amend_invalidated(self) -> None:
        record = make_record()
        record.invalidate("void")
        with pytest.raises(EducationalInvariantViolation):
            record.amend()

    def test_cannot_invalidate_twice(self) -> None:
        record = make_record()
        record.invalidate("first")
        with pytest.raises(EducationalInvariantViolation):
            record.invalidate("second")

    def test_cannot_merge_self(self) -> None:
        record = make_record()
        with pytest.raises(EducationalInvariantViolation):
            record.merge(record)

    def test_cannot_merge_different_students(self) -> None:
        a = make_record(evidence_id="a", student_id="student-a")
        b = make_record(
            evidence_id="b",
            student_id="student-b",
            items=[make_item(item_id="other", observation="Other outcome")],
        )
        with pytest.raises(EducationalInvariantViolation):
            a.merge(b)

    def test_attach_context_unknown_concept(self) -> None:
        record = make_record(known_concepts=frozenset({CONCEPT_SELECT}))
        with pytest.raises(EducationalInvariantViolation):
            record.attach_context(
                make_context(
                    context_id="ctx-2",
                    concepts=(
                        ConceptReference(concept_id=CONCEPT_ULTIMATE),
                    ),
                    episodes=(EPISODE_001,),
                )
            )

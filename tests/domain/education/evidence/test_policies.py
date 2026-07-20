"""Policy tests for Evidence domain."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceConsistencyPolicy,
    EvidenceItemKind,
    EvidenceRecordStatus,
    EvidenceSourceKind,
    EvidenceStrength,
    EvidenceValidationPolicy,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from tests.domain.education.evidence.conftest import (
    CONCEPT_SELECT,
    EPISODE_001,
    make_confidence,
    make_context,
    make_item,
    make_source,
    make_strength,
    make_timestamp,
)


class TestEvidenceValidationPolicy:
    def test_identity(self) -> None:
        eid = EvidenceId("ev-1")
        assert EvidenceValidationPolicy.assert_identity(eid) is eid

    def test_identity_type(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_identity("ev-1")  # type: ignore[arg-type]

    def test_student_id(self) -> None:
        assert EvidenceValidationPolicy.assert_student_id("student-1") == "student-1"

    def test_student_id_blank(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_student_id("  ")

    def test_items_min_one(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceValidationPolicy.assert_items(())
        assert exc.value.invariant == "EvidenceRecord.items.min_one"

    def test_items_duplicate_id(self) -> None:
        a = make_item(item_id="same", observation="A")
        b = make_item(item_id="same", observation="B")
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_items((a, b))

    def test_items_identical_duplicate(self) -> None:
        a = make_item(item_id="a", observation="Same observation")
        b = make_item(item_id="b", observation="Same observation")
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceValidationPolicy.assert_items((a, b))
        assert exc.value.invariant == "EvidenceRecord.items.no_identical_duplicate"

    def test_known_concepts(self) -> None:
        EvidenceValidationPolicy.assert_known_concepts(
            {CONCEPT_SELECT}, {CONCEPT_SELECT}
        )

    def test_unknown_concept(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceValidationPolicy.assert_known_concepts(
                {CONCEPT_SELECT}, {ConceptId("unknown-concept")}
            )
        assert exc.value.invariant == "EvidenceRecord.concepts.known"

    def test_unknown_episode(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceValidationPolicy.assert_known_episodes(
                {EPISODE_001}, {LearningEpisodeId("episode-unknown")}
            )
        assert exc.value.invariant == "EvidenceRecord.episodes.known"

    def test_mutable_invalidated(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_mutable(
                EvidenceRecordStatus.INVALIDATED, action="amend"
            )

    def test_mutable_merged(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceValidationPolicy.assert_mutable(
                EvidenceRecordStatus.MERGED, action="amend"
            )

    def test_required_constituents(self) -> None:
        source = make_source()
        context = make_context()
        confidence = make_confidence()
        strength = make_strength()
        timestamp = make_timestamp()
        assert EvidenceValidationPolicy.assert_source(source) is source
        assert EvidenceValidationPolicy.assert_context(context) is context
        assert EvidenceValidationPolicy.assert_confidence(confidence) is confidence
        assert EvidenceValidationPolicy.assert_strength(strength) is strength
        assert EvidenceValidationPolicy.assert_timestamp(timestamp) is timestamp

    @pytest.mark.parametrize(
        "method",
        [
            "assert_source",
            "assert_context",
            "assert_confidence",
            "assert_strength",
            "assert_timestamp",
        ],
    )
    def test_required_type_checks(self, method: str) -> None:
        fn = getattr(EvidenceValidationPolicy, method)
        with pytest.raises(EducationalInvariantViolation):
            fn(None)


class TestEvidenceConsistencyPolicy:
    def test_assessment_with_question_ok(self) -> None:
        EvidenceConsistencyPolicy.assert_source_item_affinity(
            make_source(kind=EvidenceSourceKind.ASSESSMENT),
            (make_item(kind=EvidenceItemKind.QUESTION_RESPONSE),),
        )

    def test_reflection_source_rejects_question(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceConsistencyPolicy.assert_source_item_affinity(
                make_source(kind=EvidenceSourceKind.REFLECTION_CAPTURE),
                (make_item(kind=EvidenceItemKind.QUESTION_RESPONSE),),
            )
        assert exc.value.invariant == "EvidenceConsistencyPolicy.source_item.affinity"

    def test_soft_items_cannot_be_very_strong(self) -> None:
        with pytest.raises(EducationalInvariantViolation) as exc:
            EvidenceConsistencyPolicy.assert_strength_consistent_with_items(
                EvidenceStrength.very_strong(),
                (
                    make_item(
                        kind=EvidenceItemKind.REFLECTION,
                        observation="I felt uncertain",
                    ),
                ),
            )
        assert exc.value.invariant == "EvidenceConsistencyPolicy.strength.soft_ceiling"

    def test_soft_items_moderate_ok(self) -> None:
        EvidenceConsistencyPolicy.assert_strength_consistent_with_items(
            EvidenceStrength.moderate(),
            (
                make_item(
                    kind=EvidenceItemKind.REFLECTION,
                    observation="I felt uncertain",
                ),
            ),
        )

    def test_confidence_floor_for_very_strong(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceConsistencyPolicy.assert_confidence_consistent_with_strength(
                ConfidenceMeasure.of(ConfidenceLevel.LOW),
                EvidenceStrength.very_strong(),
            )

    def test_confidence_floor_satisfied(self) -> None:
        EvidenceConsistencyPolicy.assert_confidence_consistent_with_strength(
            ConfidenceMeasure.of(ConfidenceLevel.HIGH),
            EvidenceStrength.very_strong(),
        )

    def test_merge_different_students(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceConsistencyPolicy.assert_merge_compatible(
                "student-a",
                "student-b",
                make_source(),
                make_source(source_id="s2"),
            )

    def test_merge_different_source_kinds(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceConsistencyPolicy.assert_merge_compatible(
                "student-a",
                "student-a",
                make_source(kind=EvidenceSourceKind.ASSESSMENT),
                make_source(
                    source_id="s2", kind=EvidenceSourceKind.STUDENT_ACTION
                ),
            )

    def test_assert_consistent_bundle(self) -> None:
        EvidenceConsistencyPolicy.assert_consistent(
            make_source(),
            (make_item(),),
            make_strength(),
            make_confidence(),
        )

"""Behavioural tests for EvidenceRecord aggregate."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    EvidenceItemKind,
    EvidenceRecordStatus,
    EvidenceSourceKind,
    EvidenceStrength,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.ids import EvidenceId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.evidence.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    EPISODE_002,
    make_confidence,
    make_context,
    make_item,
    make_record,
    make_source,
    make_strength,
    make_timestamp,
)


class TestRecordFactory:
    def test_record_creates_active(self) -> None:
        record = make_record()
        assert record.is_active()
        assert record.status is EvidenceRecordStatus.ACTIVE
        assert record.item_count() == 1
        assert record.evidence_id == EvidenceId("evidence-001")

    def test_equality_by_identity(self) -> None:
        a = make_record(evidence_id="same")
        b = make_record(evidence_id="same")
        assert a == b
        assert hash(a) == hash(b)

    def test_repr(self) -> None:
        record = make_record()
        assert "EvidenceRecord" in repr(record)
        assert "evidence-001" in repr(record)


class TestAmend:
    def test_amend_items_and_status(self) -> None:
        record = make_record()
        record.amend(
            items=[
                make_item(
                    item_id="item-amended",
                    observation="Amended observational detail",
                )
            ]
        )
        assert record.is_amended()
        assert record.items[0].observation == "Amended observational detail"

    def test_amend_confidence_strength_timestamp(self) -> None:
        record = make_record()
        new_ts = make_timestamp(hour=15)
        record.amend(
            confidence=make_confidence(ConfidenceLevel.VERY_HIGH, ratio=0.95),
            strength=EvidenceStrength.very_strong(),
            timestamp=new_ts,
        )
        assert record.confidence.level is ConfidenceLevel.VERY_HIGH
        assert record.strength.is_very_strong()
        assert record.timestamp == new_ts


class TestInvalidate:
    def test_invalidate(self) -> None:
        record = make_record()
        record.invalidate("incorrect attribution")
        assert record.is_invalidated()
        assert record.invalidation_reason == "incorrect attribution"


class TestMerge:
    def test_merge_absorbs_items(self) -> None:
        primary = make_record(evidence_id="ev-a")
        other = make_record(
            evidence_id="ev-b",
            items=[
                make_item(
                    item_id="item-b",
                    observation="Second distinct observation",
                    concept_id=CONCEPT_ULTIMATE,
                )
            ],
            concept_references=[ConceptReference(concept_id=CONCEPT_ULTIMATE)],
            learning_episode_ids=[EPISODE_002],
        )
        primary.merge(other)
        assert primary.item_count() == 2
        assert other.is_merged()
        assert primary.has_concept(CONCEPT_ULTIMATE)
        assert primary.has_learning_episode(EPISODE_002)


class TestAttachContext:
    def test_attach_context(self) -> None:
        record = make_record()
        new_ctx = make_context(
            context_id="ctx-new",
            situation="Revised educational situation",
            episodes=(EPISODE_001, EPISODE_002),
        )
        record.attach_context(new_ctx)
        assert record.context.situation == "Revised educational situation"
        assert EPISODE_002 in record.context.episode_ids()


class TestAddItem:
    def test_add_item(self) -> None:
        record = make_record()
        record.add_item(
            make_item(
                item_id="item-002",
                kind=EvidenceItemKind.RETRIEVAL_ATTEMPT,
                observation="Retrieval attempt recorded",
            )
        )
        assert record.item_count() == 2


class TestQueries:
    def test_has_concept_and_episode(self) -> None:
        record = make_record()
        assert record.has_concept(CONCEPT_SELECT)
        assert record.has_learning_episode(EPISODE_001)
        assert not record.has_concept(CONCEPT_ULTIMATE)

    @pytest.mark.parametrize(
        "kind,source_kind,strength_name,confidence",
        [
            (
                EvidenceItemKind.QUESTION_RESPONSE,
                EvidenceSourceKind.ASSESSMENT,
                "strong",
                ConfidenceLevel.HIGH,
            ),
            (
                EvidenceItemKind.WORKED_EXAMPLE_OUTCOME,
                EvidenceSourceKind.LEARNING_EPISODE,
                "moderate",
                ConfidenceLevel.MEDIUM,
            ),
            (
                EvidenceItemKind.RETRIEVAL_ATTEMPT,
                EvidenceSourceKind.STUDENT_ACTION,
                "moderate",
                ConfidenceLevel.MEDIUM,
            ),
            (
                EvidenceItemKind.TRANSFER_ATTEMPT,
                EvidenceSourceKind.ASSESSMENT,
                "strong",
                ConfidenceLevel.HIGH,
            ),
            (
                EvidenceItemKind.HINT_USAGE,
                EvidenceSourceKind.SYSTEM_OBSERVATION,
                "weak",
                ConfidenceLevel.LOW,
            ),
            (
                EvidenceItemKind.REFLECTION,
                EvidenceSourceKind.REFLECTION_CAPTURE,
                "weak",
                ConfidenceLevel.LOW,
            ),
        ],
    )
    def test_record_item_kind_matrix(
        self,
        kind: EvidenceItemKind,
        source_kind: EvidenceSourceKind,
        strength_name: str,
        confidence: ConfidenceLevel,
    ) -> None:
        record = make_record(
            items=[
                make_item(
                    kind=kind,
                    observation=f"Observation of kind {kind.value}",
                )
            ],
            source=make_source(kind=source_kind, label=f"Source {source_kind.value}"),
            strength=make_strength(level=strength_name),
            confidence=make_confidence(confidence),
        )
        assert record.items[0].kind is kind
        assert record.is_active()

"""Tests for EvidenceCollector."""

from __future__ import annotations

import pytest

from app.application.learning_session.evidence_collector import EvidenceCollector
from app.application.learning_session.exceptions import (
    EvidenceCollectionError,
    InvalidSessionState,
    SessionAlreadyArchived,
)
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_session.helpers import NOW, make_evidence, make_session


class TestEvidenceCollector:
    def setup_method(self):
        self.collector = EvidenceCollector(
            clock=lambda: NOW,
            id_factory=lambda: "e1",
        )

    def test_collect_on_active(self):
        session = make_session(state=SessionState.ACTIVE)
        updated, je = self.collector.collect(
            session,
            phase=RuntimePhase.ACTIVE,
            evidence_type=EvidenceType.STUDY_SESSION,
        )
        assert len(updated.evidence) == 1
        assert je.session_id == session.session_id
        assert je.evidence_type == EvidenceType.STUDY_SESSION

    def test_collect_on_completed(self):
        session = make_session(state=SessionState.COMPLETED)
        updated, _ = self.collector.collect(
            session,
            phase=RuntimePhase.COMPLETED,
            evidence_type=EvidenceType.QUESTION_ATTEMPT,
        )
        assert updated.evidence[0].evidence_type == EvidenceType.QUESTION_ATTEMPT

    def test_collect_rejects_planned(self):
        with pytest.raises(InvalidSessionState):
            self.collector.collect(
                make_session(),
                phase=RuntimePhase.PLANNED,
                evidence_type=EvidenceType.STUDY_SESSION,
            )

    def test_collect_rejects_ready(self):
        with pytest.raises(InvalidSessionState):
            self.collector.collect(
                make_session(),
                phase=RuntimePhase.READY,
                evidence_type=EvidenceType.STUDY_SESSION,
            )

    def test_collect_rejects_archived(self):
        with pytest.raises(SessionAlreadyArchived):
            self.collector.collect(
                make_session(state=SessionState.COMPLETED),
                phase=RuntimePhase.ARCHIVED,
                evidence_type=EvidenceType.STUDY_SESSION,
            )

    def test_collect_from_learning_evidence(self):
        le = LearningEvidence.create(
            "le-1",
            EvidenceType.QUIZ_COMPLETED,
            "evt-1",
            NOW,
            topic_id="topic-a",
            confidence_level=EvidenceConfidenceLevel.HIGH,
        )
        session = make_session(state=SessionState.ACTIVE)
        updated, je = self.collector.collect(
            session,
            phase=RuntimePhase.ACTIVE,
            evidence_type=EvidenceType.STUDY_SESSION,
            learning_evidence=le,
        )
        assert je.evidence_id == "le-1"
        assert je.evidence_type == EvidenceType.QUIZ_COMPLETED
        assert je.confidence_level == EvidenceConfidenceLevel.HIGH
        assert len(updated.evidence) == 1

    def test_collect_empty_evidence_id_raises(self):
        with pytest.raises(EvidenceCollectionError):
            self.collector.collect(
                make_session(state=SessionState.ACTIVE),
                phase=RuntimePhase.ACTIVE,
                evidence_type=EvidenceType.STUDY_SESSION,
                evidence_id="  ",
            )

    def test_summarise_empty(self):
        summary = self.collector.summarise(make_session())
        assert summary.evidence_count == 0
        assert not summary.has_evidence
        assert summary.evidence_types == ()

    def test_summarise_with_evidence(self):
        session = make_session(
            state=SessionState.ACTIVE,
            evidence=[
                make_evidence("je-1"),
                make_evidence(
                    "je-2",
                    evidence_id="ev-2",
                    confidence=EvidenceConfidenceLevel.HIGH,
                ),
            ],
        )
        # Second evidence still STUDY_SESSION type — adjust type via recreate
        summary = self.collector.summarise(session)
        assert summary.evidence_count == 2
        assert summary.has_evidence
        assert "study_session" in summary.evidence_types

    def test_collect_uses_session_objective_when_unspecified(self):
        session = make_session(state=SessionState.ACTIVE, objective_id="obj-9")
        _, je = self.collector.collect(
            session,
            phase=RuntimePhase.ACTIVE,
            evidence_type=EvidenceType.TIME_ON_TASK,
        )
        assert je.objective_id == "obj-9"

    def test_collect_append_only(self):
        session = make_session(
            state=SessionState.ACTIVE,
            evidence=[make_evidence()],
        )
        updated, _ = self.collector.collect(
            session,
            phase=RuntimePhase.ACTIVE,
            evidence_type=EvidenceType.HINT_REQUESTED,
            evidence_id="ev-new",
        )
        assert len(updated.evidence) == 2

    def test_collect_string_evidence_type(self):
        _, je = self.collector.collect(
            make_session(state=SessionState.PAUSED),
            phase=RuntimePhase.PAUSED,
            evidence_type="study_break",
        )
        assert je.evidence_type == EvidenceType.STUDY_BREAK

    def test_never_estimates_mastery(self):
        # Structural check: summary has no mastery field
        summary = self.collector.summarise(make_session())
        assert not hasattr(summary, "mastery")
        assert not hasattr(summary, "estimated_mastery")

"""EV-001B — Evidence Before Completion (SR-001A Phase P4).

Unit / integration / regression / acceptance coverage for:
accepted / rejected packages, reading-only, reflection-only, practice
acceptance, Partial / No finish review, mission + progress gates,
no Twin writes, rollback when SR_EVIDENCE_GATE is OFF.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
    SessionEvidencePackage,
)
from app.application.learning_session.dto.finish_review import FinishReviewVerdict
from app.application.learning_session.evidence_gate import (
    EvidenceBeforeCompletionGate,
)
from app.application.learning_session.evidence_package_builder import (
    EvidencePackageBuilder,
)
from app.application.learning_session.exceptions import EvidenceGateRejected
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from tests.application.learning_session.helpers import make_journey, make_objective
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def _flags_gate(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        "SR_SESSION_SUBSTANCE": "1",
        "SR_EVIDENCE_GATE": "1",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _flags_gate_off(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        "SR_EVIDENCE_GATE": "0",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _obs(
    type_id: RuntimeEvidenceType,
    *,
    student_id: str = "42",
    session_id: str = "lsr-ev-1",
) -> CandidateObservation:
    return CandidateObservation.create(
        observation_id=f"obs-{type_id.value}",
        type_id=type_id,
        student_id=student_id,
        session_id=session_id,
        topic_id="topic-cash",
        mission_instance_id="m-1",
    )


def _package(
    *types: RuntimeEvidenceType,
    finish: str = "yes",
    student_id: str = "42",
    session_id: str = "lsr-ev-1",
) -> SessionEvidencePackage:
    return SessionEvidencePackage.create(
        student_id=student_id,
        session_id=session_id,
        mission_instance_id="m-1",
        topic_id="topic-cash",
        topic_title="Cash flows",
        curriculum_identity="CS1:test",
        learning_objectives=("Explain operating cash flow",),
        observations=tuple(
            _obs(t, student_id=student_id, session_id=session_id) for t in types
        ),
        finish_review_verdict=finish,
    )


def _active_engine(monkeypatch, *, gate: bool = True):
    if gate:
        monkeypatch.setenv("SR_EVIDENCE_GATE", "1")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
        monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
    else:
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    lsr = LearningSessionRuntime()
    journey = make_journey(
        topic_id="topic-cash",
        objectives=[make_objective("obj-cash", topic_id="topic-cash")],
    )
    handle = lsr.create_session(journey, session_id="lsr-ev-1")
    handle = lsr.prepare_session(handle)
    handle = lsr.start_session(handle)
    persistence.save_binding(
        student_id="42",
        mission_instance_id="m-1",
        handle=handle,
        topic_title="Cash flows",
        topic_id="topic-cash",
        curriculum_identity="CS1:test",
    )
    engine = LearningSessionRuntimeEngine(
        runtime=lsr,
        persistence=persistence,
        mission_completer=_FakeMissionCompleter(),
    )
    return engine, persistence, lsr


class _FakeMissionCompleter:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def complete_mission(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        advance_progress: bool = True,
        evidence_package_id: str | None = None,
        evidence_disposition: str | None = None,
        may_complete_mission: bool | None = None,
        **_kwargs,
    ) -> None:
        self.calls.append(
            {
                "user_id": user_id,
                "mission_instance_id": mission_instance_id,
                "advance_progress": advance_progress,
                "evidence_package_id": evidence_package_id,
                "evidence_disposition": evidence_disposition,
                "may_complete_mission": may_complete_mission,
            }
        )


# ---------------------------------------------------------------------------
# Unit — Authority accept / reject
# ---------------------------------------------------------------------------


class TestAuthorityPackageValidation:
    def test_practice_package_accepted(self):
        package = _package(
            RuntimeEvidenceType.READING_COMPLETED,
            RuntimeEvidenceType.PRACTICE_ATTEMPTED,
            finish="yes",
        )
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS
        assert result.may_complete_session is True
        assert result.may_complete_mission is True
        assert result.may_advance_progress is True
        assert result.may_update_twin is False

    def test_scored_practice_accepted(self):
        package = _package(
            RuntimeEvidenceType.PRACTICE_CORRECT,
            finish="yes",
        )
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.ACCEPTED
        assert result.may_advance_progress is True
        assert result.may_update_twin is True

    def test_reading_only_rejected(self):
        package = _package(RuntimeEvidenceType.READING_COMPLETED, finish="yes")
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.REJECTED
        assert result.reason == "reading_only_package"
        assert result.may_complete_session is False
        assert result.may_complete_mission is False
        assert result.may_advance_progress is False

    def test_reflection_only_rejected(self):
        package = _package(RuntimeEvidenceType.REFLECTION_SUBMITTED, finish="yes")
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.REJECTED
        assert result.reason == "reflection_only_package"

    def test_duration_only_rejected(self):
        package = _package(RuntimeEvidenceType.SESSION_DURATION, finish="yes")
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.REJECTED
        assert result.reason == "duration_only_package"

    def test_checklist_only_rejected(self):
        package = _package(RuntimeEvidenceType.CHECKLIST_TICKS, finish="yes")
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.REJECTED
        assert result.reason == "checklist_only_package"

    def test_partial_review_honest_close(self):
        package = _package(
            RuntimeEvidenceType.PRACTICE_ATTEMPTED,
            finish="partially",
        )
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS
        assert result.may_complete_session is True
        assert result.may_complete_mission is False
        assert result.may_advance_progress is False
        assert result.may_update_twin is False

    def test_no_review_honest_close(self):
        package = _package(finish="no")
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS
        assert result.may_complete_session is True
        assert result.may_complete_mission is False
        assert result.reason == "explicit_no_finish_review"

    def test_finish_yes_alone_rejected(self):
        package = _package(
            RuntimeEvidenceType.FINISH_REVIEW_YES,
            finish="yes",
        )
        result = EducationalEvidenceAuthority.validate_session_evidence_package(
            package
        )
        assert result.disposition == EvidenceDisposition.REJECTED
        assert result.may_complete_mission is False


class TestPackageBuilderAndGate:
    def test_builder_maps_stages(self):
        builder = EvidencePackageBuilder(id_factory=lambda: "x")
        read = builder.observation_for_stage_response(
            stage="read",
            student_id="1",
            session_id="s1",
            response="notes",
        )
        practice = builder.observation_for_stage_response(
            stage="practice",
            student_id="1",
            session_id="s1",
            response="42",
        )
        assert read.type_id == RuntimeEvidenceType.READING_COMPLETED
        assert practice.type_id == RuntimeEvidenceType.PRACTICE_ATTEMPTED

    def test_gate_raises_on_rejected(self):
        gate = EvidenceBeforeCompletionGate()
        package = gate.build_and_validate(
            student_id="1",
            session_id="s1",
            observations=[_obs(RuntimeEvidenceType.READING_COMPLETED)],
            finish_review_verdict="yes",
        )
        with pytest.raises(EvidenceGateRejected) as exc:
            gate.assert_session_may_complete(package)
        assert exc.value.reason == "reading_only_package"

    def test_runtime_emits_candidate(self):
        lsr = LearningSessionRuntime(id_factory=lambda: "abc")
        obs = lsr.emit_candidate_observation(
            type_id=RuntimeEvidenceType.SESSION_STARTED.value,
            student_id="1",
            session_id="s1",
        )
        assert obs.type_id == RuntimeEvidenceType.SESSION_STARTED
        assert obs.lifecycle_state == "generated"


# ---------------------------------------------------------------------------
# Integration — session complete → evidence → mission
# ---------------------------------------------------------------------------


class TestSessionEvidenceIntegration:
    def test_practice_path_accepts_and_completes_mission(self, monkeypatch):
        engine, persistence, _ = _active_engine(monkeypatch, gate=True)
        engine.begin_session_opaque("42", session_id="lsr-ev-1")
        engine.record_response_opaque(
            "42",
            session_id="lsr-ev-1",
            activity_id="act-practice-1",
            response="working capital is current assets minus liabilities",
        )
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="yes",
        )
        assert result is not None
        assert result["status"] == "completed"
        assert result["evidence_disposition"] in {
            EvidenceDisposition.ACCEPTED.value,
            EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS.value,
        }
        assert result["mission_completed"] is True
        assert result["progress_advanced"] is True
        assert result["twin_updated"] is False
        saved = persistence.load_evidence_package(session_id="lsr-ev-1")
        assert saved is not None
        assert saved["lifecycle_state"] in {"persisted", "accepted"}
        assert engine._mission_completer.calls  # type: ignore[union-attr]

    def test_reading_only_blocks_completion(self, monkeypatch):
        engine, persistence, _ = _active_engine(monkeypatch, gate=True)
        engine.begin_session_opaque("42", session_id="lsr-ev-1")
        # Force reading-only candidates.
        obs = EvidencePackageBuilder().observation_for_stage_response(
            stage="read",
            student_id="42",
            session_id="lsr-ev-1",
            response="read notes",
        )
        persistence.append_candidate(session_id="lsr-ev-1", observation=obs.to_opaque())
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="yes",
        )
        assert result is not None
        assert result["error"] == "evidence_gate_rejected"
        assert result["mission_completed"] is False
        assert result["progress_advanced"] is False
        assert result["twin_updated"] is False
        assert not engine._mission_completer.calls  # type: ignore[union-attr]

    def test_partial_closes_session_without_mission(self, monkeypatch):
        engine, _, _ = _active_engine(monkeypatch, gate=True)
        engine.begin_session_opaque("42", session_id="lsr-ev-1")
        engine.record_response_opaque(
            "42",
            session_id="lsr-ev-1",
            activity_id="act-practice-1",
            response="partial attempt",
        )
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="partially",
        )
        assert result is not None
        assert result["status"] == "completed"
        assert result["mission_completed"] is False
        assert result["progress_advanced"] is False
        assert result["twin_updated"] is False
        assert result["evidence_disposition"] == (
            EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS.value
        )

    def test_no_review_closes_session_without_mission(self, monkeypatch):
        engine, _, _ = _active_engine(monkeypatch, gate=True)
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="no",
        )
        assert result is not None
        assert result["status"] == "completed"
        assert result["mission_completed"] is False
        assert result["progress_advanced"] is False


# ---------------------------------------------------------------------------
# Regression — Twin silence + flag rollback
# ---------------------------------------------------------------------------


class TestNoTwinAndRollback:
    def test_never_updates_twin(self, monkeypatch):
        engine, _, _ = _active_engine(monkeypatch, gate=True)
        engine.record_response_opaque(
            "42",
            session_id="lsr-ev-1",
            activity_id="act-practice-1",
            response="answer",
        )
        note = engine.record_reflection_note_opaque(
            "42", session_id="lsr-ev-1", note="felt hard"
        )
        assert note["twin_updated"] is False
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="yes",
        )
        assert result["twin_updated"] is False

    def test_gate_off_preserves_p2_p3_behaviour(self, monkeypatch):
        engine, persistence, _ = _active_engine(monkeypatch, gate=False)
        recorded = engine.record_response_opaque(
            "42",
            session_id="lsr-ev-1",
            activity_id="act-read-1",
            response="notes",
        )
        assert recorded["evidence_emitted"] is False
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="yes",
        )
        assert result["status"] == "completed"
        assert result["mission_completed"] is False
        assert result["progress_advanced"] is False
        assert persistence.load_evidence_package(session_id="lsr-ev-1") is None

    def test_persisted_package_survives_conceptual_rollback(self, monkeypatch):
        """C10 — flag OFF must not delete Persisted rows."""
        engine, persistence, _ = _active_engine(monkeypatch, gate=True)
        engine.record_response_opaque(
            "42",
            session_id="lsr-ev-1",
            activity_id="act-practice-1",
            response="answer",
        )
        engine.complete_session_opaque(
            "42",
            session_id="lsr-ev-1",
            finish_verdict="yes",
        )
        saved = persistence.load_evidence_package(session_id="lsr-ev-1")
        assert saved is not None
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        assert resolve_v2_feature_flags().SR_EVIDENCE_GATE is False
        assert persistence.load_evidence_package(session_id="lsr-ev-1") is not None


# ---------------------------------------------------------------------------
# Acceptance — G-Evidence + mark-complete blocked
# ---------------------------------------------------------------------------


class TestAcceptanceGEvidence:
    def test_flag_defaults_off(self):
        flags = resolve_v2_feature_flags(environ={})
        assert flags.SR_EVIDENCE_GATE is False

    def test_flag_enables(self):
        flags = _flags_gate()
        assert flags.SR_EVIDENCE_GATE is True

    def test_mark_complete_blocked_when_gate_on(
        self, app, client, db, ctx, monkeypatch
    ):
        monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
        monkeypatch.setenv("SR_PILOT_MARK_COMPLETE", "1")
        monkeypatch.setenv("SR_EVIDENCE_GATE", "1")
        user = make_user(email="ev001b@mark.test")
        db.session.add(user)
        db.session.commit()
        publish_subject("CS1")
        bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
        bridge.enrol(
            user_id=user.id,
            category_code=PUBLISHED_CATEGORY_CODE,
            subject_code="CS1",
            exam_date=date.today() + timedelta(days=120),
        )
        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True
        response = client.post(
            "/student/mission/complete",
            data={"mission_id": "does-not-matter"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        body = response.get_data(as_text=True).lower()
        assert "study session" in body or "evidence" in body


class TestFinishReviewVerdictsExport:
    def test_verdicts_stable(self):
        assert FinishReviewVerdict.YES.value == "yes"
        assert FinishReviewVerdict.PARTIALLY.value == "partially"
        assert FinishReviewVerdict.NO.value == "no"

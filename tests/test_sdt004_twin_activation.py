"""SDT-004 — Student Digital Twin Activation (SR-001A Phase P5).

Verify Twin consumes only Accepted Educational+ evidence; ignores Rejected,
Behavioural-only, Informational, reading-only, and reflection-only packages;
never becomes Evidence Authority; Progress unaffected; estimates reproducible.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
    SessionEvidencePackage,
)
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.student_twin.daily_loop_codec import (
    decode_daily_loop_twin,
    encode_daily_loop_twin,
)
from app.application.student_twin.session_evidence_consumer import (
    SessionTwinEvidenceConsumer,
)
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from tests.application.learning_session.helpers import make_journey, make_objective

FIXED = datetime(2026, 7, 30, 12, 0, tzinfo=UTC)


def _flags_twin(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        "SR_SESSION_SUBSTANCE": "1",
        "SR_EVIDENCE_GATE": "1",
        "SR_TWIN_DAILY_LOOP": "1",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _obs(
    type_id: RuntimeEvidenceType,
    *,
    student_id: str = "42",
    session_id: str = "lsr-sdt-1",
    observation_id: str | None = None,
    payload: dict | None = None,
) -> CandidateObservation:
    return CandidateObservation.create(
        observation_id=observation_id or f"obs-{type_id.value}",
        type_id=type_id,
        student_id=student_id,
        session_id=session_id,
        topic_id="topic-cash",
        mission_instance_id="m-1",
        recorded_at=FIXED,
        payload=payload,
    )


def _validated_package(
    *types: RuntimeEvidenceType,
    finish: str = "yes",
    payloads: dict[RuntimeEvidenceType, dict] | None = None,
) -> SessionEvidencePackage:
    observations = tuple(
        _obs(t, payload=(payloads or {}).get(t)) for t in types
    )
    package = SessionEvidencePackage.create(
        student_id="42",
        session_id="lsr-sdt-1",
        mission_instance_id="m-1",
        topic_id="topic-cash",
        topic_title="Cash flows",
        curriculum_identity="CS1:test",
        learning_objectives=("Explain operating cash flow",),
        observations=observations,
        finish_review_verdict=finish,
        created_at=FIXED,
    )
    validation = EducationalEvidenceAuthority.validate_session_evidence_package(
        package
    )
    return package.with_validation(validation)


def _consumer(*, twin_on: bool = True) -> tuple[
    SessionTwinEvidenceConsumer, DailyLoopTwinPersistence
]:
    store = SessionDocumentStore()
    twin_store = DailyLoopTwinPersistence(store=store)
    engine = StudentTwinEngine(clock=lambda: FIXED, id_factory=lambda: "fixed01")
    consumer = SessionTwinEvidenceConsumer(
        engine=engine,
        store=twin_store,
        clock=lambda: FIXED,
        id_factory=lambda: "fixed01",
        flag_resolver=lambda: _flags_twin()
        if twin_on
        else resolve_v2_feature_flags(
            environ={
                "SR_EVIDENCE_GATE": "1",
                "SR_TWIN_DAILY_LOOP": "0",
            }
        ),
    )
    return consumer, twin_store


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


def _active_engine(monkeypatch, *, twin: bool = True, gate: bool = True):
    monkeypatch.setenv("SR_EVIDENCE_GATE", "1" if gate else "0")
    monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
    monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
    monkeypatch.setenv("SR_TWIN_DAILY_LOOP", "1" if twin else "0")
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    lsr = LearningSessionRuntime()
    journey = make_journey(
        topic_id="topic-cash",
        objectives=[make_objective("obj-cash", topic_id="topic-cash")],
    )
    handle = lsr.create_session(journey, session_id="lsr-sdt-1")
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
    twin_store = DailyLoopTwinPersistence(store=store)
    twin_engine = StudentTwinEngine(clock=lambda: FIXED, id_factory=lambda: "eng01")
    consumer = SessionTwinEvidenceConsumer(
        engine=twin_engine,
        store=twin_store,
        clock=lambda: FIXED,
        flag_resolver=resolve_v2_feature_flags,
    )
    engine = LearningSessionRuntimeEngine(
        runtime=lsr,
        persistence=persistence,
        mission_completer=_FakeMissionCompleter(),
        twin_consumer=consumer,
    )
    return engine, persistence, twin_store


# ---------------------------------------------------------------------------
# Unit — consumer gates
# ---------------------------------------------------------------------------


class TestTwinEvidenceConsumer:
    def test_accepted_educational_updates_twin(self):
        consumer, twin_store = _consumer(twin_on=True)
        package = _validated_package(RuntimeEvidenceType.PRACTICE_CORRECT)
        assert package.validation is not None
        assert package.validation.may_update_twin is True
        result = consumer.consume(package)
        assert result.twin_updated is True
        assert result.reason == "accepted_educational_plus_consumed"
        assert result.events_ingested == 1
        assert result.twin_status == "active"
        assert "topic-cash" in (result.estimated_mastery or {})
        assert (result.estimated_mastery or {})["topic-cash"] > 0.0
        assert "topic-cash" in (result.estimated_knowledge or {})
        saved = twin_store.load_twin(learner_id="42", subject_code="CS1")
        assert saved is not None
        assert saved["status"] == "active"
        assert saved["event_count"] == 1

    def test_rejected_package_ignored(self):
        consumer, twin_store = _consumer(twin_on=True)
        package = _validated_package(RuntimeEvidenceType.READING_COMPLETED)
        assert package.validation.disposition == EvidenceDisposition.REJECTED
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "rejected_package"
        assert twin_store.load_twin(learner_id="42", subject_code="CS1") is None

    def test_behavioural_package_ignored(self):
        consumer, _ = _consumer(twin_on=True)
        package = _validated_package(
            RuntimeEvidenceType.READING_COMPLETED,
            RuntimeEvidenceType.PRACTICE_ATTEMPTED,
        )
        assert package.validation.disposition == (
            EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS
        )
        assert package.validation.may_update_twin is False
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "behavioural_package_ignored"

    def test_reading_only_ignored(self):
        consumer, _ = _consumer(twin_on=True)
        package = _validated_package(RuntimeEvidenceType.READING_COMPLETED)
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "rejected_package"

    def test_reflection_only_ignored(self):
        consumer, _ = _consumer(twin_on=True)
        package = _validated_package(RuntimeEvidenceType.REFLECTION_SUBMITTED)
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "rejected_package"

    def test_informational_duration_ignored(self):
        consumer, _ = _consumer(twin_on=True)
        package = _validated_package(RuntimeEvidenceType.SESSION_DURATION)
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "rejected_package"

    def test_flag_off_ignores_accepted_educational(self):
        consumer, twin_store = _consumer(twin_on=False)
        package = _validated_package(RuntimeEvidenceType.PRACTICE_CORRECT)
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "twin_daily_loop_flag_off"
        assert twin_store.load_twin(learner_id="42", subject_code="CS1") is None

    def test_incorrect_practice_updates_mastery_negatively(self):
        consumer, _ = _consumer(twin_on=True)
        package = _validated_package(RuntimeEvidenceType.PRACTICE_INCORRECT)
        result = consumer.consume(package)
        assert result.twin_updated is True
        # Negative polarity → mastery stays at floor 0.0 after one incorrect.
        assert (result.estimated_mastery or {}).get("topic-cash", 0.0) == 0.0

    def test_estimates_reproducible(self):
        package = _validated_package(RuntimeEvidenceType.PRACTICE_CORRECT)
        a, store_a = _consumer(twin_on=True)
        b, store_b = _consumer(twin_on=True)
        ra = a.consume(package)
        rb = b.consume(package)
        assert ra.estimated_mastery == rb.estimated_mastery
        assert ra.estimated_knowledge == rb.estimated_knowledge
        assert ra.overall_mastery == rb.overall_mastery
        decoded_a = decode_daily_loop_twin(
            store_a.load_twin(learner_id="42", subject_code="CS1"),
            engine=StudentTwinEngine(clock=lambda: FIXED),
        )
        decoded_b = decode_daily_loop_twin(
            store_b.load_twin(learner_id="42", subject_code="CS1"),
            engine=StudentTwinEngine(clock=lambda: FIXED),
        )
        assert decoded_a is not None and decoded_b is not None
        twin_a, _ = decoded_a
        twin_b, _ = decoded_b
        assert encode_daily_loop_twin(twin_a)["estimated_mastery"] == (
            encode_daily_loop_twin(twin_b)["estimated_mastery"]
        )

    def test_consumer_does_not_revalidate_authority(self):
        """Twin trusts may_update_twin; it is not a second Evidence Authority."""
        consumer, _ = _consumer(twin_on=True)
        # Forge a Rejected package that somehow claims may_update_twin — still
        # ignored because disposition Rejected is checked first.
        package = _validated_package(RuntimeEvidenceType.READING_COMPLETED)
        assert package.validation.disposition == EvidenceDisposition.REJECTED
        result = consumer.consume(package)
        assert result.twin_updated is False
        assert result.reason == "rejected_package"


# ---------------------------------------------------------------------------
# Authority — Educational+ column
# ---------------------------------------------------------------------------


class TestAuthorityTwinColumn:
    def test_educational_may_update_twin(self):
        package = _validated_package(RuntimeEvidenceType.PRACTICE_CORRECT)
        assert package.validation.may_update_twin is True
        assert package.validation.highest_grade == "educational"

    def test_behavioural_may_not_update_twin(self):
        package = _validated_package(RuntimeEvidenceType.PRACTICE_ATTEMPTED)
        assert package.validation.may_update_twin is False

    def test_structured_question_may_update_twin(self):
        package = _validated_package(
            RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS,
            payloads={
                RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS: {
                    "score": 0.8,
                    "outcome": "correct",
                }
            },
        )
        assert package.validation.may_update_twin is True


# ---------------------------------------------------------------------------
# Integration — session complete path
# ---------------------------------------------------------------------------


class TestTwinSessionIntegration:
    def test_scored_practice_updates_twin_and_progress(self, monkeypatch):
        engine, persistence, twin_store = _active_engine(monkeypatch, twin=True)
        # Inject Educational+ candidate (scored practice).
        obs = CandidateObservation.create(
            observation_id="obs-correct-1",
            type_id=RuntimeEvidenceType.PRACTICE_CORRECT,
            student_id="42",
            session_id="lsr-sdt-1",
            topic_id="topic-cash",
            mission_instance_id="m-1",
            recorded_at=FIXED,
        )
        persistence.append_candidate(
            session_id="lsr-sdt-1", observation=obs.to_opaque()
        )
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-sdt-1",
            finish_verdict="yes",
        )
        assert result["status"] == "completed"
        assert result["mission_completed"] is True
        assert result["progress_advanced"] is True
        assert result["twin_updated"] is True
        saved = twin_store.load_twin(learner_id="42", subject_code="CS1")
        assert saved is not None
        assert saved["event_count"] >= 1
        package = persistence.load_evidence_package(session_id="lsr-sdt-1")
        assert package is not None
        assert package.get("twin_updated") is True
        assert package.get("lifecycle_state") == "consumed"

    def test_behavioural_practice_progress_without_twin(self, monkeypatch):
        engine, _, twin_store = _active_engine(monkeypatch, twin=True)
        engine.record_response_opaque(
            "42",
            session_id="lsr-sdt-1",
            activity_id="act-practice-1",
            response="working capital answer",
        )
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-sdt-1",
            finish_verdict="yes",
        )
        assert result["status"] == "completed"
        assert result["mission_completed"] is True
        assert result["progress_advanced"] is True
        assert result["twin_updated"] is False
        assert twin_store.load_twin(learner_id="42", subject_code="CS1") is None

    def test_reading_only_blocks_and_no_twin(self, monkeypatch):
        engine, persistence, twin_store = _active_engine(monkeypatch, twin=True)
        obs = CandidateObservation.create(
            observation_id="obs-read-1",
            type_id=RuntimeEvidenceType.READING_COMPLETED,
            student_id="42",
            session_id="lsr-sdt-1",
            topic_id="topic-cash",
            recorded_at=FIXED,
        )
        persistence.append_candidate(
            session_id="lsr-sdt-1", observation=obs.to_opaque()
        )
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-sdt-1",
            finish_verdict="yes",
        )
        assert result["status"] == "error"
        assert result["error"] == "evidence_gate_rejected"
        assert result["twin_updated"] is False
        assert result["progress_advanced"] is False
        assert twin_store.load_twin(learner_id="42", subject_code="CS1") is None

    def test_twin_flag_off_keeps_progress_path(self, monkeypatch):
        engine, _, twin_store = _active_engine(monkeypatch, twin=False)
        obs = CandidateObservation.create(
            observation_id="obs-correct-2",
            type_id=RuntimeEvidenceType.PRACTICE_CORRECT,
            student_id="42",
            session_id="lsr-sdt-1",
            topic_id="topic-cash",
            mission_instance_id="m-1",
            recorded_at=FIXED,
        )
        engine.persistence.append_candidate(
            session_id="lsr-sdt-1", observation=obs.to_opaque()
        )
        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-sdt-1",
            finish_verdict="yes",
        )
        assert result["mission_completed"] is True
        assert result["progress_advanced"] is True
        assert result["twin_updated"] is False
        assert twin_store.load_twin(learner_id="42", subject_code="CS1") is None


# ---------------------------------------------------------------------------
# Acceptance — G-Twin flag
# ---------------------------------------------------------------------------


class TestAcceptanceGTwin:
    def test_flag_defaults_off(self):
        flags = resolve_v2_feature_flags(environ={})
        assert flags.SR_TWIN_DAILY_LOOP is False

    def test_flag_enables(self):
        flags = _flags_twin()
        assert flags.SR_TWIN_DAILY_LOOP is True
        assert flags.SR_EVIDENCE_GATE is True

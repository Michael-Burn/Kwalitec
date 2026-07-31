"""KWP-004 — Assessable Practice Activation tests.

Scoreable schema, deterministic scoring, EV-RT-07/08/40 emission,
Accepted Educational+ from a normal commercial Session, feedback fields,
and founder Learning Yield metrics. No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
)
from app.application.learning_session.evidence_package_builder import (
    EvidencePackageBuilder,
)
from app.application.learning_session.scoreable_practice import (
    AnswerKey,
    MarkScheme,
    PracticeResponseType,
    ScoreablePracticeItem,
    score_practice_response,
)
from app.application.learning_session.scoreable_seed import items_for_topic
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from app.services.educational_yield_metrics import EducationalYieldMetrics
from tests.application.learning_session.helpers import make_journey, make_objective

SESSION_BODY = Path("app/templates/session/partials/session_body.html")


# ---------------------------------------------------------------------------
# P0 — Content schema + deterministic scoring
# ---------------------------------------------------------------------------


class TestScoreableSchemaAndScoring:
    def test_mcq_scores_correct_and_incorrect(self):
        item = ScoreablePracticeItem(
            item_id="t-mcq",
            prompt="Pick A",
            response_type=PracticeResponseType.MCQ,
            answer_key=AnswerKey(accepted=("a",), correct_choice_id="a"),
            explanation="Because A.",
            model_answer="A",
            common_mistake="Choosing B",
            next_action="Continue",
            choices=(("a", "Alpha"), ("b", "Beta")),
            emit_structured=True,
        )
        ok = score_practice_response(item, "a")
        assert ok.scored is True
        assert ok.correct is True
        assert ok.feedback_outcome == "Correct"
        assert ok.emit_structured is True
        bad = score_practice_response(item, "b")
        assert bad.correct is False
        assert bad.feedback_outcome == "Incorrect"
        assert bad.common_mistake == "Choosing B"
        assert bad.model_answer == "A"

    def test_numeric_tolerance(self):
        item = ScoreablePracticeItem(
            item_id="t-num",
            prompt="PV?",
            response_type=PracticeResponseType.NUMERIC,
            answer_key=AnswerKey(accepted=("95.24",), numeric_tolerance=0.5),
            explanation="100/1.05",
            model_answer="95.24",
            mark_scheme=MarkScheme(max_marks=1),
            emit_structured=True,
        )
        assert score_practice_response(item, "95").correct is True
        assert score_practice_response(item, "90").correct is False

    def test_short_structured_variant_match(self):
        item = ScoreablePracticeItem(
            item_id="t-short",
            prompt="Define OCF",
            response_type=PracticeResponseType.SHORT_STRUCTURED,
            answer_key=AnswerKey(
                accepted=("cash from operating activities", "core trading")
            ),
            explanation="OCF is core operations cash.",
            model_answer="Cash from operating activities.",
        )
        result = score_practice_response(
            item, "Cash from operating activities of the firm"
        )
        assert result.scored is True
        assert result.correct is True

    def test_missing_key_is_unscored(self):
        result = score_practice_response(None, "anything")
        assert result.scored is False
        assert result.scored_correct is None
        assert "Not yet scored" in result.feedback_outcome


class TestSeedAndPlanner:
    def test_cash_flow_seed_items(self):
        items = items_for_topic(topic_title="Cash flows", limit=3)
        assert len(items) >= 1
        assert all(
            i.answer_key.accepted or i.answer_key.correct_choice_id for i in items
        )
        assert all(i.model_answer and i.explanation for i in items)

    def test_planner_emits_scoreable_practice(self):
        substance = EducationalSubstancePlanner()._plan_from_mission_facts(
            curriculum_identity="CS1:test",
            topic_id="topic-cash",
            topic_title="Cash flows",
            task_descriptions=("Explain operating cash flow",),
            educational_rationale="Cash flows matter.",
            objective_ids=("lo-1",),
        )
        assert substance is not None
        practice = [a for a in substance.activities if a.stage.value == "practice"]
        assert practice
        assert all(a.is_scoreable for a in practice)
        assert practice[0].scoreable is not None
        assert practice[0].scoreable.model_answer


# ---------------------------------------------------------------------------
# P1 — Evidence emission via existing builder / runtime
# ---------------------------------------------------------------------------


class TestEvidenceEmission:
    def test_builder_emits_07_08(self):
        builder = EvidencePackageBuilder(id_factory=lambda: "x")
        correct = builder.observation_for_stage_response(
            stage="practice",
            student_id="1",
            session_id="s1",
            response="ok",
            scored_correct=True,
        )
        incorrect = builder.observation_for_stage_response(
            stage="practice",
            student_id="1",
            session_id="s1",
            response="no",
            scored_correct=False,
        )
        assert correct.type_id == RuntimeEvidenceType.PRACTICE_CORRECT
        assert incorrect.type_id == RuntimeEvidenceType.PRACTICE_INCORRECT

    def test_builder_emits_40_for_structured(self):
        builder = EvidencePackageBuilder(id_factory=lambda: "y")
        obs = builder.observation_for_stage_response(
            stage="practice",
            student_id="1",
            session_id="s1",
            response="a",
            scored_correct=True,
            structured=True,
            score_payload={"item_id": "cs1-cash-mcq-1", "accuracy": 1.0},
        )
        assert obs.type_id == RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS
        assert obs.payload["scored_correct"] is True
        assert obs.payload["accuracy"] == 1.0

    def test_activity_engine_scores_and_returns_feedback(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        planner = EducationalSubstancePlanner()
        substance = planner._plan_from_mission_facts(
            curriculum_identity="CS1:test",
            topic_id="topic-cash",
            topic_title="Cash flows",
            task_descriptions=("Explain OCF",),
            educational_rationale="",
            objective_ids=("lo-1",),
        )
        engine = PackageActivityEngine(store=store, persistence=persistence)
        engine.provision_sequence("stu", session_id="s-score", substance=substance)
        # Advance past read (+ optional example) to first practice.
        current = engine.get_current_activity_opaque("stu", session_id="s-score")
        while current and current.get("stage") != "practice":
            engine.submit_response_opaque(
                "stu",
                session_id="s-score",
                activity_id=current["activity_id"],
                response="noted",
            )
            current = engine.advance_activity_opaque("stu", session_id="s-score")
        assert current is not None
        assert current["stage"] == "practice"
        # Cash MCQ correct choice.
        result = engine.submit_response_opaque(
            "stu",
            session_id="s-score",
            activity_id=current["activity_id"],
            response="a",
        )
        assert result["scored_correct"] is True
        assert result["feedback_outcome"] == "Correct"
        assert result["model_answer"]
        assert result["feedback_explanation"]


class TestCommercialSessionEducationalPlus:
    def test_scored_session_accepts_educational_plus(self, monkeypatch):
        monkeypatch.setenv("SR_EVIDENCE_GATE", "1")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
        monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
        monkeypatch.setenv("SR_TWIN_DAILY_LOOP", "0")

        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        from app.application.learning_session.runtime import LearningSessionRuntime

        lsr = LearningSessionRuntime()
        journey = make_journey(
            topic_id="topic-cash",
            objectives=[make_objective("obj-cash", topic_id="topic-cash")],
        )
        handle = lsr.create_session(journey, session_id="lsr-kwp4")
        handle = lsr.prepare_session(handle)
        handle = lsr.start_session(handle)
        persistence.save_binding(
            student_id="42",
            mission_instance_id="m-kwp4",
            handle=handle,
            topic_title="Cash flows",
            topic_id="topic-cash",
            curriculum_identity="CS1:test",
        )
        substance = EducationalSubstancePlanner()._plan_from_mission_facts(
            curriculum_identity="CS1:test",
            topic_id="topic-cash",
            topic_title="Cash flows",
            task_descriptions=("Explain operating cash flow",),
            educational_rationale="Cash flows matter.",
            objective_ids=("lo-1",),
        )
        PackageActivityEngine(store=store, persistence=persistence).provision_sequence(
            "42", session_id="lsr-kwp4", substance=substance
        )

        class _FakeMissionCompleter:
            def __init__(self) -> None:
                self.calls: list[dict] = []

            def complete_mission(self, **kwargs):
                self.calls.append(kwargs)
                return {"mission_completed": True}

        engine = LearningSessionRuntimeEngine(
            runtime=lsr,
            persistence=persistence,
            mission_completer=_FakeMissionCompleter(),
        )
        engine.begin_session_opaque("42", session_id="lsr-kwp4")

        # Emit Educational+ practice via scored_correct (activity layer result).
        recorded = engine.record_response_opaque(
            "42",
            session_id="lsr-kwp4",
            activity_id="act-practice-1",
            response="operating activities",
            scored_correct=True,
            structured=True,
            score_payload={"item_id": "cs1-cash-mcq-1", "accuracy": 1.0},
        )
        assert recorded["evidence_emitted"] is True
        assert recorded["evidence_type"] in {
            RuntimeEvidenceType.PRACTICE_CORRECT.value,
            RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS.value,
        }

        result = engine.complete_session_opaque(
            "42",
            session_id="lsr-kwp4",
            finish_verdict="yes",
        )
        assert result is not None
        assert result["evidence_disposition"] == EvidenceDisposition.ACCEPTED.value
        assert result["mission_completed"] is True
        assert result["progress_advanced"] is True

        package = persistence.load_evidence_package(session_id="lsr-kwp4")
        assert package is not None
        validation = EducationalEvidenceAuthority.validate_session_evidence_package(
            __import__(
                "app.application.learning_session.dto.evidence_package",
                fromlist=["SessionEvidencePackage"],
            ).SessionEvidencePackage.from_opaque(package)
        )
        assert validation.disposition == EvidenceDisposition.ACCEPTED
        assert validation.may_update_twin is True
        assert validation.highest_grade in {"educational", "mastery"}


# ---------------------------------------------------------------------------
# P2 — Student feedback surface
# ---------------------------------------------------------------------------


class TestStudentFeedbackSurface:
    def test_session_body_has_model_answer_and_common_mistake(self):
        text = SESSION_BODY.read_text(encoding="utf-8")
        assert "model_answer" in text
        assert "common_mistake" in text
        assert "feedback_next_action" in text
        assert "Model answer" in text
        assert "Common mistake" in text


# ---------------------------------------------------------------------------
# P3 — Founder metrics
# ---------------------------------------------------------------------------


class TestFounderEducationalYield:
    def test_learning_yield_from_packages(self):
        packages = [
            {
                "validation": {
                    "disposition": EvidenceDisposition.ACCEPTED.value,
                    "may_update_twin": True,
                },
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS.value},
                ],
                "twin_status": "active",
            },
            {
                "validation": {
                    "disposition": EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS.value,
                    "may_update_twin": False,
                },
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_ATTEMPTED.value},
                ],
            },
        ]
        snap = EducationalYieldMetrics.from_packages(packages)
        assert snap.sittings_total == 2
        assert snap.educational_plus_accepted == 1
        assert snap.behavioural_only == 1
        assert snap.educational_plus_rate == 0.5
        assert snap.learning_yield == 1.0  # 2 edu obs / 2 sittings
        assert snap.educational_observations == 2
        assert snap.twin_updated_sittings == 1

    def test_commercial_loop_still_on(self):
        flags = resolve_v2_feature_flags(
            environ={"KWALITEC_COMMERCIAL_LOOP": "1"}
        )
        assert flags.SR_SESSION_SUBSTANCE is True
        assert flags.SR_EVIDENCE_GATE is True

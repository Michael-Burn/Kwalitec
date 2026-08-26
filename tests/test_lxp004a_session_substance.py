"""LXP-004A — Educational Session Substance (SR-001A Phase P3 foundation).

Unit / integration / regression / acceptance coverage for:
package-derived Read → Practice → Reflect flow, learning objectives,
no Core methods when substance ON, no Twin / mission completion.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.educational_flow import (
    ACTIVITY_STAGES,
    SESSION_EDUCATIONAL_FLOW,
    EducationalStage,
    stage_label,
)
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
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
from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.models.user import User
from tests.application.learning_session.helpers import make_journey, make_objective
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def _flags_substance(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        "SR_SESSION_SUBSTANCE": "1",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _flags_substance_off(**extra: str):
    env = {
        "SR_SESSION_PRIMARY": "1",
        "SR_SESSION_COMPLETION_PRODUCT": "1",
        "SR_SESSION_SUBSTANCE": "0",
        **extra,
    }
    return resolve_v2_feature_flags(environ=env)


def _enrol_runtime_c(user: User, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


def _login(client, user: User) -> None:
    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True


# ---------------------------------------------------------------------------
# Unit — educational flow + substance planner
# ---------------------------------------------------------------------------


class TestEducationalFlow:
    def test_session_flow_is_continuous(self):
        assert SESSION_EDUCATIONAL_FLOW == (
            EducationalStage.LEARNING_OBJECTIVES,
            EducationalStage.READ,
            EducationalStage.WORKED_EXAMPLE,
            EducationalStage.PRACTICE,
            EducationalStage.REFLECTION,
            EducationalStage.READY_TO_FINISH,
        )

    def test_activity_stages_exclude_reflection(self):
        assert EducationalStage.REFLECTION not in ACTIVITY_STAGES
        assert EducationalStage.READ in ACTIVITY_STAGES

    def test_stage_labels(self):
        assert stage_label(EducationalStage.READ) == "Reading"
        assert stage_label("worked_example") == "Worked example"


class TestSubstancePlanner:
    def test_plan_from_package_includes_read_example_practice(self):
        planner = EducationalSubstancePlanner()
        substance = planner._plan_from_mission_facts(
            curriculum_identity="CS1:lxp004a-test",
            topic_id="topic-cash",
            topic_title="Cash flows",
            task_descriptions=(
                "Study Cash flows",
                "Work through objective 1.1.1: Explain operating cash flow components",
            ),
            educational_rationale="Cash flows matter for examination readiness.",
            objective_ids=("lo-1", "lo-2"),
        )
        assert substance is not None
        stages = [a.stage for a in substance.activities]
        assert EducationalStage.READ in stages
        assert EducationalStage.WORKED_EXAMPLE in stages
        assert EducationalStage.PRACTICE in stages
        assert stages.index(EducationalStage.READ) < stages.index(
            EducationalStage.PRACTICE
        )
        assert "Core methods" not in substance.topic_title
        assert all("Core methods" not in a.prompt for a in substance.activities)
        assert substance.learning_objectives
        lead_text = substance.learning_objectives[0].text
        assert (
            "Explain operating cash flow" in lead_text
            or "Study Cash flows" in lead_text
        )

    def test_plan_requires_topic_signal(self):
        planner = EducationalSubstancePlanner()
        assert (
            planner._plan_from_mission_facts(
                curriculum_identity="",
                topic_id="",
                topic_title="",
                task_descriptions=(),
                educational_rationale="",
                objective_ids=(),
            )
            is None
        )


class TestPackageActivityEngine:
    def test_resolves_continuous_sequence_without_core_methods(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        from app.application.learning_session.runtime import LearningSessionRuntime
        from tests.application.learning_session.helpers import make_journey

        lsr = LearningSessionRuntime()
        journey = make_journey(
            topic_id="topic-cash",
            objectives=[make_objective("obj-cash", topic_id="topic-cash")],
        )
        handle = lsr.create_session(journey, session_id="lsr-sub-1")
        handle = lsr.prepare_session(handle)
        handle = lsr.start_session(handle)
        persistence.save_binding(
            student_id="stu-1",
            mission_instance_id="m-1",
            handle=handle,
            topic_title="Cash flows",
            topic_id="topic-cash",
            curriculum_identity="CS1:lxp004a-test",
        )

        planner = EducationalSubstancePlanner()
        substance = planner._plan_from_mission_facts(
            curriculum_identity="CS1:lxp004a-test",
            topic_id="topic-cash",
            topic_title="Cash flows",
            task_descriptions=("Study Cash flows", "Apply cash flow classification"),
            educational_rationale="Cash flows support examination readiness.",
            objective_ids=("lo-1",),
        )
        engine = PackageActivityEngine(store=store, persistence=persistence)
        engine.provision_sequence("stu-1", session_id="lsr-sub-1", substance=substance)

        adapter = SessionActivityAdapter(store=store, activity_engine=engine)
        seen_stages: list[str] = []
        current = adapter.get_current_activity("stu-1", session_id="lsr-sub-1")
        assert current is not None
        assert "Core methods" not in str(current)
        assert current.get("substance") == "package"

        while current is not None:
            stage = str(current.get("stage") or current.get("activity_type") or "")
            seen_stages.append(stage)
            assert "Core methods" not in str(current.get("question") or "")
            assert "Core methods" not in str(current.get("context") or "")
            submitted = adapter.submit_response(
                "stu-1",
                session_id="lsr-sub-1",
                activity_id=str(current["activity_id"]),
                response=f"notes for {stage}",
            )
            assert submitted.get("twin_updated") is not True
            # RC2 Sprint C: explanation must survive reload so UI shows Continue.
            assert submitted.get("explanation") or submitted.get("feedback_outcome")
            reloaded = adapter.get_current_activity("stu-1", session_id="lsr-sub-1")
            assert reloaded is not None
            assert reloaded.get("activity_id") == current["activity_id"]
            assert reloaded.get("explanation") or reloaded.get("feedback_outcome")
            current = adapter.advance_activity("stu-1", session_id="lsr-sub-1")

        assert seen_stages[0] == EducationalStage.READ.value
        assert EducationalStage.PRACTICE.value in seen_stages
        assert seen_stages.index(EducationalStage.READ.value) < seen_stages.index(
            EducationalStage.PRACTICE.value
        )

    def test_defaults_not_selected_when_package_sequence_present(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        planner = EducationalSubstancePlanner()
        substance = planner._plan_from_mission_facts(
            curriculum_identity="CS1:x",
            topic_id="t1",
            topic_title="Leases",
            task_descriptions=("Study leases",),
            educational_rationale="Leases are syllabus-bound.",
            objective_ids=("lo-a",),
        )
        engine = PackageActivityEngine(store=store, persistence=persistence)
        engine.provision_sequence("stu-2", session_id="sess-2", substance=substance)
        adapter = SessionActivityAdapter(store=store, activity_engine=engine)
        activity = adapter.get_current_activity("stu-2", session_id="sess-2")
        assert activity is not None
        assert activity["authority"] == PackageActivityEngine.ENGINE_ID
        assert "Core methods" not in activity["question"]
        assert activity["stage"] == EducationalStage.READ.value


class TestFlagMatrix:
    def test_substance_flag_defaults_off(self):
        flags = resolve_v2_feature_flags(environ={})
        assert flags.SR_SESSION_SUBSTANCE is False

    def test_substance_flag_on(self):
        flags = _flags_substance()
        assert flags.SR_SESSION_SUBSTANCE is True

    def test_substance_flag_off_rollback(self):
        flags = _flags_substance_off()
        assert flags.SR_SESSION_SUBSTANCE is False


# ---------------------------------------------------------------------------
# Integration — runtime overview + reflection
# ---------------------------------------------------------------------------


class TestRuntimeSubstanceProjection:
    def test_overview_and_reflection_when_substance_on(self, monkeypatch):
        monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        monkeypatch.setenv("KWALITEC_COMMERCIAL_LOOP", "0")
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        from app.application.learning_session.runtime import LearningSessionRuntime
        from tests.application.learning_session.helpers import make_journey

        lsr = LearningSessionRuntime()
        journey = make_journey(
            topic_id="topic-cash",
            objectives=[make_objective("obj-cash", topic_id="topic-cash")],
        )
        handle = lsr.create_session(journey, session_id="lsr-ov-1")
        handle = lsr.prepare_session(handle)
        handle = lsr.start_session(handle)
        persistence.save_binding(
            student_id="stu-ov",
            mission_instance_id="m-ov",
            handle=handle,
            topic_title="Cash flows",
            topic_id="topic-cash",
            curriculum_identity="CS1:lxp004a-test",
        )
        planner = EducationalSubstancePlanner()
        substance = planner._plan_from_mission_facts(
            curriculum_identity="CS1:lxp004a-test",
            topic_id="topic-cash",
            topic_title="Cash flows",
            task_descriptions=("Explain operating cash flow components",),
            educational_rationale="Cash flows matter.",
            objective_ids=("lo-1",),
        )
        PackageActivityEngine(store=store, persistence=persistence).provision_sequence(
            "stu-ov", session_id="lsr-ov-1", substance=substance
        )
        engine = LearningSessionRuntimeEngine(persistence=persistence)
        overview = engine.get_session_overview_opaque("stu-ov", session_id="lsr-ov-1")
        assert overview is not None
        assert overview["substance"] in {"package", "educational_package"}
        assert "Core methods" not in str(overview)
        assert overview["learning_objectives"]
        reflection = engine.get_reflection_opaque("stu-ov", session_id="lsr-ov-1")
        assert reflection is not None
        assert reflection["substance"] in {"package", "educational_package"}
        assert reflection["twin_updated"] is False
        assert reflection.get("skip_available") is True
        recorded = engine.record_response_opaque(
            "stu-ov",
            session_id="lsr-ov-1",
            activity_id="act-read-1",
            response="cash from operations",
        )
        assert recorded["evidence_emitted"] is False
        assert recorded["twin_updated"] is False


# ---------------------------------------------------------------------------
# Regression — reflection alone does not update Twin / mission
# ---------------------------------------------------------------------------


class TestNoTwinFromReflection:
    def test_reflection_note_does_not_write_journal_or_twin(self, monkeypatch):
        monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        from app.application.learning_session.runtime import LearningSessionRuntime
        from tests.application.learning_session.helpers import make_journey

        lsr = LearningSessionRuntime()
        journey = make_journey()
        handle = lsr.create_session(journey, session_id="lsr-ref-1")
        handle = lsr.prepare_session(handle)
        handle = lsr.start_session(handle)
        persistence.save_binding(
            student_id="stu-ref",
            mission_instance_id="m-ref",
            handle=handle,
            topic_title="Cash flows",
            topic_id="topic-cash",
        )
        engine = LearningSessionRuntimeEngine(persistence=persistence)
        note = engine.record_reflection_note_opaque(
            "stu-ref", session_id="lsr-ref-1", note="I need more practice"
        )
        assert note["journal_written"] is False
        assert note["twin_updated"] is False
        complete = engine.complete_session_opaque(
            "stu-ref",
            session_id="lsr-ref-1",
            finish_verdict="yes",
            finish_notes="",
        )
        assert complete is not None
        assert complete["mission_completed"] is False
        assert complete["progress_advanced"] is False

    def test_reflection_note_text_round_trips_on_live_engine_path(self, monkeypatch):
        """Live engine must persist the actual note text (not only note_length)."""
        monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        from app.application.learning_session.runtime import LearningSessionRuntime

        lsr = LearningSessionRuntime()
        journey = make_journey()
        handle = lsr.create_session(journey, session_id="lsr-ref-rt")
        handle = lsr.prepare_session(handle)
        handle = lsr.start_session(handle)
        persistence.save_binding(
            student_id="stu-ref-rt",
            mission_instance_id="m-ref-rt",
            handle=handle,
            topic_title="Deferred tax",
            topic_id="topic-tax",
        )
        engine = LearningSessionRuntimeEngine(persistence=persistence)
        text = "I still find deferred tax tricky — need another pass."
        recorded = engine.record_reflection_note_opaque(
            "stu-ref-rt", session_id="lsr-ref-rt", note=text
        )
        assert recorded["student_note"] == text

        loaded = persistence.load(session_id="lsr-ref-rt")
        assert loaded is not None
        assert loaded["reflection_note"] == text

        reflection = engine.get_reflection_opaque(
            "stu-ref-rt", session_id="lsr-ref-rt"
        )
        assert reflection is not None
        assert reflection["student_note"] == text

        summary = engine.get_completion_summary_opaque(
            "stu-ref-rt", session_id="lsr-ref-rt"
        )
        assert summary is not None
        assert summary["reflection_note"] == text


# ---------------------------------------------------------------------------
# Acceptance — published CS1 path has no Core methods (when substance ON)
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("app", "db")
class TestPublishedSubstanceAcceptance:
    def test_start_session_provisions_package_sequence(self, app, client, db, ctx):
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "1")
        monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
        try:
            subject = publish_subject("CS1")
            user = make_user(email="lxp004a@example.com")
            db.session.add(user)
            db.session.commit()
            _enrol_runtime_c(user, subject)
            _login(client, user)

            flags = resolve_v2_feature_flags()
            assert flags.SR_SESSION_SUBSTANCE is True

            # Direct provision path mirrors coordinator substance wiring.
            store = SessionDocumentStore()
            persistence = LearningSessionPersistenceAdapter(store=store)
            from app.application.learning_session.runtime import LearningSessionRuntime

            lsr = LearningSessionRuntime()
            journey = make_journey(
                topic_id="topic-a",
                objectives=[make_objective(topic_id="topic-a")],
            )
            handle = lsr.create_session(journey, session_id="lsr-acc-1")
            handle = lsr.prepare_session(handle)
            handle = lsr.start_session(handle)
            persistence.save_binding(
                student_id=str(user.id),
                mission_instance_id="m-acc",
                handle=handle,
                topic_title="Cash flows",
                topic_id="topic-a",
                curriculum_identity=f"{subject}:1.0.0",
            )
            substance = EducationalSubstancePlanner()._plan_from_mission_facts(
                curriculum_identity=f"{subject}:1.0.0",
                topic_id="topic-a",
                topic_title="Cash flows",
                task_descriptions=("Explain operating cash flow components",),
                educational_rationale="Syllabus-bound cash flow study.",
                objective_ids=("lo-1",),
            )
            PackageActivityEngine(
                store=store, persistence=persistence
            ).provision_sequence(
                str(user.id), session_id="lsr-acc-1", substance=substance
            )
            engine = LearningSessionRuntimeEngine(persistence=persistence)
            overview = engine.get_session_overview_opaque(
                str(user.id), session_id="lsr-acc-1"
            )
            assert overview is not None
            assert overview["substance"] == "package"
            assert "Core methods" not in str(overview)
            assert overview["learning_objectives"]
            activity = PackageActivityEngine(
                store=store, persistence=persistence
            ).get_current_activity_opaque(str(user.id), session_id="lsr-acc-1")
            assert activity is not None
            assert activity["stage"] == EducationalStage.READ.value
            assert "Core methods" not in activity["question"]
        finally:
            monkeypatch.undo()


# ---------------------------------------------------------------------------
# Composition — opaque Phase-I must not win over Session Primary
# ---------------------------------------------------------------------------


class TestCompositionPrefersLearningSessionRuntime:
    def test_session_primary_beats_opaque_core_methods_bridge(self, ctx):
        """Durable-store Phase-I inject must not replace CMP sessions."""
        from app.infrastructure.adapters.learning_session.runtime_engine import (
            LearningSessionRuntimeEngine as LSREngine,
        )
        from app.infrastructure.engines.opaque_bridges import (
            SessionRuntimeOpaqueBridge,
        )
        from app.infrastructure.session.composition import (
            build_production_session_experience,
        )

        flags = resolve_v2_feature_flags(
            environ={
                "KWALITEC_V2_DURABLE_STORE": "1",
                "INJECT_PHASE_I_ENGINES": "1",
                "SR_SESSION_PRIMARY": "1",
                "SR_SESSION_SUBSTANCE": "1",
            }
        )
        assert flags.INJECT_PHASE_I_ENGINES is True
        composition, _service = build_production_session_experience(
            flags=flags, seed_demo_learners=False
        )
        engine = composition.runtime._engine
        assert isinstance(engine, LSREngine)
        assert not isinstance(engine, SessionRuntimeOpaqueBridge)

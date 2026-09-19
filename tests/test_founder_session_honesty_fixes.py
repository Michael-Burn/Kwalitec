"""Founder first-sitting honesty fixes: streak store, duration, Home, messaging."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.learning_strategy.dto import (
    StrategyAction,
    StrategyEvidenceInput,
)
from app.application.learning_strategy.engine import LearningStrategyEngine
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.student_microcopy import (
    return_after_gap_copy,
)
from app.infrastructure.adapters.learner_progress import (
    qualifying_study_day_persistence as qsd_persist,
)
from app.infrastructure.adapters.learner_progress.query_adapter import (
    qualifying_study_day_query,
)
from app.infrastructure.adapters.learner_progress.shown_milestones_persistence import (
    NS_MILESTONES_SHOWN,
    MilestonesShownPersistence,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    _honest_duration_minutes,
)
from app.infrastructure.composition import build_session_document_store
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.session.sitting_report import build_sitting_report
from app.presentation.student.dto.student_home import HomeMission
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
    _mission_is_open_sitting_resume,
)
from app.presentation.student.view_models import (
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)
from tests.application.learning_session.helpers import make_journey


def _page(home_vm_obj) -> StudentPageViewModel:
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home_vm_obj,
    )


class TestStreakReadWriteStoreShare:
    def test_default_query_reads_what_write_path_persists(
        self, app, db, ctx, monkeypatch
    ):
        """Home/Stats reader must share the durable composition store."""
        # Production posture: durable SQL-backed SessionDocumentStore.
        monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")

        write_store = build_session_document_store()
        writer_index = qsd_persist.QualifyingStudyDayIndexPersistence(
            store=write_store
        )
        writer_index.save_index(
            learner_id="77",
            document={
                "learner_id": "77",
                "qualifying_dates": ["2026-09-19"],
                "longest_streak_days": 1,
            },
        )

        # Default factory (Home/Stats) must see the same durable document.
        query = qualifying_study_day_query()
        stats = query.streak_stats(
            user_id=77,
            as_of=datetime(2026, 9, 19, tzinfo=UTC).date(),
        )
        assert stats.current_streak_days >= 1
        assert datetime(2026, 9, 19, tzinfo=UTC).date() in stats.qualifying_dates

        # Bare in-memory store must remain empty (the old broken default).
        bare = SessionDocumentStore()
        assert bare.get(qsd_persist.NS_QUALIFYING_STUDY_DAYS, "77") is None

        # Default QualifyingStudyDayIndexPersistence uses composition store.
        durable_default = qsd_persist.QualifyingStudyDayIndexPersistence()
        assert durable_default.load_index(learner_id="77") is not None


class TestMilestonesShownReadWriteStoreShare:
    def test_default_reader_sees_what_write_path_persists(
        self, app, db, ctx, monkeypatch
    ):
        """Milestone announcements must share the durable composition store."""
        monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")

        write_store = build_session_document_store()
        writer = MilestonesShownPersistence(store=write_store)
        recorded = writer.record_shown(
            learner_id="88",
            milestone_id="first_qualifying_day",
            label="First qualifying study day",
            shown_at=datetime(2026, 9, 19, tzinfo=UTC).date(),
        )
        assert recorded is True

        # Default factory (Home/Stats HonestProgressService) must see it.
        default_reader = MilestonesShownPersistence()
        assert "first_qualifying_day" in default_reader.previously_shown_ids(
            learner_id="88"
        )
        assert default_reader.load_document(learner_id="88") is not None

        # Bare in-memory store must remain empty (the old broken default).
        bare = SessionDocumentStore()
        assert bare.get(NS_MILESTONES_SHOWN, "88") is None


class TestHonestSessionDuration:
    def test_duration_uses_wall_clock_not_estimate(self):
        accepted = datetime(2026, 9, 19, 12, 52, 22, tzinfo=UTC)
        complete = accepted + timedelta(minutes=120)
        measured = int(round((complete - accepted).total_seconds() / 60.0))
        record = {
            "estimated_minutes": 60,
            "accepted_at": accepted.isoformat(),
            "elapsed_active_seconds": 0,
            "actual_duration_minutes": measured,
        }
        minutes = _honest_duration_minutes(record)
        assert minutes == 120
        assert minutes != record["estimated_minutes"]

    def test_honest_duration_never_falls_back_to_estimate(self):
        assert (
            _honest_duration_minutes(
                {"estimated_minutes": 60, "elapsed_active_seconds": 0}
            )
            is None
        )

    def test_honest_duration_computes_from_accepted_at(self, monkeypatch):
        accepted = datetime(2026, 9, 19, 12, 52, 22, tzinfo=UTC)
        complete = accepted + timedelta(minutes=120)

        class _FrozenDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                if tz is None:
                    return complete.replace(tzinfo=None)
                return complete.astimezone(tz)

        monkeypatch.setattr(
            "app.infrastructure.adapters.learning_session.runtime_engine.datetime",
            _FrozenDateTime,
        )
        minutes = _honest_duration_minutes(
            {
                "estimated_minutes": 60,
                "accepted_at": accepted.isoformat(),
                "elapsed_active_seconds": 0,
            }
        )
        assert minutes == 120
        assert minutes != 60

    def test_persistence_stamps_accepted_at_and_records_actual(self, app, db):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(
            store=store, enable_qualifying_study_day_index=False
        )
        journey = make_journey()
        lsr = LearningSessionRuntime()
        handle = lsr.create_session(journey, session_id="lsr-duration-test")
        handle = lsr.prepare_session(handle)
        doc = persistence.save_binding(
            student_id="9",
            mission_instance_id="msn-duration",
            handle=handle,
            topic_title="Duration topic",
            estimated_minutes=45,
        )
        assert doc.get("accepted_at")
        assert doc.get("estimated_minutes") == 45

        updated = persistence.record_actual_duration_minutes(
            session_id="lsr-duration-test", duration_minutes=119
        )
        assert updated is not None
        assert updated["actual_duration_minutes"] == 119
        assert _honest_duration_minutes(updated) == 119
        assert _honest_duration_minutes(updated) != 45


class TestHomeOpenSittingHonesty:
    def test_day_complete_continuation_is_not_open_sitting(self):
        mission = HomeMission(
            subject_name="CS1",
            objective="Complete for today",
            status_label="Complete for today",
            why_now="",
            after_completion="",
            primary_label="Continue studying",
            primary_kind="link",
            primary_href="/student/study?continue_study=1",
            title="Complete for today",
            session_id="",
        )
        assert not _mission_is_open_sitting_resume(
            mission, state="day_complete"
        )
        copy = return_after_gap_copy(
            days_since_last=0,
            display_name="Founder",
            in_progress=_mission_is_open_sitting_resume(
                mission, state="day_complete"
            ),
        )
        assert copy.support_line is None

    def test_resume_with_session_id_is_open_sitting(self):
        mission = HomeMission(
            subject_name="CS1",
            objective="Continue your open session",
            status_label="In progress",
            why_now="",
            after_completion="",
            primary_label="Continue",
            primary_kind="link",
            primary_href="/session/lsr-abc/overview",
            title="Today's Session",
            session_id="lsr-abc",
        )
        assert _mission_is_open_sitting_resume(mission, state="mission")
        copy = return_after_gap_copy(days_since_last=0, in_progress=True)
        assert copy.support_line is not None
        assert "left a sitting open" in copy.support_line

    def test_day_complete_home_omits_left_open_message(self, app, ctx):
        home = home_vm(
            HomeSnapshot(
                student_id="1",
                examination_label="CS1 FR",
                has_recommendation=True,
                recommendation_title="Done",
                can_start_session=False,
            ),
            unified_journey=False,
        )
        home = replace(home, day_complete=True)
        with app.test_request_context("/student/"):
            page = StudentHomeService().build_home(_page(home))
        assert page.state == "day_complete"
        assert page.mission is not None
        assert page.mission.primary_kind == "link"
        assert not (page.mission.session_id or "").strip()
        assert "left a sitting open" not in (page.continuity_line or "").lower()


class TestCompletionMessagingCoverageHonesty:
    def test_advance_topic_only_when_coverage_advanced(self):
        engine = LearningStrategyEngine()
        advanced = engine.evaluate(
            StrategyEvidenceInput(
                topic_title="Present value",
                practice_correct=3,
                practice_attempted=3,
                finish_verdict="yes",
                progress_advanced=True,
                mission_completed=True,
                next_topic_title="Discount factors",
            )
        )
        assert advanced.action is StrategyAction.ADVANCE_TOPIC

        not_advanced = engine.evaluate(
            StrategyEvidenceInput(
                topic_title="Present value",
                practice_correct=3,
                practice_attempted=3,
                finish_verdict="yes",
                progress_advanced=False,
                mission_completed=True,
                next_topic_title="Discount factors",
            )
        )
        assert not_advanced.action is StrategyAction.MAINTAIN_CURRENT_PACE
        assert not_advanced.action is not StrategyAction.ADVANCE_TOPIC

    def test_sitting_report_titles_match_coverage_outcome(self):
        advancing = build_sitting_report(
            topic_title="Present value",
            opaque_summary={
                "learning_objectives": ("Discount cash flows to today",),
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_YES.value},
                ],
                "progress_advanced": True,
                "mission_completed": True,
                "finish_review": {"verdict": "yes"},
            },
            metadata={
                "progress_advanced": "true",
                "mission_completed": "true",
            },
            next_recommendation="Discount factors",
        )
        assert advancing.strategy_title == "Move to the next topic"

        staying = build_sitting_report(
            topic_title="Present value",
            opaque_summary={
                "learning_objectives": ("Discount cash flows to today",),
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_YES.value},
                ],
                "progress_advanced": False,
                "mission_completed": True,
                "finish_review": {"verdict": "yes"},
            },
            metadata={
                "progress_advanced": "false",
                "mission_completed": "true",
            },
            next_recommendation="Discount factors",
        )
        assert staying.strategy_title != "Move to the next topic"
        assert "pace" in staying.strategy_title.lower() or (
            "continue" in staying.strategy_title.lower()
        )

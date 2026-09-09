"""Due-review daily composer + MISSION_COMPLETED → Spacing Scheduler wiring."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

from app.application.educational_runtime_engine import EducationalRuntimeEngineService
from app.application.educational_runtime_engine.selection_reasons import (
    SELECTION_REASON_SEQUENTIAL,
    SELECTION_REASON_SPACED_REVIEW,
)
from app.application.spacing_scheduler import (
    SchedulingStatus,
    get_spacing_scheduler,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from app.presentation.student.services.student_home_service import StudentHomeService
from app.presentation.student.view_models import (
    EducationalExperienceViewModel,
    HomePageViewModel,
)
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)

PACKAGE_DUE = "FAKE-DUE-PACK"
PACKAGE_SEQ = "FAKE-SEQ-PACK"


class _Pack:
    def __init__(
        self,
        *,
        package_id: str,
        subject_id: str,
        topic_code: str = "1.1",
        mode: str = "learning",
        campaign_day: str = "D1",
        display_title: str = "Pack",
    ) -> None:
        self.package_id = package_id
        self.subject_id = subject_id
        self.topic_code = topic_code
        self.mode = mode
        self.campaign_day = campaign_day
        self.display_title = display_title
        self.task_descriptions = ("Read", "Practice")
        self.tomorrow = SimpleNamespace(next_topic_code="")


def _patch_packages(
    monkeypatch, *, subject: str, sequential: _Pack, due: _Pack
) -> None:
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: True,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: sequential,
    )

    def _find(pid: str):
        mapping = {
            sequential.package_id: sequential,
            due.package_id: due,
        }
        return mapping.get(pid)

    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        _find,
    )


def test_mission_completed_writes_durable_spacing_state(ctx, monkeypatch) -> None:
    """Part 1: real complete_mission populates canonical Spacing Scheduler state."""
    user = make_user("spacing-wire@example.com")
    subject = publish_subject("SPWIRE")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    seq = _Pack(package_id=PACKAGE_SEQ, subject_id=subject, display_title="Seq")
    due = _Pack(package_id=PACKAGE_DUE, subject_id=subject, display_title="Due")
    _patch_packages(monkeypatch, subject=subject, sequential=seq, due=due)

    day = date(2026, 9, 1)
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
    )
    assert mission.educational_package_id == PACKAGE_SEQ

    scheduler = get_spacing_scheduler()
    assert (
        scheduler.get_state(learner_id=str(user.id), package_id=PACKAGE_SEQ) is None
    )

    runtime.complete_mission(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
    )

    completed = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.MISSION_COMPLETED.value,
    ).all()
    assert completed
    payload = json.loads(completed[-1].payload_json or "{}")
    assert payload.get("educational_package_id") == PACKAGE_SEQ

    state = scheduler.get_state(learner_id=str(user.id), package_id=PACKAGE_SEQ)
    assert state is not None
    assert state.last_completed_on == day
    assert state.next_due_on == day + timedelta(days=1)
    assert state.current_interval_days == 1

    # Fresh facade still sees the same canonical process store (Twin-style
    # shared-authority proof for the in-process store).
    again = get_spacing_scheduler()
    assert again is scheduler
    assert again.get_state(learner_id=str(user.id), package_id=PACKAGE_SEQ) is not None
    decision = again.evaluate(
        learner_id=str(user.id),
        package_id=PACKAGE_SEQ,
        as_of=day + timedelta(days=1),
    )
    assert decision.status is SchedulingStatus.DUE
    assert decision.explanation


def test_nothing_due_keeps_sequential_composition(ctx, monkeypatch) -> None:
    """When scheduler has nothing due, composition matches sequential path."""
    user = make_user("seq-path@example.com")
    subject = publish_subject("SEQPATH")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    seq = _Pack(package_id=PACKAGE_SEQ, subject_id=subject, display_title="Seq")
    due = _Pack(package_id=PACKAGE_DUE, subject_id=subject, display_title="Due")
    _patch_packages(monkeypatch, subject=subject, sequential=seq, due=due)

    day = date(2026, 9, 2)
    spec = runtime.compute_daily_sitting_selection(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
    )
    assert spec.educational_package_id == PACKAGE_SEQ
    assert spec.composer_selection_reason == SELECTION_REASON_SEQUENTIAL
    assert spec.selection_explanation == ""

    mission = runtime.materialise_daily_mission_from_spec(spec)
    assert mission.educational_package_id == PACKAGE_SEQ
    assert mission.composer_selection_reason == SELECTION_REASON_SEQUENTIAL
    assert mission.selection_explanation == ""


def test_due_package_preempts_sequential_with_spaced_review_reason(
    ctx, monkeypatch
) -> None:
    """When scheduler shows due, today's mission is that review package."""
    user = make_user("due-path@example.com")
    subject = publish_subject("DUEPATH")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    seq = _Pack(
        package_id=PACKAGE_SEQ,
        subject_id=subject,
        topic_code="2.1",
        display_title="Sequential next",
    )
    due = _Pack(
        package_id=PACKAGE_DUE,
        subject_id=subject,
        topic_code="1.1",
        display_title="Due review pack",
    )
    _patch_packages(monkeypatch, subject=subject, sequential=seq, due=due)

    completed_on = date(2026, 9, 1)
    as_of = completed_on + timedelta(days=1)
    get_spacing_scheduler().record_completed_exposure(
        learner_id=str(user.id),
        package_id=PACKAGE_DUE,
        completed_on=completed_on,
    )
    board = get_spacing_scheduler().revision_board(
        learner_id=str(user.id), as_of=as_of
    )
    assert board.has_due
    assert board.due_now[0].package_id == PACKAGE_DUE
    expected_explanation = board.due_now[0].explanation

    spec = runtime.compute_daily_sitting_selection(
        user_id=user.id,
        subject_code=subject,
        mission_date=as_of,
    )
    assert spec.educational_package_id == PACKAGE_DUE
    assert spec.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW
    assert spec.selection_explanation == expected_explanation

    mission = runtime.materialise_daily_mission_from_spec(spec)
    assert mission.educational_package_id == PACKAGE_DUE
    assert mission.composer_selection_reason == SELECTION_REASON_SPACED_REVIEW
    assert mission.selection_explanation == expected_explanation
    assert mission.title == "Due review pack"


def test_daily_composer_reads_only_canonical_spacing_state() -> None:
    """Composer must not invent due dates; only read the scheduler facade."""
    source = Path(
        "app/application/educational_runtime_engine/service.py"
    ).read_text(encoding="utf-8")
    assert "get_spacing_scheduler" in source
    assert "revision_board" in source
    assert "_due_review_package_for_day" in source
    # No independent TopicProgress / MissionOptimizer due math in this service.
    assert "next_review_date" not in source
    assert "MissionOptimizer" not in source
    assert "get_topics_due_for_review" not in source


def test_spaced_review_mission_explains_why(ctx, monkeypatch) -> None:
    """Mission payload + Home why-now carry the scheduler explanation."""
    user = make_user("explain-due@example.com")
    subject = publish_subject("EXPLDUE")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    seq = _Pack(package_id=PACKAGE_SEQ, subject_id=subject)
    due = _Pack(package_id=PACKAGE_DUE, subject_id=subject, display_title="Review me")
    _patch_packages(monkeypatch, subject=subject, sequential=seq, due=due)

    completed_on = date(2026, 9, 3)
    as_of = completed_on + timedelta(days=1)
    get_spacing_scheduler().record_completed_exposure(
        learner_id=str(user.id),
        package_id=PACKAGE_DUE,
        completed_on=completed_on,
    )
    explanation = get_spacing_scheduler().explain(
        learner_id=str(user.id),
        package_id=PACKAGE_DUE,
        as_of=as_of,
    )
    assert "due" in explanation.lower()

    mission = runtime.materialise_daily_mission_from_spec(
        runtime.compute_daily_sitting_selection(
            user_id=user.id,
            subject_code=subject,
            mission_date=as_of,
        )
    )
    assert mission.selection_explanation == explanation

    edu = EducationalExperienceViewModel(
        active=True,
        subject_code=subject,
        mission_title=mission.title,
        composer_selection_reason=SELECTION_REASON_SPACED_REVIEW,
        selection_explanation=explanation,
        why_this_mission=explanation,
    )
    home = HomePageViewModel(educational=edu)
    why = StudentHomeService._why_now(home)
    assert why == explanation[:140]
    assert "due" in why.lower()


def test_home_sequential_why_unchanged_when_nothing_due() -> None:
    edu = EducationalExperienceViewModel(
        active=True,
        subject_code="CS1",
        composer_selection_reason=SELECTION_REASON_SEQUENTIAL,
        selection_explanation="",
    )
    home = HomePageViewModel(educational=edu)
    assert StudentHomeService._why_now(home) == "Next in your study plan."

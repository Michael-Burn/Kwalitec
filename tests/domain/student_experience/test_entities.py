"""Entity and projection correctness for Student Experience domain."""

from __future__ import annotations

import pytest

from app.domain.student_experience.experience_snapshot import ExperienceSnapshot
from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    ExperienceSurface,
    ExperienceWorkspaceStatus,
    is_canonical_surface,
    resolve_surface,
    surface_index,
)
from app.domain.student_experience.history_projection import (
    AchievementCard,
    CompletedSessionCard,
    HistoryProjection,
    ReadinessPoint,
)
from app.domain.student_experience.journey_projection import (
    JourneyProjection,
    JourneyTopicCard,
)
from app.domain.student_experience.profile_projection import (
    AccountSettings,
    LearningGoal,
    LearningStatistics,
    ProfileProjection,
    StudyPreferences,
)
from app.domain.student_experience.revision_projection import (
    RevisionOption,
    RevisionProjection,
)
from app.domain.student_experience.student_home import (
    StudentHome,
    readiness_band_label,
)
from tests.domain.student_experience.helpers import (
    make_explanation,
    make_session,
    make_start_action,
    make_workspace,
)


@pytest.mark.parametrize("surface", list(ExperienceSurface))
def test_navigate_to_each_surface(surface):
    ws = make_workspace().navigate_to(surface)
    assert ws.is_on(surface)
    assert ws.active_surface_label


@pytest.mark.parametrize("status", list(ExperienceWorkspaceStatus))
def test_workspace_status(status):
    ws = make_workspace().with_status(status)
    assert ws.status is status


def test_workspace_requires_ids():
    with pytest.raises(ValueError):
        make_workspace(workspace_id="")
    with pytest.raises(ValueError):
        make_workspace(student_id="  ")


@pytest.mark.parametrize("surface", list(CANONICAL_SURFACES))
def test_surface_index_order(surface):
    assert surface_index(surface) == CANONICAL_SURFACES.index(surface)
    assert is_canonical_surface(surface)
    assert resolve_surface(surface.value) is surface


def test_unknown_surface_rejected():
    with pytest.raises(ValueError):
        resolve_surface("studio")


@pytest.mark.parametrize("score,label", [
    (0.1, "Building"),
    (0.4, "Developing"),
    (0.7, "On Track"),
    (0.9, "Exam Ready"),
])
def test_readiness_bands(score, label):
    assert readiness_band_label(score) == label


@pytest.mark.parametrize("days", range(0, 16))
def test_home_countdown(days):
    home = StudentHome.create("stu-1", exam_countdown_days=days, exam_readiness=0.5)
    assert home.exam_countdown_days == days
    assert home.exam_readiness_label


def test_home_invalid_readiness():
    with pytest.raises(ValueError):
        StudentHome.create("stu-1", exam_readiness=1.5)


@pytest.mark.parametrize("ratio", [i / 10 for i in range(11)])
def test_journey_progress_ratio(ratio):
    proj = JourneyProjection.create("stu-1", overall_progress_ratio=ratio)
    assert proj.progress_percent == int(round(ratio * 100))


def test_journey_topics():
    cur = JourneyTopicCard.create("t1", "Current", status_label="Current")
    done = JourneyTopicCard.create("t0", "Done", status_label="Completed")
    up = JourneyTopicCard.create("t2", "Next", prerequisite_note="Finish current")
    proj = JourneyProjection.create(
        "stu-1",
        current_topic=cur,
        completed_topics=(done,),
        upcoming_topics=(up,),
        overall_progress_ratio=0.5,
    )
    assert proj.completed_count == 1
    assert proj.upcoming_count == 1


@pytest.mark.parametrize("n", range(0, 8))
def test_revision_alternatives(n):
    primary = RevisionOption.create("p", "Primary", is_primary=True)
    alts = tuple(
        RevisionOption.create(f"a{i}", f"Alt {i}") for i in range(n)
    )
    proj = RevisionProjection.create("stu-1", primary=primary, alternatives=alts)
    assert proj.option_count == 1 + n
    assert proj.has_revision


def test_revision_empty_message():
    proj = RevisionProjection.create("stu-1")
    assert not proj.has_revision
    assert "revision" in proj.empty_message.lower()


@pytest.mark.parametrize("minutes", range(0, 12))
def test_history_study_minutes(minutes):
    sessions = (
        CompletedSessionCard.create("s1", "T", study_minutes=minutes),
    )
    hist = HistoryProjection.create("stu-1", completed_sessions=sessions)
    assert hist.total_study_minutes == minutes


def test_history_progression_and_achievements():
    hist = HistoryProjection.create(
        "stu-1",
        readiness_progression=(ReadinessPoint.create("d1", 0.4),),
        mastered_topics=("A", "B"),
        recent_achievements=(AchievementCard.create("a1", "Streak"),),
    )
    assert hist.mastered_count == 2
    assert hist.session_count == 0


@pytest.mark.parametrize("progress", [i / 5 for i in range(6)])
def test_profile_goals(progress):
    goal = LearningGoal.create("g1", "Pass", progress_ratio=progress)
    profile = ProfileProjection.create(
        "stu-1",
        preferences=StudyPreferences.create(preferred_session_minutes=30),
        statistics=LearningStatistics.create(total_study_minutes=10),
        goals=(goal,),
        account=AccountSettings.create(email="A@B.COM"),
    )
    assert profile.account.email == "a@b.com"
    assert profile.goals[0].progress_ratio == progress


def test_session_start_action():
    session = make_session(mission_id="m1", session_id="s1")
    action = session.start_action()
    assert action.can_start
    assert make_start_action(enabled=False).can_start is False


def test_experience_snapshot_surfaces():
    ws = make_workspace()
    home = StudentHome.create("stu-1", recommendation_title="Revise")
    snap = ExperienceSnapshot.create(ws, home=home)
    assert snap.surface_for(ExperienceSurface.HOME) is home
    assert snap.active_surface is ExperienceSurface.HOME
    assert make_explanation(topic_title="X", reason_codes=("high_roi",)).is_complete

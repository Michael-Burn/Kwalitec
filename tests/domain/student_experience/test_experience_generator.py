"""Student Experience Engine tests (EXP-001).

Covers: experience generation, streak calculation, achievement generation,
reminder scheduling, determinism, and architecture purity.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation import ProgressReport
from domain.recommendation.enums import RecommendationCategory
from domain.student_experience import (
    AchievementKind,
    ExperienceGenerator,
    LearningStreak,
    ReminderKind,
    StreakBand,
    StudentExperience,
    consecutive_run_ending_at,
    longest_consecutive_run,
    streak_band_for,
)
from tests.domain.mission_generation.conftest import (
    generate_mission,
    make_aligned_diagnosis,
    make_aligned_priority,
    make_aligned_strategy,
)
from tests.domain.student_experience.experience_engine_helpers import (
    generate_experience,
    make_experience_inputs,
)
from tests.domain.study_planning.conftest import plan_study

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "domain" / "student_experience"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "openai",
        "anthropic",
        "random",
        "secrets",
        "uuid",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "openai.",
    "anthropic.",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_package_exports_required_types() -> None:
    from domain import student_experience as package

    for name in (
        "StudentExperience",
        "ExperienceGenerator",
        "Achievement",
        "Celebration",
        "Motivation",
        "Reminder",
        "LearningStreak",
        "SessionSummary",
    ):
        assert hasattr(package, name), name
        assert name in package.__all__


@pytest.mark.parametrize(
    "path",
    sorted(PACKAGE_ROOT.glob("*.py")),
    ids=lambda p: p.name,
)
def test_no_forbidden_infrastructure_or_ai_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports {name}"


def test_generator_source_has_no_randomness_or_persistence() -> None:
    source = (PACKAGE_ROOT / "experience_generator.py").read_text(encoding="utf-8")
    for token in (
        "import random",
        "from random",
        "import uuid",
        "from uuid",
        "import secrets",
        "from secrets",
        "datetime.now",
        "time.time",
        "sqlalchemy",
        "flask",
        "openai",
        "anthropic",
    ):
        assert token not in source


def test_domain_does_not_import_app_or_infrastructure() -> None:
    for path in PACKAGE_ROOT.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "from app." not in source
        assert "import app" not in source
        assert "infrastructure" not in source


# --- experience generation --------------------------------------------------


def test_generate_returns_complete_student_experience() -> None:
    experience = generate_experience()

    assert isinstance(experience, StudentExperience)
    assert experience.student_id == "student-ada"
    assert isinstance(experience.streak, LearningStreak)
    assert experience.session_summary.planned_minutes > 0
    assert "not mastery" in experience.session_summary.honesty_note.casefold()
    assert experience.motivation.message
    assert "Learner experience for student" in experience.presentation_narrative
    assert experience.recommendation_specification_id.value


def test_generate_is_deterministic() -> None:
    mission, study_plan, progress, recommendations = make_experience_inputs()
    first = ExperienceGenerator.generate(
        mission, study_plan, progress, recommendations
    )
    second = ExperienceGenerator.generate(
        mission, study_plan, progress, recommendations
    )
    assert first == second
    assert first.experience_id == second.experience_id
    assert first.achievements == second.achievements
    assert first.reminders == second.reminders


def test_generate_does_not_modify_recommendations() -> None:
    mission, study_plan, progress, recommendations = make_experience_inputs()
    before = (
        recommendations.specification_id,
        recommendations.categories(),
        recommendations.educational_rationale,
        tuple(
            (
                item.recommendation_id,
                item.category,
                item.reason.statement,
                item.expected_outcome,
            )
            for item in recommendations.recommendations
        ),
    )
    experience = ExperienceGenerator.generate(
        mission, study_plan, progress, recommendations
    )
    after = (
        recommendations.specification_id,
        recommendations.categories(),
        recommendations.educational_rationale,
        tuple(
            (
                item.recommendation_id,
                item.category,
                item.reason.statement,
                item.expected_outcome,
            )
            for item in recommendations.recommendations
        ),
    )
    assert before == after
    assert (
        experience.session_summary.next_focus_category
        is recommendations.primary.category
    )
    assert (
        experience.recommendation_specification_id
        == recommendations.specification_id
    )


def test_generate_rejects_student_mismatch() -> None:
    mission, study_plan, progress, recommendations = make_experience_inputs()
    mismatched = ProgressReport(
        report_id=progress.report_id,
        student_id="student-other",
        twin_id=progress.twin_id,
        mastery_trend=progress.mastery_trend,
        learning_velocity=progress.learning_velocity,
        knowledge_stability=progress.knowledge_stability,
        revision_effectiveness=progress.revision_effectiveness,
        confidence_level=progress.confidence_level,
        confidence_trend=progress.confidence_trend,
        intervention_signal=progress.intervention_signal,
        metrics=progress.metrics,
        educational_explanation=progress.educational_explanation,
        evidence_ids=progress.evidence_ids,
        mission_ids=progress.mission_ids,
        plan_ids=progress.plan_ids,
    )
    with pytest.raises(EducationalInvariantViolation, match="student_id"):
        ExperienceGenerator.generate(
            mission, study_plan, mismatched, recommendations
        )


def test_generate_rejects_mission_not_on_plan() -> None:
    mission, _study_plan, progress, recommendations = make_experience_inputs()
    other_diagnosis = make_aligned_diagnosis(diagnosis_id="diag-other")
    other_priority = make_aligned_priority(
        priority_id="prio-other",
        diagnosis_id="diag-other",
    )
    other_strategy = make_aligned_strategy(
        strategy_id="ts-other",
        diagnosis_id="diag-other",
    )
    other_mission = generate_mission(
        diagnosis=other_diagnosis,
        priority=other_priority,
        strategy=other_strategy,
    )
    other_plan = plan_study(
        missions=(other_mission,),
        priority=other_priority,
    )
    assert mission.mission_id not in other_plan.mission_ids
    with pytest.raises(EducationalInvariantViolation, match="plan_id|mission"):
        ExperienceGenerator.generate(
            mission, other_plan, progress, recommendations
        )


# --- streak calculation -----------------------------------------------------


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        ((), 0),
        ((0,), 1),
        ((0, 1, 2), 3),
        ((0, 1, 3, 4, 5), 3),
        ((1, 3, 5), 1),
    ],
)
def test_consecutive_run_ending_at(days: tuple[int, ...], expected: int) -> None:
    assert consecutive_run_ending_at(days) == expected


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        ((), 0),
        ((2,), 1),
        ((0, 1, 2, 4, 5), 3),
        ((0, 2, 3, 4, 7, 8), 3),
    ],
)
def test_longest_consecutive_run(days: tuple[int, ...], expected: int) -> None:
    assert longest_consecutive_run(days) == expected


@pytest.mark.parametrize(
    ("current", "band"),
    [
        (0, StreakBand.NONE),
        (1, StreakBand.STARTING),
        (2, StreakBand.STARTING),
        (3, StreakBand.BUILDING),
        (6, StreakBand.BUILDING),
        (7, StreakBand.STRONG),
    ],
)
def test_streak_band_for(current: int, band: StreakBand) -> None:
    assert streak_band_for(current) == band


def test_streak_from_completed_mission_on_plan() -> None:
    experience = generate_experience()
    assert experience.streak.current_days >= 1
    assert experience.streak.band is not StreakBand.NONE
    assert experience.streak.is_active
    assert len(experience.streak.active_day_indices) >= 1


def test_streak_build_uses_work_session_days() -> None:
    mission, study_plan, progress, _recommendations = make_experience_inputs()
    streak = ExperienceGenerator._build_streak(study_plan, progress)
    completed = {item.value for item in progress.mission_ids}
    expected_days = sorted(
        {
            session.day_index
            for session in study_plan.ordered_sessions
            if session.is_work() and session.mission_id.value in completed
        }
    )
    assert list(streak.active_day_indices) == expected_days
    assert streak.current_days == consecutive_run_ending_at(tuple(expected_days))


def test_streak_fallback_when_missions_not_on_plan_days() -> None:
    _mission, study_plan, progress, _recommendations = make_experience_inputs(
        completed_mission_count=3
    )
    # Extra missions are not on the plan; plan-aligned days still drive streak
    # when the primary mission has work sessions.
    streak = ExperienceGenerator._build_streak(study_plan, progress)
    assert streak.current_days >= 1
    assert streak.longest_days >= streak.current_days


# --- achievement generation -------------------------------------------------


def test_achievement_generation_includes_first_mission() -> None:
    experience = generate_experience()
    assert experience.has_achievement_kind(AchievementKind.FIRST_MISSION)
    assert experience.achievement_count() >= 1


def test_achievement_generation_for_five_missions() -> None:
    experience = generate_experience(completed_mission_count=5)
    assert experience.has_achievement_kind(AchievementKind.MISSIONS_FIVE)


def test_achievement_identities_are_unique() -> None:
    experience = generate_experience(completed_mission_count=5)
    ids = [item.achievement_id.value for item in experience.achievements]
    assert len(ids) == len(set(ids))


def test_celebrations_link_achievements() -> None:
    experience = generate_experience()
    achievement_celebrations = [
        item
        for item in experience.celebrations
        if item.related_achievement_id is not None
    ]
    assert achievement_celebrations
    achievement_ids = {item.achievement_id for item in experience.achievements}
    for celebration in achievement_celebrations:
        assert celebration.related_achievement_id in achievement_ids


# --- reminder scheduling ----------------------------------------------------


def test_reminder_scheduling_includes_review_windows() -> None:
    experience = generate_experience()
    assert experience.reminder_count() >= 1
    # Study plans from StudyPlanner include review windows for missions.
    mission, study_plan, _progress, _recommendations = make_experience_inputs()
    experience = generate_experience(
        mission=mission,
        study_plan=study_plan,
        progress=_progress,
        recommendations=_recommendations,
    )
    if study_plan.review_windows:
        assert experience.has_reminder_kind(ReminderKind.REVIEW_WINDOW)
        review_reminders = [
            item
            for item in experience.reminders
            if item.kind is ReminderKind.REVIEW_WINDOW
        ]
        assert len(review_reminders) == len(study_plan.review_windows)
        for reminder, window in zip(
            review_reminders, study_plan.review_windows, strict=True
        ):
            assert reminder.day_index == window.day_index
            assert reminder.mission_id == window.mission_id


def test_reminder_scheduling_echoes_primary_recommendation() -> None:
    experience = generate_experience()
    kinds = {item.kind for item in experience.reminders}
    assert ReminderKind.NEXT_SESSION in kinds or any(
        kind
        in {
            ReminderKind.REVISION_FOCUS,
            ReminderKind.CONTINUE_MISSION,
        }
        for kind in kinds
    )


def test_reminder_identities_are_unique_and_ordered() -> None:
    experience = generate_experience()
    ids = [item.reminder_id.value for item in experience.reminders]
    assert len(ids) == len(set(ids))
    sequences = [item.sequence for item in experience.reminders]
    assert sequences == sorted(sequences)


def test_session_summary_echoes_recommendation_category() -> None:
    mission, study_plan, progress, recommendations = make_experience_inputs()
    experience = ExperienceGenerator.generate(
        mission, study_plan, progress, recommendations
    )
    assert (
        experience.session_summary.next_focus_category
        is recommendations.primary.category
    )
    assert experience.session_summary.next_focus_category in RecommendationCategory
    assert experience.session_summary.mission_id == mission.mission_id
    assert (
        experience.session_summary.objective_statement
        == mission.objective.statement
    )

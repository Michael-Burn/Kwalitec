"""ExperienceGenerator — deterministic StudentExperience from Educational OS outputs.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Experience Generation

Rules
    No educational decisions. No AI. No prompting. No randomness.
    No persistence. No wall-clock dependence.
    Same Educational OS outputs always yield the same StudentExperience.
    RecommendationSpecification contents are referenced, never modified.
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.mission_generation.mission_specification import MissionSpecification
from domain.progress_evaluation.enums import (
    RevisionEffectivenessBand,
    StabilityBand,
    TrendDirection,
)
from domain.progress_evaluation.progress_report import ProgressReport
from domain.recommendation.enums import RecommendationCategory
from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from domain.student_experience.achievement import Achievement
from domain.student_experience.celebration import Celebration
from domain.student_experience.enums import (
    AchievementKind,
    CelebrationKind,
    MilestoneKind,
    MotivationTone,
    ReminderKind,
    StreakBand,
)
from domain.student_experience.ids import (
    AchievementId,
    CelebrationId,
    MotivationId,
    ReminderId,
    SessionSummaryId,
    StudentExperienceId,
)
from domain.student_experience.learning_streak import LearningStreak
from domain.student_experience.motivation import Motivation
from domain.student_experience.reminder import Reminder
from domain.student_experience.session_summary import SessionSummary
from domain.student_experience.student_experience import StudentExperience
from domain.study_planning.enums import SessionKind
from domain.study_planning.study_plan import StudyPlan

# Fixed presentation catalogues — deterministic copy only.

_CATEGORY_FOCUS_LABEL: dict[RecommendationCategory, str] = {
    RecommendationCategory.CONTINUE_MISSION: (
        "Continue the current mission sitting"
    ),
    RecommendationCategory.REVIEW_PREVIOUS_TOPIC: (
        "Review the previous topic before advancing"
    ),
    RecommendationCategory.INCREASE_DIFFICULTY: (
        "Increase instructional challenge carefully"
    ),
    RecommendationCategory.REDUCE_COGNITIVE_LOAD: (
        "Reduce cognitive load to stabilise understanding"
    ),
    RecommendationCategory.REPEAT_ASSESSMENT: (
        "Repeat assessment to calibrate confidence"
    ),
    RecommendationCategory.SCHEDULE_REVISION: (
        "Schedule spaced revision for retention"
    ),
    RecommendationCategory.REVISIT_PREREQUISITES: (
        "Revisit prerequisites blocking progress"
    ),
    RecommendationCategory.PAUSE_FOR_CONSOLIDATION: (
        "Pause advancement to consolidate recent learning"
    ),
}

_REVISION_REMINDER_CATEGORIES = frozenset(
    {
        RecommendationCategory.SCHEDULE_REVISION,
        RecommendationCategory.REVIEW_PREVIOUS_TOPIC,
        RecommendationCategory.REVISIT_PREREQUISITES,
    }
)

_STABLE_BANDS = frozenset({StabilityBand.STABLE, StabilityBand.DURABLE})

_HONESTY_NOTE = (
    "Finishing this sitting is progress on coverage — not mastery."
)


def streak_band_for(current_days: int) -> StreakBand:
    """Public helper matching LearningStreak.band_for."""
    return LearningStreak.band_for(current_days)


def consecutive_run_ending_at(days: tuple[int, ...]) -> int:
    """Return length of consecutive day run ending at the latest day."""
    if not days:
        return 0
    run = 1
    index = len(days) - 1
    while index > 0 and days[index] == days[index - 1] + 1:
        run += 1
        index -= 1
    return run


def longest_consecutive_run(days: tuple[int, ...]) -> int:
    """Return the longest consecutive integer run in ascending days."""
    if not days:
        return 0
    longest = 1
    current = 1
    for index in range(1, len(days)):
        if days[index] == days[index - 1] + 1:
            current += 1
            if current > longest:
                longest = current
        else:
            current = 1
    return longest


class ExperienceGenerator:
    """Pure domain service that generates StudentExperience projections.

    Generation is fully deterministic and presentation-focused. Educational
    decisions remain owned by Educational OS engines. Recommendations are
    referenced by identity and category label only — never mutated.
    """

    @classmethod
    def generate(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> StudentExperience:
        """Generate a StudentExperience from Educational OS outputs.

        Args:
            mission: Current MissionSpecification to summarise.
            study_plan: Active StudyPlan providing session days and reviews.
            progress: ProgressReport with completed mission and trend signals.
            recommendations: RecommendationSpecification to echo (not modify).

        Returns:
            Immutable StudentExperience with streak, achievements,
            celebrations, motivation, reminders, and session summary.

        Raises:
            EducationalInvariantViolation: When inputs are inconsistent.
        """
        cls._assert_inputs(mission, study_plan, progress, recommendations)

        streak = cls._build_streak(study_plan, progress)
        achievements = cls._build_achievements(
            mission=mission,
            study_plan=study_plan,
            progress=progress,
            streak=streak,
        )
        celebrations = cls._build_celebrations(
            achievements=achievements,
            streak=streak,
            progress=progress,
        )
        motivation = cls._build_motivation(
            mission=mission,
            progress=progress,
            streak=streak,
            recommendations=recommendations,
        )
        reminders = cls._build_reminders(
            mission=mission,
            study_plan=study_plan,
            recommendations=recommendations,
        )
        session_summary = cls._build_session_summary(
            mission=mission,
            progress=progress,
            recommendations=recommendations,
        )
        experience_id = cls._experience_id(
            mission, study_plan, progress, recommendations
        )
        narrative = cls._build_narrative(
            mission=mission,
            streak=streak,
            achievements=achievements,
            reminders=reminders,
            recommendations=recommendations,
        )
        return StudentExperience(
            experience_id=experience_id,
            student_id=mission.student_id,
            streak=streak,
            achievements=achievements,
            celebrations=celebrations,
            motivation=motivation,
            reminders=reminders,
            session_summary=session_summary,
            presentation_narrative=narrative,
            mission_id=mission.mission_id,
            plan_id=study_plan.plan_id,
            progress_report_id=progress.report_id,
            recommendation_specification_id=recommendations.specification_id,
        )

    # --- validation ---------------------------------------------------------

    @staticmethod
    def _assert_inputs(
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> None:
        if not isinstance(mission, MissionSpecification):
            raise EducationalInvariantViolation(
                "mission must be a MissionSpecification",
                invariant="ExperienceGenerator.mission.type",
            )
        if not isinstance(study_plan, StudyPlan):
            raise EducationalInvariantViolation(
                "study_plan must be a StudyPlan",
                invariant="ExperienceGenerator.study_plan.type",
            )
        if not isinstance(progress, ProgressReport):
            raise EducationalInvariantViolation(
                "progress must be a ProgressReport",
                invariant="ExperienceGenerator.progress.type",
            )
        if not isinstance(recommendations, RecommendationSpecification):
            raise EducationalInvariantViolation(
                "recommendations must be a RecommendationSpecification",
                invariant="ExperienceGenerator.recommendations.type",
            )
        student_id = mission.student_id
        for name, value in (
            ("study_plan", study_plan.student_id),
            ("progress", progress.student_id),
            ("recommendations", recommendations.student_id),
        ):
            if value != student_id:
                raise EducationalInvariantViolation(
                    f"{name} student_id must match mission student_id",
                    invariant="ExperienceGenerator.student_id.align",
                )
        if recommendations.mission_id != mission.mission_id:
            raise EducationalInvariantViolation(
                "recommendations.mission_id must match mission.mission_id",
                invariant="ExperienceGenerator.mission_id.align",
            )
        if recommendations.plan_id != study_plan.plan_id:
            raise EducationalInvariantViolation(
                "recommendations.plan_id must match study_plan.plan_id",
                invariant="ExperienceGenerator.plan_id.align",
            )
        if recommendations.progress_report_id != progress.report_id:
            raise EducationalInvariantViolation(
                "recommendations.progress_report_id must match progress.report_id",
                invariant="ExperienceGenerator.progress_report_id.align",
            )
        if mission.mission_id not in study_plan.mission_ids:
            raise EducationalInvariantViolation(
                "mission must belong to study_plan.mission_ids",
                invariant="ExperienceGenerator.mission.in_plan",
            )

    # --- streak -------------------------------------------------------------

    @classmethod
    def _build_streak(
        cls,
        study_plan: StudyPlan,
        progress: ProgressReport,
    ) -> LearningStreak:
        completed = {mission_id.value for mission_id in progress.mission_ids}
        active_days = sorted(
            {
                session.day_index
                for session in study_plan.ordered_sessions
                if session.kind is SessionKind.WORK
                and session.mission_id.value in completed
            }
        )
        if not active_days and progress.mission_ids:
            # Fallback: treat ordered completed missions as synthetic day indices.
            active_days = list(range(len(progress.mission_ids)))
        days = tuple(active_days)
        current = consecutive_run_ending_at(days)
        longest = max(longest_consecutive_run(days), current)
        band = LearningStreak.band_for(current)
        if current == 0:
            explanation = (
                "No consecutive study days recognised from completed missions "
                "on the active plan."
            )
        elif current == 1:
            explanation = (
                "One active study day recognised from completed mission work "
                "on the active plan."
            )
        else:
            explanation = (
                f"{current} consecutive study days recognised from completed "
                "mission work on the active plan."
            )
        return LearningStreak(
            current_days=current,
            longest_days=longest,
            active_day_indices=days,
            band=band,
            explanation=explanation,
        )

    # --- achievements -------------------------------------------------------

    @classmethod
    def _build_achievements(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        streak: LearningStreak,
    ) -> tuple[Achievement, ...]:
        completed_count = len(progress.mission_ids)
        plan_completed = sum(
            1
            for mission_id in study_plan.mission_ids
            if mission_id in progress.mission_ids
        )
        candidates: list[
            tuple[AchievementKind, MilestoneKind, str, str]
        ] = []
        if completed_count >= 1:
            candidates.append(
                (
                    AchievementKind.FIRST_MISSION,
                    MilestoneKind.FIRST_COMPLETION,
                    "First mission recognised",
                    "You completed your first mission sitting on this plan.",
                )
            )
        if streak.current_days >= 3:
            candidates.append(
                (
                    AchievementKind.STREAK_THREE,
                    MilestoneKind.STREAK_THRESHOLD,
                    "Three-day streak",
                    "Three consecutive study days recognised from your plan.",
                )
            )
        if streak.current_days >= 7:
            candidates.append(
                (
                    AchievementKind.STREAK_SEVEN,
                    MilestoneKind.STREAK_THRESHOLD,
                    "Seven-day streak",
                    "Seven consecutive study days recognised from your plan.",
                )
            )
        if completed_count >= 5:
            candidates.append(
                (
                    AchievementKind.MISSIONS_FIVE,
                    MilestoneKind.MISSION_COUNT,
                    "Five missions recognised",
                    "Five completed missions are reflected in your progress report.",
                )
            )
        if progress.mastery_trend.direction is TrendDirection.IMPROVING:
            candidates.append(
                (
                    AchievementKind.IMPROVING_MASTERY,
                    MilestoneKind.PROGRESS_SIGNAL,
                    "Improving progress signal",
                    "Your progress report shows an improving mastery trend.",
                )
            )
        if progress.knowledge_stability in _STABLE_BANDS:
            candidates.append(
                (
                    AchievementKind.STABLE_KNOWLEDGE,
                    MilestoneKind.PROGRESS_SIGNAL,
                    "Stable knowledge signal",
                    "Your progress report shows stable or durable knowledge.",
                )
            )
        if (
            progress.revision_effectiveness.band
            is RevisionEffectivenessBand.EFFECTIVE
        ):
            candidates.append(
                (
                    AchievementKind.EFFECTIVE_REVISION,
                    MilestoneKind.PROGRESS_SIGNAL,
                    "Effective revision signal",
                    "Your progress report shows effective revision outcomes.",
                )
            )
        if plan_completed >= 1 and plan_completed == len(study_plan.mission_ids):
            candidates.append(
                (
                    AchievementKind.PLAN_PROGRESS,
                    MilestoneKind.PLAN_SIGNAL,
                    "Plan missions recognised",
                    "Every mission on the active study plan appears in progress.",
                )
            )
        elif plan_completed >= 1:
            candidates.append(
                (
                    AchievementKind.PLAN_PROGRESS,
                    MilestoneKind.PLAN_SIGNAL,
                    "Plan progress recognised",
                    "Completed missions on the active study plan are recognised.",
                )
            )

        achievements: list[Achievement] = []
        for index, (kind, milestone, title, message) in enumerate(
            candidates, start=1
        ):
            achievements.append(
                Achievement(
                    achievement_id=AchievementId(
                        f"ach-{mission.mission_id.value}-{kind.value}-{index}"
                    ),
                    kind=kind,
                    milestone=milestone,
                    title=title,
                    message=message,
                    sequence=index,
                )
            )
        return tuple(achievements)

    # --- celebrations -------------------------------------------------------

    @classmethod
    def _build_celebrations(
        cls,
        achievements: tuple[Achievement, ...],
        streak: LearningStreak,
        progress: ProgressReport,
    ) -> tuple[Celebration, ...]:
        celebrations: list[Celebration] = []
        sequence = 1
        for achievement in achievements:
            celebrations.append(
                Celebration(
                    celebration_id=CelebrationId(
                        f"cel-{achievement.achievement_id.value}"
                    ),
                    kind=CelebrationKind.ACHIEVEMENT,
                    headline=achievement.title,
                    detail=achievement.message,
                    sequence=sequence,
                    related_achievement_id=achievement.achievement_id,
                )
            )
            sequence += 1
        if streak.current_days >= 3:
            celebrations.append(
                Celebration(
                    celebration_id=CelebrationId(
                        f"cel-streak-{streak.current_days}"
                    ),
                    kind=CelebrationKind.STREAK,
                    headline=f"{streak.current_days}-day learning streak",
                    detail=streak.explanation,
                    sequence=sequence,
                )
            )
            sequence += 1
        if progress.mastery_trend.direction is TrendDirection.IMPROVING:
            celebrations.append(
                Celebration(
                    celebration_id=CelebrationId("cel-progress-improving"),
                    kind=CelebrationKind.PROGRESS,
                    headline="Progress celebration",
                    detail=(
                        "Your mastery trend is improving — keep the honest "
                        "learning loop going."
                    ),
                    sequence=sequence,
                )
            )
            sequence += 1
        if any(
            item.milestone is MilestoneKind.MISSION_COUNT for item in achievements
        ):
            celebrations.append(
                Celebration(
                    celebration_id=CelebrationId("cel-milestone-missions"),
                    kind=CelebrationKind.MILESTONE,
                    headline="Mission milestone recognised",
                    detail=(
                        "A mission-count milestone was recognised from your "
                        "progress report."
                    ),
                    sequence=sequence,
                )
            )
        return tuple(celebrations)

    # --- motivation ---------------------------------------------------------

    @classmethod
    def _build_motivation(
        cls,
        mission: MissionSpecification,
        progress: ProgressReport,
        streak: LearningStreak,
        recommendations: RecommendationSpecification,
    ) -> Motivation:
        primary = recommendations.primary.category
        if streak.band is StreakBand.STRONG:
            tone = MotivationTone.CELEBRATORY
            message = (
                "Your strong study streak shows steady engagement — stay "
                "consistent with the next educational step."
            )
            signal = f"streak_band={streak.band.value}"
        elif progress.mastery_trend.direction is TrendDirection.DECLINING:
            tone = MotivationTone.RECOVERING
            message = (
                "Progress dipped — follow the educational recommendation and "
                "take the next sitting one step at a time."
            )
            signal = "mastery_trend=declining"
        elif streak.band is StreakBand.BUILDING:
            tone = MotivationTone.ENCOURAGING
            message = (
                "Your streak is building — return for the next planned sitting "
                "and keep the loop honest."
            )
            signal = f"streak_band={streak.band.value}"
        elif primary is RecommendationCategory.PAUSE_FOR_CONSOLIDATION:
            tone = MotivationTone.STEADY
            message = (
                "Consolidation protects understanding — honour the pause and "
                "return ready for the next sitting."
            )
            signal = f"recommendation={primary.value}"
        else:
            tone = MotivationTone.STEADY
            message = (
                "Stay with the educational next step — consistent sittings "
                "compound without claiming mastery."
            )
            signal = f"recommendation={primary.value}"
        return Motivation(
            motivation_id=MotivationId(
                f"mot-{mission.mission_id.value}-{tone.value}"
            ),
            tone=tone,
            message=message,
            supporting_signal=signal,
        )

    # --- reminders ----------------------------------------------------------

    @classmethod
    def _build_reminders(
        cls,
        mission: MissionSpecification,
        study_plan: StudyPlan,
        recommendations: RecommendationSpecification,
    ) -> tuple[Reminder, ...]:
        reminders: list[Reminder] = []
        sequence = 1
        for window in study_plan.review_windows:
            reminders.append(
                Reminder(
                    reminder_id=ReminderId(
                        f"rem-review-{window.mission_id.value}"
                        f"-{window.day_index}-{window.sequence}"
                    ),
                    kind=ReminderKind.REVIEW_WINDOW,
                    day_index=window.day_index,
                    message=(
                        f"Review reminder on plan day {window.day_index} "
                        f"({window.duration_minutes} minutes)."
                    ),
                    sequence=sequence,
                    mission_id=window.mission_id,
                    source_label="study_plan.review_windows",
                )
            )
            sequence += 1

        work_sessions = [
            session
            for session in study_plan.ordered_sessions
            if session.kind is SessionKind.WORK
            and session.mission_id == mission.mission_id
        ]
        if work_sessions:
            next_session = work_sessions[0]
            reminders.append(
                Reminder(
                    reminder_id=ReminderId(
                        f"rem-next-{next_session.session_id.value}"
                    ),
                    kind=ReminderKind.NEXT_SESSION,
                    day_index=next_session.day_index,
                    message=(
                        f"Next work sitting scheduled on plan day "
                        f"{next_session.day_index}."
                    ),
                    sequence=sequence,
                    mission_id=mission.mission_id,
                    source_label="study_plan.sessions",
                )
            )
            sequence += 1

        primary = recommendations.primary
        if primary.category in _REVISION_REMINDER_CATEGORIES:
            reminders.append(
                Reminder(
                    reminder_id=ReminderId(
                        f"rem-rev-{primary.recommendation_id.value}"
                    ),
                    kind=ReminderKind.REVISION_FOCUS,
                    day_index=0,
                    message=(
                        "Revision focus reminder from the educational "
                        f"recommendation ({primary.category.value})."
                    ),
                    sequence=sequence,
                    mission_id=mission.mission_id,
                    source_label="recommendation.primary",
                )
            )
            sequence += 1
        elif primary.category is RecommendationCategory.CONTINUE_MISSION:
            reminders.append(
                Reminder(
                    reminder_id=ReminderId(
                        f"rem-continue-{primary.recommendation_id.value}"
                    ),
                    kind=ReminderKind.CONTINUE_MISSION,
                    day_index=0,
                    message=(
                        "Continue-mission reminder echoing the primary "
                        "educational recommendation."
                    ),
                    sequence=sequence,
                    mission_id=mission.mission_id,
                    source_label="recommendation.primary",
                )
            )
        return tuple(reminders)

    # --- session summary ----------------------------------------------------

    @classmethod
    def _build_session_summary(
        cls,
        mission: MissionSpecification,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> SessionSummary:
        primary = recommendations.primary
        return SessionSummary(
            summary_id=SessionSummaryId(f"sum-{mission.mission_id.value}"),
            mission_id=mission.mission_id,
            objective_statement=mission.objective.statement,
            planned_minutes=mission.duration.planned_minutes,
            completed_mission_count=len(progress.mission_ids),
            mastery_trend_label=progress.mastery_trend.direction.value,
            confidence_trend_label=progress.confidence_trend.direction.value,
            next_focus_category=primary.category,
            next_focus_preview=_CATEGORY_FOCUS_LABEL[primary.category],
            honesty_note=_HONESTY_NOTE,
        )

    # --- narrative / identity -----------------------------------------------

    @staticmethod
    def _experience_id(
        mission: MissionSpecification,
        study_plan: StudyPlan,
        progress: ProgressReport,
        recommendations: RecommendationSpecification,
    ) -> StudentExperienceId:
        return StudentExperienceId(
            f"exp-{mission.mission_id.value}-{study_plan.plan_id.value}"
            f"-{progress.report_id.value}"
            f"-{recommendations.specification_id.value}"
        )

    @staticmethod
    def _build_narrative(
        mission: MissionSpecification,
        streak: LearningStreak,
        achievements: tuple[Achievement, ...],
        reminders: tuple[Reminder, ...],
        recommendations: RecommendationSpecification,
    ) -> str:
        return (
            f"Learner experience for student {mission.student_id}: "
            f"streak {streak.current_days} day(s), "
            f"{len(achievements)} achievement(s), "
            f"{len(reminders)} reminder(s), "
            f"next focus {recommendations.primary.category.value}."
        )

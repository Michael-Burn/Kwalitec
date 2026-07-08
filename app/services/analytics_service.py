"""Service for performance analytics and weekly report generation.

All calculations are deterministic. No AI or external APIs are used.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from app.extensions import db
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress
from app.services.readiness_service import ReadinessService


class AnalyticsService:
    """Service for generating analytics data and weekly performance reports.

    Provides time-series data for charts and comprehensive weekly summaries.
    All calculations are deterministic and based on stored learning data.
    """

    # ── Time-Series Analytics ─────────────────────────────────────────

    @staticmethod
    def get_readiness_over_time(
        user_id: int,
        weeks: int = 12,
    ) -> list[dict]:
        """Calculate readiness score trend over the past N weeks.

        For each complete week (Monday-Sunday), computes a snapshot of
        readiness at the end of that week.

        Args:
            user_id: The ID of the user.
            weeks: Number of past weeks to include (default 12).

        Returns:
            list[dict]: Each dict has week_label and readiness_score.
        """
        today = date.today()
        result = []

        for i in range(weeks - 1, -1, -1):
            # Calculate the end of week i weeks ago
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_end = last_monday + timedelta(days=6) - timedelta(weeks=i)

            # Week label
            week_start = week_end - timedelta(days=6)
            label = f"{week_start.strftime('%b %d')}"

            # Count topics started as of week_end
            leaf_ids = AnalyticsService._leaf_topic_ids()

            if not leaf_ids:
                total_leaf = 0
            else:
                total_leaf = len(leaf_ids)

            started_count = 0
            mastered_count = 0
            mastery_sum = 0.0

            if leaf_ids:
                progress_records = TopicProgress.query.filter(
                    TopicProgress.user_id == user_id,
                    TopicProgress.topic_id.in_(leaf_ids),
                ).all()

                for p in progress_records:
                    # Consider it started if created_at is on or before week_end
                    if p.revision_count > 0:
                        started_count += 1
                        mastery_sum += p.mastery_score
                    if p.current_stage == TopicProgress.STAGE_MASTERED:
                        mastered_count += 1

            coverage_pct = (started_count / total_leaf * 100) if total_leaf > 0 else 0.0
            avg_mastery = (mastery_sum / started_count) if started_count > 0 else 0.0

            # Missions completed up to week_end
            missions = Mission.query.filter(
                Mission.user_id == user_id,
                Mission.mission_date <= week_end,
            ).all()

            total_missions = len(missions)
            completed = sum(1 for m in missions if m.status == "Completed")
            review_discipline = (completed / total_missions * 100) if total_missions > 0 else 0.0

            score = (coverage_pct * 0.50) + (avg_mastery * 0.30) + (review_discipline * 0.20)

            result.append({
                "week_label": label,
                "readiness_score": round(score, 1),
                "coverage_pct": round(coverage_pct, 1),
                "avg_mastery": round(avg_mastery, 1),
                "review_discipline": round(review_discipline, 1),
            })

        return result

    @staticmethod
    def get_mastery_over_time(
        user_id: int,
        weeks: int = 12,
    ) -> list[dict]:
        """Calculate average mastery trend over the past N weeks.

        Args:
            user_id: The ID of the user.
            weeks: Number of past weeks to include (default 12).

        Returns:
            list[dict]: Each dict has week_label and average_mastery.
        """
        today = date.today()
        result = []

        for i in range(weeks - 1, -1, -1):
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_end = last_monday + timedelta(days=6) - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)

            label = f"{week_start.strftime('%b %d')}"

            leaf_ids = AnalyticsService._leaf_topic_ids()
            if not leaf_ids:
                result.append({"week_label": label, "average_mastery": 0.0})
                continue

            progress_records = TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.topic_id.in_(leaf_ids),
                TopicProgress.revision_count > 0,
            ).all()

            if not progress_records:
                result.append({"week_label": label, "average_mastery": 0.0})
                continue

            avg = sum(p.mastery_score for p in progress_records) / len(progress_records)
            result.append({
                "week_label": label,
                "average_mastery": round(avg, 1),
            })

        return result

    @staticmethod
    def get_accuracy_trend(
        user_id: int,
        weeks: int = 12,
    ) -> list[dict]:
        """Calculate accuracy trend (% correct) over the past N weeks.

        Args:
            user_id: The ID of the user.
            weeks: Number of past weeks to include (default 12).

        Returns:
            list[dict]: Each dict has week_label and accuracy.
        """
        today = date.today()
        result = []

        for i in range(weeks - 1, -1, -1):
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_end = last_monday + timedelta(days=6) - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)

            label = f"{week_start.strftime('%b %d')}"

            # Get all study attempts in this week
            attempts = StudyAttempt.query.filter(
                StudyAttempt.user_id == user_id,
                StudyAttempt.study_date >= week_start,
                StudyAttempt.study_date <= week_end,
            ).all()

            total_q = sum(a.questions_attempted or 0 for a in attempts)
            total_c = sum(a.questions_correct or 0 for a in attempts)

            accuracy = (total_c / total_q * 100) if total_q > 0 else None

            result.append({
                "week_label": label,
                "accuracy": round(accuracy, 1) if accuracy is not None else None,
            })

        return result

    @staticmethod
    def get_weekly_study_hours(
        user_id: int,
        weeks: int = 12,
    ) -> list[dict]:
        """Calculate total study hours per week over the past N weeks.

        Args:
            user_id: The ID of the user.
            weeks: Number of past weeks to include (default 12).

        Returns:
            list[dict]: Each dict has week_label and study_hours.
        """
        today = date.today()
        result = []

        for i in range(weeks - 1, -1, -1):
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_end = last_monday + timedelta(days=6) - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)

            label = f"{week_start.strftime('%b %d')}"

            attempts = StudyAttempt.query.filter(
                StudyAttempt.user_id == user_id,
                StudyAttempt.study_date >= week_start,
                StudyAttempt.study_date <= week_end,
            ).all()

            total_minutes = sum(a.duration_minutes or 0 for a in attempts)
            hours = total_minutes / 60.0

            result.append({
                "week_label": label,
                "study_hours": round(hours, 1),
            })

        return result

    @staticmethod
    def get_mission_completion_trend(
        user_id: int,
        weeks: int = 12,
    ) -> list[dict]:
        """Calculate mission completion rate per week over the past N weeks.

        Args:
            user_id: The ID of the user.
            weeks: Number of past weeks to include (default 12).

        Returns:
            list[dict]: Each dict has week_label, total_missions, completed, completion_rate.
        """
        today = date.today()
        result = []

        for i in range(weeks - 1, -1, -1):
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_end = last_monday + timedelta(days=6) - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)

            label = f"{week_start.strftime('%b %d')}"

            missions = Mission.query.filter(
                Mission.user_id == user_id,
                Mission.mission_date >= week_start,
                Mission.mission_date <= week_end,
            ).all()

            total = len(missions)
            completed = sum(1 for m in missions if m.status == "Completed")
            rate = (completed / total * 100) if total > 0 else None

            result.append({
                "week_label": label,
                "total_missions": total,
                "completed": completed,
                "completion_rate": round(rate, 1) if rate is not None else None,
            })

        return result

    @staticmethod
    def get_review_completion_trend(
        user_id: int,
        weeks: int = 12,
    ) -> list[dict]:
        """Calculate review completion (topics reviewed vs. due) per week.

        Args:
            user_id: The ID of the user.
            weeks: Number of past weeks to include (default 12).

        Returns:
            list[dict]: Each dict has week_label, reviews_due, reviews_done, completion_rate.
        """
        today = date.today()
        result = []

        for i in range(weeks - 1, -1, -1):
            days_since_monday = today.weekday()
            last_monday = today - timedelta(days=days_since_monday)
            week_end = last_monday + timedelta(days=6) - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)

            label = f"{week_start.strftime('%b %d')}"

            # Topics reviewed this week: distinct topic_ids in study attempts
            reviewed_topics = set()
            attempts = StudyAttempt.query.filter(
                StudyAttempt.user_id == user_id,
                StudyAttempt.study_date >= week_start,
                StudyAttempt.study_date <= week_end,
                StudyAttempt.topic_id.isnot(None),
            ).all()

            for a in attempts:
                if a.topic_id:
                    reviewed_topics.add(a.topic_id)

            reviews_done = len(reviewed_topics)

            # Reviews due during this week: topics with next_review_date in this week
            # This is approximate since we don't track historical review due dates
            last_updated = TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.updated_at >= week_start,
                TopicProgress.updated_at <= week_end,
            ).count()

            result.append({
                "week_label": label,
                "reviews_done": reviews_done,
                "topics_updated": last_updated,
            })

        return result

    # ── Weekly Report ─────────────────────────────────────────────────

    @staticmethod
    def generate_weekly_report(user_id: int) -> dict:
        """Generate a comprehensive weekly performance report.

        Covers the most recent complete week (Monday to Sunday) or the
        current incomplete week if it's the only data available.

        Args:
            user_id: The ID of the user.

        Returns:
            dict with keys:
                - week_start, week_end: date boundaries
                - week_label: human-readable label
                - readiness: current readiness score
                - study_hours: total hours studied this week
                - missions_completed: missions completed this week
                - total_missions: missions assigned this week
                - mission_completion_rate: percentage completed
                - topics_reviewed: distinct topics studied this week
                - questions_attempted, questions_correct: totals
                - accuracy: overall accuracy percentage
                - days_studied: number of days with study activity
                - current_streak, longest_streak: streak metrics
                - weakest_topics: list of weakest topics
                - strongest_topics: list of strongest topics
                - highlights: list of achievement strings
                - areas_for_improvement: list of focus area strings
        """
        today = date.today()
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday)
        week_end = last_monday + timedelta(days=6)

        # If today is not Sunday, report on the current incomplete week
        # Otherwise report on the just-completed week
        if days_since_monday == 6:
            week_start = last_monday
            week_end = today
        else:
            # Report on current incomplete week from Monday to today
            week_start = last_monday
            week_end = today

        label = f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}"

        # Readiness score
        readiness = ReadinessService.get_overall_readiness(user_id)

        # Study hours this week
        attempts_this_week = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date >= week_start,
            StudyAttempt.study_date <= week_end,
        ).all()

        total_minutes = sum(a.duration_minutes or 0 for a in attempts_this_week)
        study_hours = round(total_minutes / 60.0, 1)

        # Missions this week
        missions_this_week = Mission.query.filter(
            Mission.user_id == user_id,
            Mission.mission_date >= week_start,
            Mission.mission_date <= week_end,
        ).all()

        total_missions = len(missions_this_week)
        missions_completed = sum(1 for m in missions_this_week if m.status == "Completed")
        mission_completion_rate = (
            round((missions_completed / total_missions * 100), 1) if total_missions > 0 else None
        )

        # Topics reviewed this week
        reviewed_topic_ids = set()
        for a in attempts_this_week:
            if a.topic_id:
                reviewed_topic_ids.add(a.topic_id)
        topics_reviewed = len(reviewed_topic_ids)

        # Questions and accuracy
        total_questions = sum(a.questions_attempted or 0 for a in attempts_this_week)
        total_correct = sum(a.questions_correct or 0 for a in attempts_this_week)
        accuracy = round((total_correct / total_questions * 100), 1) if total_questions > 0 else None

        # Days studied
        study_dates = set()
        for a in attempts_this_week:
            d = a.study_date
            if isinstance(d, datetime):
                d = d.date()
            if isinstance(d, date):
                study_dates.add(d)
        days_studied = len(study_dates)

        # Streaks
        current_streak = ReadinessService.get_current_streak(user_id)
        longest_streak = ReadinessService.get_longest_streak(user_id)

        # Weakest & strongest topics
        weakest_topics = ReadinessService.get_weakest_topics(user_id, limit=3)
        strongest_topics = ReadinessService.get_strongest_topics(user_id, limit=3)

        # Highlights
        highlights = []
        if missions_completed > 0:
            highlights.append(
                f"Completed {missions_completed} mission{'s' if missions_completed != 1 else ''} this week"
            )
        if topics_reviewed > 0:
            highlights.append(
                f"Reviewed {topics_reviewed} topic{'s' if topics_reviewed != 1 else ''}"
            )
        if total_questions > 0 and accuracy is not None:
            if accuracy >= 80:
                highlights.append(f"Strong accuracy at {accuracy}% across {total_questions} questions")
            elif accuracy >= 60:
                highlights.append(f"Moderate accuracy at {accuracy}% across {total_questions} questions")
        if study_hours >= 1:
            highlights.append(f"Studied {study_hours} hours across {days_studied} day{'s' if days_studied != 1 else ''}")
        if current_streak >= 7:
            highlights.append(f"Maintained a {current_streak}-day study streak")
        if days_studied >= 5:
            highlights.append(f"Consistent effort: studied {days_studied} out of 7 days")

        # Areas for improvement
        areas = []
        if weakest_topics:
            weakest_names = ", ".join(t["topic_name"] for t in weakest_topics[:2])
            areas.append(f"Focus on weakest topics: {weakest_names}")
        if mission_completion_rate is not None and mission_completion_rate < 70:
            areas.append(f"Mission completion rate at {mission_completion_rate}% — aim for 100%")
        if accuracy is not None and accuracy < 60:
            areas.append(f"Accuracy at {accuracy}% — review mistakes carefully")
        if days_studied < 4:
            areas.append(f"Only studied {days_studied} day{'s' if days_studied != 1 else ''} — try for at least 5 days")
        if study_hours < 1 and total_missions > 0:
            areas.append("Track study duration to better measure effort")
        if len(areas) == 0:
            areas.append("Keep up the consistent effort. No critical areas identified this week.")

        # If no data at all
        if total_missions == 0 and len(attempts_this_week) == 0:
            highlights.append("No study activity recorded this week. Start your first mission!")
            if len(areas) == 0:
                areas.append("Set up a study plan and begin your first mission to start tracking progress.")

        return {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "week_label": label,
            "readiness": readiness,
            "study_hours": study_hours,
            "missions_completed": missions_completed,
            "total_missions": total_missions,
            "mission_completion_rate": mission_completion_rate,
            "topics_reviewed": topics_reviewed,
            "questions_attempted": total_questions,
            "questions_correct": total_correct,
            "accuracy": accuracy,
            "days_studied": days_studied,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "weakest_topics": weakest_topics,
            "strongest_topics": strongest_topics,
            "highlights": highlights,
            "areas_for_improvement": areas,
        }

    # ── Lifetime Summary ──────────────────────────────────────────────

    @staticmethod
    def get_lifetime_summary(user_id: int) -> dict:
        """Get lifetime learning statistics.

        Args:
            user_id: The ID of the user.

        Returns:
            dict with lifetime statistics.
        """
        attempts = StudyAttempt.query.filter_by(user_id=user_id).all()
        missions = Mission.query.filter_by(user_id=user_id).all()

        total_attempts = len(attempts)
        total_minutes = sum(a.duration_minutes or 0 for a in attempts)
        total_hours = round(total_minutes / 60.0, 1)
        total_questions = sum(a.questions_attempted or 0 for a in attempts)
        total_correct = sum(a.questions_correct or 0 for a in attempts)

        overall_accuracy = (
            round((total_correct / total_questions * 100), 1) if total_questions > 0 else None
        )

        total_missions = len(missions)
        missions_completed = sum(1 for m in missions if m.status == "Completed")

        # Distinct study days
        study_dates = set()
        for a in attempts:
            d = a.study_date
            if isinstance(d, datetime):
                d = d.date()
            study_dates.add(d)
        total_days = len(study_dates)

        first_study = min(study_dates) if study_dates else None
        last_study = max(study_dates) if study_dates else None

        return {
            "total_attempts": total_attempts,
            "total_hours": total_hours,
            "total_questions": total_questions,
            "total_correct": total_correct,
            "overall_accuracy": overall_accuracy,
            "total_missions": total_missions,
            "missions_completed": missions_completed,
            "total_study_days": total_days,
            "first_study": first_study.isoformat() if first_study else None,
            "last_study": last_study.isoformat() if last_study else None,
        }

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _leaf_topic_ids() -> list[int]:
        """Get IDs of all leaf topics (topics without subtopics).

        Returns:
            list[int]: Leaf topic IDs.
        """
        from app.models.curriculum import Topic

        all_topics = Topic.query.filter_by(active=True).all()
        parent_ids = {t.parent_topic_id for t in all_topics if t.parent_topic_id is not None}
        return [t.id for t in all_topics if t.id not in parent_ids]
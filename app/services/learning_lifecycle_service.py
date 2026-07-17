"""Learning Lifecycle — authoritative Version 1 educational stage resolution.

V1SP-001A: Not Started → Learning → Revision.

Lifecycle is derived from Study Progress + active study context (one source of
truth). Presentation flags (entered / acknowledged) are persisted on the Study
Plan so celebration and revision metrics remain honest. Exam Ready is reserved
for Version 2 and is never assigned here.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime

from app.extensions import db
from app.models.curriculum import Curriculum
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.models.topic_progress import TopicProgress
from app.services.curriculum_service import CurriculumService
from app.services.study_plan_service import StudyPlanService

logger = logging.getLogger(__name__)


class LearningLifecycle:
    """Canonical Version 1 learning lifecycle stages."""

    NOT_STARTED = "not_started"
    LEARNING = "learning"
    REVISION = "revision"
    # EXAM_READY reserved for Version 2 — do not implement.


@dataclass(frozen=True)
class RevisionMetrics:
    """Revision Workspace metrics — only real observed values, never fabricated."""

    topics_completed: int
    topics_total: int
    revision_sessions: int | None
    practice_questions_completed: int | None
    revision_streak: int | None
    mixed_quiz_attempts: int | None


@dataclass(frozen=True)
class LifecycleSnapshot:
    """Immutable view of the student's Version 1 learning lifecycle."""

    stage: str
    syllabus_complete: bool
    topics_completed: int
    topics_total: int
    show_completion_acknowledgement: bool
    revision_metrics: RevisionMetrics | None
    workspace_label: str
    acknowledgement_title: str
    acknowledgement_body: str


_ACK_TITLE = "Syllabus Complete"
_ACK_BODY = (
    "Congratulations. You have completed the syllabus. "
    "Your focus is now revision and examination readiness."
)
_REVISION_INTRO = "You have now entered Revision Mode."


class LearningLifecycleService:
    """Resolve and maintain the Version 1 learning lifecycle.

    Authority: Study Progress leaf completion within the active Study Plan's
    curriculum. Does not invent Exam Ready, spaced repetition, or adaptive AI.
    """

    @staticmethod
    def resolve(
        user_id: int,
        *,
        study_plan: StudyPlan | None = None,
        today: date | None = None,
    ) -> LifecycleSnapshot:
        """Return the authoritative lifecycle snapshot for a student.

        Automatically stamps ``revision_entered_at`` the first time syllabus
        completion is detected so legacy completed students enter Revision on
        first load without a manual migration.

        Args:
            user_id: Authenticated student id.
            study_plan: Optional active plan; loaded when omitted.
            today: Optional date for streak calculations (defaults to today).

        Returns:
            LifecycleSnapshot with stage, acknowledgement flag, and metrics.
        """
        if today is None:
            today = date.today()

        plan = study_plan
        if plan is None:
            plan = StudyPlanService.get_user_active_plan(user_id)

        if plan is None or not plan.curriculum_id:
            return LearningLifecycleService._not_started_snapshot()

        curriculum = CurriculumService.get_curriculum_by_id(plan.curriculum_id)
        if curriculum is None:
            return LearningLifecycleService._not_started_snapshot()

        progress = CurriculumService.get_curriculum_progress(user_id, curriculum)
        topics_total = int(progress["total_topics"])
        topics_completed = int(progress["completed_topics"])
        syllabus_complete = (
            topics_total > 0 and topics_completed >= topics_total
        )

        if not syllabus_complete:
            return LifecycleSnapshot(
                stage=LearningLifecycle.LEARNING,
                syllabus_complete=False,
                topics_completed=topics_completed,
                topics_total=topics_total,
                show_completion_acknowledgement=False,
                revision_metrics=None,
                workspace_label="Learning Workspace",
                acknowledgement_title=_ACK_TITLE,
                acknowledgement_body=_ACK_BODY,
            )

        LearningLifecycleService._ensure_revision_entered(plan)
        metrics = LearningLifecycleService._build_revision_metrics(
            user_id=user_id,
            plan=plan,
            topics_completed=topics_completed,
            topics_total=topics_total,
            today=today,
        )
        show_ack = not bool(plan.revision_acknowledged)
        return LifecycleSnapshot(
            stage=LearningLifecycle.REVISION,
            syllabus_complete=True,
            topics_completed=topics_completed,
            topics_total=topics_total,
            show_completion_acknowledgement=show_ack,
            revision_metrics=metrics,
            workspace_label="Revision Workspace",
            acknowledgement_title=_ACK_TITLE,
            acknowledgement_body=_ACK_BODY,
        )

    @staticmethod
    def is_revision(
        user_id: int,
        *,
        study_plan: StudyPlan | None = None,
    ) -> bool:
        """Return True when the student is in the Revision lifecycle stage."""
        return (
            LearningLifecycleService.resolve(
                user_id, study_plan=study_plan
            ).stage
            == LearningLifecycle.REVISION
        )

    @staticmethod
    def is_syllabus_complete(user_id: int, curriculum: Curriculum) -> bool:
        """Return True when every required syllabus leaf is completed studying."""
        progress = CurriculumService.get_curriculum_progress(user_id, curriculum)
        total = int(progress["total_topics"])
        completed = int(progress["completed_topics"])
        return total > 0 and completed >= total

    @staticmethod
    def acknowledge_revision(user_id: int) -> bool:
        """Dismiss the one-time syllabus-complete acknowledgement.

        Args:
            user_id: Authenticated student id.

        Returns:
            True when an active plan existed and was updated.
        """
        plan = StudyPlanService.get_user_active_plan(user_id)
        if plan is None:
            return False
        if not LearningLifecycleService.is_revision(user_id, study_plan=plan):
            return False
        plan.revision_acknowledged = True
        if plan.revision_entered_at is None:
            plan.revision_entered_at = datetime.utcnow()
        db.session.commit()
        return True

    @staticmethod
    def revision_intro_line() -> str:
        """Short understated line for the completion acknowledgement."""
        return _REVISION_INTRO

    @staticmethod
    def _not_started_snapshot() -> LifecycleSnapshot:
        return LifecycleSnapshot(
            stage=LearningLifecycle.NOT_STARTED,
            syllabus_complete=False,
            topics_completed=0,
            topics_total=0,
            show_completion_acknowledgement=False,
            revision_metrics=None,
            workspace_label="Learning Workspace",
            acknowledgement_title=_ACK_TITLE,
            acknowledgement_body=_ACK_BODY,
        )

    @staticmethod
    def _ensure_revision_entered(plan: StudyPlan) -> None:
        """Stamp revision entry on first detection (legacy-safe, idempotent)."""
        if plan.revision_entered_at is not None:
            return
        plan.revision_entered_at = datetime.utcnow()
        db.session.commit()
        logger.info(
            "Learning lifecycle: user plan %s entered Revision (syllabus complete)",
            plan.id,
        )

    @staticmethod
    def _build_revision_metrics(
        *,
        user_id: int,
        plan: StudyPlan,
        topics_completed: int,
        topics_total: int,
        today: date,
    ) -> RevisionMetrics:
        """Build revision metrics from observed data only.

        Missing instrumentation surfaces as ``None`` (template shows em dash),
        never as fabricated zeros that imply activity.
        """
        entered = plan.revision_entered_at
        if entered is None:
            return RevisionMetrics(
                topics_completed=topics_completed,
                topics_total=topics_total,
                revision_sessions=None,
                practice_questions_completed=None,
                revision_streak=None,
                mixed_quiz_attempts=None,
            )

        entered_date = entered.date() if isinstance(entered, datetime) else entered
        revision_missions = (
            Mission.query.filter(
                Mission.user_id == user_id,
                Mission.study_plan_id == plan.id,
                Mission.mission_date >= entered_date,
                Mission.status == "Completed",
            )
            .order_by(Mission.mission_date.asc())
            .all()
        )
        revision_sessions = len(revision_missions)

        practice_questions = LearningLifecycleService._sum_practice_questions(
            user_id=user_id,
            entered_date=entered_date,
        )
        streak = LearningLifecycleService._revision_streak(
            revision_missions, today=today
        )
        mixed_quiz_attempts = LearningLifecycleService._count_mixed_quiz_missions(
            revision_missions
        )

        return RevisionMetrics(
            topics_completed=topics_completed,
            topics_total=topics_total,
            revision_sessions=revision_sessions,
            practice_questions_completed=practice_questions,
            revision_streak=streak,
            mixed_quiz_attempts=mixed_quiz_attempts,
        )

    @staticmethod
    def _sum_practice_questions(
        *,
        user_id: int,
        entered_date: date,
    ) -> int | None:
        """Sum recorded practice questions since revision entry, or None if none."""
        from app.models.learning import StudyAttempt

        attempts = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date >= entered_date,
            StudyAttempt.questions_attempted.isnot(None),
        ).all()
        if not attempts:
            return None
        return sum(int(a.questions_attempted or 0) for a in attempts)

    @staticmethod
    def _revision_streak(
        completed_missions: list[Mission],
        *,
        today: date,
    ) -> int | None:
        """Count consecutive days ending today with a completed revision mission."""
        if not completed_missions:
            return None
        days_with_session = {m.mission_date for m in completed_missions}
        streak = 0
        cursor = today
        while cursor in days_with_session:
            streak += 1
            cursor = date.fromordinal(cursor.toordinal() - 1)
        return streak if streak > 0 else None

    @staticmethod
    def _count_mixed_quiz_missions(missions: list[Mission]) -> int | None:
        """Count completed missions whose title indicates a mixed-topic quiz."""
        count = 0
        for mission in missions:
            title = (mission.title or "").lower()
            if "mixed" in title and "quiz" in title:
                count += 1
        return count if count > 0 else None

    @staticmethod
    def weakest_completed_topic_label(user_id: int) -> str | None:
        """Return a deterministic weak-topic label among completed topics, if any."""
        from app.services.adaptive_learning_service import AdaptiveLearningService
        from app.services.planning_service import PlanningService

        plan = StudyPlanService.get_user_active_plan(user_id)
        weak = AdaptiveLearningService.get_weak_topics(user_id, threshold=70.0)
        for progress in weak:
            if not progress.completed:
                continue
            topic = progress.topic
            if topic is None:
                continue
            code = (
                PlanningService._resolve_official_topic_code(plan, topic)
                if plan is not None
                else None
            )
            return PlanningService._topic_study_label(topic, topic_code=code)

        # Fall back to any completed topic with the lowest mastery among completed.
        completed = (
            TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.completed.is_(True),
            )
            .order_by(TopicProgress.mastery_score.asc())
            .first()
        )
        if completed is None or completed.topic is None:
            return None
        topic = completed.topic
        code = (
            PlanningService._resolve_official_topic_code(plan, topic)
            if plan is not None
            else None
        )
        return PlanningService._topic_study_label(topic, topic_code=code)

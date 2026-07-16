"""Study Session experience (LXP-002) and Practice Outcome Capture (LXP-003).

LXP-002 provides the Study Session between Today's Mission and Finish.
LXP-003 records Observed Practice Outcomes after Finish Study Session,
creating lawful Educational Evidence inputs via existing LearningService /
Evidence Authority paths — without redesigning Twin, Readiness, or
Recommendation logic.

PTP-002: This service owns the authoritative Version 1 student closure path
(Study Session → Practice Outcome Capture → Study Session Feedback). Legacy
HTTP endpoints must redirect or delegate here and must not write a second
record of the same educational event.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date

from app.extensions import db
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from app.services.learning_service import LearningService
from app.services.mission_service import MissionService

logger = logging.getLogger(__name__)

COMPLETION_YES = "yes"
COMPLETION_PARTIAL = "partially"
COMPLETION_NO = "no"

COMPLETION_LABELS = {
    COMPLETION_YES: "Yes",
    COMPLETION_PARTIAL: "Partially",
    COMPLETION_NO: "No",
}

PRACTICE_OUTCOME_SUCCESS_MESSAGE = (
    "Your practice results have been recorded. "
    "Kwalitec will use objective practice outcomes to improve future "
    "educational guidance when appropriate."
)

# LXP-004 Study Session Feedback scenarios (presentation only).
FEEDBACK_PRACTICE_RECORDED = "practice_recorded"
FEEDBACK_NO_PRACTICE = "no_practice"
FEEDBACK_PARTIAL = "partial_session"
FEEDBACK_ABANDONED = "session_abandoned"

# Educational prompts only — scored practice is captured after Finish (LXP-003).
RECOMMENDED_ACTIVITIES: tuple[str, ...] = (
    "Read today's topic",
    "Work through examples",
    "Attempt practice questions",
    "Review mistakes",
)


@dataclass(frozen=True)
class StudySessionContext:
    """Presentation context for the Study Session screens."""

    topic_title: str
    learning_objective: str
    why_studying: str
    estimated_minutes: int | None
    success_looks_like: tuple[str, ...]
    recommended_activities: tuple[str, ...]
    mission_status: str


@dataclass(frozen=True)
class StudySessionFinishResult:
    """Outcome of finishing a Study Session review."""

    mission: Mission
    completion_status: str
    study_progress_updated: bool
    mission_completed: bool


@dataclass(frozen=True)
class PracticeOutcomeResult:
    """Outcome of Practice Outcome Capture (LXP-003)."""

    mission: Mission
    study_attempt: StudyAttempt
    authorised_evidence: bool
    mission_completed: bool


class StudySessionService:
    """Orchestrate the Study Session lifecycle for a daily Mission."""

    @staticmethod
    def recommended_activities() -> tuple[str, ...]:
        return RECOMMENDED_ACTIVITIES

    @staticmethod
    def estimated_minutes_for_mission(
        mission: Mission,
        study_plan: StudyPlan | None,
    ) -> int | None:
        """Approximate duration from the active plan's day-type minutes."""
        if study_plan is None:
            return None
        day = mission.mission_date
        if day is None:
            return study_plan.weekday_study_minutes
        if day.weekday() >= 5:
            return study_plan.weekend_study_minutes
        return study_plan.weekday_study_minutes

    @staticmethod
    def build_session_context(
        mission: Mission,
        study_plan: StudyPlan | None = None,
        *,
        why_studying: str | None = None,
        learning_objective: str | None = None,
    ) -> StudySessionContext:
        """Build student-facing Study Session presentation fields."""
        topic_title = mission.title or "Today's topic"
        objective = learning_objective or (
            "Engage with today's topic through reading, examples, and practice "
            "so you can close today's planned study honestly."
        )
        why = why_studying or (
            "In Learning Mode, today's mission follows your Current Learning "
            "Topic — the next syllabus topic you have not yet completed studying."
        )
        minutes = StudySessionService.estimated_minutes_for_mission(
            mission, study_plan
        )
        success = (
            "Spend focused time on today's topic",
            "Work through the recommended study activities",
            "Finish the session and record today's practice results",
        )
        return StudySessionContext(
            topic_title=topic_title,
            learning_objective=objective,
            why_studying=why,
            estimated_minutes=minutes,
            success_looks_like=success,
            recommended_activities=RECOMMENDED_ACTIVITIES,
            mission_status=mission.status,
        )

    @staticmethod
    def get_owned_mission(mission_id: int, user_id: int) -> Mission:
        """Load a mission and enforce ownership.

        Raises:
            ValueError: If the mission is missing or not owned by the user.
        """
        mission = Mission.query.get(mission_id)
        if mission is None:
            raise ValueError(f"Mission {mission_id} not found")
        if mission.user_id != user_id:
            raise ValueError(f"Mission {mission_id} does not belong to user {user_id}")
        return mission

    @staticmethod
    def start_session(mission_id: int, user_id: int) -> Mission:
        """Move a Pending mission into In Progress for the Study Session.

        Idempotent when already In Progress. Rejects Completed missions.
        """
        mission = StudySessionService.get_owned_mission(mission_id, user_id)
        if mission.status == "Completed":
            raise ValueError("This study session has already been recorded.")
        if mission.status == "Pending":
            return MissionService.update_mission_status(
                mission_id=mission.id,
                user_id=user_id,
                status="In Progress",
            )
        return mission

    @staticmethod
    def _format_session_notes(completion_status: str, notes: str | None) -> str:
        label = COMPLETION_LABELS.get(completion_status, completion_status)
        header = f"Session completion: {label}"
        clean = (notes or "").strip()
        if clean:
            return f"{header}\n\n{clean}"
        return header

    @staticmethod
    def mark_all_tasks_complete(mission: Mission) -> None:
        """Mark every mission task done so lawful mission completion can proceed."""
        for task in mission.tasks:
            task.completed = True
        db.session.commit()

    @staticmethod
    def finish_session(
        mission_id: int,
        user_id: int,
        completion_status: str,
        notes: str | None = None,
        *,
        topic_id: int | None = None,
        apply_study_progress: Callable[[], None] | None = None,
    ) -> StudySessionFinishResult:
        """Close the Study Session from the completion review.

        Educational meaning:
        - Completing a Study Session means today's planned activity was engaged.
        - It does not mean understanding, knowledge, mastery, or Evidence.

        State rules:
        - Yes → mission completed + Study Progress may update (caller applies).
        - Partially → mission completed; Study Progress left unchanged.
        - No → mission remains open; Study Progress unchanged.

        Never writes question scores, confidence, Estimated Knowledge / Mastery,
        or authorised Educational Evidence of understanding.
        """
        if completion_status not in COMPLETION_LABELS:
            raise ValueError(f"Invalid completion status: {completion_status}")

        mission = StudySessionService.get_owned_mission(mission_id, user_id)
        if mission.status == "Completed":
            raise ValueError("This study session has already been recorded.")

        study_progress_updated = False
        mission_completed = False

        if completion_status in (COMPLETION_YES, COMPLETION_PARTIAL):
            StudySessionService.mark_all_tasks_complete(mission)
            mission = MissionService.complete_mission(mission.id, user_id)
            mission_completed = True

        LearningService.create_study_attempt(
            user_id=user_id,
            mission_id=mission.id,
            topic_id=topic_id,
            study_date=date.today(),
            notes=StudySessionService._format_session_notes(
                completion_status, notes
            ),
        )

        if completion_status == COMPLETION_YES and apply_study_progress is not None:
            apply_study_progress()
            study_progress_updated = True

        logger.info(
            "Study session finished mission=%s user=%s completion=%s "
            "mission_completed=%s study_progress_updated=%s",
            mission.id,
            user_id,
            completion_status,
            mission_completed,
            study_progress_updated,
        )
        return StudySessionFinishResult(
            mission=mission,
            completion_status=completion_status,
            study_progress_updated=study_progress_updated,
            mission_completed=mission_completed,
        )

    @staticmethod
    def validate_practice_outcome(
        questions_attempted: int,
        questions_correct: int,
    ) -> None:
        """Reject impossible Observed Practice Outcome values.

        Args:
            questions_attempted: Count of questions tried (must be > 0).
            questions_correct: Count answered correctly (0 .. attempted).

        Raises:
            ValueError: When values are missing or educationally impossible.
        """
        if questions_attempted is None or questions_correct is None:
            raise ValueError("Questions Attempted and Questions Correct are required.")
        if not isinstance(questions_attempted, int) or not isinstance(
            questions_correct, int
        ):
            raise ValueError("Practice outcome counts must be whole numbers.")
        if questions_attempted <= 0:
            raise ValueError("Questions Attempted must be greater than zero.")
        if questions_correct < 0:
            raise ValueError("Questions Correct must be zero or greater.")
        if questions_correct > questions_attempted:
            raise ValueError(
                "Questions Correct cannot exceed Questions Attempted."
            )

    @staticmethod
    def _format_practice_notes(notes: str | None) -> str | None:
        clean = (notes or "").strip()
        return clean or None

    @staticmethod
    def _find_latest_attempt_for_mission(
        user_id: int,
        mission_id: int,
    ) -> StudyAttempt | None:
        return (
            StudyAttempt.query.filter_by(user_id=user_id, mission_id=mission_id)
            .order_by(StudyAttempt.created_at.desc(), StudyAttempt.id.desc())
            .first()
        )

    @staticmethod
    def record_practice_outcome(
        mission_id: int,
        user_id: int,
        questions_attempted: int,
        questions_correct: int,
        duration_minutes: int | None = None,
        notes: str | None = None,
        *,
        topic_id: int | None = None,
    ) -> PracticeOutcomeResult:
        """Record Observed Practice Outcomes after Finish Study Session.

        Educational meaning:
        - Submitted counts are Observed Practice Outcomes only.
        - They are not Knowledge, Mastery, Competence, or Readiness.

        State rules (LXP-003):
        - May create or update a StudyAttempt with structured question results.
        - May trigger the existing Educational Evidence Authority path (via
          LearningService), which may lawfully update Estimated Knowledge.
        - Completes the Mission so the Study Session can close.
        - Must not directly write Study Progress, Readiness, or Recommendations.

        Raises:
            ValueError: On ownership, already-completed, or invalid outcomes.
        """
        StudySessionService.validate_practice_outcome(
            questions_attempted, questions_correct
        )
        if duration_minutes is not None and duration_minutes <= 0:
            raise ValueError("Time spent must be a positive number of minutes.")

        mission = StudySessionService.get_owned_mission(mission_id, user_id)
        if mission.status == "Completed":
            raise ValueError("This study session has already been recorded.")

        StudySessionService.mark_all_tasks_complete(mission)
        mission = MissionService.complete_mission(mission.id, user_id)

        practice_notes = StudySessionService._format_practice_notes(notes)
        existing = StudySessionService._find_latest_attempt_for_mission(
            user_id, mission.id
        )

        if existing is not None and not (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
                existing
            )
        ):
            existing.questions_attempted = questions_attempted
            existing.questions_correct = questions_correct
            if duration_minutes is not None:
                existing.duration_minutes = duration_minutes
            if practice_notes:
                existing.notes = practice_notes
            if topic_id is not None and existing.topic_id is None:
                existing.topic_id = topic_id
            db.session.commit()
            study_attempt = existing

            effective_topic_id = study_attempt.topic_id
            has_structured = (
                EducationalEvidenceAuthority.study_attempt_has_structured_question_results
            )
            if effective_topic_id is not None and has_structured(study_attempt):
                from app.services.adaptive_learning_service import (
                    AdaptiveLearningService,
                )

                AdaptiveLearningService.update_mastery_after_attempt(
                    user_id=user_id,
                    topic_id=effective_topic_id,
                )
        else:
            study_attempt = LearningService.create_study_attempt(
                user_id=user_id,
                mission_id=mission.id,
                topic_id=topic_id,
                study_date=date.today(),
                duration_minutes=duration_minutes,
                questions_attempted=questions_attempted,
                questions_correct=questions_correct,
                notes=practice_notes,
            )

        authorised = (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
                study_attempt
            )
        )

        logger.info(
            "Practice outcome recorded mission=%s user=%s attempted=%s "
            "correct=%s authorised_evidence=%s",
            mission.id,
            user_id,
            questions_attempted,
            questions_correct,
            authorised,
        )
        return PracticeOutcomeResult(
            mission=mission,
            study_attempt=study_attempt,
            authorised_evidence=authorised,
            mission_completed=True,
        )

    @staticmethod
    def _completion_status_from_attempt_notes(notes: str | None) -> str | None:
        """Parse LXP-002 session completion marker from attempt notes."""
        if not notes:
            return None
        for key, label in COMPLETION_LABELS.items():
            if f"Session completion: {label}" in notes:
                return key
        return None

    @staticmethod
    def resolve_feedback_scenario(
        mission: Mission,
        study_attempt: StudyAttempt | None,
    ) -> str:
        """Determine which LXP-004 feedback scenario applies.

        Uses persisted mission and attempt state only — never invents outcomes.
        """
        if study_attempt is not None and (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
                study_attempt
            )
        ):
            return FEEDBACK_PRACTICE_RECORDED

        completion = StudySessionService._completion_status_from_attempt_notes(
            study_attempt.notes if study_attempt is not None else None
        )
        if completion == COMPLETION_PARTIAL:
            return FEEDBACK_PARTIAL
        if completion == COMPLETION_NO:
            return FEEDBACK_ABANDONED
        if mission.status != "Completed":
            return FEEDBACK_ABANDONED

        return FEEDBACK_NO_PRACTICE

    @staticmethod
    def build_session_feedback(
        mission_id: int,
        user_id: int,
        *,
        topic_title: str | None = None,
        study_progress_updated: bool = False,
    ) -> "StudySessionFeedbackNarrative":
        """Assemble LXP-004 feedback narrative for a mission-owned session.

        Args:
            mission_id: Daily mission id.
            user_id: Owning student id.
            topic_title: Optional override for student-facing topic label.
            study_progress_updated: Whether Study Progress was updated on close.

        Returns:
            StudySessionFeedbackNarrative from EducationalExplainabilityService.

        Raises:
            ValueError: When the mission is missing or not owned.
        """
        from app.services.educational_explainability_service import (
            EducationalExplainabilityService,
        )

        mission = StudySessionService.get_owned_mission(mission_id, user_id)
        attempt = StudySessionService._find_latest_attempt_for_mission(
            user_id, mission.id
        )
        scenario = StudySessionService.resolve_feedback_scenario(mission, attempt)
        label = topic_title or mission.title or "Today's topic"

        questions_attempted = None
        questions_correct = None
        duration_minutes = None
        if attempt is not None:
            questions_attempted = attempt.questions_attempted
            questions_correct = attempt.questions_correct
            duration_minutes = attempt.duration_minutes

        return EducationalExplainabilityService.build_study_session_feedback(
            topic_title=label,
            scenario=scenario,
            questions_attempted=questions_attempted,
            questions_correct=questions_correct,
            duration_minutes=duration_minutes,
            study_progress_updated=study_progress_updated,
            mission_status=mission.status,
        )

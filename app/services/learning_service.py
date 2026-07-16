"""Service for managing learning data and student progress."""

from __future__ import annotations

from datetime import date

from app.extensions import db
from app.models.learning import LearningObjective, Mistake, StudyAttempt
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress
from app.services.curriculum_service import CurriculumService
from app.services.educational_evidence_authority import EducationalEvidenceAuthority


class LearningService:
    """Service for recording and managing learning outcomes.
    
    Handles creation of study attempts, mistake recording, and progress
    updates based on learning data.
    """

    @staticmethod
    def create_study_attempt(
        user_id: int,
        mission_id: int,
        topic_id: int | None = None,
        study_date: date | None = None,
        duration_minutes: int | None = None,
        questions_attempted: int | None = None,
        questions_correct: int | None = None,
        confidence_before: str | None = None,
        confidence_after: str | None = None,
        notes: str | None = None,
    ) -> StudyAttempt:
        """Create a record of a learning session.
        
        Args:
            user_id: The ID of the user.
            mission_id: The ID of the mission completed.
            topic_id: Optional topic ID (extracted from mission if not provided).
            study_date: Date of the study session (defaults to today).
            duration_minutes: Time spent studying.
            questions_attempted: Total questions attempted.
            questions_correct: Number of questions answered correctly.
            confidence_before: Confidence level before studying.
            confidence_after: Confidence level after studying.
            notes: Student's reflection on the session.
        
        Returns:
            StudyAttempt: The created study attempt record.
        
        Raises:
            ValueError: If mission_id is invalid or user_id is invalid.
        """
        if study_date is None:
            study_date = date.today()

        # Verify mission exists and belongs to user
        mission = Mission.query.get(mission_id)
        if not mission or mission.user_id != user_id:
            raise ValueError(f"Invalid mission_id {mission_id} for user {user_id}")

        # Create study attempt
        study_attempt = StudyAttempt(
            user_id=user_id,
            mission_id=mission_id,
            topic_id=topic_id,
            study_date=study_date,
            duration_minutes=duration_minutes,
            questions_attempted=questions_attempted,
            questions_correct=questions_correct,
            confidence_before=confidence_before,
            confidence_after=confidence_after,
            notes=notes,
        )
        db.session.add(study_attempt)
        db.session.commit()

        # EIP-001 / EIP-002 observation vs evidence:
        # - Confidence / duration / notes are Educational Observations only.
        # - They must never mint Educational Evidence of understanding.
        # - Twin estimates update only when authorised Structured Question
        #   Results are present (Constitution Art. V; EL-005–EL-007).
        if topic_id and confidence_after:
            LearningService._record_student_confidence(
                user_id=user_id,
                topic_id=topic_id,
                confidence_after=confidence_after,
            )

        has_authorised = topic_id is not None and (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
                study_attempt
            )
        )
        if has_authorised:
            from app.services.adaptive_learning_service import AdaptiveLearningService

            AdaptiveLearningService.update_mastery_after_attempt(
                user_id=user_id,
                topic_id=topic_id,
            )

        return study_attempt

    @staticmethod
    def record_mistake(
        study_attempt_id: int,
        description: str,
        topic_id: int | None = None,
        mistake_type: str | None = None,
        correct_solution: str | None = None,
    ) -> Mistake:
        """Record a mistake made during a study session.
        
        Args:
            study_attempt_id: The ID of the study attempt.
            description: What the student did wrong.
            topic_id: Optional topic associated with the mistake.
            mistake_type: Category of mistake (Calculation, Concept, etc.).
            correct_solution: The correct approach or answer.
        
        Returns:
            Mistake: The created mistake record.
        
        Raises:
            ValueError: If study_attempt_id is invalid.
        """
        study_attempt = StudyAttempt.query.get(study_attempt_id)
        if not study_attempt:
            raise ValueError(f"Invalid study_attempt_id {study_attempt_id}")

        # Use study attempt's topic if not provided
        if topic_id is None:
            topic_id = study_attempt.topic_id

        mistake = Mistake(
            study_attempt_id=study_attempt_id,
            topic_id=topic_id,
            mistake_type=mistake_type,
            description=description,
            correct_solution=correct_solution,
            resolved=False,
        )
        db.session.add(mistake)
        db.session.commit()

        return mistake

    @staticmethod
    def _record_student_confidence(
        user_id: int,
        topic_id: int,
        confidence_after: str,
    ) -> TopicProgress:
        """Record student-felt confidence without mutating ownership-bound states.

        EIP-001 / EIP-002 / EL-005 / Constitution IV.10:
        - Student-felt confidence may be stored as an Educational Observation.
        - Confidence must NEVER modify Study Progress (``completed``).
        - Confidence must NEVER modify Estimated Mastery / Estimated Knowledge.
        - Confidence must NEVER enter Educational Evidence of understanding
          (V1.0 authorised catalogue excludes it).

        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.
            confidence_after: Reported confidence level after studying.

        Returns:
            TopicProgress: The progress record with confidence updated when valid.
        """
        progress = CurriculumService.get_or_create_topic_progress(
            user_id=user_id,
            topic_id=topic_id,
        )

        valid_confidence = {"Not Started", "Low", "Medium", "High", "Mastered"}
        if confidence_after in valid_confidence:
            progress.confidence = confidence_after
            db.session.commit()

        return progress

    @staticmethod
    def get_study_attempts_for_topic(
        user_id: int,
        topic_id: int,
        limit: int | None = None,
    ) -> list[StudyAttempt]:
        """Get all study attempts for a user on a specific topic.
        
        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.
            limit: Maximum number of attempts to return (None = no limit).
        
        Returns:
            list[StudyAttempt]: Study attempts ordered by most recent first.
        """
        query = StudyAttempt.query.filter_by(
            user_id=user_id,
            topic_id=topic_id,
        ).order_by(StudyAttempt.study_date.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    @staticmethod
    def get_recent_study_attempts(
        user_id: int,
        limit: int = 10,
    ) -> list[StudyAttempt]:
        """Get recent study attempts for a user.
        
        Args:
            user_id: The ID of the user.
            limit: Maximum number of attempts to return (default 10).
        
        Returns:
            list[StudyAttempt]: Most recent study attempts.
        """
        return (
            StudyAttempt.query.filter_by(user_id=user_id)
            .order_by(StudyAttempt.study_date.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_mistakes_for_topic(
        user_id: int,
        topic_id: int,
        unresolved_only: bool = False,
    ) -> list[Mistake]:
        """Get mistakes made by a user on a specific topic.
        
        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.
            unresolved_only: If True, only return unresolved mistakes.
        
        Returns:
            list[Mistake]: Mistakes ordered by most recent first.
        """
        query = (
            Mistake.query.join(StudyAttempt)
            .filter(
                StudyAttempt.user_id == user_id,
                Mistake.topic_id == topic_id,
            )
            .order_by(Mistake.created_at.desc())
        )

        if unresolved_only:
            query = query.filter(Mistake.resolved == False)

        return query.all()

    @staticmethod
    def mark_mistake_resolved(mistake_id: int) -> Mistake:
        """Mark a mistake as resolved (student now understands it).
        
        Args:
            mistake_id: The ID of the mistake.
        
        Returns:
            Mistake: The updated mistake record.
        
        Raises:
            ValueError: If mistake_id is invalid.
        """
        mistake = Mistake.query.get(mistake_id)
        if not mistake:
            raise ValueError(f"Invalid mistake_id {mistake_id}")

        mistake.resolved = True
        db.session.commit()
        return mistake

    @staticmethod
    def get_learning_objectives_for_topic(
        topic_id: int,
        active_only: bool = True,
    ) -> list[LearningObjective]:
        """Get learning objectives for a topic.
        
        Args:
            topic_id: The ID of the topic.
            active_only: If True, only return active objectives.
        
        Returns:
            list[LearningObjective]: Ordered by 'order' field.
        """
        query = LearningObjective.query.filter_by(topic_id=topic_id).order_by(
            LearningObjective.order
        )

        if active_only:
            query = query.filter_by(active=True)

        return query.all()

    @staticmethod
    def calculate_topic_mastery(
        user_id: int,
        topic_id: int,
    ) -> dict:
        """Calculate mastery metrics for a user on a topic.
        
        Returns a dictionary with:
        - total_attempts: Number of study sessions
        - average_accuracy: Mean percentage correct (if available)
        - last_attempted: Date of most recent attempt
        - confidence_progression: List of confidence levels over time
        - unresolved_mistakes: Number of unresolved mistakes
        
        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.
        
        Returns:
            dict: Mastery metrics.
        """
        attempts = LearningService.get_study_attempts_for_topic(user_id, topic_id)

        total_attempts = len(attempts)
        if total_attempts == 0:
            return {
                "total_attempts": 0,
                "average_accuracy": None,
                "last_attempted": None,
                "confidence_progression": [],
                "unresolved_mistakes": 0,
            }

        # Calculate average accuracy
        accuracies = [
            a.get_accuracy_percentage()
            for a in attempts
            if a.get_accuracy_percentage() is not None
        ]
        average_accuracy = (
            sum(accuracies) / len(accuracies) if accuracies else None
        )

        # Get confidence progression
        confidence_progression = [a.confidence_after for a in attempts if a.confidence_after]

        # Count unresolved mistakes
        unresolved_mistakes = LearningService.get_mistakes_for_topic(
            user_id=user_id,
            topic_id=topic_id,
            unresolved_only=True,
        )

        return {
            "total_attempts": total_attempts,
            "average_accuracy": average_accuracy,
            "last_attempted": attempts[0].study_date if attempts else None,
            "confidence_progression": confidence_progression,
            "unresolved_mistakes": len(unresolved_mistakes),
        }

"""Service for adaptive learning calculations and mastery tracking."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta

from app.extensions import db
from app.models.learning import Mistake, StudyAttempt
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)

# Numeric mapping for confidence levels
CONFIDENCE_NUMERIC = {
    "Not Started": 0,
    "Low": 25,
    "Medium": 50,
    "High": 75,
    "Mastered": 100,
}


class AdaptiveLearningService:
    """Service for adaptive learning calculations.

    Provides deterministic estimate calculations (internal field
    ``mastery_score``; Version 1 student meaning: Estimated Knowledge),
    review scheduling, and topic detection (weak/strong) based on stored
    learning data. No external APIs or AI are used — all calculations are
    purely mathematical.
    """

    # ── Mastery Calculation ──────────────────────────────────────────

    @staticmethod
    def calculate_mastery_score(
        accuracy: float | None,
        confidence_numeric: float | None,
        revision_count: int,
        unresolved_mistakes: int,
    ) -> float:
        """Calculate an estimate scalar from 0 to 100 from authorised accuracy.

        Version 1 student meaning of the returned scalar is Estimated Knowledge
        (EIP-006). The method name and persistence field remain ``mastery_score``
        for compatibility; this is not constitutionally sufficient Estimated
        Mastery (EL-007).

        EIP-002: this formula may interpret authorised Structured Question
        Results (accuracy). It must not mint estimates from activity,
        confidence, or revision alone.

        The formula is a weighted combination of:
        - Accuracy (required for a non-zero estimate write path): average
          percentage correct across authorised attempts
        - Confidence (30%): legacy parameter retained for compatibility —
          EIP-001/EIP-002 forbid student confidence from authoring estimates;
          ``update_mastery_after_attempt`` always passes ``None``.
        - Consistency bonus: capped revision signal only when accuracy exists
        - Penalty: deduction for unresolved mistakes when accuracy exists

        If accuracy is None, returns 0.0 — callers must treat this as
        **correct silence** (do not write Twin estimates from this alone).

        Args:
            accuracy: Average accuracy percentage (0-100), or None.
            confidence_numeric: Numeric confidence (0-100), or None.
            revision_count: Number of times the topic has been reviewed.
            unresolved_mistakes: Number of unresolved mistakes.

        Returns:
            float: Estimated Knowledge scalar from 0 to 100, or 0.0 when
            accuracy is absent.
        """
        # EIP-002: no authorised Educational Evidence ⇒ no artificial estimate.
        if accuracy is None:
            return 0.0

        score = 0.0
        total_weight = 0.0

        # Accuracy component (weight: 0.40)
        score += accuracy * 0.40
        total_weight += 0.40

        # Confidence component (weight: 0.30) — never used on live estimate path.
        if confidence_numeric is not None:
            score += confidence_numeric * 0.30
            total_weight += 0.30

        score = score / total_weight

        # Consistency bonus only as soft modifier on authorised evidence.
        consistency_bonus = min(revision_count, 5) * 2.0  # max 10
        score += consistency_bonus

        # Unresolved mistakes penalty: -5 per unresolved mistake (max -20)
        mistake_penalty = min(unresolved_mistakes, 4) * 5.0
        score -= mistake_penalty

        # Clamp to 0-100
        return max(0.0, min(100.0, score))

    @staticmethod
    def determine_stage(mastery_score: float) -> str:
        """Determine the learning stage based on mastery score.

        Args:
            mastery_score: The calculated mastery score (0-100).

        Returns:
            str: One of 'Not Started', 'Learning', 'Practising', 'Mastered', 'Needs Review'.
        """
        if mastery_score >= 90:
            return TopicProgress.STAGE_MASTERED
        elif mastery_score >= 70:
            return TopicProgress.STAGE_PRACTISING
        elif mastery_score >= 30:
            return TopicProgress.STAGE_LEARNING
        else:
            return TopicProgress.STAGE_NOT_STARTED

    @staticmethod
    def get_confidence_numeric(confidence: str | None) -> float | None:
        """Convert a confidence string to its numeric equivalent.

        Args:
            confidence: Confidence level string (e.g., 'Low', 'Medium').

        Returns:
            float | None: Numeric confidence 0-100, or None if not recognized.
        """
        if confidence is None:
            return None
        return CONFIDENCE_NUMERIC.get(confidence)

    # ── Review Scheduling ────────────────────────────────────────────

    @staticmethod
    def schedule_next_review(mastery_score: float, last_reviewed: datetime | None = None) -> date:
        """Determine the next review date based on mastery score.

        Spaced-repetition-style scheduling:
        - Mastery >= 90: review in 14 days
        - Mastery >= 70: review in 7 days
        - Mastery >= 50: review in 3 days
        - Mastery >= 30: review in 2 days
        - Mastery < 30: review tomorrow

        Args:
            mastery_score: The calculated mastery score (0-100).
            last_reviewed: The datetime of the last review (defaults to today).

        Returns:
            date: The scheduled next review date.
        """
        today = date.today()
        if last_reviewed and hasattr(last_reviewed, "date"):
            today = last_reviewed.date()
        elif isinstance(last_reviewed, datetime):
            today = last_reviewed.date()

        if mastery_score >= 90:
            return today + timedelta(days=14)
        elif mastery_score >= 70:
            return today + timedelta(days=7)
        elif mastery_score >= 50:
            return today + timedelta(days=3)
        elif mastery_score >= 30:
            return today + timedelta(days=2)
        else:
            return today + timedelta(days=1)

    # ── Update After Study Attempt ───────────────────────────────────

    @staticmethod
    def update_mastery_after_attempt(
        user_id: int,
        topic_id: int,
    ) -> TopicProgress:
        """Recalculate evidence-backed understanding estimate from authorised Educational Evidence.

        Version 1 (EIP-006): the written scalar is student-facing Estimated Knowledge
        (understanding posture), not constitutionally sufficient Estimated Mastery.

        EIP-002 Evidence Authority: Twin-owned Estimated Knowledge may be mutated
        only when V1.0 authorised evidence exists (Structured Question Results and
        future quiz / assessment pathways). Absence of authorised evidence leaves
        estimates unchanged — correct silence. Estimated Mastery remains a defined
        educational construct (EL-007) but is not a Version 1 student-facing state.

        Ownership invariants enforced here:
        - Student confidence is ignored in the mastery formula (EL-005 / IV.10).
        - Study Progress (``completed``) is never written (EL-001 / FINDING-001).
        - Mission completion, time spent, revision count alone never write
          estimates (EL-004 / EL-006 / EL-007 / FINDING-003).

        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.

        Returns:
            TopicProgress: Progress record; estimate fields updated only when
            authorised evidence is present.
        """
        from app.services.curriculum_service import CurriculumService
        from app.services.educational_evidence_authority import (
            EducationalEvidenceAuthority,
        )

        progress = CurriculumService.get_or_create_topic_progress(
            user_id=user_id,
            topic_id=topic_id,
        )

        attempts = StudyAttempt.query.filter_by(
            user_id=user_id,
            topic_id=topic_id,
        ).order_by(StudyAttempt.study_date.asc()).all()

        accuracies = EducationalEvidenceAuthority.collect_authorised_accuracies(
            attempts
        )

        # EIP-002: no authorised Educational Evidence ⇒ leave Twin estimates alone.
        if not accuracies:
            logger.info(
                "No authorised Educational Evidence for user=%d topic=%d; "
                "leaving Estimated Knowledge/Mastery unchanged",
                user_id,
                topic_id,
            )
            return progress

        unresolved_mistakes = Mistake.query.join(StudyAttempt).filter(
            StudyAttempt.user_id == user_id,
            Mistake.topic_id == topic_id,
            Mistake.resolved == False,
        ).count()

        avg_accuracy = sum(accuracies) / len(accuracies)

        # Soft confidence average for display only — never formula input,
        # never Educational Evidence of understanding (EIP-002).
        confidence_after_values = [
            AdaptiveLearningService.get_confidence_numeric(a.confidence_after)
            for a in attempts
            if a.confidence_after
            and AdaptiveLearningService.get_confidence_numeric(a.confidence_after)
            is not None
        ]
        avg_confidence = (
            (sum(confidence_after_values) / len(confidence_after_values))
            if confidence_after_values
            else None
        )

        mastery_score = AdaptiveLearningService.calculate_mastery_score(
            accuracy=avg_accuracy,
            confidence_numeric=None,
            revision_count=progress.revision_count,
            unresolved_mistakes=unresolved_mistakes,
        )

        current_stage = AdaptiveLearningService.determine_stage(mastery_score)
        # EL-007 / FINDING-007: Mastered-stage language requires accumulation.
        if (
            current_stage == TopicProgress.STAGE_MASTERED
            and not EducationalEvidenceAuthority.may_assign_high_mastery_stage(
                len(accuracies)
            )
        ):
            current_stage = TopicProgress.STAGE_PRACTISING

        next_review = AdaptiveLearningService.schedule_next_review(
            mastery_score=mastery_score,
            last_reviewed=progress.last_reviewed,
        )

        # Twin-owned estimate fields only — never Study Progress (EIP-001).
        progress.mastery_score = round(mastery_score, 1)
        progress.average_accuracy = round(avg_accuracy, 1)
        progress.average_confidence = (
            round(avg_confidence, 1) if avg_confidence is not None else None
        )
        progress.next_review_date = next_review
        if not progress.completed:
            progress.current_stage = current_stage

        db.session.commit()

        logger.info(
            "Mastery updated from authorised evidence for user=%d topic=%d: "
            "score=%.1f stage=%s next_review=%s observations=%d",
            user_id,
            topic_id,
            mastery_score,
            current_stage,
            next_review,
            len(accuracies),
        )

        return progress

    # ── Weak / Mastered Topic Detection ──────────────────────────────

    @staticmethod
    def get_weak_topics(user_id: int, threshold: float = 60.0) -> list[TopicProgress]:
        """Get topics with mastery score below the threshold.

        Only returns topics that have been started (revision_count > 0).

        Args:
            user_id: The ID of the user.
            threshold: Mastery score threshold (default 60).

        Returns:
            list[TopicProgress]: Weak topics ordered by mastery (lowest first).
        """
        return (
            TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.revision_count > 0,
                TopicProgress.mastery_score < threshold,
            )
            .order_by(TopicProgress.mastery_score.asc())
            .all()
        )

    @staticmethod
    def get_mastered_topics(user_id: int, threshold: float = 90.0) -> list[TopicProgress]:
        """Get topics that have been mastered.

        Args:
            user_id: The ID of the user.
            threshold: Mastery score threshold for mastery (default 90).

        Returns:
            list[TopicProgress]: Mastered topics ordered by mastery (highest first).
        """
        return (
            TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.current_stage == TopicProgress.STAGE_MASTERED,
                TopicProgress.mastery_score >= threshold,
            )
            .order_by(TopicProgress.mastery_score.desc())
            .all()
        )

    @staticmethod
    def get_topics_due_for_review(user_id: int, target_date: date | None = None) -> list[TopicProgress]:
        """Get topics whose next review date is on or before the target date.

        Args:
            user_id: The ID of the user.
            target_date: Date to check (defaults to today).

        Returns:
            list[TopicProgress]: Topics due for review, ordered by review date.
        """
        if target_date is None:
            target_date = date.today()

        return (
            TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.next_review_date.isnot(None),
                TopicProgress.next_review_date <= target_date,
                TopicProgress.current_stage != TopicProgress.STAGE_MASTERED,
            )
            .order_by(TopicProgress.next_review_date.asc())
            .all()
        )

    # ── Dashboard Analytics ──────────────────────────────────────────

    @staticmethod
    def get_learning_snapshot(user_id: int) -> dict:
        """Generate a comprehensive learning snapshot for the dashboard.

        Returns:
        - overall_mastery: Average mastery across all started topics.
        - topics_mastered: Number of topics at 'Mastered' stage.
        - total_topics_started: Number of topics with at least one review.
        - weakest_topic: TopicProgress with lowest mastery score (or None).
        - reviews_due_today: Number of topics due for review.
        - current_streak: Consecutive days with at least one study attempt.
        """
        # Overall mastery: average across all started topics
        started_topics = TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.revision_count > 0,
        ).all()

        if started_topics:
            overall_mastery = sum(t.mastery_score for t in started_topics) / len(started_topics)
        else:
            overall_mastery = 0.0

        # Topics mastered
        topics_mastered = TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.current_stage == TopicProgress.STAGE_MASTERED,
        ).count()

        # Weakest topic
        weakest_topic = (
            TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.revision_count > 0,
            )
            .order_by(TopicProgress.mastery_score.asc())
            .first()
        )

        # Reviews due today
        today = date.today()
        reviews_due_today = TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.next_review_date.isnot(None),
            TopicProgress.next_review_date <= today,
            TopicProgress.current_stage != TopicProgress.STAGE_MASTERED,
        ).count()

        # Current streak: consecutive days with a study attempt
        current_streak = AdaptiveLearningService._calculate_streak(user_id)

        return {
            "overall_mastery": round(overall_mastery, 1),
            "topics_mastered": topics_mastered,
            "total_topics_started": len(started_topics),
            "weakest_topic": weakest_topic,
            "reviews_due_today": reviews_due_today,
            "current_streak": current_streak,
        }

    @staticmethod
    def _calculate_streak(user_id: int) -> int:
        """Calculate the current consecutive-day study streak.

        Args:
            user_id: The ID of the user.

        Returns:
            int: Number of consecutive days (including today) with a study attempt.
        """
        from sqlalchemy import func

        # Get distinct study dates ordered descending
        rows = (
            db.session.query(StudyAttempt.study_date)
            .filter(StudyAttempt.user_id == user_id)
            .distinct()
            .order_by(StudyAttempt.study_date.desc())
            .all()
        )

        if not rows:
            return 0

        today = date.today()
        dates = [row[0] for row in rows]

        streak = 0
        expected = today

        for d in dates:
            if d == expected:
                streak += 1
                expected = d - timedelta(days=1)
            elif d == expected - timedelta(days=1):
                # Allow one-day gap (e.g., didn't study yesterday but studied today)
                # However, we break the streak if we're already past the first date
                break
            else:
                break

        return streak

    # ── Daily Briefing ───────────────────────────────────────────────

    @staticmethod
    def generate_daily_briefing(user_id: int) -> str:
        """Generate a plain-English daily briefing paragraph.

        Summarises yesterday's performance and today's priorities.

        Args:
            user_id: The ID of the user.

        Returns:
            str: A briefing paragraph.
        """
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Yesterday's attempts
        yesterday_attempts = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date == yesterday,
        ).all()

        yesterday_mission_count = len(set(a.mission_id for a in yesterday_attempts))
        yesterday_total_questions = sum(
            a.questions_attempted for a in yesterday_attempts if a.questions_attempted
        )
        yesterday_total_correct = sum(
            a.questions_correct for a in yesterday_attempts if a.questions_correct
        )

        if yesterday_total_questions > 0:
            yesterday_accuracy = round(
                (yesterday_total_correct / yesterday_total_questions) * 100, 1
            )
        else:
            yesterday_accuracy = None

        # Today's priorities
        reviews_due = AdaptiveLearningService.get_topics_due_for_review(user_id, today)
        weak_topics = AdaptiveLearningService.get_weak_topics(user_id, threshold=60.0)

        # Build briefing
        parts = []

        # Yesterday summary
        if yesterday_mission_count > 0:
            part1 = (
                f"Yesterday you completed {yesterday_mission_count} "
                f"mission{'s' if yesterday_mission_count != 1 else ''}"
            )
            if yesterday_total_questions > 0:
                part1 += (
                    f" with {yesterday_total_questions} question{'s' if yesterday_total_questions != 1 else ''} "
                    f"and scored {yesterday_accuracy}% accuracy"
                )
            part1 += "."
        else:
            part1 = "You did not record any study activity yesterday."

        parts.append(part1)

        # Today's priorities
        priority_items = []

        if reviews_due:
            priority_items.append(
                f"{len(reviews_due)} topic{'s' if len(reviews_due) != 1 else ''} "
                f"due for review"
            )
        if weak_topics:
            weak_not_due = [w for w in weak_topics if w not in reviews_due]
            if weak_not_due:
                priority_items.append(
                    f"{len(weak_not_due)} topic{'s' if len(weak_not_due) != 1 else ''} "
                    f"that still need more practice"
                )
            elif reviews_due:
                # The reviews due include weak topics
                pass

        if priority_items:
            parts.append(
                "Today's priorities: " + "; ".join(priority_items) + "."
            )
        else:
            parts.append(
                "You're up to date with reviews. Continue your curriculum progress."
            )

        return " ".join(parts)

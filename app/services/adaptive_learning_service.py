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

# Exponential half-life (days) for recency-weighted accuracy aggregation.
ACCURACY_RECENCY_HALF_LIFE_DAYS = 21.0


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

        Live formula (when *accuracy* is present)::

            score = accuracy
                    + min(revision_count, 5) * 2.0   # revision bonus, max +10
                    - min(unresolved_mistakes, 4) * 5.0  # mistake penalty, max -20
            score = clamp(score, 0, 100)

        *accuracy* is the caller-supplied base — typically the exponential
        recency-weighted average from
        ``recency_weighted_accuracy`` (21-day half-life). A single fresh
        observation has weight 1 and equals that attempt's accuracy.

        ``confidence_numeric`` is retained for call-signature compatibility
        only. EIP-001/EIP-002 forbid student confidence from authoring
        estimates; ``update_mastery_after_attempt`` always passes ``None``,
        and this method ignores the value when provided.

        If accuracy is None, returns 0.0 — callers must treat this as
        **correct silence** (do not write Twin estimates from this alone).

        Args:
            accuracy: Recency-weighted (or single-observation) accuracy
                percentage (0-100), or None.
            confidence_numeric: Ignored (legacy signature; live path passes None).
            revision_count: Number of times the topic has been reviewed.
            unresolved_mistakes: Number of unresolved mistakes.

        Returns:
            float: Estimated Knowledge scalar from 0 to 100, or 0.0 when
            accuracy is absent.
        """
        # EIP-002: no authorised Educational Evidence ⇒ no artificial estimate.
        if accuracy is None:
            return 0.0

        # confidence_numeric is intentionally unused (EIP-001 / EIP-002).
        _ = confidence_numeric

        score = accuracy

        # Consistency bonus only as soft modifier on authorised evidence.
        consistency_bonus = min(revision_count, 5) * 2.0  # max 10
        score += consistency_bonus

        # Unresolved mistakes penalty: -5 per unresolved mistake (max -20)
        mistake_penalty = min(unresolved_mistakes, 4) * 5.0
        score -= mistake_penalty

        # Clamp to 0-100
        return max(0.0, min(100.0, score))

    @staticmethod
    def recency_weighted_accuracy(
        observations: list[tuple[float, date]],
        *,
        as_of: date | None = None,
    ) -> float:
        """Exponentially recency-weighted mean accuracy (21-day half-life).

        For each authorised observation ``(accuracy_i, study_date_i)``::

            weight_i = 0.5 ** (days_since_attempt_i / 21)
            result = sum(accuracy_i * weight_i) / sum(weight_i)

        ``days_since_attempt_i`` is ``(as_of - study_date_i).days``, floored
        at 0. ``as_of`` defaults to ``date.today()`` so a same-day attempt
        has weight 1.0 (recency weighting is a no-op for a single fresh
        observation).

        Args:
            observations: Non-empty list of ``(accuracy_percent, study_date)``.
            as_of: Reference date for recency (defaults to today).

        Returns:
            float: Recency-weighted accuracy in 0-100.

        Raises:
            ValueError: If *observations* is empty.
        """
        if not observations:
            raise ValueError("observations must be non-empty")

        reference = as_of if as_of is not None else date.today()
        weighted_sum = 0.0
        weight_sum = 0.0
        half_life = ACCURACY_RECENCY_HALF_LIFE_DAYS

        for accuracy, attempt_date in observations:
            days_since = max(0, (reference - attempt_date).days)
            weight = 0.5 ** (days_since / half_life)
            weighted_sum += accuracy * weight
            weight_sum += weight

        return weighted_sum / weight_sum

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
        from app.application.student_twin.cutover import phase2_twin_cutover_enabled
        from app.services.curriculum_service import CurriculumService
        from app.services.educational_evidence_authority import (
            EducationalEvidenceAuthority,
        )

        progress = CurriculumService.get_or_create_topic_progress(
            user_id=user_id,
            topic_id=topic_id,
        )

        # Phase 2 cutover: EK write retired, see ADR-027 Phase 2 design.
        # Stack B (Learner Twin) is the sole EK authority when the atomic
        # KWALITEC_ADR027_PHASE2_TWIN_CUTOVER flag is ON. Study Progress
        # (completed) is never written here regardless of flag state.
        if phase2_twin_cutover_enabled():
            logger.info(
                "Phase 2 cutover: skipping Stack A EK write for user=%d "
                "topic=%d (ADR-027 Phase 2 Stage 2)",
                user_id,
                topic_id,
            )
            return progress

        attempts = StudyAttempt.query.filter_by(
            user_id=user_id,
            topic_id=topic_id,
        ).order_by(StudyAttempt.study_date.asc()).all()

        observations = (
            EducationalEvidenceAuthority.collect_authorised_accuracy_observations(
                attempts
            )
        )

        # EIP-002: no authorised Educational Evidence ⇒ leave Twin estimates alone.
        if not observations:
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

        # Recency-weighted accuracy (21-day half-life) is the formula base and
        # the Twin average_accuracy display value — same scalar the estimate
        # uses, so UI/Twin inspection stays consistent with mastery math.
        avg_accuracy = AdaptiveLearningService.recency_weighted_accuracy(
            observations
        )

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
                len(observations)
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
            len(observations),
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
        from app.application.student_twin.cutover import (
            ek_display_0_100,
            phase2_twin_cutover_enabled,
        )
        from app.services.twin_cutover_service import (
            topic_ek_by_orm_id,
        )

        if phase2_twin_cutover_enabled():
            ek_map = topic_ek_by_orm_id(user_id=user_id)
            if not ek_map:
                return []
            rows = (
                TopicProgress.query.filter(
                    TopicProgress.user_id == user_id,
                    TopicProgress.topic_id.in_(list(ek_map.keys())),
                )
                .all()
            )
            weak: list[tuple[float, TopicProgress]] = []
            for row in rows:
                score = ek_display_0_100(ek_map.get(row.topic_id))
                if score is None or score >= threshold:
                    continue
                # In-memory overlay for callers; do not commit.
                row.mastery_score = score
                weak.append((score, row))
            weak.sort(key=lambda item: item[0])
            return [row for _score, row in weak]

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
        from app.application.student_twin.cutover import (
            ek_display_0_100,
            phase2_twin_cutover_enabled,
        )
        from app.services.twin_cutover_service import (
            topic_ek_by_orm_id,
        )

        if phase2_twin_cutover_enabled():
            ek_map = topic_ek_by_orm_id(user_id=user_id)
            if not ek_map:
                return []
            rows = (
                TopicProgress.query.filter(
                    TopicProgress.user_id == user_id,
                    TopicProgress.topic_id.in_(list(ek_map.keys())),
                )
                .all()
            )
            mastered: list[tuple[float, TopicProgress]] = []
            for row in rows:
                score = ek_display_0_100(ek_map.get(row.topic_id))
                if score is None or score < threshold:
                    continue
                row.mastery_score = score
                mastered.append((score, row))
            mastered.sort(key=lambda item: item[0], reverse=True)
            return [row for _score, row in mastered]

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
        from app.application.student_twin.cutover import (
            ek_display_0_100,
            phase2_twin_cutover_enabled,
        )
        from app.services.twin_cutover_service import (
            topic_ek_by_orm_id,
        )

        if phase2_twin_cutover_enabled():
            ek_map = topic_ek_by_orm_id(user_id=user_id)
            scores = [
                score
                for score in (ek_display_0_100(f) for f in ek_map.values())
                if score is not None
            ]
            overall_mastery = (sum(scores) / len(scores)) if scores else 0.0
            started_topics = (
                TopicProgress.query.filter(
                    TopicProgress.user_id == user_id,
                    TopicProgress.topic_id.in_(list(ek_map.keys())),
                ).all()
                if ek_map
                else []
            )
            weakest_topic = None
            if ek_map and started_topics:
                ranked = sorted(
                    (
                        (ek_display_0_100(ek_map.get(t.topic_id)), t)
                        for t in started_topics
                    ),
                    key=lambda item: (
                        item[0] if item[0] is not None else 999.0,
                        item[1].topic_id,
                    ),
                )
                if ranked and ranked[0][0] is not None:
                    weakest_topic = ranked[0][1]
                    weakest_topic.mastery_score = ranked[0][0]
        else:
            started_topics = TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.revision_count > 0,
            ).all()

            if started_topics:
                overall_mastery = sum(t.mastery_score for t in started_topics) / len(
                    started_topics
                )
            else:
                overall_mastery = 0.0

            weakest_topic = (
                TopicProgress.query.filter(
                    TopicProgress.user_id == user_id,
                    TopicProgress.revision_count > 0,
                )
                .order_by(TopicProgress.mastery_score.asc())
                .first()
            )

        # Topics mastered
        topics_mastered = TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.current_stage == TopicProgress.STAGE_MASTERED,
        ).count()

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

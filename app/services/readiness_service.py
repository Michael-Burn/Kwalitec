"""Service for calculating exam readiness and performance analytics.

All calculations are deterministic. No AI or external APIs are used.

EP-001.3: ``build_readiness_intelligence`` consumes EP-001.1 Canonical
Learner State and optional EP-001.2 planner outputs when Digital Twin
Foundation is enabled. Twin owns learner state; Planner owns planning;
this service owns readiness evaluation. Legacy getters remain unchanged
so ``ReadinessCollector`` does not recurse through Foundation.

EP-003.2: student-facing readiness surfaces and intelligence assessments
attach the P-001.2 explanation schema (drivers, confidence, evidence,
change reasoning, next action) via ``readiness_quality``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.curriculum import Topic
from app.models.learning import Mistake, StudyAttempt
from app.models.mission import Mission
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReadinessSummary:
    """Read-only summary of exam readiness calculated from a
    StudentCurriculumSummary.

    Attributes:
        readiness_percentage: The weighted completed percentage
            (0.0 to 1.0), representing the proportion of syllabus
            weighting covered by completed topics.
        weighted_completed_percentage: Mirrored from
            StudentCurriculumSummary.
        weighted_remaining_percentage: Mirrored from
            StudentCurriculumSummary.
        explanation: A deterministic human-readable sentence describing
            readiness.
    """

    readiness_percentage: float
    weighted_completed_percentage: float
    weighted_remaining_percentage: float
    explanation: str


class ReadinessService:
    """Service for calculating exam readiness and performance analytics.

    Provides deterministic calculations based on stored learning data:
    - Overall Readiness Score
    - Curriculum Coverage
    - Review Completion Rate
    - Review Backlog
    - Current & Longest Streak
    - Weakest & Strongest Topics

    EP-001.3: ``build_readiness_intelligence`` packages score, confidence,
    strongest/weakest areas, drivers, and recommended next actions from
    Canonical Learner State (+ optional planner daily plan).

    EP-003.2: student-facing surfaces and assessments attach the P-001.2
    readiness explanation schema via ``readiness_quality`` (drivers,
    confidence labels, evidence, change reasoning, next action).
    """

    # ── Readiness Intelligence (EP-001.3) ─────────────────────────────

    @staticmethod
    def build_readiness_intelligence(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
        daily_plan: dict[str, Any] | None = None,
        include_planner: bool = True,
    ) -> dict[str, Any] | None:
        """Build a readiness intelligence assessment from Canonical Learner State.

        When Digital Twin Foundation is unavailable (flag OFF or assemble
        failure), returns ``None`` so callers continue using legacy getters
        (``get_overall_readiness``, weak/strong topics). Does not invent
        learner state, does not plan missions, and does not alter
        ``get_overall_readiness`` (collector recursion safety).

        Args:
            user_id: The ID of the user.
            foundation: Optional injected ``StudentDigitalTwinFoundation``.
            canonical_state: Optional already-assembled
                ``CanonicalLearnerState`` (EP-002.2 shared DI).
            daily_plan: Optional injected EP-001.2 daily plan dict.
            include_planner: When True and ``daily_plan`` is omitted, attempt
                ``PlanningService.build_daily_study_plan`` for next actions.

        Returns:
            Serialisable readiness intelligence dict, or None when Twin is
            unavailable.
        """
        from app.infrastructure.adapters.consumer_chain import (
            API_BUILD_READINESS_INTELLIGENCE,
            SERVICE_READINESS,
            observe_build_api,
        )

        return observe_build_api(
            service_name=SERVICE_READINESS,
            api_name=API_BUILD_READINESS_INTELLIGENCE,
            user_id=user_id,
            call=lambda: ReadinessService._build_readiness_intelligence_body(
                user_id,
                foundation=foundation,
                canonical_state=canonical_state,
                daily_plan=daily_plan,
                include_planner=include_planner,
            ),
        )

    @staticmethod
    def _build_readiness_intelligence_body(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
        daily_plan: dict[str, Any] | None = None,
        include_planner: bool = True,
    ) -> dict[str, Any] | None:
        """Internal readiness intelligence body (observability wraps public API)."""
        twin_foundation = foundation
        if twin_foundation is None:
            twin_foundation = ReadinessService._resolve_twin_foundation()
        if twin_foundation is None or not getattr(
            twin_foundation, "is_enabled", lambda: False
        )():
            return None

        from app.infrastructure.adapters.consumer_chain import (
            API_BUILD_READINESS_INTELLIGENCE,
            SERVICE_READINESS,
            assemble_shared_canonical_state,
        )
        from app.infrastructure.adapters.digital_twin.contracts import (
            AVAILABILITY_AVAILABLE,
        )
        from app.infrastructure.adapters.readiness_intelligence import (
            build_canonical_readiness_consumer,
            build_readiness_assessment_assembler,
        )

        state = assemble_shared_canonical_state(
            twin_foundation,
            str(user_id),
            canonical_state=canonical_state,
            service_name=SERVICE_READINESS,
            api_name=API_BUILD_READINESS_INTELLIGENCE,
        )
        plan_payload = daily_plan
        if plan_payload is None and include_planner:
            plan_payload = ReadinessService._resolve_daily_plan(
                user_id,
                foundation=twin_foundation,
                canonical_state=state,
            )

        inputs = build_canonical_readiness_consumer().project(
            state, daily_plan=plan_payload
        )
        if inputs.availability != AVAILABILITY_AVAILABLE:
            logger.debug(
                "Canonical Learner State unavailable for readiness user %s (%s)",
                user_id,
                inputs.unavailable_reason,
            )
            return None

        assessment = build_readiness_assessment_assembler().assemble(inputs)
        payload = assessment.to_dict()
        from app.services.readiness_quality import (
            apply_readiness_quality_to_assessment,
        )

        result = apply_readiness_quality_to_assessment(user_id, payload)
        ReadinessService._emit_consistency_feedback(user_id)
        return result

    @staticmethod
    def get_dashboard_readiness_surface(
        user_id: int,
        *,
        weak_limit: int = 3,
        strong_limit: int = 3,
    ) -> dict[str, Any]:
        """Dashboard/analytics readiness surface with EP-002.6 gated cutover.

        Eligible non-production requests may receive a Twin Readiness
        Intelligence projection (score + weak/strong topic lists). Otherwise
        returns the legacy surface. Fail-open: Twin failures and blocking
        limitations fall back to legacy getters.

        Collectors and Adaptive TwinInput must continue calling
        ``get_overall_readiness`` directly — this facade is HTTP-surface only.
        """
        import time

        from app.infrastructure.adapters.consumer_chain.readiness_cutover import (
            is_readiness_cutover_active,
            is_readiness_intelligence_cutover_eligible,
            run_readiness_intelligence_http_cutover,
        )
        from app.services.readiness_quality import apply_readiness_quality_contract

        if (
            is_readiness_intelligence_cutover_eligible()
            or is_readiness_cutover_active()
        ):
            surface = run_readiness_intelligence_http_cutover(
                user_id,
                weak_limit=weak_limit,
                strong_limit=strong_limit,
            )
            result = apply_readiness_quality_contract(user_id, surface)
            ReadinessService._emit_consistency_feedback(user_id)
            return result

        started = time.perf_counter()
        surface = {
            "readiness": dict(ReadinessService.get_overall_readiness(user_id) or {}),
            "weakest_topics": list(
                ReadinessService.get_weakest_topics(user_id, limit=weak_limit) or []
            ),
            "strongest_topics": list(
                ReadinessService.get_strongest_topics(user_id, limit=strong_limit)
                or []
            ),
            "source_authority": "legacy",
            "confidence_level": "",
            "limitations_codes": [],
            "readiness_drivers": [],
            "recommended_next_actions": [],
            "explainability": {},
        }
        ReadinessService._maybe_readiness_dual_run(
            user_id,
            surface,
            legacy_latency_ms=(time.perf_counter() - started) * 1000.0,
        )
        result = apply_readiness_quality_contract(user_id, surface)
        ReadinessService._emit_consistency_feedback(user_id)
        ReadinessService.consume_personal_learning_profile(user_id)
        return result

    @staticmethod
    def _emit_consistency_feedback(user_id: int) -> None:
        """EP-003.4: emit study-consistency observation (fail-open).

        Dashboard surface only — ``get_overall_readiness`` remains collector-safe
        and does not emit feedback.
        """
        try:
            from app.infrastructure.adapters.learning_feedback import (
                emit_study_consistency_feedback,
            )

            current = int(ReadinessService.get_current_streak(user_id) or 0)
            longest = int(ReadinessService.get_longest_streak(user_id) or 0)
            emit_study_consistency_feedback(
                user_id=user_id,
                current_streak=current,
                longest_streak=longest,
            )
        except Exception:  # noqa: BLE001 — feedback must never break readiness
            logger.debug(
                "learning_feedback_consistency_emit_failed user_id=%s",
                user_id,
                exc_info=True,
            )

    @staticmethod
    def consume_personal_learning_profile(
        user_id: int,
        *,
        declared_session_minutes: int | None = None,
    ) -> dict | None:
        """EP-004.1: optional Personal Learning Profile input (fail-open).

        Returns observed behavioural attributes for optional personalisation
        inputs. Never changes readiness scores, drivers, or collector paths —
        profile summarises evidence only. ``get_overall_readiness`` does not
        call this method (collector-safe).
        """
        try:
            from app.infrastructure.adapters.personal_learning_profile import (
                consume_personal_learning_profile,
            )

            return consume_personal_learning_profile(
                student_id=user_id,
                declared_session_minutes=declared_session_minutes,
            )
        except Exception:  # noqa: BLE001 — profile must never break readiness
            logger.debug(
                "personal_learning_profile_consume_failed user_id=%s",
                user_id,
                exc_info=True,
            )
            return None

    @staticmethod
    def _maybe_readiness_dual_run(
        user_id: int,
        surface: dict[str, Any],
        *,
        legacy_latency_ms: float | None = None,
    ) -> None:
        """EP-002.6 fail-open Readiness Intelligence dual-run (diagnostic only).

        Never mutates ``surface``. Skipped when cutover is eligible or active.
        """
        try:
            from app.infrastructure.adapters.consumer_chain.readiness_cutover import (
                is_readiness_cutover_active,
                is_readiness_intelligence_cutover_eligible,
            )

            if (
                is_readiness_cutover_active()
                or is_readiness_intelligence_cutover_eligible()
            ):
                return

            from app.infrastructure.adapters.consumer_chain.readiness_dual_run import (
                run_readiness_intelligence_dual_run,
            )

            run_readiness_intelligence_dual_run(
                user_id,
                surface,
                legacy_latency_ms=legacy_latency_ms,
            )
        except Exception:  # noqa: BLE001 — dual-run must never break student path
            logger.debug(
                "readiness_dual_run_hook_failed user_id=%s",
                user_id,
                exc_info=True,
            )

    @staticmethod
    def _resolve_twin_foundation() -> object | None:
        """Resolve EP-001.1 Foundation when Digital Twin flag is ON."""
        from app.infrastructure.adapters.consumer_chain import (
            resolve_enabled_twin_foundation,
        )

        return resolve_enabled_twin_foundation()

    @staticmethod
    def _resolve_daily_plan(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
    ) -> dict[str, Any] | None:
        """Best-effort EP-001.2 daily plan for next-action grounding."""
        try:
            from app.services.planning_service import PlanningService

            return PlanningService.build_daily_study_plan(
                user_id,
                foundation=foundation,
                canonical_state=canonical_state,
            )
        except Exception:  # noqa: BLE001
            logger.debug(
                "Planner outputs unavailable for readiness user %s",
                user_id,
                exc_info=True,
            )
            return None

    # ── Overall Readiness Score ───────────────────────────────────────

    @staticmethod
    def get_overall_readiness(user_id: int) -> dict:
        """Calculate overall exam readiness.

        The readiness score is a weighted composite of:
        - Curriculum Coverage (50%): percentage of leaf topics started
        - Average Estimated Knowledge (30%): mean evidence-backed estimate
          across started topics
        - Review Discipline (20%): based on review completion rate

        Args:
            user_id: The ID of the user.

        Returns:
            dict with keys: score, coverage_pct, avg_mastery, review_discipline,
                           total_topics, topics_started, topics_mastered.
        """
        leaf_topics = ReadinessService._get_leaf_topics()
        total_topics = len(leaf_topics)
        leaf_ids = [t.id for t in leaf_topics]

        if total_topics == 0:
            return {
                "score": 0.0,
                "coverage_pct": 0.0,
                "avg_mastery": 0.0,
                "review_discipline": 0.0,
                "total_topics": 0,
                "topics_started": 0,
                "topics_mastered": 0,
            }

        progress_rows = TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.topic_id.in_(leaf_ids),
        ).all()

        topics_started = 0
        topics_mastered = 0
        mastery_sum = 0.0
        for row in progress_rows:
            if row.revision_count > 0:
                topics_started += 1
                mastery_sum += row.mastery_score
            if row.current_stage == TopicProgress.STAGE_MASTERED:
                topics_mastered += 1

        avg_mastery_score = (
            mastery_sum / topics_started if topics_started > 0 else 0.0
        )
        review_completion = ReadinessService.get_review_completion_rate(user_id)
        coverage_pct = (topics_started / total_topics) * 100
        review_discipline = review_completion["completion_rate"]

        # Weighted composite: Coverage 50%, Mastery 30%, Review Discipline 20%
        score = (
            (coverage_pct * 0.50)
            + (avg_mastery_score * 0.30)
            + (review_discipline * 0.20)
        )

        return {
            "score": round(score, 1),
            "coverage_pct": round(coverage_pct, 1),
            "avg_mastery": round(avg_mastery_score, 1),
            "review_discipline": round(review_discipline, 1),
            "total_topics": total_topics,
            "topics_started": topics_started,
            "topics_mastered": topics_mastered,
        }

    # ── Curriculum Coverage ───────────────────────────────────────────

    @staticmethod
    def get_curriculum_coverage(user_id: int) -> dict:
        """Calculate curriculum coverage across all leaf topics.

        A leaf topic is one without subtopics (the most granular learning unit).

        Args:
            user_id: The ID of the user.

        Returns:
            dict with keys: total_leaf_topics, topics_started, topics_not_started,
                           topics_mastered, coverage_percentage.
        """
        leaf_topics = ReadinessService._get_leaf_topics()
        total = len(leaf_topics)

        if total == 0:
            return {
                "total_leaf_topics": 0,
                "topics_started": 0,
                "topics_not_started": 0,
                "topics_mastered": 0,
                "coverage_percentage": 0.0,
            }

        # Get all topic progress for this user
        progress_map: dict[int, TopicProgress] = {}
        user_progress = TopicProgress.query.filter_by(user_id=user_id).all()
        for p in user_progress:
            progress_map[p.topic_id] = p

        started = 0
        mastered = 0
        for topic in leaf_topics:
            prog = progress_map.get(topic.id)
            if prog and prog.revision_count > 0:
                started += 1
            if prog and prog.current_stage == TopicProgress.STAGE_MASTERED:
                mastered += 1

        not_started = total - started
        coverage_pct = (started / total) * 100 if total > 0 else 0.0

        return {
            "total_leaf_topics": total,
            "topics_started": started,
            "topics_not_started": not_started,
            "topics_mastered": mastered,
            "coverage_percentage": round(coverage_pct, 1),
        }

    # ── Review Completion Rate ────────────────────────────────────────

    @staticmethod
    def get_review_completion_rate(user_id: int) -> dict:
        """Calculate the review completion rate: percentage of missions
        marked as 'Completed'.

        Args:
            user_id: The ID of the user.

        Returns:
            dict with keys: total_missions, completed_missions, completion_rate,
                           in_progress, pending.
        """
        from sqlalchemy import func

        rows = (
            db.session.query(Mission.status, func.count(Mission.id))
            .filter_by(user_id=user_id)
            .group_by(Mission.status)
            .all()
        )
        counts = {status: count for status, count in rows}
        completed = counts.get("Completed", 0)
        in_progress = counts.get("In Progress", 0)
        pending = counts.get("Pending", 0)
        total = sum(counts.values())

        if total == 0:
            return {
                "total_missions": 0,
                "completed_missions": 0,
                "completion_rate": 0.0,
                "in_progress": 0,
                "pending": 0,
            }

        completion_rate = (completed / total) * 100

        return {
            "total_missions": total,
            "completed_missions": completed,
            "completion_rate": round(completion_rate, 1),
            "in_progress": in_progress,
            "pending": pending,
        }

    # ── Review Backlog ────────────────────────────────────────────────

    @staticmethod
    def get_review_backlog(user_id: int) -> dict:
        """Calculate the review backlog: topics due for review and overdue.

        Args:
            user_id: The ID of the user.

        Returns:
            dict with keys: topics_due_today, topics_overdue, total_backlog,
                           next_7_days.
        """
        today = date.today()
        next_7_end = today + timedelta(days=7)

        rows = (
            TopicProgress.query.filter(
                TopicProgress.user_id == user_id,
                TopicProgress.next_review_date.isnot(None),
                TopicProgress.current_stage != TopicProgress.STAGE_MASTERED,
                TopicProgress.next_review_date <= next_7_end,
            )
            .with_entities(TopicProgress.next_review_date)
            .all()
        )

        overdue = 0
        due_today = 0
        next_7_days = 0
        for (review_date,) in rows:
            if isinstance(review_date, datetime):
                review_date = review_date.date()
            if review_date < today:
                overdue += 1
            elif review_date == today:
                due_today += 1
            elif review_date <= next_7_end:
                next_7_days += 1

        return {
            "topics_due_today": due_today,
            "topics_overdue": overdue,
            "total_backlog": overdue + due_today,
            "next_7_days": next_7_days,
        }

    # ── Streaks ───────────────────────────────────────────────────────

    @staticmethod
    def get_current_streak(user_id: int) -> int:
        """Calculate the current consecutive-day study streak.

        The streak counts backwards from today. One missing day breaks it.

        Args:
            user_id: The ID of the user.

        Returns:
            int: Number of consecutive days (including today) with a study attempt.
        """

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

        # The most recent date must be today or yesterday for the streak to continue
        most_recent = dates[0]
        if isinstance(most_recent, datetime):
            most_recent = most_recent.date()
        if most_recent < today - timedelta(days=1):
            return 0

        streak = 0
        expected = today

        for d in dates:
            if isinstance(d, datetime):
                d = d.date()
            if d == expected:
                streak += 1
                expected = d - timedelta(days=1)
            elif d == expected - timedelta(days=1):
                break
            else:
                break

        return streak

    @staticmethod
    def get_longest_streak(user_id: int) -> int:
        """Calculate the longest consecutive-day study streak ever achieved.

        Args:
            user_id: The ID of the user.

        Returns:
            int: The maximum number of consecutive study days.
        """
        rows = (
            db.session.query(StudyAttempt.study_date)
            .filter(StudyAttempt.user_id == user_id)
            .distinct()
            .order_by(StudyAttempt.study_date.asc())
            .all()
        )

        if not rows:
            return 0

        dates = []
        for row in rows:
            d = row[0]
            if isinstance(d, datetime):
                d = d.date()
            dates.append(d)

        longest = 1
        current = 1

        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        return longest

    # ── Weakest & Strongest Topics ────────────────────────────────────

    @staticmethod
    def get_weakest_topics(user_id: int, limit: int = 5) -> list[dict]:
        """Get the weakest topics based on Estimated Knowledge.

        Only includes topics with attempt-derived evidence
        (``average_accuracy`` set). Study completion alone does not qualify
        (IA-004).

        Args:
            user_id: The ID of the user.
            limit: Maximum number of topics to return (default 5).

        Returns:
            list[dict]: Each dict has topic_name, mastery_score, stage, revision_count.
        """
        progress_list = (
            TopicProgress.query.options(joinedload(TopicProgress.topic))
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.revision_count > 0,
                TopicProgress.average_accuracy.isnot(None),
            )
            .order_by(TopicProgress.mastery_score.asc())
            .limit(limit)
            .all()
        )

        result = []
        for p in progress_list:
            result.append({
                "topic_id": p.topic_id,
                "topic_name": p.topic.name if p.topic else "Unknown",
                "mastery_score": round(p.mastery_score, 1),
                "stage": p.current_stage,
                "revision_count": p.revision_count,
            })

        return result

    @staticmethod
    def get_strongest_topics(user_id: int, limit: int = 5) -> list[dict]:
        """Get the strongest topics based on Estimated Knowledge.

        Only includes topics with attempt-derived evidence
        (``average_accuracy`` set). Study completion alone does not qualify
        (IA-004).

        Args:
            user_id: The ID of the user.
            limit: Maximum number of topics to return (default 5).

        Returns:
            list[dict]: Each dict has topic_name, mastery_score, stage, revision_count.
        """
        progress_list = (
            TopicProgress.query.options(joinedload(TopicProgress.topic))
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.revision_count > 0,
                TopicProgress.average_accuracy.isnot(None),
            )
            .order_by(TopicProgress.mastery_score.desc())
            .limit(limit)
            .all()
        )

        result = []
        for p in progress_list:
            result.append({
                "topic_id": p.topic_id,
                "topic_name": p.topic.name if p.topic else "Unknown",
                "mastery_score": round(p.mastery_score, 1),
                "stage": p.current_stage,
                "revision_count": p.revision_count,
            })

        return result

    # ── Topic Readiness Detail ────────────────────────────────────────

    @staticmethod
    def get_topic_readiness(user_id: int, topic_id: int) -> dict:
        """Get detailed readiness for a single topic.

        Args:
            user_id: The ID of the user.
            topic_id: The ID of the topic.

        Returns:
            dict with topic readiness details.
        """
        from app.services.curriculum_service import CurriculumService

        progress = CurriculumService.get_or_create_topic_progress(
            user_id=user_id, topic_id=topic_id
        )

        attempts = StudyAttempt.query.filter_by(
            user_id=user_id,
            topic_id=topic_id,
        ).order_by(StudyAttempt.study_date.desc()).all()

        unresolved = Mistake.query.join(StudyAttempt).filter(
            StudyAttempt.user_id == user_id,
            Mistake.topic_id == topic_id,
            Mistake.resolved == False,
        ).count()

        total_attempts = len(attempts)
        total_questions = sum(a.questions_attempted or 0 for a in attempts)
        total_correct = sum(a.questions_correct or 0 for a in attempts)

        accuracy = (
            (total_correct / total_questions * 100) if total_questions > 0 else None
        )

        return {
            "topic_id": topic_id,
            "topic_name": progress.topic.name if progress.topic else "Unknown",
            "mastery_score": round(progress.mastery_score, 1),
            "stage": progress.current_stage,
            "revision_count": progress.revision_count,
            "total_attempts": total_attempts,
            "total_questions": total_questions,
            "accuracy": round(accuracy, 1) if accuracy is not None else None,
            "unresolved_mistakes": unresolved,
            "last_reviewed": progress.last_reviewed,
            "next_review_date": progress.next_review_date,
            "completed": progress.completed,
        }

    # ── Private helpers ───────────────────────────────────────────────

    @staticmethod
    def _get_leaf_topics() -> list[Topic]:
        """Get all leaf topics (topics with no active subtopics).

        Returns:
            list[Topic]: All leaf topics across active curricula.
        """
        all_topics = Topic.query.filter_by(active=True).all()
        leaf_ids = set()
        parent_ids = set()

        for topic in all_topics:
            if topic.parent_topic_id is not None:
                parent_ids.add(topic.parent_topic_id)

        leaf_ids = {t.id for t in all_topics if t.id not in parent_ids}

        return [t for t in all_topics if t.id in leaf_ids]

    @staticmethod
    def _count_leaf_topics(user_id: int) -> int:
        """Count total leaf topics available.

        Args:
            user_id: The ID of the user (not currently used for filtering).

        Returns:
            int: Total number of leaf topics.
        """
        return len(ReadinessService._get_leaf_topics())

    @staticmethod
    def _count_started_topics(user_id: int) -> int:
        """Count leaf topics with at least one review.

        Args:
            user_id: The ID of the user.

        Returns:
            int: Number of started leaf topics.
        """
        leaf_topics = ReadinessService._get_leaf_topics()
        leaf_ids = [t.id for t in leaf_topics]

        if not leaf_ids:
            return 0

        return TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.topic_id.in_(leaf_ids),
            TopicProgress.revision_count > 0,
        ).count()

    @staticmethod
    def _count_mastered_topics(user_id: int) -> int:
        """Count leaf topics that are mastered.

        Args:
            user_id: The ID of the user.

        Returns:
            int: Number of mastered leaf topics.
        """
        leaf_topics = ReadinessService._get_leaf_topics()
        leaf_ids = [t.id for t in leaf_topics]

        if not leaf_ids:
            return 0

        return TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.topic_id.in_(leaf_ids),
            TopicProgress.current_stage == TopicProgress.STAGE_MASTERED,
        ).count()

    # ── Curriculum-based Readiness ─────────────────────────────────────

    @staticmethod
    def calculate_readiness(
        student_curriculum: object,
    ) -> ReadinessSummary | None:
        """Calculate exam readiness from a StudentCurriculumSummary.

        readiness_percentage is derived directly from
        ``student_curriculum.weighted_completed_percentage``.  No
        mastery, confidence, revision history, question performance,
        AI, or heuristics are used.

        Args:
            student_curriculum: A ``StudentCurriculumSummary`` instance,
                or ``None``.

        Returns:
            A frozen ``ReadinessSummary``, or ``None`` if no summary
            is supplied.
        """
        if student_curriculum is None:
            return None

        readiness_pct = student_curriculum.weighted_completed_percentage
        display_pct = round(readiness_pct * 100)

        explanation = (
            f"You have completed studying topics representing "
            f"{display_pct}% of the official syllabus weighting. "
            "This is Learning Progress from Study Progress — not Estimated Knowledge."
        )

        return ReadinessSummary(
            readiness_percentage=readiness_pct,
            weighted_completed_percentage=student_curriculum.weighted_completed_percentage,
            weighted_remaining_percentage=student_curriculum.weighted_remaining_percentage,
            explanation=explanation,
        )

    @staticmethod
    def _average_mastery(user_id: int) -> float:
        """Calculate average Estimated Knowledge across started leaf topics.

        Args:
            user_id: The ID of the user.

        Returns:
            float: Average Estimated Knowledge scalar (0-100) from
            ``TopicProgress.mastery_score``.
        """
        leaf_topics = ReadinessService._get_leaf_topics()
        leaf_ids = [t.id for t in leaf_topics]

        if not leaf_ids:
            return 0.0

        started = TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.topic_id.in_(leaf_ids),
            TopicProgress.revision_count > 0,
        ).all()

        if not started:
            return 0.0

        return sum(t.mastery_score for t in started) / len(started)

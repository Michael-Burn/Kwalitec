"""Recommendation Engine service.

Generates structured, deterministic recommendations using:
- AdaptiveLearningService (mastery, weak topics, review scheduling)
- ReadinessService (exam readiness, coverage, streaks)

All logic is explainable and completely deterministic. No AI or external APIs.

Supporting service classes (BurnoutMonitor, ExamTimeline, MissionOptimizer)
have been extracted into their own modules for maintainability.
"""

from __future__ import annotations

import logging
from datetime import datetime

from app.extensions import db
from app.models.decision import Decision
from app.services.burnout_monitor import BurnoutMonitor
from app.services.exam_timeline import ExamTimeline
from app.services.readiness_service import ReadinessService

logger = logging.getLogger(__name__)

CATEGORY_REVIEW = "Review"
CATEGORY_WEAK_TOPIC = "Weak Topic"
CATEGORY_NEW_TOPIC = "New Topic"
CATEGORY_MOCK_EXAM = "Mock Exam"
CATEGORY_REST = "Rest"
CATEGORY_REVISION = "Revision"
CATEGORY_EXAM_TECHNIQUE = "Exam Technique"

PRIORITY_CRITICAL = "Critical"
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"

PRIORITY_ORDER = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
}


class RecommendationService:
    """Deterministic recommendation engine.

    Consumes data from AdaptiveLearningService, ReadinessService, and
    AnalyticsService to produce structured, explainable recommendations.
    """

    @staticmethod
    def generate_recommendations(user_id: int, limit: int = 5) -> list[dict]:
        """Generate the top N recommendations for a user."""
        from app.services.learning_lifecycle_service import (
            LearningLifecycle,
            LearningLifecycleService,
        )

        lifecycle = LearningLifecycleService.resolve(user_id)
        if lifecycle.stage == LearningLifecycle.REVISION:
            return RecommendationService._revision_lifecycle_recommendations(
                user_id, limit=limit
            )

        recommendations: list[dict] = []

        recommendations.extend(
            RecommendationService._review_backlog_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._weak_topic_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._curriculum_progression_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._mock_exam_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._burnout_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._revision_phase_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._exam_technique_recommendations(user_id)
        )

        recommendations.sort(key=lambda r: PRIORITY_ORDER.get(r["priority"], 99))

        seen_titles: set[str] = set()
        unique: list[dict] = []
        for rec in recommendations:
            if rec["title"] not in seen_titles:
                seen_titles.add(rec["title"])
                unique.append(rec)

        return unique[:limit]

    @staticmethod
    def _revision_lifecycle_recommendations(
        user_id: int, *, limit: int = 5
    ) -> list[dict]:
        """Deterministic revision recommendations when syllabus coverage is complete.

        Suppresses unread-topic progression. Uses observed weak-topic and
        timeline signals only — no adaptive AI.
        """
        from app.services.learning_lifecycle_service import LearningLifecycleService

        recs: list[dict] = []
        weak_label = LearningLifecycleService.weakest_completed_topic_label(user_id)
        now = datetime.utcnow().isoformat()

        if weak_label:
            recs.append({
                "title": f"Review weakest topic: {weak_label}",
                "category": CATEGORY_REVISION,
                "priority": PRIORITY_HIGH,
                "reason": (
                    f"Your syllabus is complete. Revisiting {weak_label} "
                    "consolidates understanding where Estimated Knowledge "
                    "is comparatively lower."
                ),
                "expected_benefit": (
                    "Strengthen a weaker completed topic before the exam."
                ),
                "generated_at": now,
            })

        recs.append({
            "title": "Complete a mixed-topic practice set",
            "category": CATEGORY_REVISION,
            "priority": PRIORITY_HIGH,
            "reason": (
                "Syllabus coverage is complete. Mixed practice consolidates "
                "knowledge across topics rather than advancing unread material."
            ),
            "expected_benefit": (
                "Build exam fluency across the full syllabus."
            ),
            "generated_at": now,
        })

        recs.append({
            "title": "Recall important formulae",
            "category": CATEGORY_REVISION,
            "priority": PRIORITY_MEDIUM,
            "reason": (
                "In Revision Mode, retrieving key formulae without notes "
                "supports examination readiness."
            ),
            "expected_benefit": "Improve recall under exam conditions.",
            "generated_at": now,
        })

        recs.append({
            "title": "Complete one timed practice session",
            "category": CATEGORY_EXAM_TECHNIQUE,
            "priority": PRIORITY_MEDIUM,
            "reason": (
                "Timed practice builds pacing discipline once the syllabus "
                "has been completed studying."
            ),
            "expected_benefit": "Strengthen timing and exam technique.",
            "generated_at": now,
        })

        recs.extend(RecommendationService._burnout_recommendations(user_id))
        recs.extend(RecommendationService._mock_exam_recommendations(user_id))

        recs.sort(key=lambda r: PRIORITY_ORDER.get(r["priority"], 99))
        seen: set[str] = set()
        unique: list[dict] = []
        for rec in recs:
            if rec["title"] not in seen:
                seen.add(rec["title"])
                unique.append(rec)
        return unique[:limit]

    @staticmethod
    def generate_today_recommendation(user_id: int) -> dict | None:
        """Generate the single best recommendation for today."""
        recs = RecommendationService.generate_recommendations(user_id, limit=1)
        return recs[0] if recs else None

    # ── Rule Set Implementations ──────────────────────────────────────────

    @staticmethod
    def _review_backlog_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        backlog = ReadinessService.get_review_backlog(user_id)

        if backlog["topics_overdue"] > 0:
            recs.append({
                "title": f"Clear your review backlog ({backlog['topics_overdue']} overdue)",
                "category": CATEGORY_REVIEW,
                "priority": PRIORITY_CRITICAL,
                "reason": (
                    f"You have {backlog['topics_overdue']} topic(s) overdue for review. "
                    "Staying current on reviews helps protect Estimated Knowledge."
                ),
                "expected_benefit": (
                    "Restore retention on overdue topics and keep review rhythm steady."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
        elif backlog["topics_due_today"] > 0:
            recs.append({
                "title": f"Review {backlog['topics_due_today']} topic(s) due today",
                "category": CATEGORY_REVIEW,
                "priority": PRIORITY_HIGH,
                "reason": (
                    f"{backlog['topics_due_today']} topic(s) are scheduled for review today."
                ),
                "expected_benefit": (
                    "Maintain your review rhythm and keep topics from becoming overdue."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _weak_topic_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        weak_topics = ReadinessService.get_weakest_topics(user_id, limit=3)

        if not weak_topics:
            return recs

        critical_weak = [t for t in weak_topics if t["mastery_score"] < 30]
        if critical_weak:
            topic_names = ", ".join(t["topic_name"] for t in critical_weak[:2])
            recs.append({
                "title": f"Practise lower Estimated Knowledge: {topic_names}",
                "category": CATEGORY_WEAK_TOPIC,
                "priority": PRIORITY_CRITICAL,
                "reason": (
                    f"Your Estimated Knowledge for {topic_names} is below 30%. "
                    "These foundational areas may benefit from more practice before "
                    "you lean on them in later topics."
                ),
                "expected_benefit": (
                    "Strengthen foundational Estimated Knowledge through practice."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
            return recs

        moderate_weak = [t for t in weak_topics if t["mastery_score"] < 60]
        if moderate_weak:
            topic_names = ", ".join(t["topic_name"] for t in moderate_weak[:2])
            recs.append({
                "title": f"Improve Estimated Knowledge: {topic_names}",
                "category": CATEGORY_WEAK_TOPIC,
                "priority": PRIORITY_HIGH,
                "reason": (
                    f"Your Estimated Knowledge for {topic_names} is between 30-60%. "
                    "Targeted practice on lower-estimate areas often helps most."
                ),
                "expected_benefit": "Bring these topics into a stronger estimated range.",
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _curriculum_progression_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        coverage = ReadinessService.get_curriculum_coverage(user_id)

        if coverage["total_leaf_topics"] == 0:
            return recs

        next_topic_name = RecommendationService._next_incomplete_topic_label(user_id)

        if coverage["coverage_percentage"] < 30 and coverage["topics_not_started"] > 0:
            if next_topic_name:
                title = f"Study {next_topic_name}"
                reason = (
                    f"Your next syllabus topic is {next_topic_name}. "
                    f"You have only covered {coverage['coverage_percentage']:.0f}% "
                    "of the curriculum."
                )
            else:
                title = (
                    f"Explore new topics — {coverage['topics_not_started']} remaining"
                )
                reason = (
                    f"You have only covered {coverage['coverage_percentage']:.0f}% "
                    "of the curriculum. Broadening coverage is essential."
                )
            recs.append({
                "title": title,
                "category": CATEGORY_NEW_TOPIC,
                "priority": PRIORITY_HIGH,
                "reason": reason,
                "expected_benefit": (
                    "Increase syllabus coverage — Study Progress, not Estimated Knowledge."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        if 30 <= coverage["coverage_percentage"] < 70:
            if next_topic_name:
                title = f"Continue with {next_topic_name}"
                reason = (
                    f"Your curriculum coverage is at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    f"Next up: {next_topic_name}."
                )
            else:
                title = "Continue progressing through the curriculum"
                reason = (
                    f"Your curriculum coverage is at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    "Steady progression ensures comprehensive exam preparation."
                )
            recs.append({
                "title": title,
                "category": CATEGORY_NEW_TOPIC,
                "priority": PRIORITY_MEDIUM,
                "reason": reason,
                "expected_benefit": (
                    "Sustained curriculum progression builds broad knowledge."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        if coverage["coverage_percentage"] >= 70 and coverage["topics_not_started"] > 0:
            if next_topic_name:
                title = f"Complete {next_topic_name}"
                reason = (
                    f"You have excellent coverage at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    f"Remaining work includes {next_topic_name}."
                )
            else:
                title = (
                    f"Complete remaining {coverage['topics_not_started']} topics"
                )
                reason = (
                    f"You have excellent coverage at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    "Complete the full syllabus for no blind spots."
                )
            recs.append({
                "title": title,
                "category": CATEGORY_NEW_TOPIC,
                "priority": PRIORITY_LOW,
                "reason": reason,
                "expected_benefit": (
                    "Finish remaining syllabus topics so Study Progress is complete."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _next_incomplete_topic_label(user_id: int) -> str | None:
        """Return a display label for the user's next incomplete syllabus topic."""
        from app.services.curriculum_service import CurriculumService
        from app.services.planning_service import PlanningService
        from app.services.study_plan_service import StudyPlanService

        plan = StudyPlanService.get_user_active_plan(user_id)
        if plan is None or not plan.curriculum_id:
            return None
        curriculum = CurriculumService.get_curriculum_by_id(plan.curriculum_id)
        if curriculum is None:
            return None
        topic = CurriculumService.get_next_incomplete_topic(user_id, curriculum)
        if topic is None:
            return None
        topic_code = PlanningService._resolve_official_topic_code(plan, topic)
        return PlanningService._topic_study_label(topic, topic_code=topic_code)

    @staticmethod
    def _mock_exam_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        readiness = ReadinessService.get_overall_readiness(user_id)

        if readiness["total_topics"] == 0:
            return recs

        if readiness["score"] >= 60 and readiness["coverage_pct"] >= 50:
            recs.append({
                "title": "Take a mock exam this week",
                "category": CATEGORY_MOCK_EXAM,
                "priority": PRIORITY_MEDIUM,
                "reason": (
                    f"Estimated readiness is about {readiness['score']:.0f}% with "
                    f"{readiness['coverage_pct']:.0f}% syllabus coverage. "
                    "Mock exams can help reveal remaining gaps — estimates are not "
                    "exam outcome guarantees."
                ),
                "expected_benefit": (
                    "Reveal remaining gaps and build exam-day familiarity."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
        elif readiness["score"] >= 40:
            recs.append({
                "title": "Begin incorporating mock exam practice",
                "category": CATEGORY_MOCK_EXAM,
                "priority": PRIORITY_LOW,
                "reason": (
                    f"Estimated readiness is about {readiness['score']:.0f}%. "
                    "Introducing occasional mock exam sections builds familiarity."
                ),
                "expected_benefit": (
                    "Early exposure to exam-style questions builds familiarity."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _burnout_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        burnout = BurnoutMonitor.detect_burnout(user_id)

        if burnout["risk_level"] == "high":
            recs.append({
                "title": "Take a rest day — study pattern notice",
                "category": CATEGORY_REST,
                "priority": PRIORITY_CRITICAL,
                "reason": f"{burnout['explanation']} Taking a rest day now prevents longer forced breaks later.",
                "expected_benefit": (
                    "Recovery, clearer focus, and steadier progress over the week."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
        elif burnout["risk_level"] == "moderate":
            recs.append({
                "title": "Consider a lighter study day",
                "category": CATEGORY_REST,
                "priority": PRIORITY_MEDIUM,
                "reason": f"{burnout['explanation']} A lighter day helps maintain momentum while recovering.",
                "expected_benefit": "Protect focus while keeping study momentum.",
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _revision_phase_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        timeline = ExamTimeline.get_timeline(user_id)

        if timeline is None:
            return recs

        days_remaining = timeline["days_remaining"]
        coverage = timeline["curriculum_coverage_pct"]

        if days_remaining <= 30 and days_remaining > 0 and coverage >= 50:
            recs.append({
                "title": f"Enter revision phase — {days_remaining} days until exam",
                "category": CATEGORY_REVISION,
                "priority": PRIORITY_HIGH if days_remaining <= 14 else PRIORITY_MEDIUM,
                "reason": (
                    f"With {days_remaining} days until your exam and {coverage:.0f}% "
                    "coverage, shift focus to consolidation and revision."
                ),
                "expected_benefit": (
                    "Focused revision in the final weeks maximises retention."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        if 14 <= days_remaining <= 45 and coverage >= 60:
            recs.append({
                "title": "Enter mock exam phase",
                "category": CATEGORY_MOCK_EXAM,
                "priority": PRIORITY_HIGH if days_remaining <= 21 else PRIORITY_MEDIUM,
                "reason": (
                    f"With {days_remaining} days remaining and {coverage:.0f}% coverage, "
                    "you should be in the mock exam phase."
                ),
                "expected_benefit": "Regular mock exams build stamina and reveal weak points.",
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _exam_technique_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        timeline = ExamTimeline.get_timeline(user_id)

        if timeline is None:
            return recs

        if (
            timeline["days_remaining"] <= 60
            and timeline["days_remaining"] > 0
            and timeline["average_mastery_pct"] >= 40
        ):
            recs.append({
                "title": "Focus on exam technique and time management",
                "category": CATEGORY_EXAM_TECHNIQUE,
                "priority": (
                    PRIORITY_HIGH if timeline["days_remaining"] <= 30
                    else PRIORITY_MEDIUM
                ),
                "reason": (
                    f"With {timeline['days_remaining']} days until your exam, "
                    "exam technique becomes increasingly important."
                ),
                "expected_benefit": (
                    "Better exam technique can add 5-15% to your score."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    # ── Decision Journal Methods ───────────────────────────────────────────

    @staticmethod
    def record_decision(
        user_id: int,
        recommendation: dict,
        accepted: bool = False,
        completed: bool = False,
        outcome_summary: str | None = None,
    ) -> Decision:
        """Record a user's decision about a recommendation.

        EIP-002: Accept / dismiss is preference history only. It must never
        create Educational Evidence of understanding or mutate Version 1
        Estimated Knowledge (Constitution Art. V §2; EL-006 / EL-008).
        """
        decision = Decision(
            user_id=user_id,
            recommendation_title=recommendation["title"],
            recommendation_category=recommendation["category"],
            recommendation_priority=recommendation["priority"],
            recommendation_reason=recommendation["reason"],
            recommendation_expected_benefit=recommendation["expected_benefit"],
            recommendation_generated_at=(
                datetime.fromisoformat(recommendation["generated_at"])
                if isinstance(recommendation["generated_at"], str)
                else recommendation["generated_at"]
            ),
            accepted=accepted,
            completed=completed,
            outcome_summary=outcome_summary,
        )
        db.session.add(decision)
        db.session.commit()
        logger.info(
            "Decision recorded for user %d: %s accepted=%s",
            user_id, recommendation["title"], accepted,
        )
        return decision

    @staticmethod
    def get_decision_journal(user_id: int, limit: int = 20) -> list[Decision]:
        """Get the decision journal for a user."""
        return (
            Decision.query.filter_by(user_id=user_id)
            .order_by(Decision.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_decision_summary(user_id: int) -> dict:
        """Get summary statistics for the decision journal."""
        decisions = Decision.query.filter_by(user_id=user_id).all()
        total = len(decisions)

        if total == 0:
            return {
                "total_decisions": 0,
                "acceptance_rate": 0.0,
                "completion_rate": 0.0,
                "categories": {},
            }

        accepted = sum(1 for d in decisions if d.accepted)
        completed = sum(1 for d in decisions if d.completed)

        categories: dict[str, dict] = {}
        for d in decisions:
            cat = d.recommendation_category
            if cat not in categories:
                categories[cat] = {"total": 0, "accepted": 0, "completed": 0}
            categories[cat]["total"] += 1
            if d.accepted:
                categories[cat]["accepted"] += 1
            if d.completed:
                categories[cat]["completed"] += 1

        return {
            "total_decisions": total,
            "acceptance_rate": round((accepted / total) * 100, 1) if total > 0 else 0.0,
            "completion_rate": round((completed / total) * 100, 1) if total > 0 else 0.0,
            "categories": {
                cat: {
                    "total": data["total"],
                    "acceptance_rate": round((data["accepted"] / data["total"]) * 100, 1),
                    "completion_rate": round((data["completed"] / data["total"]) * 100, 1),
                }
                for cat, data in categories.items()
            },
        }


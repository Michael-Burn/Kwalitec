"""Mission optimizer service — generates balanced daily missions.

Each daily mission includes three topic types:
- One review topic (spaced repetition)
- One weak topic (targeted improvement)
- One curriculum progression topic (forward momentum)
"""

from __future__ import annotations

from datetime import date

from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.curriculum_service import CurriculumService
from app.services.study_plan_service import StudyPlanService


class MissionOptimizer:
    """Generates balanced daily missions comprising three topic types."""

    @staticmethod
    def generate_balanced_mission(user_id: int) -> dict | None:
        """Generate a balanced daily mission with three topics.

        Uses priority-based selection:
        1. Review topic: highest-priority topic due for review
        2. Weak topic: weakest topic needing attention
        3. Progression topic: next topic in curriculum sequence
        """
        topics: dict[str, dict | None] = {
            "review": None,
            "weak": None,
            "progression": None,
        }

        today = date.today()

        # 1. Review topic
        due_reviews = AdaptiveLearningService.get_topics_due_for_review(user_id, today)
        if due_reviews:
            rp = due_reviews[0]
            topics["review"] = {
                "topic_id": rp.topic_id,
                "topic_name": rp.topic.name if rp.topic else "Unknown",
                "mastery_score": round(rp.mastery_score, 1),
                "stage": rp.current_stage,
                "reason": f"Due for review (scheduled {rp.next_review_date})",
                "expected_benefit": (
                    "Maintain spaced repetition schedule and prevent knowledge decay."
                ),
            }

        # 2. Weak topic
        weak_topics = AdaptiveLearningService.get_weak_topics(user_id, threshold=60.0)
        if weak_topics:
            if topics["review"]:
                weak_filtered = [
                    wp for wp in weak_topics
                    if wp.topic_id != topics["review"]["topic_id"]
                ]
            else:
                weak_filtered = weak_topics

            if weak_filtered:
                wp = weak_filtered[0]
                topics["weak"] = {
                    "topic_id": wp.topic_id,
                    "topic_name": wp.topic.name if wp.topic else "Unknown",
                    "mastery_score": round(wp.mastery_score, 1),
                    "stage": wp.current_stage,
                    "reason": (
                        f"Weak topic (mastery {wp.mastery_score:.0f}% "
                        f"— below 60% threshold)"
                    ),
                    "expected_benefit": (
                        "Improve weakest area for maximum readiness gain per study hour."
                    ),
                }

        # 3. Progression topic
        active_plan = StudyPlanService.get_user_active_plan(user_id)
        if active_plan and active_plan.curriculum_id:
            curriculum = CurriculumService.get_curriculum_by_id(
                active_plan.curriculum_id
            )
            if curriculum:
                next_topic = CurriculumService.get_next_incomplete_topic(
                    user_id=user_id, curriculum=curriculum
                )
                if next_topic:
                    existing_ids = {
                        topics[t]["topic_id"]
                        for t in ["review", "weak"]
                        if topics[t]
                    }
                    if next_topic.id not in existing_ids:
                        topics["progression"] = {
                            "topic_id": next_topic.id,
                            "topic_name": next_topic.name,
                            "mastery_score": None,
                            "stage": "Not Started",
                            "reason": "Next unstarted topic in curriculum sequence",
                            "expected_benefit": (
                                "Continue forward progress through the syllabus."
                            ),
                        }

        topic_count = sum(1 for v in topics.values() if v is not None)
        if topic_count < 2:
            return None

        return {
            "date": today.isoformat(),
            "topics": topics,
            "topic_count": topic_count,
            "mission_status": "Ready" if topic_count == 3 else "Partial",
        }
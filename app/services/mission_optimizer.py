"""Mission optimizer service — generates balanced daily missions.

.. deprecated:: EP-002.2
    ``MissionOptimizer.generate_balanced_mission`` is **quarantined**.
    It has no production callers. Do **not** wire it into HTTP, templates,
    or dashboard context. Balanced review / weak / progression slots are
    owned by ``PlanningService.build_daily_study_plan`` (EP-001.2).

    Decision: deprecate and quarantine — do not wire to production; do not
    hard-delete in this milestone. See
    ``knowledge/architecture/ep002_2_shared_foundation_di/MISSION_OPTIMIZER_DECISION.md``.

Each daily mission includes three topic types:
- One review topic (spaced repetition)
- One weak topic (targeted improvement)
- One curriculum progression topic (forward momentum)

EP-001.2: prefers EP-001.1 Canonical Learner State (via PlanningService
adaptive daily plan) when Digital Twin is ON; falls back to
AdaptiveLearningService / CurriculumService otherwise.
"""

from __future__ import annotations

import warnings
from datetime import date

from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.curriculum_service import CurriculumService
from app.services.study_plan_service import StudyPlanService

_DEPRECATION_MESSAGE = (
    "MissionOptimizer.generate_balanced_mission is quarantined (EP-002.2). "
    "Do not wire into student-facing surfaces. Use "
    "PlanningService.build_daily_study_plan for Twin-gated mission slots."
)


class MissionOptimizer:
    """Generates balanced daily missions comprising three topic types.

    Quarantined (EP-002.2): retained for behaviour preservation and
    potential EP-002.7 cleanup — not a production authority.
    """

    @staticmethod
    def generate_balanced_mission(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
    ) -> dict | None:
        """Generate a balanced daily mission with three topics.

        .. deprecated:: EP-002.2
            Quarantined — no production callers. Prefer
            ``PlanningService.build_daily_study_plan``.

        Uses priority-based selection:
        1. Review topic: highest-priority topic due for review
        2. Weak topic: weakest topic needing attention
        3. Progression topic: next topic in curriculum sequence

        When Twin Foundation is enabled, topic slots are taken from the
        Canonical Learner State daily plan projection (EP-001.2).
        """
        warnings.warn(_DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)
        from_canonical = MissionOptimizer._from_canonical_plan(
            user_id,
            foundation=foundation,
            canonical_state=canonical_state,
        )
        if from_canonical is not None:
            return from_canonical
        return MissionOptimizer._from_legacy_services(user_id)

    @staticmethod
    def _from_canonical_plan(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
    ) -> dict | None:
        from app.infrastructure.adapters.digital_twin.contracts import (
            AVAILABILITY_AVAILABLE,
        )
        from app.services.planning_service import PlanningService

        plan = PlanningService.build_daily_study_plan(
            user_id,
            foundation=foundation,
            canonical_state=canonical_state,
        )
        if not plan or plan.get("availability") != AVAILABILITY_AVAILABLE:
            return None

        today = date.today()
        slots = {slot.get("slot"): slot for slot in (plan.get("today_missions") or [])}
        topics: dict[str, dict | None] = {
            "review": None,
            "weak": None,
            "progression": None,
        }

        for key in ("review", "weak", "progression"):
            slot = slots.get(key)
            if not slot:
                continue
            mastery = None
            for row in plan.get("topic_ordering") or ():
                if str(row.get("topic_id")) == str(slot.get("topic_id")):
                    mastery = row.get("mastery_score")
                    break
            topics[key] = {
                "topic_id": int(slot["topic_id"])
                if str(slot.get("topic_id") or "").isdigit()
                else slot.get("topic_id"),
                "topic_name": slot.get("topic_name") or "Unknown",
                "mastery_score": (
                    round(float(mastery), 1) if mastery is not None else None
                ),
                "stage": None,
                "reason": slot.get("reason") or "",
                "expected_benefit": slot.get("expected_benefit") or "",
                "source": "canonical_learner_state",
            }

        topic_count = sum(1 for v in topics.values() if v is not None)
        if topic_count < 2:
            return None

        workload = plan.get("recommended_workload") or {}
        return {
            "date": today.isoformat(),
            "topics": topics,
            "topic_count": topic_count,
            "mission_status": "Ready" if topic_count == 3 else "Partial",
            "recommended_workload": workload,
            "revision_priorities": plan.get("revision_priorities") or [],
            "topic_ordering": plan.get("topic_ordering") or [],
            "source": "canonical_learner_state",
            "foundation_version": plan.get("foundation_version"),
        }

    @staticmethod
    def _from_legacy_services(user_id: int) -> dict | None:
        """Legacy AdaptiveLearning / Curriculum path (Twin OFF)."""
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
                        "Improve weakest area for maximum readiness "
                        "gain per study hour."
                    ),
                }

        # 3. Progression topic — Learning Mode only (never in Revision)
        from app.services.learning_lifecycle_service import (
            LearningLifecycle,
            LearningLifecycleService,
        )

        active_plan = StudyPlanService.get_user_active_plan(user_id)
        lifecycle = LearningLifecycleService.resolve(user_id, study_plan=active_plan)
        if lifecycle.stage != LearningLifecycle.REVISION:
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
        else:
            # Revision advisory: prefer weak / review slots only — no Topic 1.
            if topics["weak"] is None and weak_topics:
                wp = weak_topics[0]
                topics["weak"] = {
                    "topic_id": wp.topic_id,
                    "topic_name": wp.topic.name if wp.topic else "Unknown",
                    "mastery_score": round(wp.mastery_score, 1),
                    "stage": wp.current_stage,
                    "reason": "Revision focus — consolidate a weaker completed topic",
                    "expected_benefit": (
                        "Consolidate understanding without restarting the syllabus."
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

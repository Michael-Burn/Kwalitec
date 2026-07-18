"""Balance educational workload using structural signals only.

Inputs may include estimated effort, outstanding reflections, revision debt,
and journey continuity. Never infers mastery.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.mission_engine_v2.dto.daily_mission import DailyMission
from app.application.mission_engine_v2.exceptions import WorkloadExceeded
from app.application.mission_engine_v2.lifecycle import is_open_mission_state
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy


@dataclass(frozen=True)
class WorkloadAssessment:
    """Immutable structural workload posture for a learner."""

    open_count: int
    active_count: int
    deferred_count: int
    missed_count: int
    revision_count: int
    future_count: int
    effort_load: int
    outstanding_reflections: int
    revision_debt: int
    journey_continuity: bool
    within_limits: bool
    blocking_reasons: tuple[str, ...]


class WorkloadBalancer:
    """Assess and gate mission additions using structural workload signals."""

    def assess(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        *,
        journey_id: str | None = None,
    ) -> WorkloadAssessment:
        """Compute a structural workload assessment (never mastery)."""
        open_m = WorkloadPolicy.open_missions(missions)
        effort_load = sum(WorkloadPolicy.effort_weight(m.effort) for m in open_m)
        reflections = WorkloadPolicy.total_outstanding_reflections(missions)
        debt = WorkloadPolicy.total_revision_debt(missions)
        continuity = (
            WorkloadPolicy.has_journey_continuity(missions, journey_id)
            if journey_id
            else False
        )
        reasons: list[str] = []
        if len(open_m) >= WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER:
            reasons.append("open_capacity")
        if (
            len(WorkloadPolicy.active_missions(missions))
            >= WorkloadPolicy.MAX_ACTIVE_MISSIONS
        ):
            reasons.append("active_capacity")
        if (
            len(WorkloadPolicy.deferred_missions(missions))
            >= WorkloadPolicy.MAX_DEFERRED_MISSIONS
        ):
            reasons.append("deferred_capacity")
        if (
            len(WorkloadPolicy.missed_missions(missions))
            >= WorkloadPolicy.MAX_MISSED_MISSIONS
        ):
            reasons.append("missed_capacity")
        if (
            len(WorkloadPolicy.revision_missions(missions))
            >= WorkloadPolicy.MAX_REVISION_MISSIONS
        ):
            reasons.append("revision_capacity")
        if reflections > WorkloadPolicy.MAX_OUTSTANDING_REFLECTIONS:
            reasons.append("outstanding_reflections")
        if debt > WorkloadPolicy.MAX_REVISION_DEBT:
            reasons.append("revision_debt")
        return WorkloadAssessment(
            open_count=len(open_m),
            active_count=len(WorkloadPolicy.active_missions(missions)),
            deferred_count=len(WorkloadPolicy.deferred_missions(missions)),
            missed_count=len(WorkloadPolicy.missed_missions(missions)),
            revision_count=len(WorkloadPolicy.revision_missions(missions)),
            future_count=len(WorkloadPolicy.future_missions(missions)),
            effort_load=effort_load,
            outstanding_reflections=reflections,
            revision_debt=debt,
            journey_continuity=continuity,
            within_limits=not reasons,
            blocking_reasons=tuple(reasons),
        )

    def assert_can_add(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        candidate: DailyMission,
    ) -> None:
        """Raise WorkloadExceeded when adding ``candidate`` would breach caps."""
        without = [m for m in missions if m.mission_id != candidate.mission_id]
        if not WorkloadPolicy.can_add_open(without):
            raise WorkloadExceeded("Open mission capacity exceeded")
        if candidate.is_revision and not WorkloadPolicy.can_add_revision(without):
            raise WorkloadExceeded("Revision mission capacity exceeded")
        from app.application.mission_engine_v2.lifecycle import MissionSlot

        if (
            candidate.slot == MissionSlot.DEFERRED
            and not WorkloadPolicy.can_defer(without)
        ):
            raise WorkloadExceeded("Deferred mission capacity exceeded")
        if (
            candidate.slot == MissionSlot.MISSED
            and not WorkloadPolicy.can_mark_missed(without)
        ):
            raise WorkloadExceeded("Missed mission capacity exceeded")
        if (
            candidate.slot == MissionSlot.FUTURE
            and not WorkloadPolicy.can_add_future(without)
        ):
            raise WorkloadExceeded("Future mission capacity exceeded")
        projected = [*without, candidate]
        reflections = WorkloadPolicy.total_outstanding_reflections(projected)
        if reflections > WorkloadPolicy.MAX_OUTSTANDING_REFLECTIONS:
            raise WorkloadExceeded("Outstanding reflection capacity exceeded")
        debt = WorkloadPolicy.total_revision_debt(projected)
        if debt > WorkloadPolicy.MAX_REVISION_DEBT:
            raise WorkloadExceeded("Revision debt capacity exceeded")

    def prefer_continuity(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
        candidates: list[DailyMission] | tuple[DailyMission, ...],
    ) -> DailyMission | None:
        """Prefer a candidate that continues an existing open journey.

        Structural continuity only — never ranks by mastery.
        """
        open_journeys = {
            m.journey_id
            for m in missions
            if is_open_mission_state(m.state)
        }
        for candidate in candidates:
            if candidate.journey_id in open_journeys:
                return candidate
        return candidates[0] if candidates else None

    def should_defer_new_work(
        self,
        missions: list[DailyMission] | tuple[DailyMission, ...],
    ) -> bool:
        """True when structural load suggests deferring new mission creation."""
        assessment = self.assess(missions)
        if not assessment.within_limits:
            return True
        if assessment.outstanding_reflections >= 3:
            return True
        if assessment.effort_load >= 10:
            return True
        return False

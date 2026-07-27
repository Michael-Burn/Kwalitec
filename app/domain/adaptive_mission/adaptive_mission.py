"""AdaptiveMission aggregate root — one actionable daily learning mission."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, date, datetime

from app.domain.adaptive_mission.mission import Mission, MissionStatus
from app.domain.adaptive_mission.mission_completion import MissionCompletion
from app.domain.adaptive_mission.mission_objective import MissionObjective
from app.domain.adaptive_mission.mission_outcome import MissionOutcome
from app.domain.adaptive_mission.mission_plan import MissionPlan
from app.domain.adaptive_mission.mission_priority import MissionPriority
from app.domain.adaptive_mission.mission_progress import MissionProgress
from app.domain.adaptive_mission.mission_reason import MissionReason
from app.domain.adaptive_mission.mission_schedule import MissionSchedule
from app.domain.adaptive_mission.mission_step import MissionStep


@dataclass(frozen=True)
class AdaptiveMission:
    """Aggregate owning today's optimal learning plan for one learner.

    One active AdaptiveMission exists per learner. Educational reasoning is
    never performed here — decisions are consumed from Twin / Reasoning / Graph.
    """

    identity: Mission
    objective: MissionObjective
    plan: MissionPlan
    schedule: MissionSchedule
    reason: MissionReason
    expected_outcome: MissionOutcome
    priority: MissionPriority
    success_criteria: tuple[str, ...]
    reflection_prompt: str
    progress: MissionProgress
    evidence_references: tuple[str, ...] = ()
    concepts_covered: tuple[str, ...] = ()
    estimated_duration_minutes: int = 30
    source_recommendation_ids: tuple[str, ...] = ()
    source_gap_ids: tuple[str, ...] = ()
    reasoning_run_id: str = ""
    validation_passed: bool = False
    validation_summary: str = ""
    completion: MissionCompletion | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    version: int = 1

    def __post_init__(self) -> None:
        priority = (
            self.priority
            if isinstance(self.priority, MissionPriority)
            else MissionPriority(str(self.priority))
        )
        object.__setattr__(self, "priority", priority)
        object.__setattr__(
            self, "success_criteria", tuple(self.success_criteria or ())
        )
        object.__setattr__(
            self, "evidence_references", tuple(self.evidence_references or ())
        )
        object.__setattr__(
            self, "concepts_covered", tuple(self.concepts_covered or ())
        )
        object.__setattr__(
            self,
            "source_recommendation_ids",
            tuple(self.source_recommendation_ids or ()),
        )
        object.__setattr__(self, "source_gap_ids", tuple(self.source_gap_ids or ()))
        object.__setattr__(
            self,
            "estimated_duration_minutes",
            max(1, int(self.estimated_duration_minutes)),
        )
        for when_attr in ("created_at", "updated_at"):
            when = getattr(self, when_attr)
            if when is not None and when.tzinfo is not None:
                object.__setattr__(
                    self, when_attr, when.astimezone(UTC).replace(tzinfo=None)
                )

    @property
    def mission_id(self) -> str:
        return self.identity.mission_id

    @property
    def twin_id(self) -> str:
        return self.identity.twin_id

    @property
    def student_id(self) -> str:
        return self.identity.student_id

    @property
    def mission_date(self) -> date:
        return self.identity.mission_date

    @property
    def status(self) -> MissionStatus:
        return self.identity.status

    @property
    def goal(self) -> str:
        return self.identity.goal

    @property
    def steps(self) -> tuple[MissionStep, ...]:
        return self.plan.steps

    def with_status(
        self,
        status: MissionStatus,
        *,
        updated_at: datetime | None = None,
    ) -> AdaptiveMission:
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        return replace(
            self,
            identity=replace(self.identity, status=status),
            updated_at=when,
            version=self.version + 1,
        )

    def with_progress(
        self,
        progress: MissionProgress,
        *,
        updated_at: datetime | None = None,
    ) -> AdaptiveMission:
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        steps = tuple(
            replace(step, completed=(i < progress.steps_completed))
            for i, step in enumerate(self.plan.steps)
        )
        plan = replace(self.plan, steps=steps)
        status = self.status
        if (
            progress.steps_total > 0
            and progress.steps_completed >= progress.steps_total
            and status == MissionStatus.ACTIVE
        ):
            status = MissionStatus.COMPLETED
        return replace(
            self,
            identity=replace(self.identity, status=status),
            plan=plan,
            progress=progress,
            updated_at=when,
            version=self.version + 1,
        )

    def with_completion(
        self,
        completion: MissionCompletion,
        *,
        updated_at: datetime | None = None,
    ) -> AdaptiveMission:
        when = updated_at or completion.completed_at
        return replace(
            self,
            identity=replace(self.identity, status=MissionStatus.COMPLETED),
            completion=completion,
            updated_at=when,
            version=self.version + 1,
        )

    def with_validation(
        self,
        *,
        passed: bool,
        summary: str,
        updated_at: datetime | None = None,
    ) -> AdaptiveMission:
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        status = self.status
        if not passed and status == MissionStatus.DRAFT:
            status = MissionStatus.REJECTED
        elif passed and status in {MissionStatus.DRAFT, MissionStatus.REJECTED}:
            status = MissionStatus.DRAFT
        return replace(
            self,
            identity=replace(self.identity, status=status),
            validation_passed=passed,
            validation_summary=summary,
            updated_at=when,
            version=self.version + 1,
        )

    def activate(self, *, updated_at: datetime | None = None) -> AdaptiveMission:
        if not self.validation_passed:
            raise ValueError("cannot activate a mission that failed validation")
        return self.with_status(MissionStatus.ACTIVE, updated_at=updated_at)

    def as_mission_card(self) -> dict[str, object]:
        """Simple projection for the existing student Mission card surface."""
        return {
            "mission_id": self.mission_id,
            "title": self.goal,
            "status": self.status.value,
            "mission_date": self.mission_date.isoformat(),
            "reason": self.reason.summary,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "priority": self.priority.value,
            "tasks": [
                {
                    "title": step.activity.title,
                    "order": step.order,
                    "completed": step.completed,
                    "activity_type": step.activity.activity_type.value,
                }
                for step in self.steps
            ],
            "source": "adaptive_mission_engine",
        }

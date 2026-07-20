"""Orchestration plan — ordered coordination stages for one turn.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
Concept
    Orchestration Plan
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStage,
    OrchestrationStageId,
)


@dataclass(frozen=True, slots=True)
class OrchestrationPlanId(EducationalValueObject):
    """Identity of an orchestration plan within EducationalOrchestrator."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "OrchestrationPlanId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class OrchestrationPlan(EducationalEntity):
    """Ordered set of coordination stages for one orchestration turn.

    A plan must contain at least one stage. Ordering is educational
    coordination law — not diagnosis or strategy selection.
    """

    plan_id: OrchestrationPlanId
    stages: tuple[OrchestrationStage, ...]
    label: str = "orchestration plan"

    @property
    def entity_id(self) -> OrchestrationPlanId:
        return self.plan_id

    def _validate(self) -> None:
        if not isinstance(self.plan_id, OrchestrationPlanId):
            raise EducationalInvariantViolation(
                "plan_id must be an OrchestrationPlanId",
                invariant="OrchestrationPlan.plan_id.type",
            )
        if not isinstance(self.stages, tuple):
            raise EducationalInvariantViolation(
                "stages must be a tuple of OrchestrationStage",
                invariant="OrchestrationPlan.stages.type",
            )
        if len(self.stages) < 1:
            raise EducationalInvariantViolation(
                "orchestration plan must contain at least one stage",
                invariant="OrchestrationPlan.stages.min",
            )
        seen_ids: set[str] = set()
        seen_indexes: set[int] = set()
        for stage in self.stages:
            if not isinstance(stage, OrchestrationStage):
                raise EducationalInvariantViolation(
                    "stages must contain OrchestrationStage entities",
                    invariant="OrchestrationPlan.stages.element_type",
                )
            if stage.stage_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "orchestration stages must have unique identities",
                    invariant="OrchestrationPlan.stages.unique_id",
                )
            seen_ids.add(stage.stage_id.value)
            if stage.sequence_index in seen_indexes:
                raise EducationalInvariantViolation(
                    "orchestration stages must have unique sequence indexes",
                    invariant="OrchestrationPlan.stages.unique_index",
                )
            seen_indexes.add(stage.sequence_index)
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )

    def ordered_stages(self) -> tuple[OrchestrationStage, ...]:
        return tuple(sorted(self.stages, key=lambda s: s.sequence_index))

    def stage_by_id(self, stage_id: OrchestrationStageId) -> OrchestrationStage:
        for stage in self.stages:
            if stage.stage_id == stage_id:
                return stage
        raise EducationalInvariantViolation(
            "orchestration stage is not owned by this plan",
            invariant="OrchestrationPlan.stage.not_found",
        )

    def stage_count(self) -> int:
        return len(self.stages)

    def required_stage_count(self) -> int:
        return sum(1 for stage in self.stages if stage.required)

    def with_stages(
        self, stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage]
    ) -> OrchestrationPlan:
        """Return a plan with replaced stages (same identity)."""
        return OrchestrationPlan(
            plan_id=self.plan_id,
            stages=tuple(stages),
            label=self.label,
        )

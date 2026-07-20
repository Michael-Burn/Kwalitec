"""Policy governing EducationalOrchestrator construction and transitions.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    ORCHESTRATION_INVARIANTS.md
Concept
    Orchestration Policy

Enforces identity, ownership, and lifecycle law for coordination only.
Does not diagnose, interpret evidence, choose strategies, or change priorities.
"""

from __future__ import annotations

from domain.education.foundation.base import require_identity_value
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import OrchestratorId
from domain.education.orchestrator.entities.orchestration_plan import (
    OrchestrationPlan,
)
from domain.education.orchestrator.entities.orchestration_reference import (
    ApprovedDecisionReference,
    EpisodeReference,
    StrategyReference,
)
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStage,
)
from domain.education.orchestrator.enums import (
    OrchestrationStageKind,
    OrchestrationStatus,
)
from domain.education.orchestrator.value_objects.orchestration_state import (
    OrchestrationState,
)

_TERMINAL = frozenset({OrchestrationStatus.COMPLETED})
_STARTABLE = frozenset({OrchestrationStatus.PLANNED})
_ADVANCEABLE = frozenset({OrchestrationStatus.ACTIVE})
_PAUSEABLE = frozenset({OrchestrationStatus.ACTIVE})
_RESUMABLE = frozenset({OrchestrationStatus.PAUSED})


class OrchestrationPolicy:
    """Enforces EducationalOrchestrator identity, ownership, and lifecycle law."""

    @staticmethod
    def assert_identity(orchestrator_id: OrchestratorId) -> OrchestratorId:
        if not isinstance(orchestrator_id, OrchestratorId):
            raise EducationalInvariantViolation(
                "orchestrator must possess an OrchestratorId identity",
                invariant="EducationalOrchestrator.identity.required",
            )
        return orchestrator_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_decision_reference(
        decision_reference: ApprovedDecisionReference,
    ) -> ApprovedDecisionReference:
        if not isinstance(decision_reference, ApprovedDecisionReference):
            raise EducationalInvariantViolation(
                "orchestration must reference an approved decision",
                invariant="EducationalOrchestrator.decision.required",
            )
        if not decision_reference.approved:
            raise EducationalInvariantViolation(
                "orchestration must reference an approved decision",
                invariant="EducationalOrchestrator.decision.approved",
            )
        return decision_reference

    @staticmethod
    def assert_strategy_references(
        references: tuple[StrategyReference, ...] | list[StrategyReference],
    ) -> tuple[StrategyReference, ...]:
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "orchestration must reference at least one teaching strategy",
                invariant="EducationalOrchestrator.strategy.min",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, StrategyReference):
                raise EducationalInvariantViolation(
                    "strategy references must be StrategyReference values",
                    invariant="EducationalOrchestrator.strategy.type",
                )
            if ref.strategy_id.value in seen:
                raise EducationalInvariantViolation(
                    "strategy references must be unique by identity",
                    invariant="EducationalOrchestrator.strategy.unique",
                )
            seen.add(ref.strategy_id.value)
        return collected

    @staticmethod
    def assert_episode_references(
        references: tuple[EpisodeReference, ...] | list[EpisodeReference],
    ) -> tuple[EpisodeReference, ...]:
        collected = tuple(references)
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, EpisodeReference):
                raise EducationalInvariantViolation(
                    "episode references must be EpisodeReference values",
                    invariant="EducationalOrchestrator.episode.type",
                )
            if ref.episode_id.value in seen:
                raise EducationalInvariantViolation(
                    "episode references must be unique by identity",
                    invariant="EducationalOrchestrator.episode.unique",
                )
            seen.add(ref.episode_id.value)
        return collected

    @staticmethod
    def assert_plan(plan: OrchestrationPlan) -> OrchestrationPlan:
        if not isinstance(plan, OrchestrationPlan):
            raise EducationalInvariantViolation(
                "orchestration must possess an OrchestrationPlan",
                invariant="EducationalOrchestrator.plan.required",
            )
        if plan.stage_count() < 1:
            raise EducationalInvariantViolation(
                "orchestration must contain at least one stage",
                invariant="EducationalOrchestrator.stages.min",
            )
        return plan

    @staticmethod
    def assert_state(state: OrchestrationState) -> OrchestrationState:
        if not isinstance(state, OrchestrationState):
            raise EducationalInvariantViolation(
                "orchestration must possess an OrchestrationState",
                invariant="EducationalOrchestrator.state.required",
            )
        return state

    @staticmethod
    def assert_stages(
        stages: tuple[OrchestrationStage, ...] | list[OrchestrationStage],
    ) -> tuple[OrchestrationStage, ...]:
        collected = tuple(stages)
        if len(collected) < 1:
            raise EducationalInvariantViolation(
                "orchestration must contain at least one stage",
                invariant="EducationalOrchestrator.stages.min",
            )
        for stage in collected:
            if not isinstance(stage, OrchestrationStage):
                raise EducationalInvariantViolation(
                    "stages must be OrchestrationStage entities",
                    invariant="EducationalOrchestrator.stages.type",
                )
        return collected

    @classmethod
    def assert_can_start(cls, status: OrchestrationStatus) -> None:
        if status not in _STARTABLE:
            raise EducationalInvariantViolation(
                f"cannot start orchestration in status {status.value}",
                invariant="EducationalOrchestrator.start.status",
            )

    @classmethod
    def assert_can_advance(cls, status: OrchestrationStatus) -> None:
        if status not in _ADVANCEABLE:
            raise EducationalInvariantViolation(
                f"cannot advance orchestration in status {status.value}",
                invariant="EducationalOrchestrator.advance.status",
            )

    @classmethod
    def assert_can_pause(cls, status: OrchestrationStatus) -> None:
        if status not in _PAUSEABLE:
            raise EducationalInvariantViolation(
                f"cannot pause orchestration in status {status.value}",
                invariant="EducationalOrchestrator.pause.status",
            )

    @classmethod
    def assert_can_resume(cls, status: OrchestrationStatus) -> None:
        if status in _TERMINAL:
            raise EducationalInvariantViolation(
                "cannot resume a completed orchestration",
                invariant="EducationalOrchestrator.resume.completed",
            )
        if status not in _RESUMABLE:
            raise EducationalInvariantViolation(
                f"cannot resume orchestration in status {status.value}",
                invariant="EducationalOrchestrator.resume.status",
            )

    @classmethod
    def assert_can_complete(
        cls,
        status: OrchestrationStatus,
        *,
        required_stages_complete: bool,
    ) -> None:
        if status in _TERMINAL:
            raise EducationalInvariantViolation(
                "orchestration is already completed",
                invariant="EducationalOrchestrator.complete.already",
            )
        if status is not OrchestrationStatus.ACTIVE:
            raise EducationalInvariantViolation(
                f"cannot complete orchestration in status {status.value}",
                invariant="EducationalOrchestrator.complete.status",
            )
        if not required_stages_complete:
            raise EducationalInvariantViolation(
                "orchestration cannot complete with incomplete required stages",
                invariant="EducationalOrchestrator.complete.required_stages",
            )

    @staticmethod
    def assert_not_terminal(
        status: OrchestrationStatus, *, action: str
    ) -> None:
        if status in _TERMINAL:
            raise EducationalInvariantViolation(
                f"cannot {action} a completed orchestration",
                invariant=f"EducationalOrchestrator.{action}.terminal",
            )

    @staticmethod
    def assert_episode_creation_stage(
        stage: OrchestrationStage,
    ) -> None:
        if stage.kind is not OrchestrationStageKind.EPISODE_CREATION:
            raise EducationalInvariantViolation(
                "episode registration is only lawful on episode creation stages",
                invariant="EducationalOrchestrator.register_episode.stage_kind",
            )

    @staticmethod
    def assert_pause_reason(reason: str) -> str:
        cleaned = reason.strip() if isinstance(reason, str) else ""
        if not cleaned:
            raise EducationalInvariantViolation(
                "pause reason is required",
                invariant="EducationalOrchestrator.pause.reason.required",
            )
        return cleaned

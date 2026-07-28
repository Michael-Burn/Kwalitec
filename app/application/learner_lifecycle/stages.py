"""Lifecycle stage catalogue — operational identifiers only (LP-001)."""

from __future__ import annotations

from enum import StrEnum

from app.application.learner_lifecycle.versions import (
    EVIDENCE_RECORD_STAGE_ORDER,
    EVIDENCE_STAGE_ORDER,
    ONBOARDING_STAGE_ORDER,
)


class LifecycleStage(StrEnum):
    """Named stages of learner lifecycle orchestration."""

    BIND_INSTANCE = "bind_instance"
    INITIALISE_NODE_STATE = "initialise_node_state"
    RECORD_EVIDENCE = "record_evidence"
    TWIN_BELIEFS = "twin_beliefs"
    EDUCATIONAL_DECISIONS = "educational_decisions"
    EXPERIENCE_MODELS = "experience_models"

    @classmethod
    def onboarding_ordered(cls) -> tuple[LifecycleStage, ...]:
        return tuple(cls(token) for token in ONBOARDING_STAGE_ORDER)

    @classmethod
    def evidence_ordered(
        cls, *, include_record: bool = False
    ) -> tuple[LifecycleStage, ...]:
        order = (
            EVIDENCE_RECORD_STAGE_ORDER if include_record else EVIDENCE_STAGE_ORDER
        )
        return tuple(cls(token) for token in order)


class OperationType(StrEnum):
    """Lifecycle operation kinds."""

    ONBOARD = "onboard"
    EVIDENCE_REFRESH = "evidence_refresh"
    RECOVER = "recover"
    ENSURE = "ensure"


class OperationStatus(StrEnum):
    """Persisted lifecycle operation status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

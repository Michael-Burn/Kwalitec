"""Curriculum Intelligence Agent framework (EI-001B).

Agents execute educational transformations.
Generations are immutable snapshots produced by Agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime

from app.application.curriculum_intelligence.mock_generation_runners import (
    GenerationRunContext,
    GenerationRunner,
)
from app.domain.curriculum_intelligence.agent import AgentDescriptor
from app.domain.curriculum_intelligence.decision_ledger import (
    ledger_entry_from_educational_decision,
)
from app.domain.curriculum_intelligence.generation import CurriculumGenerationSnapshot
from app.domain.curriculum_intelligence.policy import EducationalDecision


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def record_educational_decisions(
    context: GenerationRunContext,
    decisions: tuple[EducationalDecision, ...] | list[EducationalDecision],
    *,
    generation_index: int,
    generation_id: str,
    agent_id: str,
    created_at_iso: str,
    snapshot_id: str = "",
) -> None:
    """Append EducationalDecisions onto the context Decision Ledger sink."""
    if context.pending_decisions is None:
        return
    for decision in decisions:
        context.pending_decisions.append(
            ledger_entry_from_educational_decision(
                decision,
                chain_id=context.chain_id,
                generation_index=generation_index,
                generation_id=generation_id,
                agent_id=agent_id,
                created_at_iso=created_at_iso,
                snapshot_id=snapshot_id,
            )
        )


@dataclass(frozen=True)
class AgentRunResult:
    """Outcome wrapper for agent execution (snapshot is the generation)."""

    snapshot: CurriculumGenerationSnapshot


class CurriculumIntelligenceAgent(GenerationRunner, ABC):
    """Common Agent interface — also a GenerationRunner for the orchestrator."""

    @property
    @abstractmethod
    def descriptor(self) -> AgentDescriptor:
        """Expose agent metadata required by EI-001B."""

    @abstractmethod
    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        """Perform the educational transformation for this agent."""

    def run(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        """GenerationRunner compatibility — delegates to ``execute``."""
        return self.execute(context)

    @property
    def agent_id(self) -> str:
        return self.descriptor.agent_id

    @property
    def name(self) -> str:
        return self.descriptor.name

    @property
    def purpose(self) -> str:
        return self.descriptor.purpose

    @property
    def consumes(self) -> tuple[str, ...]:
        return self.descriptor.consumes

    @property
    def produces(self) -> tuple[str, ...]:
        return self.descriptor.produces

    @property
    def dependencies(self) -> tuple[str, ...]:
        return self.descriptor.dependencies

    @property
    def version(self) -> str:
        return self.descriptor.version

    @property
    def deterministic(self) -> bool:
        return self.descriptor.deterministic

    @property
    def supports_rollback(self) -> bool:
        return self.descriptor.supports_rollback

    @property
    def quality_metrics_produced(self) -> tuple[str, ...]:
        return self.descriptor.quality_metrics_produced

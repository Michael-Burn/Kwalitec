"""Domain Strategy Output — lawful Strategy contribution under Composition.

Capability 4.9.5 cargo collected by the Twin Update Coordinator and supplied
to Twin Composer. Opaque to educational interpretation: the Coordinator
never densifies, scores, or recommends from this payload.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.application.twin_update.reasoning import ReasoningTrace
from app.domain.twin.knowledge_state import KnowledgeState

KNOWLEDGE_STRATEGY_IDENTITY = "Knowledge"
KNOWLEDGE_OWNED_DOMAIN = "knowledge"


@dataclass(frozen=True)
class DomainStrategyOutput:
    """Interpretive contribution for one Strategy-owned Twin domain.

    Attributes:
        strategy_identity: Named Twin Update Strategy that authored this output.
        owned_domain: Domain key the Strategy owns (e.g. ``knowledge``).
        domain_contribution: Opaque domain state contribution (never inspected
            educationally by the Coordinator).
        preserved: True when Educational Sufficiency yielded preservation —
            still a lawful success output, not failure.
        reasoning_trace: Optional explainability cargo (required for Knowledge
            Strategy Version 1.0 outputs via ``KnowledgeStrategyOutput``).
    """

    strategy_identity: str
    owned_domain: str
    domain_contribution: Any
    preserved: bool = False
    reasoning_trace: ReasoningTrace | None = None

    @classmethod
    def create(
        cls,
        strategy_identity: str,
        owned_domain: str,
        domain_contribution: Any,
        *,
        preserved: bool = False,
        reasoning_trace: ReasoningTrace | None = None,
    ) -> DomainStrategyOutput:
        """Construct a Domain Strategy Output.

        Raises:
            ValueError: If strategy identity or owned domain is blank.
        """
        identity = (
            strategy_identity.strip() if isinstance(strategy_identity, str) else ""
        )
        if not identity:
            raise ValueError("strategy_identity must be a non-empty string")
        domain = owned_domain.strip() if isinstance(owned_domain, str) else ""
        if not domain:
            raise ValueError("owned_domain must be a non-empty string")
        return cls(
            strategy_identity=identity,
            owned_domain=domain,
            domain_contribution=domain_contribution,
            preserved=bool(preserved),
            reasoning_trace=reasoning_trace,
        )


@dataclass(frozen=True)
class KnowledgeStrategyOutput(DomainStrategyOutput):
    """Knowledge-domain DomainStrategyOutput with required ReasoningTrace.

    Speaks DomainStrategyOutput for Composer / Coordinator assembly. Adds no
    new dataclass fields — factories enforce explainability and domain ownership.
    """

    @classmethod
    def create_knowledge(
        cls,
        knowledge: KnowledgeState,
        reasoning_trace: ReasoningTrace,
        *,
        preserved: bool = False,
        strategy_identity: str = KNOWLEDGE_STRATEGY_IDENTITY,
    ) -> KnowledgeStrategyOutput:
        """Author a Knowledge Strategy Output.

        Raises:
            ValueError: If ``knowledge`` is not a KnowledgeState or identity blank.
            TypeError: If ``reasoning_trace`` is not a ReasoningTrace.
        """
        if not isinstance(knowledge, KnowledgeState):
            raise ValueError(
                "domain_contribution must be a KnowledgeState, "
                f"got {type(knowledge).__name__}"
            )
        if not isinstance(reasoning_trace, ReasoningTrace):
            raise TypeError(
                "reasoning_trace must be a ReasoningTrace, "
                f"got {type(reasoning_trace).__name__}"
            )
        identity = (
            strategy_identity.strip()
            if isinstance(strategy_identity, str)
            else ""
        )
        if not identity:
            raise ValueError("strategy_identity must be a non-empty string")
        return cls(
            strategy_identity=identity,
            owned_domain=KNOWLEDGE_OWNED_DOMAIN,
            domain_contribution=knowledge,
            preserved=bool(preserved),
            reasoning_trace=reasoning_trace,
        )

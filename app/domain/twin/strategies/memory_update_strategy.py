"""Memory Update Strategy for the Twin Update Pipeline.

Evolves ``MemoryState`` from Memory-related Learning Evidence using
intentionally simple structural rules: create retention slots, append
revision evidence references, refresh ``last_reinforced`` / ``last_updated``.
Does not compute retention, forgetting, spaced repetition, memory strength,
confidence, or readiness.
"""

from __future__ import annotations

from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.memory_state import MemoryState, RetentionRecord
from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.update_context import UpdateContext

# Evidence types that may revise Memory structure. Knowledge / Behaviour /
# Performance / Planning types are intentionally excluded so sibling
# strategies own those domains without double-counting here.
MEMORY_EVIDENCE_TYPES: frozenset[EvidenceType] = frozenset(
    {
        EvidenceType.REVISION_SESSION,
        EvidenceType.FLASHCARD_REVIEW,
    }
)


class MemoryUpdateStrategy(BaseUpdateStrategy):
    """Update MemoryState from Memory-related Learning Evidence.

    Behaviour (Capability 2.4 — intentionally simple):

    - ``supports`` when the context contains at least one Memory-related
      evidence record with a non-empty ``topic_id``.
    - Create a ``RetentionRecord`` when a topic is first observed.
    - Append the evidence id to ``MemoryState.revision_ids``.
    - Set ``RetentionRecord.last_reinforced`` to the evidence timestamp
      when it is newer than the stored value (structural clock only).
    - Set ``MemoryState.last_updated`` to the latest processed timestamp.
    - Leave ``retention_belief`` untouched (never computed here).
    - Return a new immutable ``DigitalTwin``; never mutate the input Twin.
    """

    @property
    def name(self) -> str:
        """Stable strategy identifier recorded in UpdateResult."""
        return "memory_update"

    def supports(self, context: UpdateContext) -> bool:
        """Return True when Memory-related, topic-scoped evidence is present.

        Args:
            context: Immutable update context under consideration.

        Returns:
            Whether ``apply`` should run for this context.
        """
        return any(self._is_applicable_evidence(item) for item in context.evidence)

    def apply(self, context: UpdateContext) -> DigitalTwin:
        """Produce a Twin with MemoryState evolved from applicable evidence.

        Args:
            context: Immutable update context previously accepted by
                ``supports``. Must not be mutated.

        Returns:
            A new DigitalTwin whose ``memory`` reflects structural updates.
            Other domain states are preserved by reference from the input Twin.
        """
        twin = context.twin
        applicable = [
            item for item in context.evidence if self._is_applicable_evidence(item)
        ]
        if not applicable:
            return twin

        retention: dict[str, RetentionRecord] = {
            record.topic_id: record for record in twin.memory.retention
        }
        topic_order = [record.topic_id for record in twin.memory.retention]
        revision_ids = list(twin.memory.revision_ids)
        last_updated = twin.memory.last_updated

        for evidence in applicable:
            topic_id = self._normalized_topic_id(evidence)
            if topic_id is None:
                continue

            if evidence.evidence_id not in revision_ids:
                revision_ids.append(evidence.evidence_id)

            existing = retention.get(topic_id)
            if existing is None:
                retention[topic_id] = RetentionRecord.create(
                    topic_id,
                    last_reinforced=evidence.timestamp,
                )
                topic_order.append(topic_id)
            else:
                last_reinforced = existing.last_reinforced
                if last_reinforced is None or evidence.timestamp > last_reinforced:
                    last_reinforced = evidence.timestamp
                retention[topic_id] = RetentionRecord.create(
                    topic_id,
                    retention_belief=existing.retention_belief,
                    last_reinforced=last_reinforced,
                )

            if last_updated is None or evidence.timestamp > last_updated:
                last_updated = evidence.timestamp

        memory = MemoryState.create(
            retention=[retention[topic_id] for topic_id in topic_order],
            revision_ids=revision_ids,
            last_updated=last_updated,
        )
        return DigitalTwin.create(
            twin.identity,
            goals=twin.goals,
            knowledge=twin.knowledge,
            memory=memory,
            behaviour=twin.behaviour,
            performance=twin.performance,
            predictions=twin.predictions,
        )

    @staticmethod
    def _is_memory_type(evidence: LearningEvidence) -> bool:
        """Return True when ``evidence`` belongs to the Memory catalogue."""
        return evidence.evidence_type in MEMORY_EVIDENCE_TYPES

    @classmethod
    def _normalized_topic_id(cls, evidence: LearningEvidence) -> str | None:
        """Return a non-empty topic id, or None when absent/blank."""
        topic_id = evidence.topic_id
        if not isinstance(topic_id, str):
            return None
        normalized = topic_id.strip()
        return normalized or None

    @classmethod
    def _is_applicable_evidence(cls, evidence: LearningEvidence) -> bool:
        """Return True for Memory-related evidence with a usable topic id."""
        return cls._is_memory_type(evidence) and cls._normalized_topic_id(
            evidence
        ) is not None

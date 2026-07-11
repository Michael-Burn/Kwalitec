"""Knowledge Update Strategy for the Twin Update Pipeline.

Evolves ``KnowledgeState`` from Knowledge-related Learning Evidence using
intentionally simple structural rules: create topic slots, append evidence
references, and refresh ``last_updated``. Does not compute mastery,
confidence, readiness, pass probability, or forgetting curves.
"""

from __future__ import annotations

from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.knowledge_state import KnowledgeState, TopicMasteryRecord
from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.update_context import UpdateContext

# Evidence types that may revise Knowledge structure. Memory / Behaviour /
# Performance / Planning types are intentionally excluded so later strategies
# own those domains without double-counting here.
KNOWLEDGE_EVIDENCE_TYPES: frozenset[EvidenceType] = frozenset(
    {
        EvidenceType.TOPIC_STARTED,
        EvidenceType.TOPIC_COMPLETED,
        EvidenceType.QUESTION_ATTEMPT,
        EvidenceType.QUESTION_CORRECT,
        EvidenceType.QUESTION_INCORRECT,
        EvidenceType.QUESTION_DIFFICULTY,
        EvidenceType.QUIZ_COMPLETED,
        EvidenceType.MOCK_EXAM,
        EvidenceType.PAST_PAPER_ATTEMPT,
        EvidenceType.DIAGNOSTIC_ASSESSMENT,
        EvidenceType.CONFIDENCE_RATING,
    }
)


class KnowledgeUpdateStrategy(BaseUpdateStrategy):
    """Update KnowledgeState from Knowledge-related Learning Evidence.

    Behaviour (Capability 2.3 — intentionally simple):

    - ``supports`` when the context contains at least one Knowledge-related
      evidence record with a non-empty ``topic_id``.
    - Create a ``TopicMasteryRecord`` when a topic is first observed.
    - Append the evidence id to the topic record (evidence count =
      ``len(evidence_ids)``).
    - Append the evidence id to ``KnowledgeState.evidence_ids``.
    - Set ``KnowledgeState.last_updated`` to the latest processed timestamp.
    - Leave ``mastery_belief`` untouched (never computed here).
    - Return a new immutable ``DigitalTwin``; never mutate the input Twin.
    """

    @property
    def name(self) -> str:
        """Stable strategy identifier recorded in UpdateResult."""
        return "knowledge_update"

    def supports(self, context: UpdateContext) -> bool:
        """Return True when Knowledge-related, topic-scoped evidence is present.

        Args:
            context: Immutable update context under consideration.

        Returns:
            Whether ``apply`` should run for this context.
        """
        return any(self._is_applicable_evidence(item) for item in context.evidence)

    def apply(self, context: UpdateContext) -> DigitalTwin:
        """Produce a Twin with KnowledgeState evolved from applicable evidence.

        Args:
            context: Immutable update context previously accepted by
                ``supports``. Must not be mutated.

        Returns:
            A new DigitalTwin whose ``knowledge`` reflects structural updates.
            Other domain states are preserved by reference from the input Twin.
        """
        twin = context.twin
        applicable = [
            item for item in context.evidence if self._is_applicable_evidence(item)
        ]
        if not applicable:
            return twin

        topics: dict[str, TopicMasteryRecord] = {
            record.topic_id: record for record in twin.knowledge.topic_mastery
        }
        topic_order = [record.topic_id for record in twin.knowledge.topic_mastery]
        state_evidence_ids = list(twin.knowledge.evidence_ids)
        last_updated = twin.knowledge.last_updated

        for evidence in applicable:
            topic_id = self._normalized_topic_id(evidence)
            if topic_id is None:
                continue

            if evidence.evidence_id not in state_evidence_ids:
                state_evidence_ids.append(evidence.evidence_id)

            existing = topics.get(topic_id)
            if existing is None:
                topics[topic_id] = TopicMasteryRecord.create(
                    topic_id,
                    evidence_ids=(evidence.evidence_id,),
                )
                topic_order.append(topic_id)
            else:
                evidence_ids = list(existing.evidence_ids)
                if evidence.evidence_id not in evidence_ids:
                    evidence_ids.append(evidence.evidence_id)
                topics[topic_id] = TopicMasteryRecord.create(
                    topic_id,
                    mastery_belief=existing.mastery_belief,
                    evidence_ids=evidence_ids,
                )

            if last_updated is None or evidence.timestamp > last_updated:
                last_updated = evidence.timestamp

        knowledge = KnowledgeState.create(
            topic_mastery=[topics[topic_id] for topic_id in topic_order],
            evidence_ids=state_evidence_ids,
            last_updated=last_updated,
        )
        return DigitalTwin.create(
            twin.identity,
            goals=twin.goals,
            knowledge=knowledge,
            memory=twin.memory,
            behaviour=twin.behaviour,
            performance=twin.performance,
            predictions=twin.predictions,
        )

    @staticmethod
    def _is_knowledge_type(evidence: LearningEvidence) -> bool:
        """Return True when ``evidence`` belongs to the Knowledge catalogue."""
        return evidence.evidence_type in KNOWLEDGE_EVIDENCE_TYPES

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
        """Return True for Knowledge-related evidence with a usable topic id."""
        return cls._is_knowledge_type(evidence) and cls._normalized_topic_id(
            evidence
        ) is not None

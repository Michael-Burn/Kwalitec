"""Knowledge Update Strategy — Version 1.0 Application Layer interpreter.

Capability 4.9.9 realisation of Twin Update Strategies (4.9.1–4.9.5) for the
Knowledge domain. Consumes Current Twin + EducationalEvidencePackage and
returns a KnowledgeStrategyOutput (DomainStrategyOutput) containing only a
replacement KnowledgeState — never a whole Twin.

Educational policy (Version 1): prefer preservation. Knowledge evolves only
when assessment observation satisfies Version 1 educational sufficiency.
Mission completion, practice alone, study duration, and reflection alone do
not justify Knowledge growth. Unknown remains unknown. No mastery scores,
readiness, recommendations, or predictions.

Coexists with Cap 2.3 ``app.domain.twin.strategies.KnowledgeUpdateStrategy``
(LearningEvidence → whole Twin). This module is the Cap 4.9 composition path.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping

from app.application.twin_update.evidence import (
    EducationalEvidencePackage,
    ObservedEvent,
)
from app.application.twin_update.outputs import (
    KNOWLEDGE_OWNED_DOMAIN,
    KNOWLEDGE_STRATEGY_IDENTITY,
    KnowledgeStrategyOutput,
)
from app.application.twin_update.reasoning import ReasoningTrace
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.knowledge_state import KnowledgeState, TopicMasteryRecord

logger = logging.getLogger(__name__)

_PRESERVE_NO_EVIDENCE = (
    "Knowledge preserved — no educational warrant for Knowledge evolution."
)
_PRESERVE_MISSION = (
    "Knowledge preserved — mission completion alone is insufficient."
)
_PRESERVE_PRACTICE = (
    "Knowledge preserved — practice observation without assessment."
)
_PRESERVE_REFLECTION = (
    "Knowledge preserved — reflection alone is insufficient."
)
_PRESERVE_DURATION = (
    "Knowledge preserved — study duration alone is insufficient."
)
_PRESERVE_ASSESSMENT_NO_TOPIC = (
    "Knowledge preserved — assessment observation without topic scope."
)
_PRESERVE_UNCERTAIN = (
    "Knowledge preserved — educational sufficiency uncertain."
)
_UPDATE_ASSESSMENT = (
    "Knowledge updated — assessment observation satisfied "
    "Version 1 educational sufficiency."
)

_KNOWN_OBSERVED_EVENTS: frozenset[ObservedEvent] = frozenset(ObservedEvent)


class KnowledgeUpdateStrategy:
    """Interpret Educational Evidence for KnowledgeState succession only.

    Implements TwinUpdateStrategyProtocol. Never mutates Current Twin.
    Never inspects Behaviour / Memory / Performance / Goals / Identity for
    authorship. Never recommends, scores readiness, or persists.
    """

    @property
    def strategy_identity(self) -> str:
        """Named Strategy identity for operational tracing."""
        return KNOWLEDGE_STRATEGY_IDENTITY

    @property
    def owned_domain(self) -> str:
        """Twin domain this Strategy owns under Composition."""
        return KNOWLEDGE_OWNED_DOMAIN

    def interpret(
        self,
        current_twin: DigitalTwin,
        evidence: EducationalEvidencePackage,
    ) -> KnowledgeStrategyOutput:
        """Author a Knowledge Domain Strategy Output.

        Args:
            current_twin: Lawful immutable Current Twin (Knowledge domain read).
            evidence: Immutable Educational Evidence Package.

        Returns:
            KnowledgeStrategyOutput with replacement KnowledgeState and
            ReasoningTrace. ``preserved=True`` when Educational Sufficiency
            does not warrant densification.

        Raises:
            ValueError: Invalid KnowledgeState, unknown observed_event, or
                malformed assessment_result. Never fabricates Knowledge.
        """
        logger.info("Knowledge Strategy started")

        knowledge = _require_knowledge_state(current_twin)
        _validate_evidence(evidence)
        logger.info("Evidence validated")

        if _assessment_update_eligible(evidence):
            updated = _structural_knowledge_update(knowledge, evidence)
            output = KnowledgeStrategyOutput.create_knowledge(
                updated,
                ReasoningTrace.create(_UPDATE_ASSESSMENT),
                preserved=False,
                strategy_identity=self.strategy_identity,
            )
            logger.info("Knowledge updated")
            logger.info("Strategy completed")
            return output

        reason = _preservation_reason(evidence)
        output = KnowledgeStrategyOutput.create_knowledge(
            knowledge,
            ReasoningTrace.create(reason),
            preserved=True,
            strategy_identity=self.strategy_identity,
        )
        logger.info("Knowledge preserved")
        logger.info("Strategy completed")
        return output


def _require_knowledge_state(current_twin: DigitalTwin) -> KnowledgeState:
    if current_twin is None:
        raise ValueError("Current Twin is required")
    if not isinstance(current_twin, DigitalTwin):
        raise ValueError("Current Twin payload is not a DigitalTwin")
    knowledge = getattr(current_twin, "knowledge", None)
    if not isinstance(knowledge, KnowledgeState):
        raise ValueError(
            "Invalid KnowledgeState: Current Twin.knowledge must be a "
            f"KnowledgeState, got {type(knowledge).__name__}"
        )
    return knowledge


def _validate_evidence(evidence: EducationalEvidencePackage) -> None:
    if evidence is None:
        raise ValueError("Educational Evidence Package is required")
    if not isinstance(evidence, EducationalEvidencePackage):
        raise ValueError(
            "evidence must be an EducationalEvidencePackage, "
            f"got {type(evidence).__name__}"
        )

    events = evidence.observed_events
    if events is None or not isinstance(events, tuple) or len(events) == 0:
        raise ValueError("observed_events must be a non-empty collection")

    for event in events:
        if not isinstance(event, ObservedEvent):
            raise ValueError(
                f"unknown observed_event: {event!r}"
            )
        if event not in _KNOWN_OBSERVED_EVENTS:
            raise ValueError(
                f"unknown observed_event: {event!r}"
            )

    if evidence.assessment_result is not None:
        _validate_assessment_result(evidence.assessment_result)


def _validate_assessment_result(assessment: Mapping[str, object]) -> None:
    if not isinstance(assessment, Mapping):
        raise ValueError("malformed assessment_result: must be a mapping")
    if len(assessment) == 0:
        raise ValueError("malformed assessment_result: empty mapping")
    for key in assessment:
        if not isinstance(key, str) or not key.strip():
            raise ValueError(
                "malformed assessment_result: keys must be non-blank strings"
            )


def _assessment_update_eligible(evidence: EducationalEvidencePackage) -> bool:
    """Version 1 educational sufficiency for Knowledge evolution.

    Assessment observation may justify Knowledge evolution when a topic scope
    is present so structural Knowledge can be placed honestly. Absence of
    either returns False — preservation preferred under uncertainty.
    """
    if evidence.assessment_result is None:
        return False
    topic_id = evidence.topic_id
    if not isinstance(topic_id, str) or not topic_id.strip():
        return False
    return True


def _preservation_reason(evidence: EducationalEvidencePackage) -> str:
    """Deterministic preservation attribution (audit wording only)."""
    events = set(evidence.observed_events)

    if evidence.assessment_result is not None:
        topic_id = evidence.topic_id
        if not isinstance(topic_id, str) or not topic_id.strip():
            return _PRESERVE_ASSESSMENT_NO_TOPIC

    if events == {ObservedEvent.MISSION_COMPLETED}:
        return _PRESERVE_MISSION
    if events == {ObservedEvent.PRACTICE_COMPLETED} or events == {
        ObservedEvent.PRACTICE_ATTEMPTED
    }:
        return _PRESERVE_PRACTICE
    if events == {ObservedEvent.STUDY_DURATION}:
        return _PRESERVE_DURATION

    # Reflection is Optional cargo, not an observed_event token.
    if evidence.reflection is not None and evidence.assessment_result is None:
        non_reflection_signal = events - {
            ObservedEvent.SESSION_ENDED_MANUAL,
            ObservedEvent.SESSION_ENDED_TIMEOUT,
            ObservedEvent.SYSTEM_TIMESTAMP,
        }
        if not non_reflection_signal:
            return _PRESERVE_REFLECTION
        if non_reflection_signal <= {
            ObservedEvent.TOPIC_STUDIED,
            ObservedEvent.STUDY_DURATION,
        }:
            return _PRESERVE_REFLECTION

    if ObservedEvent.PRACTICE_COMPLETED in events or (
        ObservedEvent.PRACTICE_ATTEMPTED in events
    ):
        if evidence.assessment_result is None:
            return _PRESERVE_PRACTICE

    if ObservedEvent.MISSION_COMPLETED in events and (
        evidence.assessment_result is None
    ):
        return _PRESERVE_MISSION

    if events == {
        ObservedEvent.SYSTEM_TIMESTAMP,
    } or events <= {
        ObservedEvent.SYSTEM_TIMESTAMP,
        ObservedEvent.SESSION_ENDED_MANUAL,
        ObservedEvent.SESSION_ENDED_TIMEOUT,
    }:
        return _PRESERVE_NO_EVIDENCE

    if ObservedEvent.STUDY_DURATION in events and evidence.assessment_result is None:
        other = events - {
            ObservedEvent.STUDY_DURATION,
            ObservedEvent.SYSTEM_TIMESTAMP,
            ObservedEvent.SESSION_ENDED_MANUAL,
            ObservedEvent.SESSION_ENDED_TIMEOUT,
        }
        if not other:
            return _PRESERVE_DURATION

    return _PRESERVE_UNCERTAIN


def _structural_knowledge_update(
    current: KnowledgeState,
    evidence: EducationalEvidencePackage,
) -> KnowledgeState:
    """Structural Knowledge succession from assessment warrant (Version 1).

    Creates or densifies topic evidence references and refreshes last_updated.
    Never invents mastery_belief values from assessment scores.
    """
    assert evidence.topic_id is not None
    topic_id = evidence.topic_id.strip()
    topics: dict[str, TopicMasteryRecord] = {
        record.topic_id: record for record in current.topic_mastery
    }
    topic_order = [record.topic_id for record in current.topic_mastery]
    state_evidence_ids = list(current.evidence_ids)

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
        topic_evidence_ids = list(existing.evidence_ids)
        if evidence.evidence_id not in topic_evidence_ids:
            topic_evidence_ids.append(evidence.evidence_id)
        topics[topic_id] = TopicMasteryRecord.create(
            topic_id,
            mastery_belief=existing.mastery_belief,
            evidence_ids=topic_evidence_ids,
        )

    return KnowledgeState.create(
        topic_mastery=[topics[tid] for tid in topic_order],
        evidence_ids=state_evidence_ids,
        last_updated=evidence.evidence_timestamp,
    )

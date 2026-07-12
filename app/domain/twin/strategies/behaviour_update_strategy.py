"""Behaviour Update Strategy for the Twin Update Pipeline.

Evolves ``BehaviourState`` from Behaviour-related Learning Evidence using
intentionally simple structural rules: append session/history lineage,
preserve ``consistency_metrics``, append evidence references, and refresh
``last_updated``. Does not compute consistency, adherence, burnout,
velocity, readiness, or recommendations.

Session / practice-unit identity extraction priority (deterministic):

1. Explicit payload keys when present: ``session_id``, ``mission_id``,
   ``practice_unit_id`` (first non-empty string found, in that order)
2. Else ``originating_event_id`` when non-empty
3. Else ``evidence_id`` as the session-history reference for that event

Pattern ids are appended only when already supplied on evidence payload or
metadata (``study_pattern_id`` / ``study_pattern_ids``); never invented.
"""

from __future__ import annotations

from typing import Any

from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.update_context import UpdateContext

# Evidence types that may revise Behaviour structure. Knowledge / Memory /
# Performance / Planning primary types are intentionally excluded so sibling
# strategies own those domains without double-counting here.
# Choice A (Capability 2.5): primary set only — no secondary weak updates.
BEHAVIOUR_EVIDENCE_TYPES: frozenset[EvidenceType] = frozenset(
    {
        EvidenceType.MISSION_COMPLETED,
        EvidenceType.MISSION_MISSED,
        EvidenceType.SKIPPED_SESSION,
        EvidenceType.SESSION_ABANDONED,
        EvidenceType.STUDY_SESSION,
        EvidenceType.TIME_ON_TASK,
        EvidenceType.STUDY_BREAK,
    }
)

_SESSION_ID_PAYLOAD_KEYS: tuple[str, ...] = (
    "session_id",
    "mission_id",
    "practice_unit_id",
)


class BehaviourUpdateStrategy(BaseUpdateStrategy):
    """Update BehaviourState from Behaviour-related Learning Evidence.

    Behaviour (Capability 2.5 — intentionally simple):

    - ``supports`` when the context contains at least one Behaviour-primary
      evidence record. Does **not** require ``topic_id``.
    - Append a practice-unit / session id to ``session_history_ids`` (deduped).
    - Append pattern ids to ``study_pattern_ids`` only when supplied.
    - Append the evidence id to ``BehaviourState.evidence_ids`` (deduped).
    - Preserve ``consistency_metrics`` unchanged (never invent scores).
    - Set ``BehaviourState.last_updated`` to the latest processed timestamp.
    - Return a new immutable ``DigitalTwin``; never mutate the input Twin.
    """

    @property
    def name(self) -> str:
        """Stable strategy identifier recorded in UpdateResult."""
        return "behaviour_update"

    def supports(self, context: UpdateContext) -> bool:
        """Return True when Behaviour-primary evidence is present.

        Args:
            context: Immutable update context under consideration.

        Returns:
            Whether ``apply`` should run for this context.
        """
        return any(self._is_applicable_evidence(item) for item in context.evidence)

    def apply(self, context: UpdateContext) -> DigitalTwin:
        """Produce a Twin with BehaviourState evolved from applicable evidence.

        Args:
            context: Immutable update context previously accepted by
                ``supports``. Must not be mutated.

        Returns:
            A new DigitalTwin whose ``behaviour`` reflects structural updates.
            Other domain states are preserved by reference from the input Twin.
        """
        twin = context.twin
        applicable = [
            item for item in context.evidence if self._is_applicable_evidence(item)
        ]
        if not applicable:
            return twin

        consistency_metrics = dict(twin.behaviour.consistency_metrics)
        session_history_ids = list(twin.behaviour.session_history_ids)
        study_pattern_ids = list(twin.behaviour.study_pattern_ids)
        evidence_ids = list(twin.behaviour.evidence_ids)
        last_updated = twin.behaviour.last_updated

        for evidence in applicable:
            session_id = self._resolve_session_history_id(evidence)
            if session_id not in session_history_ids:
                session_history_ids.append(session_id)

            for pattern_id in self._supplied_pattern_ids(evidence):
                if pattern_id not in study_pattern_ids:
                    study_pattern_ids.append(pattern_id)

            if evidence.evidence_id not in evidence_ids:
                evidence_ids.append(evidence.evidence_id)

            if last_updated is None or evidence.timestamp > last_updated:
                last_updated = evidence.timestamp

        behaviour = BehaviourState.create(
            consistency_metrics=consistency_metrics,
            session_history_ids=session_history_ids,
            study_pattern_ids=study_pattern_ids,
            evidence_ids=evidence_ids,
            last_updated=last_updated,
        )
        return DigitalTwin.create(
            twin.identity,
            goals=twin.goals,
            knowledge=twin.knowledge,
            memory=twin.memory,
            behaviour=behaviour,
            performance=twin.performance,
            predictions=twin.predictions,
        )

    @staticmethod
    def _is_behaviour_type(evidence: LearningEvidence) -> bool:
        """Return True when ``evidence`` belongs to the Behaviour catalogue."""
        return evidence.evidence_type in BEHAVIOUR_EVIDENCE_TYPES

    @classmethod
    def _is_applicable_evidence(cls, evidence: LearningEvidence) -> bool:
        """Return True for Behaviour-primary evidence (topic_id not required)."""
        return cls._is_behaviour_type(evidence)

    @classmethod
    def _resolve_session_history_id(cls, evidence: LearningEvidence) -> str:
        """Resolve a deterministic session/history lineage id for ``evidence``.

        Priority: payload ``session_id`` / ``mission_id`` / ``practice_unit_id``,
        then non-empty ``originating_event_id``, then ``evidence_id``.
        """
        for key in _SESSION_ID_PAYLOAD_KEYS:
            value = cls._normalized_string(evidence.payload.get(key))
            if value is not None:
                return value

        originating = cls._normalized_string(evidence.originating_event_id)
        if originating is not None:
            return originating

        return evidence.evidence_id

    @classmethod
    def _supplied_pattern_ids(cls, evidence: LearningEvidence) -> tuple[str, ...]:
        """Return pattern ids already present on evidence; never invent any."""
        collected: list[str] = []
        for bag in (evidence.payload, evidence.metadata):
            single = cls._normalized_string(bag.get("study_pattern_id"))
            if single is not None and single not in collected:
                collected.append(single)
            multi = bag.get("study_pattern_ids")
            if isinstance(multi, list | tuple):
                for item in multi:
                    normalized = cls._normalized_string(item)
                    if normalized is not None and normalized not in collected:
                        collected.append(normalized)
        return tuple(collected)

    @staticmethod
    def _normalized_string(value: Any) -> str | None:
        """Return a non-empty stripped string, or None when absent/blank."""
        if not isinstance(value, str):
            return None
        normalized = value.strip()
        return normalized or None

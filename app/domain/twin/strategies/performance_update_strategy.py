"""Performance Update Strategy for the Twin Update Pipeline.

Evolves ``PerformanceState`` from Performance-related Learning Evidence using
intentionally simple structural rules: append assessment lineage, create or
merge scoped ``performance_summaries``, append evidence references, and
refresh ``last_updated``. Does not compute accuracy, strength, IRT, pass
probability, readiness, or recommendations.

Scope identity extraction priority (deterministic):

1. Explicit payload / metadata keys when present: ``scope_id``,
   ``assessment_id``, ``quiz_id``, ``mock_id``, ``past_paper_id``,
   ``diagnostic_id`` (first non-empty string found, in that order)
2. Else non-empty ``topic_id`` for topic-scoped summaries
3. Else ``originating_event_id`` when non-empty
4. Else assessment / evidence reference only — do **not** fabricate a scope

Assessment lineage id priority: assessment-instance keys above, else
``evidence_id``.
"""

from __future__ import annotations

from typing import Any

from app.domain.evidence.evidence_type import EvidenceType
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.performance_state import PerformanceState, PerformanceSummary
from app.domain.twin.strategies.base_strategy import BaseUpdateStrategy
from app.domain.twin.update_context import UpdateContext

# Evidence types that may revise Performance structure. Memory / Behaviour /
# Confidence / Planning primary types are intentionally excluded so sibling
# strategies own those domains without double-counting here.
# Choice A (Capability 2.6): primary set only — no secondary weak updates.
PERFORMANCE_EVIDENCE_TYPES: frozenset[EvidenceType] = frozenset(
    {
        EvidenceType.QUIZ_COMPLETED,
        EvidenceType.MOCK_EXAM,
        EvidenceType.PAST_PAPER_ATTEMPT,
        EvidenceType.DIAGNOSTIC_ASSESSMENT,
        EvidenceType.POST_EXAM_OUTCOME,
    }
)

_ASSESSMENT_INSTANCE_KEYS: tuple[str, ...] = (
    "assessment_id",
    "quiz_id",
    "mock_id",
    "past_paper_id",
    "diagnostic_id",
)

_SCOPE_ID_KEYS: tuple[str, ...] = (
    "scope_id",
    *_ASSESSMENT_INSTANCE_KEYS,
)

_CONDITION_KEYS: tuple[str, ...] = (
    "condition",
    "assessment_condition",
)


class PerformanceUpdateStrategy(BaseUpdateStrategy):
    """Update PerformanceState from Performance-related Learning Evidence.

    Behaviour (Capability 2.6 — intentionally simple):

    - ``supports`` when the context contains at least one Performance-primary
      evidence record. Does **not** require ``topic_id`` for all primary types.
    - Append an assessment / attempt id to ``assessment_ids`` (deduped).
    - Append the evidence id to ``PerformanceState.evidence_ids`` (deduped).
    - Create or merge a ``PerformanceSummary`` when a usable ``scope_id`` is
      resolved; overlay only facts supplied by evidence; preserve unknown keys.
    - Store condition tags when evidence supplies them; never upgrade formative
      success to exam-condition strength.
    - Set ``PerformanceState.last_updated`` to the latest processed timestamp.
    - Return a new immutable ``DigitalTwin``; never mutate the input Twin.
    """

    @property
    def name(self) -> str:
        """Stable strategy identifier recorded in UpdateResult."""
        return "performance_update"

    def supports(self, context: UpdateContext) -> bool:
        """Return True when Performance-primary evidence is present.

        Args:
            context: Immutable update context under consideration.

        Returns:
            Whether ``apply`` should run for this context.
        """
        return any(self._is_applicable_evidence(item) for item in context.evidence)

    def apply(self, context: UpdateContext) -> DigitalTwin:
        """Produce a Twin with PerformanceState evolved from applicable evidence.

        Args:
            context: Immutable update context previously accepted by
                ``supports``. Must not be mutated.

        Returns:
            A new DigitalTwin whose ``performance`` reflects structural updates.
            Other domain states are preserved by reference from the input Twin.
        """
        twin = context.twin
        applicable = [
            item for item in context.evidence if self._is_applicable_evidence(item)
        ]
        if not applicable:
            return twin

        assessment_ids = list(twin.performance.assessment_ids)
        evidence_ids = list(twin.performance.evidence_ids)
        summaries: dict[str, PerformanceSummary] = {
            record.scope_id: record
            for record in twin.performance.performance_summaries
        }
        summary_order = [
            record.scope_id for record in twin.performance.performance_summaries
        ]
        last_updated = twin.performance.last_updated

        for evidence in applicable:
            assessment_id = self._resolve_assessment_id(evidence)
            if assessment_id not in assessment_ids:
                assessment_ids.append(assessment_id)

            if evidence.evidence_id not in evidence_ids:
                evidence_ids.append(evidence.evidence_id)

            scope_id = self._resolve_scope_id(evidence)
            if scope_id is not None:
                supplied = self._supplied_summary_facts(evidence)
                existing = summaries.get(scope_id)
                if existing is None:
                    summaries[scope_id] = PerformanceSummary.create(
                        scope_id,
                        summary=supplied,
                    )
                    summary_order.append(scope_id)
                else:
                    merged = dict(existing.summary)
                    merged.update(supplied)
                    summaries[scope_id] = PerformanceSummary.create(
                        scope_id,
                        summary=merged,
                    )

            if last_updated is None or evidence.timestamp > last_updated:
                last_updated = evidence.timestamp

        performance = PerformanceState.create(
            assessment_ids=assessment_ids,
            performance_summaries=[summaries[scope_id] for scope_id in summary_order],
            evidence_ids=evidence_ids,
            last_updated=last_updated,
        )
        return DigitalTwin.create(
            twin.identity,
            goals=twin.goals,
            knowledge=twin.knowledge,
            memory=twin.memory,
            behaviour=twin.behaviour,
            performance=performance,
            predictions=twin.predictions,
        )

    @staticmethod
    def _is_performance_type(evidence: LearningEvidence) -> bool:
        """Return True when ``evidence`` belongs to the Performance catalogue."""
        return evidence.evidence_type in PERFORMANCE_EVIDENCE_TYPES

    @classmethod
    def _is_applicable_evidence(cls, evidence: LearningEvidence) -> bool:
        """Return True for Performance-primary evidence (topic_id not required)."""
        return cls._is_performance_type(evidence)

    @classmethod
    def _resolve_assessment_id(cls, evidence: LearningEvidence) -> str:
        """Resolve a deterministic assessment lineage id for ``evidence``.

        Priority: assessment-instance payload/metadata keys, else
        ``evidence_id``.
        """
        for bag in (evidence.payload, evidence.metadata):
            for key in _ASSESSMENT_INSTANCE_KEYS:
                value = cls._normalized_string(bag.get(key))
                if value is not None:
                    return value
        return evidence.evidence_id

    @classmethod
    def _resolve_scope_id(cls, evidence: LearningEvidence) -> str | None:
        """Resolve a usable ``scope_id``, or None when only weak lineage applies.

        Priority: explicit scope / assessment-instance keys, else non-empty
        ``topic_id``, else non-empty ``originating_event_id``. Never invents
        scopes from free text.
        """
        for bag in (evidence.payload, evidence.metadata):
            for key in _SCOPE_ID_KEYS:
                value = cls._normalized_string(bag.get(key))
                if value is not None:
                    return value

        topic_id = cls._normalized_string(evidence.topic_id)
        if topic_id is not None:
            return topic_id

        return cls._normalized_string(evidence.originating_event_id)

    @classmethod
    def _supplied_summary_facts(cls, evidence: LearningEvidence) -> dict[str, Any]:
        """Return summary facts already present on evidence; never invent scores.

        Copies a nested ``summary`` bag when supplied, and stores condition
        tags only when evidence already carries them.
        """
        facts: dict[str, Any] = {}
        nested = evidence.payload.get("summary")
        if isinstance(nested, dict):
            facts.update(nested)

        for bag in (evidence.payload, evidence.metadata):
            for key in _CONDITION_KEYS:
                value = cls._normalized_string(bag.get(key))
                if value is not None:
                    facts["condition"] = value
                    return facts
        return facts

    @staticmethod
    def _normalized_string(value: Any) -> str | None:
        """Return a non-empty stripped string, or None when absent/blank."""
        if not isinstance(value, str):
            return None
        normalized = value.strip()
        return normalized or None

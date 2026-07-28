"""DecisionBuilder — deterministic EducationalDecision construction."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.reasoning.decisions.versions import (
    DECISION_PROVENANCE_PREFIX,
    DECISION_VERSION,
)
from app.domain.reasoning.decisions.category import (
    DecisionCategory,
    parse_decision_category,
)
from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.reference import DecisionReference


class DecisionBuilder:
    """Build immutable educational decisions without inventing missing facts."""

    def __init__(
        self,
        *,
        context: DecisionContext,
        created_at: datetime | None = None,
    ) -> None:
        self._context = context
        self._created_at = created_at or datetime.now(UTC).replace(tzinfo=None)
        self._seen_ids: set[str] = set()

    @property
    def context(self) -> DecisionContext:
        return self._context

    @property
    def seen_ids(self) -> frozenset[str]:
        return frozenset(self._seen_ids)

    def build(
        self,
        *,
        category: DecisionCategory | str,
        subject_ref: str,
        value: Any,
        reason: DecisionReason,
        observation_ids: tuple[str, ...],
        learning_objective_reference: str,
        concept_reference: str = "",
        payload: dict[str, Any] | None = None,
        decision_key: str | None = None,
    ) -> EducationalDecision:
        """Create one decision; reject duplicate ids within this builder."""
        resolved_category = parse_decision_category(category)
        decision_id = self._decision_id(
            category=resolved_category,
            subject_ref=subject_ref,
            decision_key=decision_key,
        )
        if decision_id in self._seen_ids:
            from app.domain.reasoning.decisions.errors import DuplicateDecision

            raise DuplicateDecision(f"duplicate decision: {decision_id!r}")
        self._seen_ids.add(decision_id)

        context = self._context
        reference = DecisionReference(
            evidence_bundle_id=context.evidence_bundle_id,
            educational_observation_ids=tuple(observation_ids),
            reasoning_request_id=context.reasoning_request_id,
            assessment_session_id=context.session_id,
            correlation_id=context.correlation_id,
            learning_objective_reference=learning_objective_reference,
            concept_reference=concept_reference or "",
            decision_id=decision_id,
        )
        provenance = {
            "prefix": DECISION_PROVENANCE_PREFIX,
            "evidence_bundle_id": context.evidence_bundle_id,
            "educational_observation_ids": list(observation_ids),
            "reasoning_request_id": context.reasoning_request_id,
            "decision_id": decision_id,
            "decision_version": DECISION_VERSION,
            "assessment_session_id": context.session_id,
            "correlation_id": context.correlation_id,
        }
        traceability = {
            **provenance,
            "twin_id": context.twin_id,
            "observation_set_id": context.observation_set_id,
            "prior_twin_version": context.prior_twin_version,
            "subject_ref": subject_ref,
            "category": resolved_category.value,
            "learning_objective_reference": learning_objective_reference,
            "concept_reference": concept_reference or "",
        }
        return EducationalDecision(
            decision_id=decision_id,
            category=resolved_category,
            twin_id=context.twin_id,
            subject_ref=subject_ref,
            value=value,
            reason=reason,
            reference=reference,
            decision_version=DECISION_VERSION,
            created_at=self._created_at,
            provenance=provenance,
            traceability=traceability,
            payload=payload or {},
        )

    def _decision_id(
        self,
        *,
        category: DecisionCategory,
        subject_ref: str,
        decision_key: str | None,
    ) -> str:
        context = self._context
        key = (decision_key or subject_ref or "twin").strip() or "twin"
        return (
            f"ed:{context.reasoning_request_id}:"
            f"{context.evidence_bundle_id}:{category.value}:{key}"
        )

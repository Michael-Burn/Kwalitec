"""Immutable EducationalDecisionSet ready for Twin application."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision import EducationalDecision


@dataclass(frozen=True)
class EducationalDecisionSet:
    """Ordered, immutable set of educational decisions for one reasoning cycle."""

    set_id: str
    decisions: tuple[EducationalDecision, ...]
    context: DecisionContext
    decision_version: str

    def __post_init__(self) -> None:
        if not (self.set_id or "").strip():
            raise ValueError("set_id is required")
        if not (self.decision_version or "").strip():
            raise ValueError("decision_version is required")
        if not isinstance(self.context, DecisionContext):
            raise TypeError("context must be DecisionContext")
        if self.context.decision_version != self.decision_version:
            raise ValueError("decision_version mismatch between context and set")
        if not isinstance(self.decisions, tuple):
            object.__setattr__(self, "decisions", tuple(self.decisions))

        seen: set[str] = set()
        for decision in self.decisions:
            if not isinstance(decision, EducationalDecision):
                raise TypeError(
                    "EducationalDecisionSet accepts EducationalDecision only"
                )
            if decision.decision_id in seen:
                from app.domain.reasoning.decisions.errors import DuplicateDecision

                raise DuplicateDecision(
                    f"duplicate decision: {decision.decision_id!r}"
                )
            seen.add(decision.decision_id)
            if decision.twin_id != self.context.twin_id:
                raise ValueError("decision twin_id mismatch with context")
            if decision.decision_version != self.decision_version:
                raise ValueError("decision_version mismatch within set")

    @property
    def decision_ids(self) -> tuple[str, ...]:
        return tuple(d.decision_id for d in self.decisions)

    @property
    def observation_ids(self) -> tuple[str, ...]:
        ids: list[str] = []
        seen: set[str] = set()
        for decision in self.decisions:
            for oid in decision.reference.educational_observation_ids:
                if oid not in seen:
                    seen.add(oid)
                    ids.append(oid)
        return tuple(ids)

    def __len__(self) -> int:
        return len(self.decisions)

    def by_category(self, category: str) -> tuple[EducationalDecision, ...]:
        return tuple(d for d in self.decisions if d.category.value == category)

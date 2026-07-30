"""Append-only Decision Ledger for Curriculum Intelligence (EI-001D).

Every EducationalDecision is persisted as a DecisionLedgerEntry so Founder
Preview and certification can inspect why the curriculum exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.policy import EducationalDecision


class DecisionType(StrEnum):
    """Educational decision kinds recorded on the ledger."""

    MERGE = "merge"
    SPLIT = "split"
    RETAIN = "retain"
    ATTACH_OBJECTIVE = "attach_objective"
    COVERED = "covered"
    MISSING = "missing"
    UNEXPECTED = "unexpected"
    HIERARCHY = "hierarchy"
    REJECT_NOISE = "reject_noise"
    REPARENT = "reparent"
    CERTIFY = "certify"
    OTHER = "other"


class DecisionOutcome(StrEnum):
    """Outcome recorded for a ledger entry."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WARNING = "warning"
    INFORMATIONAL = "informational"


@dataclass(frozen=True)
class DecisionLedgerEntry:
    """One append-only educational decision record.

    Fields match EI-001D Decision Ledger contract:
    Decision ID · Generation · Agent · Policy · Evidence · Evidence Grade ·
    Confidence · Reasoning Confidence · Affected Nodes · Decision Type ·
    Timestamp · Decision Outcome.
    """

    decision_id: str
    chain_id: str
    generation_index: int
    generation_id: str
    agent_id: str
    policy_id: str
    evidence_refs: tuple[str, ...]
    evidence_grade: EvidenceGrade
    confidence: float
    reasoning_confidence: float
    affected_node_ids: tuple[str, ...]
    decision_type: DecisionType
    created_at_iso: str
    decision_outcome: DecisionOutcome
    reason: str = ""
    detail: str = ""
    snapshot_id: str = ""

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError("decision_id is required")
        if self.generation_index < 1 or self.generation_index > 7:
            raise ValueError(
                f"generation_index must be 1..7, got {self.generation_index}"
            )


@dataclass(frozen=True)
class DecisionLedgerSummary:
    """Aggregated view of a chain's decision ledger for Review Pack."""

    chain_id: str
    entry_count: int
    by_type: tuple[tuple[str, int], ...]
    by_generation: tuple[tuple[int, int], ...]
    mean_confidence: float
    mean_reasoning_confidence: float
    mean_evidence_weight: float
    accepted_count: int
    warning_count: int
    rejected_count: int


def infer_decision_type(action: str) -> DecisionType:
    """Map a policy action string to a DecisionType."""
    normalised = (action or "").strip().lower()
    mapping = {
        "merge": DecisionType.MERGE,
        "split": DecisionType.SPLIT,
        "retain": DecisionType.RETAIN,
        "cover:covered": DecisionType.COVERED,
        "cover:missing": DecisionType.MISSING,
        "cover:unexpected": DecisionType.UNEXPECTED,
        "cover:hierarchy": DecisionType.HIERARCHY,
        "hierarchy_consistent": DecisionType.HIERARCHY,
        "hierarchy_inconsistent": DecisionType.HIERARCHY,
        "reject_noise": DecisionType.REJECT_NOISE,
        "reparent": DecisionType.REPARENT,
        "certify": DecisionType.CERTIFY,
    }
    if normalised in mapping:
        return mapping[normalised]
    if normalised.startswith("obj:") or normalised.startswith("attach"):
        return DecisionType.ATTACH_OBJECTIVE
    if "merge" in normalised:
        return DecisionType.MERGE
    if "split" in normalised:
        return DecisionType.SPLIT
    if "missing" in normalised:
        return DecisionType.MISSING
    if "unexpected" in normalised:
        return DecisionType.UNEXPECTED
    if "cover" in normalised:
        return DecisionType.COVERED
    if "hierarchy" in normalised:
        return DecisionType.HIERARCHY
    if "reject" in normalised or "noise" in normalised:
        return DecisionType.REJECT_NOISE
    return DecisionType.OTHER


def ledger_entry_from_educational_decision(
    decision: EducationalDecision,
    *,
    chain_id: str,
    generation_index: int,
    generation_id: str,
    agent_id: str,
    created_at_iso: str,
    snapshot_id: str = "",
    decision_outcome: DecisionOutcome = DecisionOutcome.ACCEPTED,
    reasoning_confidence: float | None = None,
) -> DecisionLedgerEntry:
    """Lift a Phase C EducationalDecision into a durable ledger entry."""
    affected = tuple(
        dict.fromkeys(decision.subject_node_ids + decision.related_node_ids)
    )
    reasoning = (
        reasoning_confidence
        if reasoning_confidence is not None
        else round(min(1.0, decision.confidence * 0.98 + 0.02), 4)
    )
    return DecisionLedgerEntry(
        decision_id=decision.decision_id,
        chain_id=chain_id,
        generation_index=generation_index,
        generation_id=generation_id,
        agent_id=agent_id,
        policy_id=decision.policy_id,
        evidence_refs=decision.evidence_refs,
        evidence_grade=decision.evidence_grade,
        confidence=decision.confidence,
        reasoning_confidence=reasoning,
        affected_node_ids=affected,
        decision_type=infer_decision_type(decision.action),
        created_at_iso=created_at_iso,
        decision_outcome=decision_outcome,
        reason=decision.reason,
        detail=decision.detail or decision.action,
        snapshot_id=snapshot_id,
    )

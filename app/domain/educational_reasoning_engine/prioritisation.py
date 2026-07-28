"""Deterministic prioritisation and decision merging (EI-007)."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.educational_reasoning_engine.decision import clamp01
from app.domain.educational_reasoning_engine.rules.base import RuleProposal
from app.domain.educational_reasoning_engine.rules.thresholds import (
    DEFAULT_EFFORT_MINUTES,
)


@dataclass
class MergedCandidate:
    """Internal merge accumulator for one (decision_type, target) key."""

    decision_type: str
    curriculum_target: str
    priority_raw: float = 0.0
    rationales: list[str] = field(default_factory=list)
    prerequisite_chain: tuple[str, ...] = ()
    estimated_effort_minutes: int | None = None
    expected_educational_outcome: str = ""
    supporting_belief_ids: set[str] = field(default_factory=set)
    supporting_curriculum_refs: set[str] = field(default_factory=set)
    supporting_evidence_ids: set[str] = field(default_factory=set)
    applied_rule_ids: set[str] = field(default_factory=set)
    proposals: list[RuleProposal] = field(default_factory=list)
    priority_components: list[str] = field(default_factory=list)


def merge_proposals(
    proposals: tuple[RuleProposal, ...] | list[RuleProposal],
) -> list[MergedCandidate]:
    """Merge typed proposals; attach typeless boosts to matching targets."""
    typed: dict[tuple[str, str], MergedCandidate] = {}
    boosts: list[RuleProposal] = []

    for p in proposals:
        if p.decision_type is None:
            boosts.append(p)
            continue
        key = (p.decision_type, p.curriculum_target)
        cand = typed.get(key)
        if cand is None:
            cand = MergedCandidate(
                decision_type=p.decision_type,
                curriculum_target=p.curriculum_target,
            )
            typed[key] = cand
        _apply_proposal(cand, p)

    for p in boosts:
        matches = [
            c for c in typed.values() if c.curriculum_target == p.curriculum_target
        ]
        if not matches:
            continue
        for cand in matches:
            _apply_proposal(cand, p)

    return list(typed.values())


def _apply_proposal(cand: MergedCandidate, proposal: RuleProposal) -> None:
    cand.priority_raw += float(proposal.priority_delta)
    cand.applied_rule_ids.add(proposal.rule_id)
    cand.proposals.append(proposal)
    cand.priority_components.append(
        f"{proposal.rule_id}:{proposal.priority_delta:+.4f}"
    )
    if proposal.rationale:
        cand.rationales.append(proposal.rationale)
    if proposal.prerequisite_chain and not cand.prerequisite_chain:
        cand.prerequisite_chain = proposal.prerequisite_chain
    if proposal.estimated_effort_minutes is not None:
        cand.estimated_effort_minutes = proposal.estimated_effort_minutes
    if proposal.expected_educational_outcome and not cand.expected_educational_outcome:
        cand.expected_educational_outcome = proposal.expected_educational_outcome
    cand.supporting_belief_ids.update(proposal.supporting_belief_ids)
    cand.supporting_curriculum_refs.update(proposal.supporting_curriculum_refs)
    cand.supporting_evidence_ids.update(proposal.supporting_evidence_ids)


def rank_candidates(candidates: list[MergedCandidate]) -> list[MergedCandidate]:
    """Sort by priority desc, then decision_type, then curriculum_target."""
    decorated: list[tuple[float, str, str, MergedCandidate]] = []
    for cand in candidates:
        priority = clamp01(cand.priority_raw)
        decorated.append(
            (-priority, cand.decision_type, cand.curriculum_target, cand)
        )
    decorated.sort()
    return [item[3] for item in decorated]


def resolve_effort(cand: MergedCandidate) -> int:
    if cand.estimated_effort_minutes is not None:
        return int(cand.estimated_effort_minutes)
    return DEFAULT_EFFORT_MINUTES

"""Decision quality scoring for Generation 7 certification (EI-001D)."""

from __future__ import annotations

from collections import Counter

from app.domain.curriculum_intelligence.certification import DecisionQualityScores
from app.domain.curriculum_intelligence.decision_ledger import (
    DecisionLedgerEntry,
    DecisionLedgerSummary,
    DecisionOutcome,
    DecisionType,
)
from app.domain.curriculum_intelligence.evidence import evidence_grade_weight
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    QualitySnapshot,
)


def _mean(values: list[float], default: float = 1.0) -> float:
    if not values:
        return default
    return round(sum(values) / len(values), 4)


def _type_quality(
    entries: tuple[DecisionLedgerEntry, ...],
    decision_type: DecisionType,
    *,
    default: float,
) -> float:
    matched = [e for e in entries if e.decision_type is decision_type]
    if not matched:
        return default
    scores: list[float] = []
    for entry in matched:
        outcome_factor = {
            DecisionOutcome.ACCEPTED: 1.0,
            DecisionOutcome.INFORMATIONAL: 0.9,
            DecisionOutcome.WARNING: 0.7,
            DecisionOutcome.REJECTED: 0.3,
        }.get(entry.decision_outcome, 0.5)
        grade = evidence_grade_weight(entry.evidence_grade)
        scores.append(
            round(
                0.45 * entry.confidence
                + 0.35 * entry.reasoning_confidence
                + 0.15 * grade
                + 0.05 * outcome_factor,
                4,
            )
        )
    return _mean(scores, default)


def compute_decision_quality(
    entries: tuple[DecisionLedgerEntry, ...],
    *,
    snapshot: CurriculumGenerationSnapshot | None = None,
    metrics: QualitySnapshot | None = None,
) -> DecisionQualityScores:
    """Evaluate merge / split / objective / coverage / hierarchy / policy / evidence."""
    merge_q = _type_quality(entries, DecisionType.MERGE, default=0.85)
    split_q = _type_quality(entries, DecisionType.SPLIT, default=0.85)
    objective_q = _type_quality(
        entries, DecisionType.ATTACH_OBJECTIVE, default=0.80
    )
    coverage_entries = [
        e
        for e in entries
        if e.decision_type
        in {
            DecisionType.COVERED,
            DecisionType.MISSING,
            DecisionType.UNEXPECTED,
        }
    ]
    if coverage_entries:
        # Missing concepts depress coverage quality; covered raises it.
        covered = sum(
            1 for e in coverage_entries if e.decision_type is DecisionType.COVERED
        )
        missing = sum(
            1 for e in coverage_entries if e.decision_type is DecisionType.MISSING
        )
        unexpected = sum(
            1 for e in coverage_entries if e.decision_type is DecisionType.UNEXPECTED
        )
        total = max(covered + missing + unexpected, 1)
        coverage_q = round(
            (covered / total) * 0.7
            + (1.0 - missing / total) * 0.2
            + (1.0 - unexpected / total) * 0.1,
            4,
        )
        coverage_q = min(
            1.0,
            coverage_q
            + 0.15
            * _mean([e.confidence for e in coverage_entries], default=0.0)
            * 0.5,
        )
    elif metrics is not None:
        coverage_q = round(metrics.coverage, 4)
    else:
        coverage_q = 0.75

    hierarchy_q = _type_quality(entries, DecisionType.HIERARCHY, default=0.0)
    if hierarchy_q == 0.0 and metrics is not None:
        hierarchy_q = round(metrics.hierarchy, 4)
    elif hierarchy_q == 0.0 and snapshot is not None:
        hierarchy_q = round(snapshot.metrics.hierarchy, 4)
    elif hierarchy_q == 0.0:
        hierarchy_q = 0.7

    # Policy consistency: share of entries that carry a non-empty policy id.
    if entries:
        with_policy = sum(1 for e in entries if e.policy_id)
        policy_consistency = round(with_policy / len(entries), 4)
        # Penalise mixed outcomes with contradictory types on same nodes.
        node_types: dict[str, set[str]] = {}
        for entry in entries:
            for nid in entry.affected_node_ids:
                node_types.setdefault(nid, set()).add(entry.decision_type.value)
        conflicts = sum(
            1
            for types in node_types.values()
            if "merge" in types and "split" in types
        )
        if node_types:
            policy_consistency = round(
                policy_consistency * (1.0 - 0.1 * min(conflicts, 5)),
                4,
            )
    else:
        policy_consistency = 0.7

    if entries:
        evidence_q = _mean(
            [evidence_grade_weight(e.evidence_grade) for e in entries],
            default=0.5,
        )
    elif metrics is not None:
        evidence_q = round(metrics.evidence_quality, 4)
    else:
        evidence_q = 0.5

    aggregate = round(
        0.15 * merge_q
        + 0.10 * split_q
        + 0.15 * objective_q
        + 0.20 * coverage_q
        + 0.15 * hierarchy_q
        + 0.10 * policy_consistency
        + 0.15 * evidence_q,
        4,
    )
    return DecisionQualityScores(
        merge_quality=merge_q,
        split_quality=split_q,
        objective_quality=objective_q,
        coverage_quality=coverage_q,
        hierarchy_quality=hierarchy_q,
        policy_consistency=policy_consistency,
        evidence_quality=evidence_q,
        aggregate=aggregate,
    )


def summarise_decision_ledger(
    chain_id: str,
    entries: tuple[DecisionLedgerEntry, ...],
) -> DecisionLedgerSummary:
    """Build a DecisionLedgerSummary for Review Pack consumers."""
    by_type_counter = Counter(e.decision_type.value for e in entries)
    by_gen_counter = Counter(e.generation_index for e in entries)
    return DecisionLedgerSummary(
        chain_id=chain_id,
        entry_count=len(entries),
        by_type=tuple(sorted(by_type_counter.items())),
        by_generation=tuple(sorted(by_gen_counter.items())),
        mean_confidence=_mean([e.confidence for e in entries], default=0.0),
        mean_reasoning_confidence=_mean(
            [e.reasoning_confidence for e in entries], default=0.0
        ),
        mean_evidence_weight=_mean(
            [evidence_grade_weight(e.evidence_grade) for e in entries],
            default=0.0,
        ),
        accepted_count=sum(
            1 for e in entries if e.decision_outcome is DecisionOutcome.ACCEPTED
        ),
        warning_count=sum(
            1 for e in entries if e.decision_outcome is DecisionOutcome.WARNING
        ),
        rejected_count=sum(
            1 for e in entries if e.decision_outcome is DecisionOutcome.REJECTED
        ),
    )

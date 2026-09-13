"""Pure Progression Readiness evaluator (read-only over Assessment Evidence).

Standalone: no live student-facing consumers. Never writes OEA evidence.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import ObjectiveAssessmentEvidenceStore
from app.application.progression_readiness.contracts import (
    ContractKind,
    DemonstrationPair,
    EvidenceModality,
    ProgressionReadinessContract,
)
from app.application.progression_readiness.results import (
    InsufficientReason,
    ProgressionReadiness,
    ProgressionReadinessResult,
)


def _scored_only(
    evidence: Sequence[AssessmentEvidenceRecord],
) -> tuple[AssessmentEvidenceRecord, ...]:
    """Exclude unscored attempts (scored_correct is None)."""
    return tuple(r for r in evidence if r.scored_correct is not None)


def _latest_per_item(
    evidence: Sequence[AssessmentEvidenceRecord],
    item_ids: frozenset[str],
) -> dict[str, AssessmentEvidenceRecord]:
    """Latest scored observation per contracted item_id."""
    latest: dict[str, AssessmentEvidenceRecord] = {}
    for record in sorted(
        (r for r in evidence if r.item_id in item_ids),
        key=lambda r: (r.occurred_at, r.evidence_id),
    ):
        latest[record.item_id] = record
    return latest


def _prerequisite_verified(
    evidence: Sequence[AssessmentEvidenceRecord],
    prerequisite_objective_id: str,
) -> bool:
    """True iff at least one scored-correct row exists for the prerequisite."""
    oid = (prerequisite_objective_id or "").strip()
    if not oid:
        return True
    return any(
        r.objective_id == oid and r.scored_correct is True for r in evidence
    )


def _critical_misconception_hit(
    latest_by_item: dict[str, AssessmentEvidenceRecord],
    critical_tags: frozenset[str],
) -> bool:
    if not critical_tags:
        return False
    for record in latest_by_item.values():
        if record.scored_correct is False:
            tag = (record.selected_misconception_tag or "").strip()
            if tag and tag in critical_tags:
                return True
    return False


def _result(
    *,
    objective_id: str,
    student_id: str,
    readiness: ProgressionReadiness,
    reason: InsufficientReason | None = None,
) -> ProgressionReadinessResult:
    return ProgressionReadinessResult(
        objective_id=objective_id,
        student_id=student_id,
        readiness=readiness,
        reason=reason,
    )


def _evaluate_conceptual(
    *,
    objective_id: str,
    student_id: str,
    contract: ProgressionReadinessContract,
    latest_by_item: dict[str, AssessmentEvidenceRecord],
) -> ProgressionReadinessResult:
    n = contract.item_count
    ready_min = contract.ready_min_correct
    correct_count = sum(
        1 for r in latest_by_item.values() if r.scored_correct is True
    )
    observed_count = len(latest_by_item)

    if correct_count >= ready_min:
        return _result(
            objective_id=objective_id,
            student_id=student_id,
            readiness=ProgressionReadiness.READY,
        )
    if correct_count == 0 and observed_count == n:
        return _result(
            objective_id=objective_id,
            student_id=student_id,
            readiness=ProgressionReadiness.NOT_READY,
        )
    return _result(
        objective_id=objective_id,
        student_id=student_id,
        readiness=ProgressionReadiness.INSUFFICIENT_EVIDENCE,
        reason=InsufficientReason.INSUFFICIENT_SAMPLE,
    )


def _modality_outcome(
    contract: ProgressionReadinessContract,
    latest_by_item: dict[str, AssessmentEvidenceRecord],
    modality: EvidenceModality,
) -> bool | None:
    """True / False for latest scored of that modality, or None if unobserved."""
    for spec in contract.evidence_items:
        if spec.modality is modality:
            record = latest_by_item.get(spec.item_id)
            if record is None:
                return None
            return bool(record.scored_correct)
    return None


def _pair_four_outcome(
    *,
    latest_by_item: dict[str, AssessmentEvidenceRecord],
    pair: DemonstrationPair,
) -> tuple[ProgressionReadiness, InsufficientReason | None]:
    """Apply the locked single-pair four-outcome matrix to one demonstration pair.

    Returns the pair-stage readiness and, when insufficient, the per-pair
    intermediate reason REQUIRED_MODALITY_NOT_OBSERVED.
    """
    mcq_record = latest_by_item.get(pair.mcq_item_id)
    numeric_record = latest_by_item.get(pair.numeric_item_id)
    if mcq_record is None or numeric_record is None:
        return (
            ProgressionReadiness.INSUFFICIENT_EVIDENCE,
            InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED,
        )

    mcq = bool(mcq_record.scored_correct)
    numeric = bool(numeric_record.scored_correct)

    if mcq and numeric:
        return ProgressionReadiness.READY, None
    if mcq and not numeric:
        return ProgressionReadiness.NOT_READY, None
    if not mcq and numeric:
        return (
            ProgressionReadiness.INSUFFICIENT_EVIDENCE,
            InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED,
        )
    return ProgressionReadiness.NOT_READY, None


def _combine_dual_demonstration(
    pair_a: ProgressionReadiness,
    pair_b: ProgressionReadiness,
) -> tuple[ProgressionReadiness, InsufficientReason]:
    """Apply the locked 9-cell objective-level combination matrix."""
    a, b = pair_a, pair_b
    ready = ProgressionReadiness.READY
    not_ready = ProgressionReadiness.NOT_READY
    insuff = ProgressionReadiness.INSUFFICIENT_EVIDENCE

    if a is ready and b is ready:
        return ready, InsufficientReason.ALL_REQUIRED_MODALITIES_DEMONSTRATED
    if (a is ready and b is insuff) or (a is insuff and b is ready):
        return ready, InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE
    if (a is ready and b is not_ready) or (a is not_ready and b is ready):
        return insuff, InsufficientReason.CONFLICTING_DEMONSTRATIONS
    if a is insuff and b is insuff:
        return insuff, InsufficientReason.INSUFFICIENT_SAMPLE
    # Remaining cells: NOT_READY with INSUFFICIENT, or both NOT_READY.
    return not_ready, InsufficientReason.NEGATIVE_DEMONSTRATION


def _evaluate_mixed_modality(
    *,
    objective_id: str,
    student_id: str,
    contract: ProgressionReadinessContract,
    latest_by_item: dict[str, AssessmentEvidenceRecord],
) -> ProgressionReadinessResult:
    mcq = _modality_outcome(contract, latest_by_item, EvidenceModality.MCQ)
    numeric = _modality_outcome(
        contract, latest_by_item, EvidenceModality.NUMERIC
    )

    if mcq is None or numeric is None:
        return _result(
            objective_id=objective_id,
            student_id=student_id,
            readiness=ProgressionReadiness.INSUFFICIENT_EVIDENCE,
            reason=InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED,
        )

    if mcq and numeric:
        return _result(
            objective_id=objective_id,
            student_id=student_id,
            readiness=ProgressionReadiness.READY,
        )
    if mcq and not numeric:
        return _result(
            objective_id=objective_id,
            student_id=student_id,
            readiness=ProgressionReadiness.NOT_READY,
        )
    if not mcq and numeric:
        return _result(
            objective_id=objective_id,
            student_id=student_id,
            readiness=ProgressionReadiness.INSUFFICIENT_EVIDENCE,
            reason=InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED,
        )
    return _result(
        objective_id=objective_id,
        student_id=student_id,
        readiness=ProgressionReadiness.NOT_READY,
    )


def _evaluate_mixed_modality_dual_demonstration(
    *,
    objective_id: str,
    student_id: str,
    contract: ProgressionReadinessContract,
    latest_by_item: dict[str, AssessmentEvidenceRecord],
) -> ProgressionReadinessResult:
    """Two-stage dual-pair evaluation: per-pair matrix, then 9-cell combine."""
    pairs = contract.demonstration_pairs
    if len(pairs) != 2:
        raise ValueError(
            f"MIXED_MODALITY_DUAL_DEMONSTRATION contract "
            f"{contract.objective_id!r} requires exactly 2 demonstration "
            f"pairs, got {len(pairs)}"
        )

    pair_a_outcome, _ = _pair_four_outcome(
        latest_by_item=latest_by_item, pair=pairs[0]
    )
    pair_b_outcome, _ = _pair_four_outcome(
        latest_by_item=latest_by_item, pair=pairs[1]
    )
    readiness, reason = _combine_dual_demonstration(pair_a_outcome, pair_b_outcome)
    return _result(
        objective_id=objective_id,
        student_id=student_id,
        readiness=readiness,
        reason=reason,
    )


def evaluate(
    objective_id: str,
    student_id: str,
    contract: ProgressionReadinessContract,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> ProgressionReadinessResult:
    """Evaluate Progression Readiness from an authored contract and evidence.

    Args:
        objective_id: Target curriculum objective id (must match contract).
        student_id: Student whose evidence is being evaluated.
        contract: Authored contract for the target objective.
        evidence: Assessment Evidence available for this student (may include
            other objectives; unscored rows are ignored for correctness).

    Returns:
        ProgressionReadinessResult with READY, NOT_READY, or
        INSUFFICIENT_EVIDENCE plus a specific reason code.
    """
    oid = (objective_id or "").strip()
    sid = (student_id or "").strip()
    if contract.objective_id != oid:
        raise ValueError(
            f"contract objective_id {contract.objective_id!r} "
            f"does not match target {oid!r}"
        )

    scored = _scored_only(evidence)

    prereq = contract.required_prerequisite_objective_id
    if prereq and not _prerequisite_verified(scored, prereq):
        return _result(
            objective_id=oid,
            student_id=sid,
            readiness=ProgressionReadiness.INSUFFICIENT_EVIDENCE,
            reason=InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED,
        )

    own = tuple(r for r in scored if r.objective_id == oid)
    latest = _latest_per_item(own, contract.item_ids)

    if _critical_misconception_hit(latest, contract.critical_misconception_tags):
        return _result(
            objective_id=oid,
            student_id=sid,
            readiness=ProgressionReadiness.NOT_READY,
        )

    if contract.kind is ContractKind.CONCEPTUAL:
        return _evaluate_conceptual(
            objective_id=oid,
            student_id=sid,
            contract=contract,
            latest_by_item=latest,
        )
    if contract.kind is ContractKind.MIXED_MODALITY:
        return _evaluate_mixed_modality(
            objective_id=oid,
            student_id=sid,
            contract=contract,
            latest_by_item=latest,
        )
    if contract.kind is ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION:
        return _evaluate_mixed_modality_dual_demonstration(
            objective_id=oid,
            student_id=sid,
            contract=contract,
            latest_by_item=latest,
        )
    return _result(
        objective_id=oid,
        student_id=sid,
        readiness=ProgressionReadiness.INSUFFICIENT_EVIDENCE,
        reason=InsufficientReason.CONFLICTING_EVIDENCE,
    )


def evaluate_from_store(
    objective_id: str,
    student_id: str,
    contract: ProgressionReadinessContract,
    store: ObjectiveAssessmentEvidenceStore,
) -> ProgressionReadinessResult:
    """Evaluate using the real OEA read path (list_for_student only).

    Read-only: never appends or otherwise mutates the store.
    """
    evidence = store.list_for_student(student_id)
    return evaluate(objective_id, student_id, contract, evidence)

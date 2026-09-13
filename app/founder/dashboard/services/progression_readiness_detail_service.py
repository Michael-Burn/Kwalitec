"""Founder Console: Progression Readiness detail for one student.

Read-only projection over authored contracts + OEA evidence. Raw internal
status and reason codes are allowed here. Never mutates evidence or decisions.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
    get_objective_assessment_evidence_store,
)
from app.application.progression_readiness import (
    PROGRESSION_READINESS_CONTRACTS,
    ContractKind,
    ProgressionReadinessContract,
    evaluate,
)


@dataclass(frozen=True)
class ProgressionItemEvidenceView:
    item_id: str
    modality: str
    correctness: str  # correct | incorrect | unobserved | unscored_attempt


@dataclass(frozen=True)
class ProgressionContractDetailView:
    objective_id: str
    kind: str
    readiness: str
    reason_code: str
    requirement_summary: str
    prerequisite_objective_id: str
    prerequisite_verified: bool | None
    critical_misconception_tags: tuple[str, ...]
    critical_misconception_hit: bool
    items: tuple[ProgressionItemEvidenceView, ...]


@dataclass(frozen=True)
class ProgressionReadinessDetailPage:
    page_title: str
    page_support: str
    student_id: int
    student_email: str
    contracts: tuple[ProgressionContractDetailView, ...]


def _latest_scored(
    evidence: Sequence[AssessmentEvidenceRecord],
    item_ids: frozenset[str],
) -> dict[str, AssessmentEvidenceRecord]:
    latest: dict[str, AssessmentEvidenceRecord] = {}
    for record in sorted(
        (r for r in evidence if r.item_id in item_ids and r.scored_correct is not None),
        key=lambda r: (r.occurred_at, r.evidence_id),
    ):
        latest[record.item_id] = record
    return latest


def _any_attempt(
    evidence: Sequence[AssessmentEvidenceRecord],
    item_id: str,
) -> bool:
    return any(r.item_id == item_id for r in evidence)


def _prerequisite_verified(
    evidence: Sequence[AssessmentEvidenceRecord],
    prerequisite_objective_id: str | None,
) -> bool | None:
    if not prerequisite_objective_id:
        return None
    return any(
        r.objective_id == prerequisite_objective_id and r.scored_correct is True
        for r in evidence
    )


def _critical_hit(
    contract: ProgressionReadinessContract,
    latest: dict[str, AssessmentEvidenceRecord],
) -> bool:
    tags = contract.critical_misconception_tags
    if not tags:
        return False
    for record in latest.values():
        if record.scored_correct is False:
            tag = (record.selected_misconception_tag or "").strip()
            if tag and tag in tags:
                return True
    return False


def _requirement_summary(contract: ProgressionReadinessContract) -> str:
    if contract.kind is ContractKind.CONCEPTUAL:
        return (
            f"Conceptual: at least {contract.ready_min_correct} of "
            f"{contract.item_count} contracted items scored correct"
        )
    if contract.kind is ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION:
        pair_bits = []
        for i, pair in enumerate(contract.demonstration_pairs, start=1):
            pair_bits.append(
                f"Pair {i}: {pair.mcq_item_id} (mcq) + "
                f"{pair.numeric_item_id} (numeric)"
            )
        return (
            "Mixed modality dual demonstration: evaluate each pair with the "
            "four-outcome matrix, then combine with the locked 9-cell matrix. "
            + "; ".join(pair_bits)
        )
    parts = [
        f"{spec.item_id} ({spec.modality.value})"
        for spec in contract.evidence_items
    ]
    base = "Mixed modality: require scored observations for " + "; ".join(parts)
    if contract.required_prerequisite_objective_id:
        return (
            f"{base}. Prerequisite: "
            f"{contract.required_prerequisite_objective_id} must have at least "
            "one scored-correct evidence row"
        )
    return base


def _item_views(
    contract: ProgressionReadinessContract,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> tuple[ProgressionItemEvidenceView, ...]:
    latest = _latest_scored(evidence, contract.item_ids)
    rows: list[ProgressionItemEvidenceView] = []
    for spec in contract.evidence_items:
        record = latest.get(spec.item_id)
        if record is not None:
            correctness = "correct" if record.scored_correct else "incorrect"
        elif _any_attempt(evidence, spec.item_id):
            correctness = "unscored_attempt"
        else:
            correctness = "unobserved"
        rows.append(
            ProgressionItemEvidenceView(
                item_id=spec.item_id,
                modality=spec.modality.value,
                correctness=correctness,
            )
        )
    return tuple(rows)


def build_contract_detail(
    contract: ProgressionReadinessContract,
    *,
    student_id: str,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> ProgressionContractDetailView:
    result = evaluate(contract.objective_id, student_id, contract, evidence)
    latest = _latest_scored(evidence, contract.item_ids)
    return ProgressionContractDetailView(
        objective_id=contract.objective_id,
        kind=contract.kind.value,
        readiness=result.readiness.value,
        reason_code=result.reason.value if result.reason is not None else "",
        requirement_summary=_requirement_summary(contract),
        prerequisite_objective_id=(
            contract.required_prerequisite_objective_id or ""
        ),
        prerequisite_verified=_prerequisite_verified(
            evidence, contract.required_prerequisite_objective_id
        ),
        critical_misconception_tags=tuple(
            sorted(contract.critical_misconception_tags)
        ),
        critical_misconception_hit=_critical_hit(contract, latest),
        items=_item_views(contract, evidence),
    )


class ProgressionReadinessDetailService:
    """Build the founder richer view for all authored contracts."""

    def __init__(
        self,
        *,
        store: ObjectiveAssessmentEvidenceStore | None = None,
    ) -> None:
        self._store = store

    def build(
        self,
        *,
        user_id: int,
        student_email: str,
    ) -> ProgressionReadinessDetailPage:
        sid = str(user_id)
        store = self._store or get_objective_assessment_evidence_store()
        evidence = store.list_for_student(sid)
        n = len(PROGRESSION_READINESS_CONTRACTS)
        contracts = tuple(
            build_contract_detail(contract, student_id=sid, evidence=evidence)
            for contract in PROGRESSION_READINESS_CONTRACTS.values()
        )
        return ProgressionReadinessDetailPage(
            page_title="Progression Readiness",
            page_support=(
                f"Complete internal evaluation for the {n} authored contracts. "
                "Informational only: does not change what the student can do."
            ),
            student_id=user_id,
            student_email=student_email,
            contracts=contracts,
        )

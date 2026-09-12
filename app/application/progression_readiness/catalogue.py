"""Six real Progression Readiness contracts for fully evidenced CS1 objectives.

Item ids match the live OEA tagged freeze (topic 1.1 and topic 2.3).
Critical misconception tags are empty today; the override path remains present.
"""

from __future__ import annotations

from app.application.progression_readiness.contracts import (
    ContractKind,
    EvidenceItemSpec,
    EvidenceModality,
    ProgressionReadinessContract,
)

# Prerequisite for CS1-B-T03-LO01 (joint-distribution / 2.2.1). Real syllabus
# id; no OEA-tagged items yet. Check is genuine, not hard-coded to fail.
PREREQUISITE_JOINT_DISTRIBUTION_LO = "CS1-B-T02-LO01"

CS1_A_T01_LO01 = ProgressionReadinessContract(
    objective_id="CS1-A-T01-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1017-1.1.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.1.1-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("ep001-1.1-ar-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_A_T01_LO02 = ProgressionReadinessContract(
    objective_id="CS1-A-T01-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1017-1.1.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.1.2-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("ep001-1.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_A_T01_LO03 = ProgressionReadinessContract(
    objective_id="CS1-A-T01-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1017-1.1.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.1.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_A_T01_LO04 = ProgressionReadinessContract(
    objective_id="CS1-A-T01-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1017-1.1.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.1.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T03_LO01 = ProgressionReadinessContract(
    objective_id="CS1-B-T03-LO01",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1006-2.3.1-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1006-2.3.1-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
    required_prerequisite_objective_id=PREREQUISITE_JOINT_DISTRIBUTION_LO,
)

CS1_B_T03_LO02 = ProgressionReadinessContract(
    objective_id="CS1-B-T03-LO02",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1006-2.3.2-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1006-2.3.2-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

PROGRESSION_READINESS_CONTRACTS: dict[str, ProgressionReadinessContract] = {
    CS1_A_T01_LO01.objective_id: CS1_A_T01_LO01,
    CS1_A_T01_LO02.objective_id: CS1_A_T01_LO02,
    CS1_A_T01_LO03.objective_id: CS1_A_T01_LO03,
    CS1_A_T01_LO04.objective_id: CS1_A_T01_LO04,
    CS1_B_T03_LO01.objective_id: CS1_B_T03_LO01,
    CS1_B_T03_LO02.objective_id: CS1_B_T03_LO02,
}


def get_contract(objective_id: str) -> ProgressionReadinessContract | None:
    """Return the authored contract for ``objective_id``, or None."""
    return PROGRESSION_READINESS_CONTRACTS.get((objective_id or "").strip())

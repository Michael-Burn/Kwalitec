"""Real Progression Readiness contracts for evidenced CS1 objectives.

Item ids match the live OEA tagged freeze (topics 1.1, 1.2, 2.1, and 2.3).
Critical misconception tags are empty today; the override path remains present.
"""

from __future__ import annotations

from app.application.progression_readiness.contracts import (
    ContractKind,
    DemonstrationPair,
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

CS1_A_T02_LO01 = ProgressionReadinessContract(
    objective_id="CS1-A-T02-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("ep001-1.2a-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("ep001-1.2a-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.2.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.2.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=3,
    critical_misconception_tags=frozenset(),
)

CS1_A_T02_LO02 = ProgressionReadinessContract(
    objective_id="CS1-A-T02-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("ep001-1.2b-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("ep001-1.2b-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.2.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.2.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=3,
    critical_misconception_tags=frozenset(),
)

CS1_A_T02_LO03 = ProgressionReadinessContract(
    objective_id="CS1-A-T02-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1002-1.2c-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1002-1.2c-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.2.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-1.2.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=3,
    critical_misconception_tags=frozenset(),
)

CS1_B_T01_LO01 = ProgressionReadinessContract(
    objective_id="CS1-B-T01-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1002-2.1a-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1002-2.1a-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-2.1.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-2.1.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=3,
    critical_misconception_tags=frozenset(),
)

CS1_B_T01_LO02 = ProgressionReadinessContract(
    objective_id="CS1-B-T01-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1002-2.1b-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1002-2.1b-cp-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-2.1.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1017-2.1.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=3,
    critical_misconception_tags=frozenset(),
)

CS1_B_T01_LO03 = ProgressionReadinessContract(
    objective_id="CS1-B-T01-LO03",
    kind=ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION,
    evidence_items=(
        EvidenceItemSpec("cs1004-2.1c-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1004-2.1c-cp-01", EvidenceModality.NUMERIC),
        EvidenceItemSpec("cs1016-2.1.3-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1016-2.1.3-cp-01", EvidenceModality.NUMERIC),
    ),
    demonstration_pairs=(
        DemonstrationPair(
            mcq_item_id="cs1004-2.1c-ar-01",
            numeric_item_id="cs1004-2.1c-cp-01",
        ),
        DemonstrationPair(
            mcq_item_id="cs1016-2.1.3-ar-01",
            numeric_item_id="cs1016-2.1.3-cp-01",
        ),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_B_T01_LO04 = ProgressionReadinessContract(
    objective_id="CS1-B-T01-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1004-2.1d-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1004-2.1d-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T01_LO05 = ProgressionReadinessContract(
    objective_id="CS1-B-T01-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1004-2.1e-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1004-2.1e-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T01_LO06 = ProgressionReadinessContract(
    objective_id="CS1-B-T01-LO06",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1004-2.1f-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1004-2.1f-cp-01", EvidenceModality.CONCEPTUAL),
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
    CS1_A_T02_LO01.objective_id: CS1_A_T02_LO01,
    CS1_A_T02_LO02.objective_id: CS1_A_T02_LO02,
    CS1_A_T02_LO03.objective_id: CS1_A_T02_LO03,
    CS1_B_T01_LO01.objective_id: CS1_B_T01_LO01,
    CS1_B_T01_LO02.objective_id: CS1_B_T01_LO02,
    CS1_B_T01_LO03.objective_id: CS1_B_T01_LO03,
    CS1_B_T01_LO04.objective_id: CS1_B_T01_LO04,
    CS1_B_T01_LO05.objective_id: CS1_B_T01_LO05,
    CS1_B_T01_LO06.objective_id: CS1_B_T01_LO06,
    CS1_B_T03_LO01.objective_id: CS1_B_T03_LO01,
    CS1_B_T03_LO02.objective_id: CS1_B_T03_LO02,
}


def get_contract(objective_id: str) -> ProgressionReadinessContract | None:
    """Return the authored contract for ``objective_id``, or None."""
    return PROGRESSION_READINESS_CONTRACTS.get((objective_id or "").strip())

"""Real Progression Readiness contracts for evidenced CS1 objectives.

Item ids match the live OEA tagged freeze (topics 1.1, 1.2, 2.1, 2.2, 2.3,
2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 4.1, and 4.2). Critical misconception tags are
empty today; the override path remains present.
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
# id with OEA-tagged topic 2.2 items. Check is genuine, not hard-coded to fail.
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
        EvidenceItemSpec("cs1017-1.1.3-ar-02", EvidenceModality.CONCEPTUAL),
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
        EvidenceItemSpec("cs1017-1.1.4-ar-02", EvidenceModality.CONCEPTUAL),
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

# Topic 2.2: cs1016-2.2.1-* are OEA-tagged for CS1-B-T02-LO01 but are not
# listed here, so this contract's evaluation never consumes them.
CS1_B_T02_LO01 = ProgressionReadinessContract(
    objective_id="CS1-B-T02-LO01",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1005-2.2.1-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1005-2.2.1-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_B_T02_LO02 = ProgressionReadinessContract(
    objective_id="CS1-B-T02-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1005-2.2.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1005-2.2.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T02_LO03 = ProgressionReadinessContract(
    objective_id="CS1-B-T02-LO03",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1005-2.2.3-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1005-2.2.3-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_B_T02_LO04 = ProgressionReadinessContract(
    objective_id="CS1-B-T02-LO04",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1005-2.2.4-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1005-2.2.4-cp-01", EvidenceModality.NUMERIC),
    ),
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

CS1_B_T04_LO01 = ProgressionReadinessContract(
    objective_id="CS1-B-T04-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1007-2.4.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1007-2.4.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T04_LO02 = ProgressionReadinessContract(
    objective_id="CS1-B-T04-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1007-2.4.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1007-2.4.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

# Topic 2.5: cs1016-2.5.1-* are OEA-tagged for CS1-B-T05-LO01 but are not
# listed here, so this contract's evaluation never consumes them.
CS1_B_T05_LO01 = ProgressionReadinessContract(
    objective_id="CS1-B-T05-LO01",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1008-2.5.1-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1008-2.5.1-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_B_T05_LO02 = ProgressionReadinessContract(
    objective_id="CS1-B-T05-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1008-2.5.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1008-2.5.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

# Topic 2.6: cs1016-2.6.1-* are OEA-tagged for CS1-B-T06-LO01 but are not
# listed here, so this contract's evaluation never consumes them.
CS1_B_T06_LO01 = ProgressionReadinessContract(
    objective_id="CS1-B-T06-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1009-2.6.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1009-2.6.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T06_LO02 = ProgressionReadinessContract(
    objective_id="CS1-B-T06-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1009-2.6.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1009-2.6.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T06_LO03 = ProgressionReadinessContract(
    objective_id="CS1-B-T06-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1009-2.6.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1009-2.6.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T06_LO04 = ProgressionReadinessContract(
    objective_id="CS1-B-T06-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1009-2.6.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1009-2.6.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T06_LO05 = ProgressionReadinessContract(
    objective_id="CS1-B-T06-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1009-2.6.5-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1009-2.6.5-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_B_T06_LO06 = ProgressionReadinessContract(
    objective_id="CS1-B-T06-LO06",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1009-2.6.6-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1009-2.6.6-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

# Topic 3.1: cs1016-3.1.1-* are OEA-tagged for CS1-C-T01-LO01 but are not
# listed here, so this contract's evaluation never consumes them.
CS1_C_T01_LO01 = ProgressionReadinessContract(
    objective_id="CS1-C-T01-LO01",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1010-3.1.1-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1010-3.1.1-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_C_T01_LO02 = ProgressionReadinessContract(
    objective_id="CS1-C-T01-LO02",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1010-3.1.2-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1010-3.1.2-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_C_T01_LO03 = ProgressionReadinessContract(
    objective_id="CS1-C-T01-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1010-3.1.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1010-3.1.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T01_LO04 = ProgressionReadinessContract(
    objective_id="CS1-C-T01-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1010-3.1.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1010-3.1.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T01_LO05 = ProgressionReadinessContract(
    objective_id="CS1-C-T01-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1010-3.1.5-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1010-3.1.5-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T01_LO06 = ProgressionReadinessContract(
    objective_id="CS1-C-T01-LO06",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1010-3.1.6-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1010-3.1.6-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

# Topic 3.2: cs1016-3.2.1-* are OEA-tagged for CS1-C-T02-LO01 but are not
# listed here, so this contract's evaluation never consumes them.
CS1_C_T02_LO01 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO02 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO03 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO04 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO05 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.5-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.5-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO06 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO06",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.6-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.6-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO07 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO07",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.7-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.7-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T02_LO08 = ProgressionReadinessContract(
    objective_id="CS1-C-T02-LO08",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1011-3.2.8-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1011-3.2.8-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

# Topic 3.3: cs1016-3.3.1-* are OEA-tagged for CS1-C-T03-LO01 but are not
# listed here, so this contract's evaluation never consumes them.
CS1_C_T03_LO01 = ProgressionReadinessContract(
    objective_id="CS1-C-T03-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1012-3.3.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1012-3.3.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T03_LO02 = ProgressionReadinessContract(
    objective_id="CS1-C-T03-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1012-3.3.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1012-3.3.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T03_LO03 = ProgressionReadinessContract(
    objective_id="CS1-C-T03-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1012-3.3.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1012-3.3.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T03_LO04 = ProgressionReadinessContract(
    objective_id="CS1-C-T03-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1012-3.3.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1012-3.3.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_C_T03_LO05 = ProgressionReadinessContract(
    objective_id="CS1-C-T03-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1012-3.3.5-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1012-3.3.5-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

# Topic 4.1: Continuity (cs1013) and Memory (cs1016, LO01 only) twins are
# OEA-tagged for the matching CS1-D-T01 LO but are not listed here, so each
# contract's evaluation never consumes them.
CS1_D_T01_LO01 = ProgressionReadinessContract(
    objective_id="CS1-D-T01-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.1.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.1.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T01_LO02 = ProgressionReadinessContract(
    objective_id="CS1-D-T01-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.1.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.1.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T01_LO03 = ProgressionReadinessContract(
    objective_id="CS1-D-T01-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.1.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.1.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T01_LO04 = ProgressionReadinessContract(
    objective_id="CS1-D-T01-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.1.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.1.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T01_LO05 = ProgressionReadinessContract(
    objective_id="CS1-D-T01-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.1.5-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.1.5-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

# Topic 4.2: Continuity (cs1014) twins are OEA-tagged for the matching
# CS1-D-T02 LO but are omitted from conceptual contracts and from LO08
# (byte-identical AR disqualifies the twin pair from dual-pair treatment),
# so those evaluations never consume them. LO05 and LO10 include both
# independent mixed-modality pairs via demonstration_pairs.
CS1_D_T02_LO01 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO01",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.1-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.1-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO02 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO03 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO04 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO04",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.4-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.4-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO05 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO05",
    kind=ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.5-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-4.2.5-cp-01", EvidenceModality.NUMERIC),
        EvidenceItemSpec("cs1014-4.2.5-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1014-4.2.5-cp-01", EvidenceModality.NUMERIC),
    ),
    demonstration_pairs=(
        DemonstrationPair(
            mcq_item_id="cs1003-4.2.5-ar-01",
            numeric_item_id="cs1003-4.2.5-cp-01",
        ),
        DemonstrationPair(
            mcq_item_id="cs1014-4.2.5-ar-01",
            numeric_item_id="cs1014-4.2.5-cp-01",
        ),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO06 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO06",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.6-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.6-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO07 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO07",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.7-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.7-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO08 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO08",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.8-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-4.2.8-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO09 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO09",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.9-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-4.2.9-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_D_T02_LO10 = ProgressionReadinessContract(
    objective_id="CS1-D-T02-LO10",
    kind=ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION,
    evidence_items=(
        EvidenceItemSpec("cs1003-4.2.10-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-4.2.10-cp-01", EvidenceModality.NUMERIC),
        EvidenceItemSpec("cs1014-4.2.10-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1014-4.2.10-cp-01", EvidenceModality.NUMERIC),
    ),
    demonstration_pairs=(
        DemonstrationPair(
            mcq_item_id="cs1003-4.2.10-ar-01",
            numeric_item_id="cs1003-4.2.10-cp-01",
        ),
        DemonstrationPair(
            mcq_item_id="cs1014-4.2.10-ar-01",
            numeric_item_id="cs1014-4.2.10-cp-01",
        ),
    ),
    critical_misconception_tags=frozenset(),
)

# Topic 5.1: Continuity (cs1015) twins are OEA-tagged for the matching
# CS1-E-T01 LO but are omitted from conceptual contracts and from single-
# pair mixed contracts (LO04/LO06/LO08), so those evaluations never consume
# them. LO07 includes both independent mixed-modality pairs via
# demonstration_pairs. LO01 uses the approved cross-package pairing
# (cs1003 conceptual/MCQ + cs1016 numeric); other LO01 items remain
# OEA-only.
CS1_E_T01_LO01 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO01",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.1-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1016-5.1.1-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO02 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO02",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.2-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-5.1.2-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO03 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO03",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.3-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-5.1.3-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO04 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO04",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.4-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-5.1.4-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO05 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO05",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.5-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-5.1.5-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO06 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO06",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.6-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-5.1.6-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO07 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO07",
    kind=ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.7-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-5.1.7-cp-01", EvidenceModality.NUMERIC),
        EvidenceItemSpec("cs1015-5.1.7-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1015-5.1.7-cp-01", EvidenceModality.NUMERIC),
    ),
    demonstration_pairs=(
        DemonstrationPair(
            mcq_item_id="cs1003-5.1.7-ar-01",
            numeric_item_id="cs1003-5.1.7-cp-01",
        ),
        DemonstrationPair(
            mcq_item_id="cs1015-5.1.7-ar-01",
            numeric_item_id="cs1015-5.1.7-cp-01",
        ),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO08 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO08",
    kind=ContractKind.MIXED_MODALITY,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.8-ar-01", EvidenceModality.MCQ),
        EvidenceItemSpec("cs1003-5.1.8-cp-01", EvidenceModality.NUMERIC),
    ),
    critical_misconception_tags=frozenset(),
)

CS1_E_T01_LO09 = ProgressionReadinessContract(
    objective_id="CS1-E-T01-LO09",
    kind=ContractKind.CONCEPTUAL,
    evidence_items=(
        EvidenceItemSpec("cs1003-5.1.9-ar-01", EvidenceModality.CONCEPTUAL),
        EvidenceItemSpec("cs1003-5.1.9-cp-01", EvidenceModality.CONCEPTUAL),
    ),
    ready_min_correct=2,
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
    CS1_B_T02_LO01.objective_id: CS1_B_T02_LO01,
    CS1_B_T02_LO02.objective_id: CS1_B_T02_LO02,
    CS1_B_T02_LO03.objective_id: CS1_B_T02_LO03,
    CS1_B_T02_LO04.objective_id: CS1_B_T02_LO04,
    CS1_B_T03_LO01.objective_id: CS1_B_T03_LO01,
    CS1_B_T03_LO02.objective_id: CS1_B_T03_LO02,
    CS1_B_T04_LO01.objective_id: CS1_B_T04_LO01,
    CS1_B_T04_LO02.objective_id: CS1_B_T04_LO02,
    CS1_B_T05_LO01.objective_id: CS1_B_T05_LO01,
    CS1_B_T05_LO02.objective_id: CS1_B_T05_LO02,
    CS1_B_T06_LO01.objective_id: CS1_B_T06_LO01,
    CS1_B_T06_LO02.objective_id: CS1_B_T06_LO02,
    CS1_B_T06_LO03.objective_id: CS1_B_T06_LO03,
    CS1_B_T06_LO04.objective_id: CS1_B_T06_LO04,
    CS1_B_T06_LO05.objective_id: CS1_B_T06_LO05,
    CS1_B_T06_LO06.objective_id: CS1_B_T06_LO06,
    CS1_C_T01_LO01.objective_id: CS1_C_T01_LO01,
    CS1_C_T01_LO02.objective_id: CS1_C_T01_LO02,
    CS1_C_T01_LO03.objective_id: CS1_C_T01_LO03,
    CS1_C_T01_LO04.objective_id: CS1_C_T01_LO04,
    CS1_C_T01_LO05.objective_id: CS1_C_T01_LO05,
    CS1_C_T01_LO06.objective_id: CS1_C_T01_LO06,
    CS1_C_T02_LO01.objective_id: CS1_C_T02_LO01,
    CS1_C_T02_LO02.objective_id: CS1_C_T02_LO02,
    CS1_C_T02_LO03.objective_id: CS1_C_T02_LO03,
    CS1_C_T02_LO04.objective_id: CS1_C_T02_LO04,
    CS1_C_T02_LO05.objective_id: CS1_C_T02_LO05,
    CS1_C_T02_LO06.objective_id: CS1_C_T02_LO06,
    CS1_C_T02_LO07.objective_id: CS1_C_T02_LO07,
    CS1_C_T02_LO08.objective_id: CS1_C_T02_LO08,
    CS1_C_T03_LO01.objective_id: CS1_C_T03_LO01,
    CS1_C_T03_LO02.objective_id: CS1_C_T03_LO02,
    CS1_C_T03_LO03.objective_id: CS1_C_T03_LO03,
    CS1_C_T03_LO04.objective_id: CS1_C_T03_LO04,
    CS1_C_T03_LO05.objective_id: CS1_C_T03_LO05,
    CS1_D_T01_LO01.objective_id: CS1_D_T01_LO01,
    CS1_D_T01_LO02.objective_id: CS1_D_T01_LO02,
    CS1_D_T01_LO03.objective_id: CS1_D_T01_LO03,
    CS1_D_T01_LO04.objective_id: CS1_D_T01_LO04,
    CS1_D_T01_LO05.objective_id: CS1_D_T01_LO05,
    CS1_D_T02_LO01.objective_id: CS1_D_T02_LO01,
    CS1_D_T02_LO02.objective_id: CS1_D_T02_LO02,
    CS1_D_T02_LO03.objective_id: CS1_D_T02_LO03,
    CS1_D_T02_LO04.objective_id: CS1_D_T02_LO04,
    CS1_D_T02_LO05.objective_id: CS1_D_T02_LO05,
    CS1_D_T02_LO06.objective_id: CS1_D_T02_LO06,
    CS1_D_T02_LO07.objective_id: CS1_D_T02_LO07,
    CS1_D_T02_LO08.objective_id: CS1_D_T02_LO08,
    CS1_D_T02_LO09.objective_id: CS1_D_T02_LO09,
    CS1_D_T02_LO10.objective_id: CS1_D_T02_LO10,
    CS1_E_T01_LO01.objective_id: CS1_E_T01_LO01,
    CS1_E_T01_LO02.objective_id: CS1_E_T01_LO02,
    CS1_E_T01_LO03.objective_id: CS1_E_T01_LO03,
    CS1_E_T01_LO04.objective_id: CS1_E_T01_LO04,
    CS1_E_T01_LO05.objective_id: CS1_E_T01_LO05,
    CS1_E_T01_LO06.objective_id: CS1_E_T01_LO06,
    CS1_E_T01_LO07.objective_id: CS1_E_T01_LO07,
    CS1_E_T01_LO08.objective_id: CS1_E_T01_LO08,
    CS1_E_T01_LO09.objective_id: CS1_E_T01_LO09,
}


def get_contract(objective_id: str) -> ProgressionReadinessContract | None:
    """Return the authored contract for ``objective_id``, or None."""
    return PROGRESSION_READINESS_CONTRACTS.get((objective_id or "").strip())

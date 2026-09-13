"""Progression Readiness evaluator (OEA read consumer).

Does not write evidence. Does not claim permanent mastery. Does not notify
Twin, Spacing, Policy V1, or Decision Engine. Informational Study / founder
presentation may read evaluate_from_store; decision paths must not.
"""

from app.application.progression_readiness.catalogue import (
    CS1_A_T01_LO01,
    CS1_A_T01_LO02,
    CS1_A_T01_LO03,
    CS1_A_T01_LO04,
    CS1_A_T02_LO01,
    CS1_A_T02_LO02,
    CS1_A_T02_LO03,
    CS1_B_T01_LO01,
    CS1_B_T01_LO02,
    CS1_B_T01_LO03,
    CS1_B_T01_LO04,
    CS1_B_T01_LO05,
    CS1_B_T01_LO06,
    CS1_B_T03_LO01,
    CS1_B_T03_LO02,
    PREREQUISITE_JOINT_DISTRIBUTION_LO,
    PROGRESSION_READINESS_CONTRACTS,
    get_contract,
)
from app.application.progression_readiness.contracts import (
    ContractKind,
    DemonstrationPair,
    EvidenceItemSpec,
    EvidenceModality,
    ProgressionReadinessContract,
)
from app.application.progression_readiness.evaluator import (
    evaluate,
    evaluate_from_store,
)
from app.application.progression_readiness.results import (
    InsufficientReason,
    ProgressionReadiness,
    ProgressionReadinessResult,
)

__all__ = (
    "CS1_A_T01_LO01",
    "CS1_A_T01_LO02",
    "CS1_A_T01_LO03",
    "CS1_A_T01_LO04",
    "CS1_A_T02_LO01",
    "CS1_A_T02_LO02",
    "CS1_A_T02_LO03",
    "CS1_B_T01_LO01",
    "CS1_B_T01_LO02",
    "CS1_B_T01_LO03",
    "CS1_B_T01_LO04",
    "CS1_B_T01_LO05",
    "CS1_B_T01_LO06",
    "CS1_B_T03_LO01",
    "CS1_B_T03_LO02",
    "ContractKind",
    "DemonstrationPair",
    "EvidenceItemSpec",
    "EvidenceModality",
    "InsufficientReason",
    "PREREQUISITE_JOINT_DISTRIBUTION_LO",
    "PROGRESSION_READINESS_CONTRACTS",
    "ProgressionReadiness",
    "ProgressionReadinessContract",
    "ProgressionReadinessResult",
    "evaluate",
    "evaluate_from_store",
    "get_contract",
)

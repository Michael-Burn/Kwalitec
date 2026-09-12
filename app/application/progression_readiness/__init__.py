"""Progression Readiness evaluator (standalone; unwired from live product).

Reads Assessment Evidence via OEA. Does not write evidence. Does not claim
permanent mastery. Does not notify Twin, Spacing, Policy V1, or Decision Engine.
"""

from app.application.progression_readiness.catalogue import (
    CS1_A_T01_LO01,
    CS1_A_T01_LO02,
    CS1_A_T01_LO03,
    CS1_A_T01_LO04,
    CS1_B_T03_LO01,
    CS1_B_T03_LO02,
    PREREQUISITE_JOINT_DISTRIBUTION_LO,
    PROGRESSION_READINESS_CONTRACTS,
    get_contract,
)
from app.application.progression_readiness.contracts import (
    ContractKind,
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
    "CS1_B_T03_LO01",
    "CS1_B_T03_LO02",
    "ContractKind",
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

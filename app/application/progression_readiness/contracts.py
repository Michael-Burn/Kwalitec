"""Authored Progression Readiness contracts (readable data, not nested logic).

An author should be able to read a contract and understand which items provide
evidence, which misconceptions are critical, which modalities are required,
and whether a prerequisite objective must show scored-correct evidence first.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceModality(str, Enum):
    """Capability / response modality an evidence item contributes."""

    CONCEPTUAL = "conceptual"
    MCQ = "mcq"
    NUMERIC = "numeric"


class ContractKind(str, Enum):
    """Which evaluation rule family this contract uses."""

    CONCEPTUAL = "conceptual"
    MIXED_MODALITY = "mixed_modality"


@dataclass(frozen=True)
class EvidenceItemSpec:
    """One authored evidence item that contributes to the contract."""

    item_id: str
    modality: EvidenceModality


@dataclass(frozen=True)
class ProgressionReadinessContract:
    """Per-objective authored readiness contract.

    Attributes:
        objective_id: Curriculum learning-objective id this contract governs.
        kind: Conceptual n-item rules, or mixed-modality MCQ+numeric rules.
        evidence_items: Ordered list of items that provide evidence.
        ready_min_correct: For conceptual contracts, minimum correct items for
            READY (e.g. 2 of 3). Ignored for mixed_modality.
        critical_misconception_tags: Tags that force NOT_READY if selected on
            a scored-incorrect attempt. Empty when none are flagged.
        required_prerequisite_objective_id: If set, at least one scored-correct
            evidence row for that objective must exist before own evidence is
            interpreted as READY.
    """

    objective_id: str
    kind: ContractKind
    evidence_items: tuple[EvidenceItemSpec, ...]
    ready_min_correct: int = 0
    critical_misconception_tags: frozenset[str] = frozenset()
    required_prerequisite_objective_id: str | None = None

    @property
    def item_ids(self) -> frozenset[str]:
        return frozenset(spec.item_id for spec in self.evidence_items)

    @property
    def item_count(self) -> int:
        return len(self.evidence_items)

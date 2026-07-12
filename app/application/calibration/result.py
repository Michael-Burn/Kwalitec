"""Calibration birth result — Twin priors + mandatory provenance metadata.

Application output of StudentCalibrationBuilder. Priors live in birth
metadata so Knowledge ``mastery_belief`` and Performance assessment warrant
remain intentionally empty (Capability 3.6.5 unknown preservation).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.application.calibration.contract import (
    CONTRACT_VERSION_1_0,
    SOURCE_SELF_DECLARED,
    WARRANT_THIN,
    BeginnerOrHistoryPosture,
    DeclaredPosture,
    StudyObjective,
)
from app.domain.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class PriorProvenance:
    """Mandatory self-declared provenance cargo for one history prior."""

    source: str
    warrant: str
    contract_version: str
    contract_field: str
    non_evidence: bool = True

    @classmethod
    def self_declared(
        cls,
        *,
        contract_field: str,
        contract_version: str = CONTRACT_VERSION_1_0,
    ) -> PriorProvenance:
        """Attach Version 1.0 self_declared / thin provenance."""
        return cls(
            source=SOURCE_SELF_DECLARED,
            warrant=WARRANT_THIN,
            contract_version=contract_version,
            contract_field=contract_field,
            non_evidence=True,
        )


@dataclass(frozen=True)
class KnowledgePriorMarker:
    """Structural Knowledge exposure / coverage prior — never mastery."""

    kind: str
    scope_id: str | None
    section_ids: tuple[str, ...]
    provenance: PriorProvenance
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        *,
        kind: str,
        provenance: PriorProvenance,
        scope_id: str | None = None,
        section_ids: tuple[str, ...] = (),
        payload: dict[str, Any] | None = None,
    ) -> KnowledgePriorMarker:
        """Construct an immutable Knowledge prior marker."""
        return cls(
            kind=kind,
            scope_id=scope_id,
            section_ids=tuple(section_ids),
            provenance=provenance,
            payload=dict(payload or {}),
        )


@dataclass(frozen=True)
class PerformancePriorMarker:
    """Structural attempt-history prior — never marks or pass probability."""

    kind: str
    provenance: PriorProvenance
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        *,
        kind: str,
        provenance: PriorProvenance,
        payload: dict[str, Any] | None = None,
    ) -> PerformancePriorMarker:
        """Construct an immutable Performance prior marker."""
        return cls(
            kind=kind,
            provenance=provenance,
            payload=dict(payload or {}),
        )


@dataclass(frozen=True)
class CalibrationBirthMetadata:
    """Calibration lineage carried with the birth Twin (not a belief domain)."""

    contract_version: str
    declaration_confirmation: bool
    declared_posture: DeclaredPosture
    beginner_or_history_posture: BeginnerOrHistoryPosture
    study_objective: StudyObjective
    warrant_posture: str
    source: str
    emitted_at: datetime | None
    sitting_label: str | None
    knowledge_priors: tuple[KnowledgePriorMarker, ...]
    performance_priors: tuple[PerformancePriorMarker, ...]

    @classmethod
    def create(
        cls,
        *,
        contract_version: str,
        declaration_confirmation: bool,
        declared_posture: DeclaredPosture,
        beginner_or_history_posture: BeginnerOrHistoryPosture,
        study_objective: StudyObjective,
        emitted_at: datetime | None,
        sitting_label: str | None,
        knowledge_priors: tuple[KnowledgePriorMarker, ...] | list[KnowledgePriorMarker],
        performance_priors: (
            tuple[PerformancePriorMarker, ...] | list[PerformancePriorMarker]
        ),
        warrant_posture: str = WARRANT_THIN,
        source: str = SOURCE_SELF_DECLARED,
    ) -> CalibrationBirthMetadata:
        """Construct immutable birth metadata."""
        return cls(
            contract_version=contract_version,
            declaration_confirmation=declaration_confirmation,
            declared_posture=declared_posture,
            beginner_or_history_posture=beginner_or_history_posture,
            study_objective=study_objective,
            warrant_posture=warrant_posture,
            source=source,
            emitted_at=emitted_at,
            sitting_label=sitting_label,
            knowledge_priors=tuple(knowledge_priors),
            performance_priors=tuple(performance_priors),
        )


@dataclass(frozen=True)
class CalibrationResult:
    """Calibrated birth Twin plus Calibration metadata / prior markers.

    The Twin holds Identity / Goals anchors and intentionally empty belief
    domains (Memory, Behaviour, Predictions, mastery, assessment warrant).
    History priors live in ``metadata`` under self_declared provenance so
    they cannot be mistaken for Evidence-backed beliefs.
    """

    twin: DigitalTwin
    metadata: CalibrationBirthMetadata

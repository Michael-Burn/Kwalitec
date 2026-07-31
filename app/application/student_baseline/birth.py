"""Baseline Twin birth — reuses Builder + TwinRepository with Baseline cargo.

Does not redesign StudentCalibrationBuilder. Adds self-declared Baseline
provenance (confidence, objective tokens) into Persistence cargo only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.application.calibration.birth_persistence import PersistedCalibrationBirth
from app.application.calibration.contract import (
    SOURCE_SELF_DECLARED,
    StudentCalibrationContract,
)
from app.application.calibration.student_calibration_builder import (
    StudentCalibrationBuilder,
)
from app.application.student_baseline.declarations import BaselineDeclarations
from app.application.student_baseline.mapper import baseline_provenance_cargo
from app.application.twin_repository.shared import get_shared_twin_repository
from app.application.twin_repository.twin_repository import TwinRepository
from app.application.twin_repository.types import (
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinScope,
)


class BaselineTwinBirth:
    """Compose Contract → Builder → TwinRepository with Baseline provenance."""

    def __init__(
        self,
        *,
        builder: StudentCalibrationBuilder | None = None,
        repository: TwinRepository | None = None,
    ) -> None:
        self._builder = builder or StudentCalibrationBuilder()
        self._repository = repository or get_shared_twin_repository()

    def persist(
        self,
        contract: StudentCalibrationContract,
        declarations: BaselineDeclarations,
        *,
        scope: TwinScope,
        snapshot_id: str | None = None,
        persisted_at: datetime | None = None,
    ) -> PersistedCalibrationBirth | TwinPersistenceFailure:
        """Birth Twin from Contract; attach Baseline self-declared cargo."""
        calibration = self._builder.build(contract)
        provenance = _provenance_from_metadata(calibration.metadata)
        provenance.update(baseline_provenance_cargo(declarations))

        acknowledgement = self._repository.persist_birth_twin(
            calibration.twin,
            scope=scope,
            snapshot_id=snapshot_id,
            provenance=provenance,
            persisted_at=persisted_at,
        )
        if isinstance(acknowledgement, TwinPersistenceFailure):
            return acknowledgement

        return PersistedCalibrationBirth(
            twin=calibration.twin,
            metadata=calibration.metadata,
            acknowledgement=acknowledgement,
            calibration=calibration,
        )


def _provenance_from_metadata(metadata: Any) -> dict[str, Any]:
    return {
        "source": getattr(metadata, "source", None) or SOURCE_SELF_DECLARED,
        "authorship": TwinAuthorship.BIRTH.value,
        "contract_version": metadata.contract_version,
        "warrant_posture": metadata.warrant_posture,
        "declared_posture": metadata.declared_posture.value,
        "study_objective": metadata.study_objective.value,
        "beginner_or_history_posture": (
            metadata.beginner_or_history_posture.value
        ),
    }

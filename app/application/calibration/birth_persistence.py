"""Calibration Birth → TwinRepository persistence composition.

Composes StudentCalibrationBuilder with TwinRepository.persist_birth_twin so a
Birth Twin is authored and immediately stored as the first immutable snapshot.

Owns wiring only: Contract → build → persist → immutable persisted result.
Never redesigns Builder or Repository. Never reasons educationally. Never
invokes Readiness / Decision / Recommendation / Mission / Orchestrator /
or retrieval adapters. Never imports Flask / ORM / SQL.

See Capabilities 3.6.1–3.6.5, 3.7.1–3.7.3, and APPLICATION_LAYER_ARCHITECTURE.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.application.calibration.contract import (
    SOURCE_SELF_DECLARED,
    StudentCalibrationContract,
)
from app.application.calibration.result import (
    CalibrationBirthMetadata,
    CalibrationResult,
)
from app.application.calibration.student_calibration_builder import (
    StudentCalibrationBuilder,
)
from app.application.twin_repository.twin_repository import TwinRepository
from app.application.twin_repository.types import (
    PersistAcknowledgement,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinScope,
)
from app.domain.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class PersistedCalibrationBirth:
    """Immutable Birth Twin after successful TwinRepository persist.

    Carries the Builder output (Twin + Calibration metadata) and the
    Persistence acknowledgement. Educational meaning remains Builder-authored;
    Persistence only confirms durable current designation.
    """

    twin: DigitalTwin
    metadata: CalibrationBirthMetadata
    acknowledgement: PersistAcknowledgement
    calibration: CalibrationResult

    @property
    def snapshot_id(self) -> str:
        """Durable snapshot identity assigned at persist."""
        return self.acknowledgement.snapshot_id

    @property
    def scope(self) -> TwinScope:
        """Authorised persistence scope for the Birth Twin."""
        return self.acknowledgement.scope


class CalibrationBirthPersister:
    """Application composer: Calibration Contract → Birth Twin → Persist.

    Builder creates. Repository stores. This class only sequences those steps
    and returns the immutable persisted result (or Persistence honesty failure).
    """

    def __init__(
        self,
        *,
        builder: StudentCalibrationBuilder | None = None,
        repository: TwinRepository | None = None,
    ) -> None:
        self._builder = builder if builder is not None else StudentCalibrationBuilder()
        self._repository = (
            repository if repository is not None else TwinRepository()
        )

    @property
    def builder(self) -> StudentCalibrationBuilder:
        """Injected or default StudentCalibrationBuilder (independent component)."""
        return self._builder

    @property
    def repository(self) -> TwinRepository:
        """Injected or default TwinRepository (independent component)."""
        return self._repository

    def persist_birth(
        self,
        contract: StudentCalibrationContract,
        *,
        scope: TwinScope | None = None,
        snapshot_id: str | None = None,
        persisted_at: datetime | None = None,
    ) -> PersistedCalibrationBirth | TwinPersistenceFailure:
        """Build Birth Twin from Contract, then persist as current snapshot.

        Args:
            contract: Immutable, student-confirmed Calibration Contract.
            scope: Optional authorised TwinScope. Defaults from Contract /
                Twin Identity (student, curriculum, sitting label).
            snapshot_id: Optional explicit snapshot identity.
            persisted_at: Optional persist timestamp (defaults inside Repository).

        Returns:
            ``PersistedCalibrationBirth`` on success, or ``TwinPersistenceFailure``
            honesty when Persistence cannot store. Builder structural failures
            raise ``CalibrationValidationError`` (unlawful Contract).

        Raises:
            CalibrationValidationError: Structurally unlawful Contract.
        """
        calibration = self._builder.build(contract)
        resolved_scope = (
            scope if scope is not None else self._scope_from_contract(contract)
        )
        provenance = self._provenance_from_metadata(calibration.metadata)

        acknowledgement = self._repository.persist_birth_twin(
            calibration.twin,
            scope=resolved_scope,
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

    def _scope_from_contract(self, contract: StudentCalibrationContract) -> TwinScope:
        """Map Contract identity anchors to TwinScope — wiring only."""
        return TwinScope.create(
            contract.authorised_student_identity,
            sitting_id=contract.intended_sitting.sitting_label,
            curriculum_id=contract.curriculum_exam_scope.curriculum_id,
        )

    def _provenance_from_metadata(
        self, metadata: CalibrationBirthMetadata
    ) -> dict[str, Any]:
        """Opaque Calibration lineage cargo for Persistence — no reinterpretation."""
        return {
            "source": metadata.source or SOURCE_SELF_DECLARED,
            "authorship": TwinAuthorship.BIRTH.value,
            "contract_version": metadata.contract_version,
            "warrant_posture": metadata.warrant_posture,
            "declared_posture": metadata.declared_posture.value,
            "study_objective": metadata.study_objective.value,
            "beginner_or_history_posture": (
                metadata.beginner_or_history_posture.value
            ),
            "declaration_confirmation": metadata.declaration_confirmation,
            "sitting_label": metadata.sitting_label,
        }

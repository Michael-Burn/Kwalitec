"""StudentCalibrationBuilder — Application Layer Twin-birth prior constructor.

Accepts an immutable Student Calibration Contract, performs structural
validation only, and emits an immutable calibrated birth Twin with
self_declared provenance.

Owns capture → validate structure → map priors → emit.
Never infers mastery, confidence, readiness, recommendations, or predictions.
Never persists. Never calls Educational Intelligence domains, Flask, or ORM.

See Capabilities 3.6.1–3.6.5 and APPLICATION_LAYER_ARCHITECTURE.md.
"""

from __future__ import annotations

from app.application.calibration.contract import (
    CONTRACT_VERSION_1_0,
    SOURCE_SELF_DECLARED,
    WARRANT_THIN,
    BeginnerOrHistoryPosture,
    CoreReadingCompleted,
    CoreReadingDeclaration,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationContract,
    StudyObjective,
    derive_declared_posture,
)
from app.application.calibration.result import (
    CalibrationBirthMetadata,
    CalibrationResult,
    KnowledgePriorMarker,
    PerformancePriorMarker,
    PriorProvenance,
)
from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.goal_state import GoalState
from app.domain.twin.identity_state import IdentityState
from app.domain.twin.knowledge_state import KnowledgeState
from app.domain.twin.memory_state import MemoryState
from app.domain.twin.performance_state import PerformanceState
from app.domain.twin.prediction_state import PredictionState

_ACCEPTED_CONTRACT_VERSIONS = frozenset({CONTRACT_VERSION_1_0})


class CalibrationBuildError(Exception):
    """Base class for StudentCalibrationBuilder fail-closed outcomes."""


class CalibrationValidationError(CalibrationBuildError):
    """Contract failed structural validation — Twin birth must not proceed."""


class StudentCalibrationBuilder:
    """Application constructor: Calibration Contract → birth Twin + metadata.

    Structural placement only. Domains never import this builder; they receive
    Twin snapshots as arguments after Persistence / retrieval adapters (future).
    """

    def build(self, contract: StudentCalibrationContract) -> CalibrationResult:
        """Validate structure and emit an immutable calibrated birth Twin.

        Args:
            contract: Immutable, student-confirmed Version 1.0 Calibration
                Contract. Draft / unconfirmed artefacts must not be passed.

        Returns:
            ``CalibrationResult`` with Identity / Goals anchors, empty belief
            domains, and self_declared prior markers in birth metadata.

        Raises:
            CalibrationValidationError: Structurally unlawful contract.
        """
        if not isinstance(contract, StudentCalibrationContract):
            raise CalibrationValidationError(
                "contract must be StudentCalibrationContract, "
                f"got {type(contract)!r}"
            )

        self._validate_structure(contract)

        identity = self._map_identity(contract)
        goals = self._map_goals(contract)
        knowledge_priors = self._map_knowledge_priors(contract)
        performance_priors = self._map_performance_priors(contract)
        metadata = self._build_metadata(
            contract,
            knowledge_priors=knowledge_priors,
            performance_priors=performance_priors,
        )

        # Intentional unknowns: mastery, confidence, readiness, Memory,
        # Behaviour, Predictions, assessment Performance warrant — all empty.
        # optional_notes are ignored for Twin prior construction.
        twin = DigitalTwin.create(
            identity,
            goals=goals,
            knowledge=KnowledgeState.create(),
            memory=MemoryState.create(),
            behaviour=BehaviourState.create(),
            performance=PerformanceState.create(),
            predictions=PredictionState.create(),
        )

        return CalibrationResult(twin=twin, metadata=metadata)

    def _validate_structure(self, contract: StudentCalibrationContract) -> None:
        """Structural legality only — never educational worth."""
        if not contract.declaration_confirmation:
            raise CalibrationValidationError(
                "declaration_confirmation must be true; drafts are not contracts"
            )

        if contract.contract_version not in _ACCEPTED_CONTRACT_VERSIONS:
            raise CalibrationValidationError(
                f"unsupported contract_version: {contract.contract_version!r}"
            )

        if not contract.authorised_student_identity.strip():
            raise CalibrationValidationError(
                "authorised_student_identity is required"
            )

        if not contract.curriculum_exam_scope.curriculum_id.strip():
            raise CalibrationValidationError(
                "curriculum_exam_scope.curriculum_id is required"
            )

        if not isinstance(contract.study_objective, StudyObjective):
            raise CalibrationValidationError(
                f"unrecognised study_objective: {contract.study_objective!r}"
            )

        if not isinstance(contract.previously_studied, PreviouslyStudied):
            raise CalibrationValidationError(
                f"unrecognised previously_studied: {contract.previously_studied!r}"
            )

        if not isinstance(
            contract.beginner_or_history_posture, BeginnerOrHistoryPosture
        ):
            raise CalibrationValidationError(
                "unrecognised beginner_or_history_posture: "
                f"{contract.beginner_or_history_posture!r}"
            )

        self._validate_posture_consistency(contract)
        self._validate_core_reading(contract.core_reading_completed)
        self._validate_attempts(contract.previous_attempts)
        self._validate_sections(contract)
        self._validate_capacity(contract.declared_study_capacity)

        if (
            contract.intended_sitting.sitting_date is None
            and contract.intended_sitting.sitting_label is None
        ):
            raise CalibrationValidationError(
                "intended_sitting requires sitting_date and/or sitting_label"
            )

    def _validate_posture_consistency(
        self, contract: StudentCalibrationContract
    ) -> None:
        """Reject silent Mid coercion; require coherent empty vs history posture."""
        first_time = contract.previously_studied is PreviouslyStudied.FIRST_TIME
        empty = (
            contract.beginner_or_history_posture
            is BeginnerOrHistoryPosture.EMPTY_HISTORY
        )
        history = (
            contract.beginner_or_history_posture
            is BeginnerOrHistoryPosture.HISTORY_PRESENT
        )

        if first_time and history:
            raise CalibrationValidationError(
                "previously_studied=first_time conflicts with "
                "beginner_or_history_posture=history_present"
            )
        if not first_time and empty:
            raise CalibrationValidationError(
                "previously_studied=previously_studied conflicts with "
                "beginner_or_history_posture=empty_history"
            )

        if empty and contract.declared_completed_sections:
            raise CalibrationValidationError(
                "empty_history posture must not declare completed sections"
            )

        if empty and not contract.previous_attempts.none:
            raise CalibrationValidationError(
                "empty_history posture must not declare previous attempts"
            )

        if (
            empty
            and contract.core_reading_completed.posture
            is not CoreReadingCompleted.NONE
        ):
            raise CalibrationValidationError(
                "empty_history posture requires core_reading_completed=none"
            )

    def _validate_core_reading(self, declaration: CoreReadingDeclaration) -> None:
        if not isinstance(declaration, CoreReadingDeclaration):
            raise CalibrationValidationError(
                "core_reading_completed must be CoreReadingDeclaration"
            )
        if not isinstance(declaration.posture, CoreReadingCompleted):
            raise CalibrationValidationError(
                f"unrecognised core_reading posture: {declaration.posture!r}"
            )
        for section_id in declaration.section_ids:
            if not isinstance(section_id, str) or not section_id.strip():
                raise CalibrationValidationError(
                    "core_reading section_ids must be non-blank canonical ids"
                )

    def _validate_attempts(self, declaration: PreviousAttemptsDeclaration) -> None:
        if not isinstance(declaration, PreviousAttemptsDeclaration):
            raise CalibrationValidationError(
                "previous_attempts must be PreviousAttemptsDeclaration"
            )
        if declaration.none:
            if declaration.count not in (None, 0):
                raise CalibrationValidationError(
                    "previous_attempts none must not carry a positive count"
                )
            if declaration.sitting_labels:
                raise CalibrationValidationError(
                    "previous_attempts none must not carry sitting_labels"
                )
            return
        if declaration.count is None and not declaration.sitting_labels:
            raise CalibrationValidationError(
                "previous_attempts requires count and/or sitting_labels when not none"
            )
        if declaration.count is not None and declaration.count < 0:
            raise CalibrationValidationError(
                "previous_attempts count must be non-negative"
            )

    def _validate_sections(self, contract: StudentCalibrationContract) -> None:
        for section_id in contract.declared_completed_sections:
            if not isinstance(section_id, str) or not section_id.strip():
                raise CalibrationValidationError(
                    "declared_completed_sections must be non-blank canonical ids"
                )

    def _validate_capacity(self, capacity: float | None) -> None:
        if capacity is None:
            return
        if isinstance(capacity, bool) or not isinstance(capacity, int | float):
            raise CalibrationValidationError(
                "declared_study_capacity must be a number or None"
            )
        if float(capacity) < 0.0:
            raise CalibrationValidationError(
                "declared_study_capacity must be non-negative"
            )

    def _map_identity(self, contract: StudentCalibrationContract) -> IdentityState:
        scope = contract.curriculum_exam_scope
        return IdentityState.create(
            contract.authorised_student_identity,
            curriculum_id=scope.curriculum_id,
            current_exam=scope.current_exam,
            target_sitting=contract.intended_sitting.sitting_date,
        )

    def _map_goals(self, contract: StudentCalibrationContract) -> GoalState:
        # study_objective is Goals posture — stored in birth metadata because
        # Version 1.0 GoalState has no objective token slot (no Twin redesign).
        # Capacity maps to planned_study_hours_per_week only — never Behaviour.
        # Pass-ambition / forecast fields stay unset (intentional unknown).
        return GoalState.create(
            target_completion_date=contract.intended_sitting.sitting_date,
            planned_study_hours_per_week=contract.declared_study_capacity,
        )

    def _map_knowledge_priors(
        self, contract: StudentCalibrationContract
    ) -> tuple[KnowledgePriorMarker, ...]:
        """Map history declarations to Knowledge prior markers — never mastery."""
        version = contract.contract_version
        priors: list[KnowledgePriorMarker] = []
        scope_id = contract.curriculum_exam_scope.curriculum_id

        if contract.previously_studied is PreviouslyStudied.FIRST_TIME:
            priors.append(
                KnowledgePriorMarker.create(
                    kind="exposure_prior",
                    scope_id=scope_id,
                    provenance=PriorProvenance.self_declared(
                        contract_field="previously_studied",
                        contract_version=version,
                    ),
                    payload={
                        "previously_studied": PreviouslyStudied.FIRST_TIME.value,
                        "empty_history": True,
                    },
                )
            )
        else:
            priors.append(
                KnowledgePriorMarker.create(
                    kind="exposure_prior",
                    scope_id=scope_id,
                    provenance=PriorProvenance.self_declared(
                        contract_field="previously_studied",
                        contract_version=version,
                    ),
                    payload={
                        "previously_studied": (
                            PreviouslyStudied.PREVIOUSLY_STUDIED.value
                        ),
                        "empty_history": False,
                    },
                )
            )

        cr = contract.core_reading_completed
        priors.append(
            KnowledgePriorMarker.create(
                kind="core_reading_prior",
                scope_id=scope_id,
                section_ids=cr.section_ids,
                provenance=PriorProvenance.self_declared(
                    contract_field="core_reading_completed",
                    contract_version=version,
                ),
                payload={
                    "posture": cr.posture.value,
                    "section_ids": list(cr.section_ids),
                },
            )
        )

        if contract.declared_completed_sections:
            priors.append(
                KnowledgePriorMarker.create(
                    kind="declared_complete_prior",
                    scope_id=scope_id,
                    section_ids=contract.declared_completed_sections,
                    provenance=PriorProvenance.self_declared(
                        contract_field="declared_completed_sections",
                        contract_version=version,
                    ),
                    payload={
                        "section_ids": list(contract.declared_completed_sections),
                    },
                )
            )

        return tuple(priors)

    def _map_performance_priors(
        self, contract: StudentCalibrationContract
    ) -> tuple[PerformancePriorMarker, ...]:
        """Map attempt history to Performance prior markers — never marks."""
        attempts = contract.previous_attempts
        version = contract.contract_version
        if attempts.none:
            return (
                PerformancePriorMarker.create(
                    kind="attempt_history_prior",
                    provenance=PriorProvenance.self_declared(
                        contract_field="previous_attempts",
                        contract_version=version,
                    ),
                    payload={"none": True},
                ),
            )

        payload: dict[str, object] = {"none": False}
        if attempts.count is not None:
            payload["count"] = attempts.count
        if attempts.sitting_labels:
            payload["sitting_labels"] = list(attempts.sitting_labels)
        if attempts.declared_outcome is not None:
            payload["declared_outcome"] = attempts.declared_outcome

        return (
            PerformancePriorMarker.create(
                kind="attempt_history_prior",
                provenance=PriorProvenance.self_declared(
                    contract_field="previous_attempts",
                    contract_version=version,
                ),
                payload=payload,
            ),
        )

    def _build_metadata(
        self,
        contract: StudentCalibrationContract,
        *,
        knowledge_priors: tuple[KnowledgePriorMarker, ...],
        performance_priors: tuple[PerformancePriorMarker, ...],
    ) -> CalibrationBirthMetadata:
        return CalibrationBirthMetadata.create(
            contract_version=contract.contract_version,
            declaration_confirmation=contract.declaration_confirmation,
            declared_posture=derive_declared_posture(contract),
            beginner_or_history_posture=contract.beginner_or_history_posture,
            study_objective=contract.study_objective,
            warrant_posture=WARRANT_THIN,
            source=SOURCE_SELF_DECLARED,
            emitted_at=contract.emitted_at,
            sitting_label=contract.intended_sitting.sitting_label,
            knowledge_priors=knowledge_priors,
            performance_priors=performance_priors,
        )

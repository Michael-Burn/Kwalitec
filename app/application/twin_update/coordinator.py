"""Twin Update Coordinator — Application Layer write-path orchestrator.

Sequences Current Twin + Educational Evidence through Strategies → Twin
Composer → Twin Repository. Owns orchestration and honest failure only.

Does not interpret Evidence, author educational state, assemble Twins, persist
directly, retrieve Twins, or access Flask request/session objects. Educational
judgement and product packaging remain outside this conductor.

See Capability 4.9.6 architecture and Capability 4.9.7 implementation.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence

from app.application.twin_repository.types import (
    PersistAcknowledgement,
    TwinPersistenceFailure,
    TwinScope,
)
from app.application.twin_update.evidence import (
    EVIDENCE_PACKAGE_VERSION_1_0,
    EducationalEvidencePackage,
)
from app.application.twin_update.outputs import DomainStrategyOutput
from app.application.twin_update.protocols import (
    TwinComposerProtocol,
    TwinSuccessorRepositoryProtocol,
    TwinUpdateStrategyProtocol,
)
from app.application.twin_update.result import (
    TwinUpdateFailure,
    TwinUpdateFailureReason,
    TwinUpdateResult,
    TwinUpdateSuccess,
)
from app.domain.twin.digital_twin import DigitalTwin

logger = logging.getLogger(__name__)


class TwinUpdateCoordinator:
    """Application Layer conductor for Evidence-driven Twin succession.

    Injected Strategy, Composer, and Repository collaborators own their
    respective interpretation, assembly, and persistence responsibilities.
    """

    def __init__(
        self,
        *,
        strategies: Sequence[TwinUpdateStrategyProtocol],
        composer: TwinComposerProtocol,
        repository: TwinSuccessorRepositoryProtocol,
    ) -> None:
        """Wire Strategy, Composer, and Repository collaborators.

        Args:
            strategies: Invited Twin Update Strategies for this composition cycle.
            composer: Twin Composer assembly authority.
            repository: Twin Repository successor persistence adapter.
        """
        self._strategies = tuple(strategies)
        self._composer = composer
        self._repository = repository

    def update(
        self,
        current_twin: DigitalTwin | None,
        evidence: EducationalEvidencePackage | None,
        *,
        scope: TwinScope | None = None,
    ) -> TwinUpdateResult:
        """Orchestrate Strategy → Composer → Repository for Twin succession.

        Args:
            current_twin: Lawful immutable Current Twin (caller-supplied).
            evidence: Immutable Educational Evidence Package (caller-supplied).
            scope: Optional TwinScope for persistence; defaults from Twin identity.

        Returns:
            TwinUpdateSuccess when the Successor Twin is persisted, or
            TwinUpdateFailure on honest structural / collaborator failure.
            Never fabricates Successor Twins.
        """
        logger.info("Twin update started")

        twin_check = self._validate_current_twin(current_twin)
        if twin_check is not None:
            logger.info("Twin update failed: missing current twin")
            return twin_check
        assert current_twin is not None

        evidence_check = self._validate_evidence(current_twin, evidence)
        if evidence_check is not None:
            logger.info("Twin update failed: invalid evidence")
            return evidence_check
        assert evidence is not None

        if not self._strategies:
            logger.info("Twin update failed: strategy failure")
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.STRATEGY_FAILURE,
                detail="no Twin Update Strategies invited for composition cycle",
            )

        outputs: list[DomainStrategyOutput] = []
        strategy_identities: list[str] = []
        for strategy in self._strategies:
            identity = strategy.strategy_identity
            logger.info("%s Strategy invoked", identity)
            try:
                output = strategy.interpret(current_twin, evidence)
            except Exception as exc:  # noqa: BLE001 — honest collaborator failure
                logger.info("Twin update failed: strategy failure")
                return TwinUpdateFailure(
                    reason=TwinUpdateFailureReason.STRATEGY_FAILURE,
                    detail=f"{identity}: {exc}",
                )
            output_check = self._validate_strategy_output(identity, output)
            if output_check is not None:
                logger.info("Twin update failed: strategy failure")
                return output_check
            outputs.append(output)
            strategy_identities.append(identity)

        try:
            successor = self._composer.compose(current_twin, tuple(outputs))
        except Exception as exc:  # noqa: BLE001 — honest collaborator failure
            logger.info("Twin update failed: composer failure")
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.COMPOSER_FAILURE,
                detail=str(exc),
            )

        if not isinstance(successor, DigitalTwin):
            logger.info("Twin update failed: composer failure")
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.COMPOSER_FAILURE,
                detail="composer did not return a DigitalTwin Successor",
            )

        logger.info("Composer completed")

        resolved_scope = scope
        if resolved_scope is None:
            resolved_scope = TwinScope.create(
                current_twin.identity.student_id,
                curriculum_id=current_twin.identity.curriculum_id,
                sitting_id=evidence.sitting_id,
            )

        provenance = {
            "evidence_id": evidence.evidence_id,
            "strategy_identities": tuple(strategy_identities),
            "package_version": evidence.package_version,
        }

        try:
            persist_result = self._repository.persist_successor_twin(
                successor,
                scope=resolved_scope,
                provenance=provenance,
            )
        except Exception as exc:  # noqa: BLE001 — honest collaborator failure
            logger.info("Twin update failed: repository failure")
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.REPOSITORY_FAILURE,
                detail=str(exc),
            )

        if isinstance(persist_result, TwinPersistenceFailure):
            logger.info("Twin update failed: repository failure")
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.REPOSITORY_FAILURE,
                detail=persist_result.detail or persist_result.reason.value,
            )

        if not isinstance(persist_result, PersistAcknowledgement):
            logger.info("Twin update failed: repository failure")
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.REPOSITORY_FAILURE,
                detail="repository returned unrecognised persist result",
            )

        logger.info("Repository persisted successor")
        logger.info("Twin update completed")

        return TwinUpdateSuccess(
            successor_twin=successor,
            acknowledgement=persist_result,
            strategy_identities=tuple(strategy_identities),
        )

    @staticmethod
    def _validate_current_twin(
        current_twin: DigitalTwin | None,
    ) -> TwinUpdateFailure | None:
        """Structural Current Twin integrity — never educational judgement."""
        if current_twin is None:
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.MISSING_CURRENT_TWIN,
                detail="Current Twin is required; Calibration remains birth author",
            )
        if not isinstance(current_twin, DigitalTwin):
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.MISSING_CURRENT_TWIN,
                detail="Current Twin payload is not a DigitalTwin",
            )
        student_id = getattr(
            getattr(current_twin, "identity", None), "student_id", None
        )
        if not isinstance(student_id, str) or not student_id.strip():
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.MISSING_CURRENT_TWIN,
                detail="Current Twin identity.student_id is missing",
            )
        for attr in (
            "identity",
            "goals",
            "knowledge",
            "memory",
            "behaviour",
            "performance",
            "predictions",
        ):
            if not hasattr(current_twin, attr):
                return TwinUpdateFailure(
                    reason=TwinUpdateFailureReason.MISSING_CURRENT_TWIN,
                    detail=f"Current Twin missing domain attribute: {attr}",
                )
        return None

    @staticmethod
    def _validate_evidence(
        current_twin: DigitalTwin,
        evidence: EducationalEvidencePackage | None,
    ) -> TwinUpdateFailure | None:
        """Structural Evidence integrity — never educational correctness."""
        if evidence is None:
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="Educational Evidence Package is required",
            )
        if not isinstance(evidence, EducationalEvidencePackage):
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="Evidence payload is not an EducationalEvidencePackage",
            )

        if not evidence.evidence_id.strip():
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="evidence_id must be present",
            )
        if not evidence.student_id.strip():
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="student_id must be present",
            )
        if not evidence.provenance.strip():
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="provenance must be present",
            )
        if evidence.contract_version.strip() != EVIDENCE_PACKAGE_VERSION_1_0:
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail=(
                    f"unsupported Evidence contract_version: "
                    f"{evidence.contract_version!r}"
                ),
            )
        if not evidence.study_plan_id.strip():
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="study_plan_id must be present",
            )
        if not evidence.curriculum_id.strip():
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="curriculum_id must be present",
            )
        if not evidence.observed_events:
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="observed_events must be non-empty",
            )

        if evidence.student_id != current_twin.identity.student_id:
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail="Evidence student_id does not match Current Twin identity",
            )

        twin_curriculum = current_twin.identity.curriculum_id
        if (
            evidence.curriculum_id is not None
            and twin_curriculum is not None
            and evidence.curriculum_id != twin_curriculum
        ):
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.INVALID_EVIDENCE,
                detail=(
                    "Evidence curriculum_id does not match Current Twin identity"
                ),
            )

        return None

    @staticmethod
    def _validate_strategy_output(
        expected_identity: str,
        output: object,
    ) -> TwinUpdateFailure | None:
        """Reject unlawful Strategy outputs — structural only, never educational."""
        if not isinstance(output, DomainStrategyOutput):
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.STRATEGY_FAILURE,
                detail=(
                    f"{expected_identity}: Strategy must return DomainStrategyOutput"
                ),
            )
        if output.strategy_identity != expected_identity:
            return TwinUpdateFailure(
                reason=TwinUpdateFailureReason.STRATEGY_FAILURE,
                detail=(
                    f"{expected_identity}: Strategy identity mismatch in output "
                    f"({output.strategy_identity!r})"
                ),
            )
        return None

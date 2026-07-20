"""Policy governing EducationalDiagnosis construction and identity integrity.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Diagnosis Validation Policy
"""

from __future__ import annotations

from domain.education.diagnosis.entities.diagnosis_indicator import (
    DiagnosisIndicator,
    InterpretationReference,
)
from domain.education.diagnosis.entities.diagnosis_reason import DiagnosisReason
from domain.education.diagnosis.entities.diagnosis_scope import DiagnosisScope
from domain.education.diagnosis.enums import DiagnosisStatus
from domain.education.diagnosis.value_objects.diagnosis_confidence import (
    DiagnosisConfidence,
)
from domain.education.diagnosis.value_objects.diagnosis_severity import (
    DiagnosisSeverity,
)
from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId

_TERMINAL_STATUSES = frozenset({DiagnosisStatus.INVALIDATED})


class DiagnosisValidationPolicy:
    """Enforces EducationalDiagnosis identity, ownership, and support invariants."""

    @staticmethod
    def assert_identity(diagnosis_id: DiagnosisId) -> DiagnosisId:
        if not isinstance(diagnosis_id, DiagnosisId):
            raise EducationalInvariantViolation(
                "diagnosis must possess a DiagnosisId identity",
                invariant="EducationalDiagnosis.identity.required",
            )
        return diagnosis_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_diagnosis_type(diagnosis_type: DiagnosisType) -> DiagnosisType:
        if not isinstance(diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis must name a DiagnosisType from the authoritative "
                "deficiency catalogue",
                invariant="EducationalDiagnosis.type.required",
            )
        return diagnosis_type

    @staticmethod
    def assert_scope(scope: DiagnosisScope) -> DiagnosisScope:
        if not isinstance(scope, DiagnosisScope):
            raise EducationalInvariantViolation(
                "diagnosis must identify educational scope",
                invariant="EducationalDiagnosis.scope.required",
            )
        if not scope.statement.strip():
            raise EducationalInvariantViolation(
                "diagnosis must identify educational scope",
                invariant="EducationalDiagnosis.scope.statement.required",
            )
        return scope

    @staticmethod
    def assert_confidence(confidence: DiagnosisConfidence) -> DiagnosisConfidence:
        if not isinstance(confidence, DiagnosisConfidence):
            raise EducationalInvariantViolation(
                "diagnosis must possess confidence",
                invariant="EducationalDiagnosis.confidence.required",
            )
        return confidence

    @staticmethod
    def assert_severity(severity: DiagnosisSeverity) -> DiagnosisSeverity:
        if not isinstance(severity, DiagnosisSeverity):
            raise EducationalInvariantViolation(
                "diagnosis must possess severity",
                invariant="EducationalDiagnosis.severity.required",
            )
        return severity

    @staticmethod
    def assert_status(status: DiagnosisStatus) -> DiagnosisStatus:
        if not isinstance(status, DiagnosisStatus):
            raise EducationalInvariantViolation(
                "status must be a DiagnosisStatus",
                invariant="EducationalDiagnosis.status.type",
            )
        return status

    @staticmethod
    def assert_mutable(status: DiagnosisStatus, *, action: str) -> None:
        if status in _TERMINAL_STATUSES:
            raise EducationalInvariantViolation(
                f"cannot {action} an invalidated diagnosis",
                invariant="EducationalDiagnosis.status.mutable",
            )

    @staticmethod
    def assert_invalidation_reason(reason: str) -> str:
        return require_non_empty_text(reason, "invalidation_reason")

    @staticmethod
    def assert_indicators(
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
    ) -> tuple[DiagnosisIndicator, ...]:
        """Diagnosis cannot exist without support — at least one indicator."""
        collected = tuple(indicators)
        if not collected:
            raise EducationalInvariantViolation(
                "diagnosis cannot exist without support "
                "(at least one diagnosis indicator required)",
                invariant="EducationalDiagnosis.indicators.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, frozenset[str], frozenset[str]]] = set()
        for indicator in collected:
            if not isinstance(indicator, DiagnosisIndicator):
                raise EducationalInvariantViolation(
                    "indicators must be DiagnosisIndicator entities",
                    invariant="EducationalDiagnosis.indicators.type",
                )
            if indicator.indicator_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate diagnosis indicator identity is not allowed",
                    invariant="EducationalDiagnosis.indicators.no_duplicate_id",
                )
            signature = indicator.support_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "identical supporting indicators must not be duplicated",
                    invariant="EducationalDiagnosis.indicators.no_identical_duplicate",
                )
            seen_ids.add(indicator.indicator_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_reasons(
        reasons: tuple[DiagnosisReason, ...] | list[DiagnosisReason],
    ) -> tuple[DiagnosisReason, ...]:
        """Diagnosis must state at least one reason; no duplicate reasons."""
        collected = tuple(reasons)
        if not collected:
            raise EducationalInvariantViolation(
                "diagnosis must possess at least one reason",
                invariant="EducationalDiagnosis.reasons.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str | None]] = set()
        for reason in collected:
            if not isinstance(reason, DiagnosisReason):
                raise EducationalInvariantViolation(
                    "reasons must be DiagnosisReason entities",
                    invariant="EducationalDiagnosis.reasons.type",
                )
            if reason.reason_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate diagnosis reason identity is not allowed",
                    invariant="EducationalDiagnosis.reasons.no_duplicate_id",
                )
            signature = reason.reason_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "cannot duplicate reasons",
                    invariant="EducationalDiagnosis.reasons.no_identical_duplicate",
                )
            seen_ids.add(reason.reason_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_reason_not_duplicate(
        existing: list[DiagnosisReason] | tuple[DiagnosisReason, ...],
        candidate: DiagnosisReason,
    ) -> None:
        signatures = {r.reason_signature() for r in existing}
        ids = {r.reason_id.value for r in existing}
        if candidate.reason_id.value in ids:
            raise EducationalInvariantViolation(
                "duplicate diagnosis reason identity is not allowed",
                invariant="EducationalDiagnosis.reasons.no_duplicate_id",
            )
        if candidate.reason_signature() in signatures:
            raise EducationalInvariantViolation(
                "cannot duplicate reasons",
                invariant="EducationalDiagnosis.reasons.no_identical_duplicate",
            )

    @staticmethod
    def assert_indicator_not_duplicate(
        existing: list[DiagnosisIndicator] | tuple[DiagnosisIndicator, ...],
        candidate: DiagnosisIndicator,
    ) -> None:
        signatures = {i.support_signature() for i in existing}
        ids = {i.indicator_id.value for i in existing}
        if candidate.indicator_id.value in ids:
            raise EducationalInvariantViolation(
                "duplicate diagnosis indicator identity is not allowed",
                invariant="EducationalDiagnosis.indicators.no_duplicate_id",
            )
        if candidate.support_signature() in signatures:
            raise EducationalInvariantViolation(
                "identical supporting indicators must not be duplicated",
                invariant="EducationalDiagnosis.indicators.no_identical_duplicate",
            )

    @staticmethod
    def assert_references_interpretation(
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
    ) -> frozenset[str]:
        """Diagnosis must reference at least one Interpretation."""
        ids: set[str] = set()
        for indicator in indicators:
            for ref in indicator.interpretation_references:
                ids.add(ref.interpretation_id)
        if not ids:
            raise EducationalInvariantViolation(
                "diagnosis must reference at least one Interpretation",
                invariant="EducationalDiagnosis.interpretations.min_one",
            )
        return frozenset(ids)

    @staticmethod
    def assert_references_evidence(
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
    ) -> frozenset[EvidenceId]:
        """Diagnosis must reference supporting Evidence."""
        ids: set[EvidenceId] = set()
        for indicator in indicators:
            ids.update(indicator.evidence_ids)
        if not ids:
            raise EducationalInvariantViolation(
                "diagnosis must reference supporting Evidence",
                invariant="EducationalDiagnosis.evidence.min_one",
            )
        return frozenset(ids)

    @staticmethod
    def assert_known_evidence(
        known: frozenset[EvidenceId] | set[EvidenceId],
        referenced: frozenset[EvidenceId] | set[EvidenceId],
    ) -> None:
        if not known:
            return
        unknown = referenced - set(known)
        if unknown:
            sample = next(iter(unknown))
            raise EducationalInvariantViolation(
                f"evidence {sample.value} is not among known evidence ids",
                invariant="EducationalDiagnosis.evidence.known",
            )

    @staticmethod
    def assert_known_interpretations(
        known: frozenset[str] | set[str],
        referenced: frozenset[str] | set[str],
    ) -> None:
        if not known:
            return
        unknown = referenced - set(known)
        if unknown:
            sample = next(iter(unknown))
            raise EducationalInvariantViolation(
                f"interpretation {sample} is not among known interpretation ids",
                invariant="EducationalDiagnosis.interpretations.known",
            )

    @staticmethod
    def collect_interpretation_references(
        indicators: tuple[DiagnosisIndicator, ...] | list[DiagnosisIndicator],
        extra: tuple[InterpretationReference, ...]
        | list[InterpretationReference]
        | None = None,
    ) -> tuple[InterpretationReference, ...]:
        by_id: dict[str, InterpretationReference] = {}
        for indicator in indicators:
            for ref in indicator.interpretation_references:
                by_id[ref.interpretation_id] = ref
        for ref in extra or ():
            if not isinstance(ref, InterpretationReference):
                raise EducationalInvariantViolation(
                    "interpretation references must be InterpretationReference",
                    invariant="EducationalDiagnosis.interpretation_references.type",
                )
            by_id[ref.interpretation_id] = ref
        return tuple(by_id.values())

"""EducationalDiagnosis aggregate root — named educational deficiency.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Educational Diagnosis
"""

from __future__ import annotations

from domain.education.diagnosis.entities.diagnosis_indicator import (
    DiagnosisIndicator,
    InterpretationReference,
)
from domain.education.diagnosis.entities.diagnosis_reason import DiagnosisReason
from domain.education.diagnosis.entities.diagnosis_scope import DiagnosisScope
from domain.education.diagnosis.enums import DiagnosisStatus
from domain.education.diagnosis.events.diagnosis_created import DiagnosisCreated
from domain.education.diagnosis.events.diagnosis_invalidated import DiagnosisInvalidated
from domain.education.diagnosis.policies.diagnosis_consistency_policy import (
    DiagnosisConsistencyPolicy,
)
from domain.education.diagnosis.policies.diagnosis_validation_policy import (
    DiagnosisValidationPolicy,
)
from domain.education.diagnosis.value_objects.diagnosis_confidence import (
    DiagnosisConfidence,
)
from domain.education.diagnosis.value_objects.diagnosis_severity import (
    DiagnosisSeverity,
)
from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId

DomainEvent = DiagnosisCreated | DiagnosisInvalidated


class EducationalDiagnosis:
    """Aggregate root for educational diagnosis.

    Owns diagnosis type, supporting interpretation references, supporting
    evidence references, educational scope, confidence, severity, and reasons.
    Behaviour is exposed only through methods — no public setters.

    This aggregate produces educational explanations of *what problem exists*.
    It does not prioritise, recommend, select teaching strategies, or generate
    hypotheses.
    """

    def __init__(
        self,
        diagnosis_id: DiagnosisId,
        student_id: str,
        diagnosis_type: DiagnosisType,
        scope: DiagnosisScope,
        confidence: DiagnosisConfidence,
        severity: DiagnosisSeverity,
        indicators: list[DiagnosisIndicator] | tuple[DiagnosisIndicator, ...],
        reasons: list[DiagnosisReason] | tuple[DiagnosisReason, ...],
        *,
        known_evidence_ids: frozenset[EvidenceId]
        | set[EvidenceId]
        | tuple[EvidenceId, ...]
        | None = None,
        known_interpretation_ids: frozenset[str]
        | set[str]
        | tuple[str, ...]
        | None = None,
        interpretation_references: list[InterpretationReference]
        | tuple[InterpretationReference, ...]
        | None = None,
        status: DiagnosisStatus = DiagnosisStatus.ACTIVE,
        invalidation_reason: str | None = None,
        _record_created: bool = False,
    ) -> None:
        self._diagnosis_id = DiagnosisValidationPolicy.assert_identity(diagnosis_id)
        self._student_id = DiagnosisValidationPolicy.assert_student_id(student_id)
        self._diagnosis_type = DiagnosisValidationPolicy.assert_diagnosis_type(
            diagnosis_type
        )
        self._scope = DiagnosisValidationPolicy.assert_scope(scope)
        self._confidence = DiagnosisValidationPolicy.assert_confidence(confidence)
        self._severity = DiagnosisValidationPolicy.assert_severity(severity)
        self._indicators = list(
            DiagnosisValidationPolicy.assert_indicators(indicators)
        )
        self._reasons = list(DiagnosisValidationPolicy.assert_reasons(reasons))
        self._status = DiagnosisValidationPolicy.assert_status(status)
        self._invalidation_reason = (
            require_non_empty_text(invalidation_reason, "invalidation_reason")
            if invalidation_reason is not None
            else None
        )

        referenced_interpretations = (
            DiagnosisValidationPolicy.assert_references_interpretation(
                self._indicators
            )
        )
        referenced_evidence = DiagnosisValidationPolicy.assert_references_evidence(
            self._indicators
        )

        self._known_evidence_ids: frozenset[EvidenceId] = frozenset(
            known_evidence_ids or ()
        )
        self._known_interpretation_ids: frozenset[str] = frozenset(
            known_interpretation_ids or ()
        )
        DiagnosisValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        DiagnosisValidationPolicy.assert_known_interpretations(
            self._known_interpretation_ids, referenced_interpretations
        )

        self._interpretation_references = list(
            DiagnosisValidationPolicy.collect_interpretation_references(
                self._indicators,
                interpretation_references or (),
            )
        )

        DiagnosisConsistencyPolicy.assert_consistent(
            self._diagnosis_type,
            self._indicators,
            self._reasons,
            self._confidence,
            self._severity,
        )

        self._pending_events: list[DomainEvent] = []
        if _record_created:
            self._pending_events.append(
                DiagnosisCreated(
                    diagnosis_id=self._diagnosis_id,
                    student_id=self._student_id,
                    diagnosis_type=self._diagnosis_type,
                    confidence_level=self._confidence.level,
                    severity_level=self._severity.level,
                    indicator_count=len(self._indicators),
                    reason_count=len(self._reasons),
                )
            )

    @classmethod
    def create(
        cls,
        diagnosis_id: DiagnosisId,
        student_id: str,
        diagnosis_type: DiagnosisType,
        scope: DiagnosisScope,
        confidence: DiagnosisConfidence,
        severity: DiagnosisSeverity,
        indicators: list[DiagnosisIndicator] | tuple[DiagnosisIndicator, ...],
        reasons: list[DiagnosisReason] | tuple[DiagnosisReason, ...],
        *,
        known_evidence_ids: frozenset[EvidenceId]
        | set[EvidenceId]
        | tuple[EvidenceId, ...]
        | None = None,
        known_interpretation_ids: frozenset[str]
        | set[str]
        | tuple[str, ...]
        | None = None,
        interpretation_references: list[InterpretationReference]
        | tuple[InterpretationReference, ...]
        | None = None,
    ) -> EducationalDiagnosis:
        """Factory: name an educational problem from interpreted support."""
        return cls(
            diagnosis_id=diagnosis_id,
            student_id=student_id,
            diagnosis_type=diagnosis_type,
            scope=scope,
            confidence=confidence,
            severity=severity,
            indicators=indicators,
            reasons=reasons,
            known_evidence_ids=known_evidence_ids,
            known_interpretation_ids=known_interpretation_ids,
            interpretation_references=interpretation_references,
            status=DiagnosisStatus.ACTIVE,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def diagnosis_id(self) -> DiagnosisId:
        return self._diagnosis_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def diagnosis_type(self) -> DiagnosisType:
        return self._diagnosis_type

    @property
    def scope(self) -> DiagnosisScope:
        return self._scope

    @property
    def confidence(self) -> DiagnosisConfidence:
        return self._confidence

    @property
    def severity(self) -> DiagnosisSeverity:
        return self._severity

    @property
    def indicators(self) -> tuple[DiagnosisIndicator, ...]:
        return tuple(self._indicators)

    @property
    def reasons(self) -> tuple[DiagnosisReason, ...]:
        return tuple(self._reasons)

    @property
    def interpretation_references(self) -> tuple[InterpretationReference, ...]:
        return tuple(self._interpretation_references)

    @property
    def known_evidence_ids(self) -> frozenset[EvidenceId]:
        return self._known_evidence_ids

    @property
    def known_interpretation_ids(self) -> frozenset[str]:
        return self._known_interpretation_ids

    @property
    def status(self) -> DiagnosisStatus:
        return self._status

    @property
    def invalidation_reason(self) -> str | None:
        return self._invalidation_reason

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def revise(
        self,
        *,
        diagnosis_type: DiagnosisType | None = None,
        scope: DiagnosisScope | None = None,
        confidence: DiagnosisConfidence | None = None,
        severity: DiagnosisSeverity | None = None,
        indicators: list[DiagnosisIndicator]
        | tuple[DiagnosisIndicator, ...]
        | None = None,
        reasons: list[DiagnosisReason] | tuple[DiagnosisReason, ...] | None = None,
    ) -> None:
        """Revise diagnostic detail without prioritising or recommending."""
        DiagnosisValidationPolicy.assert_mutable(self._status, action="revise")
        next_type = (
            DiagnosisValidationPolicy.assert_diagnosis_type(diagnosis_type)
            if diagnosis_type is not None
            else self._diagnosis_type
        )
        next_scope = (
            DiagnosisValidationPolicy.assert_scope(scope)
            if scope is not None
            else self._scope
        )
        next_confidence = (
            DiagnosisValidationPolicy.assert_confidence(confidence)
            if confidence is not None
            else self._confidence
        )
        next_severity = (
            DiagnosisValidationPolicy.assert_severity(severity)
            if severity is not None
            else self._severity
        )
        next_indicators = (
            list(DiagnosisValidationPolicy.assert_indicators(indicators))
            if indicators is not None
            else list(self._indicators)
        )
        next_reasons = (
            list(DiagnosisValidationPolicy.assert_reasons(reasons))
            if reasons is not None
            else list(self._reasons)
        )

        referenced_interpretations = (
            DiagnosisValidationPolicy.assert_references_interpretation(
                next_indicators
            )
        )
        referenced_evidence = DiagnosisValidationPolicy.assert_references_evidence(
            next_indicators
        )
        DiagnosisValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        DiagnosisValidationPolicy.assert_known_interpretations(
            self._known_interpretation_ids, referenced_interpretations
        )
        DiagnosisConsistencyPolicy.assert_consistent(
            next_type,
            next_indicators,
            next_reasons,
            next_confidence,
            next_severity,
        )

        self._diagnosis_type = next_type
        self._scope = next_scope
        self._confidence = next_confidence
        self._severity = next_severity
        self._indicators = next_indicators
        self._reasons = next_reasons
        self._interpretation_references = list(
            DiagnosisValidationPolicy.collect_interpretation_references(
                self._indicators,
                self._interpretation_references,
            )
        )
        self._status = DiagnosisStatus.REVISED

    def invalidate(self, reason: str) -> None:
        """Void diagnostic trust in this named deficiency (compensating posture)."""
        DiagnosisValidationPolicy.assert_mutable(self._status, action="invalidate")
        self._invalidation_reason = (
            DiagnosisValidationPolicy.assert_invalidation_reason(reason)
        )
        self._status = DiagnosisStatus.INVALIDATED
        self._pending_events.append(
            DiagnosisInvalidated(
                diagnosis_id=self._diagnosis_id,
                student_id=self._student_id,
                diagnosis_type=self._diagnosis_type,
                reason=self._invalidation_reason,
            )
        )

    def merge_support(self, other: EducationalDiagnosis) -> None:
        """Absorb compatible supporting indicators and reasons from another.

        ``other`` must share student and diagnosis type. Identical duplicate
        support is rejected. ``other`` is not mutated — support is copied.
        """
        DiagnosisValidationPolicy.assert_mutable(self._status, action="merge_support")
        if not isinstance(other, EducationalDiagnosis):
            raise EducationalInvariantViolation(
                "other must be an EducationalDiagnosis",
                invariant="EducationalDiagnosis.merge_support.type",
            )
        if other.diagnosis_id == self._diagnosis_id:
            raise EducationalInvariantViolation(
                "cannot merge support from a diagnosis into itself",
                invariant="EducationalDiagnosis.merge_support.self",
            )
        if other.student_id != self._student_id:
            raise EducationalInvariantViolation(
                "cannot merge support across different students",
                invariant="EducationalDiagnosis.merge_support.student",
            )
        if other.diagnosis_type is not self._diagnosis_type:
            raise EducationalInvariantViolation(
                "cannot merge support across different diagnosis types",
                invariant="EducationalDiagnosis.merge_support.type_match",
            )
        if other.status is DiagnosisStatus.INVALIDATED:
            raise EducationalInvariantViolation(
                "cannot merge support from an invalidated diagnosis",
                invariant="EducationalDiagnosis.merge_support.source_status",
            )

        expanded_evidence = set(self._known_evidence_ids) | set(
            other.known_evidence_ids
        )
        expanded_interpretations = set(self._known_interpretation_ids) | set(
            other.known_interpretation_ids
        )
        self._known_evidence_ids = frozenset(expanded_evidence)
        self._known_interpretation_ids = frozenset(expanded_interpretations)

        next_indicators = list(self._indicators)
        for indicator in other.indicators:
            DiagnosisValidationPolicy.assert_indicator_not_duplicate(
                next_indicators, indicator
            )
            next_indicators.append(indicator)

        next_reasons = list(self._reasons)
        for reason in other.reasons:
            DiagnosisValidationPolicy.assert_reason_not_duplicate(
                next_reasons, reason
            )
            next_reasons.append(reason)

        referenced_interpretations = (
            DiagnosisValidationPolicy.assert_references_interpretation(
                next_indicators
            )
        )
        referenced_evidence = DiagnosisValidationPolicy.assert_references_evidence(
            next_indicators
        )
        DiagnosisValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        DiagnosisValidationPolicy.assert_known_interpretations(
            self._known_interpretation_ids, referenced_interpretations
        )
        DiagnosisConsistencyPolicy.assert_consistent(
            self._diagnosis_type,
            next_indicators,
            next_reasons,
            self._confidence,
            self._severity,
        )

        self._indicators = next_indicators
        self._reasons = next_reasons
        self._interpretation_references = list(
            DiagnosisValidationPolicy.collect_interpretation_references(
                self._indicators,
                list(self._interpretation_references)
                + list(other.interpretation_references),
            )
        )
        self._status = DiagnosisStatus.REVISED

    # --- queries ---

    def is_active(self) -> bool:
        return self._status is DiagnosisStatus.ACTIVE

    def is_revised(self) -> bool:
        return self._status is DiagnosisStatus.REVISED

    def is_invalidated(self) -> bool:
        return self._status is DiagnosisStatus.INVALIDATED

    def supporting_interpretation_ids(self) -> frozenset[str]:
        ids: set[str] = {
            ref.interpretation_id for ref in self._interpretation_references
        }
        for indicator in self._indicators:
            for ref in indicator.interpretation_references:
                ids.add(ref.interpretation_id)
        return frozenset(ids)

    def supporting_evidence_ids(self) -> frozenset[EvidenceId]:
        ids: set[EvidenceId] = set()
        for indicator in self._indicators:
            ids.update(indicator.evidence_ids)
        return frozenset(ids)

    def has_interpretation(self, interpretation_id: str) -> bool:
        return interpretation_id in self.supporting_interpretation_ids()

    def has_evidence(self, evidence_id: EvidenceId) -> bool:
        return evidence_id in self.supporting_evidence_ids()

    def indicator_count(self) -> int:
        return len(self._indicators)

    def reason_count(self) -> int:
        return len(self._reasons)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalDiagnosis):
            return NotImplemented
        return self._diagnosis_id == other._diagnosis_id

    def __hash__(self) -> int:
        return hash((type(self), self._diagnosis_id))

    def __repr__(self) -> str:
        return (
            f"EducationalDiagnosis(diagnosis_id={self._diagnosis_id!r}, "
            f"type={self._diagnosis_type!r}, status={self._status!r})"
        )

"""Educational Diagnosis bounded context — pure educational domain model.

IMP-006 implementation of Educational Diagnosis architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask,
SQLAlchemy, APIs, repositories, serialization, or DTOs.

This domain converts interpreted educational patterns into educational
diagnoses. It does not prioritise, recommend, select teaching strategies, or
generate hypotheses.
"""

from __future__ import annotations

from domain.education.diagnosis.aggregates.educational_diagnosis import (
    EducationalDiagnosis,
)
from domain.education.diagnosis.entities.diagnosis_indicator import (
    DiagnosisIndicator,
    DiagnosisIndicatorId,
    InterpretationReference,
)
from domain.education.diagnosis.entities.diagnosis_reason import (
    DiagnosisReason,
    DiagnosisReasonId,
)
from domain.education.diagnosis.entities.diagnosis_scope import (
    DiagnosisScope,
    DiagnosisScopeId,
)
from domain.education.diagnosis.enums import (
    DiagnosisSeverityLevel,
    DiagnosisStatus,
    EducationalScopeKind,
    IndicatorKind,
)
from domain.education.diagnosis.events.diagnosis_created import DiagnosisCreated
from domain.education.diagnosis.events.diagnosis_invalidated import (
    DiagnosisInvalidated,
)
from domain.education.diagnosis.policies.diagnosis_consistency_policy import (
    DiagnosisConsistencyPolicy,
)
from domain.education.diagnosis.policies.diagnosis_validation_policy import (
    DiagnosisValidationPolicy,
)
from domain.education.diagnosis.specifications.diagnosis_is_actionable import (
    DiagnosisIsActionableSpecification,
)
from domain.education.diagnosis.specifications.diagnosis_is_supported import (
    DiagnosisIsSupportedSpecification,
)
from domain.education.diagnosis.value_objects.diagnosis_confidence import (
    DiagnosisConfidence,
)
from domain.education.diagnosis.value_objects.diagnosis_severity import (
    DiagnosisSeverity,
)
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.ids import DiagnosisId

__all__ = [
    # Aggregate
    "EducationalDiagnosis",
    # Entities
    "DiagnosisIndicator",
    "DiagnosisIndicatorId",
    "InterpretationReference",
    "DiagnosisReason",
    "DiagnosisReasonId",
    "DiagnosisScope",
    "DiagnosisScopeId",
    # Value objects / identity
    "DiagnosisConfidence",
    "DiagnosisSeverity",
    "DiagnosisId",
    # Enums
    "DiagnosisType",
    "DiagnosisStatus",
    "DiagnosisSeverityLevel",
    "EducationalScopeKind",
    "IndicatorKind",
    # Policies
    "DiagnosisValidationPolicy",
    "DiagnosisConsistencyPolicy",
    # Specifications
    "DiagnosisIsSupportedSpecification",
    "DiagnosisIsActionableSpecification",
    # Events
    "DiagnosisCreated",
    "DiagnosisInvalidated",
]

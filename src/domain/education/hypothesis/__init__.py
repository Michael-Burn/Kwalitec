"""Educational Hypothesis bounded context — pure educational domain model.

IMP-007 implementation of Educational Hypothesis architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask,
SQLAlchemy, APIs, repositories, serialization, or DTOs.

This domain converts Educational Diagnoses into revisable educational
explanations. Hypotheses are not facts — they represent the current best
explanation and must remain revisable. This domain does not diagnose,
prioritise, select teaching strategies, or generate teaching intentions.
"""

from __future__ import annotations

from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.ids import HypothesisId
from domain.education.hypothesis.aggregates.educational_hypothesis import (
    EducationalHypothesis,
)
from domain.education.hypothesis.entities.competing_hypothesis import (
    CompetingHypothesis,
    CompetingHypothesisId,
)
from domain.education.hypothesis.entities.hypothesis_reason import (
    DiagnosisReference,
    HypothesisReason,
    HypothesisReasonId,
    InterpretationReference,
)
from domain.education.hypothesis.entities.hypothesis_scope import (
    HypothesisScope,
    HypothesisScopeId,
)
from domain.education.hypothesis.enums import (
    ExplanatoryStrengthLevel,
    HypothesisKind,
    HypothesisScopeKind,
    HypothesisStatus,
    PlausibilityLevel,
    RevisionForm,
)
from domain.education.hypothesis.events.hypothesis_created import HypothesisCreated
from domain.education.hypothesis.events.hypothesis_discarded import HypothesisDiscarded
from domain.education.hypothesis.events.hypothesis_revised import HypothesisRevised
from domain.education.hypothesis.policies.hypothesis_revision_policy import (
    HypothesisRevisionPolicy,
)
from domain.education.hypothesis.policies.hypothesis_validation_policy import (
    HypothesisValidationPolicy,
)
from domain.education.hypothesis.specifications.hypothesis_is_revisable import (
    HypothesisIsRevisableSpecification,
)
from domain.education.hypothesis.specifications.hypothesis_is_supported import (
    HypothesisIsSupportedSpecification,
)
from domain.education.hypothesis.value_objects.explanatory_strength import (
    ExplanatoryStrength,
)
from domain.education.hypothesis.value_objects.plausibility import Plausibility

__all__ = [
    # Aggregate
    "EducationalHypothesis",
    # Entities
    "HypothesisReason",
    "HypothesisReasonId",
    "HypothesisScope",
    "HypothesisScopeId",
    "CompetingHypothesis",
    "CompetingHypothesisId",
    "DiagnosisReference",
    "InterpretationReference",
    # Value objects / identity
    "Plausibility",
    "ExplanatoryStrength",
    "HypothesisId",
    # Enums
    "HypothesisKind",
    "HypothesisStatus",
    "PlausibilityLevel",
    "ExplanatoryStrengthLevel",
    "HypothesisScopeKind",
    "RevisionForm",
    "DiagnosisType",
    # Policies
    "HypothesisValidationPolicy",
    "HypothesisRevisionPolicy",
    # Specifications
    "HypothesisIsSupportedSpecification",
    "HypothesisIsRevisableSpecification",
    # Events
    "HypothesisCreated",
    "HypothesisRevised",
    "HypothesisDiscarded",
]

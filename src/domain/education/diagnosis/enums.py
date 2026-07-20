"""Educational Diagnosis domain enumerations.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    Diagnosis Status / Severity Level / Scope Kind / Indicator Kind
"""

from __future__ import annotations

from enum import StrEnum


class DiagnosisStatus(StrEnum):
    """Lifecycle status of an EducationalDiagnosis aggregate.

    Diagnosis names an educational problem. INVALIDATED voids diagnostic trust;
    REVISED records lawful correction of diagnostic detail. Diagnosis never
    selects teaching strategy, priority, or hypothesis.
    """

    ACTIVE = "active"
    REVISED = "revised"
    INVALIDATED = "invalidated"


class DiagnosisSeverityLevel(StrEnum):
    """Qualitative educational severity of a named deficiency.

    Severity describes how educationally consequential the named problem is
    within its scope. It is not a priority ranking, mastery score, or
    numerical educational law.
    """

    MILD = "mild"
    MODERATE = "moderate"
    SUBSTANTIAL = "substantial"
    SEVERE = "severe"


class EducationalScopeKind(StrEnum):
    """Grain of educational scope identified by a diagnosis."""

    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"
    LEARNING_EPISODE = "learning_episode"
    LEARNING_DIMENSION = "learning_dimension"
    CROSS_CONCEPT = "cross_concept"
    PREREQUISITE_CHAIN = "prerequisite_chain"
    SESSION_WINDOW = "session_window"


class IndicatorKind(StrEnum):
    """Kinds of supporting indicators that warrant a diagnosis.

    Indicators cite interpreted patterns and evidence. They never recommend
    teaching moves or assign priority.
    """

    FRAGILE_EXPLANATION = "fragile_explanation"
    PATTERNED_ERROR = "patterned_error"
    EXECUTION_FAILURE = "execution_failure"
    DELAYED_RETRIEVAL_COLLAPSE = "delayed_retrieval_collapse"
    ISOLATED_LOCAL_SUCCESS = "isolated_local_success"
    UPSTREAM_CAPABILITY_ABSENCE = "upstream_capability_absence"
    STABLE_WRONG_MODEL = "stable_wrong_model"
    UNDERESTIMATED_CAPACITY = "underestimated_capacity"
    OVERESTIMATED_CAPACITY = "overestimated_capacity"
    TIMED_DEPLOYMENT_FAILURE = "timed_deployment_failure"
    TASK_APPLICATION_FAILURE = "task_application_failure"
    VARIANT_TRANSFER_FAILURE = "variant_transfer_failure"
    PARTIAL_FACET_GRASP = "partial_facet_grasp"
    CONFLICTING_SIGNAL = "conflicting_signal"

"""Shared factories for Educational Diagnosis domain tests."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisConfidence,
    DiagnosisIndicator,
    DiagnosisIndicatorId,
    DiagnosisReason,
    DiagnosisReasonId,
    DiagnosisScope,
    DiagnosisScopeId,
    DiagnosisSeverity,
    DiagnosisSeverityLevel,
    EducationalDiagnosis,
    EducationalScopeKind,
    IndicatorKind,
    InterpretationReference,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    DiagnosisType,
    LearningDimension,
)
from domain.education.foundation.ids import (
    ConceptId,
    DiagnosisId,
    EvidenceId,
    LearningEpisodeId,
    LearningObjectiveId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)

CONCEPT_SELECT = ConceptId("concept-select-mortality")
CONCEPT_ULTIMATE = ConceptId("concept-ultimate-mortality")
EPISODE_001 = LearningEpisodeId("episode-001")
EPISODE_002 = LearningEpisodeId("episode-002")
EVIDENCE_001 = EvidenceId("evidence-001")
EVIDENCE_002 = EvidenceId("evidence-002")
EVIDENCE_003 = EvidenceId("evidence-003")
INTERP_001 = "interp-001"
INTERP_002 = "interp-002"
INTERP_003 = "interp-003"
KNOWN_EVIDENCE = frozenset({EVIDENCE_001, EVIDENCE_002, EVIDENCE_003})
KNOWN_INTERPRETATIONS = frozenset({INTERP_001, INTERP_002, INTERP_003})

# Primary compatible indicator per deficiency category (authoritative catalogue).
PRIMARY_INDICATOR_FOR_TYPE: dict[DiagnosisType, IndicatorKind] = {
    DiagnosisType.CONCEPTUAL_MISUNDERSTANDING: IndicatorKind.FRAGILE_EXPLANATION,
    DiagnosisType.PROCEDURAL_WEAKNESS: IndicatorKind.EXECUTION_FAILURE,
    DiagnosisType.WEAK_RETENTION: IndicatorKind.DELAYED_RETRIEVAL_COLLAPSE,
    DiagnosisType.KNOWLEDGE_FRAGMENTATION: IndicatorKind.ISOLATED_LOCAL_SUCCESS,
    DiagnosisType.PREREQUISITE_GAP: IndicatorKind.UPSTREAM_CAPABILITY_ABSENCE,
    DiagnosisType.MISCONCEPTION: IndicatorKind.STABLE_WRONG_MODEL,
    DiagnosisType.LOW_CONFIDENCE: IndicatorKind.UNDERESTIMATED_CAPACITY,
    DiagnosisType.FALSE_CONFIDENCE: IndicatorKind.OVERESTIMATED_CAPACITY,
    DiagnosisType.EXAM_TECHNIQUE_WEAKNESS: IndicatorKind.TIMED_DEPLOYMENT_FAILURE,
    DiagnosisType.APPLICATION_WEAKNESS: IndicatorKind.TASK_APPLICATION_FAILURE,
    DiagnosisType.TRANSFER_WEAKNESS: IndicatorKind.VARIANT_TRANSFER_FAILURE,
    DiagnosisType.INCOMPLETE_UNDERSTANDING: IndicatorKind.PARTIAL_FACET_GRASP,
}

DEFAULT_TYPE = DiagnosisType.CONCEPTUAL_MISUNDERSTANDING


@pytest.fixture
def diagnosis_id() -> DiagnosisId:
    return DiagnosisId("diag-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_confidence(
    level: ConfidenceLevel = ConfidenceLevel.HIGH,
    *,
    ratio: float | None = 0.8,
) -> DiagnosisConfidence:
    return DiagnosisConfidence.of(level, ratio=ratio)


def make_severity(
    level: DiagnosisSeverityLevel = DiagnosisSeverityLevel.MODERATE,
    *,
    rationale: str | None = "educationally consequential within scope",
) -> DiagnosisSeverity:
    return DiagnosisSeverity.of(level, rationale=rationale)


def make_scope(
    *,
    scope_id: str = "scope-001",
    statement: str = "Relative to select mortality objective, conceptual grasp is thin",
    scope_kind: EducationalScopeKind = EducationalScopeKind.LEARNING_OBJECTIVE,
    dimension: LearningDimension | None = LearningDimension.UNDERSTANDING,
    concepts: tuple[ConceptReference, ...] | None = None,
    objectives: tuple[LearningObjectiveReference, ...] | None = None,
    episodes: tuple[LearningEpisodeId, ...] | None = None,
) -> DiagnosisScope:
    return DiagnosisScope(
        scope_id=DiagnosisScopeId(scope_id),
        statement=statement,
        scope_kind=scope_kind,
        learning_dimension=dimension,
        concept_references=concepts
        if concepts is not None
        else (ConceptReference(concept_id=CONCEPT_SELECT, label="Select mortality"),),
        learning_objective_references=objectives
        if objectives is not None
        else (
            LearningObjectiveReference(
                objective_id=LearningObjectiveId("lo-select-ultimate"),
                label="Interpret select mortality tables",
            ),
        ),
        learning_episode_ids=episodes if episodes is not None else (EPISODE_001,),
    )


def make_reason(
    *,
    reason_id: str = "reason-001",
    statement: str = "Fragile explanations collapse when asked why select applies",
    code: str | None = "fragile_why",
) -> DiagnosisReason:
    return DiagnosisReason(
        reason_id=DiagnosisReasonId(reason_id),
        statement=statement,
        code=code,
    )


def make_indicator(
    *,
    indicator_id: str = "indicator-001",
    kind: IndicatorKind | None = None,
    description: str = "Fragile explanations on select mortality probes",
    interpretation_ids: tuple[str, ...] | None = None,
    evidence_ids: tuple[EvidenceId, ...] | None = None,
    diagnosis_type: DiagnosisType = DEFAULT_TYPE,
) -> DiagnosisIndicator:
    indicator_kind = kind or PRIMARY_INDICATOR_FOR_TYPE[diagnosis_type]
    refs = tuple(
        InterpretationReference(interpretation_id=i)
        for i in (interpretation_ids or (INTERP_001,))
    )
    return DiagnosisIndicator(
        indicator_id=DiagnosisIndicatorId(indicator_id),
        kind=indicator_kind,
        description=description,
        interpretation_references=refs,
        evidence_ids=evidence_ids
        if evidence_ids is not None
        else (EVIDENCE_001, EVIDENCE_002),
    )


def make_diagnosis(
    *,
    diagnosis_id: str = "diag-001",
    student_id: str = "student-ada",
    diagnosis_type: DiagnosisType = DEFAULT_TYPE,
    scope: DiagnosisScope | None = None,
    confidence: DiagnosisConfidence | None = None,
    severity: DiagnosisSeverity | None = None,
    indicators: list[DiagnosisIndicator] | None = None,
    reasons: list[DiagnosisReason] | None = None,
    known_evidence: frozenset[EvidenceId] | None = KNOWN_EVIDENCE,
    known_interpretations: frozenset[str] | None = KNOWN_INTERPRETATIONS,
    interpretation_references: list[InterpretationReference] | None = None,
) -> EducationalDiagnosis:
    indicator_list = (
        indicators
        if indicators is not None
        else [make_indicator(diagnosis_type=diagnosis_type)]
    )
    reason_list = (
        reasons
        if reasons is not None
        else [
            make_reason(
                statement=f"Warrant for {diagnosis_type.value.replace('_', ' ')}"
            )
        ]
    )
    # Soft-only types: keep severity moderate and confidence medium by default
    # so consistency policy soft_support rule does not fire unexpectedly.
    default_severity = severity
    default_confidence = confidence
    if diagnosis_type in {
        DiagnosisType.LOW_CONFIDENCE,
        DiagnosisType.FALSE_CONFIDENCE,
    }:
        if default_severity is None:
            default_severity = make_severity(DiagnosisSeverityLevel.MODERATE)
        if default_confidence is None:
            default_confidence = make_confidence(ConfidenceLevel.MEDIUM)
    return EducationalDiagnosis.create(
        diagnosis_id=DiagnosisId(diagnosis_id),
        student_id=student_id,
        diagnosis_type=diagnosis_type,
        scope=scope or make_scope(),
        confidence=default_confidence or make_confidence(),
        severity=default_severity or make_severity(),
        indicators=indicator_list,
        reasons=reason_list,
        known_evidence_ids=known_evidence,
        known_interpretation_ids=known_interpretations,
        interpretation_references=interpretation_references,
    )

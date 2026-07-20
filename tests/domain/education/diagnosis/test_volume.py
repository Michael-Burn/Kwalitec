"""High-volume matrices exercising Educational Diagnosis domain surface area."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisConsistencyPolicy,
    DiagnosisIsActionableSpecification,
    DiagnosisIsSupportedSpecification,
    DiagnosisSeverityLevel,
    DiagnosisStatus,
    DiagnosisValidationPolicy,
    EducationalScopeKind,
    IndicatorKind,
)
from domain.education.foundation.enums import (
    ConfidenceLevel,
    DiagnosisType,
    LearningDimension,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, EvidenceId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from tests.domain.education.diagnosis.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    EPISODE_002,
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
    INTERP_001,
    INTERP_002,
    INTERP_003,
    KNOWN_EVIDENCE,
    KNOWN_INTERPRETATIONS,
    PRIMARY_INDICATOR_FOR_TYPE,
    make_confidence,
    make_diagnosis,
    make_indicator,
    make_reason,
    make_scope,
    make_severity,
)

DIAGNOSIS_TYPES = list(DiagnosisType)
SCOPE_KINDS = list(EducationalScopeKind)
CONFIDENCE_LEVELS = [
    ConfidenceLevel.VERY_LOW,
    ConfidenceLevel.LOW,
    ConfidenceLevel.MEDIUM,
    ConfidenceLevel.HIGH,
    ConfidenceLevel.VERY_HIGH,
]
SEVERITY_LEVELS = list(DiagnosisSeverityLevel)
DIMENSIONS = list(LearningDimension)
STUDENTS = tuple(f"student-{i}" for i in range(1, 8))
SECONDARY_INDICATOR: dict[DiagnosisType, IndicatorKind] = {
    DiagnosisType.CONCEPTUAL_MISUNDERSTANDING: IndicatorKind.PARTIAL_FACET_GRASP,
    DiagnosisType.PROCEDURAL_WEAKNESS: IndicatorKind.TASK_APPLICATION_FAILURE,
    DiagnosisType.WEAK_RETENTION: IndicatorKind.CONFLICTING_SIGNAL,
    DiagnosisType.KNOWLEDGE_FRAGMENTATION: IndicatorKind.VARIANT_TRANSFER_FAILURE,
    DiagnosisType.PREREQUISITE_GAP: IndicatorKind.FRAGILE_EXPLANATION,
    DiagnosisType.MISCONCEPTION: IndicatorKind.PATTERNED_ERROR,
    DiagnosisType.LOW_CONFIDENCE: IndicatorKind.CONFLICTING_SIGNAL,
    DiagnosisType.FALSE_CONFIDENCE: IndicatorKind.CONFLICTING_SIGNAL,
    DiagnosisType.EXAM_TECHNIQUE_WEAKNESS: IndicatorKind.CONFLICTING_SIGNAL,
    DiagnosisType.APPLICATION_WEAKNESS: IndicatorKind.EXECUTION_FAILURE,
    DiagnosisType.TRANSFER_WEAKNESS: IndicatorKind.ISOLATED_LOCAL_SUCCESS,
    DiagnosisType.INCOMPLETE_UNDERSTANDING: IndicatorKind.FRAGILE_EXPLANATION,
}


def _default_confidence_for(diagnosis_type: DiagnosisType) -> ConfidenceLevel:
    if diagnosis_type in {
        DiagnosisType.LOW_CONFIDENCE,
        DiagnosisType.FALSE_CONFIDENCE,
    }:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.HIGH


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
@pytest.mark.parametrize("student", STUDENTS)
def test_create_per_type_and_student(
    diagnosis_type: DiagnosisType, student: str
) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-{diagnosis_type.value}-{student}",
        student_id=student,
        diagnosis_type=diagnosis_type,
        confidence=make_confidence(_default_confidence_for(diagnosis_type)),
    )
    assert diagnosis.student_id == student
    assert diagnosis.diagnosis_type is diagnosis_type
    assert DiagnosisIsSupportedSpecification().is_satisfied_by(diagnosis)
    assert DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis) or (
        diagnosis.confidence.level is ConfidenceLevel.VERY_LOW
    )


@pytest.mark.parametrize("level", CONFIDENCE_LEVELS)
@pytest.mark.parametrize("ratio", [None, 0.0, 0.25, 0.5, 0.75, 1.0])
def test_confidence_matrix(level: ConfidenceLevel, ratio: float | None) -> None:
    measure = make_confidence(level, ratio=ratio)
    assert measure.level is level
    assert measure.is_at_least(ConfidenceLevel.VERY_LOW)


@pytest.mark.parametrize("severity_level", SEVERITY_LEVELS)
@pytest.mark.parametrize("rationale", [None, "blocks progress", "local fragility"])
def test_severity_matrix(
    severity_level: DiagnosisSeverityLevel, rationale: str | None
) -> None:
    severity = make_severity(severity_level, rationale=rationale)
    assert severity.level is severity_level


@pytest.mark.parametrize("scope_kind", SCOPE_KINDS)
@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_scope_kind_and_dimension_matrix(
    scope_kind: EducationalScopeKind, dimension: LearningDimension
) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-{scope_kind.value}-{dimension.value}",
        scope=make_scope(
            scope_id=f"scope-{scope_kind.value}-{dimension.value}",
            statement=f"Scope {scope_kind.value} {dimension.value}",
            scope_kind=scope_kind,
            dimension=dimension,
        ),
    )
    assert diagnosis.scope.scope_kind is scope_kind
    assert diagnosis.scope.learning_dimension is dimension


@pytest.mark.parametrize("status_action", ["revise", "invalidate"])
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_mutation_matrix(status_action: str, student: str) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-mut-{status_action}-{student}",
        student_id=student,
    )
    diagnosis.pull_events()
    if status_action == "revise":
        diagnosis.revise(confidence=make_confidence(ConfidenceLevel.MEDIUM))
        assert diagnosis.is_revised()
    else:
        diagnosis.invalidate(f"void-{student}")
        assert diagnosis.is_invalidated()


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
def test_duplicate_indicator_rejected_per_type(diagnosis_type: DiagnosisType) -> None:
    kind = PRIMARY_INDICATOR_FOR_TYPE[diagnosis_type]
    with pytest.raises(EducationalInvariantViolation):
        make_diagnosis(
            diagnosis_type=diagnosis_type,
            indicators=[
                make_indicator(
                    indicator_id="a",
                    kind=kind,
                    diagnosis_type=diagnosis_type,
                    description=f"Dup {kind.value}",
                ),
                make_indicator(
                    indicator_id="b",
                    kind=kind,
                    diagnosis_type=diagnosis_type,
                    description=f"Dup {kind.value}",
                ),
            ],
            confidence=make_confidence(_default_confidence_for(diagnosis_type)),
        )


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
def test_consistency_policy_per_type(diagnosis_type: DiagnosisType) -> None:
    indicator = make_indicator(
        kind=PRIMARY_INDICATOR_FOR_TYPE[diagnosis_type],
        diagnosis_type=diagnosis_type,
        description=f"Consistent {diagnosis_type.value}",
    )
    DiagnosisConsistencyPolicy.assert_consistent(
        diagnosis_type,
        (indicator,),
        (make_reason(statement=f"Warrant for {diagnosis_type.value}"),),
        make_confidence(_default_confidence_for(diagnosis_type)),
        make_severity(DiagnosisSeverityLevel.MODERATE),
    )


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
def test_merge_support_distinct_per_type(diagnosis_type: DiagnosisType) -> None:
    primary = make_diagnosis(
        diagnosis_id=f"primary-{diagnosis_type.value}",
        diagnosis_type=diagnosis_type,
        confidence=make_confidence(_default_confidence_for(diagnosis_type)),
    )
    secondary_kind = SECONDARY_INDICATOR[diagnosis_type]
    other = make_diagnosis(
        diagnosis_id=f"other-{diagnosis_type.value}",
        diagnosis_type=diagnosis_type,
        indicators=[
            make_indicator(
                indicator_id=f"ind-sec-{diagnosis_type.value}",
                kind=secondary_kind,
                description=f"Secondary {secondary_kind.value}",
                interpretation_ids=(INTERP_002,),
                evidence_ids=(EVIDENCE_003,),
            )
        ],
        reasons=[
            make_reason(
                reason_id=f"r-sec-{diagnosis_type.value}",
                statement=f"Secondary warrant for {diagnosis_type.value}",
                code=f"sec-{diagnosis_type.value}",
            )
        ],
        confidence=make_confidence(_default_confidence_for(diagnosis_type)),
    )
    primary.merge_support(other)
    assert primary.indicator_count() == 2
    assert primary.reason_count() == 2


@pytest.mark.parametrize("i", range(24))
def test_merge_support_volume(i: int) -> None:
    primary = make_diagnosis(diagnosis_id=f"primary-vol-{i}")
    other = make_diagnosis(
        diagnosis_id=f"other-vol-{i}",
        indicators=[
            make_indicator(
                indicator_id=f"ind-vol-{i}",
                kind=IndicatorKind.PARTIAL_FACET_GRASP,
                description=f"Distinct facet signal {i}",
                interpretation_ids=(INTERP_002,),
                evidence_ids=(EVIDENCE_003,),
            )
        ],
        reasons=[
            make_reason(
                reason_id=f"r-vol-{i}",
                statement=f"Distinct educational warrant {i}",
                code=f"vol-{i}",
            )
        ],
    )
    primary.merge_support(other)
    assert primary.is_revised()


@pytest.mark.parametrize("evidence_value", [e.value for e in KNOWN_EVIDENCE])
def test_known_evidence_matrix(evidence_value: str) -> None:
    evidence_id = EvidenceId(evidence_value)
    DiagnosisValidationPolicy.assert_known_evidence(KNOWN_EVIDENCE, {evidence_id})
    if evidence_id == EVIDENCE_001:
        ids = (EVIDENCE_001, EVIDENCE_002)
    else:
        ids = (EVIDENCE_001, evidence_id)
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-ev-{evidence_value}",
        indicators=[
            make_indicator(
                description=f"Evidence involvement of {evidence_value}",
                evidence_ids=ids,
            )
        ],
    )
    assert diagnosis.has_evidence(evidence_id)


@pytest.mark.parametrize("interp_id", sorted(KNOWN_INTERPRETATIONS))
def test_known_interpretation_matrix(interp_id: str) -> None:
    DiagnosisValidationPolicy.assert_known_interpretations(
        KNOWN_INTERPRETATIONS, {interp_id}
    )
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-interp-{interp_id}",
        indicators=[
            make_indicator(
                interpretation_ids=(interp_id,),
                description=f"Warrant from {interp_id}",
            )
        ],
    )
    assert diagnosis.has_interpretation(interp_id)


@pytest.mark.parametrize("status", list(DiagnosisStatus))
def test_status_enum_values(status: DiagnosisStatus) -> None:
    assert isinstance(status.value, str)
    assert DiagnosisValidationPolicy.assert_status(status) is status


@pytest.mark.parametrize(
    "pair",
    [
        (CONCEPT_SELECT, EPISODE_001),
        (CONCEPT_SELECT, EPISODE_002),
        (CONCEPT_ULTIMATE, EPISODE_001),
        (CONCEPT_ULTIMATE, EPISODE_002),
    ],
)
@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES[:6])
def test_concept_episode_type_matrix(
    pair: tuple[ConceptId, LearningEpisodeId], diagnosis_type: DiagnosisType
) -> None:
    concept_id, episode_id = pair
    diagnosis = make_diagnosis(
        diagnosis_id=f"i-{concept_id.value}-{episode_id.value}-{diagnosis_type.value}",
        diagnosis_type=diagnosis_type,
        scope=make_scope(
            scope_id=f"s-{concept_id.value}-{episode_id.value}-{diagnosis_type.value}",
            statement=f"Scope for {concept_id.value} {episode_id.value}",
            concepts=(ConceptReference(concept_id=concept_id),),
            episodes=(episode_id,),
        ),
        confidence=make_confidence(_default_confidence_for(diagnosis_type)),
    )
    assert concept_id in diagnosis.scope.concept_ids()
    assert episode_id in diagnosis.scope.episode_ids()


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
@pytest.mark.parametrize("severity_level", SEVERITY_LEVELS)
def test_type_severity_matrix(
    diagnosis_type: DiagnosisType, severity_level: DiagnosisSeverityLevel
) -> None:
    # Soft types + SEVERE + HIGH confidence are inconsistent; keep medium.
    confidence = make_confidence(_default_confidence_for(diagnosis_type))
    if diagnosis_type in {
        DiagnosisType.LOW_CONFIDENCE,
        DiagnosisType.FALSE_CONFIDENCE,
    } and severity_level is DiagnosisSeverityLevel.SEVERE:
        confidence = make_confidence(ConfidenceLevel.MEDIUM)
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-{diagnosis_type.value}-{severity_level.value}",
        diagnosis_type=diagnosis_type,
        severity=make_severity(severity_level),
        confidence=confidence,
    )
    assert diagnosis.severity.level is severity_level


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
@pytest.mark.parametrize(
    "level",
    [ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH],
)
def test_type_confidence_actionability_matrix(
    diagnosis_type: DiagnosisType, level: ConfidenceLevel
) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-act-{diagnosis_type.value}-{level.value}",
        diagnosis_type=diagnosis_type,
        confidence=make_confidence(level),
        severity=make_severity(DiagnosisSeverityLevel.MODERATE),
    )
    assert DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis)


@pytest.mark.parametrize("kind", list(IndicatorKind))
def test_indicator_kind_enum(kind: IndicatorKind) -> None:
    assert isinstance(kind.value, str)


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
def test_compatible_kinds_non_empty(diagnosis_type: DiagnosisType) -> None:
    kinds = DiagnosisConsistencyPolicy.compatible_indicator_kinds(diagnosis_type)
    assert PRIMARY_INDICATOR_FOR_TYPE[diagnosis_type] in kinds
    assert len(kinds) >= 1


@pytest.mark.parametrize("i", range(16))
def test_revise_volume(i: int) -> None:
    diagnosis = make_diagnosis(diagnosis_id=f"diag-rev-{i}")
    diagnosis.revise(
        confidence=make_confidence(ConfidenceLevel.MEDIUM, ratio=0.1 * (i % 10)),
        reasons=[
            make_reason(
                reason_id=f"r-rev-{i}",
                statement=f"Revised educational warrant number {i}",
            )
        ],
    )
    assert diagnosis.is_revised()


@pytest.mark.parametrize(
    "interp_pair",
    [
        (INTERP_001, INTERP_002),
        (INTERP_001, INTERP_003),
        (INTERP_002, INTERP_003),
    ],
)
@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES[:4])
def test_multi_interpretation_support(
    interp_pair: tuple[str, str], diagnosis_type: DiagnosisType
) -> None:
    a, b = interp_pair
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-mi-{a}-{b}-{diagnosis_type.value}",
        diagnosis_type=diagnosis_type,
        indicators=[
            make_indicator(
                interpretation_ids=(a, b),
                kind=PRIMARY_INDICATOR_FOR_TYPE[diagnosis_type],
                description=f"Joint warrant {a} {b}",
            )
        ],
        confidence=make_confidence(_default_confidence_for(diagnosis_type)),
    )
    assert diagnosis.has_interpretation(a)
    assert diagnosis.has_interpretation(b)

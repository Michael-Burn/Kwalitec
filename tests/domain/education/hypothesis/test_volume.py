"""High-volume matrices exercising Educational Hypothesis domain surface area."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId
from domain.education.hypothesis import (
    DiagnosisReference,
    ExplanatoryStrengthLevel,
    HypothesisIsRevisableSpecification,
    HypothesisIsSupportedSpecification,
    HypothesisKind,
    HypothesisRevisionPolicy,
    HypothesisScopeKind,
    HypothesisStatus,
    HypothesisValidationPolicy,
    InterpretationReference,
    Plausibility,
    PlausibilityLevel,
    RevisionForm,
)
from tests.domain.education.hypothesis.conftest import (
    EVIDENCE_001,
    EVIDENCE_002,
    EVIDENCE_003,
    INTERP_001,
    INTERP_002,
    INTERP_003,
    PRIMARY_DIAGNOSIS_FOR_KIND,
    make_competitor,
    make_hypothesis,
    make_plausibility,
    make_reason,
    make_scope,
    make_strength,
)

HYPOTHESIS_KINDS = list(HypothesisKind)
SCOPE_KINDS = list(HypothesisScopeKind)
PLAUSIBILITY_LEVELS = list(PlausibilityLevel)
STRENGTH_LEVELS = list(ExplanatoryStrengthLevel)
DIMENSIONS = list(LearningDimension)
REVISION_FORMS = list(RevisionForm)
STUDENTS = tuple(f"student-{i}" for i in range(1, 9))
RATIOS = (None, 0.0, 0.25, 0.5, 0.75, 1.0)
INTERP_PAIRS = (
    (INTERP_001,),
    (INTERP_001, INTERP_002),
    (INTERP_001, INTERP_002, INTERP_003),
)
EVIDENCE_PAIRS = (
    (EVIDENCE_001,),
    (EVIDENCE_001, EVIDENCE_002),
    (EVIDENCE_001, EVIDENCE_002, EVIDENCE_003),
)

# Secondary compatible diagnosis where available.
SECONDARY_DIAGNOSIS: dict[HypothesisKind, DiagnosisType] = {
    HypothesisKind.PREREQUISITE_DEFICIENCY: DiagnosisType.INCOMPLETE_UNDERSTANDING,
    HypothesisKind.REPRESENTATION_MISMATCH: DiagnosisType.INCOMPLETE_UNDERSTANDING,
    HypothesisKind.WEAK_ABSTRACTION: DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
    HypothesisKind.SURFACE_MEMORISATION: DiagnosisType.TRANSFER_WEAKNESS,
    HypothesisKind.PROCEDURAL_FIXATION: DiagnosisType.APPLICATION_WEAKNESS,
    HypothesisKind.TRANSFER_LIMITATION: DiagnosisType.APPLICATION_WEAKNESS,
    HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE: DiagnosisType.LOW_CONFIDENCE,
}

COMPETITOR_KIND: dict[HypothesisKind, HypothesisKind] = {
    HypothesisKind.PREREQUISITE_DEFICIENCY: HypothesisKind.TRANSFER_LIMITATION,
    HypothesisKind.REPRESENTATION_MISMATCH: HypothesisKind.WEAK_ABSTRACTION,
    HypothesisKind.WEAK_ABSTRACTION: HypothesisKind.SURFACE_MEMORISATION,
    HypothesisKind.SURFACE_MEMORISATION: HypothesisKind.PROCEDURAL_FIXATION,
    HypothesisKind.PROCEDURAL_FIXATION: HypothesisKind.TRANSFER_LIMITATION,
    HypothesisKind.TRANSFER_LIMITATION: HypothesisKind.PREREQUISITE_DEFICIENCY,
    HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE: HypothesisKind.SURFACE_MEMORISATION,
}


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_propose_per_kind_and_student(
    hypothesis_kind: HypothesisKind, student: str
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-{hypothesis_kind.value}-{student}",
        student_id=student,
        hypothesis_kind=hypothesis_kind,
    )
    assert hypothesis.student_id == student
    assert hypothesis.hypothesis_kind is hypothesis_kind
    assert HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)
    assert HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)


@pytest.mark.parametrize("level", PLAUSIBILITY_LEVELS)
@pytest.mark.parametrize("ratio", RATIOS)
def test_plausibility_matrix(
    level: PlausibilityLevel, ratio: float | None
) -> None:
    measure = make_plausibility(level, ratio=ratio)
    assert measure.level is level
    if level is not PlausibilityLevel.SUSPENDED:
        assert measure.is_at_least(PlausibilityLevel.TENTATIVE) or (
            level is PlausibilityLevel.TENTATIVE
        )


@pytest.mark.parametrize("strength_level", STRENGTH_LEVELS)
def test_strength_matrix(strength_level: ExplanatoryStrengthLevel) -> None:
    strength = make_strength(strength_level)
    assert strength.level is strength_level


@pytest.mark.parametrize("scope_kind", SCOPE_KINDS)
@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_scope_kind_and_dimension_matrix(
    scope_kind: HypothesisScopeKind, dimension: LearningDimension
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-{scope_kind.value}-{dimension.value}",
        scope=make_scope(
            scope_id=f"scope-{scope_kind.value}-{dimension.value}",
            statement=f"Scope {scope_kind.value} {dimension.value}",
            scope_kind=scope_kind,
            dimension=dimension,
        ),
    )
    assert hypothesis.scope.scope_kind is scope_kind
    assert hypothesis.scope.learning_dimension is dimension


@pytest.mark.parametrize("status_action", ["revise", "strengthen", "weaken", "discard"])
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_mutation_matrix(status_action: str, student: str) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-mut-{status_action}-{student}",
        student_id=student,
        explanatory_strength=make_strength(ExplanatoryStrengthLevel.MODERATE),
        plausibility=make_plausibility(PlausibilityLevel.WORKING),
    )
    hypothesis.pull_events()
    if status_action == "revise":
        hypothesis.revise(explanation=f"Revised for {student}")
        assert hypothesis.is_revised()
    elif status_action == "strengthen":
        hypothesis.strengthen()
        assert hypothesis.explanatory_strength.level is ExplanatoryStrengthLevel.STRONG
    elif status_action == "weaken":
        hypothesis.weaken()
        assert hypothesis.explanatory_strength.level is ExplanatoryStrengthLevel.WEAK
    else:
        hypothesis.discard(f"void-{student}")
        assert hypothesis.is_discarded()


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("revision_form", REVISION_FORMS)
def test_revision_form_matrix(
    hypothesis_kind: HypothesisKind, revision_form: RevisionForm
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-rev-{hypothesis_kind.value}-{revision_form.value}",
        hypothesis_kind=hypothesis_kind,
    )
    hypothesis.revise(
        explanation=f"Revised ({revision_form.value}) for {hypothesis_kind.value}",
        revision_form=revision_form,
    )
    assert hypothesis.is_revised()


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_competitor_matrix(hypothesis_kind: HypothesisKind, student: str) -> None:
    competitor_kind = COMPETITOR_KIND[hypothesis_kind]
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-comp-{hypothesis_kind.value}-{student}",
        student_id=student,
        hypothesis_kind=hypothesis_kind,
        competing_hypotheses=[
            make_competitor(
                competing_id=f"comp-{hypothesis_kind.value}-{student}",
                hypothesis_kind=competitor_kind,
                explanation=(
                    f"Competing {competitor_kind.value} reading for {student}"
                ),
            )
        ],
    )
    assert hypothesis.competitor_count() == 1
    assert HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("interp_pair", INTERP_PAIRS)
def test_multi_interpretation_support(
    hypothesis_kind: HypothesisKind, interp_pair: tuple[str, ...]
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-interp-{hypothesis_kind.value}-{len(interp_pair)}",
        hypothesis_kind=hypothesis_kind,
        interpretation_references=[
            InterpretationReference(interpretation_id=i) for i in interp_pair
        ],
    )
    assert len(hypothesis.supporting_interpretation_ids()) == len(interp_pair)


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("evidence_pair", EVIDENCE_PAIRS)
def test_multi_evidence_support(
    hypothesis_kind: HypothesisKind, evidence_pair: tuple[EvidenceId, ...]
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-ev-{hypothesis_kind.value}-{len(evidence_pair)}",
        hypothesis_kind=hypothesis_kind,
        evidence_ids=list(evidence_pair),
        reasons=[make_reason(evidence_ids=())],
    )
    for evidence_id in evidence_pair:
        assert hypothesis.has_evidence(evidence_id)


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("use_secondary", [False, True])
def test_diagnosis_compatibility_matrix(
    hypothesis_kind: HypothesisKind, use_secondary: bool
) -> None:
    diagnosis_type = (
        SECONDARY_DIAGNOSIS[hypothesis_kind]
        if use_secondary
        else PRIMARY_DIAGNOSIS_FOR_KIND[hypothesis_kind]
    )
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-diag-{hypothesis_kind.value}-{use_secondary}",
        hypothesis_kind=hypothesis_kind,
        diagnosis_references=[
            DiagnosisReference(
                diagnosis_id=DiagnosisId(
                    f"diag-{hypothesis_kind.value}-{use_secondary}"
                ),
                diagnosis_type=diagnosis_type,
            )
        ],
    )
    assert hypothesis.primary_diagnosis_type() is diagnosis_type


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("plausibility_level", [
    PlausibilityLevel.TENTATIVE,
    PlausibilityLevel.WORKING,
    PlausibilityLevel.STRONG,
])
@pytest.mark.parametrize("strength_level", [
    ExplanatoryStrengthLevel.WEAK,
    ExplanatoryStrengthLevel.MODERATE,
    ExplanatoryStrengthLevel.STRONG,
])
def test_kind_plausibility_strength_matrix(
    hypothesis_kind: HypothesisKind,
    plausibility_level: PlausibilityLevel,
    strength_level: ExplanatoryStrengthLevel,
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=(
            f"hyp-kps-{hypothesis_kind.value}-"
            f"{plausibility_level.value}-{strength_level.value}"
        ),
        hypothesis_kind=hypothesis_kind,
        plausibility=make_plausibility(plausibility_level),
        explanatory_strength=make_strength(strength_level),
    )
    assert hypothesis.plausibility.level is plausibility_level
    assert hypothesis.explanatory_strength.level is strength_level
    assert HypothesisIsSupportedSpecification().is_satisfied_by(hypothesis)


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:3])
def test_discard_then_strengthen_rejected(
    hypothesis_kind: HypothesisKind, student: str
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-disc-{hypothesis_kind.value}-{student}",
        student_id=student,
        hypothesis_kind=hypothesis_kind,
    )
    hypothesis.discard(f"retired-{student}")
    with pytest.raises(EducationalInvariantViolation):
        hypothesis.strengthen()
    assert not HypothesisIsRevisableSpecification().is_satisfied_by(hypothesis)


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
def test_compatible_catalogue_covers_kind(hypothesis_kind: HypothesisKind) -> None:
    compatible = HypothesisValidationPolicy.compatible_diagnosis_types(
        hypothesis_kind
    )
    primary = PRIMARY_DIAGNOSIS_FOR_KIND[hypothesis_kind]
    assert primary in compatible


@pytest.mark.parametrize("status", list(HypothesisStatus))
def test_revision_policy_status_matrix(status: HypothesisStatus) -> None:
    if status is HypothesisStatus.DISCARDED:
        with pytest.raises(EducationalInvariantViolation):
            HypothesisRevisionPolicy.assert_revisable(status, action="revise")
    else:
        HypothesisRevisionPolicy.assert_revisable(status, action="revise")


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_add_competitor_then_revise(
    hypothesis_kind: HypothesisKind, student: str
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-addc-{hypothesis_kind.value}-{student}",
        student_id=student,
        hypothesis_kind=hypothesis_kind,
    )
    competitor_kind = COMPETITOR_KIND[hypothesis_kind]
    hypothesis.add_competing_hypothesis(
        make_competitor(
            competing_id=f"late-{hypothesis_kind.value}-{student}",
            hypothesis_kind=competitor_kind,
            explanation=f"Late competing {competitor_kind.value} for {student}",
        )
    )
    hypothesis.revise(explanation=f"Still revisable after competitor for {student}")
    assert hypothesis.competitor_count() == 1
    assert hypothesis.is_revised()


@pytest.mark.parametrize("scope_kind", SCOPE_KINDS)
@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS[:4])
def test_scope_and_kind_matrix(
    scope_kind: HypothesisScopeKind, hypothesis_kind: HypothesisKind
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-sk-{scope_kind.value}-{hypothesis_kind.value}",
        hypothesis_kind=hypothesis_kind,
        scope=make_scope(
            scope_id=f"s-{scope_kind.value}-{hypothesis_kind.value}",
            statement=f"{scope_kind.value} scope for {hypothesis_kind.value}",
            scope_kind=scope_kind,
        ),
    )
    assert hypothesis.scope.scope_kind is scope_kind


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
@pytest.mark.parametrize("ratio", RATIOS[:4])
def test_working_plausibility_ratios(
    hypothesis_kind: HypothesisKind, ratio: float | None
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-ratio-{hypothesis_kind.value}-{ratio}",
        hypothesis_kind=hypothesis_kind,
        plausibility=make_plausibility(PlausibilityLevel.WORKING, ratio=ratio),
    )
    assert hypothesis.plausibility.level is PlausibilityLevel.WORKING


@pytest.mark.parametrize("from_level", [
    ExplanatoryStrengthLevel.WEAK,
    ExplanatoryStrengthLevel.MODERATE,
    ExplanatoryStrengthLevel.STRONG,
])
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_strengthen_from_levels(
    from_level: ExplanatoryStrengthLevel, student: str
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-str-{from_level.value}-{student}",
        student_id=student,
        explanatory_strength=make_strength(from_level),
        plausibility=make_plausibility(PlausibilityLevel.TENTATIVE),
    )
    hypothesis.strengthen()
    assert hypothesis.explanatory_strength.at_least(make_strength(from_level))


@pytest.mark.parametrize("from_level", [
    ExplanatoryStrengthLevel.MODERATE,
    ExplanatoryStrengthLevel.STRONG,
    ExplanatoryStrengthLevel.COMPELLING,
])
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_weaken_from_levels(
    from_level: ExplanatoryStrengthLevel, student: str
) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-wk-{from_level.value}-{student}",
        student_id=student,
        explanatory_strength=make_strength(from_level),
        plausibility=make_plausibility(PlausibilityLevel.STRONG),
    )
    hypothesis.weaken()
    assert not hypothesis.explanatory_strength.at_least(make_strength(from_level))


@pytest.mark.parametrize("hypothesis_kind", HYPOTHESIS_KINDS)
def test_suspend_then_resume(hypothesis_kind: HypothesisKind) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-sus-{hypothesis_kind.value}",
        hypothesis_kind=hypothesis_kind,
    )
    hypothesis.revise(plausibility=Plausibility.suspended())
    assert hypothesis.is_suspended()
    hypothesis.revise(plausibility=Plausibility.working())
    assert hypothesis.is_revised()
    assert not hypothesis.plausibility.is_suspended()

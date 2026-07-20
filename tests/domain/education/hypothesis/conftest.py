"""Shared factories for Educational Hypothesis domain tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.ids import (
    ConceptId,
    DiagnosisId,
    EvidenceId,
    HypothesisId,
    LearningEpisodeId,
    LearningObjectiveId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.hypothesis import (
    CompetingHypothesis,
    CompetingHypothesisId,
    DiagnosisReference,
    EducationalHypothesis,
    ExplanatoryStrength,
    ExplanatoryStrengthLevel,
    HypothesisKind,
    HypothesisReason,
    HypothesisReasonId,
    HypothesisScope,
    HypothesisScopeId,
    HypothesisScopeKind,
    InterpretationReference,
    Plausibility,
    PlausibilityLevel,
)

CONCEPT_SELECT = ConceptId("concept-select-mortality")
CONCEPT_ULTIMATE = ConceptId("concept-ultimate-mortality")
EPISODE_001 = LearningEpisodeId("episode-001")
EPISODE_002 = LearningEpisodeId("episode-002")
EVIDENCE_001 = EvidenceId("evidence-001")
EVIDENCE_002 = EvidenceId("evidence-002")
EVIDENCE_003 = EvidenceId("evidence-003")
DIAG_001 = DiagnosisId("diag-001")
DIAG_002 = DiagnosisId("diag-002")
INTERP_001 = "interp-001"
INTERP_002 = "interp-002"
INTERP_003 = "interp-003"
KNOWN_EVIDENCE = frozenset({EVIDENCE_001, EVIDENCE_002, EVIDENCE_003})
KNOWN_INTERPRETATIONS = frozenset({INTERP_001, INTERP_002, INTERP_003})

# Primary compatible diagnosis type per explanation family.
PRIMARY_DIAGNOSIS_FOR_KIND: dict[HypothesisKind, DiagnosisType] = {
    HypothesisKind.PREREQUISITE_DEFICIENCY: DiagnosisType.PREREQUISITE_GAP,
    HypothesisKind.REPRESENTATION_MISMATCH: DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
    HypothesisKind.WEAK_ABSTRACTION: DiagnosisType.INCOMPLETE_UNDERSTANDING,
    HypothesisKind.SURFACE_MEMORISATION: DiagnosisType.WEAK_RETENTION,
    HypothesisKind.PROCEDURAL_FIXATION: DiagnosisType.PROCEDURAL_WEAKNESS,
    HypothesisKind.TRANSFER_LIMITATION: DiagnosisType.TRANSFER_WEAKNESS,
    HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE: DiagnosisType.FALSE_CONFIDENCE,
}

DEFAULT_KIND = HypothesisKind.PREREQUISITE_DEFICIENCY

EXPLANATIONS: dict[HypothesisKind, str] = {
    HypothesisKind.PREREQUISITE_DEFICIENCY: (
        "GLM struggle arises because exponential-family intuition is missing"
    ),
    HypothesisKind.REPRESENTATION_MISMATCH: (
        "Errors arise from mismatch between symbolic GLM notation and verbal meaning"
    ),
    HypothesisKind.WEAK_ABSTRACTION: (
        "Student holds surface procedures without abstracting the family structure"
    ),
    HypothesisKind.SURFACE_MEMORISATION: (
        "Success on textbook clones reflects memorisation rather than "
        "transferable grasp"
    ),
    HypothesisKind.PROCEDURAL_FIXATION: (
        "Student fixes on one surplus-distribution procedure and cannot adapt steps"
    ),
    HypothesisKind.TRANSFER_LIMITATION: (
        "Knowledge is present only on drilled stems and fails under variant wording"
    ),
    HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE: (
        "False confidence comes from success on clones without varied stems"
    ),
}


@pytest.fixture
def hypothesis_id() -> HypothesisId:
    return HypothesisId("hyp-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_plausibility(
    level: PlausibilityLevel = PlausibilityLevel.WORKING,
    *,
    ratio: float | None = 0.6,
) -> Plausibility:
    return Plausibility.of(level, ratio=ratio)


def make_strength(
    level: ExplanatoryStrengthLevel = ExplanatoryStrengthLevel.MODERATE,
) -> ExplanatoryStrength:
    return ExplanatoryStrength.of(level)


def make_scope(
    *,
    scope_id: str = "scope-001",
    statement: str = (
        "Relative to GLM objective, explanation applies to prerequisite chain"
    ),
    scope_kind: HypothesisScopeKind = HypothesisScopeKind.PREREQUISITE_CHAIN,
    dimension: LearningDimension | None = LearningDimension.UNDERSTANDING,
    concepts: tuple[ConceptReference, ...] | None = None,
    objectives: tuple[LearningObjectiveReference, ...] | None = None,
    episodes: tuple[LearningEpisodeId, ...] | None = None,
) -> HypothesisScope:
    return HypothesisScope(
        scope_id=HypothesisScopeId(scope_id),
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
                objective_id=LearningObjectiveId("lo-glm-exp-family"),
                label="Build exponential-family intuition for GLMs",
            ),
        ),
        learning_episode_ids=episodes if episodes is not None else (EPISODE_001,),
    )


def make_reason(
    *,
    reason_id: str = "reason-001",
    statement: str = (
        "Upstream probes fail while downstream GLM items collapse similarly"
    ),
    code: str | None = "upstream_predicts_downstream",
    evidence_ids: tuple[EvidenceId, ...] | None = None,
) -> HypothesisReason:
    return HypothesisReason(
        reason_id=HypothesisReasonId(reason_id),
        statement=statement,
        code=code,
        evidence_ids=evidence_ids if evidence_ids is not None else (EVIDENCE_001,),
    )


def make_diagnosis_ref(
    *,
    diagnosis_id: str = "diag-001",
    diagnosis_type: DiagnosisType | None = None,
    hypothesis_kind: HypothesisKind = DEFAULT_KIND,
) -> DiagnosisReference:
    return DiagnosisReference(
        diagnosis_id=DiagnosisId(diagnosis_id),
        diagnosis_type=diagnosis_type
        if diagnosis_type is not None
        else PRIMARY_DIAGNOSIS_FOR_KIND[hypothesis_kind],
    )


def make_competitor(
    *,
    competing_id: str = "comp-001",
    hypothesis_kind: HypothesisKind = HypothesisKind.TRANSFER_LIMITATION,
    explanation: str | None = None,
    plausibility: Plausibility | None = None,
) -> CompetingHypothesis:
    return CompetingHypothesis(
        competing_id=CompetingHypothesisId(competing_id),
        hypothesis_kind=hypothesis_kind,
        explanation=explanation
        or EXPLANATIONS.get(
            hypothesis_kind,
            "Alternative reading of the same evidence pattern",
        ),
        plausibility=plausibility,
    )


def make_hypothesis(
    *,
    hypothesis_id: str = "hyp-001",
    student_id: str = "student-ada",
    hypothesis_kind: HypothesisKind = DEFAULT_KIND,
    explanation: str | None = None,
    scope: HypothesisScope | None = None,
    plausibility: Plausibility | None = None,
    explanatory_strength: ExplanatoryStrength | None = None,
    diagnosis_references: list[DiagnosisReference] | None = None,
    reasons: list[HypothesisReason] | None = None,
    interpretation_references: list[InterpretationReference] | None = None,
    evidence_ids: list[EvidenceId] | None = None,
    competing_hypotheses: list[CompetingHypothesis] | None = None,
    known_evidence: frozenset[EvidenceId] | None = KNOWN_EVIDENCE,
    known_interpretations: frozenset[str] | None = KNOWN_INTERPRETATIONS,
) -> EducationalHypothesis:
    return EducationalHypothesis.propose(
        hypothesis_id=HypothesisId(hypothesis_id),
        student_id=student_id,
        hypothesis_kind=hypothesis_kind,
        explanation=explanation or EXPLANATIONS[hypothesis_kind],
        scope=scope or make_scope(),
        plausibility=plausibility or make_plausibility(),
        explanatory_strength=explanatory_strength or make_strength(),
        diagnosis_references=diagnosis_references
        if diagnosis_references is not None
        else [make_diagnosis_ref(hypothesis_kind=hypothesis_kind)],
        reasons=reasons
        if reasons is not None
        else [
            make_reason(
                statement=f"Warrant for {hypothesis_kind.value.replace('_', ' ')}"
            )
        ],
        interpretation_references=interpretation_references
        if interpretation_references is not None
        else [InterpretationReference(interpretation_id=INTERP_001)],
        evidence_ids=evidence_ids
        if evidence_ids is not None
        else [EVIDENCE_001, EVIDENCE_002],
        competing_hypotheses=competing_hypotheses,
        known_evidence_ids=known_evidence,
        known_interpretation_ids=known_interpretations,
    )

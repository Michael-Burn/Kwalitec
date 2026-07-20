"""High-volume matrices exercising Educational Priority domain surface area."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningEpisodeId
from domain.education.foundation.references import ConceptReference
from domain.education.priority import (
    InstructionalImpactLevel,
    PriorityCalculationPolicy,
    PriorityConstraintKind,
    PriorityFactorKind,
    PriorityIsActionableSpecification,
    PriorityIsStableSpecification,
    PriorityRevisionKind,
    PriorityScopeKind,
    PriorityScoreBand,
    PriorityStatus,
    PriorityValidationPolicy,
    UrgencyLevel,
)
from tests.domain.education.priority.conftest import (
    CONCEPT_SELECT,
    CONCEPT_ULTIMATE,
    EPISODE_001,
    EPISODE_002,
    make_constraint,
    make_diagnosis_ref,
    make_factor,
    make_hypothesis_ref,
    make_impact,
    make_priority,
    make_scope,
    make_score,
    make_urgency,
)

FACTOR_KINDS = list(PriorityFactorKind)
SCOPE_KINDS = list(PriorityScopeKind)
SCORE_BANDS = list(PriorityScoreBand)
URGENCY_LEVELS = list(UrgencyLevel)
IMPACT_LEVELS = list(InstructionalImpactLevel)
DIMENSIONS = list(LearningDimension)
CONSTRAINT_KINDS = [
    PriorityConstraintKind.PROTECT_PREREQUISITE_OVER_EXTENSION,
    PriorityConstraintKind.PROTECT_MISCONCEPTION_OVER_PRACTICE,
    PriorityConstraintKind.PROTECT_UNDERSTANDING_OVER_SPEED,
    PriorityConstraintKind.PROTECT_DURABLE_LEARNING_OVER_THEATRE,
    PriorityConstraintKind.FORBID_ENGAGEMENT_ORDERING,
]
STUDENTS = tuple(f"student-{i}" for i in range(1, 9))
CONTRIBUTIONS = (0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0)
DIAGNOSIS_TYPES = list(DiagnosisType)


@pytest.mark.parametrize("kind", FACTOR_KINDS)
@pytest.mark.parametrize("student", STUDENTS)
def test_assign_per_factor_kind_and_student(
    kind: PriorityFactorKind, student: str
) -> None:
    priority = make_priority(
        priority_id=f"prio-{kind.value}-{student}",
        student_id=student,
        factors=[
            make_factor(
                factor_id=f"f-{kind.value}-{student}",
                kind=kind,
                contribution=0.8,
            )
        ],
    )
    assert priority.student_id == student
    assert priority.has_factor_kind(kind)
    assert PriorityIsActionableSpecification().is_satisfied_by(priority) or (
        priority.score.band is PriorityScoreBand.NEGLIGIBLE
    )


@pytest.mark.parametrize("kind", FACTOR_KINDS)
@pytest.mark.parametrize("contribution", CONTRIBUTIONS)
def test_calculation_matrix_per_kind_and_contribution(
    kind: PriorityFactorKind, contribution: float
) -> None:
    score, urgency, impact = PriorityCalculationPolicy.calculate(
        [
            make_factor(
                factor_id=f"f-{kind.value}-{contribution}",
                kind=kind,
                contribution=contribution,
            )
        ]
    )
    assert score.band in SCORE_BANDS
    assert urgency.level in URGENCY_LEVELS
    assert impact.level in IMPACT_LEVELS
    assert score.ratio is not None
    assert 0.0 <= score.ratio <= 1.0


@pytest.mark.parametrize("band", SCORE_BANDS)
@pytest.mark.parametrize("urgency_level", URGENCY_LEVELS)
def test_explicit_score_urgency_matrix(
    band: PriorityScoreBand, urgency_level: UrgencyLevel
) -> None:
    priority = make_priority(
        priority_id=f"prio-{band.value}-{urgency_level.value}",
        calculate=False,
        score=make_score(band, ratio=0.5),
        urgency=make_urgency(urgency_level),
        instructional_impact=make_impact(InstructionalImpactLevel.MATERIAL),
    )
    assert priority.score.band is band
    assert priority.urgency.level is urgency_level


@pytest.mark.parametrize("scope_kind", SCOPE_KINDS)
@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_scope_kind_and_dimension_matrix(
    scope_kind: PriorityScopeKind, dimension: LearningDimension
) -> None:
    priority = make_priority(
        priority_id=f"prio-{scope_kind.value}-{dimension.value}",
        scope=make_scope(
            scope_id=f"scope-{scope_kind.value}-{dimension.value}",
            statement=f"Scope {scope_kind.value} {dimension.value}",
            scope_kind=scope_kind,
            dimension=dimension,
        ),
    )
    assert priority.scope.scope_kind is scope_kind
    assert priority.scope.learning_dimension is dimension


@pytest.mark.parametrize("action", ["promote", "demote", "recalculate", "stabilise"])
@pytest.mark.parametrize("student", STUDENTS[:5])
def test_mutation_matrix(action: str, student: str) -> None:
    priority = make_priority(
        priority_id=f"prio-mut-{action}-{student}",
        student_id=student,
        calculate=False,
        score=make_score(PriorityScoreBand.MEDIUM, ratio=0.5),
        urgency=make_urgency(UrgencyLevel.ROUTINE),
    )
    priority.pull_events()
    if action == "promote":
        priority.promote()
        assert priority.is_revised()
    elif action == "demote":
        priority.demote()
        assert priority.is_revised()
    elif action == "recalculate":
        priority.recalculate()
        assert priority.is_revised()
    else:
        priority.stabilise(f"stable-{student}")
        assert priority.is_stabilised()


@pytest.mark.parametrize("kind", FACTOR_KINDS)
def test_duplicate_factor_rejected_per_kind(kind: PriorityFactorKind) -> None:
    with pytest.raises(EducationalInvariantViolation):
        make_priority(
            factors=[
                make_factor(factor_id="a", kind=kind, contribution=0.4),
                make_factor(factor_id="b", kind=kind, contribution=0.6),
            ]
        )


@pytest.mark.parametrize("kind", FACTOR_KINDS)
def test_gate_and_weight_per_kind(kind: PriorityFactorKind) -> None:
    factor = make_factor(kind=kind, contribution=0.5)
    gate = PriorityCalculationPolicy.gate_for(kind)
    weight = PriorityCalculationPolicy.factor_ordering_weight(factor)
    assert 1 <= gate <= 10
    assert 0.0 < weight <= 1.0


@pytest.mark.parametrize("constraint_kind", CONSTRAINT_KINDS)
@pytest.mark.parametrize("student", STUDENTS[:4])
def test_protective_constraints_with_lawful_factors(
    constraint_kind: PriorityConstraintKind, student: str
) -> None:
    priority = make_priority(
        priority_id=f"prio-c-{constraint_kind.value}-{student}",
        student_id=student,
        factors=[
            make_factor(
                kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                contribution=0.9,
            ),
            make_factor(
                factor_id="exam",
                kind=PriorityFactorKind.EXAM_RELEVANCE,
                contribution=0.2,
            ),
            make_factor(
                factor_id="misc",
                kind=PriorityFactorKind.MISCONCEPTION_PERSISTENCE,
                contribution=0.85,
            ),
            make_factor(
                factor_id="central",
                kind=PriorityFactorKind.CONCEPT_CENTRALITY,
                contribution=0.7,
            ),
            make_factor(
                factor_id="leverage",
                kind=PriorityFactorKind.EDUCATIONAL_LEVERAGE,
                contribution=0.65,
            ),
        ],
        constraints=[
            make_constraint(
                constraint_id=f"c-{constraint_kind.value}",
                kind=constraint_kind,
            )
        ],
    )
    assert priority.constraint_count() == 1
    assert PriorityIsActionableSpecification().is_satisfied_by(priority)


@pytest.mark.parametrize("i", range(24))
def test_recalculate_volume(i: int) -> None:
    priority = make_priority(priority_id=f"prio-recalc-{i}")
    priority.pull_events()
    priority.recalculate(
        factors=[
            make_factor(
                factor_id=f"f-recalc-{i}",
                kind=FACTOR_KINDS[i % len(FACTOR_KINDS)],
                contribution=0.2 + (i % 8) * 0.1,
            )
        ]
    )
    assert priority.is_revised()
    assert priority.pull_events()[0].revision_kind in {
        PriorityRevisionKind.RECALCULATED,
        PriorityRevisionKind.FACTORS_REPLACED,
    }


@pytest.mark.parametrize("i", range(16))
def test_promote_demote_roundtrip_volume(i: int) -> None:
    priority = make_priority(
        priority_id=f"prio-pd-{i}",
        calculate=False,
        score=make_score(PriorityScoreBand.MEDIUM, ratio=0.5),
        urgency=make_urgency(UrgencyLevel.ROUTINE),
    )
    priority.promote()
    priority.demote()
    assert priority.score.band is PriorityScoreBand.MEDIUM
    assert priority.urgency.level is UrgencyLevel.ROUTINE


@pytest.mark.parametrize("status", list(PriorityStatus))
def test_status_enum_values(status: PriorityStatus) -> None:
    assert isinstance(status.value, str)
    assert PriorityValidationPolicy.assert_status(status) is status


@pytest.mark.parametrize(
    "pair",
    [
        (CONCEPT_SELECT, EPISODE_001),
        (CONCEPT_SELECT, EPISODE_002),
        (CONCEPT_ULTIMATE, EPISODE_001),
        (CONCEPT_ULTIMATE, EPISODE_002),
    ],
)
@pytest.mark.parametrize("kind", FACTOR_KINDS[:6])
def test_concept_episode_factor_matrix(
    pair: tuple[ConceptId, LearningEpisodeId], kind: PriorityFactorKind
) -> None:
    concept_id, episode_id = pair
    priority = make_priority(
        priority_id=f"i-{concept_id.value}-{episode_id.value}-{kind.value}",
        scope=make_scope(
            scope_id=f"s-{concept_id.value}-{episode_id.value}-{kind.value}",
            statement=f"Scope for {concept_id.value} {episode_id.value}",
            concepts=(ConceptReference(concept_id=concept_id),),
            episodes=(episode_id,),
        ),
        factors=[
            make_factor(
                factor_id=f"f-{kind.value}-{episode_id.value}",
                kind=kind,
                contribution=0.7,
            )
        ],
    )
    assert concept_id in priority.scope.concept_ids()
    assert episode_id in priority.scope.episode_ids()


@pytest.mark.parametrize("kind", FACTOR_KINDS)
@pytest.mark.parametrize("band", SCORE_BANDS[:4])
def test_kind_band_matrix(kind: PriorityFactorKind, band: PriorityScoreBand) -> None:
    priority = make_priority(
        priority_id=f"prio-{kind.value}-{band.value}",
        calculate=False,
        factors=[make_factor(kind=kind, contribution=0.55)],
        score=make_score(band, ratio=0.45),
        urgency=make_urgency(UrgencyLevel.ROUTINE),
    )
    assert priority.score.band is band
    assert priority.has_factor_kind(kind)


@pytest.mark.parametrize("diagnosis_type", DIAGNOSIS_TYPES)
@pytest.mark.parametrize("kind", FACTOR_KINDS[:4])
def test_diagnosis_type_factor_matrix(
    diagnosis_type: DiagnosisType, kind: PriorityFactorKind
) -> None:
    priority = make_priority(
        priority_id=f"prio-{diagnosis_type.value}-{kind.value}",
        diagnosis_references=[
            make_diagnosis_ref(
                diagnosis_id=f"diag-{diagnosis_type.value}",
                diagnosis_type=diagnosis_type,
            )
        ],
        factors=[
            make_factor(
                factor_id=f"f-{kind.value}",
                kind=kind,
                contribution=0.75,
            )
        ],
    )
    assert priority.diagnosis_references[0].diagnosis_type is diagnosis_type


@pytest.mark.parametrize("impact_level", IMPACT_LEVELS)
@pytest.mark.parametrize("urgency_level", URGENCY_LEVELS[:3])
def test_impact_urgency_matrix(
    impact_level: InstructionalImpactLevel, urgency_level: UrgencyLevel
) -> None:
    priority = make_priority(
        priority_id=f"prio-{impact_level.value}-{urgency_level.value}",
        calculate=False,
        score=make_score(PriorityScoreBand.MEDIUM, ratio=0.5),
        urgency=make_urgency(urgency_level),
        instructional_impact=make_impact(
            impact_level, statement=f"Impact {impact_level.value}"
        ),
    )
    assert priority.instructional_impact.level is impact_level


@pytest.mark.parametrize("i", range(20))
def test_stabilise_and_reopen_volume(i: int) -> None:
    priority = make_priority(priority_id=f"prio-stable-{i}")
    priority.stabilise(f"commit-{i}")
    assert PriorityIsStableSpecification().is_satisfied_by(priority)
    priority.recalculate()
    assert not PriorityIsStableSpecification().is_satisfied_by(priority)


@pytest.mark.parametrize("kind", FACTOR_KINDS)
def test_peak_factor_matches_kind(kind: PriorityFactorKind) -> None:
    priority = make_priority(
        priority_id=f"prio-peak-{kind.value}",
        factors=[make_factor(kind=kind, contribution=0.8)],
    )
    assert priority.peak_factor().kind is kind


@pytest.mark.parametrize("student", STUDENTS)
def test_hypothesis_and_diagnosis_presence(student: str) -> None:
    priority = make_priority(
        priority_id=f"prio-refs-{student}",
        student_id=student,
        diagnosis_references=[
            make_diagnosis_ref(diagnosis_id=f"diag-{student}")
        ],
        hypothesis_references=[
            make_hypothesis_ref(hypothesis_id=f"hyp-{student}")
        ],
    )
    assert priority.diagnosis_count() == 1
    assert priority.hypothesis_count() == 1


@pytest.mark.parametrize(
    "ratio",
    [0.0, 0.14, 0.15, 0.34, 0.35, 0.54, 0.55, 0.74, 0.75, 1.0],
)
def test_band_threshold_edges(ratio: float) -> None:
    band = PriorityCalculationPolicy.band_for_ratio(ratio)
    assert band in SCORE_BANDS


@pytest.mark.parametrize("kind_a", FACTOR_KINDS)
@pytest.mark.parametrize("kind_b", FACTOR_KINDS)
def test_pairwise_distinct_factor_kinds_assignable(
    kind_a: PriorityFactorKind, kind_b: PriorityFactorKind
) -> None:
    if kind_a is kind_b:
        with pytest.raises(EducationalInvariantViolation):
            make_priority(
                priority_id=f"prio-pair-{kind_a.value}-dup",
                factors=[
                    make_factor(factor_id="a", kind=kind_a, contribution=0.5),
                    make_factor(factor_id="b", kind=kind_b, contribution=0.6),
                ],
            )
        return
    priority = make_priority(
        priority_id=f"prio-pair-{kind_a.value}-{kind_b.value}",
        factors=[
            make_factor(factor_id="a", kind=kind_a, contribution=0.55),
            make_factor(factor_id="b", kind=kind_b, contribution=0.45),
        ],
    )
    assert priority.factor_count() == 2
    assert priority.has_factor_kind(kind_a)
    assert priority.has_factor_kind(kind_b)

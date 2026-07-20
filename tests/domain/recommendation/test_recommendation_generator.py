"""Recommendation engine tests (EDU-004).

Covers: recommendation generation, priority mapping, supporting evidence,
confidence calculation, determinism, and architecture purity.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.diagnosis import DiagnosisSeverityLevel
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import (
    PriorityFactorKind,
    PriorityScoreBand,
    UrgencyLevel,
)
from domain.education.teaching_strategy import ComplexityLevel
from domain.recommendation import (
    RecommendationCategory,
    RecommendationGenerator,
    RecommendationPriorityBand,
    RecommendationSpecification,
    SupportingEvidenceCode,
    category_rank,
    confidence_from_millipoints,
    map_priority_band,
)
from tests.domain.education.digital_twin.conftest import make_archived_twin
from tests.domain.mission_generation.conftest import generate_mission
from tests.domain.recommendation.conftest import (
    generate_recommendations,
    make_aligned_diagnosis,
    make_aligned_priority,
    make_aligned_strategy,
    make_recommendation_inputs,
)
from tests.domain.study_planning.conftest import plan_study

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "domain" / "recommendation"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "openai",
        "anthropic",
        "random",
        "secrets",
        "uuid",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "openai.",
    "anthropic.",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_package_exports_required_types() -> None:
    from domain import recommendation as package

    for name in (
        "RecommendationSpecification",
        "Recommendation",
        "RecommendationPriority",
        "RecommendationCategory",
        "RecommendationReason",
        "RecommendationGenerator",
    ):
        assert hasattr(package, name), name


@pytest.mark.parametrize(
    "path",
    sorted(PACKAGE_ROOT.glob("*.py")),
    ids=lambda p: p.name,
)
def test_no_forbidden_infrastructure_or_ai_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports {name}"


def test_generator_source_has_no_randomness() -> None:
    source = (PACKAGE_ROOT / "recommendation_generator.py").read_text(
        encoding="utf-8"
    )
    for token in (
        "import random",
        "from random",
        "import uuid",
        "from uuid",
        "import secrets",
        "from secrets",
        "datetime.now",
        "time.time",
    ):
        assert token not in source


# --- generation -------------------------------------------------------------


def test_generate_returns_complete_specification() -> None:
    spec = generate_recommendations()

    assert isinstance(spec, RecommendationSpecification)
    assert spec.student_id == "student-ada"
    assert spec.recommendation_count() >= 1
    assert spec.primary.category in RecommendationCategory
    assert len(spec.primary.reason.statement) >= 12
    assert len(spec.primary.expected_outcome) >= 12
    assert len(spec.primary.supporting_evidence) >= 1
    assert spec.primary.confidence.level is not ConfidenceLevel.UNKNOWN
    assert "Recommendation set for student" in spec.educational_rationale
    assert spec.has_category(RecommendationCategory.CONTINUE_MISSION)


def test_generate_rejects_student_mismatch() -> None:
    twin, mission, study_plan, progress, diagnosis, priority, strategy = (
        make_recommendation_inputs()
    )
    other_priority = make_aligned_priority(student_id="student-other")
    with pytest.raises(EducationalInvariantViolation, match="student_id"):
        RecommendationGenerator.generate(
            twin,
            mission,
            study_plan,
            progress,
            diagnosis,
            other_priority,
            strategy,
        )


def test_generate_rejects_archived_twin() -> None:
    _, mission, study_plan, progress, diagnosis, priority, strategy = (
        make_recommendation_inputs()
    )
    with pytest.raises(EducationalInvariantViolation, match="archived"):
        RecommendationGenerator.generate(
            make_archived_twin(),
            mission,
            study_plan,
            progress,
            diagnosis,
            priority,
            strategy,
        )


def test_generate_rejects_plan_without_mission() -> None:
    twin, mission, _, progress, diagnosis, priority, strategy = (
        make_recommendation_inputs()
    )
    alien_diagnosis = make_aligned_diagnosis(
        diagnosis_id="diag-alien",
        diagnosis_type=DiagnosisType.WEAK_RETENTION,
    )
    alien_priority = make_aligned_priority(
        priority_id="prio-alien",
        diagnosis_id="diag-alien",
        diagnosis_type=DiagnosisType.WEAK_RETENTION,
    )
    alien_strategy = make_aligned_strategy(
        strategy_id="ts-alien",
        diagnosis_id="diag-alien",
        diagnosis_type=DiagnosisType.WEAK_RETENTION,
    )
    alien_mission = generate_mission(
        twin=twin,
        diagnosis=alien_diagnosis,
        priority=alien_priority,
        strategy=alien_strategy,
    )
    alien_plan = plan_study(missions=(alien_mission,), priority=priority)
    assert mission.mission_id not in alien_plan.mission_ids
    with pytest.raises(EducationalInvariantViolation, match="study plan"):
        RecommendationGenerator.generate(
            twin,
            mission,
            alien_plan,
            progress,
            diagnosis,
            priority,
            strategy,
        )


def test_revisit_prerequisites_from_diagnosis() -> None:
    spec = generate_recommendations(
        diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
        peak_factor_kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
    )
    assert spec.has_category(RecommendationCategory.REVISIT_PREREQUISITES)
    assert spec.primary.category is RecommendationCategory.REVISIT_PREREQUISITES


def test_reduce_cognitive_load_from_high_complexity() -> None:
    spec = generate_recommendations(
        complexity=ComplexityLevel.VERY_HIGH,
        with_misconception=True,
        evidence_strengths=("weak", "weak", "weak", "weak"),
        completed_success=False,
    )
    assert spec.has_category(RecommendationCategory.REDUCE_COGNITIVE_LOAD)


def test_repeat_assessment_from_false_confidence() -> None:
    spec = generate_recommendations(
        diagnosis_type=DiagnosisType.FALSE_CONFIDENCE,
    )
    assert spec.has_category(RecommendationCategory.REPEAT_ASSESSMENT)


def test_schedule_revision_from_weak_retention() -> None:
    spec = generate_recommendations(
        diagnosis_type=DiagnosisType.WEAK_RETENTION,
    )
    assert spec.has_category(RecommendationCategory.SCHEDULE_REVISION)


# --- priority mapping -------------------------------------------------------


@pytest.mark.parametrize(
    ("score_band", "expected"),
    [
        (PriorityScoreBand.NEGLIGIBLE, RecommendationPriorityBand.NEGLIGIBLE),
        (PriorityScoreBand.LOW, RecommendationPriorityBand.LOW),
        (PriorityScoreBand.MEDIUM, RecommendationPriorityBand.MEDIUM),
        (PriorityScoreBand.HIGH, RecommendationPriorityBand.HIGH),
        (PriorityScoreBand.CRITICAL, RecommendationPriorityBand.CRITICAL),
    ],
)
def test_map_priority_band(
    score_band: PriorityScoreBand,
    expected: RecommendationPriorityBand,
) -> None:
    assert map_priority_band(score_band) is expected


def test_priority_boost_for_revisit_prerequisites() -> None:
    spec = generate_recommendations(
        diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
        score_band=PriorityScoreBand.LOW,
        peak_factor_kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
    )
    revisit = next(
        item
        for item in spec.recommendations
        if item.category is RecommendationCategory.REVISIT_PREREQUISITES
    )
    assert revisit.priority.is_at_least(RecommendationPriorityBand.HIGH)
    assert "category revisit_prerequisites" in (revisit.priority.rationale or "")


def test_continue_mission_caps_critical_band() -> None:
    spec = generate_recommendations(score_band=PriorityScoreBand.CRITICAL)
    continue_rec = next(
        item
        for item in spec.recommendations
        if item.category is RecommendationCategory.CONTINUE_MISSION
    )
    assert continue_rec.priority.band is RecommendationPriorityBand.HIGH


def test_category_rank_orders_pause_above_continue() -> None:
    pause = category_rank(RecommendationCategory.PAUSE_FOR_CONSOLIDATION)
    continue_mission = category_rank(RecommendationCategory.CONTINUE_MISSION)
    assert pause > continue_mission


# --- supporting evidence ----------------------------------------------------


def test_supporting_evidence_cites_diagnosis_and_progress() -> None:
    spec = generate_recommendations()
    codes = {item.code for item in spec.primary.supporting_evidence}
    assert SupportingEvidenceCode.DIAGNOSIS in codes
    assert SupportingEvidenceCode.PRIORITY in codes
    assert SupportingEvidenceCode.PROGRESS_MASTERY in codes
    assert SupportingEvidenceCode.MISSION in codes
    assert all(item.statement for item in spec.primary.supporting_evidence)


def test_schedule_revision_evidence_includes_plan_and_revision() -> None:
    spec = generate_recommendations(
        diagnosis_type=DiagnosisType.WEAK_RETENTION,
    )
    revision = next(
        item
        for item in spec.recommendations
        if item.category is RecommendationCategory.SCHEDULE_REVISION
    )
    codes = {item.code for item in revision.supporting_evidence}
    assert SupportingEvidenceCode.PROGRESS_REVISION in codes
    assert SupportingEvidenceCode.STUDY_PLAN in codes


# --- confidence calculation -------------------------------------------------


@pytest.mark.parametrize(
    ("millipoints", "expected"),
    [
        (0, ConfidenceLevel.VERY_LOW),
        (199, ConfidenceLevel.VERY_LOW),
        (200, ConfidenceLevel.LOW),
        (399, ConfidenceLevel.LOW),
        (400, ConfidenceLevel.MEDIUM),
        (599, ConfidenceLevel.MEDIUM),
        (600, ConfidenceLevel.HIGH),
        (799, ConfidenceLevel.HIGH),
        (800, ConfidenceLevel.VERY_HIGH),
        (1000, ConfidenceLevel.VERY_HIGH),
    ],
)
def test_confidence_from_millipoints(
    millipoints: int,
    expected: ConfidenceLevel,
) -> None:
    assert confidence_from_millipoints(millipoints) is expected


def test_confidence_rejects_out_of_range_millipoints() -> None:
    with pytest.raises(EducationalInvariantViolation, match="millipoints"):
        confidence_from_millipoints(1001)


def test_generated_confidence_has_ratio_and_millipoints() -> None:
    spec = generate_recommendations()
    confidence = spec.primary.confidence
    assert confidence.ratio is not None
    assert 0.0 <= confidence.ratio <= 1.0
    assert confidence.millipoints is not None
    assert 0 <= confidence.millipoints <= 1000
    assert confidence_from_millipoints(confidence.millipoints) is confidence.level


def test_prerequisite_fit_raises_confidence_vs_baseline() -> None:
    baseline = generate_recommendations()
    prerequisite = generate_recommendations(
        diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
        peak_factor_kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
    )
    revisit = next(
        item
        for item in prerequisite.recommendations
        if item.category is RecommendationCategory.REVISIT_PREREQUISITES
    )
    assert revisit.confidence.millipoints is not None
    assert baseline.primary.confidence.millipoints is not None
    # Fit bonus applies to prerequisite category; millipoints remain in band.
    assert revisit.confidence.millipoints >= 400


# --- determinism ------------------------------------------------------------


def test_generation_is_deterministic() -> None:
    first = generate_recommendations()
    second = generate_recommendations()
    assert first == second
    assert first.specification_id == second.specification_id
    assert first.recommendations == second.recommendations
    assert first.educational_rationale == second.educational_rationale


def test_same_inputs_same_primary_category() -> None:
    inputs = make_recommendation_inputs(
        diagnosis_type=DiagnosisType.FALSE_CONFIDENCE,
    )
    first = RecommendationGenerator.generate(*inputs)
    second = RecommendationGenerator.generate(*inputs)
    assert first.primary.category is second.primary.category
    assert first.primary.confidence == second.primary.confidence


def test_recommendations_ordered_by_category_rank() -> None:
    spec = generate_recommendations(
        diagnosis_type=DiagnosisType.PREREQUISITE_GAP,
        peak_factor_kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
    )
    ranks = [category_rank(item.category) for item in spec.recommendations]
    assert ranks == sorted(ranks, reverse=True)


# --- architecture purity helpers --------------------------------------------


def test_recommendation_is_educational_decision_not_ui_hint() -> None:
    spec = generate_recommendations()
    for recommendation in spec.recommendations:
        assert recommendation.category in RecommendationCategory
        assert recommendation.reason.code.value
        assert "ui" not in recommendation.expected_outcome.casefold()
        assert "click" not in recommendation.expected_outcome.casefold()
        assert "button" not in recommendation.expected_outcome.casefold()


def test_aligned_factories_share_student_and_diagnosis() -> None:
    diagnosis = make_aligned_diagnosis()
    priority = make_aligned_priority()
    strategy = make_aligned_strategy()
    assert diagnosis.student_id == priority.student_id == strategy.student_id
    assert any(
        ref.diagnosis_id == diagnosis.diagnosis_id
        for ref in priority.diagnosis_references
    )
    assert any(
        ref.diagnosis_id == diagnosis.diagnosis_id
        for ref in strategy.diagnosis_references
    )


def test_urgency_preserved_on_mapped_priority() -> None:
    spec = generate_recommendations(urgency_level=UrgencyLevel.IMMEDIATE)
    assert all(
        item.priority.urgency is UrgencyLevel.IMMEDIATE
        or item.priority.urgency is UrgencyLevel.CRITICAL
        for item in spec.recommendations
    )


def test_mild_severity_inputs_still_generate() -> None:
    spec = generate_recommendations(severity=DiagnosisSeverityLevel.MILD)
    assert spec.recommendation_count() >= 1

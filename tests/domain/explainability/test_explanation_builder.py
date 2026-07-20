"""Educational Explainability Engine tests (EDU-005).

Covers: explanation generation, four-question sections, decision traces,
evidence references, determinism, and architecture purity.
"""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability import (
    DecisionStage,
    DecisionTrace,
    EducationalExplanation,
    EvidenceReference,
    EvidenceSourceKind,
    ExplanationBuilder,
    ExplanationSection,
    ExplanationSectionKind,
)
from tests.domain.explainability.explainability_helpers import (
    generate_explanation,
    make_explanation_inputs,
)
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
    Path(__file__).resolve().parents[3] / "src" / "domain" / "explainability"
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
    from domain import explainability as package

    for name in (
        "EducationalExplanation",
        "ExplanationSection",
        "ExplanationBuilder",
        "DecisionTrace",
        "EvidenceReference",
        "TraceStep",
        "ExplanationSectionKind",
        "DecisionStage",
        "EvidenceSourceKind",
    ):
        assert hasattr(package, name), name
        assert name in package.__all__


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


def test_builder_source_has_no_randomness_or_persistence() -> None:
    source = (PACKAGE_ROOT / "explanation_builder.py").read_text(encoding="utf-8")
    for token in (
        "import random",
        "from random",
        "import uuid",
        "from uuid",
        "import secrets",
        "from secrets",
        "datetime.now",
        "time.time",
        "sqlalchemy",
        "flask",
        "openai",
        "anthropic",
    ):
        assert token not in source


def test_domain_does_not_import_app_or_infrastructure() -> None:
    for path in PACKAGE_ROOT.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "from app." not in source
        assert "import app" not in source
        assert "infrastructure" not in source


# --- explanation generation -------------------------------------------------


def test_build_returns_complete_educational_explanation() -> None:
    explanation = generate_explanation()

    assert isinstance(explanation, EducationalExplanation)
    assert explanation.section_count() == 4
    assert explanation.evidence_count() >= 4
    assert isinstance(explanation.decision_trace, DecisionTrace)
    assert len(explanation.summary) >= 24


def test_explanation_includes_all_four_question_sections() -> None:
    explanation = generate_explanation()

    for kind in (
        ExplanationSectionKind.OBSERVED_FACTS,
        ExplanationSectionKind.ESTIMATES,
        ExplanationSectionKind.WHY,
        ExplanationSectionKind.NEXT_ACTION,
    ):
        assert explanation.has_section_kind(kind)
        section = explanation.section_for(kind)
        assert isinstance(section, ExplanationSection)
        assert section.kind is kind
        assert len(section.body) >= 12


def test_estimates_section_labels_uncertainty() -> None:
    explanation = generate_explanation()
    estimates = explanation.section_for(ExplanationSectionKind.ESTIMATES)
    assert estimates is not None
    assert "estimate" in estimates.body.casefold()
    assert "mastery" in estimates.body.casefold()


def test_next_action_preserves_mission_authority_disclosure() -> None:
    explanation = generate_explanation()
    next_action = explanation.section_for(ExplanationSectionKind.NEXT_ACTION)
    assert next_action is not None
    assert "mission" in next_action.body.casefold()


def test_decision_trace_covers_all_stages() -> None:
    explanation = generate_explanation()
    trace = explanation.decision_trace

    assert trace.stage_count() == 4
    for stage in (
        DecisionStage.MISSION,
        DecisionStage.STUDY_PLAN,
        DecisionStage.PROGRESS,
        DecisionStage.RECOMMENDATION,
    ):
        assert trace.has_stage(stage)
        step = trace.step_for(stage)
        assert step is not None
        assert step.stage is stage


def test_decision_trace_primary_matches_recommendation() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    explanation = ExplanationBuilder.build(
        mission, study_plan, progress, recommendations
    )

    assert (
        explanation.decision_trace.primary_decision
        == recommendations.primary.category.value
    )


def test_evidence_references_cite_lawful_sources() -> None:
    explanation = generate_explanation()
    kinds = {ref.source_kind for ref in explanation.evidence_references}

    assert EvidenceSourceKind.MISSION in kinds
    assert EvidenceSourceKind.STUDY_PLAN in kinds
    assert EvidenceSourceKind.PROGRESS in kinds
    assert EvidenceSourceKind.RECOMMENDATION in kinds
    for ref in explanation.evidence_references:
        assert isinstance(ref, EvidenceReference)
        assert len(ref.statement) >= 12


def test_section_evidence_links_resolve() -> None:
    explanation = generate_explanation()
    known = {ref.reference_id for ref in explanation.evidence_references}

    for section in explanation.sections:
        assert section.evidence_reference_ids
        for reference_id in section.evidence_reference_ids:
            assert reference_id in known


def test_lineage_ids_match_inputs() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    explanation = ExplanationBuilder.build(
        mission, study_plan, progress, recommendations
    )

    assert explanation.mission_id == mission.mission_id
    assert explanation.plan_id == study_plan.plan_id
    assert explanation.progress_report_id == progress.report_id
    assert (
        explanation.recommendation_specification_id
        == recommendations.specification_id
    )
    assert explanation.student_id == mission.student_id


# --- determinism ------------------------------------------------------------


def test_identical_inputs_yield_identical_explanations() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    first = ExplanationBuilder.build(
        mission, study_plan, progress, recommendations
    )
    second = ExplanationBuilder.build(
        mission, study_plan, progress, recommendations
    )

    assert first == second
    assert first.explanation_id == second.explanation_id
    assert first.decision_trace == second.decision_trace
    assert first.sections == second.sections
    assert first.evidence_references == second.evidence_references


def test_explanation_id_is_stable_from_source_ids() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    explanation = ExplanationBuilder.build(
        mission, study_plan, progress, recommendations
    )

    expected = (
        f"expl-{mission.mission_id.value}-{study_plan.plan_id.value}"
        f"-{progress.report_id.value}"
        f"-{recommendations.specification_id.value}"
    )
    assert explanation.explanation_id.value == expected


# --- invariants -------------------------------------------------------------


def test_mismatched_student_id_raises() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    other_plan = replace(study_plan, student_id="student-other")
    with pytest.raises(EducationalInvariantViolation, match="student_id"):
        ExplanationBuilder.build(
            mission, other_plan, progress, recommendations
        )


def test_mission_not_in_plan_raises() -> None:
    twin, mission, _study_plan, progress, _diagnosis, priority, _strategy = (
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
    recommendations = generate_recommendations(
        twin=twin,
        mission=mission,
        study_plan=_study_plan,
        progress=progress,
        diagnosis=_diagnosis,
        priority=priority,
        strategy=_strategy,
    )
    # Cite the alien plan so membership is checked after plan_id alignment.
    recommendations = replace(recommendations, plan_id=alien_plan.plan_id)
    assert mission.mission_id not in alien_plan.mission_ids
    with pytest.raises(EducationalInvariantViolation, match="mission_ids"):
        ExplanationBuilder.build(
            mission, alien_plan, progress, recommendations
        )


def test_wrong_input_type_raises() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    with pytest.raises(EducationalInvariantViolation, match="MissionSpecification"):
        ExplanationBuilder.build(
            "not-a-mission",  # type: ignore[arg-type]
            study_plan,
            progress,
            recommendations,
        )


def test_does_not_mutate_recommendation_specification() -> None:
    mission, study_plan, progress, recommendations = make_explanation_inputs()
    before = (
        recommendations.specification_id,
        recommendations.primary.recommendation_id,
        recommendations.primary.category,
        recommendations.educational_rationale,
    )
    ExplanationBuilder.build(mission, study_plan, progress, recommendations)
    after = (
        recommendations.specification_id,
        recommendations.primary.recommendation_id,
        recommendations.primary.category,
        recommendations.educational_rationale,
    )
    assert before == after

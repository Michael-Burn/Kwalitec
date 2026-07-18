"""Compilation policy and BlueprintCompiler tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.blueprint_compiler import (
    BlueprintCompiler,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintCompilationError,
)
from app.application.instructional_blueprint.policies.compilation_policy import (
    CompilationPolicy,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand
from tests.application.instructional_blueprint.helpers import (
    make_blueprint,
    make_profile,
    make_registry,
    make_rule,
    make_step,
    make_steps,
)


def test_practice_and_theory_classification():
    assert CompilationPolicy.is_practice("guided_practice")
    assert CompilationPolicy.is_theory("concept_learning")
    assert not CompilationPolicy.is_practice("concept_learning")


def test_practice_ratio():
    steps = make_steps("introduction", "guided_practice", "summary")
    assert CompilationPolicy.practice_ratio(steps) == pytest.approx(1 / 3)


def test_theory_ratio_empty():
    assert CompilationPolicy.theory_ratio(()) == 0.0
    assert CompilationPolicy.practice_ratio(()) == 0.0


def test_reindex():
    steps = (
        make_step("a", "introduction", sequence_index=5),
        make_step("b", "summary", sequence_index=9),
    )
    reindexed = CompilationPolicy.reindex(steps)
    assert [s.sequence_index for s in reindexed] == [0, 1]


def test_apply_bookends_introduction_summary_reflection():
    steps = make_steps("concept_learning")
    rules = (
        make_rule("bi", "bookend_introduction"),
        make_rule("br", "bookend_reflection"),
        make_rule("bs", "bookend_summary"),
    )
    result = CompilationPolicy.apply_bookends(steps, rules)
    kinds = [s.activity_kind for s in result]
    assert kinds[0] == "introduction"
    assert "reflection" in kinds
    assert kinds[-1] == "summary"


def test_apply_bookends_idempotent_when_present():
    steps = make_steps("introduction", "concept_learning", "summary")
    rules = (make_rule("bi", "bookend_introduction"),)
    result = CompilationPolicy.apply_bookends(steps, rules)
    assert sum(1 for s in result if s.activity_kind == "introduction") == 1


def test_enforce_required_activities_appends_missing():
    steps = make_steps("introduction", "summary")
    rules = (
        make_rule(
            "req",
            "require_activity",
            parameters={"activity_kind": "review"},
        ),
    )
    result = CompilationPolicy.enforce_required_activities(steps, rules)
    assert "review" in [s.activity_kind for s in result]


def test_estimate_effort_units_positive():
    bp = make_blueprint()
    units = CompilationPolicy.estimate_effort_units(bp)
    assert units > 0


def test_estimate_effort_band_uplift_for_many_steps():
    steps = make_steps(
        "introduction",
        "concept_learning",
        "worked_example",
        "guided_practice",
        "independent_practice",
        "knowledge_check",
        "reflection",
        "summary",
    )
    bp = make_blueprint(
        steps=steps,
        profile=make_profile(default_effort_band=EffortBand.MEDIUM, intensity=5),
    )
    band = CompilationPolicy.estimate_effort_band(bp)
    assert band in {EffortBand.HIGH, EffortBand.EXTENSIVE}


def test_estimate_effort_band_downshift_for_light():
    bp = make_blueprint(
        steps=make_steps("introduction", "summary"),
        profile=make_profile(default_effort_band=EffortBand.MEDIUM, intensity=1),
    )
    # weight_sum may be 2 with intensity 1 and len 2 -> downshift
    band = CompilationPolicy.estimate_effort_band(bp)
    assert effort_not_above_medium(band)


def effort_not_above_medium(band: EffortBand) -> bool:
    return band in {EffortBand.LOW, EffortBand.MEDIUM}


def test_compilation_policy_rejects_flags():
    assert CompilationPolicy.rejects_content_generation() is True
    assert CompilationPolicy.rejects_ai() is True


def test_compiler_compiles_defaults():
    compiler = BlueprintCompiler()
    registry = make_registry()
    for bp in registry.list_blueprints():
        if bp.blueprint_type == BlueprintType.CUSTOM:
            compiled = compiler.compile(
                bp,
                extra_steps=make_steps("custom", "summary"),
            )
        else:
            compiled = compiler.compile(bp)
        assert compiled.step_count >= 1
        assert compiled.estimated_effort_units > 0
        assert "no_content_generation" in compiled.rationale_tags


@pytest.mark.parametrize("blueprint_type", list(BlueprintType))
def test_compiler_produces_activity_kinds(blueprint_type):
    compiler = BlueprintCompiler()
    bp = make_registry().get_by_type(blueprint_type)
    extra = None
    if blueprint_type == BlueprintType.CUSTOM:
        extra = make_steps("guided_practice", "summary")
    compiled = compiler.compile(bp, extra_steps=extra)
    assert compiled.activity_kinds
    assert compiled.blueprint_type == blueprint_type


def test_compiler_custom_without_extra_raises():
    compiler = BlueprintCompiler()
    bp = make_registry().get_by_type(BlueprintType.CUSTOM)
    with pytest.raises(BlueprintCompilationError):
        compiler.compile(bp)


def test_compiler_rejects_forbidden_after_compile():
    compiler = BlueprintCompiler()
    bp = make_blueprint(
        steps=make_steps("introduction", "review", "summary"),
        rules=(
            make_rule(
                "forbid",
                "forbid_activity",
                parameters={"activity_kind": "review"},
            ),
        ),
    )
    with pytest.raises(BlueprintCompilationError):
        compiler.compile(bp)


def test_compiler_validate_false_allows_soft_failures():
    compiler = BlueprintCompiler()
    bp = make_blueprint(
        steps=make_steps("introduction", "summary"),
        rules=(
            make_rule(
                "pr",
                "min_practice_ratio",
                parameters={"ratio": "0.9"},
                severity="soft",
            ),
        ),
    )
    compiled = compiler.compile(bp, validate=False)
    assert compiled.step_count == 2


def test_compiler_adds_required_activity():
    compiler = BlueprintCompiler()
    bp = make_blueprint(
        steps=make_steps("introduction", "summary"),
        rules=(
            make_rule(
                "req",
                "require_activity",
                parameters={"activity_kind": "knowledge_check"},
            ),
        ),
    )
    compiled = compiler.compile(bp)
    assert "knowledge_check" in compiled.activity_kinds


def test_compiler_applies_bookend_rules():
    compiler = BlueprintCompiler()
    bp = make_blueprint(
        steps=make_steps("concept_learning"),
        rules=(
            make_rule("bi", "bookend_introduction"),
            make_rule("bs", "bookend_summary"),
        ),
    )
    compiled = compiler.compile(bp)
    assert compiled.activity_kinds[0] == "introduction"
    assert compiled.activity_kinds[-1] == "summary"


def test_compiled_applied_rule_ids():
    compiler = BlueprintCompiler()
    bp = make_blueprint(rules=(make_rule("r-a"), make_rule("r-b", "bookend_summary")))
    compiled = compiler.compile(bp)
    assert compiled.applied_rule_ids == ("r-a", "r-b")


def test_compiled_ratios():
    compiler = BlueprintCompiler()
    bp = make_blueprint(steps=make_steps("guided_practice", "concept_learning"))
    compiled = compiler.compile(bp)
    assert 0.0 <= compiled.practice_ratio <= 1.0
    assert 0.0 <= compiled.theory_ratio <= 1.0

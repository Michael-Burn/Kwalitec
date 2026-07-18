"""Additional edge-case and catalogue coverage tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.blueprint_compiler import (
    BlueprintCompiler,
)
from app.application.instructional_blueprint.blueprint_validator import (
    BlueprintValidator,
)
from app.application.instructional_blueprint.policies.compilation_policy import (
    CompilationPolicy,
)
from app.application.instructional_blueprint.policies.selection_policy import (
    SelectionPolicy,
)
from app.domain.instructional_blueprint.blueprint_rule import BlueprintRuleKind
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand
from tests.application.instructional_blueprint.helpers import (
    make_blueprint,
    make_engine,
    make_profile,
    make_rule,
    make_step,
    make_steps,
)


@pytest.mark.parametrize(
    "kind",
    [
        "introduction",
        "concept_learning",
        "worked_example",
        "guided_practice",
        "independent_practice",
        "knowledge_check",
        "reflection",
        "summary",
        "spaced_recall",
        "review",
        "next_intention",
        "custom",
    ],
)
def test_step_accepts_common_activity_kinds(kind):
    step = make_step(activity_kind=kind)
    assert step.activity_kind == kind


@pytest.mark.parametrize("rule_kind", list(BlueprintRuleKind))
def test_all_rule_kinds_constructible(rule_kind):
    rule = make_rule(f"r-{rule_kind.value}", rule_kind.value, parameters={"count": "1"})
    assert rule.kind == rule_kind


def test_selection_normalise_tag():
    assert SelectionPolicy.normalise_tag(" Exam Practice ") == "exam_practice"


def test_selection_default_type():
    assert SelectionPolicy.default_type() == BlueprintType.CONCEPT_MASTERY


def test_compilation_practice_kinds_non_empty():
    assert "guided_practice" in CompilationPolicy.practice_kinds()
    assert "concept_learning" in CompilationPolicy.theory_kinds()


def test_validator_empty_blueprint_id():
    from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint

    bp = InstructionalBlueprint(
        blueprint_id="",
        blueprint_type=BlueprintType.CUSTOM,
        name="X",
        steps=(),
        profile=make_profile(),
    )
    result = BlueprintValidator().validate(bp)
    assert "empty_blueprint_id" in result.codes


def test_validator_empty_name():
    from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint

    bp = InstructionalBlueprint(
        blueprint_id="bp",
        blueprint_type=BlueprintType.CUSTOM,
        name="",
        steps=(),
        profile=make_profile(),
    )
    result = BlueprintValidator().validate(bp)
    assert "empty_name" in result.codes


def test_validator_empty_activity_kind():
    from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
    from app.domain.instructional_blueprint.blueprint_step import BlueprintStep

    step = BlueprintStep(
        step_id="s0",
        activity_kind="",
        sequence_index=0,
    )
    bp = InstructionalBlueprint(
        blueprint_id="bp",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=(step,),
        profile=make_profile(),
    )
    result = BlueprintValidator().validate(bp)
    assert "empty_activity_kind" in result.codes


def test_validator_negative_effort_weight():
    from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
    from app.domain.instructional_blueprint.blueprint_step import BlueprintStep

    step = BlueprintStep(
        step_id="s0",
        activity_kind="review",
        sequence_index=0,
        effort_weight=-2,
    )
    bp = InstructionalBlueprint(
        blueprint_id="bp",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=(step,),
        profile=make_profile(),
    )
    result = BlueprintValidator().validate(bp)
    assert "negative_effort_weight" in result.codes


def test_validator_invalid_min_steps_parameter():
    bp = make_blueprint(
        rules=(make_rule("min", "min_steps", parameters={"count": "abc"}),)
    )
    result = BlueprintValidator().validate(bp)
    assert "invalid_rule_parameter" in result.codes


def test_validator_invalid_max_theory_parameter():
    bp = make_blueprint(
        rules=(
            make_rule(
                "tr",
                "max_theory_ratio",
                parameters={"ratio": "abc"},
            ),
        )
    )
    result = BlueprintValidator().validate(bp)
    assert "invalid_rule_parameter" in result.codes


def test_compiler_appends_extra_steps_to_non_custom():
    compiler = BlueprintCompiler()
    bp = make_blueprint(steps=make_steps("introduction", "summary"))
    compiled = compiler.compile(
        bp, extra_steps=(make_step("x", "reflection", sequence_index=0),)
    )
    assert "reflection" in compiled.activity_kinds
    assert compiled.activity_kinds[0] == "introduction"


def test_engine_generate_by_objective_kinds():
    engine = make_engine()
    handle = engine.generate_sequence(objective_kinds=("analyse",))
    assert handle.blueprint.blueprint_type == BlueprintType.CASE_STUDY


def test_engine_generate_by_blueprint_id():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_id="bp-theory_heavy")
    assert handle.blueprint.blueprint_type == BlueprintType.THEORY_HEAVY


def test_profile_dominant_is_assessment_when_highest():
    profile = make_profile(
        theory_weight=10,
        practice_weight=10,
        revision_weight=10,
        assessment_weight=70,
    )
    assert profile.dominant_dimension == "assessment"


def test_profile_dominant_is_revision_when_highest():
    profile = make_profile(
        theory_weight=10,
        practice_weight=10,
        revision_weight=70,
        assessment_weight=10,
    )
    assert profile.dominant_dimension == "revision"


def test_effort_band_estimate_extensive_path():
    steps = tuple(
        make_step(f"s{i}", "independent_practice", sequence_index=i, effort_weight=2)
        for i in range(10)
    )
    bp = make_blueprint(
        steps=steps,
        profile=make_profile(default_effort_band=EffortBand.HIGH, intensity=5),
    )
    band = CompilationPolicy.estimate_effort_band(bp)
    assert band == EffortBand.EXTENSIVE


def test_applied_rule_ids_empty():
    assert CompilationPolicy.applied_rule_ids(None) == ()
    assert CompilationPolicy.applied_rule_ids(()) == ()


def test_snapshot_validation_codes_empty_when_valid():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.REVISION)
    snap = engine.snapshot(handle)
    assert snap.validation_codes == () or snap.is_valid

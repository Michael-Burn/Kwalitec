"""BlueprintValidator tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.blueprint_validator import (
    BlueprintValidator,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintValidationError,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from tests.application.instructional_blueprint.helpers import (
    make_blueprint,
    make_profile,
    make_registry,
    make_rule,
    make_step,
    make_steps,
)


@pytest.fixture
def validator() -> BlueprintValidator:
    return BlueprintValidator()


def test_valid_default_blueprints(validator):
    registry = make_registry()
    for bp in registry.list_blueprints():
        if bp.blueprint_type == BlueprintType.CUSTOM:
            result = validator.validate(bp)
            # empty custom may have soft min_steps
            assert result.is_valid or not result.hard_issues
        else:
            assert validator.validate(bp).is_valid


def test_validate_happy_path(validator):
    result = validator.validate(make_blueprint())
    assert result.is_valid
    assert result.codes == ()


def test_empty_steps_non_custom(validator):
    bp = InstructionalBlueprint(
        blueprint_id="bp1",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=(),
        rules=(),
        profile=make_profile(),
    )
    result = validator.validate(bp)
    assert not result.is_valid
    assert "empty_steps" in result.codes


def test_duplicate_step_id(validator):
    steps = (
        make_step("dup", "introduction", sequence_index=0),
        make_step("dup", "summary", sequence_index=1),
    )
    # Bypass create() duplicate check via raw dataclass.
    bp = InstructionalBlueprint(
        blueprint_id="bp1",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=steps,
        rules=(),
        profile=make_profile(),
    )
    result = validator.validate(bp)
    assert "duplicate_step_id" in result.codes


def test_index_gap(validator):
    steps = (
        make_step("a", "introduction", sequence_index=0),
        make_step("b", "summary", sequence_index=2),
    )
    bp = InstructionalBlueprint(
        blueprint_id="bp1",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=steps,
        profile=make_profile(),
    )
    result = validator.validate(bp)
    assert "index_gap" in result.codes


def test_order_mismatch(validator):
    steps = (
        make_step("a", "summary", sequence_index=1),
        make_step("b", "introduction", sequence_index=0),
    )
    bp = InstructionalBlueprint(
        blueprint_id="bp1",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=steps,
        profile=make_profile(),
    )
    result = validator.validate(bp)
    assert "order_mismatch" in result.codes


def test_require_activity_rule(validator):
    bp = make_blueprint(
        steps=make_steps("introduction", "summary"),
        rules=(
            make_rule(
                "req",
                "require_activity",
                parameters={"activity_kind": "review"},
            ),
        ),
    )
    result = validator.validate(bp)
    assert "missing_required_activity" in result.codes


def test_forbid_activity_rule(validator):
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
    result = validator.validate(bp)
    assert "forbidden_activity_present" in result.codes


def test_max_steps_rule(validator):
    bp = make_blueprint(
        steps=make_steps("a", "b", "c"),
        rules=(make_rule("max", "max_steps", parameters={"count": "2"}),),
    )
    result = validator.validate(bp)
    assert "max_steps_exceeded" in result.codes


def test_min_steps_rule(validator):
    bp = make_blueprint(
        steps=make_steps("introduction"),
        rules=(make_rule("min", "min_steps", parameters={"count": "3"}),),
    )
    result = validator.validate(bp)
    assert "min_steps_not_met" in result.codes


def test_min_practice_ratio_rule(validator):
    bp = make_blueprint(
        steps=make_steps("introduction", "concept_learning", "summary"),
        rules=(
            make_rule(
                "pr",
                "min_practice_ratio",
                parameters={"ratio": "0.8"},
            ),
        ),
    )
    result = validator.validate(bp)
    assert "min_practice_ratio_not_met" in result.codes


def test_max_theory_ratio_rule(validator):
    bp = make_blueprint(
        steps=make_steps("introduction", "concept_learning", "summary"),
        rules=(
            make_rule(
                "tr",
                "max_theory_ratio",
                parameters={"ratio": "0.2"},
            ),
        ),
    )
    result = validator.validate(bp)
    assert "max_theory_ratio_exceeded" in result.codes


def test_soft_rule_does_not_invalidate(validator):
    bp = make_blueprint(
        steps=make_steps("introduction"),
        rules=(
            make_rule(
                "min",
                "min_steps",
                parameters={"count": "5"},
                severity="soft",
            ),
        ),
    )
    result = validator.validate(bp)
    assert result.is_valid
    assert result.soft_issues
    assert not result.hard_issues


def test_invalid_rule_parameter_max_steps(validator):
    bp = make_blueprint(
        rules=(make_rule("max", "max_steps", parameters={"count": "x"}),),
    )
    result = validator.validate(bp)
    assert "invalid_rule_parameter" in result.codes


def test_invalid_rule_parameter_min_practice(validator):
    bp = make_blueprint(
        rules=(
            make_rule(
                "pr",
                "min_practice_ratio",
                parameters={"ratio": "nope"},
            ),
        ),
    )
    result = validator.validate(bp)
    assert "invalid_rule_parameter" in result.codes


def test_assert_valid_raises(validator):
    bp = make_blueprint(
        steps=make_steps("introduction"),
        rules=(make_rule("min", "min_steps", parameters={"count": "9"}),),
    )
    with pytest.raises(BlueprintValidationError):
        validator.assert_valid(bp)


def test_assert_valid_passes(validator):
    validator.assert_valid(make_blueprint())


def test_duplicate_rule_id(validator):
    bp = InstructionalBlueprint(
        blueprint_id="bp1",
        blueprint_type=BlueprintType.REVISION,
        name="Rev",
        steps=make_steps("review"),
        rules=(make_rule("r1"), make_rule("r1")),
        profile=make_profile(),
    )
    result = validator.validate(bp)
    assert "duplicate_rule_id" in result.codes


def test_zero_profile_weight_soft(validator):
    bp = make_blueprint(
        profile=make_profile(
            theory_weight=0,
            practice_weight=0,
            revision_weight=0,
            assessment_weight=0,
        ),
    )
    result = validator.validate(bp)
    assert result.is_valid
    assert "zero_profile_weight" in result.codes

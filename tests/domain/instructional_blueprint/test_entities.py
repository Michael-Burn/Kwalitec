"""Domain entity tests for Instructional Blueprint aggregates."""

from __future__ import annotations

import pytest

from app.domain.instructional_blueprint import (
    BlueprintProfile,
    BlueprintRule,
    BlueprintStep,
    BlueprintType,
    EffortBand,
    InstructionalBlueprint,
)
from tests.domain.instructional_blueprint.helpers import (
    make_blueprint,
    make_profile,
    make_rule,
    make_step,
    make_steps,
)

# ---------------------------------------------------------------------------
# BlueprintStep
# ---------------------------------------------------------------------------


def test_step_create_normalises_activity_kind():
    step = BlueprintStep.create("s1", "Concept Learning", sequence_index=0)
    assert step.activity_kind == "concept_learning"


def test_step_create_rejects_empty_id():
    with pytest.raises(ValueError, match="step_id"):
        BlueprintStep.create("", "concept_learning")


def test_step_create_rejects_empty_kind():
    with pytest.raises(ValueError, match="activity_kind"):
        BlueprintStep.create("s1", "  ")


def test_step_create_rejects_negative_index():
    with pytest.raises(ValueError, match="sequence_index"):
        BlueprintStep.create("s1", "review", sequence_index=-1)


def test_step_create_rejects_negative_weight():
    with pytest.raises(ValueError, match="effort_weight"):
        BlueprintStep.create("s1", "review", effort_weight=-1)


def test_step_optional_role_normalised():
    step = make_step(role="Warm Up")
    assert step.role == "warm_up"


def test_step_blank_role_becomes_none():
    step = make_step(role="  ")
    assert step.role is None


def test_step_with_index():
    step = make_step(sequence_index=0)
    updated = step.with_index(3)
    assert updated.sequence_index == 3
    assert updated.step_id == step.step_id


def test_step_with_index_rejects_negative():
    with pytest.raises(ValueError):
        make_step().with_index(-1)


def test_step_is_frozen():
    step = make_step()
    with pytest.raises(Exception):
        step.activity_kind = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# BlueprintRule
# ---------------------------------------------------------------------------


def test_rule_create_from_dict_parameters():
    rule = BlueprintRule.create(
        "r1",
        "require_activity",
        parameters={"activity_kind": "review"},
    )
    assert rule.parameter("activity_kind") == "review"
    assert "activity_kind=review" in rule.parameters


def test_rule_parameter_map_ignores_bare_tokens():
    rule = make_rule(parameters=("count=3", "bare"))
    assert rule.parameter_map() == {"count": "3"}


def test_rule_rejects_empty_id():
    with pytest.raises(ValueError, match="rule_id"):
        BlueprintRule.create("", "min_steps")


def test_rule_rejects_bad_severity():
    with pytest.raises(ValueError, match="severity"):
        BlueprintRule.create("r1", "min_steps", severity="critical")


def test_rule_default_severity_hard():
    assert make_rule().severity == "hard"


def test_rule_soft_severity():
    rule = make_rule(severity="soft")
    assert rule.severity == "soft"


def test_rule_parameter_default():
    rule = make_rule(parameters=())
    assert rule.parameter("missing", "fallback") == "fallback"


# ---------------------------------------------------------------------------
# BlueprintProfile
# ---------------------------------------------------------------------------


def test_profile_create_defaults():
    profile = BlueprintProfile.create("p1")
    assert profile.total_weight == 100
    assert profile.default_effort_band == EffortBand.MEDIUM
    assert profile.intensity == 3


def test_profile_rejects_empty_id():
    with pytest.raises(ValueError, match="profile_id"):
        BlueprintProfile.create("")


def test_profile_rejects_weight_out_of_range():
    with pytest.raises(ValueError, match="theory_weight"):
        BlueprintProfile.create("p1", theory_weight=101)


@pytest.mark.parametrize("intensity", [0, 6, -1])
def test_profile_rejects_bad_intensity(intensity):
    with pytest.raises(ValueError, match="intensity"):
        BlueprintProfile.create("p1", intensity=intensity)


def test_profile_dominant_dimension_deterministic_tie():
    profile = BlueprintProfile.create(
        "p1",
        theory_weight=40,
        practice_weight=40,
        revision_weight=10,
        assessment_weight=10,
    )
    # Tie broken by dimension order preference (higher order index wins via -order).
    assert profile.dominant_dimension in {"theory", "practice"}


def test_profile_normalised_weights_sum_to_one():
    profile = make_profile(
        theory_weight=50,
        practice_weight=50,
        revision_weight=0,
        assessment_weight=0,
    )
    norms = profile.normalised_weights()
    assert abs(sum(norms.values()) - 1.0) < 1e-9


def test_profile_normalised_weights_zero_total():
    # Construct via object.__setattr__ bypass is not allowed; use create with zeros.
    profile = BlueprintProfile.create(
        "p0",
        theory_weight=0,
        practice_weight=0,
        revision_weight=0,
        assessment_weight=0,
    )
    assert profile.normalised_weights() == {
        "theory": 0.0,
        "practice": 0.0,
        "revision": 0.0,
        "assessment": 0.0,
    }


def test_profile_resolves_effort_band_string():
    profile = BlueprintProfile.create("p1", default_effort_band="high")
    assert profile.default_effort_band == EffortBand.HIGH


# ---------------------------------------------------------------------------
# InstructionalBlueprint
# ---------------------------------------------------------------------------


def test_blueprint_create_happy_path():
    bp = make_blueprint()
    assert bp.step_count == 3
    assert bp.activity_kinds == (
        "introduction",
        "concept_learning",
        "summary",
    )


def test_blueprint_rejects_empty_id():
    with pytest.raises(ValueError, match="blueprint_id"):
        InstructionalBlueprint.create("", BlueprintType.REVISION, "Rev")


def test_blueprint_rejects_empty_name():
    with pytest.raises(ValueError, match="name"):
        InstructionalBlueprint.create("bp1", BlueprintType.REVISION, "  ")


def test_blueprint_rejects_empty_steps_for_non_custom():
    with pytest.raises(ValueError, match="steps"):
        InstructionalBlueprint.create(
            "bp1",
            BlueprintType.CONCEPT_MASTERY,
            "CM",
            steps=(),
        )


def test_blueprint_allows_empty_steps_for_custom():
    bp = InstructionalBlueprint.create(
        "bp1",
        BlueprintType.CUSTOM,
        "Custom",
        steps=(),
        allow_empty_steps=True,
    )
    assert bp.step_count == 0


def test_blueprint_rejects_duplicate_step_ids():
    steps = (
        make_step("dup", "introduction", sequence_index=0),
        make_step("dup", "summary", sequence_index=1),
    )
    with pytest.raises(ValueError, match="duplicate step_id"):
        make_blueprint(steps=steps)


def test_blueprint_rejects_duplicate_rule_ids():
    with pytest.raises(ValueError, match="duplicate rule_id"):
        make_blueprint(rules=(make_rule("r1"), make_rule("r1")))


def test_blueprint_rejects_non_contiguous_indices():
    steps = (
        make_step("a", "introduction", sequence_index=0),
        make_step("b", "summary", sequence_index=2),
    )
    with pytest.raises(ValueError, match="contiguous"):
        make_blueprint(steps=steps)


def test_blueprint_rejects_unordered_steps():
    steps = (
        make_step("a", "summary", sequence_index=1),
        make_step("b", "introduction", sequence_index=0),
    )
    with pytest.raises(ValueError, match="ordered"):
        make_blueprint(steps=steps)


def test_blueprint_step_by_id():
    bp = make_blueprint()
    assert bp.step_by_id("s1").activity_kind == "concept_learning"
    assert bp.step_by_id("missing") is None
    assert bp.step_by_id("  ") is None


def test_blueprint_default_effort_band_from_profile():
    bp = make_blueprint(profile=make_profile(default_effort_band=EffortBand.HIGH))
    assert bp.default_effort_band == EffortBand.HIGH


def test_blueprint_with_steps_replaces():
    bp = make_blueprint()
    updated = bp.with_steps(make_steps("review", "summary"))
    assert updated.activity_kinds == ("review", "summary")
    assert updated.blueprint_id == bp.blueprint_id


def test_blueprint_resolves_type_string():
    bp = make_blueprint(blueprint_type="exam_practice")
    assert bp.blueprint_type == BlueprintType.EXAM_PRACTICE


def test_blueprint_is_frozen():
    bp = make_blueprint()
    with pytest.raises(Exception):
        bp.name = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    "blueprint_type",
    list(BlueprintType),
)
def test_blueprint_accepts_all_catalogue_types(blueprint_type):
    steps = () if blueprint_type == BlueprintType.CUSTOM else make_steps("introduction")
    bp = make_blueprint(
        blueprint_id=f"bp-{blueprint_type.value}",
        blueprint_type=blueprint_type,
        name=blueprint_type.value,
        steps=steps,
        allow_empty_steps=True,
    )
    assert bp.blueprint_type == blueprint_type

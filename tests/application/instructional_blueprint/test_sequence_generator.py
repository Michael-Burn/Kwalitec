"""SequenceGenerator and BlueprintPlan output tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.blueprint_compiler import (
    BlueprintCompiler,
)
from app.application.instructional_blueprint.exceptions import (
    SequenceGenerationError,
)
from app.application.instructional_blueprint.sequence_generator import (
    SequenceGenerator,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from tests.application.instructional_blueprint.helpers import (
    make_blueprint,
    make_registry,
    make_steps,
)


@pytest.fixture
def generator() -> SequenceGenerator:
    return SequenceGenerator()


@pytest.fixture
def compiled_concept():
    bp = make_registry().get_by_type(BlueprintType.CONCEPT_MASTERY)
    return BlueprintCompiler().compile(bp)


def test_generate_plan_slots(generator, compiled_concept):
    plan = generator.generate(compiled_concept)
    assert len(plan.activity_slots) == compiled_concept.step_count
    assert plan.session_skeleton.slot_count == compiled_concept.step_count
    assert len(plan.learning_sequence) == compiled_concept.step_count


def test_generate_plan_effort(generator, compiled_concept):
    plan = generator.generate(compiled_concept)
    assert plan.estimated_effort_band == compiled_concept.estimated_effort_band
    assert plan.estimated_effort_units == compiled_concept.estimated_effort_units


def test_generate_plan_rationale_forbids_content(generator, compiled_concept):
    plan = generator.generate(compiled_concept)
    for tag in (
        "no_content_generation",
        "no_questions",
        "no_explanations",
        "no_pdfs",
        "no_ai",
    ):
        assert tag in plan.rationale_tags


def test_objective_ids_round_robin(generator, compiled_concept):
    plan = generator.generate(
        compiled_concept, objective_ids=("obj-a", "obj-b")
    )
    assert plan.objective_ids == ("obj-a", "obj-b")
    kinds = [slot.objective_id for slot in plan.activity_slots]
    assert kinds[0] == "obj-a"
    assert kinds[1] == "obj-b"
    assert kinds[2] == "obj-a"


def test_blank_objective_ids_ignored(generator, compiled_concept):
    plan = generator.generate(compiled_concept, objective_ids=("  ", "obj-1"))
    assert plan.objective_ids == ("obj-1",)


def test_session_skeleton_phase_labels(generator, compiled_concept):
    skeleton = generator.session_skeleton(compiled_concept)
    assert len(skeleton.phase_labels) == skeleton.slot_count
    assert skeleton.phase_labels[0].startswith("0:")


def test_learning_sequence_entries(generator, compiled_concept):
    sequence = generator.learning_sequence(compiled_concept)
    assert sequence[0].sequence_index == 0
    assert sequence[0].activity_kind
    assert sequence[0].step_id


def test_generate_empty_compiled_raises(generator):
    from app.application.instructional_blueprint.dto.compiled_blueprint import (
        CompiledBlueprint,
    )
    from app.domain.instructional_blueprint.effort_band import EffortBand

    empty = CompiledBlueprint(
        blueprint_id="bp",
        blueprint_type=BlueprintType.CUSTOM,
        steps=(),
        applied_rule_ids=(),
        estimated_effort_band=EffortBand.LOW,
        estimated_effort_units=0,
        practice_ratio=0.0,
        theory_ratio=0.0,
        rationale_tags=(),
    )
    with pytest.raises(SequenceGenerationError):
        generator.generate(empty)


_NON_CUSTOM = [t for t in BlueprintType if t != BlueprintType.CUSTOM]


@pytest.mark.parametrize("blueprint_type", _NON_CUSTOM)
def test_generate_for_all_default_types(generator, blueprint_type):
    bp = make_registry().get_by_type(blueprint_type)
    compiled = BlueprintCompiler().compile(bp)
    plan = generator.generate(compiled)
    assert plan.blueprint_type == blueprint_type
    assert plan.session_skeleton.slot_count >= 5


def test_custom_compile_then_generate(generator):
    bp = make_registry().get_by_type(BlueprintType.CUSTOM)
    compiled = BlueprintCompiler().compile(
        bp, extra_steps=make_steps("custom", "reflection", "summary")
    )
    plan = generator.generate(compiled)
    assert plan.activity_slots[0].activity_kind == "custom"


def test_plan_slots_preserve_roles(generator):
    from tests.application.instructional_blueprint.helpers import make_step

    bp = make_blueprint(
        steps=(
            make_step("s0", "introduction", sequence_index=0, role="warm_up"),
            make_step("s1", "summary", sequence_index=1, role="consolidate"),
        )
    )
    compiled = BlueprintCompiler().compile(bp)
    plan = generator.generate(compiled)
    assert plan.activity_slots[0].role == "warm_up"
    assert plan.activity_slots[1].role == "consolidate"

"""InstructionalBlueprintEngine facade tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.engine import (
    BlueprintHandle,
    InstructionalBlueprintEngine,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintAlreadyRegistered,
    BlueprintCompilationError,
    BlueprintNotFound,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand
from tests.application.instructional_blueprint.helpers import (
    make_blueprint,
    make_engine,
    make_steps,
)


def test_engine_identity():
    engine = make_engine()
    assert engine.engine_id == "instructional_blueprint"
    assert engine.engine_version == "1.0.0"


def test_engine_lists_defaults():
    engine = make_engine()
    assert len(engine.list_blueprints()) == 8


def test_engine_get_blueprint():
    engine = make_engine()
    bp = engine.get_blueprint("bp-mixed_practice")
    assert bp.blueprint_type == BlueprintType.MIXED_PRACTICE


def test_engine_get_by_type():
    engine = make_engine()
    bp = engine.get_blueprint_by_type("exam_practice")
    assert bp.name == "Exam Practice"


def test_engine_register_custom():
    engine = make_engine(seed_defaults=False)
    bp = make_blueprint(blueprint_id="bp-x")
    engine.register_blueprint(bp)
    assert engine.get_blueprint("bp-x") is bp


def test_engine_register_duplicate_raises():
    engine = make_engine()
    bp = make_blueprint(blueprint_id="bp-revision")
    with pytest.raises(BlueprintAlreadyRegistered):
        engine.register_blueprint(bp)


def test_engine_select_and_validate():
    engine = make_engine()
    selection = engine.select_blueprint(intent_tags=("revision",))
    result = engine.validate_blueprint(selection.blueprint)
    assert result.is_valid


def test_engine_compile_and_generate_plan():
    engine = make_engine()
    bp = engine.get_blueprint_by_type(BlueprintType.THEORY_HEAVY)
    compiled = engine.compile_blueprint(bp)
    plan = engine.generate_plan(compiled, objective_ids=("o1",))
    assert plan.session_skeleton.slot_count == compiled.step_count
    assert plan.objective_ids == ("o1",)


def test_engine_generate_sequence_pipeline():
    engine = make_engine()
    handle = engine.generate_sequence(intent_tags=("exam",), objective_ids=("a", "b"))
    assert isinstance(handle, BlueprintHandle)
    assert handle.compiled is not None
    assert handle.plan is not None
    assert handle.blueprint.blueprint_type == BlueprintType.EXAM_PRACTICE
    assert handle.selection_rationale


def test_engine_generate_sequence_by_type():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.CASE_STUDY)
    assert handle.plan.blueprint_type == BlueprintType.CASE_STUDY


def test_engine_generate_sequence_custom_with_extra_steps():
    engine = make_engine()
    handle = engine.generate_sequence(
        blueprint_type=BlueprintType.CUSTOM,
        extra_steps=make_steps("custom", "summary"),
    )
    assert handle.compiled.activity_kinds[0] == "custom"


def test_engine_estimate_effort():
    engine = make_engine()
    bp = engine.get_blueprint_by_type(BlueprintType.CALCULATION_INTENSIVE)
    band, units = engine.estimate_effort(bp)
    assert isinstance(band, EffortBand)
    assert units > 0


def test_engine_instructional_structure():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_type="concept_mastery")
    structure = engine.instructional_structure(handle)
    assert structure.step_count == handle.compiled.step_count
    assert structure.activity_kinds
    assert structure.phase_labels


def test_engine_instructional_structure_without_compiled():
    engine = make_engine()
    bp = engine.get_blueprint_by_type(BlueprintType.REVISION)
    handle = BlueprintHandle(blueprint=bp)
    structure = engine.instructional_structure(handle)
    assert structure.blueprint_type == BlueprintType.REVISION
    assert structure.step_count > 0


def test_engine_session_skeleton():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.MIXED_PRACTICE)
    skeleton = engine.session_skeleton(handle)
    assert skeleton.slot_count == handle.plan.session_skeleton.slot_count


def test_engine_session_skeleton_without_plan():
    engine = make_engine()
    bp = engine.get_blueprint_by_type(BlueprintType.REVISION)
    handle = BlueprintHandle(blueprint=bp)
    skeleton = engine.session_skeleton(handle)
    assert skeleton.slot_count > 0


def test_engine_snapshot():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.CONCEPT_MASTERY)
    snap = engine.snapshot(handle)
    assert snap.is_valid
    assert snap.blueprint is handle.blueprint
    assert snap.compiled is handle.compiled
    assert snap.plan is handle.plan
    assert snap.structure.step_count > 0


def test_engine_rehydrate():
    engine = make_engine()
    bp = engine.get_blueprint_by_type(BlueprintType.REVISION)
    handle = engine.rehydrate(bp)
    assert handle.blueprint is bp
    assert handle.compiled is None


def test_engine_assert_valid():
    engine = make_engine()
    bp = engine.get_blueprint_by_type(BlueprintType.CONCEPT_MASTERY)
    engine.assert_valid(bp)


def test_engine_missing_blueprint_raises():
    engine = make_engine()
    with pytest.raises(BlueprintNotFound):
        engine.get_blueprint("nope")


def test_engine_compile_invalid_raises():
    from tests.application.instructional_blueprint.helpers import make_rule

    engine = make_engine()
    bp = make_blueprint(
        steps=make_steps("introduction", "review"),
        rules=(
            make_rule(
                "f",
                "forbid_activity",
                parameters={"activity_kind": "review"},
            ),
        ),
    )
    with pytest.raises(BlueprintCompilationError):
        engine.compile_blueprint(bp)


@pytest.mark.parametrize(
    "intent,expected",
    [
        ("concept", BlueprintType.CONCEPT_MASTERY),
        ("calculation", BlueprintType.CALCULATION_INTENSIVE),
        ("theory", BlueprintType.THEORY_HEAVY),
        ("revision", BlueprintType.REVISION),
        ("mixed", BlueprintType.MIXED_PRACTICE),
        ("exam", BlueprintType.EXAM_PRACTICE),
        ("case", BlueprintType.CASE_STUDY),
    ],
)
def test_engine_end_to_end_intents(intent, expected):
    engine = make_engine()
    handle = engine.generate_sequence(intent_tags=(intent,))
    assert handle.blueprint.blueprint_type == expected
    assert handle.plan.learning_sequence
    assert handle.plan.session_skeleton.slot_count >= 1
    assert "no_questions" in handle.plan.rationale_tags


def test_engine_deterministic_for_same_inputs():
    engine = make_engine()
    a = engine.generate_sequence(blueprint_type=BlueprintType.REVISION)
    b = engine.generate_sequence(blueprint_type=BlueprintType.REVISION)
    assert a.compiled.activity_kinds == b.compiled.activity_kinds
    assert a.plan.estimated_effort_units == b.plan.estimated_effort_units


def test_engine_without_defaults():
    engine = InstructionalBlueprintEngine(seed_defaults=False)
    assert engine.list_blueprints() == ()

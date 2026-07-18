"""DTO immutability and package export tests."""

from __future__ import annotations

import pytest

from app.application.instructional_blueprint.dto.blueprint_plan import (
    ActivityPlanSlot,
    BlueprintPlan,
    LearningSequenceEntry,
    SessionSkeleton,
)
from app.application.instructional_blueprint.dto.blueprint_snapshot import (
    BlueprintSnapshot,
    InstructionalStructure,
)
from app.application.instructional_blueprint.dto.compiled_blueprint import (
    CompiledBlueprint,
)
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand
from tests.application.instructional_blueprint.helpers import make_engine


def _sample_plan() -> BlueprintPlan:
    slots = (
        ActivityPlanSlot("introduction", 0, role="warm_up"),
        ActivityPlanSlot("summary", 1, role="consolidate"),
    )
    skeleton = SessionSkeleton(
        slot_count=2,
        phase_labels=("0:introduction:warm_up", "1:summary:consolidate"),
        estimated_effort_units=5,
    )
    sequence = (
        LearningSequenceEntry(0, "introduction", "warm_up", "s0"),
        LearningSequenceEntry(1, "summary", "consolidate", "s1"),
    )
    return BlueprintPlan(
        blueprint_id="bp",
        blueprint_type=BlueprintType.CUSTOM,
        activity_slots=slots,
        session_skeleton=skeleton,
        learning_sequence=sequence,
        estimated_effort_band=EffortBand.LOW,
        estimated_effort_units=5,
        rationale_tags=("tag",),
    )


def test_activity_plan_slot_frozen():
    slot = ActivityPlanSlot("review", 0)
    with pytest.raises(Exception):
        slot.activity_kind = "other"  # type: ignore[misc]


def test_session_skeleton_frozen():
    skeleton = SessionSkeleton(1, ("0:a:core",), 2)
    with pytest.raises(Exception):
        skeleton.slot_count = 9  # type: ignore[misc]


def test_learning_sequence_entry_frozen():
    entry = LearningSequenceEntry(0, "review")
    with pytest.raises(Exception):
        entry.activity_kind = "x"  # type: ignore[misc]


def test_blueprint_plan_frozen():
    plan = _sample_plan()
    with pytest.raises(Exception):
        plan.blueprint_id = "x"  # type: ignore[misc]


def test_compiled_blueprint_properties():
    compiled = CompiledBlueprint(
        blueprint_id="bp",
        blueprint_type=BlueprintType.REVISION,
        steps=(),
        applied_rule_ids=(),
        estimated_effort_band=EffortBand.MEDIUM,
        estimated_effort_units=4,
        practice_ratio=0.5,
        theory_ratio=0.5,
        rationale_tags=(),
    )
    assert compiled.step_count == 0
    assert compiled.activity_kinds == ()


def test_compiled_blueprint_frozen():
    compiled = CompiledBlueprint(
        blueprint_id="bp",
        blueprint_type=BlueprintType.REVISION,
        steps=(),
        applied_rule_ids=(),
        estimated_effort_band=EffortBand.MEDIUM,
        estimated_effort_units=4,
        practice_ratio=0.5,
        theory_ratio=0.5,
        rationale_tags=(),
    )
    with pytest.raises(Exception):
        compiled.blueprint_id = "x"  # type: ignore[misc]


def test_instructional_structure_frozen():
    structure = InstructionalStructure(
        blueprint_type=BlueprintType.REVISION,
        activity_kinds=("review",),
        step_count=1,
        estimated_effort_band=EffortBand.LOW,
        estimated_effort_units=2,
        phase_labels=("0:review:core",),
        rationale_tags=(),
    )
    with pytest.raises(Exception):
        structure.step_count = 2  # type: ignore[misc]


def test_blueprint_snapshot_frozen():
    snap = BlueprintSnapshot(
        blueprint=None,
        compiled=None,
        plan=None,
        structure=InstructionalStructure(
            blueprint_type=BlueprintType.CUSTOM,
            activity_kinds=(),
            step_count=0,
            estimated_effort_band=EffortBand.LOW,
            estimated_effort_units=0,
            phase_labels=(),
            rationale_tags=(),
        ),
        is_valid=True,
    )
    with pytest.raises(Exception):
        snap.is_valid = False  # type: ignore[misc]


def test_dto_package_lazy_exports():
    import app.application.instructional_blueprint.dto as dto

    for name in dto.__all__:
        assert getattr(dto, name) is not None


def test_application_package_lazy_exports():
    import app.application.instructional_blueprint as pkg

    for name in (
        "InstructionalBlueprintEngine",
        "BlueprintRegistry",
        "BlueprintSelector",
        "BlueprintCompiler",
        "SequenceGenerator",
        "SelectionPolicy",
        "CompilationPolicy",
        "BlueprintPlan",
        "CompiledBlueprint",
        "BlueprintSnapshot",
    ):
        assert getattr(pkg, name) is not None


def test_application_package_unknown_export():
    import app.application.instructional_blueprint as pkg

    with pytest.raises(AttributeError):
        getattr(pkg, "DefinitelyMissing")


def test_policies_package_exports():
    import app.application.instructional_blueprint.policies as policies

    assert policies.SelectionPolicy is not None
    assert policies.CompilationPolicy is not None


def test_engine_handle_frozen():
    engine = make_engine()
    handle = engine.generate_sequence(blueprint_type=BlueprintType.REVISION)
    with pytest.raises(Exception):
        handle.blueprint = handle.blueprint  # type: ignore[misc]


def test_plan_from_engine_has_no_content_fields():
    engine = make_engine()
    plan = engine.generate_sequence(blueprint_type=BlueprintType.EXAM_PRACTICE).plan
    # Structural fields only — no question/explanation/pdf attributes.
    assert not hasattr(plan, "questions")
    assert not hasattr(plan, "explanations")
    assert not hasattr(plan, "pdf_path")
    assert not hasattr(plan.activity_slots[0], "prompt")
    assert not hasattr(plan.activity_slots[0], "content")

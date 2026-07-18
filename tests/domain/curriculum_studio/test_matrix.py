"""Matrix and regression tests for Curriculum Studio domain."""

from __future__ import annotations

import itertools

import pytest

from app.domain.curriculum_studio.curriculum_diff import CurriculumDiff
from app.domain.curriculum_studio.publication_checklist import (
    CHECKLIST_ORDER,
    ChecklistItemCode,
    PublicationChecklist,
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.studio_workflow import (
    WorkflowTransitionEvent,
    is_lawful_transition,
    next_workflow_state,
)
from app.domain.curriculum_studio.workflow_stage import (
    CANONICAL_WORKFLOW,
    WorkflowStage,
    has_reached,
    stage_index,
)
from tests.domain.curriculum_studio.helpers import (
    make_curriculum,
    make_facts,
    make_topic,
    make_workflow,
)

FACT_FIELDS = (
    "cmp_uploaded",
    "official_syllabus_uploaded",
    "validation_passed",
    "blueprint_assigned",
    "preview_approved",
    "version_assigned",
    "rollback_snapshot_created",
)


@pytest.mark.parametrize("mask", range(128))
def test_checklist_ready_iff_all_seven_facts(mask):
    """Exhaustive 2^7 fact combinations — READY only when mask == 127."""
    kwargs = {
        field: bool(mask & (1 << i)) for i, field in enumerate(FACT_FIELDS)
    }
    checklist = PublicationChecklist.compute(make_facts(**kwargs))
    assert checklist.ready_to_publish is (mask == 127)


@pytest.mark.parametrize(
    ("left_stage", "right_stage"),
    list(itertools.combinations(CANONICAL_WORKFLOW, 2)),
)
def test_has_reached_asymmetric(left_stage, right_stage):
    if stage_index(left_stage) < stage_index(right_stage):
        assert has_reached(right_stage, left_stage) is True
        assert has_reached(left_stage, right_stage) is False
    else:
        assert has_reached(left_stage, right_stage) is True
        assert has_reached(right_stage, left_stage) is False


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
@pytest.mark.parametrize("event", list(WorkflowTransitionEvent))
def test_transition_matrix_consistent(stage, event):
    lawful = is_lawful_transition(stage, event)
    if lawful:
        target = next_workflow_state(stage, event)
        assert isinstance(target, WorkflowStage)
        wf = make_workflow(stage=stage).with_transition(event)
        assert wf.current_stage is target
    else:
        with pytest.raises(ValueError):
            next_workflow_state(stage, event)


@pytest.mark.parametrize("n_topics", range(0, 8))
def test_diff_scale_identical(n_topics):
    topics = [make_topic(f"t{i}", f"Title {i}") for i in range(n_topics)]
    left = make_curriculum("L", topics=topics)
    right = make_curriculum("R", topics=topics)
    assert CurriculumDiff.compare(left, right).is_identical


@pytest.mark.parametrize("remove_idx", range(5))
def test_diff_remove_each_topic(remove_idx):
    topics = [make_topic(f"t{i}") for i in range(5)]
    left = make_curriculum("L", topics=topics)
    right_topics = [t for i, t in enumerate(topics) if i != remove_idx]
    right = make_curriculum("R", topics=right_topics)
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.removed_topics) == 1
    assert diff.removed_topics[0].topic_id == f"t{remove_idx}"


@pytest.mark.parametrize("add_idx", range(5))
def test_diff_add_each_topic(add_idx):
    base = [make_topic(f"t{i}") for i in range(5) if i != add_idx]
    left = make_curriculum("L", topics=base)
    right = make_curriculum(
        "R", topics=[make_topic(f"t{i}") for i in range(5)]
    )
    diff = CurriculumDiff.compare(left, right)
    assert any(e.topic_id == f"t{add_idx}" for e in diff.added_topics)


@pytest.mark.parametrize("code", list(ChecklistItemCode))
def test_facts_fact_for_each_code(code):
    facts = WorkspacePublicationFacts.create(
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_approved=True,
        version_assigned=True,
        rollback_snapshot_created=True,
    )
    assert facts.fact_for(code) is True


@pytest.mark.parametrize("i", range(len(CHECKLIST_ORDER)))
def test_checklist_order_stable(i):
    assert CHECKLIST_ORDER[i] in ChecklistItemCode

"""Domain entity and workflow tests for Curriculum Studio."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.curriculum_studio.curriculum_workspace import (
    CurriculumWorkspace,
    WorkspaceStatus,
)
from app.domain.curriculum_studio.publication_checklist import (
    CHECKLIST_ORDER,
    ChecklistItemCode,
    PublicationChecklist,
)
from app.domain.curriculum_studio.studio_workflow import (
    LAWFUL_WORKFLOW_TRANSITIONS,
    StudioWorkflow,
    WorkflowTransitionEvent,
    is_lawful_transition,
    next_workflow_state,
)
from app.domain.curriculum_studio.workflow_stage import (
    CANONICAL_WORKFLOW,
    STAGE_LABELS,
    WorkflowStage,
    has_reached,
    next_stage,
    previous_stage,
    resolve_workflow_stage,
    stage_index,
    stage_label,
)
from tests.domain.curriculum_studio.helpers import (
    make_facts,
    make_ready_facts,
    make_workflow,
    make_workspace,
)

# ---------------------------------------------------------------------------
# Workflow stages
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("stage", list(WorkflowStage))
def test_stage_in_canonical_or_resolvable(stage):
    assert resolve_workflow_stage(stage) is stage
    assert resolve_workflow_stage(stage.value) is stage


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
def test_canonical_stage_has_label(stage):
    assert stage_label(stage) == STAGE_LABELS[stage]
    assert stage_label(stage.value) == STAGE_LABELS[stage]


@pytest.mark.parametrize(
    "token",
    ["subject", "CONTENT_SOURCES", "Validation", "preview", "approval", "publication"],
)
def test_resolve_stage_normalises(token):
    assert isinstance(resolve_workflow_stage(token), WorkflowStage)


@pytest.mark.parametrize("bad", ["", "  ", "unknown", "publish"])
def test_resolve_stage_rejects_bad(bad):
    with pytest.raises(ValueError):
        resolve_workflow_stage(bad)


def test_canonical_workflow_order():
    assert CANONICAL_WORKFLOW == (
        WorkflowStage.SUBJECT,
        WorkflowStage.CONTENT_SOURCES,
        WorkflowStage.VALIDATION,
        WorkflowStage.PREVIEW,
        WorkflowStage.APPROVAL,
        WorkflowStage.PUBLICATION,
    )


@pytest.mark.parametrize(
    ("current", "milestone", "expected"),
    [
        ("subject", "subject", True),
        ("preview", "validation", True),
        ("validation", "preview", False),
        ("publication", "subject", True),
    ],
)
def test_has_reached(current, milestone, expected):
    assert has_reached(current, milestone) is expected


@pytest.mark.parametrize(
    ("stage", "nxt"),
    [
        (WorkflowStage.SUBJECT, WorkflowStage.CONTENT_SOURCES),
        (WorkflowStage.CONTENT_SOURCES, WorkflowStage.VALIDATION),
        (WorkflowStage.VALIDATION, WorkflowStage.PREVIEW),
        (WorkflowStage.PREVIEW, WorkflowStage.APPROVAL),
        (WorkflowStage.APPROVAL, WorkflowStage.PUBLICATION),
        (WorkflowStage.PUBLICATION, None),
    ],
)
def test_next_stage(stage, nxt):
    assert next_stage(stage) is nxt


@pytest.mark.parametrize(
    ("stage", "prev"),
    [
        (WorkflowStage.SUBJECT, None),
        (WorkflowStage.CONTENT_SOURCES, WorkflowStage.SUBJECT),
        (WorkflowStage.PUBLICATION, WorkflowStage.APPROVAL),
    ],
)
def test_previous_stage(stage, prev):
    assert previous_stage(stage) is prev


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
def test_stage_index_matches_order(stage):
    assert stage_index(stage) == CANONICAL_WORKFLOW.index(stage)


# ---------------------------------------------------------------------------
# Studio workflow transitions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
def test_advance_or_terminal(stage):
    nxt = next_stage(stage)
    if nxt is None:
        assert not is_lawful_transition(stage, WorkflowTransitionEvent.ADVANCE)
    else:
        assert next_workflow_state(stage, "advance") is nxt


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
def test_retreat_or_initial(stage):
    prev = previous_stage(stage)
    if prev is None:
        assert not is_lawful_transition(stage, WorkflowTransitionEvent.RETREAT)
    else:
        assert next_workflow_state(stage, "retreat") is prev


@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
def test_reset_always_to_subject(stage):
    assert next_workflow_state(stage, WorkflowTransitionEvent.RESET) is (
        WorkflowStage.SUBJECT
    )


@pytest.mark.parametrize(
    "event",
    [
        WorkflowTransitionEvent.JUMP_TO_SUBJECT,
        WorkflowTransitionEvent.JUMP_TO_CONTENT_SOURCES,
        WorkflowTransitionEvent.JUMP_TO_VALIDATION,
        WorkflowTransitionEvent.JUMP_TO_PREVIEW,
        WorkflowTransitionEvent.JUMP_TO_APPROVAL,
        WorkflowTransitionEvent.JUMP_TO_PUBLICATION,
    ],
)
@pytest.mark.parametrize("stage", list(CANONICAL_WORKFLOW))
def test_jumps_lawful_from_every_stage(stage, event):
    assert is_lawful_transition(stage, event)
    assert (stage, event) in LAWFUL_WORKFLOW_TRANSITIONS


def test_workflow_with_transition_records_history():
    wf = make_workflow()
    advanced = wf.with_transition("advance", actor_id="founder-1", reason="go")
    assert advanced.current_stage is WorkflowStage.CONTENT_SOURCES
    assert advanced.transition_count == 1
    assert advanced.history[0].actor_id == "founder-1"
    assert advanced.highest_stage_reached is WorkflowStage.CONTENT_SOURCES


def test_workflow_retreat_keeps_highest():
    wf = make_workflow(stage=WorkflowStage.VALIDATION)
    # Simulate having reached validation as highest
    wf = StudioWorkflow.create(
        "wf-1",
        "ws-1",
        current_stage=WorkflowStage.VALIDATION,
        highest_stage_reached=WorkflowStage.VALIDATION,
    )
    retreated = wf.with_transition("retreat")
    assert retreated.current_stage is WorkflowStage.CONTENT_SOURCES
    assert retreated.highest_stage_reached is WorkflowStage.VALIDATION


def test_workflow_rejects_empty_ids():
    with pytest.raises(ValueError):
        StudioWorkflow.create("", "ws-1")
    with pytest.raises(ValueError):
        StudioWorkflow.create("wf-1", "  ")


def test_workflow_frozen():
    wf = make_workflow()
    with pytest.raises(FrozenInstanceError):
        wf.current_stage = WorkflowStage.PREVIEW  # type: ignore[misc]


def test_illegal_event_raises():
    with pytest.raises(ValueError):
        next_workflow_state(WorkflowStage.SUBJECT, "not_an_event")


# ---------------------------------------------------------------------------
# Publication checklist
# ---------------------------------------------------------------------------


def test_checklist_all_pending_by_default():
    checklist = PublicationChecklist.compute(make_facts())
    assert checklist.ready_to_publish is False
    assert checklist.satisfied_count == 0
    assert checklist.pending_count == len(CHECKLIST_ORDER)


def test_checklist_ready_when_all_facts_true():
    checklist = PublicationChecklist.compute(make_ready_facts())
    assert checklist.ready_to_publish is True
    assert checklist.item(ChecklistItemCode.READY_TO_PUBLISH).satisfied is True


@pytest.mark.parametrize("code", list(CHECKLIST_ORDER[:-1]))
def test_checklist_ready_requires_each_prerequisite(code):
    kwargs = {
        "cmp_uploaded": True,
        "official_syllabus_uploaded": True,
        "validation_passed": True,
        "blueprint_assigned": True,
        "preview_approved": True,
        "version_assigned": True,
        "rollback_snapshot_created": True,
    }
    field_map = {
        ChecklistItemCode.CMP_UPLOADED: "cmp_uploaded",
        ChecklistItemCode.OFFICIAL_SYLLABUS_UPLOADED: "official_syllabus_uploaded",
        ChecklistItemCode.VALIDATION_PASSED: "validation_passed",
        ChecklistItemCode.BLUEPRINT_ASSIGNED: "blueprint_assigned",
        ChecklistItemCode.PREVIEW_APPROVED: "preview_approved",
        ChecklistItemCode.VERSION_ASSIGNED: "version_assigned",
        ChecklistItemCode.ROLLBACK_SNAPSHOT_CREATED: "rollback_snapshot_created",
    }
    kwargs[field_map[code]] = False
    checklist = PublicationChecklist.compute(make_facts(**kwargs))
    assert checklist.ready_to_publish is False
    assert code in checklist.blocking_codes


@pytest.mark.parametrize("code", list(ChecklistItemCode))
def test_checklist_item_labels(code):
    checklist = PublicationChecklist.compute(make_facts())
    item = checklist.item(code)
    assert item.label
    assert item.code is code


def test_checklist_order_ends_with_ready():
    assert CHECKLIST_ORDER[-1] is ChecklistItemCode.READY_TO_PUBLISH


def test_checklist_never_manually_toggled_concept():
    """Facts drive checklist — flipping a fact recomputes, no set_item API."""
    facts = make_facts(cmp_uploaded=True)
    c1 = PublicationChecklist.compute(facts)
    assert c1.item(ChecklistItemCode.CMP_UPLOADED).satisfied is True
    facts2 = make_facts(cmp_uploaded=False)
    c2 = PublicationChecklist.compute(facts2)
    assert c2.item(ChecklistItemCode.CMP_UPLOADED).satisfied is False


# ---------------------------------------------------------------------------
# Workspace
# ---------------------------------------------------------------------------


def test_workspace_create_defaults():
    ws = make_workspace()
    assert ws.subject_code == "CS1"
    assert ws.current_stage is WorkflowStage.SUBJECT
    assert ws.ready_to_publish is False


def test_workspace_ready_with_facts():
    ws = make_workspace(facts=make_ready_facts())
    assert ws.ready_to_publish is True


def test_workspace_normalises_subject_code():
    ws = CurriculumWorkspace.create("ws-x", "cs1")
    assert ws.subject_code == "CS1"


@pytest.mark.parametrize("status", list(WorkspaceStatus))
def test_workspace_status_roundtrip(status):
    ws = make_workspace().with_status(status)
    assert ws.status is status


def test_workspace_rejects_negative_workload():
    with pytest.raises(ValueError):
        CurriculumWorkspace.create("ws-1", "CS1", estimated_workload_hours=-1)


def test_workspace_with_facts_immutable_original():
    ws = make_workspace()
    updated = ws.with_facts(make_ready_facts())
    assert ws.ready_to_publish is False
    assert updated.ready_to_publish is True


def test_workspace_frozen():
    ws = make_workspace()
    with pytest.raises(FrozenInstanceError):
        ws.subject_code = "XX"  # type: ignore[misc]

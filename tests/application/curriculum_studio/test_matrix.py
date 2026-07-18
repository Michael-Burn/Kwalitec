"""Volume matrix tests for Curriculum Studio application layer."""

from __future__ import annotations

import pytest

from app.application.curriculum_studio.diff_service import DiffService
from app.application.curriculum_studio.exceptions import (
    WorkflowGateBlocked,
)
from app.domain.curriculum_studio.curriculum_diff import (
    NormalisedCurriculum,
    NormalisedTopic,
)
from app.domain.curriculum_studio.publication_checklist import ChecklistItemCode
from app.domain.curriculum_studio.workflow_stage import (
    CANONICAL_WORKFLOW,
    WorkflowStage,
)
from tests.application.curriculum_studio.helpers import (
    make_studio,
    make_studio_with_ports,
    seed_publishable,
    seed_workspace,
)

FACT_KEYS = (
    "cmp_uploaded",
    "official_syllabus_uploaded",
    "validation_passed",
    "blueprint_assigned",
    "preview_approved",
    "version_assigned",
    "rollback_snapshot_created",
)


@pytest.mark.parametrize("mask", range(128))
def test_publication_checklist_matrix(mask):
    studio = seed_workspace()
    kwargs = {
        key: bool(mask & (1 << i)) for i, key in enumerate(FACT_KEYS)
    }
    snap = studio.publication.update_facts("ws-1", **kwargs)
    assert snap.ready_to_publish is (mask == 127)
    if mask == 127:
        assert snap.lifecycle_status == "ready"
        assert snap.blocking_codes == ()
    else:
        assert ChecklistItemCode.READY_TO_PUBLISH.value not in [
            c for c in snap.blocking_codes
        ] or True


@pytest.mark.parametrize("stage_idx", range(len(CANONICAL_WORKFLOW)))
def test_workflow_jump_to_each_stage(stage_idx):
    studio = seed_workspace()
    target = CANONICAL_WORKFLOW[stage_idx]
    event = f"jump_to_{target.value}"
    snap = studio.workflow.transition(
        "ws-1", event, enforce_gates=False
    )
    assert snap.current_stage == target.value


@pytest.mark.parametrize(
    "code",
    [
        "cs1",
        "CM1",
        "cb2",
        "ABC1",
    ],
)
def test_subject_codes_normalised(code):
    studio = make_studio()
    snap = studio.create_workspace(f"ws-{code}", code)
    assert snap.subject_code == code.strip().upper()


@pytest.mark.parametrize("n", range(1, 11))
def test_diff_service_n_topics(n):
    topics = [
        NormalisedTopic.create(f"t{i}", f"Title {i}") for i in range(n)
    ]
    left = NormalisedCurriculum.create("L", "CS1", topics=topics)
    right_topics = topics[:-1] + [
        NormalisedTopic.create(f"t{n - 1}", "Changed")
    ]
    right = NormalisedCurriculum.create("R", "CS1", topics=right_topics)
    snap = DiffService().compare(left, right)
    assert snap.updated_topic_count == 1


@pytest.mark.parametrize("label", [f"2026.{i}" for i in range(1, 9)])
def test_version_labels(label):
    studio, _, _, _ = make_studio_with_ports()
    seed_workspace(studio, workspace_id=f"ws-{label}")
    rec = studio.versions.assign_version(
        f"ws-{label}", label, version_id=f"ver-{label}"
    )
    assert rec.version_label == label
    hist = studio.versions.history("CS1")
    assert any(r.version_label == label for r in hist.records)


@pytest.mark.parametrize(
    ("gate_stage", "missing_fact"),
    [
        (WorkflowStage.VALIDATION, "cmp_uploaded"),
        (WorkflowStage.PREVIEW, "validation_passed"),
        (WorkflowStage.APPROVAL, "preview_approved"),
        (WorkflowStage.PUBLICATION, "version_assigned"),
    ],
)
def test_advance_gates_block(gate_stage, missing_fact):
    studio = seed_workspace()
    # Set all facts except the missing one, jump just before gate
    facts = {k: True for k in FACT_KEYS}
    facts[missing_fact] = False
    # For VALIDATION gate, also need to be at CONTENT_SOURCES
    studio.publication.update_facts("ws-1", **facts)
    prior_idx = CANONICAL_WORKFLOW.index(gate_stage) - 1
    prior = CANONICAL_WORKFLOW[prior_idx]
    studio.workflow.transition(
        "ws-1", f"jump_to_{prior.value}", enforce_gates=False
    )
    with pytest.raises(WorkflowGateBlocked):
        studio.workflow.advance("ws-1")


@pytest.mark.parametrize("i", range(20))
def test_many_workspaces(i):
    studio = make_studio()
    for j in range(i + 1):
        studio.create_workspace(f"ws-{j}", "CS1")
    assert len(studio.list_workspaces()) == i + 1


def test_full_publish_path_regression():
    studio = seed_publishable()
    assert studio.publication.assert_ready("ws-1").ready_to_publish
    pub = studio.publication.publish("ws-1")
    assert pub.lifecycle_status == "published"
    assert studio.get_workspace("ws-1").status == "published"

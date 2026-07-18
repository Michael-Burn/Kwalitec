"""Diff, version history, validation, preview domain tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.curriculum_studio.curriculum_diff import (
    CurriculumDiff,
    DiffChangeKind,
    NormalisedCurriculum,
)
from app.domain.curriculum_studio.preview_summary import (
    PreviewNode,
    PreviewReadiness,
    PreviewSummary,
)
from app.domain.curriculum_studio.publication_checklist import PublicationChecklist
from app.domain.curriculum_studio.publication_summary import (
    PublicationLifecycleStatus,
    PublicationSummary,
)
from app.domain.curriculum_studio.validation_summary import (
    ValidationFinding,
    ValidationFindingSeverity,
    ValidationReadiness,
    ValidationSummary,
)
from app.domain.curriculum_studio.version_history import (
    StudioVersionStatus,
    VersionHistory,
    is_lawful_version_transition,
)
from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from tests.domain.curriculum_studio.helpers import (
    make_curriculum,
    make_ready_facts,
    make_topic,
    make_version_record,
)

# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------


def test_diff_identical_curricula():
    left = make_curriculum("a")
    right = make_curriculum("b")
    diff = CurriculumDiff.compare(left, right)
    assert diff.is_identical
    assert diff.change_count == 0


def test_diff_added_topic():
    left = make_curriculum(topics=[make_topic("t1")])
    right = make_curriculum(
        curriculum_id="r",
        topics=[make_topic("t1"), make_topic("t2", "Topic 2")],
    )
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.added_topics) == 1
    assert diff.added_topics[0].topic_id == "t2"


def test_diff_removed_topic():
    left = make_curriculum(topics=[make_topic("t1"), make_topic("t2")])
    right = make_curriculum(curriculum_id="r", topics=[make_topic("t1")])
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.removed_topics) == 1
    assert diff.removed_topics[0].topic_id == "t2"


def test_diff_updated_topic_title():
    left = make_curriculum(topics=[make_topic("t1", "Old")])
    right = make_curriculum(
        curriculum_id="r", topics=[make_topic("t1", "New")]
    )
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.updated_topics) == 1


def test_diff_objective_change():
    left = make_curriculum(
        topics=[make_topic("t1", objectives=("a",))]
    )
    right = make_curriculum(
        curriculum_id="r",
        topics=[make_topic("t1", objectives=("a", "b"))],
    )
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.of_kind(DiffChangeKind.LEARNING_OBJECTIVE_CHANGE)) == 1


def test_diff_prerequisite_change():
    left = make_curriculum(
        topics=[make_topic("t1", prerequisites=("p1",))]
    )
    right = make_curriculum(
        curriculum_id="r",
        topics=[make_topic("t1", prerequisites=("p2",))],
    )
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.of_kind(DiffChangeKind.PREREQUISITE_CHANGE)) == 1


def test_diff_metadata_change():
    left = make_curriculum(metadata={"year": "2026"})
    right = make_curriculum(curriculum_id="r", metadata={"year": "2027"})
    diff = CurriculumDiff.compare(left, right)
    assert len(diff.of_kind(DiffChangeKind.METADATA_CHANGE)) == 1


def test_diff_topic_metadata_change():
    left = make_curriculum(
        topics=[make_topic("t1", metadata={"k": "1"})]
    )
    right = make_curriculum(
        curriculum_id="r",
        topics=[make_topic("t1", metadata={"k": "2"})],
    )
    diff = CurriculumDiff.compare(left, right)
    assert any(
        e.kind is DiffChangeKind.METADATA_CHANGE for e in diff.entries
    )


def test_diff_deterministic_order():
    left = make_curriculum(
        topics=[make_topic("a"), make_topic("b"), make_topic("c")]
    )
    right = make_curriculum(
        curriculum_id="r",
        topics=[make_topic("b"), make_topic("d")],
    )
    d1 = CurriculumDiff.compare(left, right, diff_id="x")
    d2 = CurriculumDiff.compare(left, right, diff_id="x")
    assert [e.path for e in d1.entries] == [e.path for e in d2.entries]


def test_diff_rejects_duplicate_topics():
    with pytest.raises(ValueError, match="duplicate"):
        NormalisedCurriculum.create(
            "c",
            "CS1",
            topics=[make_topic("t1"), make_topic("t1")],
        )


@pytest.mark.parametrize("kind", list(DiffChangeKind))
def test_diff_change_kinds_exist(kind):
    assert kind.value


def test_normalised_topic_frozen():
    t = make_topic()
    with pytest.raises(FrozenInstanceError):
        t.title = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Version history
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status", list(StudioVersionStatus))
def test_version_status_properties(status):
    rec = make_version_record(status=status, rollback_snapshot_id="rb-1")
    assert rec.is_draft is (status is StudioVersionStatus.DRAFT)
    assert rec.is_published is (status is StudioVersionStatus.PUBLISHED)
    assert rec.is_archived is (status is StudioVersionStatus.ARCHIVED)


@pytest.mark.parametrize(
    ("cur", "tgt", "ok"),
    [
        ("draft", "published", True),
        ("published", "archived", True),
        ("draft", "archived", False),
        ("archived", "published", False),
        ("published", "draft", False),
        ("draft", "draft", True),
    ],
)
def test_version_transitions(cur, tgt, ok):
    assert is_lawful_version_transition(cur, tgt) is ok


def test_version_history_lookup():
    r1 = make_version_record("v1", version_label="2026.1")
    r2 = make_version_record("v2", version_label="2026.2")
    hist = VersionHistory.create("CS1", [r1, r2])
    assert hist.get("v1") is not None
    assert hist.by_label("2026.2") is not None
    assert hist.get("missing") is None


def test_version_history_filters():
    draft = make_version_record("v1", status=StudioVersionStatus.DRAFT)
    pub = make_version_record(
        "v2",
        status=StudioVersionStatus.PUBLISHED,
        rollback_snapshot_id="rb",
    )
    arch = make_version_record(
        "v3",
        status=StudioVersionStatus.ARCHIVED,
        rollback_snapshot_id="rb2",
    )
    hist = VersionHistory.create("CS1", [draft, pub, arch])
    assert len(hist.drafts()) == 1
    assert len(hist.published()) == 1
    assert len(hist.archived()) == 1
    assert len(hist.rollback_eligible()) == 2
    assert hist.current_published().version_id == "v2"


def test_version_history_subject_mismatch():
    with pytest.raises(ValueError):
        VersionHistory.create("CS1", [make_version_record(subject_code="CM1")])


def test_rollback_eligible_requires_snapshot():
    pub = make_version_record(status=StudioVersionStatus.PUBLISHED)
    assert pub.rollback_eligible is False
    pub2 = pub.with_status(
        StudioVersionStatus.PUBLISHED, rollback_snapshot_id="rb"
    )
    assert pub2.rollback_eligible is True


# ---------------------------------------------------------------------------
# Validation / Preview / Publication summaries
# ---------------------------------------------------------------------------


def test_validation_summary_passed():
    summary = ValidationSummary.create(
        "s1",
        "ws-1",
        detected_sections=("a",),
        detected_objectives=("o",),
    )
    assert summary.passed is True
    assert summary.readiness is ValidationReadiness.PASSED


def test_validation_summary_failed_on_errors():
    err = ValidationFinding.create(
        "x", "bad", severity=ValidationFindingSeverity.ERROR
    )
    summary = ValidationSummary.create(
        "s1", "ws-1", errors=[err], detected_sections=("a",)
    )
    assert summary.passed is False
    assert summary.blocks_publication is True


@pytest.mark.parametrize("sev", list(ValidationFindingSeverity))
def test_validation_finding_severity(sev):
    f = ValidationFinding.create("c", "m", severity=sev)
    assert f.severity is sev


def test_preview_summary_hierarchy():
    node = PreviewNode.create("n1", "Section", kind="section")
    summary = PreviewSummary.create(
        "p1",
        "ws-1",
        hierarchy=[node],
        validation_passed=True,
        subject_code="cs1",
    )
    assert summary.node_count == 1
    assert summary.subject_code == "CS1"
    assert summary.readiness is PreviewReadiness.READY_FOR_REVIEW


def test_preview_approve_readiness():
    summary = PreviewSummary.create(
        "p1", "ws-1", readiness=PreviewReadiness.APPROVED
    )
    assert summary.is_approved is True


def test_preview_rejects_negative_hours():
    with pytest.raises(ValueError):
        PreviewSummary.create("p1", "ws-1", estimated_workload_hours=-0.1)


def test_publication_summary_ready():
    checklist = PublicationChecklist.compute(make_ready_facts())
    summary = PublicationSummary.create(
        "ps1",
        "ws-1",
        "CS1",
        checklist=checklist,
        workflow_stage=WorkflowStage.PUBLICATION,
    )
    assert summary.ready_to_publish is True
    assert summary.lifecycle_status is PublicationLifecycleStatus.READY


@pytest.mark.parametrize("status", list(PublicationLifecycleStatus))
def test_publication_lifecycle_statuses(status):
    checklist = (
        PublicationChecklist.compute(make_ready_facts())
        if status is PublicationLifecycleStatus.READY
        else None
    )
    summary = PublicationSummary.create(
        "ps1",
        "ws-1",
        "CS1",
        lifecycle_status=status,
        checklist=checklist,
    )
    if status is PublicationLifecycleStatus.READY:
        assert summary.lifecycle_status is PublicationLifecycleStatus.READY
        assert summary.ready_to_publish is True
    elif status is PublicationLifecycleStatus.DRAFT:
        assert summary.lifecycle_status in {
            PublicationLifecycleStatus.DRAFT,
            PublicationLifecycleStatus.BLOCKED,
        }
    else:
        assert summary.lifecycle_status is status


def test_version_record_frozen():
    rec = make_version_record()
    with pytest.raises(FrozenInstanceError):
        rec.version_label = "x"  # type: ignore[misc]

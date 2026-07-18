"""Domain entity tests for Curriculum Management."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.curriculum_management.approval import ApprovalDecision
from app.domain.curriculum_management.curriculum_asset import AssetKind
from app.domain.curriculum_management.publication import Publication
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
    has_reached,
    is_editable_publication_state,
    is_terminal_publication_state,
    next_publication_state,
    pipeline_index,
    resolve_publication_state,
)
from app.domain.curriculum_management.subject_identifier import SubjectIdentifier
from app.domain.curriculum_management.subject_metadata import SubjectMetadata
from app.domain.curriculum_management.validation_report import (
    ValidationIssueCode,
    ValidationSeverity,
)
from tests.domain.curriculum_management.helpers import (
    make_approval,
    make_asset,
    make_assignment,
    make_identifier,
    make_issue,
    make_metadata,
    make_notes,
    make_package,
    make_report,
    make_subject,
    make_version,
)

# ---------------------------------------------------------------------------
# SubjectIdentifier
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("code", ["CS1", "CM1", "CB2", "ABC123", "Z9"])
def test_identifier_accepts_valid_codes(code):
    assert SubjectIdentifier.create(code).code == code


@pytest.mark.parametrize("code", ["cs1", " Cm1 ", "cb2"])
def test_identifier_normalises_case(code):
    assert SubjectIdentifier.create(code).code == code.strip().upper()


@pytest.mark.parametrize("code", ["", "  ", "1CS", "c", "toolongcodeeeeeeeeee", "CS-1"])
def test_identifier_rejects_invalid(code):
    with pytest.raises(ValueError):
        SubjectIdentifier.create(code)


def test_identifier_str():
    assert str(make_identifier("CS1")) == "CS1"


def test_identifier_frozen():
    ident = make_identifier()
    with pytest.raises(FrozenInstanceError):
        ident.code = "XX"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# SubjectMetadata
# ---------------------------------------------------------------------------


def test_metadata_create_defaults():
    md = SubjectMetadata.create("Title")
    assert md.title == "Title"
    assert md.locale == "en-GB"
    assert md.tags == ()


def test_metadata_with_tags():
    md = make_metadata().with_tags(["a", "b"])
    assert md.tags == ("a", "b")


def test_metadata_rejects_empty_title():
    with pytest.raises(ValueError, match="title"):
        SubjectMetadata.create("  ")


def test_metadata_blank_exam_board_becomes_none():
    md = SubjectMetadata.create("T", exam_board="  ")
    assert md.exam_board is None


def test_metadata_frozen():
    md = make_metadata()
    with pytest.raises(FrozenInstanceError):
        md.title = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------


def test_subject_create_and_code():
    subject = make_subject(code="CM1", title="Core Maths")
    assert subject.code == "CM1"
    assert subject.title == "Core Maths"
    assert subject.version_count == 0


def test_subject_with_version():
    subject = make_subject().with_version("v1").with_version("v2")
    assert subject.version_ids == ("v1", "v2")
    assert subject.version_count == 2


def test_subject_duplicate_version_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        make_subject(version_ids=("v1", "v1"))


def test_subject_active_must_be_known():
    with pytest.raises(ValueError, match="active_version_id"):
        make_subject(version_ids=("v1",), active_version_id="v2")


def test_subject_with_active_version():
    subject = make_subject(version_ids=("v1",)).with_active_version("v1")
    assert subject.active_version_id == "v1"
    cleared = subject.with_active_version(None)
    assert cleared.active_version_id is None


def test_subject_with_metadata():
    subject = make_subject().with_metadata(SubjectMetadata.create("New"))
    assert subject.title == "New"


def test_subject_frozen():
    subject = make_subject()
    with pytest.raises(FrozenInstanceError):
        subject.subject_id = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# CurriculumAsset / Package
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kind,expected",
    [
        ("cmp", AssetKind.CMP),
        ("syllabus", AssetKind.SYLLABUS),
        ("learning_objectives", AssetKind.LEARNING_OBJECTIVES),
        ("formula_sheet", AssetKind.FORMULA_SHEET),
        ("supporting_document", AssetKind.SUPPORTING_DOCUMENT),
        ("objectives", AssetKind.LEARNING_OBJECTIVES),
        ("formula", AssetKind.FORMULA_SHEET),
    ],
)
def test_asset_kind_aliases(kind, expected):
    asset = make_asset(kind=kind)
    assert asset.kind is expected


def test_asset_rejects_data_uri():
    with pytest.raises(ValueError, match="data URI"):
        make_asset(reference="data:application/pdf;base64,AAA")


def test_asset_rejects_pdf_marker():
    with pytest.raises(ValueError, match="PDF"):
        make_asset(reference="%PDF-1.4 binary")


def test_asset_rejects_empty_reference():
    with pytest.raises(ValueError, match="reference"):
        make_asset(reference="  ")


def test_package_with_and_without_asset():
    package = make_package(with_syllabus=True, with_cmp=True)
    assert package.asset_count == 2
    assert package.has_kind(AssetKind.SYLLABUS)
    assert package.asset_by_id("a-syllabus") is not None
    trimmed = package.without_asset("a-cmp")
    assert trimmed.asset_count == 1
    with pytest.raises(ValueError, match="not found"):
        package.without_asset("missing")


def test_package_duplicate_asset_rejected():
    package = make_package()
    with pytest.raises(ValueError, match="duplicate"):
        package.with_asset(make_asset("a-syllabus"))


def test_package_assets_of_kind():
    package = make_package(with_syllabus=True, with_cmp=True)
    assert len(package.assets_of_kind(AssetKind.CMP)) == 1


# ---------------------------------------------------------------------------
# BlueprintAssignment / Validation / Approval / Notes
# ---------------------------------------------------------------------------


def test_assignment_create():
    asg = make_assignment(notes="explicit")
    assert asg.section_ref == "ch1"
    assert asg.notes == "explicit"


def test_issue_blocking_codes():
    issue = make_issue(ValidationIssueCode.MISSING_SYLLABUS)
    assert issue.is_blocking


def test_issue_warning_not_blocking():
    issue = make_issue(
        ValidationIssueCode.MISSING_CMP,
        severity=ValidationSeverity.WARNING,
    )
    assert not issue.is_blocking


def test_report_passed_when_no_blocking():
    report = make_report(
        issues=(
            make_issue(
                ValidationIssueCode.MISSING_CMP,
                severity=ValidationSeverity.WARNING,
            ),
        )
    )
    assert report.passed
    assert not report.blocks_publication


def test_report_failed_when_blocking():
    report = make_report(issues=(make_issue(),))
    assert not report.passed
    assert report.blocking_issues


def test_approval_is_approved():
    assert make_approval().is_approved
    rejected = make_approval(decision=ApprovalDecision.REJECTED)
    assert not rejected.is_approved


def test_release_notes_with_entry():
    notes = make_notes(texts=("A",))
    notes2 = notes.with_entry(
        __import__(
            "app.domain.curriculum_management.release_notes",
            fromlist=["ReleaseNoteEntry"],
        ).ReleaseNoteEntry.create("e99", "B")
    )
    assert notes2.texts() == ("A", "B")
    assert notes2.entry_count == 2


# ---------------------------------------------------------------------------
# Publication state machine
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("draft", PublicationState.DRAFT),
        ("UPLOADED", PublicationState.UPLOADED),
        ("blueprint-assigned", PublicationState.BLUEPRINT_ASSIGNED),
        ("preview ready", PublicationState.PREVIEW_READY),
        (PublicationState.APPROVED, PublicationState.APPROVED),
    ],
)
def test_resolve_publication_state(raw, expected):
    assert resolve_publication_state(raw) is expected


def test_resolve_publication_state_unknown():
    with pytest.raises(ValueError):
        resolve_publication_state("nope")


def test_forward_pipeline_transitions():
    state = PublicationState.DRAFT
    events = [
        PublicationTransitionEvent.MARK_UPLOADED,
        PublicationTransitionEvent.MARK_VALIDATED,
        PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
        PublicationTransitionEvent.MARK_PREVIEW_READY,
        PublicationTransitionEvent.MARK_APPROVED,
        PublicationTransitionEvent.MARK_PUBLISHED,
        PublicationTransitionEvent.MARK_ARCHIVED,
    ]
    for event in events:
        nxt = next_publication_state(state, event)
        assert nxt is not None
        state = nxt
    assert state is PublicationState.ARCHIVED
    assert is_terminal_publication_state(state)


def test_illegal_transition_returns_none():
    assert (
        next_publication_state(
            PublicationState.DRAFT,
            PublicationTransitionEvent.MARK_PUBLISHED,
        )
        is None
    )


@pytest.mark.parametrize(
    "state,editable",
    [
        (PublicationState.DRAFT, True),
        (PublicationState.UPLOADED, True),
        (PublicationState.APPROVED, False),
        (PublicationState.PUBLISHED, False),
        (PublicationState.ARCHIVED, False),
    ],
)
def test_is_editable(state, editable):
    assert is_editable_publication_state(state) is editable


def test_pipeline_index_and_has_reached():
    assert pipeline_index(PublicationState.VALIDATED) == 2
    assert pipeline_index(PublicationState.ARCHIVED) == -1
    assert has_reached(PublicationState.APPROVED, PublicationState.VALIDATED)
    assert not has_reached(PublicationState.DRAFT, PublicationState.UPLOADED)


def test_publication_transition_records_history():
    pub = Publication.create("p1", "v1")
    pub2 = pub.transition(
        PublicationTransitionEvent.MARK_UPLOADED,
        actor_id="u1",
        reason="upload",
        occurred_at="t1",
    )
    assert pub2.state is PublicationState.UPLOADED
    assert pub2.history is not None
    assert pub2.history.entry_count == 1
    assert pub2.history.latest().actor_id == "u1"


def test_publication_illegal_transition_raises():
    pub = Publication.create("p1", "v1")
    with pytest.raises(ValueError, match="Illegal"):
        pub.transition(PublicationTransitionEvent.MARK_PUBLISHED)


def test_publication_published_sets_timestamp():
    pub = Publication.create("p1", "v1", state=PublicationState.APPROVED)
    pub2 = pub.transition(
        PublicationTransitionEvent.MARK_PUBLISHED,
        occurred_at="2026-01-01",
    )
    assert pub2.published_at == "2026-01-01"
    assert pub2.is_published


# ---------------------------------------------------------------------------
# SubjectVersion
# ---------------------------------------------------------------------------


def test_version_display_name_and_state():
    version = make_version(subject_id="CS1-sub", version_label="2026.1")
    assert version.display_name == "CS1-sub 2026.1"
    assert version.state is PublicationState.DRAFT


@pytest.mark.parametrize("label", ["2026", "26.1", "2026.1.0", "v2026.1"])
def test_version_rejects_bad_label(label):
    with pytest.raises(ValueError, match="version_label"):
        make_version(version_label=label)


def test_version_with_package_and_assignment():
    version = make_version(package=make_package())
    version = version.with_assignment(make_assignment())
    assert version.package is not None
    assert len(version.assignments) == 1


def test_version_with_validation_and_approval():
    version = make_version()
    version = version.with_validation_report(make_report())
    version = version.with_approval(make_approval())
    assert version.latest_validation is not None
    assert version.latest_approval is not None


def test_version_with_release_notes():
    version = make_version().with_release_notes(make_notes())
    assert version.release_notes is not None


def test_version_duplicate_section_refs_rejected():
    with pytest.raises(ValueError, match="duplicate section"):
        make_version(section_refs=("a", "a"))


def test_version_assignment_version_mismatch():
    with pytest.raises(ValueError, match="assignment version_id"):
        make_version(assignments=(make_assignment(version_id="other"),))

"""Publication state matrix and immutability domain tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.curriculum_management.publication_history import (
    PublicationHistory,
    PublicationHistoryEntry,
)
from app.domain.curriculum_management.publication_state import (
    LAWFUL_PUBLICATION_TRANSITIONS,
    PUBLICATION_PIPELINE,
    PublicationState,
    PublicationTransitionEvent,
    next_publication_state,
)
from tests.domain.curriculum_management.helpers import (
    make_approval,
    make_asset,
    make_assignment,
    make_history,
    make_issue,
    make_notes,
    make_package,
    make_report,
    make_subject,
    make_version,
)


@pytest.mark.parametrize(
    "from_state,event,to_state",
    [
        (frm, evt, to)
        for (frm, evt), to in LAWFUL_PUBLICATION_TRANSITIONS.items()
    ],
)
def test_lawful_transition_map(from_state, event, to_state):
    assert next_publication_state(from_state, event) is to_state


def test_pipeline_order():
    assert PUBLICATION_PIPELINE[0] is PublicationState.DRAFT
    assert PUBLICATION_PIPELINE[-1] is PublicationState.PUBLISHED
    assert PublicationState.ARCHIVED not in PUBLICATION_PIPELINE


@pytest.mark.parametrize("state", list(PublicationState))
def test_all_states_are_str_enum(state):
    assert isinstance(state.value, str)
    assert state.value == state.value.lower()


@pytest.mark.parametrize("event", list(PublicationTransitionEvent))
def test_all_events_are_str_enum(event):
    assert isinstance(event.value, str)


def test_history_with_entry_and_latest():
    hist = make_history()
    assert hist.latest() is None
    entry = PublicationHistoryEntry.create(
        "e1",
        PublicationState.DRAFT,
        PublicationState.UPLOADED,
        PublicationTransitionEvent.MARK_UPLOADED,
    )
    hist2 = hist.with_entry(entry)
    assert hist2.entry_count == 1
    assert hist2.latest() is entry


def test_history_duplicate_entry_rejected():
    entry = PublicationHistoryEntry.create(
        "e1",
        PublicationState.DRAFT,
        PublicationState.UPLOADED,
        PublicationTransitionEvent.MARK_UPLOADED,
    )
    with pytest.raises(ValueError, match="duplicate"):
        PublicationHistory.create("h1", "v1", entries=(entry, entry))


def test_domain_objects_frozen():
    subject = make_subject()
    with pytest.raises(FrozenInstanceError):
        subject.subject_id = "x"  # type: ignore[misc]
    version = make_version()
    with pytest.raises(FrozenInstanceError):
        version.version_label = "x"  # type: ignore[misc]
    asset = make_asset()
    with pytest.raises(FrozenInstanceError):
        asset.label = "x"  # type: ignore[misc]
    package = make_package()
    with pytest.raises(FrozenInstanceError):
        package.package_id = "x"  # type: ignore[misc]
    assignment = make_assignment()
    with pytest.raises(FrozenInstanceError):
        assignment.section_ref = "x"  # type: ignore[misc]
    report = make_report()
    with pytest.raises(FrozenInstanceError):
        report.passed = False  # type: ignore[misc]
    issue = make_issue()
    with pytest.raises(FrozenInstanceError):
        issue.message = "x"  # type: ignore[misc]
    approval = make_approval()
    with pytest.raises(FrozenInstanceError):
        approval.reviewer_id = "x"  # type: ignore[misc]
    notes = make_notes()
    with pytest.raises(FrozenInstanceError):
        notes.headline = "x"  # type: ignore[misc]
    history = make_history()
    with pytest.raises(FrozenInstanceError):
        history.history_id = "x"  # type: ignore[misc]


def test_version_package_version_mismatch():
    package = make_package(version_id="other")
    with pytest.raises(ValueError, match="package version_id"):
        make_version(package=package)


def test_notes_duplicate_entry_rejected():
    from app.domain.curriculum_management.release_notes import (
        ReleaseNoteEntry,
        ReleaseNotes,
    )

    entry = ReleaseNoteEntry.create("e1", "text")
    with pytest.raises(ValueError, match="duplicate"):
        ReleaseNotes.create("n1", "v1", entries=(entry, entry))

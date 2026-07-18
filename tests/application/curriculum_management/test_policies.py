"""Policy unit tests for Curriculum Management."""

from __future__ import annotations

import pytest

from app.application.curriculum_management.exceptions import PolicyViolation
from app.application.curriculum_management.policies.approval_policy import (
    ApprovalPolicy,
)
from app.application.curriculum_management.policies.publication_policy import (
    PublicationPolicy,
)
from app.application.curriculum_management.policies.validation_policy import (
    ValidationPolicy,
)
from app.application.curriculum_management.policies.version_policy import (
    VersionPolicy,
)
from app.domain.curriculum_management.approval import ApprovalDecision
from app.domain.curriculum_management.publication_state import (
    PublicationState,
    PublicationTransitionEvent,
)
from app.domain.curriculum_management.validation_report import (
    ValidationIssueCode,
)
from tests.domain.curriculum_management.helpers import (
    make_approval,
    make_assignment,
    make_package,
    make_report,
    make_subject,
    make_version,
)


@pytest.mark.parametrize(
    "state,event",
    [
        (PublicationState.DRAFT, PublicationTransitionEvent.MARK_UPLOADED),
        (PublicationState.UPLOADED, PublicationTransitionEvent.MARK_VALIDATED),
        (
            PublicationState.VALIDATED,
            PublicationTransitionEvent.MARK_BLUEPRINT_ASSIGNED,
        ),
        (
            PublicationState.BLUEPRINT_ASSIGNED,
            PublicationTransitionEvent.MARK_PREVIEW_READY,
        ),
        (
            PublicationState.PREVIEW_READY,
            PublicationTransitionEvent.MARK_APPROVED,
        ),
        (PublicationState.APPROVED, PublicationTransitionEvent.MARK_PUBLISHED),
        (PublicationState.PUBLISHED, PublicationTransitionEvent.MARK_ARCHIVED),
    ],
)
def test_publication_policy_allows_forward(state, event):
    nxt = PublicationPolicy.assert_transition_allowed(state, event)
    assert nxt is not None


def test_publication_policy_rejects_illegal():
    with pytest.raises(PolicyViolation):
        PublicationPolicy.assert_transition_allowed(
            PublicationState.DRAFT,
            PublicationTransitionEvent.MARK_PUBLISHED,
        )


def test_publication_policy_assert_not_archived():
    version = make_version(state=PublicationState.ARCHIVED)
    with pytest.raises(PolicyViolation, match="Archived"):
        PublicationPolicy.assert_not_archived(version)


def test_publication_policy_assert_can_publish():
    version = make_version(
        state=PublicationState.APPROVED,
        package=make_package(),
        assignments=(make_assignment(),),
    )
    version = version.with_validation_report(make_report())
    version = version.with_approval(make_approval())
    # empty report passes — ok
    PublicationPolicy.assert_can_publish(version)


def test_publication_policy_publish_requires_approval_record():
    version = make_version(state=PublicationState.APPROVED)
    version = version.with_validation_report(make_report())
    with pytest.raises(PolicyViolation, match="approval"):
        PublicationPolicy.assert_can_publish(version)


@pytest.mark.parametrize(
    "state,expected",
    [
        (PublicationState.DRAFT, PublicationTransitionEvent.MARK_UPLOADED),
        (PublicationState.APPROVED, PublicationTransitionEvent.MARK_PUBLISHED),
        (PublicationState.ARCHIVED, None),
    ],
)
def test_next_forward_event(state, expected):
    assert PublicationPolicy.next_forward_event(state) is expected


def test_version_policy_label():
    assert VersionPolicy.assert_valid_label("2026.1") == "2026.1"
    with pytest.raises(PolicyViolation):
        VersionPolicy.assert_valid_label("bad")


def test_version_policy_belongs_and_mutable():
    subject = make_subject(subject_id="sub-1")
    version = make_version(subject_id="sub-1")
    VersionPolicy.assert_belongs_to_subject(version, subject)
    with pytest.raises(PolicyViolation):
        VersionPolicy.assert_belongs_to_subject(
            make_version(subject_id="other"),
            subject,
        )
    VersionPolicy.assert_mutable(version)
    with pytest.raises(PolicyViolation):
        VersionPolicy.assert_mutable(
            make_version(state=PublicationState.PUBLISHED)
        )


def test_version_policy_compare_labels():
    assert VersionPolicy.compare_labels("2026.1", "2026.2") < 0
    assert VersionPolicy.compare_labels("2027.1", "2026.9") > 0
    assert VersionPolicy.compare_labels("2026.1", "2026.1") == 0


def test_version_policy_activate():
    subject = make_subject(subject_id="sub-1", version_ids=("ver-1",))
    version = make_version(
        version_id="ver-1",
        subject_id="sub-1",
        state=PublicationState.PUBLISHED,
    )
    VersionPolicy.assert_can_activate(subject, version)
    with pytest.raises(PolicyViolation):
        VersionPolicy.assert_can_activate(
            subject,
            make_version(
                version_id="ver-1",
                subject_id="sub-1",
                state=PublicationState.APPROVED,
            ),
        )


def test_approval_policy_can_approve():
    version = make_version(
        state=PublicationState.PREVIEW_READY,
        package=make_package(),
        assignments=(make_assignment(),),
    )
    version = version.with_validation_report(make_report())
    ApprovalPolicy.assert_can_approve(version)
    assert ApprovalPolicy.can_advance_to_approved(version)


def test_approval_policy_rejects_wrong_state():
    version = make_version(state=PublicationState.UPLOADED)
    assert not ApprovalPolicy.can_advance_to_approved(version)
    with pytest.raises(PolicyViolation):
        ApprovalPolicy.assert_can_approve(version)


def test_approval_policy_decision():
    ApprovalPolicy.assert_decision_is_approval(make_approval())
    with pytest.raises(PolicyViolation):
        ApprovalPolicy.assert_decision_is_approval(
            make_approval(decision=ApprovalDecision.REJECTED)
        )


def test_validation_policy_empty_package():
    issues = ValidationPolicy.collect_issues(make_version())
    codes = {i.code for i in issues}
    assert ValidationIssueCode.EMPTY_PACKAGE in codes
    assert ValidationIssueCode.MISSING_BLUEPRINT_ASSIGNMENT in codes
    assert not ValidationPolicy.is_ready_for_validation_gate(make_version())


def test_validation_policy_ready_version():
    version = make_version(
        package=make_package(with_syllabus=True, with_cmp=True),
        assignments=(make_assignment(),),
        section_refs=("ch1",),
    )
    issues = ValidationPolicy.collect_issues(version)
    assert not any(i.is_blocking for i in issues)
    assert ValidationPolicy.is_ready_for_validation_gate(version)


def test_validation_policy_duplicate_section_assignment():
    version = make_version(
        package=make_package(),
        assignments=(
            make_assignment("a1", section_ref="ch1"),
            make_assignment("a2", section_ref="ch1"),
        ),
    )
    # SubjectVersion.create rejects duplicate assignment ids but allows
    # same section via create path — with_assignment would append; here
    # create with two same sections should work if assignment ids differ.
    codes = {i.code for i in ValidationPolicy.collect_issues(version)}
    assert ValidationIssueCode.DUPLICATE_SECTION in codes


def test_validation_policy_case_insensitive_duplicate_topic():
    version = make_version(
        package=make_package(),
        assignments=(make_assignment(),),
        section_refs=("Topic-A", "topic-a"),
    )
    codes = {i.code for i in ValidationPolicy.collect_issues(version)}
    assert ValidationIssueCode.DUPLICATE_TOPIC in codes


def test_validation_policy_missing_section_assignment():
    version = make_version(
        package=make_package(),
        assignments=(make_assignment(section_ref="ch1"),),
        section_refs=("ch1", "ch2"),
    )
    issues = [
        i
        for i in ValidationPolicy.collect_issues(version)
        if i.code is ValidationIssueCode.MISSING_BLUEPRINT_ASSIGNMENT
        and i.section_ref == "ch2"
    ]
    assert issues

"""Core TeachingIntention aggregate lifecycle and behaviour tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import DiagnosisType, TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingIntentionId
from domain.education.teaching_intention import (
    IntentionIsActionableSpecification,
    IntentionIsAlignedSpecification,
    IntentionRevisionKind,
    IntentionStatus,
    IntentionStrengthLevel,
    TeachingIntentionCreated,
    TeachingIntentionRevised,
)
from tests.domain.education.teaching_intention.conftest import (
    make_diagnosis_ref,
    make_goal,
    make_intention,
    make_outcome,
    make_priority_ref,
    make_scope,
)


def test_create_emits_created_event_and_starts_draft() -> None:
    intention = make_intention()
    events = intention.pull_events()
    assert intention.is_draft()
    assert len(events) == 1
    assert isinstance(events[0], TeachingIntentionCreated)
    assert events[0].intention_type is TeachingIntentionType.STRENGTHEN_PREREQUISITE
    assert events[0].priority_count == 1
    assert events[0].diagnosis_count == 1


def test_activate_locks_type_and_emits_revised() -> None:
    intention = make_intention()
    intention.pull_events()
    intention.activate()
    assert intention.is_active()
    assert intention.is_activated()
    events = intention.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], TeachingIntentionRevised)
    assert events[0].revision_kind is IntentionRevisionKind.ACTIVATED


def test_cannot_change_type_after_activation() -> None:
    intention = make_intention(activate=True)
    with pytest.raises(EducationalInvariantViolation, match="after activation"):
        intention.revise(
            intention_type=TeachingIntentionType.IMPROVE_TRANSFER,
            goal=make_goal(intention_type=TeachingIntentionType.IMPROVE_TRANSFER),
            diagnosis_references=[
                make_diagnosis_ref(diagnosis_type=DiagnosisType.TRANSFER_WEAKNESS)
            ],
        )


def test_draft_may_change_intention_type_with_aligned_diagnosis() -> None:
    intention = make_intention()
    intention.revise(
        intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION,
        goal=make_goal(intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION),
        diagnosis_references=[
            make_diagnosis_ref(diagnosis_type=DiagnosisType.MISCONCEPTION)
        ],
    )
    assert intention.intention_type is TeachingIntentionType.REPAIR_MISCONCEPTION
    assert intention.is_draft()


def test_strengthen_and_weaken_require_activation() -> None:
    intention = make_intention()
    with pytest.raises(EducationalInvariantViolation, match="activated"):
        intention.strengthen()
    intention.activate()
    intention.strengthen()
    assert intention.strength.level is IntentionStrengthLevel.FIRM
    intention.weaken()
    assert intention.strength.level is IntentionStrengthLevel.MODERATE
    assert intention.is_revised()


def test_retired_cannot_be_strengthened() -> None:
    intention = make_intention(activate=True)
    intention.retire(reason="superseded by clearer diagnosis")
    assert intention.is_retired()
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        intention.strengthen()
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        intention.weaken()
    with pytest.raises(EducationalInvariantViolation, match="retired"):
        intention.revise(scope=make_scope(statement="new scope statement"))


def test_must_reference_priority() -> None:
    with pytest.raises(EducationalInvariantViolation, match="Priority"):
        make_intention(priority_references=[])


def test_must_possess_expected_outcome_and_scope() -> None:
    intention = make_intention()
    assert intention.expected_outcome.statement
    assert intention.scope.statement
    assert intention.goal.statement


def test_identity_equality() -> None:
    a = make_intention(intention_id="ti-eq")
    b = make_intention(intention_id="ti-eq")
    c = make_intention(intention_id="ti-other")
    assert a == b
    assert a != c
    assert hash(a) == hash(b)


def test_actionable_only_when_activated_and_aligned() -> None:
    draft = make_intention()
    assert not IntentionIsActionableSpecification().is_satisfied_by(draft)
    draft.activate()
    assert IntentionIsActionableSpecification().is_satisfied_by(draft)
    assert IntentionIsAlignedSpecification().is_satisfied_by(draft)


def test_revise_outcome_emits_outcome_amended() -> None:
    intention = make_intention(activate=True)
    intention.pull_events()
    intention.revise(
        expected_outcome=make_outcome(
            statement="Improved transfer under surface variation",
            success_evidence="Success on varied stems within syllabus scope",
        )
    )
    events = intention.pull_events()
    assert events[0].revision_kind is IntentionRevisionKind.OUTCOME_AMENDED
    assert intention.status is IntentionStatus.REVISED


def test_query_helpers() -> None:
    intention = make_intention(activate=True)
    assert intention.priority_count() == 1
    assert intention.diagnosis_count() == 1
    assert intention.hypothesis_count() == 1
    assert intention.has_priority(
        make_priority_ref().priority_id
    )
    assert "TeachingIntention" in repr(intention)


def test_create_requires_teaching_intention_id() -> None:
    with pytest.raises(EducationalInvariantViolation):
        TeachingIntentionId(" ")

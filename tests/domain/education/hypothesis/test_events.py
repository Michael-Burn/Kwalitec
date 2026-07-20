"""Domain event tests for Educational Hypothesis."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import HypothesisId
from domain.education.hypothesis import (
    ExplanatoryStrengthLevel,
    HypothesisCreated,
    HypothesisDiscarded,
    HypothesisKind,
    HypothesisRevised,
    PlausibilityLevel,
    RevisionForm,
)
from tests.domain.education.hypothesis.conftest import make_hypothesis


def test_propose_emits_hypothesis_created() -> None:
    hypothesis = make_hypothesis()
    events = hypothesis.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, HypothesisCreated)
    assert event.hypothesis_id == hypothesis.hypothesis_id
    assert event.hypothesis_kind is hypothesis.hypothesis_kind
    assert event.diagnosis_count == 1
    assert event.reason_count == 1


def test_revise_emits_hypothesis_revised() -> None:
    hypothesis = make_hypothesis()
    hypothesis.pull_events()
    hypothesis.revise(revision_form=RevisionForm.NARROWING)
    events = hypothesis.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], HypothesisRevised)
    assert events[0].revision_form is RevisionForm.NARROWING


def test_strengthen_and_weaken_emit_revised() -> None:
    hypothesis = make_hypothesis()
    hypothesis.pull_events()
    hypothesis.strengthen()
    events = hypothesis.pull_events()
    assert isinstance(events[0], HypothesisRevised)
    hypothesis.weaken()
    events = hypothesis.pull_events()
    assert isinstance(events[0], HypothesisRevised)


def test_discard_emits_hypothesis_discarded() -> None:
    hypothesis = make_hypothesis()
    hypothesis.pull_events()
    hypothesis.discard("contradicted by successful prerequisite probe")
    events = hypothesis.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], HypothesisDiscarded)
    assert "prerequisite" in events[0].reason


def test_pull_events_clears_pending() -> None:
    hypothesis = make_hypothesis()
    assert hypothesis.pull_events()
    assert hypothesis.pull_events() == []


def test_hypothesis_created_validation() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisCreated(
            hypothesis_id=HypothesisId("h1"),
            student_id="student-ada",
            hypothesis_kind=HypothesisKind.PREREQUISITE_DEFICIENCY,
            plausibility_level=PlausibilityLevel.WORKING,
            explanatory_strength_level=ExplanatoryStrengthLevel.MODERATE,
            diagnosis_count=0,
            reason_count=1,
        )


def test_hypothesis_revised_immutable() -> None:
    event = HypothesisRevised(
        hypothesis_id=HypothesisId("h1"),
        student_id="student-ada",
        hypothesis_kind=HypothesisKind.TRANSFER_LIMITATION,
        plausibility_level=PlausibilityLevel.TENTATIVE,
        explanatory_strength_level=ExplanatoryStrengthLevel.WEAK,
        revision_form=RevisionForm.SHIFT,
    )
    with pytest.raises(AttributeError):
        event.student_id = "other"  # type: ignore[misc]


def test_hypothesis_discarded_requires_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        HypothesisDiscarded(
            hypothesis_id=HypothesisId("h1"),
            student_id="student-ada",
            hypothesis_kind=HypothesisKind.WEAK_ABSTRACTION,
            reason="  ",
        )


@pytest.mark.parametrize("kind", list(HypothesisKind))
def test_created_event_per_kind(kind: HypothesisKind) -> None:
    hypothesis = make_hypothesis(
        hypothesis_id=f"hyp-evt-{kind.value}",
        hypothesis_kind=kind,
    )
    event = hypothesis.pull_events()[0]
    assert isinstance(event, HypothesisCreated)
    assert event.hypothesis_kind is kind

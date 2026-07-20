"""Sequencing enforcement tests for Learning Episode steps."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId
from domain.education.learning_episode import EpisodeStepKind, SequencingPolicy
from tests.domain.education.learning_episode.conftest import (
    make_episode,
    make_outcome,
    make_reflection,
    make_step,
)


def classic_fade_steps():
    return [
        make_step(
            step_id="intro",
            kind=EpisodeStepKind.explanation(),
            index=0,
            label="Explanation",
        ),
        make_step(
            step_id="example",
            kind=EpisodeStepKind.worked_example(),
            index=1,
            label="Worked Example",
        ),
        make_step(
            step_id="guided",
            kind=EpisodeStepKind.guided_practice(),
            index=2,
            label="Guided Practice",
        ),
        make_step(
            step_id="independent",
            kind=EpisodeStepKind.independent_practice(),
            index=3,
            label="Independent Practice",
        ),
        make_step(
            step_id="reflect",
            kind=EpisodeStepKind.reflection(),
            index=4,
            label="Reflection Stage",
            required=False,
        ),
    ]


class TestClassicSequence:
    def test_order_of_advancement(self) -> None:
        episode = make_episode(steps=classic_fade_steps())
        episode.start()
        assert episode.steps[0].kind == EpisodeStepKind.explanation()
        completed = []
        for _ in range(4):
            completed.append(episode.advance_step().step_id.value)
        assert completed == ["intro", "example", "guided", "independent"]
        assert episode.progress.required_sequence_complete

    def test_can_complete_after_required_even_if_optional_pending(self) -> None:
        episode = make_episode(steps=classic_fade_steps())
        episode.start()
        for _ in range(4):
            episode.advance_step()
        assert episode.progress.required_sequence_complete
        assert not episode.progress.all_steps_complete
        episode.attach_evidence(EvidenceId("ev"))
        episode.record_reflection(make_reflection())
        episode.complete(make_outcome())
        assert episode.is_completed()

    def test_optional_can_still_be_advanced(self) -> None:
        episode = make_episode(steps=classic_fade_steps())
        episode.start()
        for _ in range(4):
            episode.advance_step()
        episode.advance_step()
        assert episode.progress.all_steps_complete


class TestNoSkip:
    def test_single_active_enforced_via_advance(self) -> None:
        episode = make_episode(steps=classic_fade_steps())
        episode.start()
        active = [s for s in episode.steps if s.is_active()]
        assert len(active) == 1

    def test_progress_tracks_index(self) -> None:
        episode = make_episode(steps=classic_fade_steps())
        episode.start()
        assert episode.progress.current_index == 0
        episode.advance_step()
        assert episode.progress.current_index == 1


class TestSequencingPolicyDirect:
    def test_required_steps_complete_false_initially(self) -> None:
        steps = classic_fade_steps()
        assert not SequencingPolicy.required_steps_complete(steps)

    def test_build_sequence_required_excludes_optional(self) -> None:
        seq = SequencingPolicy.build_sequence(classic_fade_steps())
        assert seq.length == 5
        assert len(seq.required_step_ids) == 4
        assert not seq.is_required(
            next(s.step_id for s in classic_fade_steps() if not s.required)
        )


class TestIllegalTransitions:
    @pytest.mark.parametrize(
        "action",
        ["advance", "evidence", "reflect", "complete"],
    )
    def test_actions_illegal_when_planned(self, action: str) -> None:
        episode = make_episode()
        if action == "advance":
            with pytest.raises(EducationalInvariantViolation):
                episode.advance_step()
        elif action == "evidence":
            with pytest.raises(EducationalInvariantViolation):
                episode.attach_evidence(EvidenceId("ev"))
        elif action == "reflect":
            with pytest.raises(EducationalInvariantViolation):
                episode.record_reflection(make_reflection())
        else:
            with pytest.raises(EducationalInvariantViolation):
                episode.complete(make_outcome())

    def test_actions_illegal_when_interrupted(self) -> None:
        episode = make_episode()
        episode.interrupt(
            make_outcome(
                kind=__import__(
                    "domain.education.learning_episode",
                    fromlist=["EpisodeOutcomeKind"],
                ).EpisodeOutcomeKind.INTERRUPTED,
                summary="aborted",
            )
        )
        with pytest.raises(EducationalInvariantViolation):
            episode.start()
        with pytest.raises(EducationalInvariantViolation):
            episode.advance_step()
        with pytest.raises(EducationalInvariantViolation):
            episode.attach_evidence(EvidenceId("ev"))

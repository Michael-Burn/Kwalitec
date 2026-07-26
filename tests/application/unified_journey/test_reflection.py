"""Unit tests — ReflectionPrompt / ReflectionAssembler (P2-MS005)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.application.unified_journey import (
    ReflectionAssembler,
    ReflectionExperience,
    ReflectionPrompt,
    ReflectionState,
    SessionOutcome,
    default_reflection_prompts,
    empty_reflection_experience,
)


@pytest.fixture
def assembler() -> ReflectionAssembler:
    return ReflectionAssembler()


def _outcome(**overrides) -> SessionOutcome:
    base = dict(
        mission_title="Revise equity",
        completion_status="complete",
        reflection_available=True,
        summary_message="You finished Revise equity",
        next_transition="Take a brief moment to reflect",
        upcoming_action="Reflect briefly",
    )
    base.update(overrides)
    return SessionOutcome(**base)


def test_default_prompts_are_presentation_only():
    prompts = default_reflection_prompts()
    assert len(prompts) == 3
    texts = [p.prompt.casefold() for p in prompts]
    assert any("feel" in text for text in texts)
    assert any("manageable" in text for text in texts)
    assert any("note" in text for text in texts)
    note = next(p for p in prompts if p.response_type == "note")
    assert note.optional_note_placeholder
    with pytest.raises(FrozenInstanceError):
        prompts[0].prompt = "changed"  # type: ignore[misc]


def test_reflection_prompt_rejects_unknown_response_type():
    with pytest.raises(ValueError):
        ReflectionPrompt(prompt="x", response_type="diagnostic")


def test_assemble_reflection_experience(assembler: ReflectionAssembler):
    experience = assembler.assemble(_outcome())
    assert isinstance(experience, ReflectionExperience)
    assert experience.is_available
    assert experience.is_active
    assert experience.skip_available is True
    assert len(experience.prompts) == 3
    assert "reflect" in experience.next_transition.casefold()
    assert experience.session_outcome.mission_title == "Revise equity"


def test_assemble_respects_state(assembler: ReflectionAssembler):
    done = assembler.assemble(
        _outcome(),
        state=ReflectionState.COMPLETED,
    )
    assert done.is_completed
    assert done.is_active is False
    assert "complete" in done.next_transition.casefold()

    skipped = assembler.assemble(_outcome(), state=ReflectionState.SKIPPED)
    assert skipped.is_skipped


def test_unavailable_outcome_yields_placeholder(assembler: ReflectionAssembler):
    experience = assembler.assemble(
        _outcome(reflection_available=False)
    )
    assert experience.prompts == ()
    assert experience.metadata


def test_empty_reflection_experience():
    empty = empty_reflection_experience()
    assert empty.prompts == ()

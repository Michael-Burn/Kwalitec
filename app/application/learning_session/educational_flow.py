"""Educational Session Substance flow (LXP-004A / SR-001A P3 foundation).

Defines the continuous in-session educational sequence:

    Learning Objectives → Read → Worked Examples → Practice → Reflect → Ready to Finish

Structural sequencing only. Never invents mastery, evidence, or Twin updates.
LearningSessionRuntime remains the sole session AUTHORITY; this module
describes educational substance stages inside an ACTIVE session.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.application.learning_session.scoreable_practice import ScoreablePracticeItem


class EducationalStage(StrEnum):
    """Student-visible educational stages inside one Study Session."""

    LEARNING_OBJECTIVES = "learning_objectives"
    READ = "read"
    WORKED_EXAMPLE = "worked_example"
    PRACTICE = "practice"
    REFLECTION = "reflection"
    READY_TO_FINISH = "ready_to_finish"


# Continuous educational arc inside the Activity surface (before Reflection).
ACTIVITY_STAGES: tuple[EducationalStage, ...] = (
    EducationalStage.READ,
    EducationalStage.WORKED_EXAMPLE,
    EducationalStage.PRACTICE,
)

# Full session educational sequence including overview / reflection / finish.
SESSION_EDUCATIONAL_FLOW: tuple[EducationalStage, ...] = (
    EducationalStage.LEARNING_OBJECTIVES,
    EducationalStage.READ,
    EducationalStage.WORKED_EXAMPLE,
    EducationalStage.PRACTICE,
    EducationalStage.REFLECTION,
    EducationalStage.READY_TO_FINISH,
)

_STAGE_LABELS: dict[EducationalStage, str] = {
    EducationalStage.LEARNING_OBJECTIVES: "Learning objectives",
    EducationalStage.READ: "Reading",
    EducationalStage.WORKED_EXAMPLE: "Worked example",
    EducationalStage.PRACTICE: "Practice",
    EducationalStage.REFLECTION: "Reflection",
    EducationalStage.READY_TO_FINISH: "Ready to finish",
}

_NEXT_TRANSITION: dict[EducationalStage, str] = {
    EducationalStage.LEARNING_OBJECTIVES: "Continue to Reading",
    EducationalStage.READ: "Continue to Worked Example",
    EducationalStage.WORKED_EXAMPLE: "Continue to Practice",
    EducationalStage.PRACTICE: "Continue to Reflection",
    EducationalStage.REFLECTION: "Ready to Finish",
    EducationalStage.READY_TO_FINISH: "Finish Session",
}


@dataclass(frozen=True)
class LearningObjectiveRef:
    """Syllabus-bound learning objective reference for session presentation."""

    objective_id: str
    code: str
    text: str
    topic_id: str = ""


@dataclass(frozen=True)
class EducationalActivitySpec:
    """One package-derived activity step in the continuous educational sequence."""

    activity_id: str
    stage: EducationalStage
    title: str
    prompt: str
    body: str
    supporting_material: str = ""
    hints: tuple[str, ...] = ()
    answer_prompt: str = "Your notes"
    requires_response: bool = True
    objective_ids: tuple[str, ...] = ()
    syllabus_refs: tuple[str, ...] = ()
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    scoreable: ScoreablePracticeItem | None = None

    @property
    def stage_label(self) -> str:
        return stage_label(self.stage)

    @property
    def next_action_label(self) -> str:
        return next_transition_label(self.stage)

    @property
    def is_scoreable(self) -> bool:
        return self.scoreable is not None


@dataclass(frozen=True)
class EducationalSessionSubstance:
    """Package-derived substance for one Study Session topic."""

    topic_id: str
    topic_title: str
    topic_code: str
    curriculum_identity: str
    learning_objectives: tuple[LearningObjectiveRef, ...]
    activities: tuple[EducationalActivitySpec, ...]
    educational_rationale: str = ""
    task_descriptions: tuple[str, ...] = ()
    source: str = "package"

    @property
    def activity_count(self) -> int:
        return len(self.activities)

    @property
    def objective_texts(self) -> tuple[str, ...]:
        return tuple(obj.text for obj in self.learning_objectives if obj.text)

    @property
    def has_worked_example(self) -> bool:
        return any(
            act.stage is EducationalStage.WORKED_EXAMPLE for act in self.activities
        )


def stage_label(stage: EducationalStage | str) -> str:
    """Human label for an educational stage."""
    resolved = EducationalStage(str(stage))
    return _STAGE_LABELS.get(resolved, resolved.value.replace("_", " ").title())


def next_transition_label(stage: EducationalStage | str) -> str:
    """CTA copy for advancing from ``stage`` in the continuous flow."""
    resolved = EducationalStage(str(stage))
    return _NEXT_TRANSITION.get(resolved, "Continue")


def is_activity_stage(stage: EducationalStage | str) -> bool:
    """True when the stage belongs inside the Activity surface sequence."""
    return EducationalStage(str(stage)) in ACTIVITY_STAGES

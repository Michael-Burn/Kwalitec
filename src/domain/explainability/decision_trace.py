"""DecisionTrace — ordered educational decision chain for explainability.

Architecture Source
    EDU-005 Educational Explainability Engine
    EDUCATIONAL_EXPLAINABILITY_STANDARD.md (EIP-003)
Concept
    Decision Trace
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.explainability.enums import DecisionStage
from domain.explainability.ids import DecisionTraceId


@dataclass(frozen=True, slots=True)
class TraceStep(EducationalValueObject):
    """One stage in the educational decision chain.

    Records which Educational OS projection contributed, in what order, and
    which reason codes support that contribution.
    """

    stage: DecisionStage
    source_id: str
    summary: str
    sequence: int
    reason_codes: tuple[str, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.stage, DecisionStage):
            raise EducationalInvariantViolation(
                "stage must be a DecisionStage",
                invariant="TraceStep.stage.type",
            )
        object.__setattr__(
            self,
            "source_id",
            require_non_empty_text(self.source_id, "source_id"),
        )
        object.__setattr__(
            self,
            "summary",
            require_non_empty_text(self.summary, "summary"),
        )
        if len(self.summary) < 12:
            raise EducationalInvariantViolation(
                "trace step summary must be educationally substantive",
                invariant="TraceStep.summary.substantive",
            )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="TraceStep.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="TraceStep.sequence.positive",
            )
        if not isinstance(self.reason_codes, tuple):
            raise EducationalInvariantViolation(
                "reason_codes must be a tuple",
                invariant="TraceStep.reason_codes.type",
            )
        cleaned: list[str] = []
        for code in self.reason_codes:
            cleaned.append(require_non_empty_text(code, "reason_code"))
        object.__setattr__(self, "reason_codes", tuple(cleaned))


@dataclass(frozen=True, slots=True)
class DecisionTrace(EducationalValueObject):
    """Ordered chain from mission through recommendation for one explanation.

    A DecisionTrace makes educational decisions reconstructible: mission →
    study plan → progress → recommendation. It does not invent decisions or
    alter Educational OS outputs.
    """

    trace_id: DecisionTraceId
    steps: tuple[TraceStep, ...]
    primary_decision: str
    chain_summary: str

    def _validate(self) -> None:
        if not isinstance(self.trace_id, DecisionTraceId):
            raise EducationalInvariantViolation(
                "trace_id must be a DecisionTraceId",
                invariant="DecisionTrace.trace_id.type",
            )
        if not isinstance(self.steps, tuple) or not self.steps:
            raise EducationalInvariantViolation(
                "steps must be a non-empty tuple",
                invariant="DecisionTrace.steps.min_one",
            )
        seen_sequences: set[int] = set()
        seen_stages: set[DecisionStage] = set()
        expected = 1
        for step in self.steps:
            if not isinstance(step, TraceStep):
                raise EducationalInvariantViolation(
                    "steps must contain TraceStep values",
                    invariant="DecisionTrace.steps.item_type",
                )
            if step.sequence in seen_sequences:
                raise EducationalInvariantViolation(
                    "trace step sequences must be unique",
                    invariant="DecisionTrace.steps.unique_sequence",
                )
            seen_sequences.add(step.sequence)
            if step.sequence != expected:
                raise EducationalInvariantViolation(
                    "trace step sequences must be contiguous from 1",
                    invariant="DecisionTrace.steps.contiguous",
                )
            expected += 1
            if step.stage in seen_stages:
                raise EducationalInvariantViolation(
                    "each DecisionStage may appear at most once in a trace",
                    invariant="DecisionTrace.steps.unique_stage",
                )
            seen_stages.add(step.stage)
        object.__setattr__(
            self,
            "primary_decision",
            require_non_empty_text(self.primary_decision, "primary_decision"),
        )
        object.__setattr__(
            self,
            "chain_summary",
            require_non_empty_text(self.chain_summary, "chain_summary"),
        )
        if len(self.chain_summary) < 24:
            raise EducationalInvariantViolation(
                "chain summary must be educationally substantive",
                invariant="DecisionTrace.chain_summary.substantive",
            )

    def stage_count(self) -> int:
        return len(self.steps)

    def has_stage(self, stage: DecisionStage) -> bool:
        return any(step.stage is stage for step in self.steps)

    def step_for(self, stage: DecisionStage) -> TraceStep | None:
        for step in self.steps:
            if step.stage is stage:
                return step
        return None

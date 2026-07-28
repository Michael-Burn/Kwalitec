"""Canonical Experience Model (EX-001).

UI-agnostic presentation of one Educational Decision. Experience models
communicate decisions; they never create or modify them.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.domain.educational_experience_engine.urgency import UrgencyLevel
from app.domain.educational_experience_engine.version import EXPERIENCE_VERSION


@dataclass(frozen=True)
class EffortPresentation:
    """Estimated effort for student-facing surfaces."""

    minutes: int
    label: str

    def __post_init__(self) -> None:
        if self.minutes < 0:
            raise ValueError("effort minutes must be >= 0")
        if not (self.label or "").strip():
            raise ValueError("effort label is required")

    def to_dict(self) -> dict[str, Any]:
        return {"minutes": self.minutes, "label": self.label}


@dataclass(frozen=True)
class ExperienceTrace:
    """Explainability references preserved from the Educational Decision."""

    decision_id: str
    decision_type: str
    curriculum_target: str
    supporting_belief_ids: tuple[str, ...]
    supporting_curriculum_refs: tuple[str, ...]
    supporting_evidence_ids: tuple[str, ...]
    applied_rule_ids: tuple[str, ...]
    reasoning_version: str
    priority: float
    rank_position: int

    def __post_init__(self) -> None:
        if not (self.decision_id or "").strip():
            raise ValueError("decision_id is required for traceability")
        if not (self.curriculum_target or "").strip():
            raise ValueError("curriculum_target is required for traceability")
        if not (self.reasoning_version or "").strip():
            raise ValueError("reasoning_version is required for traceability")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type,
            "curriculum_target": self.curriculum_target,
            "supporting_belief_ids": list(self.supporting_belief_ids),
            "supporting_curriculum_refs": list(self.supporting_curriculum_refs),
            "supporting_evidence_ids": list(self.supporting_evidence_ids),
            "applied_rule_ids": list(self.applied_rule_ids),
            "reasoning_version": self.reasoning_version,
            "priority": self.priority,
            "rank_position": self.rank_position,
        }


@dataclass(frozen=True)
class ExperienceModel:
    """Reusable, UI-agnostic student experience for one educational decision.

    Required presentation fields:
    title, summary, educational rationale, estimated effort, expected outcome,
    urgency, prerequisite explanation, motivational framing, next steps.
    """

    experience_id: str
    instance_id: str
    title: str
    summary: str
    educational_rationale: str
    estimated_effort: EffortPresentation
    expected_outcome: str
    urgency: str
    prerequisite_explanation: str
    motivational_framing: str
    next_steps: tuple[str, ...]
    curriculum_area: str
    trace: ExperienceTrace
    presented_at: datetime
    experience_version: str = EXPERIENCE_VERSION

    def __post_init__(self) -> None:
        for field_name in (
            "experience_id",
            "instance_id",
            "title",
            "summary",
            "educational_rationale",
            "expected_outcome",
            "prerequisite_explanation",
            "motivational_framing",
            "curriculum_area",
            "experience_version",
        ):
            value = getattr(self, field_name)
            if not (value or "").strip():
                raise ValueError(f"{field_name} is required")

        urgency = (self.urgency or "").strip().lower()
        if urgency not in {m.value for m in UrgencyLevel}:
            raise ValueError(f"Invalid urgency: {self.urgency!r}")
        object.__setattr__(self, "urgency", urgency)

        steps = tuple(
            s.strip() for s in self.next_steps if isinstance(s, str) and s.strip()
        )
        if not steps:
            raise ValueError("next_steps must be non-empty")
        object.__setattr__(self, "next_steps", steps)

    def to_dict(self) -> dict[str, Any]:
        return {
            "experience_id": self.experience_id,
            "instance_id": self.instance_id,
            "title": self.title,
            "summary": self.summary,
            "educational_rationale": self.educational_rationale,
            "estimated_effort": self.estimated_effort.to_dict(),
            "expected_outcome": self.expected_outcome,
            "urgency": self.urgency,
            "prerequisite_explanation": self.prerequisite_explanation,
            "motivational_framing": self.motivational_framing,
            "next_steps": list(self.next_steps),
            "curriculum_area": self.curriculum_area,
            "trace": self.trace.to_dict(),
            "presented_at": self.presented_at.isoformat(),
            "experience_version": self.experience_version,
        }

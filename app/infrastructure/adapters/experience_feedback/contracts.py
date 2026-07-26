"""Immutable Experience Feedback contracts (P2-MS008).

Factual Evidence → Experience display DTOs only. No educational
interpretation, scoring, recommendations, or behavioural adaptation.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

CONTRACT_VERSION = "p2.ms008.1"
AUTHORITY_EXPERIENCE_FEEDBACK = "experience_feedback"

DEFAULT_SOURCE_DESCRIPTION = "Based on your recorded study activity."

REPORTING_PERIOD_THIS_WEEK = "this_week"
REPORTING_PERIOD_LABELS = MappingProxyType(
    {
        REPORTING_PERIOD_THIS_WEEK: "This week",
        "all": "All recorded activity",
    }
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    raw = dict(value or {})
    frozen: dict[str, Any] = {}
    for key, item in raw.items():
        if isinstance(item, Mapping):
            frozen[str(key)] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[str(key)] = list(item)
        else:
            frozen[str(key)] = item
    return MappingProxyType(frozen)


def serialize_canonical(value: Any) -> str:
    """Deterministic JSON serialization (sorted keys, compact separators)."""
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        items = sorted(value.items(), key=lambda i: str(i[0]))
        return {str(k): _canonical(v) for k, v in items}
    if isinstance(value, list | tuple):
        return [_canonical(v) for v in value]
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int | float):
        return value
    return str(value)


def deterministic_feedback_id(
    *,
    student_id: str,
    reporting_period: str,
    completed_missions: int,
    completed_reflections: int,
    study_sessions: int,
    active_streak: int,
    generated_at: str,
    evidence_summary_id: str,
    contract_version: str = CONTRACT_VERSION,
) -> str:
    """Derive feedback_id from factual material fields (no wall-clock)."""
    material = {
        "active_streak": active_streak,
        "completed_missions": completed_missions,
        "completed_reflections": completed_reflections,
        "contract_version": contract_version,
        "evidence_summary_id": evidence_summary_id,
        "generated_at": generated_at,
        "reporting_period": reporting_period,
        "student_id": student_id,
        "study_sessions": study_sessions,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"expfb-{digest[:32]}"


@dataclass(frozen=True)
class ExperienceFeedbackFact:
    """One presentation-ready factual line with explainability."""

    key: str
    label: str
    value: int
    value_label: str
    source_description: str = DEFAULT_SOURCE_DESCRIPTION

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", (self.key or "").strip())
        object.__setattr__(self, "label", (self.label or "").strip())
        if not isinstance(self.value, int):
            raise TypeError("value must be an int")
        object.__setattr__(self, "value_label", (self.value_label or "").strip())
        object.__setattr__(
            self,
            "source_description",
            (self.source_description or "").strip() or DEFAULT_SOURCE_DESCRIPTION,
        )
        if not self.key:
            raise ValueError("key is required")
        if not self.label:
            raise ValueError("label is required")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "source_description": self.source_description,
            "value": self.value,
            "value_label": self.value_label,
        }


@dataclass(frozen=True)
class ExperienceFeedback:
    """Immutable factual feedback from Evidence for Experience display.

    Every field represents a factual observation returned by the Evidence
    Platform public read interface. No scores, predictions, or educational
    interpretation.
    """

    feedback_id: str
    reporting_period: str
    completed_missions: int
    completed_reflections: int
    study_sessions: int
    active_streak: int
    generated_at: str
    facts: tuple[ExperienceFeedbackFact, ...] = ()
    student_id: str = ""
    evidence_summary_id: str = ""
    evidence_refs: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(default_factory=dict)
    source_description: str = DEFAULT_SOURCE_DESCRIPTION
    reporting_period_label: str = ""
    contract_version: str = CONTRACT_VERSION
    authority: str = AUTHORITY_EXPERIENCE_FEEDBACK

    def __post_init__(self) -> None:
        object.__setattr__(self, "feedback_id", (self.feedback_id or "").strip())
        object.__setattr__(
            self,
            "reporting_period",
            (self.reporting_period or REPORTING_PERIOD_THIS_WEEK).strip().lower()
            or REPORTING_PERIOD_THIS_WEEK,
        )
        for label, value in (
            ("completed_missions", self.completed_missions),
            ("completed_reflections", self.completed_reflections),
            ("study_sessions", self.study_sessions),
            ("active_streak", self.active_streak),
        ):
            if not isinstance(value, int):
                raise TypeError(f"{label} must be an int")
            if value < 0:
                raise ValueError(f"{label} must be >= 0")
        object.__setattr__(self, "generated_at", (self.generated_at or "").strip())
        object.__setattr__(self, "facts", tuple(self.facts or ()))
        for fact in self.facts:
            if not isinstance(fact, ExperienceFeedbackFact):
                raise TypeError("facts must contain ExperienceFeedbackFact values")
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self, "evidence_summary_id", (self.evidence_summary_id or "").strip()
        )
        object.__setattr__(
            self, "evidence_refs", tuple(str(r) for r in (self.evidence_refs or ()))
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(
            self,
            "source_description",
            (self.source_description or "").strip() or DEFAULT_SOURCE_DESCRIPTION,
        )
        period_label = (self.reporting_period_label or "").strip()
        if not period_label:
            period_label = REPORTING_PERIOD_LABELS.get(
                self.reporting_period, self.reporting_period.replace("_", " ").title()
            )
        object.__setattr__(self, "reporting_period_label", period_label)
        object.__setattr__(
            self,
            "contract_version",
            (self.contract_version or CONTRACT_VERSION).strip(),
        )
        object.__setattr__(
            self,
            "authority",
            (self.authority or AUTHORITY_EXPERIENCE_FEEDBACK).strip(),
        )
        if not self.feedback_id:
            raise ValueError("feedback_id is required")
        if not self.generated_at:
            raise ValueError("generated_at is required")

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "active_streak": self.active_streak,
            "authority": self.authority,
            "completed_missions": self.completed_missions,
            "completed_reflections": self.completed_reflections,
            "contract_version": self.contract_version,
            "evidence_refs": list(self.evidence_refs),
            "evidence_summary_id": self.evidence_summary_id,
            "facts": [fact.to_canonical_dict() for fact in self.facts],
            "feedback_id": self.feedback_id,
            "generated_at": self.generated_at,
            "provenance": dict(self.provenance),
            "reporting_period": self.reporting_period,
            "reporting_period_label": self.reporting_period_label,
            "source_description": self.source_description,
            "student_id": self.student_id,
            "study_sessions": self.study_sessions,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


@runtime_checkable
class EvidenceFeedbackReadPort(Protocol):
    """Evidence public read surface used by Experience Feedback.

    Callers must use this contract only — no repository / collector bypass.
    """

    def query_factual_summary(
        self,
        student_id: str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Any = None,
    ) -> Any:
        """Return an EvidenceResult carrying EvidenceFactualSummary."""

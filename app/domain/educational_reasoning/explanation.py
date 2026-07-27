"""Human-readable explanations for educational decisions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True)
class Explanation:
    """Explainability payload for one educational inference.

    Answers: why it happened, which observations triggered it, which curriculum
    evidence supported it, and which rule generated it.
    """

    summary: str
    rule_code: str
    observation_ids: tuple[str, ...] = ()
    curriculum_evidence_ids: tuple[str, ...] = ()
    detail: str = ""
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.summary or "").strip():
            raise ValueError("explanation summary is required")
        if not (self.rule_code or "").strip():
            raise ValueError("explanation rule_code is required")
        object.__setattr__(self, "observation_ids", tuple(self.observation_ids or ()))
        object.__setattr__(
            self, "curriculum_evidence_ids", tuple(self.curriculum_evidence_ids or ())
        )
        object.__setattr__(
            self, "metadata", MappingProxyType(dict(self.metadata or {}))
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "rule_code": self.rule_code,
            "observation_ids": list(self.observation_ids),
            "curriculum_evidence_ids": list(self.curriculum_evidence_ids),
            "detail": self.detail,
            "metadata": dict(self.metadata),
        }

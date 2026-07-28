"""DecisionReason — explainable justification for one educational decision."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DecisionReason:
    """Immutable reason linking a decision to approved rule semantics."""

    code: str
    summary: str
    detail: str = ""
    observation_ids: tuple[str, ...] = ()
    rule_code: str = ""

    def __post_init__(self) -> None:
        if not (self.code or "").strip():
            raise ValueError("reason code is required")
        if not (self.summary or "").strip():
            raise ValueError("reason summary is required")
        object.__setattr__(self, "observation_ids", tuple(self.observation_ids or ()))

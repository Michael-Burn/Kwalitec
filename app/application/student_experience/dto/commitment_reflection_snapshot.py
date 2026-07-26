"""Immutable completion-reflection DTO (EP-008.3)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommitmentReflectionSnapshot:
    """Brief post-completion reflection — authored + humble frames only."""

    what_you_did: str = ""
    what_changed: str = ""
    why_it_mattered: str = ""
    what_was_learned: str = ""
    what_happens_next: str = ""

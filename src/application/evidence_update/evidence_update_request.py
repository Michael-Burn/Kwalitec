"""EvidenceUpdateRequest — application input for educational evidence update.

Carries captured session evidence plus optional educational anchors. Does not
diagnose, recommend, or plan study.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.evidence_capture.captured_evidence import CapturedEvidence


@dataclass(frozen=True, slots=True)
class EvidenceUpdateRequest:
    """Request to transform and store captured session evidence.

    Attributes:
        captured: Immutable session evidence from Learning Evidence Capture.
        twin_id: Optional Twin identity for educational-state memory update.
        concept_ids: Optional known concept identities to attach (never invented).
        learning_episode_ids: Optional known episode identities to attach.
        update_twin: When True, append Twin evidence history when a Twin exists.
    """

    captured: CapturedEvidence
    twin_id: str | None = None
    concept_ids: tuple[str, ...] = ()
    learning_episode_ids: tuple[str, ...] = ()
    update_twin: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.captured, CapturedEvidence):
            raise ValueError("captured must be a CapturedEvidence")

        twin_id = (self.twin_id or "").strip() or None
        object.__setattr__(self, "twin_id", twin_id)

        concepts = tuple(
            cleaned
            for raw in self.concept_ids
            if (cleaned := (raw or "").strip())
        )
        object.__setattr__(self, "concept_ids", concepts)

        episodes = tuple(
            cleaned
            for raw in self.learning_episode_ids
            if (cleaned := (raw or "").strip())
        )
        object.__setattr__(self, "learning_episode_ids", episodes)

        if not isinstance(self.update_twin, bool):
            raise ValueError("update_twin must be a bool")

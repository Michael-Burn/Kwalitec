"""Finish Review DTO — explicit Yes / Partially / No before session close.

LXP-003 / SR-001A P2. Records whether planned study for this sitting occurred.
Does not claim mastery, Twin updates, or mission/topic completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class FinishReviewVerdict(StrEnum):
    """Student answer to: did you complete today's planned study?"""

    YES = "yes"
    PARTIALLY = "partially"
    NO = "no"


FINISH_REVIEW_LABELS: dict[FinishReviewVerdict, str] = {
    FinishReviewVerdict.YES: "Yes",
    FinishReviewVerdict.PARTIALLY: "Partially",
    FinishReviewVerdict.NO: "No",
}


@dataclass(frozen=True)
class FinishReview:
    """Immutable record of an explicit finish review.

    Attributes:
        verdict: Yes / Partially / No.
        notes: Optional free-text note (presentation only).
        recorded_at: UTC timestamp when the review was accepted.
    """

    verdict: FinishReviewVerdict
    notes: str = ""
    recorded_at: datetime | None = None

    @classmethod
    def create(
        cls,
        verdict: FinishReviewVerdict | str,
        *,
        notes: str | None = None,
        recorded_at: datetime | None = None,
    ) -> FinishReview:
        resolved = (
            verdict
            if isinstance(verdict, FinishReviewVerdict)
            else FinishReviewVerdict(str(verdict).strip().lower())
        )
        return cls(
            verdict=resolved,
            notes=(notes or "").strip(),
            recorded_at=recorded_at,
        )

    @property
    def label(self) -> str:
        return FINISH_REVIEW_LABELS[self.verdict]

    def to_opaque(self) -> dict[str, str | None]:
        return {
            "verdict": self.verdict.value,
            "label": self.label,
            "notes": self.notes,
            "recorded_at": (
                self.recorded_at.isoformat() if self.recorded_at is not None else None
            ),
        }

    @classmethod
    def from_opaque(cls, raw: dict | None) -> FinishReview | None:
        if not isinstance(raw, dict) or not raw.get("verdict"):
            return None
        recorded = raw.get("recorded_at")
        recorded_at = None
        if isinstance(recorded, str) and recorded.strip():
            recorded_at = datetime.fromisoformat(recorded)
        return cls.create(
            str(raw["verdict"]),
            notes=str(raw.get("notes") or ""),
            recorded_at=recorded_at,
        )

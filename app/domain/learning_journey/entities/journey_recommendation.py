"""Explainable next-step advice for a Learning Journey.

Recommendations continue, adjust, or prepare journey work. They never claim
certainty, never complete topics, and are not Educational Evidence of
understanding.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class RecommendationKind(StrEnum):
    """What the recommendation proposes next.

    Vocabulary is advisory — never a completion authority.
    """

    CONTINUE_CURRENT_SESSION = "continue_current_session"
    BEGIN_NEXT_OBJECTIVE = "begin_next_objective"
    REVIEW_PREVIOUS_CONCEPT = "review_previous_concept"
    REVISE_EARLIER_EVIDENCE = "revise_earlier_evidence"
    ATTEMPT_PRACTICE = "attempt_practice"
    CAPTURE_REFLECTION = "capture_reflection"
    PAUSE_JOURNEY = "pause_journey"
    CONFIRM_TOPIC_COMPLETE = "confirm_topic_complete"


class RecommendationLifecycle(StrEnum):
    """Advisory artefact lifecycle — not journey completion state."""

    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REALISED = "realised"
    DISMISSED = "dismissed"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"


class RecommendationCertainty(StrEnum):
    """Honesty about how provisional the advice is.

    Recommendations must never claim certainty.
    """

    SUGGESTED = "suggested"
    PROVISIONAL = "provisional"
    CONDITIONAL = "conditional"


@dataclass(frozen=True)
class JourneyRecommendation:
    """Journey-scoped educational recommendation.

    Attributes:
        recommendation_id: Stable identity.
        journey_id: Parent journey.
        kind: Proposed next educational move.
        lifecycle: Advisory artefact lifecycle.
        certainty: Explicit non-certainty posture.
        rationale_tags: Short structural explainability tags (not marketing).
        session_id: Optional session this advice targets or realised.
        objective_id: Optional objective focus.
        created_at: When proposed.
    """

    recommendation_id: str
    journey_id: str
    kind: RecommendationKind
    lifecycle: RecommendationLifecycle
    certainty: RecommendationCertainty
    rationale_tags: tuple[str, ...] = ()
    session_id: str | None = None
    objective_id: str | None = None
    created_at: datetime | None = None

    @classmethod
    def create(
        cls,
        recommendation_id: str,
        journey_id: str,
        kind: RecommendationKind | str,
        *,
        lifecycle: RecommendationLifecycle
        | str = RecommendationLifecycle.PROPOSED,
        certainty: RecommendationCertainty
        | str = RecommendationCertainty.PROVISIONAL,
        rationale_tags: list[str] | tuple[str, ...] | None = None,
        session_id: str | None = None,
        objective_id: str | None = None,
        created_at: datetime | None = None,
    ) -> JourneyRecommendation:
        """Construct a JourneyRecommendation.

        Raises:
            ValueError: When required identities are empty, or certainty
                attempts to express absolute confidence.
        """
        kind_value = (
            kind if isinstance(kind, RecommendationKind) else RecommendationKind(kind)
        )
        life = (
            lifecycle
            if isinstance(lifecycle, RecommendationLifecycle)
            else RecommendationLifecycle(lifecycle)
        )
        cert = (
            certainty
            if isinstance(certainty, RecommendationCertainty)
            else RecommendationCertainty(certainty)
        )
        tags = tuple(t.strip() for t in (rationale_tags or ()) if t and t.strip())
        return cls(
            recommendation_id=_require_non_empty(
                recommendation_id, "recommendation_id"
            ),
            journey_id=_require_non_empty(journey_id, "journey_id"),
            kind=kind_value,
            lifecycle=life,
            certainty=cert,
            rationale_tags=tags,
            session_id=_optional_id(session_id),
            objective_id=_optional_id(objective_id),
            created_at=created_at,
        )

    @property
    def claims_certainty(self) -> bool:
        """Recommendations never claim certainty by design."""
        return False


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_id(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None

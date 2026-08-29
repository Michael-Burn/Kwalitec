"""Reflection projection — educational guidance at session checkpoints.

No scoring language. Guidance only. Educational insights arrive from ports.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Scoring / gamification language is forbidden on reflection surfaces.
FORBIDDEN_REFLECTION_TERMS: tuple[str, ...] = (
    "score",
    "points",
    "grade",
    "streak",
    "badge",
    "xp",
    "leaderboard",
    "digital twin",
    "adaptive decision",
    "learning orchestrator",
    "mastery score",
)

# Short tokens that false-positive inside ordinary educational words
# (e.g. "xp" in "exploratory" / "Explain").
_BOUNDARY_FORBIDDEN_TERMS: frozenset[str] = frozenset(
    {"xp", "score", "grade", "points", "badge", "streak"}
)


@dataclass(frozen=True)
class ReflectionProjection:
    """Domain projection for a Learning Session reflection checkpoint.

    Displays key insight, concept confidence, suggested improvement,
    and a reflection prompt — educational guidance only.
    """

    session_id: str
    key_insight: str = ""
    concept_confidence: str = ""
    suggested_improvement: str = ""
    reflection_prompt: str = ""
    confidence_prompt: str = ""
    topic_title: str = ""
    next_action_label: str = "Continue to Summary"
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        session_id: str,
        *,
        key_insight: str = "",
        concept_confidence: str = "",
        suggested_improvement: str = "",
        reflection_prompt: str = "",
        confidence_prompt: str = "",
        topic_title: str = "",
        next_action_label: str = "Continue to Summary",
        metadata: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None = None,
    ) -> ReflectionProjection:
        """Build a reflection projection from opaque port facts."""
        insight = (key_insight or "").strip()
        confidence = (concept_confidence or "").strip()
        improvement = (suggested_improvement or "").strip()
        prompt = (reflection_prompt or "").strip()
        conf_prompt = (confidence_prompt or "").strip()
        for label, text in (
            ("key_insight", insight),
            ("concept_confidence", confidence),
            ("suggested_improvement", improvement),
            ("reflection_prompt", prompt),
            ("confidence_prompt", conf_prompt),
        ):
            if text and not is_reflection_safe(text):
                raise ValueError(f"{label} contains forbidden scoring language")
        return cls(
            session_id=_require_non_empty(session_id, "session_id"),
            key_insight=insight,
            concept_confidence=confidence,
            suggested_improvement=improvement,
            reflection_prompt=prompt
            or "What felt clearest, and what still needs practice?",
            confidence_prompt=conf_prompt,
            topic_title=(topic_title or "").strip(),
            next_action_label=(
                (next_action_label or "Continue to Summary").strip()
                or "Continue to Summary"
            ),
            metadata=tuple(metadata or ()),
        )

    @property
    def has_insight(self) -> bool:
        """True when a key insight is present."""
        return bool(self.key_insight)

    @property
    def is_complete(self) -> bool:
        """True when core reflection guidance fields are populated."""
        return bool(
            self.key_insight and self.concept_confidence and self.reflection_prompt
        )


def is_reflection_safe(text: str) -> bool:
    """True when ``text`` avoids scoring / internal engine language.

    Short gamification tokens are matched on word boundaries so substance-backed
    copy such as \"exploratory data analysis\" or \"Explain the aims…\" is not
    rejected (PB-001 F6 / PB-002).
    """
    lowered = (text or "").lower()
    for term in FORBIDDEN_REFLECTION_TERMS:
        if term in _BOUNDARY_FORBIDDEN_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", lowered):
                return False
        elif term in lowered:
            return False
    return True


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized

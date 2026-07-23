"""Plain-language narration for already-produced reason codes and evidence.

Presentation only. Maps existing Education OS / Application reason codes and
evidence phrases into one-sentence learner copy. Never invents educational
concepts, never scores, never recommends.
"""

from __future__ import annotations

from presentation.provenance.enums import ProvenanceKind

# Existing RecommendationReasonCode values → one-sentence learner narration.
_REASON_CODE_SENTENCES: dict[str, str] = {
    "weak_prerequisite": (
        "A prerequisite topic still needs attention before you move on."
    ),
    "low_mastery_high_confidence": (
        "Mastery is still developing even though confidence feels high."
    ),
    "low_mastery_low_confidence": (
        "Both mastery and confidence are still building on this topic."
    ),
    "stable_high_mastery": (
        "Mastery looks stable, so the plan keeps this knowledge maintained."
    ),
    "contradictory_evidence": (
        "Recent practice signals do not fully agree, so the focus stays careful."
    ),
    "active_mission": "You already have an active mission in progress.",
    "active_checkpoint": (
        "A recent or upcoming checkpoint shapes this focus."
    ),
    "volatile_mastery": (
        "Mastery has been fluctuating, so a steady review helps."
    ),
    "developing_mastery": (
        "Mastery is developing, so continued practice is warranted."
    ),
    "advanced_without_foundation": (
        "Advanced material depends on foundation topics that still need work."
    ),
    "secure_ready_for_checkpoint": (
        "The topic looks secure enough to prepare for a checkpoint."
    ),
    "stable_revision_load": (
        "Revision spacing keeps the current study load steady."
    ),
    "direct_knowledge_gap": (
        "A weak topic was identified in your recent learning evidence."
    ),
    # Adaptive / revision planner codes already emitted as opaque evidence.
    "low_retention": (
        "Recall has softened, so a short review protects what you learned."
    ),
    "declining_confidence": (
        "Confidence has dipped relative to recent performance."
    ),
    "exam_proximity": "This topic is high value with the exam approaching.",
    "prerequisite_gap": (
        "Strengthening this topic unlocks the next steps on your journey."
    ),
    "high_roi": (
        "A short session here offers strong educational return for the time."
    ),
    "overdue_revision": (
        "It has been a while since you last revisited this topic."
    ),
    "mastery_incomplete": (
        "Progress is underway, but the topic is not yet solid for exam conditions."
    ),
    "low_mastery_revision_needed": (
        "Revision is needed because mastery on this topic is still low."
    ),
}

_REASON_CODE_KINDS: dict[str, ProvenanceKind] = {
    "weak_prerequisite": ProvenanceKind.PREREQUISITE_DEPENDENCY,
    "advanced_without_foundation": ProvenanceKind.CURRICULUM_DEPENDENCY,
    "prerequisite_gap": ProvenanceKind.PREREQUISITE_DEPENDENCY,
    "active_checkpoint": ProvenanceKind.RECENT_CHECKPOINT,
    "secure_ready_for_checkpoint": ProvenanceKind.RECENT_CHECKPOINT,
    "volatile_mastery": ProvenanceKind.MASTERY_TREND,
    "developing_mastery": ProvenanceKind.MASTERY_TREND,
    "stable_high_mastery": ProvenanceKind.MASTERY_TREND,
    "low_mastery_high_confidence": ProvenanceKind.MASTERY_TREND,
    "low_mastery_low_confidence": ProvenanceKind.MASTERY_TREND,
    "mastery_incomplete": ProvenanceKind.MASTERY_TREND,
    "direct_knowledge_gap": ProvenanceKind.WEAK_TOPIC,
    "low_retention": ProvenanceKind.WEAK_TOPIC,
    "low_mastery_revision_needed": ProvenanceKind.WEAK_TOPIC,
    "stable_revision_load": ProvenanceKind.REVISION_SPACING,
    "overdue_revision": ProvenanceKind.REVISION_SPACING,
    "exam_proximity": ProvenanceKind.UPCOMING_MILESTONE,
    "contradictory_evidence": ProvenanceKind.EVIDENCE_FRESHNESS,
    "active_mission": ProvenanceKind.MISSION_PURPOSE,
    "declining_confidence": ProvenanceKind.READINESS,
    "high_roi": ProvenanceKind.RECOMMENDATION,
}

_KIND_HINTS: tuple[tuple[tuple[str, ...], ProvenanceKind], ...] = (
    (
        ("prerequisite", "foundation", "depends on", "dependency"),
        ProvenanceKind.PREREQUISITE_DEPENDENCY,
    ),
    (("checkpoint",), ProvenanceKind.RECENT_CHECKPOINT),
    (
        ("mastery", "trend", "improving", "declining", "volatile"),
        ProvenanceKind.MASTERY_TREND,
    ),
    (
        ("weak", "gap", "needs attention", "strengthen"),
        ProvenanceKind.WEAK_TOPIC,
    ),
    (
        ("revision", "spacing", "revisit", "recall"),
        ProvenanceKind.REVISION_SPACING,
    ),
    (
        ("milestone", "exam", "upcoming", "days remaining"),
        ProvenanceKind.UPCOMING_MILESTONE,
    ),
    (
        ("evidence", "fresh", "recent session", "just captured", "reflection"),
        ProvenanceKind.EVIDENCE_FRESHNESS,
    ),
    (
        ("curriculum", "journey", "next topic", "syllabus"),
        ProvenanceKind.CURRICULUM_DEPENDENCY,
    ),
)


def narrate_reason_code(code: str | None) -> str | None:
    """Return a one-sentence narration for a known reason code, else None."""
    key = _normalise_code(code)
    if not key:
        return None
    return _REASON_CODE_SENTENCES.get(key)


def kind_for_reason_code(code: str | None) -> ProvenanceKind:
    """Map a known reason code to a provenance kind."""
    key = _normalise_code(code)
    if not key:
        return ProvenanceKind.RECOMMENDATION
    return _REASON_CODE_KINDS.get(key, ProvenanceKind.RECOMMENDATION)


def kind_for_sentence(
    sentence: str,
    *,
    fallback: ProvenanceKind = ProvenanceKind.RECOMMENDATION,
) -> ProvenanceKind:
    """Best-effort kind from existing display text — never invents meaning."""
    lowered = (sentence or "").strip().lower()
    if not lowered:
        return fallback
    for needles, kind in _KIND_HINTS:
        if any(needle in lowered for needle in needles):
            return kind
    return fallback


def one_sentence(text: str | None) -> str:
    """Clip already-produced copy to a single plain-language sentence."""
    cleaned = " ".join(str(text or "").split()).strip()
    if not cleaned:
        return ""
    for separator in (". ", "! ", "? "):
        index = cleaned.find(separator)
        if index != -1:
            return cleaned[: index + 1].strip()
    if cleaned[-1] not in ".!?":
        return f"{cleaned}."
    return cleaned


def _normalise_code(code: str | None) -> str:
    if code is None:
        return ""
    return str(code).strip().lower().replace("-", "_").replace(" ", "_")

"""Recommendation explanations in student-facing language.

Translates educational evidence into explanations learners can act on.
Never exposes internal architectural terminology.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Internal → student terminology (authoritative for this package).
TERMINOLOGY_MAP: dict[str, str] = {
    "Student Digital Twin": "Learning Insights",
    "student digital twin": "Learning Insights",
    "Digital Twin": "Learning Insights",
    "digital twin": "Learning Insights",
    "Adaptive Decision Engine": "Today's Recommendation",
    "adaptive decision engine": "Today's Recommendation",
    "Adaptive Decision": "Today's Recommendation",
    "adaptive decision": "Today's Recommendation",
    "Readiness Score": "Exam Readiness",
    "readiness score": "Exam Readiness",
    "Mission Engine": "Today's Session",
    "mission engine": "Today's Session",
    "Learning Orchestrator": "Learning Activity",
    "learning orchestrator": "Learning Activity",
}

# Phrases that must never appear in student-facing copy.
FORBIDDEN_INTERNAL_TERMS: tuple[str, ...] = (
    "Student Digital Twin",
    "Digital Twin",
    "Adaptive Decision Engine",
    "Adaptive Decision",
    "Learning Orchestrator",
    "Mission Engine",
    "Readiness Score",
    "curriculum graph",
    "Curriculum Graph",
    "bounded context",
    "port adapter",
)


@dataclass(frozen=True)
class RecommendationExplanation:
    """Student-safe explanation of why something was recommended."""

    summary: str
    why_recommended: str
    evidence_points: tuple[str, ...] = field(default_factory=tuple)
    expected_benefit: str = ""
    confidence_label: str = ""

    @classmethod
    def create(
        cls,
        *,
        summary: str = "",
        why_recommended: str = "",
        evidence_points: list[str] | tuple[str, ...] | None = None,
        expected_benefit: str = "",
        confidence_label: str = "",
    ) -> RecommendationExplanation:
        """Build an explanation after translating and validating copy."""
        points = tuple(
            translate_to_student_language(p)
            for p in (evidence_points or ())
        )
        return cls(
            summary=assert_student_safe(translate_to_student_language(summary)),
            why_recommended=assert_student_safe(
                translate_to_student_language(why_recommended)
            ),
            evidence_points=tuple(assert_student_safe(p) for p in points),
            expected_benefit=assert_student_safe(
                translate_to_student_language(expected_benefit)
            ),
            confidence_label=assert_student_safe(
                translate_to_student_language(confidence_label)
            ),
        )

    @property
    def is_complete(self) -> bool:
        """True when summary and why_recommended are both present."""
        return bool(self.summary.strip() and self.why_recommended.strip())


def translate_to_student_language(text: str | None) -> str:
    """Replace internal terms with student-facing vocabulary."""
    if text is None:
        return ""
    result = str(text)
    # Longer keys first to avoid partial replacements.
    for internal, student in sorted(
        TERMINOLOGY_MAP.items(), key=lambda kv: len(kv[0]), reverse=True
    ):
        result = result.replace(internal, student)
    return result.strip()


def is_student_safe(text: str | None) -> bool:
    """True when ``text`` contains no forbidden internal terminology."""
    if not text:
        return True
    lowered = text.lower()
    for term in FORBIDDEN_INTERNAL_TERMS:
        if term.lower() in lowered:
            return False
    return True


def assert_student_safe(text: str) -> str:
    """Return ``text`` or raise if forbidden internal terms remain."""
    translated = translate_to_student_language(text)
    if not is_student_safe(translated):
        offenders = [
            t
            for t in FORBIDDEN_INTERNAL_TERMS
            if t.lower() in translated.lower()
        ]
        raise ValueError(
            "student-facing text contains internal terminology: "
            + ", ".join(offenders)
        )
    return translated


def build_explanation(
    *,
    topic_title: str = "",
    reason_codes: list[str] | tuple[str, ...] | None = None,
    evidence_phrases: list[str] | tuple[str, ...] | None = None,
    expected_benefit: str = "",
    priority_band: str = "",
    confidence: str = "",
) -> RecommendationExplanation:
    """Compose a student explanation from educational evidence phrases.

    Does not calculate educational signals — only projects provided evidence
    into learner language.
    """
    topic = (topic_title or "").strip() or "this topic"
    codes = tuple(reason_codes or ())
    phrases = [
        translate_to_student_language(p)
        for p in (evidence_phrases or ())
        if str(p).strip()
    ]

    why_parts: list[str] = []
    for code in codes:
        key = str(code).strip().lower()
        why_parts.append(_reason_code_to_phrase(key, topic))
    if not why_parts and phrases:
        why_parts.append(phrases[0])
    if not why_parts:
        why_parts.append(
            f"This is the highest-value next step for {topic} based on "
            "your recent learning evidence."
        )

    summary = f"Focus on {topic} next."
    if priority_band:
        band = translate_to_student_language(priority_band)
        summary = f"{band.capitalize()} priority: focus on {topic}."

    benefit = translate_to_student_language(expected_benefit) or (
        f"Studying {topic} now is expected to strengthen your exam readiness."
    )
    confidence_label = translate_to_student_language(confidence)

    return RecommendationExplanation.create(
        summary=summary,
        why_recommended=" ".join(why_parts),
        evidence_points=tuple(phrases),
        expected_benefit=benefit,
        confidence_label=confidence_label,
    )


def _reason_code_to_phrase(code: str, topic: str) -> str:
    mapping = {
        "low_retention": (
            f"Your recall for {topic} has softened, so a short review "
            "will protect what you have already learned."
        ),
        "declining_confidence": (
            f"Your confidence for {topic} has dipped relative to recent "
            "performance, so a focused review will rebuild certainty."
        ),
        "exam_proximity": (
            f"{topic.capitalize()} is high value with the exam approaching."
        ),
        "prerequisite_gap": (
            f"Strengthening {topic} unlocks the next topics on your journey."
        ),
        "high_roi": (
            f"A short session on {topic} offers strong educational return "
            "for the time invested."
        ),
        "overdue_revision": (
            f"It has been a while since you last revisited {topic}."
        ),
        "mastery_incomplete": (
            f"You have made progress on {topic}, but it is not yet solid "
            "enough for exam conditions."
        ),
    }
    return mapping.get(
        code,
        f"Your learning evidence points to {topic} as the best next step.",
    )

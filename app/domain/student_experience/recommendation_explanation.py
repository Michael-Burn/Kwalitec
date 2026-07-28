"""Recommendation explanations in student-facing language.

Translates educational evidence into explanations learners can act on.
Never exposes internal architectural terminology.

EP-006.2: when Runtime A attaches a schema-complete Meaningful Explanation
Schema (MES), presentation must pass authored fields through — reason-code
re-narration is fallback only for incomplete / cold-start payloads.
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
    suggested_next_action: str = ""
    review_point: str = ""
    confidence_basis: str = ""
    # EP-008.1 — Recommendation Trust (pass-through / composed presentation).
    plan_coherence: str = ""
    plan_coherence_label: str = ""
    honest_refusal: bool = False
    timeliness_line: str = ""
    completion_loop_line: str = ""

    @classmethod
    def create(
        cls,
        *,
        summary: str = "",
        why_recommended: str = "",
        evidence_points: list[str] | tuple[str, ...] | None = None,
        expected_benefit: str = "",
        confidence_label: str = "",
        suggested_next_action: str = "",
        review_point: str = "",
        confidence_basis: str = "",
        plan_coherence: str = "",
        plan_coherence_label: str = "",
        honest_refusal: bool = False,
        timeliness_line: str = "",
        completion_loop_line: str = "",
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
            suggested_next_action=assert_student_safe(
                translate_to_student_language(suggested_next_action)
            ),
            review_point=assert_student_safe(
                translate_to_student_language(review_point)
            ),
            confidence_basis=assert_student_safe(
                translate_to_student_language(confidence_basis)
            ),
            plan_coherence=assert_student_safe(
                translate_to_student_language(plan_coherence)
            ),
            plan_coherence_label=assert_student_safe(
                translate_to_student_language(plan_coherence_label)
            ),
            honest_refusal=bool(honest_refusal),
            timeliness_line=assert_student_safe(
                translate_to_student_language(timeliness_line)
            ),
            completion_loop_line=assert_student_safe(
                translate_to_student_language(completion_loop_line)
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
    suggested_next_action: str = "",
    review_point: str = "",
    confidence_basis: str = "",
    why_recommended: str = "",
    summary: str = "",
    plan_coherence: str = "",
    plan_coherence_label: str = "",
    honest_refusal: bool = False,
    timeliness_line: str = "",
    completion_loop_line: str = "",
) -> RecommendationExplanation:
    """Compose a student explanation from educational evidence phrases.

    Does not calculate educational signals — only projects provided evidence
    into learner language.

    When ``why_recommended`` is already authored (schema-complete MES), pass it
    through instead of synthesising from reason codes.
    """
    topic = (topic_title or "").strip() or "this topic"
    codes = tuple(reason_codes or ())
    phrases = [
        translate_to_student_language(p)
        for p in (evidence_phrases or ())
        if str(p).strip()
    ]

    authored_why = translate_to_student_language(why_recommended)
    if authored_why:
        why_text = authored_why
    else:
        why_parts: list[str] = []
        for code in codes:
            key = str(code).strip().lower()
            why_parts.append(_reason_code_to_phrase(key, topic))
        if not why_parts and phrases:
            why_parts.append(phrases[0])
        if not why_parts:
            why_parts.append(
                f"This is the highest-value next step for {topic} based on "
                "your recent practice."
            )
        why_text = " ".join(why_parts)

    authored_summary = translate_to_student_language(summary)
    if authored_summary:
        summary_text = authored_summary
    else:
        summary_text = f"Focus on {topic} next."
        if priority_band:
            band = translate_to_student_language(priority_band)
            summary_text = f"{band.capitalize()} priority: focus on {topic}."

    benefit = translate_to_student_language(expected_benefit)
    if not benefit and not honest_refusal:
        benefit = (
            f"Studying {topic} now can support steady progress toward "
            "exam readiness."
        )
    confidence_label = translate_to_student_language(confidence)
    review = translate_to_student_language(review_point)
    loop_line = translate_to_student_language(completion_loop_line) or review

    return RecommendationExplanation.create(
        summary=summary_text,
        why_recommended=why_text,
        evidence_points=tuple(phrases),
        expected_benefit=benefit,
        confidence_label=confidence_label,
        suggested_next_action=translate_to_student_language(suggested_next_action),
        review_point=review,
        confidence_basis=translate_to_student_language(confidence_basis),
        plan_coherence=translate_to_student_language(plan_coherence),
        plan_coherence_label=translate_to_student_language(plan_coherence_label),
        honest_refusal=bool(honest_refusal),
        timeliness_line=translate_to_student_language(timeliness_line),
        completion_loop_line=loop_line,
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
        f"Your recent practice points to {topic} as the best next step.",
    )

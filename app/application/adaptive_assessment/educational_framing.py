"""ILE-001C — Contextual intent and educational framing (presentation only).

Composes Study Sensei explanation arcs from the Adaptive Assessment copy
registry and a lightweight presentation intent context. Does not call Twin,
Reasoning, Mission planning, Assessment Engine, or Tutor services.

Authority: ILE-001C0 communication standards, ILE-010 / ILE-011, P-001.2,
P-001.3. Learner-facing speech must never expose algorithms or scores.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.application.adaptive_assessment.accessibility import (
    AccessibilityMetadata,
    accessibility_for_session,
)
from app.application.adaptive_assessment.localisation import resolve_copy
from app.application.adaptive_assessment.session_registry import SessionTypeId


class EvidenceBand(StrEnum):
    """Qualitative presentation confidence band (ILE-011 labels).

    Not an internal model score. Used only to select registered copy.
    """

    INSUFFICIENT = "insufficient"
    OBSERVATION_ONLY = "observation_only"
    EMERGING = "emerging"
    RELIABLE = "reliable"
    HIGH = "high"


@dataclass(frozen=True)
class PresentationIntentContext:
    """Presentation-only intent inputs for framing composition.

    Attributes:
        focus_label: Learner-visible topic / Mission focus label.
        evidence_band: Qualitative band selecting copy variants.
        session_type_id: Session type for accessibility / labels.
    """

    focus_label: str = "today's focus"
    evidence_band: EvidenceBand = EvidenceBand.EMERGING
    session_type_id: str = SessionTypeId.QUICK_CHECK


@dataclass(frozen=True)
class ContextCardContract:
    """Pre-check Context Card — observation through invitation arc."""

    title: str
    observation_label: str
    observation: str
    meaning_label: str
    meaning: str
    purpose_label: str
    purpose: str
    benefit_label: str
    benefit: str
    invitation: str
    duration_label: str
    begin_label: str
    defer_label: str
    why_control_label: str
    why_expanded_body: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class EducationalSummaryContract:
    """Post-check Educational Summary — never scores or pass/fail."""

    title: str
    learned_label: str
    learned: str
    evidence_label: str
    evidence: str
    meaning_label: str
    meaning: str
    next_label: str
    next_step: str
    return_label: str
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class RecommendationFrameContract:
    """Recommendation framing — educational reasoning only."""

    headline_label: str
    recommendation: str
    reason_label: str
    reason: str
    evidence_label: str
    supporting_evidence: str
    confidence_label: str
    confidence_level: str
    outcome_label: str
    expected_outcome: str
    uncertainty: str
    show_uncertainty: bool
    why_label: str
    why_body: str
    accept_label: str
    defer_label: str
    is_guidance_only: bool
    guidance_note: str
    suppress_primary: bool
    accessibility: AccessibilityMetadata


@dataclass(frozen=True)
class ReflectionFrameContract:
    """Expanded reflection — observation → meaning → action → student choice."""

    title: str
    observation_label: str
    observation: str
    meaning_label: str
    meaning: str
    action_label: str
    suggested_action: str
    choice_label: str
    student_choice_prompt: str
    prompt: str
    continue_label: str
    accept_choice_label: str
    defer_choice_label: str
    own_choice_label: str
    pause_label: str
    accessibility: AccessibilityMetadata


def _a11y() -> AccessibilityMetadata:
    return accessibility_for_session(SessionTypeId.QUICK_CHECK)


def _focus(ctx: PresentationIntentContext) -> str:
    label = (ctx.focus_label or "").strip()
    return label if label else resolve_copy("framing.focus.fallback")


def _fmt(key: str, *, focus: str) -> str:
    return resolve_copy(key).format(focus=focus)


def default_intent_context(
    *,
    focus_label: str = "",
    evidence_band: EvidenceBand | str = EvidenceBand.EMERGING,
) -> PresentationIntentContext:
    """Build a default presentation intent context (no Twin lookup)."""
    band = (
        evidence_band
        if isinstance(evidence_band, EvidenceBand)
        else EvidenceBand(str(evidence_band))
    )
    return PresentationIntentContext(
        focus_label=(focus_label or "").strip()
        or resolve_copy("framing.focus.fallback"),
        evidence_band=band,
    )


def build_context_card(
    ctx: PresentationIntentContext,
    *,
    duration_label: str,
) -> ContextCardContract:
    """Compose the Context Card from ILE-001C0-aligned copy keys."""
    focus = _focus(ctx)
    return ContextCardContract(
        title=resolve_copy("framing.context.title"),
        observation_label=resolve_copy("framing.label.observation"),
        observation=_fmt("framing.context.observation", focus=focus),
        meaning_label=resolve_copy("framing.label.meaning"),
        meaning=_fmt("framing.context.meaning", focus=focus),
        purpose_label=resolve_copy("framing.label.purpose"),
        purpose=_fmt("framing.context.purpose", focus=focus),
        benefit_label=resolve_copy("framing.label.benefit"),
        benefit=resolve_copy("framing.context.benefit"),
        invitation=resolve_copy("framing.context.invitation"),
        duration_label=duration_label,
        begin_label=resolve_copy("quick_check.intro.begin"),
        defer_label=resolve_copy("action.defer"),
        why_control_label=resolve_copy("explain.why_am_i_seeing_this"),
        why_expanded_body=_fmt("framing.context.why_expanded", focus=focus),
        accessibility=_a11y(),
    )


def build_educational_summary(
    ctx: PresentationIntentContext,
) -> EducationalSummaryContract:
    """Compose the post-check Educational Summary."""
    focus = _focus(ctx)
    return EducationalSummaryContract(
        title=resolve_copy("framing.summary.title"),
        learned_label=resolve_copy("framing.label.learned"),
        learned=_fmt("framing.summary.learned", focus=focus),
        evidence_label=resolve_copy("framing.label.evidence"),
        evidence=resolve_copy("framing.summary.evidence"),
        meaning_label=resolve_copy("framing.label.meaning"),
        meaning=resolve_copy("framing.summary.meaning"),
        next_label=resolve_copy("framing.label.next"),
        next_step=resolve_copy("framing.summary.next"),
        return_label=resolve_copy("quick_check.completion.return"),
        accessibility=_a11y(),
    )


def build_recommendation_frame(
    ctx: PresentationIntentContext,
) -> RecommendationFrameContract:
    """Compose recommendation framing with honesty for thin evidence."""
    focus = _focus(ctx)
    band = ctx.evidence_band
    suppress = band in {
        EvidenceBand.INSUFFICIENT,
        EvidenceBand.OBSERVATION_ONLY,
    }
    confidence_key = f"framing.confidence.{band.value}"
    reason_key = (
        "framing.recommendation.reason.insufficient"
        if suppress
        else f"framing.recommendation.reason.{band.value}"
    )
    if band == EvidenceBand.HIGH:
        reason_key = "framing.recommendation.reason.reliable"
    uncertainty_key = {
        EvidenceBand.INSUFFICIENT: "framing.uncertainty.insufficient",
        EvidenceBand.OBSERVATION_ONLY: "framing.uncertainty.observation_only",
        EvidenceBand.EMERGING: "framing.uncertainty.emerging",
        EvidenceBand.RELIABLE: "framing.uncertainty.reliable",
        EvidenceBand.HIGH: "framing.uncertainty.reliable",
    }[band]
    recommendation = (
        resolve_copy("framing.recommendation.hold")
        if suppress
        else _fmt("framing.recommendation.continue_mission", focus=focus)
    )
    reason_template = resolve_copy(reason_key)
    reason = (
        reason_template.format(focus=focus)
        if "{focus}" in reason_template
        else reason_template
    )
    show_uncertainty = band != EvidenceBand.HIGH
    return RecommendationFrameContract(
        headline_label=resolve_copy("framing.label.recommendation"),
        recommendation=recommendation,
        reason_label=resolve_copy("framing.label.reason"),
        reason=reason,
        evidence_label=resolve_copy("framing.label.supporting_evidence"),
        supporting_evidence=_fmt(
            "framing.recommendation.supporting_evidence", focus=focus
        ),
        confidence_label=resolve_copy("framing.label.confidence"),
        confidence_level=resolve_copy(confidence_key),
        outcome_label=resolve_copy("framing.label.expected_outcome"),
        expected_outcome=resolve_copy(
            "framing.recommendation.expected_outcome"
        ),
        uncertainty=resolve_copy(uncertainty_key),
        show_uncertainty=show_uncertainty,
        why_label=resolve_copy("framing.recommendation.why_label"),
        why_body=_fmt("framing.recommendation.why_body", focus=focus),
        accept_label=resolve_copy("framing.recommendation.accept"),
        defer_label=resolve_copy("framing.recommendation.defer"),
        is_guidance_only=True,
        guidance_note=resolve_copy("framing.recommendation.guidance_note"),
        suppress_primary=suppress,
        accessibility=_a11y(),
    )


def build_reflection_frame(
    ctx: PresentationIntentContext,
) -> ReflectionFrameContract:
    """Compose expanded reflection with student agency preserved."""
    focus = _focus(ctx)
    return ReflectionFrameContract(
        title=resolve_copy("framing.reflection.title"),
        observation_label=resolve_copy("framing.label.observation"),
        observation=_fmt("framing.reflection.observation", focus=focus),
        meaning_label=resolve_copy("framing.label.meaning"),
        meaning=resolve_copy("framing.reflection.meaning"),
        action_label=resolve_copy("framing.label.suggested_action"),
        suggested_action=resolve_copy("framing.reflection.suggested_action"),
        choice_label=resolve_copy("framing.label.student_choice"),
        student_choice_prompt=resolve_copy(
            "framing.reflection.student_choice"
        ),
        prompt=resolve_copy("quick_check.reflection.prompt"),
        continue_label=resolve_copy("quick_check.reflection.continue"),
        accept_choice_label=resolve_copy("framing.reflection.choice_accept"),
        defer_choice_label=resolve_copy("framing.reflection.choice_defer"),
        own_choice_label=resolve_copy("framing.reflection.choice_own"),
        pause_label=resolve_copy("action.pause"),
        accessibility=_a11y(),
    )

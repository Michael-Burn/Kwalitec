"""Daily Mission Intelligence composition (ILE-004).

Pure projection of authorised educational evidence into one primary daily
mission brief. Never re-selects next actions, never invents ranking, never
duplicates Decision / Recommendation / Twin authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from app.domain.daily_mission_intelligence.enums import (
    AXIS_LABELS,
    MissionLifecyclePhase,
    MissionOptimisationAxis,
)
from app.domain.daily_mission_intelligence.invariants import (
    assert_mission_speech_safe,
)
from app.domain.decision_journal.enums import QualitativeConfidence


@dataclass(frozen=True)
class DailyMissionEvidenceInput:
    """Opaque educational evidence available for today's mission brief.

    All fields are already-authored student-safe fragments from upstream
    Recommendation / MES / Home projection. Composition never calls the
    Decision Engine or Recommendation Engine.
    """

    title: str = ""
    summary: str = ""
    why_recommended: str = ""
    timeliness_line: str = ""
    supporting_evidence: tuple[str, ...] = ()
    estimated_effort: str = ""
    expected_benefit: str = ""
    suggested_next_action: str = ""
    review_point: str = ""
    completion_loop_line: str = ""
    confidence_label: str = ""
    confidence_basis: str = ""
    uncertainty: str = ""
    honest_refusal: bool = False
    alternative_titles: tuple[str, ...] = ()
    recommendation_key: str = ""
    mission_id: str = ""
    session_id: str = ""
    educational_context: str = ""
    optimisation_axis: str = MissionOptimisationAxis.LEARNING_VALUE.value
    lifecycle_phase: str = MissionLifecyclePhase.CREATED.value
    prior_deferral_note: str = ""


@dataclass(frozen=True)
class DailyMissionBrief:
    """One primary daily educational mission — Study Sensei projection.

    Guiding principle: one day, one primary mission, one educational reason,
    one expected benefit.
    """

    title: str
    educational_purpose: str
    why_today: str
    why_not_something_else: str
    supporting_evidence: tuple[str, ...]
    estimated_effort: str
    expected_learning_outcome: str
    what_happens_after_completion: str
    reflection_prompt: str
    mission_confidence: str
    uncertainty: str
    mission_explanation: str
    skip_consequence: str
    optimisation_axis_label: str
    lifecycle_phase: MissionLifecyclePhase
    qualitative_confidence: QualitativeConfidence
    recommendation_key: str = ""
    mission_id: str = ""
    session_id: str = ""
    educational_context: str = ""
    empty: bool = False
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @property
    def has_mission(self) -> bool:
        return not self.empty and bool(self.title.strip())


def empty_mission_brief(
    *,
    reason: str = "",
) -> DailyMissionBrief:
    """Calm empty state when no authorised recommendation is available."""
    purpose = reason or (
        "When educational evidence supports a clear next step, "
        "today's Mission will appear here."
    )
    return DailyMissionBrief(
        title="Today's Mission",
        educational_purpose=purpose,
        why_today="",
        why_not_something_else="",
        supporting_evidence=(),
        estimated_effort="",
        expected_learning_outcome="",
        what_happens_after_completion="",
        reflection_prompt=(
            "What would make tomorrow's focus clearer than today's?"
        ),
        mission_confidence="Not enough evidence yet",
        uncertainty=(
            "Without a clear recommendation, the Study Sensei waits "
            "rather than inventing work."
        ),
        mission_explanation=purpose,
        skip_consequence="",
        optimisation_axis_label=AXIS_LABELS[
            MissionOptimisationAxis.LEARNING_VALUE.value
        ],
        lifecycle_phase=MissionLifecyclePhase.CREATED,
        qualitative_confidence=QualitativeConfidence.INSUFFICIENT,
        empty=True,
        metadata=(("availability", "empty"),),
    )


def compose_daily_mission(
    evidence: DailyMissionEvidenceInput | Mapping[str, Any],
) -> DailyMissionBrief:
    """Compose one primary mission brief from authorised evidence.

    Args:
        evidence: Authored educational fragments (DTO or mapping).

    Returns:
        Immutable ``DailyMissionBrief``. Empty when no title/recommendation.
    """
    inp = _normalise_input(evidence)
    title = (inp.title or "").strip()
    if not title or inp.honest_refusal:
        reason = ""
        if inp.honest_refusal:
            reason = (
                inp.confidence_label
                or "Evidence is not strong enough to name a confident Mission."
            )
        return empty_mission_brief(reason=reason)

    purpose = _first_nonempty(
        inp.why_recommended,
        inp.summary,
        inp.suggested_next_action,
        f"Today's Mission focuses on {title}.",
    )
    why_today = _first_nonempty(
        inp.timeliness_line,
        "It is the highest-value next step given your plan and recent evidence.",
    )
    why_not = _why_not_something_else(inp)
    evidence_points = tuple(
        p.strip() for p in inp.supporting_evidence if (p or "").strip()
    )
    if not evidence_points and inp.summary:
        evidence_points = (inp.summary.strip(),)

    outcome = _first_nonempty(
        inp.expected_benefit,
        "A clearer sense of where this focus sits in your learning.",
    )
    after = _first_nonempty(
        inp.completion_loop_line,
        inp.review_point,
        "Mission complete — evidence from today's loop is recorded.",
    )
    confidence = _first_nonempty(
        inp.confidence_label,
        "Emerging confidence",
    )
    uncertainty = _first_nonempty(
        inp.uncertainty,
        inp.confidence_basis if _looks_uncertain(inp.confidence_basis) else "",
        "Some uncertainty remains — guidance stays provisional.",
    )
    explanation = _compose_explanation(
        purpose=purpose,
        why_today=why_today,
        outcome=outcome,
        uncertainty=uncertainty,
        prior_deferral=inp.prior_deferral_note,
    )
    skip = _first_nonempty(
        _skip_line(inp),
        "If you skip today, the same educational need may remain — "
        "the Study Sensei will meet you when you return.",
    )
    reflection = _reflection_prompt(inp)
    axis = _resolve_axis(inp.optimisation_axis)
    phase = _resolve_phase(inp.lifecycle_phase)
    qual = _map_confidence(confidence, inp.honest_refusal)

    brief = DailyMissionBrief(
        title=title,
        educational_purpose=purpose,
        why_today=why_today,
        why_not_something_else=why_not,
        supporting_evidence=evidence_points,
        estimated_effort=(inp.estimated_effort or "").strip(),
        expected_learning_outcome=outcome,
        what_happens_after_completion=after,
        reflection_prompt=reflection,
        mission_confidence=confidence,
        uncertainty=uncertainty,
        mission_explanation=explanation,
        skip_consequence=skip,
        optimisation_axis_label=AXIS_LABELS[axis.value],
        lifecycle_phase=phase,
        qualitative_confidence=qual,
        recommendation_key=(inp.recommendation_key or "").strip(),
        mission_id=(inp.mission_id or "").strip(),
        session_id=(inp.session_id or "").strip(),
        educational_context=_first_nonempty(
            inp.educational_context,
            "Today's Mission",
        ),
        empty=False,
        metadata=(
            ("source", "authorised_recommendation"),
            ("axis", axis.value),
        ),
    )
    _validate_brief(brief)
    return brief


def _normalise_input(
    evidence: DailyMissionEvidenceInput | Mapping[str, Any],
) -> DailyMissionEvidenceInput:
    if isinstance(evidence, DailyMissionEvidenceInput):
        return evidence
    alts = evidence.get("alternative_titles") or ()
    if isinstance(alts, str):
        alts = (alts,)
    supporting = evidence.get("supporting_evidence") or ()
    if isinstance(supporting, str):
        supporting = (supporting,)
    return DailyMissionEvidenceInput(
        title=str(evidence.get("title") or ""),
        summary=str(evidence.get("summary") or ""),
        why_recommended=str(evidence.get("why_recommended") or ""),
        timeliness_line=str(evidence.get("timeliness_line") or ""),
        supporting_evidence=tuple(str(p) for p in supporting),
        estimated_effort=str(evidence.get("estimated_effort") or ""),
        expected_benefit=str(evidence.get("expected_benefit") or ""),
        suggested_next_action=str(
            evidence.get("suggested_next_action") or ""
        ),
        review_point=str(evidence.get("review_point") or ""),
        completion_loop_line=str(
            evidence.get("completion_loop_line") or ""
        ),
        confidence_label=str(evidence.get("confidence_label") or ""),
        confidence_basis=str(evidence.get("confidence_basis") or ""),
        uncertainty=str(evidence.get("uncertainty") or ""),
        honest_refusal=bool(evidence.get("honest_refusal")),
        alternative_titles=tuple(str(a) for a in alts),
        recommendation_key=str(evidence.get("recommendation_key") or ""),
        mission_id=str(evidence.get("mission_id") or ""),
        session_id=str(evidence.get("session_id") or ""),
        educational_context=str(evidence.get("educational_context") or ""),
        optimisation_axis=str(
            evidence.get("optimisation_axis")
            or MissionOptimisationAxis.LEARNING_VALUE.value
        ),
        lifecycle_phase=str(
            evidence.get("lifecycle_phase")
            or MissionLifecyclePhase.CREATED.value
        ),
        prior_deferral_note=str(evidence.get("prior_deferral_note") or ""),
    )


def _first_nonempty(*parts: str) -> str:
    for part in parts:
        if (part or "").strip():
            return part.strip()
    return ""


def _why_not_something_else(inp: DailyMissionEvidenceInput) -> str:
    alts = [a.strip() for a in inp.alternative_titles if (a or "").strip()]
    if alts:
        listed = ", ".join(alts[:3])
        return (
            f"Other options such as {listed} remain available, "
            "but today's Mission is the highest-value focus given "
            "current evidence."
        )
    return (
        "Other syllabus work can wait — this Mission is the clearest "
        "educational priority for today."
    )


def _compose_explanation(
    *,
    purpose: str,
    why_today: str,
    outcome: str,
    uncertainty: str,
    prior_deferral: str,
) -> str:
    parts = [
        purpose,
        f"Why today: {why_today}" if why_today else "",
        f"Expected benefit: {outcome}" if outcome else "",
    ]
    if prior_deferral.strip():
        parts.append(prior_deferral.strip())
    if uncertainty.strip():
        parts.append(f"Uncertainty: {uncertainty.strip()}")
    return " ".join(p for p in parts if p)


def _skip_line(inp: DailyMissionEvidenceInput) -> str:
    if inp.prior_deferral_note.strip():
        return (
            "You deferred related guidance before. Skipping again is honest — "
            "the educational need may still be waiting when you return."
        )
    return ""


def _reflection_prompt(inp: DailyMissionEvidenceInput) -> str:
    if inp.prior_deferral_note.strip():
        return (
            "Was today's Mission appropriate — and should tomorrow be different?"
        )
    return (
        "Was this Mission the right focus today? What changed — "
        "and should tomorrow be different?"
    )


def _looks_uncertain(text: str) -> bool:
    lowered = (text or "").lower()
    markers = ("uncertain", "limited", "provisional", "not enough", "emerging")
    return any(m in lowered for m in markers)


def _resolve_axis(raw: str) -> MissionOptimisationAxis:
    try:
        return MissionOptimisationAxis(str(raw))
    except ValueError:
        return MissionOptimisationAxis.LEARNING_VALUE


def _resolve_phase(raw: str) -> MissionLifecyclePhase:
    try:
        return MissionLifecyclePhase(str(raw))
    except ValueError:
        return MissionLifecyclePhase.CREATED


def _map_confidence(
    label: str,
    honest_refusal: bool,
) -> QualitativeConfidence:
    if honest_refusal:
        return QualitativeConfidence.INSUFFICIENT
    lowered = (label or "").lower()
    if "not enough" in lowered or "insufficient" in lowered:
        return QualitativeConfidence.INSUFFICIENT
    if "observation" in lowered or "gathering" in lowered:
        return QualitativeConfidence.OBSERVATION_ONLY
    if "high" in lowered:
        return QualitativeConfidence.HIGH
    if "reliable" in lowered:
        return QualitativeConfidence.RELIABLE
    if "emerging" in lowered:
        return QualitativeConfidence.EMERGING
    return QualitativeConfidence.EMERGING


def _validate_brief(brief: DailyMissionBrief) -> None:
    for field_name, text in (
        ("title", brief.title),
        ("educational_purpose", brief.educational_purpose),
        ("why_today", brief.why_today),
        ("why_not_something_else", brief.why_not_something_else),
        ("expected_learning_outcome", brief.expected_learning_outcome),
        ("what_happens_after_completion", brief.what_happens_after_completion),
        ("reflection_prompt", brief.reflection_prompt),
        ("mission_confidence", brief.mission_confidence),
        ("uncertainty", brief.uncertainty),
        ("mission_explanation", brief.mission_explanation),
        ("skip_consequence", brief.skip_consequence),
    ):
        if text:
            assert_mission_speech_safe(text, field=field_name)
    for point in brief.supporting_evidence:
        assert_mission_speech_safe(point, field="supporting_evidence")

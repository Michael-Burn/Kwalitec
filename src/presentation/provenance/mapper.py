"""ProvenanceMapper — project existing evidence into provenance view models.

Presentation only. Surfaces already-produced Education OS / Application /
Student Experience evidence as up to three one-sentence reasons. Never
changes recommendation logic, never adds educational reasoning, never uses AI.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from presentation.provenance.enums import ProvenanceKind
from presentation.provenance.narration import (
    kind_for_reason_code,
    kind_for_sentence,
    narrate_reason_code,
    one_sentence,
)
from presentation.provenance.view_models import (
    DEFAULT_PROVENANCE_TITLE,
    MAX_PROVENANCE_REASONS,
    ProvenanceReasonView,
    ProvenanceViewModel,
)

_PLACEHOLDER_FRAGMENTS = (
    "will appear",
    "not available",
    "not ready",
    "not visible",
    "pending",
    "once you",
    "as you study",
    "as you complete",
    "when available",
    "when a study plan",
)


class ProvenanceMapper:
    """Collect and cap deterministic provenance reasons from display cargo."""

    @classmethod
    def for_mission(
        cls,
        workspace: Any = None,
        *,
        result: Any = None,
        experience: Any = None,
        title: str = "Why this mission",
    ) -> ProvenanceViewModel:
        candidates: list[ProvenanceReasonView] = []
        recommendation = getattr(workspace, "recommendation_summary", None)
        cls._push_code(
            candidates,
            getattr(recommendation, "category_label", None),
            fallback_kind=ProvenanceKind.RECOMMENDATION,
        )
        # Prefer structured reason codes from pipeline / evaluation decisions.
        cls._extend_from_result(candidates, result)
        cls._push_text(
            candidates,
            getattr(workspace, "mission_explanation", None),
            kind=ProvenanceKind.MISSION_PURPOSE,
        )
        cls._push_text(
            candidates,
            getattr(recommendation, "detail", None),
            kind=ProvenanceKind.RECOMMENDATION,
        )
        progress = getattr(workspace, "progress_summary", None)
        cls._push_text(
            candidates,
            getattr(progress, "trend_label", None),
            kind=ProvenanceKind.MASTERY_TREND,
        )
        session = getattr(workspace, "session_progress", None)
        cls._push_text(
            candidates,
            getattr(session, "mastery_trend_label", None),
            kind=ProvenanceKind.MASTERY_TREND,
        )
        if experience is not None:
            focus = _focus(experience)
            cls._push_text(
                candidates,
                getattr(focus, "reason", None),
                kind=ProvenanceKind.MISSION_PURPOSE,
            )
        return ProvenanceViewModel.from_reasons(
            candidates, title=title, surface="mission"
        )

    @classmethod
    def for_dashboard_hero(
        cls,
        *,
        workspace: Any = None,
        result: Any = None,
        experience: Any = None,
        hero: Any = None,
    ) -> ProvenanceViewModel:
        candidates: list[ProvenanceReasonView] = []
        cls._extend_from_result(candidates, result)
        focus = _focus(experience)
        cls._push_text(
            candidates,
            getattr(focus, "reason", None) or getattr(hero, "purpose", None),
            kind=ProvenanceKind.MISSION_PURPOSE,
        )
        cls._push_text(
            candidates,
            getattr(workspace, "mission_explanation", None),
            kind=ProvenanceKind.MISSION_PURPOSE,
        )
        home = getattr(experience, "home_snapshot", None) if experience else None
        cls._push_text(
            candidates,
            getattr(home, "progress_message", None),
            kind=ProvenanceKind.MASTERY_TREND,
        )
        return ProvenanceViewModel.from_reasons(
            candidates, title="Why today's mission", surface="dashboard"
        )

    @classmethod
    def for_journey(
        cls, experience: Any = None, *, result: Any = None
    ) -> ProvenanceViewModel:
        candidates: list[ProvenanceReasonView] = []
        snap = getattr(experience, "journey_snapshot", None) if experience else None
        cls._push_text(
            candidates,
            getattr(snap, "trajectory_message", None),
            kind=ProvenanceKind.JOURNEY,
        )
        cls._push_text(
            candidates,
            getattr(snap, "consistency_message", None),
            kind=ProvenanceKind.MASTERY_TREND,
        )
        cls._push_text(
            candidates,
            getattr(snap, "habits_message", None),
            kind=ProvenanceKind.JOURNEY,
        )
        cls._push_text(
            candidates,
            getattr(snap, "home_focus_headline", None),
            kind=ProvenanceKind.CURRICULUM_DEPENDENCY,
        )
        if not candidates:
            cls._extend_from_result(candidates, result)
        return ProvenanceViewModel.from_reasons(
            candidates, title="Why this journey view", surface="journey"
        )

    @classmethod
    def for_readiness(
        cls, experience: Any = None, *, result: Any = None
    ) -> ProvenanceViewModel:
        candidates: list[ProvenanceReasonView] = []
        snap = (
            getattr(experience, "readiness_snapshot", None) if experience else None
        )
        cls._push_text(
            candidates,
            getattr(snap, "direction_message", None),
            kind=ProvenanceKind.READINESS,
        )
        cls._push_text(
            candidates,
            getattr(snap, "assessment_confidence_label", None),
            kind=ProvenanceKind.EVIDENCE_FRESHNESS,
        )
        cls._push_text(
            candidates,
            getattr(snap, "journey_trajectory_message", None),
            kind=ProvenanceKind.MASTERY_TREND,
        )
        if getattr(snap, "days_remaining", None) is not None:
            days = snap.days_remaining
            cls._push_text(
                candidates,
                f"Your exam target is {days} day{'s' if days != 1 else ''} away.",
                kind=ProvenanceKind.UPCOMING_MILESTONE,
            )
        if not candidates:
            cls._extend_from_result(candidates, result)
        return ProvenanceViewModel.from_reasons(
            candidates, title="Why this readiness state", surface="readiness"
        )

    @classmethod
    def for_coach(
        cls, experience: Any = None, *, result: Any = None
    ) -> ProvenanceViewModel:
        """Coach consumes the same provenance sources — explains, never decides."""
        candidates: list[ProvenanceReasonView] = []
        coach = getattr(experience, "coach", None) if experience else None
        snap = getattr(experience, "coach_snapshot", None) if experience else None
        cards = getattr(coach, "explanation_cards", None) if coach else None
        card_items = getattr(cards, "cards", None) if cards is not None else None
        if card_items:
            for card in tuple(card_items)[:MAX_PROVENANCE_REASONS]:
                cls._push_text(
                    candidates,
                    getattr(card, "body", None),
                    kind=ProvenanceKind.COACH,
                )
        cls._push_text(
            candidates,
            getattr(snap, "focus_headline", None),
            kind=ProvenanceKind.MISSION_PURPOSE,
        )
        cls._push_text(
            candidates,
            getattr(snap, "journey_message", None),
            kind=ProvenanceKind.JOURNEY,
        )
        cls._push_text(
            candidates,
            getattr(snap, "readiness_label", None),
            kind=ProvenanceKind.READINESS,
        )
        # Same evaluation evidence the dashboard/mission surfaces use.
        cls._extend_from_result(candidates, result)
        if not candidates and experience is not None:
            # Fall back to shared mission / readiness / journey evidence.
            shared = [
                *cls.for_dashboard_hero(experience=experience, result=result).reasons,
                *cls.for_readiness(experience, result=result).reasons,
                *cls.for_journey(experience, result=result).reasons,
            ]
            for reason in shared:
                if len(candidates) >= MAX_PROVENANCE_REASONS:
                    break
                if reason.sentence not in {item.sentence for item in candidates}:
                    candidates.append(reason)
        return ProvenanceViewModel.from_reasons(
            candidates, title="Why this coach insight", surface="coach"
        )

    @classmethod
    def for_revision(
        cls,
        revision: Any = None,
        *,
        experience: Any = None,
        result: Any = None,
    ) -> ProvenanceViewModel:
        candidates: list[ProvenanceReasonView] = []
        primary = getattr(revision, "primary", None) if revision else None
        explanation = getattr(primary, "explanation", None) if primary else None
        if explanation is None and revision is not None:
            explanation = getattr(revision, "explanation", None)
        cls._push_text(
            candidates,
            getattr(explanation, "why_recommended", None),
            kind=ProvenanceKind.REVISION_SPACING,
        )
        for point in tuple(getattr(explanation, "evidence_points", ()) or ())[
            :MAX_PROVENANCE_REASONS
        ]:
            cls._push_text(
                candidates, point, kind=ProvenanceKind.REVISION_SPACING
            )
        cls._push_text(
            candidates,
            getattr(primary, "expected_benefit", None)
            or getattr(explanation, "expected_benefit", None),
            kind=ProvenanceKind.RECOMMENDATION,
        )
        cls._push_text(
            candidates,
            getattr(primary, "priority_label", None),
            kind=ProvenanceKind.REVISION_SPACING,
        )
        # Revision missions from Education OS schedule / evaluation.
        cls._extend_from_result(candidates, result)
        if experience is not None and not candidates:
            focus = _focus(experience)
            cls._push_text(
                candidates,
                getattr(focus, "reason", None),
                kind=ProvenanceKind.REVISION_SPACING,
            )
        return ProvenanceViewModel.from_reasons(
            candidates, title="Why this revision", surface="revision"
        )

    @classmethod
    def for_reflection(
        cls,
        summary: Any = None,
        *,
        session: Any = None,
        weak_concept: str | None = None,
    ) -> ProvenanceViewModel:
        candidates: list[ProvenanceReasonView] = []
        for line in tuple(getattr(summary, "lines", ()) or ())[
            :MAX_PROVENANCE_REASONS
        ]:
            cls._push_text(candidates, line, kind=ProvenanceKind.REFLECTION)
        cls._push_text(
            candidates,
            getattr(summary, "detail", None),
            kind=ProvenanceKind.REFLECTION,
        )
        cls._push_text(
            candidates,
            weak_concept,
            kind=ProvenanceKind.WEAK_TOPIC,
        )
        explanation = getattr(session, "explanation", None) if session else None
        cls._push_text(
            candidates,
            getattr(explanation, "description", None),
            kind=ProvenanceKind.EVIDENCE_FRESHNESS,
        )
        if getattr(summary, "headline", None):
            cls._push_text(
                candidates,
                "This summary reflects evidence you just captured for the session.",
                kind=ProvenanceKind.EVIDENCE_FRESHNESS,
            )
        return ProvenanceViewModel.from_reasons(
            candidates, title="Why this reflection summary", surface="reflection"
        )

    @classmethod
    def for_surface(
        cls,
        surface: str,
        *,
        experience: Any = None,
        result: Any = None,
        workspace: Any = None,
        revision: Any = None,
        reflection_summary: Any = None,
    ) -> ProvenanceViewModel:
        key = (surface or "").strip().lower()
        if key in {"dashboard", "home", "hero"}:
            return cls.for_dashboard_hero(
                workspace=workspace, result=result, experience=experience
            )
        if key == "mission":
            return cls.for_mission(
                workspace, result=result, experience=experience
            )
        if key == "journey":
            return cls.for_journey(experience, result=result)
        if key == "readiness":
            return cls.for_readiness(experience, result=result)
        if key == "coach":
            return cls.for_coach(experience, result=result)
        if key in {"revision", "revision_planner"}:
            return cls.for_revision(
                revision, experience=experience, result=result
            )
        if key == "reflection":
            return cls.for_reflection(reflection_summary)
        return ProvenanceViewModel.empty(surface=key)

    # --- collectors ---------------------------------------------------------

    @classmethod
    def _extend_from_result(
        cls, candidates: list[ProvenanceReasonView], result: Any
    ) -> None:
        if result is None:
            return
        explanation = getattr(result, "explanation", None)
        cls._push_text(
            candidates,
            getattr(explanation, "summary", None),
            kind=ProvenanceKind.RECOMMENDATION,
        )
        recommendations = getattr(result, "recommendations", None)
        primary = getattr(recommendations, "primary", None)
        reason = getattr(primary, "reason", None) if primary else None
        cls._push_code(
            candidates,
            getattr(reason, "code", None) or getattr(reason, "value", None),
        )
        cls._push_text(
            candidates,
            getattr(reason, "statement", None),
            kind=ProvenanceKind.RECOMMENDATION,
        )
        evaluation = getattr(result, "evaluation", None)
        decisions = getattr(evaluation, "decisions", None) if evaluation else None
        if decisions:
            top = min(tuple(decisions), key=lambda item: getattr(item, "rank", 999))
            cls._push_code(candidates, getattr(top, "reason_summary", None))
            cls._push_text(
                candidates,
                getattr(top, "reason_summary", None),
                kind=ProvenanceKind.RECOMMENDATION,
            )
        progress = getattr(result, "progress", None)
        cls._push_text(
            candidates,
            getattr(progress, "educational_explanation", None),
            kind=ProvenanceKind.MASTERY_TREND,
        )
        mission = getattr(result, "mission", None)
        cls._push_text(
            candidates,
            getattr(mission, "educational_rationale", None),
            kind=ProvenanceKind.MISSION_PURPOSE,
        )

    @classmethod
    def _push_code(
        cls,
        candidates: list[ProvenanceReasonView],
        code: Any,
        *,
        fallback_kind: ProvenanceKind = ProvenanceKind.RECOMMENDATION,
    ) -> None:
        if len(candidates) >= MAX_PROVENANCE_REASONS:
            return
        raw = _enum_or_text(code)
        if not raw:
            return
        narrated = narrate_reason_code(raw)
        if narrated:
            kind = kind_for_reason_code(raw)
            cls._append(candidates, kind=kind, sentence=narrated)
            return
        # Unknown codes may already be plain sentences from application DTOs.
        sentence = one_sentence(raw.replace("_", " "))
        if sentence and not _looks_like_placeholder(sentence):
            cls._append(
                candidates,
                kind=kind_for_sentence(sentence, fallback=fallback_kind),
                sentence=sentence,
            )

    @classmethod
    def _push_text(
        cls,
        candidates: list[ProvenanceReasonView],
        text: Any,
        *,
        kind: ProvenanceKind,
    ) -> None:
        if len(candidates) >= MAX_PROVENANCE_REASONS:
            return
        sentence = one_sentence(_enum_or_text(text))
        if not sentence or _looks_like_placeholder(sentence):
            return
        # Prefer structured narration when the text is itself a reason code.
        narrated = narrate_reason_code(sentence.rstrip("."))
        if narrated:
            cls._append(
                candidates,
                kind=kind_for_reason_code(sentence.rstrip(".")),
                sentence=narrated,
            )
            return
        resolved_kind = kind_for_sentence(sentence, fallback=kind)
        cls._append(candidates, kind=resolved_kind, sentence=sentence)

    @staticmethod
    def _append(
        candidates: list[ProvenanceReasonView],
        *,
        kind: ProvenanceKind,
        sentence: str,
    ) -> None:
        if len(candidates) >= MAX_PROVENANCE_REASONS:
            return
        if sentence in {item.sentence for item in candidates}:
            return
        candidates.append(
            ProvenanceReasonView(kind=kind.value, sentence=sentence)
        )


def _focus(experience: Any) -> Any:
    if experience is None:
        return None
    home = getattr(experience, "home", None)
    if home is not None:
        focus = getattr(home, "todays_focus", None)
        if focus is not None:
            return focus
    return getattr(experience, "todays_focus", None) or getattr(
        experience, "primary_focus", None
    )


def _enum_or_text(value: Any) -> str:
    if value is None:
        return ""
    if hasattr(value, "value") and not isinstance(value, str | bytes):
        try:
            return str(value.value).strip()
        except Exception:
            pass
    return str(value).strip()


def _looks_like_placeholder(text: str) -> bool:
    lowered = text.lower()
    return any(fragment in lowered for fragment in _PLACEHOLDER_FRAGMENTS)


def merge_provenance(
    *views: ProvenanceViewModel | None,
    title: str = DEFAULT_PROVENANCE_TITLE,
    surface: str = "",
) -> ProvenanceViewModel:
    """Merge existing provenance views without inventing new reasons."""
    reasons: list[ProvenanceReasonView] = []
    for view in views:
        if view is None or not view.available:
            continue
        for reason in view.reasons:
            if len(reasons) >= MAX_PROVENANCE_REASONS:
                break
            if reason.sentence not in {item.sentence for item in reasons}:
                reasons.append(reason)
    return ProvenanceViewModel.from_reasons(
        reasons, title=title, surface=surface
    )


def iter_reason_sentences(view: ProvenanceViewModel | None) -> Iterable[str]:
    if view is None:
        return ()
    return view.sentences

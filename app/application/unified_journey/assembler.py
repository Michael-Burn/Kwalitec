"""JourneyContextAssembler — compose presentation state from Programme I (P2-MS002).

Consumes Runtime A, Strategy, Digital Twin, Adaptive, and Evidence projections
read-only. Resolves presentation-ready JourneyContext values.

Must not create recommendations, override subsystem decisions, or perform
educational calculations.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.application.unified_journey.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_PLACEHOLDER,
    COMPLETION_VALUES,
    SOURCE_ADAPTIVE,
    SOURCE_DIGITAL_TWIN,
    SOURCE_EVIDENCE,
    SOURCE_EXPERIENCE,
    SOURCE_PLACEHOLDER,
    SOURCE_RUNTIME_A,
    SOURCE_STRATEGY,
    URGENCY_VALUES,
    JourneyContext,
    JourneySubsystemInputs,
    empty_journey_context,
)
from app.application.unified_journey.navigation_map import endpoint_for_stage
from app.application.unified_journey.stage_mapping import (
    mapping_for_stage,
    primary_subsystem_for_stage,
)
from app.application.unified_journey.stages import JourneyStage, resolve_journey_stage

# Pass-through source order for primary mission fields when stage mapping
# does not yield a filled projection. Strategy / Adaptive first match the
# coordinator's existing opaque next-action priority; Runtime A follows.
_SOURCE_ATTRS: tuple[tuple[str, str], ...] = (
    ("strategy", SOURCE_STRATEGY),
    ("adaptive", SOURCE_ADAPTIVE),
    ("runtime_a", SOURCE_RUNTIME_A),
    ("digital_twin", SOURCE_DIGITAL_TWIN),
    ("evidence", SOURCE_EVIDENCE),
)

_TITLE_KEYS = (
    "title",
    "topic_title",
    "recommendation_label",
    "mission_title",
    "primary_mission_title",
)
_REASON_KEYS = (
    "why_it_matters",
    "mission_reason",
    "summary",
    "rationale",
    "reason",
    "why_summary",
    "recommendation_rationale",
)
_OUTCOME_KEYS = (
    "expected_outcome",
    "expected_benefit",
    "educational_objective",
    "expected_benefit_delta",
)
_DURATION_MINUTE_KEYS = (
    "estimated_minutes",
    "minutes_budget",
    "estimated_study_minutes",
)
_DURATION_LABEL_KEYS = (
    "estimated_duration",
    "estimated_duration_label",
    "time_label",
)
_COMPLETION_KEYS = ("completion_state", "completion", "status")
_URGENCY_KEYS = ("urgency", "priority")
_TRANSITION_KEYS = ("next_transition", "next_stage", "journey_stage")
_CTA_KEYS = ("cta_label", "label", "action_label")
_ENDPOINT_KEYS = ("endpoint", "cta_endpoint")
_INSIGHT_KEYS = (
    "supporting_insight",
    "insight",
    "summary",
    "why_summary",
    "overall_completeness_explanation",
    "evidence_coverage_summary",
)


class JourneyContextAssembler:
    """Assemble JourneyContext from existing Programme I opaque projections.

    Responsibilities:
    - Consume Runtime A recommendations
    - Consume Strategy / Digital Twin / Adaptive / Evidence projections
    - Resolve presentation-ready values for the active stage

    Non-responsibilities:
    - Educational calculations
    - Recommendation generation
    - Overriding subsystem decisions
    - Persistence
    """

    def assemble(
        self,
        *,
        student_id: str,
        stage: JourneyStage | str,
        inputs: JourneySubsystemInputs | None = None,
    ) -> JourneyContext:
        """Compose an immutable JourneyContext for ``stage``.

        Prefers an explicit ``inputs.journey_context`` when provided. Otherwise
        resolves fields from opaque subsystem maps without inventing education.
        """
        _ = _require_student_id(student_id)
        resolved_stage = resolve_journey_stage(stage)
        active = inputs or JourneySubsystemInputs()

        if active.journey_context is not None:
            provided = active.journey_context
            if provided.stage != resolved_stage:
                return JourneyContext(
                    stage=resolved_stage,
                    mission_title=provided.mission_title,
                    mission_reason=provided.mission_reason,
                    estimated_duration=provided.estimated_duration,
                    expected_outcome=provided.expected_outcome,
                    completion_state=provided.completion_state,
                    urgency=provided.urgency,
                    next_transition=provided.next_transition,
                    supporting_insights=provided.supporting_insights,
                    cta_label=provided.cta_label,
                    cta_enabled=provided.cta_enabled,
                    endpoint=provided.endpoint or endpoint_for_stage(resolved_stage),
                    estimated_minutes=provided.estimated_minutes,
                    source=provided.source,
                    availability=provided.availability,
                    unavailable_reason=provided.unavailable_reason,
                    metadata=provided.metadata,
                    suggested_next_action=provided.suggested_next_action,
                    review_point=provided.review_point,
                    confidence_label=provided.confidence_label,
                    evidence_points=provided.evidence_points,
                    plan_drivers=provided.plan_drivers,
                    why_recommended=provided.why_recommended,
                )
            return provided

        if active.home_mission is not None and active.home_mission.title:
            mission = active.home_mission
            return JourneyContext(
                stage=resolved_stage,
                mission_title=mission.title,
                mission_reason=mission.why_it_matters,
                estimated_duration=mission.estimated_duration_label,
                expected_outcome=mission.expected_outcome,
                completion_state="",
                urgency="",
                next_transition="",
                supporting_insights=_supporting_insights(active),
                cta_label=mission.cta_label or "Continue",
                cta_enabled=mission.cta_enabled,
                endpoint=mission.endpoint or endpoint_for_stage(resolved_stage),
                estimated_minutes=None,
                source=_source_from_metadata(mission.metadata) or SOURCE_EXPERIENCE,
                availability=mission.availability,
                unavailable_reason=mission.unavailable_reason,
                metadata=mission.metadata + (("via", "home_mission"),),
            )

        if active.next_action is not None and active.next_action.title:
            action = active.next_action
            return JourneyContext(
                stage=resolved_stage,
                mission_title=action.title,
                mission_reason=action.why_it_matters or action.summary,
                estimated_duration=_duration_label(action.estimated_minutes),
                expected_outcome=action.expected_outcome,
                completion_state="",
                urgency="",
                next_transition="",
                supporting_insights=_supporting_insights(active),
                cta_label=action.cta_label or "Continue",
                cta_enabled=bool(action.endpoint),
                endpoint=action.endpoint or endpoint_for_stage(resolved_stage),
                estimated_minutes=action.estimated_minutes,
                source=action.source,
                availability=action.availability,
                unavailable_reason=action.unavailable_reason,
                metadata=action.metadata + (("via", "next_action"),),
            )

        primary = _primary_projection_bundle(active, stage=resolved_stage)
        if primary is None:
            placeholder = empty_journey_context(stage=resolved_stage)
            return JourneyContext(
                stage=resolved_stage,
                mission_title=placeholder.mission_title,
                mission_reason=placeholder.mission_reason,
                estimated_duration=placeholder.estimated_duration,
                expected_outcome=placeholder.expected_outcome,
                completion_state=placeholder.completion_state,
                urgency=placeholder.urgency,
                next_transition=placeholder.next_transition,
                supporting_insights=_supporting_insights(active),
                cta_label=placeholder.cta_label,
                cta_enabled=False,
                endpoint=endpoint_for_stage(resolved_stage),
                estimated_minutes=None,
                source=SOURCE_PLACEHOLDER,
                availability=AVAILABILITY_PLACEHOLDER,
                unavailable_reason=placeholder.unavailable_reason,
                metadata=(
                    ("primary_subsystem", primary_subsystem_for_stage(resolved_stage)),
                ),
            )

        source, payload = primary
        # Pass through an explicit stage on the projection when present —
        # never infer educationally; only honour subsystem-supplied values.
        payload_stage = _stage_from_payload(payload) or resolved_stage
        minutes = _first_int(payload, _DURATION_MINUTE_KEYS)
        duration = _first_str(payload, _DURATION_LABEL_KEYS) or _duration_label(minutes)
        title = _first_str(payload, _TITLE_KEYS)
        reason = _reason_from_payload(payload)
        outcome = _outcome_from_payload(payload)
        completion = _normalize_completion(_first_str(payload, _COMPLETION_KEYS))
        urgency = _normalize_urgency(_first_str(payload, _URGENCY_KEYS))
        transition = _first_str(payload, _TRANSITION_KEYS)
        cta = _first_str(payload, _CTA_KEYS) or "Continue"
        endpoint = (
            _first_str(payload, _ENDPOINT_KEYS) or endpoint_for_stage(payload_stage)
        )
        available = bool(title)
        mes = _mes_from_payload(payload)
        return JourneyContext(
            stage=payload_stage,
            mission_title=title,
            mission_reason=reason,
            estimated_duration=duration,
            expected_outcome=outcome,
            completion_state=completion,
            urgency=urgency,
            next_transition=transition,
            supporting_insights=_supporting_insights(active),
            cta_label=cta,
            cta_enabled=bool(endpoint) and available,
            endpoint=endpoint if available else endpoint_for_stage(payload_stage),
            estimated_minutes=minutes,
            source=source if available else SOURCE_PLACEHOLDER,
            availability=(
                AVAILABILITY_AVAILABLE if available else AVAILABILITY_PLACEHOLDER
            ),
            unavailable_reason="" if available else "engines_not_connected",
            metadata=(
                (
                    "primary_subsystem",
                    primary_subsystem_for_stage(payload_stage),
                ),
                ("capability", mapping_for_stage(payload_stage).capability),
            ),
            suggested_next_action=mes["suggested_next_action"],
            review_point=mes["review_point"],
            confidence_label=mes["confidence_label"],
            evidence_points=mes["evidence_points"],
            plan_drivers=mes["plan_drivers"],
            why_recommended=mes["why_recommended"],
        )


def _stage_from_payload(payload: Mapping[str, Any]) -> JourneyStage | None:
    raw = payload.get("stage") or payload.get("journey_stage")
    if raw is None:
        return None
    try:
        return resolve_journey_stage(str(raw))
    except ValueError:
        return None


def _require_student_id(student_id: str) -> str:
    if not isinstance(student_id, str) or not student_id.strip():
        raise ValueError("student_id must be a non-empty string")
    return student_id.strip()


def _primary_projection_bundle(
    inputs: JourneySubsystemInputs,
    *,
    stage: JourneyStage,
) -> tuple[str, Mapping[str, Any]] | None:
    """Pick the first non-empty primary payload for the stage.

    Prefer the stage's primary subsystem, then the remaining source order.
    Never recalculates recommendations — only selects an existing map.
    """
    preferred = primary_subsystem_for_stage(stage)
    ordered = _ordered_sources(preferred)
    for attr, source in ordered:
        projection = getattr(inputs, attr)
        payload = _mission_payload(projection)
        if payload is not None and _first_str(payload, _TITLE_KEYS):
            return source, payload
    # Partial: return first non-empty payload even without a title so
    # supporting fields (duration / insights) can still surface.
    for attr, source in ordered:
        projection = getattr(inputs, attr)
        payload = _mission_payload(projection)
        if payload is not None:
            return source, payload
    return None


def _ordered_sources(preferred: str) -> tuple[tuple[str, str], ...]:
    preferred_row = tuple(
        (attr, source) for attr, source in _SOURCE_ATTRS if source == preferred
    )
    rest = tuple(
        (attr, source) for attr, source in _SOURCE_ATTRS if source != preferred
    )
    return preferred_row + rest


def _mission_payload(
    projection: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    if not projection:
        return None
    nested = projection.get("next_action")
    if isinstance(nested, Mapping):
        # Merge nested next_action over top-level so either shape works.
        merged = dict(projection)
        merged.update(dict(nested))
        return merged
    return projection


def _supporting_insights(inputs: JourneySubsystemInputs) -> tuple[str, ...]:
    """Collect presentation-only insights from Twin / Evidence (never decisions)."""
    insights: list[str] = []
    for attr, _source in (
        ("digital_twin", SOURCE_DIGITAL_TWIN),
        ("evidence", SOURCE_EVIDENCE),
    ):
        projection = getattr(inputs, attr)
        if not projection:
            continue
        insights.extend(_insights_from_mapping(projection))
    # Deduplicate while preserving order.
    seen: set[str] = set()
    unique: list[str] = []
    for item in insights:
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return tuple(unique[:5])


def _insights_from_mapping(projection: Mapping[str, Any]) -> list[str]:
    found: list[str] = []
    explanation = projection.get("explanation_summary")
    if isinstance(explanation, Mapping):
        for key in _INSIGHT_KEYS:
            value = explanation.get(key)
            text = _as_insight(value)
            if text:
                found.append(text)
        facet_notes = explanation.get("facet_explanation_summaries")
        if isinstance(facet_notes, list | tuple):
            for note in facet_notes:
                text = _as_insight(note)
                if text:
                    found.append(text)
    for key in _INSIGHT_KEYS:
        text = _as_insight(projection.get(key))
        if text:
            found.append(text)
    facet_summaries = projection.get("facet_summaries")
    if isinstance(facet_summaries, Mapping):
        for facet in facet_summaries.values():
            if isinstance(facet, Mapping):
                for note_key in ("note", "summary", "cadence_note", "adherence_note"):
                    text = _as_insight(facet.get(note_key))
                    if text:
                        found.append(text)
    insights_list = projection.get("supporting_insights")
    if isinstance(insights_list, list | tuple):
        for item in insights_list:
            text = _as_insight(item)
            if text:
                found.append(text)
    return found


def _as_insight(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text or text.lower() in {"none", "null", "unavailable"}:
        return ""
    return text


def _reason_from_payload(payload: Mapping[str, Any]) -> str:
    direct = _first_str(payload, _REASON_KEYS)
    if direct:
        return direct
    explanation = payload.get("explanation")
    if isinstance(explanation, Mapping):
        return _first_str(
            explanation,
            ("why_recommended", "reason", "summary", "why_summary", "rationale"),
        )
    explanation_summary = payload.get("explanation_summary")
    if isinstance(explanation_summary, Mapping):
        return _first_str(
            explanation_summary,
            ("why_summary", "educational_objective", "confidence_rationale"),
        )
    return ""


def _outcome_from_payload(payload: Mapping[str, Any]) -> str:
    direct = _first_str(payload, _OUTCOME_KEYS)
    if direct:
        return direct
    explanation = payload.get("explanation")
    if isinstance(explanation, Mapping):
        return _first_str(explanation, ("expected_benefit", "expected_outcome"))
    return ""


def _mes_from_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Extract authored MES slots from an opaque Runtime A / explanation map."""
    explanation = payload.get("explanation")
    nested: Mapping[str, Any] = (
        explanation if isinstance(explanation, Mapping) else {}
    )

    def _pick(*keys: str) -> str:
        for key in keys:
            for source in (payload, nested):
                value = source.get(key)
                if value is None:
                    continue
                text = str(value).strip()
                if text:
                    return text
        return ""

    evidence_raw = (
        payload.get("supporting_evidence")
        or payload.get("evidence_points")
        or nested.get("supporting_evidence")
        or nested.get("evidence_points")
        or ()
    )
    evidence: list[str] = []
    if isinstance(evidence_raw, str) and evidence_raw.strip():
        evidence = [evidence_raw.strip()]
    elif isinstance(evidence_raw, list | tuple):
        evidence = [str(item).strip() for item in evidence_raw if str(item).strip()]

    drivers_raw = payload.get("plan_drivers") or nested.get("plan_drivers") or ()
    drivers: list[str] = []
    if isinstance(drivers_raw, list | tuple):
        for item in drivers_raw:
            if isinstance(item, Mapping):
                label = str(item.get("label") or item.get("driver_id") or "").strip()
                if label:
                    drivers.append(label.replace("_", " "))
            elif str(item).strip():
                drivers.append(str(item).strip())

    return {
        "suggested_next_action": _pick(
            "suggested_next_action", "next_action"
        ),
        "review_point": _pick("review_point"),
        "confidence_label": _pick(
            "confidence_label", "confidence_level", "confidence"
        ),
        "evidence_points": tuple(evidence[:6]),
        "plan_drivers": tuple(drivers[:3]),
        "why_recommended": _pick("why_recommended", "why_this_plan"),
    }


def _first_str(payload: Mapping[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def _first_int(payload: Mapping[str, Any], keys: tuple[str, ...]) -> int | None:
    for key in keys:
        value = payload.get(key)
        if value is None or value == "":
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _normalize_completion(raw: str) -> str:
    value = (raw or "").strip().lower().replace(" ", "_")
    aliases = {
        "done": "complete",
        "completed": "complete",
        "finished": "complete",
        "started": "in_progress",
        "active": "in_progress",
        "pending": "not_started",
        "new": "not_started",
    }
    value = aliases.get(value, value)
    return value if value in COMPLETION_VALUES else ""


def _normalize_urgency(raw: str) -> str:
    value = (raw or "").strip().lower()
    aliases = {
        "high": "high",
        "urgent": "high",
        "medium": "normal",
        "normal": "normal",
        "moderate": "normal",
        "low": "low",
    }
    value = aliases.get(value, value)
    return value if value in URGENCY_VALUES else ""


def _source_from_metadata(metadata: tuple[tuple[str, str], ...]) -> str:
    for key, value in metadata or ():
        if key == "source" and value:
            return str(value).strip().lower()
    return ""


def _duration_label(minutes: int | None) -> str:
    if minutes is None:
        return ""
    if minutes <= 0:
        return "Less than a minute"
    if minutes == 1:
        return "1 minute"
    if minutes < 60:
        return f"{minutes} minutes"
    hours, rem = divmod(minutes, 60)
    if rem == 0:
        return "1 hour" if hours == 1 else f"{hours} hours"
    hour_part = "1 hour" if hours == 1 else f"{hours} hours"
    return f"{hour_part} {rem} min"

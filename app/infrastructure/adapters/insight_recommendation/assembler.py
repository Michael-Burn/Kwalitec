"""Assemble student-facing study insight guidance (EP-001.4).

Presentation composition only. Explains Twin / Planner / Readiness outputs —
never invents learner state, plans, or readiness scores.
"""

from __future__ import annotations

from collections.abc import Mapping

from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
)
from app.infrastructure.adapters.insight_recommendation.contracts import (
    INSIGHT_LAYER_VERSION,
    InsightField,
    StudyInsightGuidance,
    StudyInsightInputs,
)


def _topic_id(row: Mapping[str, object] | None) -> str | None:
    if not row:
        return None
    value = row.get("topic_id")
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _topic_name(row: Mapping[str, object] | None) -> str:
    if not row:
        return ""
    return str(row.get("topic_name") or "").strip()


def _reason(row: Mapping[str, object] | None) -> str:
    if not row:
        return ""
    for key in ("reason", "rationale", "expected_benefit"):
        value = str(row.get(key) or "").strip()
        if value:
            return value
    return ""


def _focus_field(inputs: StudyInsightInputs) -> InsightField | None:
    if inputs.planner_missions:
        mission = inputs.planner_missions[0]
        name = _topic_name(mission) or str(mission.get("slot") or "today's mission")
        reason = _reason(mission) or "Planner priority for today."
        return InsightField(
            field_id="todays_key_focus",
            title="Today's key focus",
            message=f"Focus on {name}. {reason}",
            topic_id=_topic_id(mission),
            source="adaptive_study_planner.today_missions",
        )
    if inputs.planner_revision_priorities:
        revision = inputs.planner_revision_priorities[0]
        name = _topic_name(revision) or "a priority topic"
        reason = _reason(revision) or "Highest revision priority."
        return InsightField(
            field_id="todays_key_focus",
            title="Today's key focus",
            message=f"Focus on revising {name}. {reason}",
            topic_id=_topic_id(revision),
            source="adaptive_study_planner.revision_priorities",
        )
    if inputs.recommended_next_actions:
        action = inputs.recommended_next_actions[0]
        title = str(action.get("title") or "").strip() or "your next study step"
        reason = _reason(action) or "Readiness-grounded next action."
        return InsightField(
            field_id="todays_key_focus",
            title="Today's key focus",
            message=f"Focus on {title}. {reason}",
            topic_id=_topic_id(action),
            source="readiness_intelligence.recommended_next_actions",
        )
    return None


def _strongest_field(inputs: StudyInsightInputs) -> InsightField | None:
    if not inputs.strongest_areas:
        return None
    area = inputs.strongest_areas[0]
    name = _topic_name(area) or "a syllabus topic"
    reason = _reason(area) or "Highest Estimated Knowledge among observed topics."
    mastery = area.get("mastery_score")
    mastery_bit = (
        f" Estimated Knowledge {float(mastery):.0f}%."
        if isinstance(mastery, int | float)
        else ""
    )
    return InsightField(
        field_id="strongest_area",
        title="Strongest area",
        message=f"Your strongest area is {name}.{mastery_bit} {reason}".strip(),
        topic_id=_topic_id(area),
        source="readiness_intelligence.strongest_areas",
    )


def _risk_field(inputs: StudyInsightInputs) -> InsightField | None:
    if not inputs.weakest_areas:
        return None
    area = inputs.weakest_areas[0]
    name = _topic_name(area) or "a syllabus topic"
    reason = _reason(area) or "Lowest Estimated Knowledge among observed topics."
    mastery = area.get("mastery_score")
    mastery_bit = (
        f" Estimated Knowledge {float(mastery):.0f}%."
        if isinstance(mastery, int | float)
        else ""
    )
    return InsightField(
        field_id="greatest_risk",
        title="Greatest risk",
        message=(
            f"Your greatest risk is {name}.{mastery_bit} {reason}"
        ).strip(),
        topic_id=_topic_id(area),
        source="readiness_intelligence.weakest_areas",
    )


def _next_action_field(inputs: StudyInsightInputs) -> InsightField | None:
    if inputs.recommended_next_actions:
        action = inputs.recommended_next_actions[0]
        title = str(action.get("title") or "").strip() or "Continue today's plan"
        reason = _reason(action) or "Grounded in readiness and planner outputs."
        return InsightField(
            field_id="recommended_next_action",
            title="Recommended next action",
            message=f"{title}. {reason}",
            topic_id=_topic_id(action),
            source="readiness_intelligence.recommended_next_actions",
        )
    if inputs.planner_missions:
        mission = inputs.planner_missions[0]
        name = _topic_name(mission) or str(mission.get("slot") or "today's mission")
        reason = _reason(mission) or "Planner mission slot for today."
        return InsightField(
            field_id="recommended_next_action",
            title="Recommended next action",
            message=f"Start your planned work on {name}. {reason}",
            topic_id=_topic_id(mission),
            source="adaptive_study_planner.today_missions",
        )
    return None


def _workload_field(inputs: StudyInsightInputs) -> InsightField | None:
    workload = inputs.recommended_workload
    if not workload:
        return None
    recommended = workload.get("recommended_minutes")
    available = workload.get("available_study_minutes")
    rationale = str(workload.get("rationale") or "").strip()
    parts: list[str] = []
    if isinstance(recommended, int | float):
        parts.append(
            f"Recommended study load today is {int(recommended)} minutes"
        )
        if isinstance(available, int | float):
            parts.append(f"(available capacity {int(available)} minutes)")
        parts[-1] = parts[-1] + "."
    if rationale:
        parts.append(rationale)
    if not parts:
        return None
    return InsightField(
        field_id="workload_explanation",
        title="Workload explanation",
        message=" ".join(parts),
        topic_id=None,
        source="adaptive_study_planner.recommended_workload",
    )


def _readiness_field(inputs: StudyInsightInputs) -> InsightField | None:
    if inputs.readiness_score is None and not inputs.confidence_level:
        return None
    parts: list[str] = []
    if inputs.readiness_score is not None:
        parts.append(f"Estimated readiness is {inputs.readiness_score:.0f}%")
    if inputs.confidence_level:
        confidence = inputs.confidence_level.replace("_", " ")
        parts.append(f"confidence in this estimate is {confidence}")
    message = ". ".join(parts)
    if message and not message.endswith("."):
        message += "."
    driver_bits: list[str] = []
    for driver in inputs.readiness_drivers[:2]:
        label = str(driver.get("label") or "").strip()
        rationale = str(driver.get("rationale") or "").strip()
        if label and rationale:
            driver_bits.append(f"{label}: {rationale}")
        elif label:
            driver_bits.append(label)
    if driver_bits:
        message = f"{message} Drivers — {'; '.join(driver_bits)}"
    source = (
        "readiness_intelligence"
        if inputs.readiness_available
        else "canonical.study_state.readiness_overall"
    )
    return InsightField(
        field_id="readiness_explanation",
        title="Readiness explanation",
        message=message.strip(),
        topic_id=None,
        source=source,
    )


def _progress_field(inputs: StudyInsightInputs) -> InsightField | None:
    bits: list[str] = []
    if inputs.lifecycle_stage:
        bits.append(f"You are in the {inputs.lifecycle_stage} stage")
    if inputs.current_streak is not None and inputs.current_streak > 0:
        bits.append(f"on a {inputs.current_streak}-day study streak")
    elif inputs.longest_streak is not None and inputs.longest_streak > 0:
        bits.append(
            f"with a longest study streak of {inputs.longest_streak} days so far"
        )
    if inputs.mission_completed_count > 0:
        bits.append(
            f"having completed {inputs.mission_completed_count} recorded mission(s)"
        )
    if (
        inputs.topics_started is not None
        and inputs.total_topics is not None
        and inputs.total_topics > 0
    ):
        bits.append(
            f"with {inputs.topics_started} of {inputs.total_topics} "
            "syllabus topics started"
        )
    if inputs.consistency_label:
        bits.append(f"study consistency looks {inputs.consistency_label}")
    if not bits:
        if inputs.evidence_attempt_count <= 0:
            return InsightField(
                field_id="motivational_progress_summary",
                title="Progress summary",
                message=(
                    "Progress insights will appear once study activity is recorded. "
                    "Open today's plan when you are ready to begin."
                ),
                topic_id=None,
                source="canonical_learner_state",
            )
        return None

    # Compose a readable sentence from observational CLS facts only.
    if len(bits) == 1:
        message = f"{bits[0]}."
    elif len(bits) == 2:
        message = f"{bits[0]}, {bits[1]}."
    else:
        message = f"{bits[0]}, {', '.join(bits[1:-1])}, and {bits[-1]}."
    # Capitalise first character without changing domain labels mid-sentence.
    message = message[0].upper() + message[1:]
    return InsightField(
        field_id="motivational_progress_summary",
        title="Progress summary",
        message=message,
        topic_id=None,
        source="canonical_learner_state",
    )


class StudyInsightAssembler:
    """Assembles StudyInsightGuidance from projected insight inputs."""

    def assemble(self, inputs: StudyInsightInputs) -> StudyInsightGuidance:
        if inputs.availability != AVAILABILITY_AVAILABLE:
            return StudyInsightGuidance(
                student_id=inputs.student_id,
                as_of=inputs.as_of,
                consumer_version=INSIGHT_LAYER_VERSION,
                foundation_version=inputs.foundation_version,
                twin_id=inputs.twin_id,
                availability=AVAILABILITY_UNAVAILABLE,
                unavailable_reason=inputs.unavailable_reason,
                todays_key_focus=None,
                strongest_area=None,
                greatest_risk=None,
                recommended_next_action=None,
                workload_explanation=None,
                readiness_explanation=None,
                motivational_progress_summary=None,
                provenance_refs=inputs.provenance_refs,
                limitations_codes=inputs.limitations_codes,
                explainability={
                    "role": "communication",
                    "calculates_intelligence": False,
                },
            )

        focus = _focus_field(inputs)
        strongest = _strongest_field(inputs)
        risk = _risk_field(inputs)
        next_action = _next_action_field(inputs)
        workload = _workload_field(inputs)
        readiness = _readiness_field(inputs)
        progress = _progress_field(inputs)

        limitations = list(inputs.limitations_codes)
        if focus is None:
            limitations.append("todays_key_focus_unavailable")
        if strongest is None:
            limitations.append("strongest_area_unavailable")
        if risk is None:
            limitations.append("greatest_risk_unavailable")
        if next_action is None:
            limitations.append("recommended_next_action_unavailable")
        if workload is None:
            limitations.append("workload_explanation_unavailable")
        if readiness is None:
            limitations.append("readiness_explanation_unavailable")

        return StudyInsightGuidance(
            student_id=inputs.student_id,
            as_of=inputs.as_of,
            consumer_version=INSIGHT_LAYER_VERSION,
            foundation_version=inputs.foundation_version,
            twin_id=inputs.twin_id,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            todays_key_focus=focus,
            strongest_area=strongest,
            greatest_risk=risk,
            recommended_next_action=next_action,
            workload_explanation=workload,
            readiness_explanation=readiness,
            motivational_progress_summary=progress,
            provenance_refs=inputs.provenance_refs,
            limitations_codes=tuple(dict.fromkeys(limitations)),
            explainability={
                "role": "communication",
                "calculates_intelligence": False,
                "planner_available": inputs.planner_available,
                "readiness_available": inputs.readiness_available,
                "composition_rules": {
                    "todays_key_focus": (
                        "planner.missions|planner.revision|readiness.next_action"
                    ),
                    "strongest_area": "readiness.strongest_areas",
                    "greatest_risk": "readiness.weakest_areas",
                    "recommended_next_action": (
                        "readiness.next_action|planner.missions"
                    ),
                    "workload_explanation": "planner.recommended_workload",
                    "readiness_explanation": (
                        "readiness.score+confidence+drivers"
                    ),
                    "motivational_progress_summary": (
                        "canonical streaks/missions/lifecycle"
                    ),
                },
            },
        )


def build_study_insight_assembler() -> StudyInsightAssembler:
    return StudyInsightAssembler()


__all__ = [
    "StudyInsightAssembler",
    "build_study_insight_assembler",
]

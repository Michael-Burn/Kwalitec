"""Sitting Report — student-facing projection of a completed Session (KWP-005).

Presentation only. Consumes opaque completion / evidence package facts already
produced by LearningSessionRuntime + Evidence Authority. Never recomputes
evidence grades, Progress, Twin estimates, or mission selection.

KWP-007: projects Learning Strategy Engine recommendations + WHY.
KWP-008: projects Learning Diagnostics Engine cause guidance (no labels).
KWP-009: projects Learning Difficulty Engine pacing / load guidance (no bands).
KWP-010: projects Intervention Effectiveness natural feedback (no verdict labels).
KWP-011: prefers frozen Educational Memory snapshots when present — never
rebuilds historical advice with current rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.application.intervention_effectiveness import (
    InterventionEffectivenessReport,
    get_intervention_effectiveness_engine,
)
from app.application.learning_diagnostics import (
    LearningDiagnosticsReport,
    get_learning_diagnostics_engine,
)
from app.application.learning_difficulty import (
    DifficultyProfile,
    get_learning_difficulty_engine,
)
from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.learning_strategy import (
    LearningStrategyAdvice,
    get_learning_strategy_engine,
)

_FORBIDDEN_FRAGMENTS: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "educational+",
    "educational +",
    "evidence package",
    "mission engine",
    "cognitive load",
    "mental load",
    "burnout",
    "overloaded",
    "very demanding",
    "load points",
    "recommendation effective",
    "recommendation partially effective",
    "recommendation ineffective",
    "insufficient evidence",
)

_PRACTICE_CORRECT = RuntimeEvidenceType.PRACTICE_CORRECT.value
_PRACTICE_INCORRECT = RuntimeEvidenceType.PRACTICE_INCORRECT.value
_PRACTICE_ATTEMPTED = RuntimeEvidenceType.PRACTICE_ATTEMPTED.value
_PRACTICE_PARTIAL = RuntimeEvidenceType.PRACTICE_PARTIAL_UNSCORED.value
_STRUCTURED = RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS.value
_REFLECTION = RuntimeEvidenceType.REFLECTION_SUBMITTED.value
_READING_DONE = RuntimeEvidenceType.READING_COMPLETED.value
_EXAMPLE_DONE = RuntimeEvidenceType.WORKED_EXAMPLE_COMPLETED.value


@dataclass(frozen=True)
class SittingReportViewModel:
    """Premium Sitting Report for the Session Complete surface."""

    headline: str = ""
    what_studied: str = ""
    learning_objectives: tuple[str, ...] = ()
    exercises_assigned: tuple[str, ...] = ()
    exercises_completed: tuple[str, ...] = ()
    practice_correct: int = 0
    practice_incorrect: int = 0
    practice_attempted: int = 0
    performance_summary: str = ""
    learning_insights: tuple[str, ...] = ()
    strengthened: tuple[str, ...] = ()
    needs_reinforcement: tuple[str, ...] = ()
    syllabus_refs: tuple[str, ...] = ()
    progress_explanation: str = ""
    tomorrow_preview: str = ""
    finish_outcome_label: str = ""
    assessment_mode_active: bool = False
    assessment_summary: str = ""
    has_report: bool = False
    # KWP-007 — Learning Strategy (student-safe; no calibration labels).
    strategy_title: str = ""
    strategy_body: str = ""
    strategy_explanation: str = ""
    strategy_spacing_guidance: str = ""
    strategy_momentum_guidance: str = ""
    strategy_confidence_guidance: str = ""
    # KWP-008 — Learning Diagnostics (guidance only; never category labels).
    diagnostic_guidance: str = ""
    diagnostic_explanation: str = ""
    # KWP-009 — Learning Difficulty / load (guidance only; never band labels).
    difficulty_title: str = ""
    difficulty_guidance: str = ""
    difficulty_explanation: str = ""
    # KWP-010 — Intervention Effectiveness (natural feedback; never verdict labels).
    effectiveness_feedback: str = ""
    effectiveness_explanation: str = ""
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


def build_sitting_report(
    *,
    topic_title: str = "",
    opaque_summary: dict[str, Any] | None = None,
    metadata: dict[str, str] | None = None,
    next_recommendation: str = "",
    twin_insights: dict[str, Any] | None = None,
    twin_signals: dict[str, Any] | None = None,
    cadence: dict[str, Any] | None = None,
) -> SittingReportViewModel:
    """Project a student-safe Sitting Report from opaque Session facts."""
    opaque = dict(opaque_summary or {})
    meta = dict(metadata or {})
    topic = (
        str(topic_title or opaque.get("topic_title") or "").strip()
        or "today's topic"
    )
    if topic_title and not opaque.get("topic_title"):
        opaque["topic_title"] = topic
    if next_recommendation and not opaque.get("next_recommendation"):
        opaque["next_recommendation"] = next_recommendation
    objectives = _string_tuple(
        opaque.get("learning_objectives") or opaque.get("objectives")
    )
    assigned, completed, syllabus_refs = _exercise_lists(opaque)
    counts = _practice_counts(opaque)
    finish_label = _finish_label(opaque, meta)
    progress_advanced = _truthy(meta.get("progress_advanced")) or bool(
        opaque.get("progress_advanced")
    )
    mission_completed = _truthy(meta.get("mission_completed")) or bool(
        opaque.get("mission_completed")
    )
    disposition = str(
        meta.get("evidence_disposition") or opaque.get("evidence_disposition") or ""
    ).strip().lower()

    progress_explanation = _progress_explanation(
        topic=topic,
        progress_advanced=progress_advanced,
        mission_completed=mission_completed,
        finish_label=finish_label,
        disposition=disposition,
        correct=counts["correct"],
        incorrect=counts["incorrect"],
    )
    insights = _learning_insights(
        topic=topic,
        objectives=objectives,
        counts=counts,
        opaque=opaque,
        twin_insights=twin_insights or {},
        finish_label=finish_label,
    )
    strengthened = _strengthened(topic=topic, counts=counts, objectives=objectives)
    needs = _needs_reinforcement(
        topic=topic, counts=counts, objectives=objectives, opaque=opaque
    )
    performance = _performance_summary(counts)
    has_scored = counts["correct"] + counts["incorrect"] > 0
    assessment_summary = ""
    if has_scored:
        total = counts["correct"] + counts["incorrect"]
        assessment_summary = (
            f"You answered {counts['correct']} of {total} scored practice "
            f"questions correctly on {topic}."
        )
    elif counts["attempted"]:
        assessment_summary = (
            f"You attempted {counts['attempted']} practice items on {topic}. "
            "Scored results will appear when practice includes checkable answers."
        )

    twin_enrichment = twin_signals or twin_insights or {}
    # KWP-011 — prefer frozen Sitting Report fields when present.
    # Never rebuild historical advice with current rules.
    frozen = _frozen_intelligence(opaque=opaque, metadata=meta)
    if frozen is not None:
        strategy_title = frozen.get("strategy_title", "")
        strategy_body = frozen.get("strategy_body", "")
        strategy_explanation = frozen.get("strategy_explanation", "")
        strategy_spacing = frozen.get("strategy_spacing_guidance", "")
        strategy_momentum = frozen.get("strategy_momentum_guidance", "")
        strategy_confidence = frozen.get("strategy_confidence_guidance", "")
        diagnostic_guidance = frozen.get("diagnostic_guidance", "")
        diagnostic_explanation = frozen.get("diagnostic_explanation", "")
        difficulty_title = frozen.get("difficulty_title", "")
        difficulty_guidance = frozen.get("difficulty_guidance", "")
        difficulty_explanation = frozen.get("difficulty_explanation", "")
        effectiveness_feedback = frozen.get("effectiveness_feedback", "")
        effectiveness_explanation = frozen.get("effectiveness_explanation", "")
        tomorrow = _tomorrow_preview(
            next_recommendation=(
                next_recommendation
                or str(opaque.get("next_recommendation") or "")
            ),
            needs=needs,
            progress_advanced=progress_advanced,
            topic=topic,
            strategy=None,
            strategy_title=strategy_title,
            opaque=opaque,
            metadata=meta,
        )
        what_studied = _what_studied(topic, objectives, opaque)
        headline = f"Sitting Report · {topic}"
        if strategy_explanation and strategy_explanation not in insights:
            insights = tuple(list(insights[:4]) + [strategy_explanation])[:5]
        return SittingReportViewModel(
            headline=_safe(headline),
            what_studied=_safe(what_studied),
            learning_objectives=tuple(_safe(o) for o in objectives[:6]),
            exercises_assigned=tuple(_safe(e) for e in assigned[:8]),
            exercises_completed=tuple(_safe(e) for e in completed[:8]),
            practice_correct=counts["correct"],
            practice_incorrect=counts["incorrect"],
            practice_attempted=counts["attempted"],
            performance_summary=_safe(performance),
            learning_insights=tuple(_safe(i) for i in insights[:5]),
            strengthened=tuple(_safe(s) for s in strengthened[:4]),
            needs_reinforcement=tuple(_safe(n) for n in needs[:4]),
            syllabus_refs=tuple(_safe(r) for r in syllabus_refs[:6]),
            progress_explanation=_safe(progress_explanation),
            tomorrow_preview=_safe(tomorrow),
            finish_outcome_label=_safe(finish_label),
            assessment_mode_active=has_scored or bool(assigned),
            assessment_summary=_safe(assessment_summary),
            has_report=True,
            strategy_title=_safe(strategy_title),
            strategy_body=_safe(strategy_body),
            strategy_explanation=_safe(strategy_explanation),
            strategy_spacing_guidance=_safe(strategy_spacing),
            strategy_momentum_guidance=_safe(strategy_momentum),
            strategy_confidence_guidance=_safe(strategy_confidence),
            diagnostic_guidance=_safe(diagnostic_guidance),
            diagnostic_explanation=_safe(diagnostic_explanation),
            difficulty_title=_safe(difficulty_title),
            difficulty_guidance=_safe(difficulty_guidance),
            difficulty_explanation=_safe(difficulty_explanation),
            effectiveness_feedback=_safe(effectiveness_feedback),
            effectiveness_explanation=_safe(effectiveness_explanation),
        )

    strategy = _learning_strategy(
        opaque=opaque,
        metadata=meta,
        twin_signals=twin_enrichment,
        cadence=cadence,
        next_recommendation=next_recommendation,
    )
    diagnostics = _learning_diagnostics(
        opaque=opaque,
        metadata=meta,
        twin_signals=twin_enrichment,
        cadence=cadence,
    )
    difficulty = _learning_difficulty(
        opaque=opaque,
        metadata=meta,
        twin_signals=twin_enrichment,
        cadence=cadence,
    )
    effectiveness = _intervention_effectiveness(
        opaque=opaque,
        metadata=meta,
        twin_signals=twin_enrichment,
        cadence=cadence,
    )
    # Prefer cause-level WHY when diagnostics have a concrete signal.
    composed_why = _compose_why(strategy=strategy, diagnostics=diagnostics)
    tomorrow = _tomorrow_preview(
        next_recommendation=(
            next_recommendation
            or str(opaque.get("next_recommendation") or "")
        ),
        needs=needs,
        progress_advanced=progress_advanced,
        topic=topic,
        strategy=strategy,
        opaque=opaque,
        metadata=meta,
    )
    what_studied = _what_studied(topic, objectives, opaque)
    headline = f"Sitting Report · {topic}"
    if composed_why and composed_why not in insights:
        insights = tuple(list(insights[:4]) + [composed_why])[:5]
    elif strategy.explanation and strategy.explanation not in insights:
        insights = tuple(list(insights[:4]) + [strategy.explanation])[:5]

    report = SittingReportViewModel(
        headline=_safe(headline),
        what_studied=_safe(what_studied),
        learning_objectives=tuple(_safe(o) for o in objectives[:6]),
        exercises_assigned=tuple(_safe(e) for e in assigned[:8]),
        exercises_completed=tuple(_safe(e) for e in completed[:8]),
        practice_correct=counts["correct"],
        practice_incorrect=counts["incorrect"],
        practice_attempted=counts["attempted"],
        performance_summary=_safe(performance),
        learning_insights=tuple(_safe(i) for i in insights[:5]),
        strengthened=tuple(_safe(s) for s in strengthened[:4]),
        needs_reinforcement=tuple(_safe(n) for n in needs[:4]),
        syllabus_refs=tuple(_safe(r) for r in syllabus_refs[:6]),
        progress_explanation=_safe(progress_explanation),
        tomorrow_preview=_safe(tomorrow),
        finish_outcome_label=_safe(finish_label),
        assessment_mode_active=has_scored or bool(assigned),
        assessment_summary=_safe(assessment_summary),
        has_report=True,
        strategy_title=_safe(strategy.recommendation_title),
        strategy_body=_safe(strategy.recommendation_body),
        strategy_explanation=_safe(composed_why or strategy.explanation),
        strategy_spacing_guidance=_safe(strategy.spacing_guidance),
        strategy_momentum_guidance=_safe(strategy.momentum_guidance),
        strategy_confidence_guidance=_safe(strategy.confidence_guidance),
        diagnostic_guidance=_safe(diagnostics.guidance),
        diagnostic_explanation=_safe(diagnostics.explanation),
        difficulty_title=_safe(difficulty.recommendation_title),
        difficulty_guidance=_safe(difficulty.guidance),
        difficulty_explanation=_safe(difficulty.explanation),
        effectiveness_feedback=_safe(
            effectiveness.feedback if effectiveness.has_student_feedback else ""
        ),
        effectiveness_explanation=_safe(
            effectiveness.explanation
            if effectiveness.has_student_feedback
            else ""
        ),
    )
    return report


def _learning_strategy(
    *,
    opaque: dict[str, Any],
    metadata: dict[str, Any],
    twin_signals: dict[str, Any],
    cadence: dict[str, Any] | None,
    next_recommendation: str,
) -> LearningStrategyAdvice:
    return get_learning_strategy_engine().evaluate_opaque(
        opaque,
        metadata=metadata,
        twin_signals=twin_signals,
        cadence=cadence,
        next_recommendation=next_recommendation,
    )


def _learning_diagnostics(
    *,
    opaque: dict[str, Any],
    metadata: dict[str, Any],
    twin_signals: dict[str, Any],
    cadence: dict[str, Any] | None,
) -> LearningDiagnosticsReport:
    return get_learning_diagnostics_engine().evaluate_opaque(
        opaque,
        metadata=metadata,
        twin_signals=twin_signals,
        cadence=cadence,
    )


def _learning_difficulty(
    *,
    opaque: dict[str, Any],
    metadata: dict[str, Any],
    twin_signals: dict[str, Any],
    cadence: dict[str, Any] | None,
) -> DifficultyProfile:
    return get_learning_difficulty_engine().evaluate_opaque(
        opaque,
        metadata=metadata,
        twin_signals=twin_signals,
        cadence=cadence,
    )


def _intervention_effectiveness(
    *,
    opaque: dict[str, Any],
    metadata: dict[str, Any],
    twin_signals: dict[str, Any],
    cadence: dict[str, Any] | None,
) -> InterventionEffectivenessReport:
    return get_intervention_effectiveness_engine().evaluate_opaque(
        opaque,
        metadata=metadata,
        twin_signals=twin_signals,
        cadence=cadence,
    )


def _compose_why(
    *,
    strategy: LearningStrategyAdvice,
    diagnostics: LearningDiagnosticsReport,
) -> str:
    """Compose strategy WHAT with diagnostic cause WHY when available.

    Insufficient-signal diagnostics fall back to the strategy explanation.
    """
    from app.application.learning_diagnostics.dto import DiagnosticCategory

    if diagnostics.primary.category is DiagnosticCategory.INSUFFICIENT_SIGNAL:
        return strategy.explanation
    cause = (diagnostics.explanation or "").strip()
    if not cause:
        return strategy.explanation
    # Prefer cause-level WHY; strategy body already carries WHAT.
    return cause


def insights_from_sitting_report(report: SittingReportViewModel) -> tuple[str, ...]:
    """Prefer Sitting Report insights for Learning Insights chrome."""
    if report.learning_insights:
        return report.learning_insights
    lines: list[str] = []
    if report.strategy_explanation:
        lines.append(report.strategy_explanation)
    if report.performance_summary:
        lines.append(report.performance_summary)
    if report.progress_explanation:
        lines.append(report.progress_explanation)
    if report.tomorrow_preview:
        lines.append(report.tomorrow_preview)
    return tuple(lines[:5])


def _what_studied(
    topic: str, objectives: tuple[str, ...], opaque: dict[str, Any]
) -> str:
    stages: list[str] = []
    type_ids = _type_ids(opaque)
    if _READING_DONE in type_ids:
        stages.append("reading")
    if _EXAMPLE_DONE in type_ids:
        stages.append("worked examples")
    if any(
        t in type_ids
        for t in (
            _PRACTICE_CORRECT,
            _PRACTICE_INCORRECT,
            _PRACTICE_ATTEMPTED,
            _PRACTICE_PARTIAL,
            _STRUCTURED,
        )
    ):
        stages.append("practice")
    if _REFLECTION in type_ids:
        stages.append("reflection")
    if not stages and opaque.get("substance") == "package":
        stages = ["reading", "practice", "reflection"]
    stage_text = ", ".join(stages) if stages else "today's study flow"
    if objectives:
        lead = objectives[0]
        return f"You studied {topic} — focusing on {lead} — through {stage_text}."
    return f"You studied {topic} through {stage_text}."


def _exercise_lists(
    opaque: dict[str, Any],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    activities = opaque.get("activities") or opaque.get("activity_items") or ()
    assigned: list[str] = []
    completed: list[str] = []
    refs: list[str] = []
    if isinstance(activities, list | tuple):
        for raw in activities:
            if not isinstance(raw, dict):
                continue
            stage = str(raw.get("stage") or raw.get("activity_type") or "").lower()
            title = str(raw.get("title") or raw.get("label") or "").strip()
            if stage and stage not in {"practice", "question", "assessment"}:
                # Still list practice-like titles; skip pure reading labels when named.
                if stage in {
                    "reading", "read", "worked_example", "example", "reflection"
                }:
                    label = title or stage.replace("_", " ").title()
                    assigned.append(label)
                    done = (
                        raw.get("completed")
                        or raw.get("done")
                        or raw.get("status") == "completed"
                    )
                    if done:
                        completed.append(label)
                    for ref in raw.get("syllabus_refs") or ():
                        text = str(ref).strip()
                        if text and text not in refs:
                            refs.append(text)
                    continue
            label = title or "Practice exercise"
            if stage == "practice" or "practice" in label.lower() or not stage:
                assigned.append(label)
                done = (
                    raw.get("completed")
                    or raw.get("done")
                    or raw.get("status") == "completed"
                )
                if done:
                    completed.append(label)
            for ref in raw.get("syllabus_refs") or ():
                text = str(ref).strip()
                if text and text not in refs:
                    refs.append(text)
    # Fallback: opaque practice labels
    for key in ("exercises_assigned", "practice_labels"):
        for item in opaque.get(key) or ():
            text = str(item).strip()
            if text and text not in assigned:
                assigned.append(text)
    for item in opaque.get("exercises_completed") or ():
        text = str(item).strip()
        if text and text not in completed:
            completed.append(text)
    for ref in opaque.get("syllabus_refs") or ():
        text = str(ref).strip()
        if text and text not in refs:
            refs.append(text)
    return tuple(assigned), tuple(completed), tuple(refs)


def _practice_counts(opaque: dict[str, Any]) -> dict[str, int]:
    if opaque.get("practice_correct") is not None or opaque.get(
        "practice_incorrect"
    ) is not None:
        correct = int(opaque.get("practice_correct") or 0)
        incorrect = int(opaque.get("practice_incorrect") or 0)
        attempted = int(
            opaque.get("practice_attempted")
            or (correct + incorrect + int(opaque.get("practice_unscored") or 0))
        )
        return {
            "correct": max(0, correct),
            "incorrect": max(0, incorrect),
            "attempted": max(0, attempted),
            "unscored": int(opaque.get("practice_unscored") or 0),
        }
    correct = 0
    incorrect = 0
    attempted = 0
    unscored = 0
    for obs in opaque.get("observations") or ():
        if not isinstance(obs, dict):
            continue
        tid = str(obs.get("type_id") or "")
        payload = obs.get("payload") or {}
        if tid == _PRACTICE_CORRECT:
            correct += 1
            attempted += 1
        elif tid == _PRACTICE_INCORRECT:
            incorrect += 1
            attempted += 1
        elif tid == _STRUCTURED:
            attempted += 1
            if payload.get("scored_correct") is True or payload.get("correct") is True:
                correct += 1
            elif (
                payload.get("scored_correct") is False
                or payload.get("correct") is False
            ):
                incorrect += 1
        elif tid in {_PRACTICE_ATTEMPTED, _PRACTICE_PARTIAL}:
            attempted += 1
            unscored += 1
    return {
        "correct": correct,
        "incorrect": incorrect,
        "attempted": attempted,
        "unscored": unscored,
    }


def _type_ids(opaque: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for obs in opaque.get("observations") or ():
        if isinstance(obs, dict) and obs.get("type_id"):
            ids.append(str(obs["type_id"]))
    for tid in opaque.get("observation_type_ids") or ():
        ids.append(str(tid))
    return ids


def _finish_label(opaque: dict[str, Any], meta: dict[str, str]) -> str:
    review = opaque.get("finish_review")
    if isinstance(review, dict):
        label = str(review.get("label") or "").strip()
        verdict = str(review.get("verdict") or "").strip().lower()
        if label:
            return label
        if verdict == "yes":
            return "You confirmed today's planned study was complete"
        if verdict == "partially":
            return "You marked today's study as partially complete"
        if verdict == "no":
            return "You marked today's planned study as not complete"
    raw = str(
        meta.get("finish_review_label") or meta.get("finish_review") or ""
    ).strip()
    if raw == "yes":
        return "You confirmed today's planned study was complete"
    if raw == "partially":
        return "You marked today's study as partially complete"
    if raw == "no":
        return "You marked today's planned study as not complete"
    return raw


def _progress_explanation(
    *,
    topic: str,
    progress_advanced: bool,
    mission_completed: bool,
    finish_label: str,
    disposition: str,
    correct: int,
    incorrect: int,
) -> str:
    if progress_advanced and mission_completed:
        if correct and not incorrect:
            return (
                f"Your Journey moved forward on {topic} because you finished "
                "honestly and answered practice correctly."
            )
        return (
            f"Your Journey moved forward on {topic} because today's Session "
            "was accepted as complete study."
        )
    if progress_advanced:
        return (
            f"Coverage for {topic} advanced from today's accepted practice."
        )
    if "partial" in finish_label.lower() or disposition == "accepted_with_restrictions":
        return (
            "Progress stayed where it was — honest finish reviews that are "
            "partial do not claim Journey movement."
        )
    if finish_label and "not complete" in finish_label.lower():
        return (
            "Progress stayed where it was — you recorded that planned study "
            "was not complete, so no Journey advance was claimed."
        )
    if disposition == "rejected":
        return (
            "Progress did not change — today's Session did not meet the bar "
            "for Journey movement. You can continue when ready."
        )
    if correct or incorrect:
        return (
            f"Practice on {topic} was recorded. Journey movement depends on "
            "an honest finish and accepted study for the day."
        )
    return (
        f"Today's Session on {topic} is closed. Journey updates appear when "
        "study is accepted as complete."
    )


def _learning_insights(
    *,
    topic: str,
    objectives: tuple[str, ...],
    counts: dict[str, int],
    opaque: dict[str, Any],
    twin_insights: dict[str, Any],
    finish_label: str,
) -> tuple[str, ...]:
    lines: list[str] = []
    lead = objectives[0] if objectives else topic
    if counts["correct"] and not counts["incorrect"]:
        lines.append(f"You consistently answered {lead} practice correctly.")
    elif counts["correct"] and counts["incorrect"]:
        lines.append(
            f"You got {counts['correct']} practice items right on {topic}, "
            f"and missed {counts['incorrect']} — worth a short revisit."
        )
    elif counts["incorrect"] and not counts["correct"]:
        lines.append(f"You struggled with {lead} practice today.")
    elif counts["unscored"] or counts["attempted"]:
        lines.append(
            f"You put practice time into {topic}. Checkable answers will "
            "sharpen what comes next."
        )
    if _REFLECTION in _type_ids(opaque):
        lines.append("You left a reflection — that helps shape tomorrow's Session.")
    recent = twin_insights.get("recent_insights") or twin_insights.get("insights") or ()
    if isinstance(recent, str) and recent.strip():
        lines.append(recent.strip())
    elif isinstance(recent, list | tuple):
        for item in recent:
            text = str(item).strip()
            if text and text not in lines:
                lines.append(text)
            if len(lines) >= 4:
                break
    if finish_label and "partial" in finish_label.lower():
        lines.append("Tomorrow's Session can pick up where you left off.")
    elif counts["incorrect"]:
        lines.append("Tomorrow's Session has been adjusted toward reinforcement.")
    # Drop hollow / technical placeholders from older runtime strings.
    filtered = [
        line
        for line in lines
        if line
        and "does not claim mastery" not in line.lower()
        and "session product complete" not in line.lower()
        and "educational substance arrives" not in line.lower()
    ]
    return tuple(filtered[:5])


def _strengthened(
    *, topic: str, counts: dict[str, int], objectives: tuple[str, ...]
) -> tuple[str, ...]:
    if counts["correct"] <= 0:
        return ()
    if objectives:
        if counts["correct"] >= counts["incorrect"]:
            return tuple(objectives[:2])
        return (objectives[0],)
    if counts["correct"] >= counts["incorrect"]:
        return (topic,)
    return ()


def _needs_reinforcement(
    *,
    topic: str,
    counts: dict[str, int],
    objectives: tuple[str, ...],
    opaque: dict[str, Any],
) -> tuple[str, ...]:
    needs: list[str] = []
    if counts["incorrect"] > 0:
        if len(objectives) > 1:
            needs.append(objectives[-1])
        elif objectives:
            needs.append(objectives[0])
        else:
            needs.append(topic)
    for item in opaque.get("needs_reinforcement") or ():
        text = str(item).strip()
        if text and text not in needs:
            needs.append(text)
    return tuple(needs[:4])


def _performance_summary(counts: dict[str, int]) -> str:
    scored = counts["correct"] + counts["incorrect"]
    if scored <= 0:
        if counts["attempted"]:
            return f"{counts['attempted']} practice attempts recorded."
        return "No scored practice in this Session yet."
    return (
        f"Practice results · {counts['correct']} correct, "
        f"{counts['incorrect']} to revisit."
    )


def _tomorrow_preview(
    *,
    next_recommendation: str,
    needs: tuple[str, ...],
    progress_advanced: bool,
    topic: str,
    strategy: LearningStrategyAdvice | None = None,
    strategy_title: str = "",
    educational_package_id: str = "",
    opaque: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    # RO1-R1 / EA-006: bind Finish chrome to the sitting's approved package
    # tomorrow_preview — never shared topic_code first-match alone.
    try:
        from app.application.educational_packages.tomorrow_chrome import (
            format_tomorrow_preview_text,
            resolve_package_for_tomorrow_chrome,
        )

        pack_id = (educational_package_id or "").strip()
        opaque_map = opaque or {}
        meta_map = metadata or {}
        if not pack_id:
            pack_id = str(
                opaque_map.get("educational_package_id")
                or meta_map.get("educational_package_id")
                or ""
            ).strip()
        pack = resolve_package_for_tomorrow_chrome(
            educational_package_id=pack_id,
            subject_id=str(
                opaque_map.get("subject_id")
                or opaque_map.get("subject_code")
                or meta_map.get("subject_id")
                or ""
            ),
            syllabus_topic_code=str(
                opaque_map.get("topic_code") or meta_map.get("topic_code") or ""
            ),
            topic_title=topic,
        )
        if pack is not None:
            text = format_tomorrow_preview_text(
                pack, next_recommendation=next_recommendation
            )
            if text:
                return text
    except Exception:  # noqa: BLE001 — sitting report must stay resilient
        pass
    if strategy is not None and strategy.recommendation_title:
        if next_recommendation and strategy.action.value == "advance_topic":
            return (
                f"{strategy.recommendation_title} · "
                f"Tomorrow's Session · {next_recommendation}"
            )
        if strategy.spacing_guidance:
            return (
                f"{strategy.recommendation_title} · {strategy.spacing_guidance}"
            )
        return (
            f"{strategy.recommendation_title} · {strategy.recommendation_body}"
        )
    if strategy_title:
        if next_recommendation:
            return f"{strategy_title} · Tomorrow's Session · {next_recommendation}"
        return f"{strategy_title} · continue {topic}."
    if next_recommendation:
        return f"Tomorrow's Session · {next_recommendation}"
    if needs:
        return (
            f"Tomorrow's Session will make space to reinforce {needs[0]}."
        )
    if progress_advanced:
        return "Tomorrow's Session continues to the next topic on your Journey."
    return f"Return tomorrow to continue {topic}."


def _frozen_intelligence(
    *,
    opaque: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, str] | None:
    """Return frozen Sitting Report fields when Educational Memory captured them.

    Prefers ``intelligence_snapshot.student_sitting_report``, then metadata
    pairs written at completion (``intelligence_captured=true``).
    """
    snap_raw = opaque.get("intelligence_snapshot")
    if isinstance(snap_raw, dict):
        report = snap_raw.get("student_sitting_report")
        if isinstance(report, dict) and (
            report.get("strategy_title")
            or report.get("diagnostic_guidance")
            or report.get("difficulty_guidance")
            or report.get("effectiveness_feedback")
        ):
            return {str(k): str(v or "") for k, v in report.items()}

    captured = str(metadata.get("intelligence_captured") or "").lower()
    if captured not in {"1", "true", "yes"}:
        # Also accept when strategy fields were flattened into metadata.
        if not metadata.get("strategy_title"):
            return None
    keys = (
        "strategy_title",
        "strategy_body",
        "strategy_explanation",
        "strategy_spacing_guidance",
        "strategy_momentum_guidance",
        "strategy_confidence_guidance",
        "diagnostic_guidance",
        "diagnostic_explanation",
        "difficulty_title",
        "difficulty_guidance",
        "difficulty_explanation",
        "effectiveness_feedback",
        "effectiveness_explanation",
    )
    frozen = {k: str(metadata.get(k) or "") for k in keys}
    if not any(frozen.values()):
        return None
    return frozen


def _string_tuple(raw: Any) -> tuple[str, ...]:
    if isinstance(raw, str):
        text = raw.strip()
        return (text,) if text else ()
    if isinstance(raw, list | tuple):
        return tuple(str(x).strip() for x in raw if str(x).strip())
    return ()


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def _safe(text: str) -> str:
    value = (text or "").strip()
    lowered = value.lower()
    if any(term in lowered for term in _FORBIDDEN_FRAGMENTS):
        return ""
    return value

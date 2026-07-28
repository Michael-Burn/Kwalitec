"""Educational Timeline narrative generation (ILE-003).

Pure interpretation of Decision Journal evidence into calm educational
narrative. No Twin, ranking, readiness prediction, or analytics scores.
Never claims certainty beyond available journal evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from app.domain.decision_journal.enums import (
    EntryKind,
    JournalLifecycleStatus,
    QualitativeConfidence,
    ReflectionStatus,
    StudentAction,
)
from app.domain.educational_timeline.enums import (
    SECTION_INTROS,
    SECTION_LABELS,
    NarrativeCertainty,
    TimelineSectionKind,
)


@dataclass(frozen=True)
class NarrativeMoment:
    """One Observation → Pattern → Meaning → Reflection unit."""

    observation: str
    pattern: str
    educational_meaning: str
    reflection_question: str
    certainty: NarrativeCertainty = NarrativeCertainty.SUGGESTIVE
    evidence_decision_ids: tuple[str, ...] = ()
    when_label: str = ""
    title: str = ""


@dataclass(frozen=True)
class TimelineSection:
    """One named timeline section with zero or more narrative moments."""

    kind: TimelineSectionKind
    label: str
    intro: str
    moments: tuple[NarrativeMoment, ...] = ()
    empty_note: str = ""


@dataclass(frozen=True)
class EducationalNarrative:
    """Full Educational Timeline derived from journal entries."""

    sections: tuple[TimelineSection, ...] = ()
    entry_count: int = 0
    certainty: NarrativeCertainty = NarrativeCertainty.INSUFFICIENT
    empty: bool = True


@dataclass
class _EvidenceEntry:
    """Normalised journal evidence for pattern detection."""

    decision_id: str
    recorded_at: datetime | None
    kind: str
    lifecycle_status: str
    educational_context: str
    observation: str
    meaning: str
    recommendation: str
    qualitative_confidence: str
    uncertainty: str
    student_action: str
    outcome_summary: str
    reflection_status: str
    reflection_note: str
    expected_benefit: str


def build_educational_narrative(
    entries: list[dict[str, Any]] | list[Any],
) -> EducationalNarrative:
    """Interpret journal entry payloads into a reflective timeline.

    Args:
        entries: Newest-first or oldest-first student dicts / ORM-like rows.
            Required keys match ``DecisionJournalService.to_student_dict``
            plus optional ``recorded_at`` datetime.

    Returns:
        EducationalNarrative with sections that have evidence-backed moments.
        Empty sections are omitted rather than inventing content.
    """
    evidence = [_normalise(e) for e in entries]
    evidence = [e for e in evidence if e.decision_id]
    if not evidence:
        return EducationalNarrative(empty=True, entry_count=0)

    chronological = sorted(
        evidence,
        key=lambda e: e.recorded_at or datetime.min,
    )
    certainty = _overall_certainty(chronological)

    builders = (
        _section_learning_journey,
        _section_turning_points,
        _section_recoveries,
        _section_consistency,
        _section_uncertainty,
        _section_mission_milestones,
        _section_reflection_highlights,
        _section_decision_milestones,
        _section_learning_momentum,
    )
    sections: list[TimelineSection] = []
    for builder in builders:
        section = builder(chronological, certainty)
        if section is not None and section.moments:
            sections.append(section)

    return EducationalNarrative(
        sections=tuple(sections),
        entry_count=len(chronological),
        certainty=certainty,
        empty=len(sections) == 0,
    )


def _normalise(raw: Any) -> _EvidenceEntry:
    if hasattr(raw, "entry_id") and not isinstance(raw, dict):
        return _EvidenceEntry(
            decision_id=str(getattr(raw, "entry_id", "") or ""),
            recorded_at=getattr(raw, "recorded_at", None),
            kind=str(getattr(raw, "kind", "") or ""),
            lifecycle_status=str(getattr(raw, "lifecycle_status", "") or ""),
            educational_context=str(
                getattr(raw, "educational_context", "") or ""
            ),
            observation=str(getattr(raw, "observation", "") or ""),
            meaning=str(getattr(raw, "meaning", "") or ""),
            recommendation=str(getattr(raw, "recommendation", "") or ""),
            qualitative_confidence=str(
                getattr(raw, "qualitative_confidence", "") or ""
            ),
            uncertainty=str(getattr(raw, "uncertainty", "") or ""),
            student_action=str(getattr(raw, "student_action", "") or ""),
            outcome_summary=str(getattr(raw, "outcome_summary", "") or ""),
            reflection_status=str(
                getattr(raw, "reflection_status", "") or ""
            ),
            reflection_note=str(getattr(raw, "reflection_note", "") or ""),
            expected_benefit=str(getattr(raw, "expected_benefit", "") or ""),
        )

    data = dict(raw) if not isinstance(raw, dict) else raw
    recorded = data.get("recorded_at")
    if recorded is None and data.get("timestamp"):
        try:
            recorded = datetime.fromisoformat(str(data["timestamp"]))
        except ValueError:
            recorded = None
    elif isinstance(recorded, str):
        try:
            recorded = datetime.fromisoformat(recorded)
        except ValueError:
            recorded = None

    return _EvidenceEntry(
        decision_id=str(
            data.get("decision_id") or data.get("entry_id") or ""
        ),
        recorded_at=recorded if isinstance(recorded, datetime) else None,
        kind=str(data.get("kind") or ""),
        lifecycle_status=str(data.get("lifecycle_status") or ""),
        educational_context=str(data.get("educational_context") or ""),
        observation=str(data.get("observation") or ""),
        meaning=str(data.get("meaning") or ""),
        recommendation=str(data.get("recommendation") or ""),
        qualitative_confidence=str(data.get("qualitative_confidence") or ""),
        uncertainty=str(data.get("uncertainty") or ""),
        student_action=str(data.get("student_action") or ""),
        outcome_summary=str(data.get("outcome_summary") or ""),
        reflection_status=str(data.get("reflection_status") or ""),
        reflection_note=str(data.get("reflection_note") or ""),
        expected_benefit=str(data.get("expected_benefit") or ""),
    )


def _overall_certainty(entries: list[_EvidenceEntry]) -> NarrativeCertainty:
    n = len(entries)
    if n < 2:
        return NarrativeCertainty.INSUFFICIENT
    if n < 4:
        return NarrativeCertainty.SUGGESTIVE
    return NarrativeCertainty.SUPPORTED


def _when(entry: _EvidenceEntry) -> str:
    if entry.recorded_at is None:
        return ""
    return entry.recorded_at.strftime("%d %b %Y")


def _hedge(certainty: NarrativeCertainty, strong: str, soft: str) -> str:
    if certainty == NarrativeCertainty.SUPPORTED:
        return strong
    return soft


def _moment(
    *,
    title: str,
    observation: str,
    pattern: str,
    educational_meaning: str,
    reflection_question: str,
    certainty: NarrativeCertainty,
    evidence: tuple[_EvidenceEntry, ...],
) -> NarrativeMoment:
    return NarrativeMoment(
        title=title,
        observation=observation.strip(),
        pattern=pattern.strip(),
        educational_meaning=educational_meaning.strip(),
        reflection_question=reflection_question.strip(),
        certainty=certainty,
        evidence_decision_ids=tuple(e.decision_id for e in evidence),
        when_label=_when(evidence[0]) if evidence else "",
    )


def _pack(
    kind: TimelineSectionKind,
    moments: list[NarrativeMoment],
    *,
    empty_note: str = "",
) -> TimelineSection | None:
    if not moments:
        return None
    return TimelineSection(
        kind=kind,
        label=SECTION_LABELS[kind],
        intro=SECTION_INTROS[kind],
        moments=tuple(moments),
        empty_note=empty_note,
    )


# ── Section builders ───────────────────────────────────────────────────────


def _section_learning_journey(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    moments: list[NarrativeMoment] = []
    # Cap journey beats so the page stays readable.
    sample = entries if len(entries) <= 8 else _journey_sample(entries)
    for entry in sample:
        obs = entry.observation or entry.recommendation or "Guidance was recorded."
        pattern = (
            f"Around this time, your journal recorded "
            f"{_kind_phrase(entry.kind)} with status "
            f"“{_lifecycle_phrase(entry.lifecycle_status)}”."
        )
        meaning = entry.meaning or (
            "This entry is part of the longer sequence of guidance "
            "you have received."
        )
        question = _journey_question(entry)
        moments.append(
            _moment(
                title=entry.recommendation
                or entry.educational_context
                or _kind_phrase(entry.kind).capitalize(),
                observation=obs,
                pattern=pattern,
                educational_meaning=meaning,
                reflection_question=question,
                certainty=certainty,
                evidence=(entry,),
            )
        )
    return _pack(TimelineSectionKind.LEARNING_JOURNEY, moments)


def _journey_sample(entries: list[_EvidenceEntry]) -> list[_EvidenceEntry]:
    """Keep first, last, and evenly spaced middle entries."""
    if len(entries) <= 8:
        return list(entries)
    indices = {0, len(entries) - 1}
    step = max(1, (len(entries) - 1) // 6)
    for i in range(0, len(entries), step):
        indices.add(i)
    return [entries[i] for i in sorted(indices)][:8]


def _journey_question(entry: _EvidenceEntry) -> str:
    if entry.student_action == StudentAction.ACCEPTED.value:
        return "What helped you act on this guidance?"
    if entry.student_action == StudentAction.DEFERRED.value:
        return "What would make similar guidance more useful next time?"
    if entry.outcome_summary:
        return "Looking back, what stands out from what followed?"
    return "What would you want to remember from this moment?"


def _section_turning_points(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    moments: list[NarrativeMoment] = []

    first_stable = next(
        (
            e
            for e in entries
            if e.qualitative_confidence
            in (
                QualitativeConfidence.RELIABLE.value,
                QualitativeConfidence.HIGH.value,
            )
            and e.student_action == StudentAction.ACCEPTED.value
        ),
        None,
    )
    if first_stable is not None:
        moments.append(
            _moment(
                title="First steadier understanding signal",
                observation=(
                    first_stable.observation
                    or "Guidance arrived with clearer supporting evidence."
                ),
                pattern=_hedge(
                    certainty,
                    "This appears to be the first journal entry where "
                    "confidence was described as reliable or high and you "
                    "accepted the guidance.",
                    "With the evidence available, this may be an early "
                    "moment when confidence looked steadier and you "
                    "accepted the guidance.",
                ),
                educational_meaning=(
                    first_stable.meaning
                    or "Steadier evidence can mark a turning point in how "
                    "guidance feels to follow."
                ),
                reflection_question=(
                    "What helped your understanding feel more stable here?"
                ),
                certainty=certainty,
                evidence=(first_stable,),
            )
        )

    first_recovery = next(
        (
            e
            for e in entries
            if e.kind == EntryKind.RECOVERY_RECOMMENDATION.value
            and e.student_action == StudentAction.ACCEPTED.value
        ),
        None,
    )
    if first_recovery is not None:
        moments.append(
            _moment(
                title="Successful recovery step",
                observation=(
                    first_recovery.observation
                    or "Recovery guidance was offered after a difficult stretch."
                ),
                pattern=(
                    "Your journal shows recovery guidance that you accepted — "
                    "a possible turning point toward rebuilding."
                ),
                educational_meaning=(
                    first_recovery.meaning
                    or "Choosing recovery work can reopen progress after "
                    "uncertainty or struggle."
                ),
                reflection_question=(
                    "Which part of that recovery approach felt useful?"
                ),
                certainty=certainty,
                evidence=(first_recovery,),
            )
        )

    first_milestone = next(
        (
            e
            for e in entries
            if e.kind == EntryKind.LEARNING_MILESTONE.value
            or (
                e.lifecycle_status
                == JournalLifecycleStatus.OUTCOME_RECORDED.value
                and e.kind == EntryKind.MISSION_RECOMMENDATION.value
            )
        ),
        None,
    )
    if first_milestone is not None:
        moments.append(
            _moment(
                title="Milestone in the journal",
                observation=(
                    first_milestone.observation
                    or first_milestone.recommendation
                    or "A learning milestone was recorded."
                ),
                pattern=(
                    "This entry marks a recorded milestone or completed "
                    "mission outcome in your educational memory."
                ),
                educational_meaning=(
                    first_milestone.meaning
                    or first_milestone.outcome_summary
                    or "Milestones help name progress without claiming "
                    "more than the journal supports."
                ),
                reflection_question=(
                    "What made this milestone feel significant?"
                ),
                certainty=certainty,
                evidence=(first_milestone,),
            )
        )

    uncertain = [
        e
        for e in entries
        if e.uncertainty.strip()
        or e.qualitative_confidence
        in (
            QualitativeConfidence.INSUFFICIENT.value,
            QualitativeConfidence.OBSERVATION_ONLY.value,
        )
    ]
    if len(uncertain) >= 3:
        sample = uncertain[:3]
        moments.append(
            _moment(
                title="Repeated uncertainty",
                observation=(
                    "Several journal entries note limited evidence or "
                    "open uncertainty."
                ),
                pattern=_hedge(
                    certainty,
                    f"Across {len(uncertain)} entries, uncertainty or "
                    "thin evidence appears repeatedly.",
                    f"At least {len(uncertain)} entries mention "
                    "uncertainty or limited evidence — a pattern worth "
                    "noticing, not a verdict.",
                ),
                educational_meaning=(
                    "Recurring uncertainty often means learning is still "
                    "forming — not that effort is wasted."
                ),
                reflection_question=(
                    "Where would you approach uncertainty differently?"
                ),
                certainty=certainty,
                evidence=tuple(sample),
            )
        )

    return _pack(TimelineSectionKind.TURNING_POINTS, moments)


def _section_recoveries(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    moments: list[NarrativeMoment] = []
    recoveries = [
        e
        for e in entries
        if e.kind == EntryKind.RECOVERY_RECOMMENDATION.value
        or (
            "recover" in (e.recommendation + e.observation + e.meaning).lower()
            and e.student_action == StudentAction.ACCEPTED.value
        )
    ]
    for entry in recoveries[:5]:
        moments.append(
            _moment(
                title=entry.recommendation
                or "Recovery guidance",
                observation=(
                    entry.observation
                    or "Recovery-oriented guidance appears in your journal."
                ),
                pattern=(
                    f"You {_action_phrase(entry.student_action)} this "
                    "recovery-related guidance"
                    + (
                        f"; afterwards: {entry.outcome_summary}"
                        if entry.outcome_summary
                        else "."
                    )
                ),
                educational_meaning=(
                    entry.meaning
                    or "Recovery work aims to rebuild a steadier base "
                    "before pushing further."
                ),
                reflection_question=(
                    "What helped your recent recovery, if anything?"
                ),
                certainty=certainty,
                evidence=(entry,),
            )
        )
    return _pack(TimelineSectionKind.RECOVERIES, moments)


def _section_consistency(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    accepted = [
        e
        for e in entries
        if e.student_action == StudentAction.ACCEPTED.value
        and e.recorded_at is not None
    ]
    streaks = _find_streaks(accepted, min_length=3, max_gap_days=3)
    moments: list[NarrativeMoment] = []
    for streak in streaks[:3]:
        first, last = streak[0], streak[-1]
        moments.append(
            _moment(
                title=(
                    f"Consistent stretch "
                    f"({_when(first)} – {_when(last)})"
                ),
                observation=(
                    f"Your journal shows {len(streak)} accepted guidance "
                    f"entries across a short period."
                ),
                pattern=_hedge(
                    certainty,
                    "Accepted guidance appears in a steady sequence — "
                    "a period of consistency in how you responded.",
                    "Accepted guidance appears close together; this may "
                    "suggest a more consistent study stretch.",
                ),
                educational_meaning=(
                    "Consistency in responding to guidance often supports "
                    "cumulative learning more than isolated effort."
                ),
                reflection_question=(
                    "Which habits supported this stretch of consistency?"
                ),
                certainty=certainty,
                evidence=tuple(streak[:3]),
            )
        )
    return _pack(TimelineSectionKind.PERIODS_OF_CONSISTENCY, moments)


def _section_uncertainty(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    uncertain = [
        e
        for e in entries
        if e.uncertainty.strip()
        or e.qualitative_confidence
        in (
            QualitativeConfidence.INSUFFICIENT.value,
            QualitativeConfidence.OBSERVATION_ONLY.value,
            QualitativeConfidence.EMERGING.value,
        )
    ]
    if not uncertain:
        return None
    # Cluster by week where possible
    moments: list[NarrativeMoment] = []
    sample = uncertain[:4]
    for entry in sample:
        moments.append(
            _moment(
                title=_when(entry) or "Open uncertainty",
                observation=(
                    entry.uncertainty
                    or entry.observation
                    or "Evidence for this guidance was still limited."
                ),
                pattern=(
                    "Confidence at the time was described as "
                    f"“{_confidence_phrase(entry.qualitative_confidence)}”."
                ),
                educational_meaning=(
                    entry.meaning
                    or "Naming uncertainty keeps guidance honest while "
                    "understanding is still forming."
                ),
                reflection_question=(
                    "What evidence would help reduce this uncertainty?"
                ),
                certainty=NarrativeCertainty.SUGGESTIVE
                if certainty == NarrativeCertainty.INSUFFICIENT
                else certainty,
                evidence=(entry,),
            )
        )
    return _pack(TimelineSectionKind.PERIODS_OF_UNCERTAINTY, moments)


def _section_mission_milestones(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    missions = [
        e
        for e in entries
        if e.kind == EntryKind.MISSION_RECOMMENDATION.value
        and e.lifecycle_status
        in (
            JournalLifecycleStatus.ACCEPTED.value,
            JournalLifecycleStatus.OUTCOME_RECORDED.value,
            JournalLifecycleStatus.REFLECTED.value,
        )
    ]
    moments: list[NarrativeMoment] = []
    for entry in missions[:6]:
        moments.append(
            _moment(
                title=entry.recommendation
                or "Mission guidance",
                observation=(
                    entry.observation
                    or "Mission-related guidance was recorded."
                ),
                pattern=(
                    f"Mission tip marked as "
                    f"“{_lifecycle_phrase(entry.lifecycle_status)}”"
                    + (
                        f"; outcome: {entry.outcome_summary}"
                        if entry.outcome_summary
                        else "."
                    )
                ),
                educational_meaning=(
                    entry.meaning
                    or entry.expected_benefit
                    or "Mission milestones mark concrete study steps "
                    "you chose to take."
                ),
                reflection_question=(
                    "Which strategy from this Mission proved effective?"
                ),
                certainty=certainty,
                evidence=(entry,),
            )
        )
    return _pack(TimelineSectionKind.MISSION_MILESTONES, moments)


def _section_reflection_highlights(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    reflected = [
        e
        for e in entries
        if e.reflection_status == ReflectionStatus.REFLECTED.value
        or e.lifecycle_status == JournalLifecycleStatus.REFLECTED.value
        or bool(e.reflection_note.strip())
    ]
    moments: list[NarrativeMoment] = []
    for entry in reflected[:6]:
        moments.append(
            _moment(
                title=entry.recommendation
                or "Reflection",
                observation=(
                    entry.observation
                    or "You closed a reflection loop on this guidance."
                ),
                pattern=(
                    entry.reflection_note
                    or "Reflection was recorded without a written note."
                ),
                educational_meaning=(
                    "Reflection turns a single decision into lasting "
                    "educational insight."
                ),
                reflection_question=(
                    "What would you carry forward from this reflection?"
                ),
                certainty=certainty,
                evidence=(entry,),
            )
        )
    return _pack(TimelineSectionKind.REFLECTION_HIGHLIGHTS, moments)


def _section_decision_milestones(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    decisions = [
        e
        for e in entries
        if e.student_action
        in (
            StudentAction.ACCEPTED.value,
            StudentAction.DEFERRED.value,
            StudentAction.DISMISSED.value,
        )
        and e.lifecycle_status
        in (
            JournalLifecycleStatus.ACCEPTED.value,
            JournalLifecycleStatus.DEFERRED.value,
            JournalLifecycleStatus.OUTCOME_RECORDED.value,
            JournalLifecycleStatus.REFLECTED.value,
            JournalLifecycleStatus.EVIDENCE_EVOLVING.value,
        )
    ]
    moments: list[NarrativeMoment] = []
    for entry in decisions[:6]:
        afterwards = (
            entry.outcome_summary
            or entry.reflection_note
            or "No later outcome is recorded yet."
        )
        moments.append(
            _moment(
                title=entry.recommendation
                or entry.educational_context
                or "Study decision",
                observation=(
                    f"You {_action_phrase(entry.student_action)}: "
                    f"{entry.recommendation or entry.observation}"
                ),
                pattern=(
                    f"Choice recorded as "
                    f"“{_lifecycle_phrase(entry.lifecycle_status)}”."
                ),
                educational_meaning=(
                    f"Afterwards: {afterwards}"
                ),
                reflection_question=(
                    "Would you make the same choice again, and why?"
                ),
                certainty=certainty,
                evidence=(entry,),
            )
        )
    return _pack(TimelineSectionKind.DECISION_MILESTONES, moments)


def _section_learning_momentum(
    entries: list[_EvidenceEntry],
    certainty: NarrativeCertainty,
) -> TimelineSection | None:
    dated = [e for e in entries if e.recorded_at is not None]
    if len(dated) < 2:
        return None

    latest = dated[-1].recorded_at
    assert latest is not None
    recent_cut = latest - timedelta(days=14)
    recent = [e for e in dated if e.recorded_at and e.recorded_at >= recent_cut]
    earlier = [e for e in dated if e.recorded_at and e.recorded_at < recent_cut]

    recent_accepted = sum(
        1
        for e in recent
        if e.student_action == StudentAction.ACCEPTED.value
    )
    earlier_accepted = sum(
        1
        for e in earlier
        if e.student_action == StudentAction.ACCEPTED.value
    )

    if not recent and not earlier:
        return None

    if recent_accepted > earlier_accepted and recent_accepted >= 2:
        pattern = _hedge(
            certainty,
            "Recent entries show more accepted guidance than the earlier "
            "window in this journal — a possible increase in learning "
            "momentum.",
            "Recent accepted guidance looks a little more frequent than "
            "earlier entries; treat this as a tentative reading only.",
        )
        meaning = (
            "Momentum here means rhythm of engagement with guidance, "
            "not a score of ability."
        )
        question = "What helped your recent improvement in follow-through?"
        title = "Possible recent momentum"
    elif earlier_accepted > recent_accepted and earlier_accepted >= 2:
        pattern = _hedge(
            certainty,
            "Earlier entries show more accepted guidance than the most "
            "recent fortnight — rhythm may have slowed.",
            "Accepted guidance appears less frequent recently than earlier; "
            "this may simply reflect fewer recorded tips.",
        )
        meaning = (
            "A quieter period in the journal is not a judgement — it is "
            "a chance to notice what changed."
        )
        question = "What would support a steadier rhythm again?"
        title = "Quieter recent rhythm"
    else:
        pattern = (
            "Accepted guidance appears at a similar pace across the "
            "available journal window."
        )
        meaning = (
            "Steady rhythm can matter as much as dramatic change."
        )
        question = "What keeps your study rhythm sustainable?"
        title = "Steady engagement with guidance"

    evidence = tuple((recent or earlier)[-3:])
    moment = _moment(
        title=title,
        observation=(
            f"Across {len(dated)} dated journal entries, "
            f"{recent_accepted} accepted recently"
            + (
                f" versus {earlier_accepted} earlier."
                if earlier
                else "."
            )
        ),
        pattern=pattern,
        educational_meaning=meaning,
        reflection_question=question,
        certainty=certainty
        if earlier
        else NarrativeCertainty.SUGGESTIVE,
        evidence=evidence,
    )
    return _pack(TimelineSectionKind.LEARNING_MOMENTUM, [moment])


# ── Helpers ────────────────────────────────────────────────────────────────


def _find_streaks(
    entries: list[_EvidenceEntry],
    *,
    min_length: int,
    max_gap_days: int,
) -> list[list[_EvidenceEntry]]:
    if len(entries) < min_length:
        return []
    streaks: list[list[_EvidenceEntry]] = []
    current: list[_EvidenceEntry] = [entries[0]]
    for entry in entries[1:]:
        prev = current[-1].recorded_at
        cur = entry.recorded_at
        if prev is None or cur is None:
            if len(current) >= min_length:
                streaks.append(current)
            current = [entry]
            continue
        gap = (cur.date() - prev.date()).days
        if 0 <= gap <= max_gap_days:
            current.append(entry)
        else:
            if len(current) >= min_length:
                streaks.append(current)
            current = [entry]
    if len(current) >= min_length:
        streaks.append(current)
    return streaks


def _kind_phrase(kind: str) -> str:
    mapping = {
        EntryKind.MISSION_RECOMMENDATION.value: "a Mission recommendation",
        EntryKind.QUICK_CHECK_RECOMMENDATION.value: "a Quick Check suggestion",
        EntryKind.REVISION_RECOMMENDATION.value: "revision guidance",
        EntryKind.RECOVERY_RECOMMENDATION.value: "recovery guidance",
        EntryKind.LEARNING_MILESTONE.value: "a learning milestone",
        EntryKind.EDUCATIONAL_REFLECTION.value: "an educational reflection",
    }
    return mapping.get(kind, "educational guidance")


def _lifecycle_phrase(status: str) -> str:
    mapping = {
        JournalLifecycleStatus.RECOMMENDED.value: "Recommended",
        JournalLifecycleStatus.ACCEPTED.value: "Accepted",
        JournalLifecycleStatus.DEFERRED.value: "Deferred",
        JournalLifecycleStatus.EVIDENCE_EVOLVING.value: "Evidence updated",
        JournalLifecycleStatus.REFLECTED.value: "Reflected",
        JournalLifecycleStatus.OUTCOME_RECORDED.value: "Outcome recorded",
        JournalLifecycleStatus.ARCHIVED.value: "Archived",
    }
    return mapping.get(status, status.replace("_", " "))


def _action_phrase(action: str) -> str:
    mapping = {
        StudentAction.ACCEPTED.value: "accepted",
        StudentAction.DEFERRED.value: "deferred",
        StudentAction.DISMISSED.value: "set aside",
        StudentAction.NONE_YET.value: "had not yet chosen on",
    }
    return mapping.get(action, "responded to")


def _confidence_phrase(band: str) -> str:
    mapping = {
        QualitativeConfidence.INSUFFICIENT.value: "Not enough evidence yet",
        QualitativeConfidence.OBSERVATION_ONLY.value: "Still gathering evidence",
        QualitativeConfidence.EMERGING.value: "Emerging confidence",
        QualitativeConfidence.RELIABLE.value: "Reliable guidance",
        QualitativeConfidence.HIGH.value: "High confidence",
    }
    return mapping.get(band, "Emerging confidence")

"""Learning Timeline — chronological events from Evidence Packages (KWP-011).

Never fabricates events. Each entry requires supporting sitting evidence.
"""

from __future__ import annotations

from typing import Any

from app.application.educational_memory.dto import (
    TIMELINE_TITLES,
    TimelineEntry,
    TimelineEventKind,
)
from app.application.educational_memory.snapshot import snapshot_from_package
from app.application.learning_strategy.dto import StrategyEvidenceInput


def build_learning_timeline(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> tuple[TimelineEntry, ...]:
    """Derive a chronological educational timeline from persisted packages."""
    ordered = _chronological(packages, student_id=student_id)
    if not ordered:
        return ()

    entries: list[TimelineEntry] = []
    seen_topics: set[str] = set()
    topic_sittings: dict[str, list[dict[str, Any]]] = {}

    for package in ordered:
        topic = str(package.get("topic_title") or "").strip() or "a topic"
        topic_key = topic.lower()
        practice = StrategyEvidenceInput.from_opaque(package)
        snap = snapshot_from_package(package)
        stamp = _stamp(package, snap)
        session_id = str(package.get("session_id") or "")
        package_id = str(package.get("package_id") or "")
        strategy_action = ""
        if snap and snap.strategy:
            strategy_action = str(snap.strategy.get("action") or "")

        prior_list = list(topic_sittings.get(topic_key) or ())
        topic_sittings.setdefault(topic_key, []).append(package)

        # Always record the sitting spine.
        entries.append(
            TimelineEntry(
                kind=TimelineEventKind.SITTING_RECORDED,
                title=TIMELINE_TITLES[TimelineEventKind.SITTING_RECORDED],
                body=f"You studied {topic}.",
                topic_title=topic,
                session_id=session_id,
                package_id=package_id,
                recorded_at=stamp,
                evidence_codes=("sitting_package",),
            )
        )

        if topic_key not in seen_topics:
            seen_topics.add(topic_key)
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.STARTED_TOPIC,
                    title=TIMELINE_TITLES[TimelineEventKind.STARTED_TOPIC],
                    body=f"You began working on {topic}.",
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("first_topic_sitting",),
                )
            )

        if strategy_action in {
            "immediate_reinforcement",
            "repeat_practice",
            "practice_for_certainty",
        } or (
            len(prior_list) >= 1
            and practice.practice_incorrect > practice.practice_correct
        ):
            if len(prior_list) >= 1:
                entries.append(
                    TimelineEntry(
                        kind=TimelineEventKind.REPEATED_REINFORCEMENT,
                        title=TIMELINE_TITLES[
                            TimelineEventKind.REPEATED_REINFORCEMENT
                        ],
                        body=(
                            f"Evidence shows continued reinforcement on {topic}."
                        ),
                        topic_title=topic,
                        session_id=session_id,
                        package_id=package_id,
                        recorded_at=stamp,
                        evidence_codes=("reinforcement", strategy_action or "weak"),
                    )
                )

        if strategy_action == "consolidate_understanding":
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.CONSOLIDATED,
                    title=TIMELINE_TITLES[TimelineEventKind.CONSOLIDATED],
                    body=f"You consolidated understanding of {topic}.",
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("consolidate_understanding",),
                )
            )

        if prior_list:
            prior_practice = StrategyEvidenceInput.from_opaque(prior_list[-1])
            prior_acc = _accuracy(prior_practice)
            curr_acc = _accuracy(practice)
            if (
                prior_acc is not None
                and curr_acc is not None
                and curr_acc > prior_acc
                and practice.practice_attempted > 0
            ):
                entries.append(
                    TimelineEntry(
                        kind=TimelineEventKind.UNDERSTANDING_IMPROVED,
                        title=TIMELINE_TITLES[
                            TimelineEventKind.UNDERSTANDING_IMPROVED
                        ],
                        body=(
                            f"Recent evidence suggests stronger understanding "
                            f"of {topic}."
                        ),
                        topic_title=topic,
                        session_id=session_id,
                        package_id=package_id,
                        recorded_at=stamp,
                        evidence_codes=("accuracy_improved",),
                    )
                )

        if practice.progress_advanced or strategy_action == "advance_topic":
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.ADVANCED,
                    title=TIMELINE_TITLES[TimelineEventKind.ADVANCED],
                    body=f"You advanced on {topic}.",
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("progress_advanced",),
                )
            )

        if strategy_action == "recover_prior_knowledge" or (
            practice.retention_risk and practice.weak_topic
        ):
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.KNOWLEDGE_DECAYED,
                    title=TIMELINE_TITLES[TimelineEventKind.KNOWLEDGE_DECAYED],
                    body=(
                        f"Evidence suggested knowledge of {topic} needed recovery."
                    ),
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("retention_or_recovery",),
                )
            )

        eff_verdict = ""
        if snap and snap.effectiveness:
            eff_verdict = str(snap.effectiveness.get("verdict") or "")
        prior_kind = ""
        if snap and snap.prior_intervention:
            prior_kind = str(snap.prior_intervention.get("kind") or "")
        if (
            strategy_action == "recover_prior_knowledge"
            and _is_strong(practice)
        ) or (
            prior_kind == "recovery" and eff_verdict == "effective"
        ):
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.RECOVERED,
                    title=TIMELINE_TITLES[TimelineEventKind.RECOVERED],
                    body=f"You recovered understanding of {topic}.",
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("recovery",),
                )
            )

        # Sustained mastery: strong sitting after prior strong + advance or maintain.
        if (
            _is_strong(practice)
            and practice.progress_advanced
            and len(prior_list) >= 1
            and _is_strong(StrategyEvidenceInput.from_opaque(prior_list[-1]))
        ):
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.MASTERED,
                    title=TIMELINE_TITLES[TimelineEventKind.MASTERED],
                    body=(
                        f"Evidence supports sustained mastery signals on {topic}."
                    ),
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("sustained_mastery",),
                )
            )

        if practice.has_reflection:
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.REFLECTED,
                    title=TIMELINE_TITLES[TimelineEventKind.REFLECTED],
                    body=f"You reflected after studying {topic}.",
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("reflection",),
                )
            )

        # KWP-014 — optional curriculum movement when difficulty band advances.
        movement = _curriculum_movement_for(package, practice, prior_list)
        if movement is not None:
            kind, body, movement_label = movement
            entries.append(
                TimelineEntry(
                    kind=kind,
                    title=TIMELINE_TITLES[kind],
                    body=body,
                    topic_title=topic,
                    session_id=session_id,
                    package_id=package_id,
                    recorded_at=stamp,
                    evidence_codes=("curriculum_movement", kind.value),
                    curriculum_movement=movement_label,
                )
            )

    return tuple(entries)


def _chronological(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> list[dict[str, Any]]:
    sid = (student_id or "").strip()
    rows = [
        p
        for p in packages
        if isinstance(p, dict)
        and (not sid or str(p.get("student_id") or "").strip() == sid)
    ]
    rows.sort(key=lambda p: str(p.get("created_at") or ""))
    return rows


def _stamp(package: dict[str, Any], snap: Any) -> str:
    if snap is not None and getattr(snap, "captured_at", ""):
        return str(snap.captured_at)
    return str(package.get("created_at") or "")


def _accuracy(practice: StrategyEvidenceInput) -> float | None:
    scored = practice.practice_correct + practice.practice_incorrect
    if scored <= 0:
        return None
    return practice.practice_correct / scored


def _is_strong(practice: StrategyEvidenceInput) -> bool:
    scored = practice.practice_correct + practice.practice_incorrect
    if scored <= 0:
        return False
    return practice.practice_correct >= practice.practice_incorrect and scored >= 2


def _curriculum_movement_for(
    package: dict[str, Any],
    practice: StrategyEvidenceInput,
    prior_list: list[dict[str, Any]],
) -> tuple[TimelineEventKind, str, str] | None:
    """Optionally reference curriculum stage movement from sitting evidence."""
    if not practice.progress_advanced and not _is_strong(practice):
        return None
    difficulty = str(
        package.get("difficulty")
        or package.get("topic_difficulty")
        or ""
    ).strip().lower()
    topic = str(package.get("topic_title") or "").strip() or "this topic"

    if difficulty in {"foundational", "foundation"} and (
        practice.progress_advanced or len(prior_list) >= 1
    ):
        return (
            TimelineEventKind.FOUNDATION_COMPLETE,
            f"Foundation complete on {topic} — ready to build further.",
            "foundation → intermediate modelling",
        )
    if difficulty in {"intermediate"} and practice.progress_advanced:
        return (
            TimelineEventKind.INTERMEDIATE_MODELLING,
            f"Intermediate modelling progress on {topic}.",
            "intermediate modelling",
        )
    if difficulty in {"advanced", "capstone"} and practice.progress_advanced:
        return (
            TimelineEventKind.EXAM_INTEGRATION,
            f"Exam integration work on {topic}.",
            "exam integration",
        )
    return None

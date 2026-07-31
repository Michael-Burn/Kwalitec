"""Student Learning Journey narrative (KWP-011).

Transforms sitting memory into an educational story — not raw analytics.
"""

from __future__ import annotations

from typing import Any

from app.application.educational_memory.dto import (
    LearningJourneyNarrative,
    TimelineEventKind,
)
from app.application.educational_memory.milestones import detect_learning_milestones
from app.application.educational_memory.patterns import detect_longitudinal_patterns
from app.application.educational_memory.snapshot import snapshot_from_package
from app.application.educational_memory.timeline import build_learning_timeline


def build_learning_journey_narrative(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> LearningJourneyNarrative:
    """Compose My Learning Journey from Evidence Packages + snapshots."""
    sid = (student_id or "").strip()
    ordered = [
        p
        for p in packages
        if isinstance(p, dict)
        and (not sid or str(p.get("student_id") or "").strip() == sid)
    ]
    ordered.sort(key=lambda p: str(p.get("created_at") or ""))

    if not ordered:
        return LearningJourneyNarrative(
            headline="Your learning journey is just beginning",
            story_paragraphs=(
                "As you complete study sittings, this page will tell the "
                "story of how your understanding develops over time.",
            ),
            has_memory=False,
        )

    timeline = build_learning_timeline(ordered, student_id=sid)
    patterns = detect_longitudinal_patterns(ordered, student_id=sid)
    milestones = detect_learning_milestones(ordered, student_id=sid)
    archives = _sitting_archives(ordered)
    topics = {
        str(p.get("topic_title") or "").strip()
        for p in ordered
        if str(p.get("topic_title") or "").strip()
    }

    story = _story_paragraphs(ordered, timeline=timeline, patterns=patterns)
    headline = (
        "My Learning Journey"
        if len(ordered) >= 2
        else "Your first chapter is underway"
    )

    return LearningJourneyNarrative(
        headline=headline,
        story_paragraphs=story,
        timeline=timeline,
        patterns=patterns,
        milestones=milestones,
        sitting_archives=archives,
        sitting_count=len(ordered),
        topic_count=len(topics),
        has_memory=True,
    )


def _sitting_archives(
    packages: list[dict[str, Any]],
) -> tuple[dict[str, str], ...]:
    """Newest-first archive rows for revisiting Sitting Reports."""
    rows: list[dict[str, str]] = []
    for package in reversed(packages):
        snap = snapshot_from_package(package)
        topic = str(package.get("topic_title") or "").strip() or "Study sitting"
        session_id = str(package.get("session_id") or "")
        stamp = str(
            (snap.captured_at if snap else "")
            or package.get("created_at")
            or ""
        )
        strategy = ""
        if snap and snap.student_sitting_report:
            strategy = str(
                snap.student_sitting_report.get("strategy_title") or ""
            )
        elif snap and snap.strategy:
            strategy = str(snap.strategy.get("recommendation_title") or "")
        rows.append(
            {
                "session_id": session_id,
                "topic_title": topic,
                "recorded_at": stamp,
                "strategy_title": strategy,
                "has_snapshot": "true" if snap is not None else "false",
            }
        )
    return tuple(rows)


def _story_paragraphs(
    packages: list[dict[str, Any]],
    *,
    timeline: tuple[Any, ...],
    patterns: tuple[Any, ...],
) -> tuple[str, ...]:
    paragraphs: list[str] = []
    topics = [
        str(p.get("topic_title") or "").strip()
        for p in packages
        if str(p.get("topic_title") or "").strip()
    ]
    if not topics:
        return (
            "Your study sittings are recorded. Meaning will thicken as "
            "evidence accumulates.",
        )

    # Opening — earliest topic that needed reinforcement or first topic.
    first_topic = topics[0]
    reinforce_kinds = {
        TimelineEventKind.REPEATED_REINFORCEMENT,
        TimelineEventKind.CONSOLIDATED,
    }
    early_reinforce = next(
        (
            e
            for e in timeline
            if e.kind in reinforce_kinds and e.topic_title
        ),
        None,
    )
    if early_reinforce is not None:
        paragraphs.append(
            f"Earlier evidence shows {early_reinforce.topic_title} required "
            "careful reinforcement before it settled."
        )
    else:
        paragraphs.append(
            f"Your journey includes focused study on {first_topic}"
            + (
                f" and {len(set(topics)) - 1} other topic(s)."
                if len(set(topics)) > 1
                else "."
            )
        )

    improved = [
        e
        for e in timeline
        if e.kind is TimelineEventKind.UNDERSTANDING_IMPROVED
    ]
    if improved:
        latest = improved[-1]
        paragraphs.append(
            f"Recent evidence suggests you now apply {latest.topic_title} "
            "more consistently than earlier sittings."
        )

    recovered = [
        e for e in timeline if e.kind is TimelineEventKind.RECOVERED
    ]
    if recovered:
        latest = recovered[-1]
        paragraphs.append(
            f"You recovered understanding of {latest.topic_title} after "
            "it needed attention — growth that only shows across time."
        )

    if patterns:
        paragraphs.append(patterns[0].narrative)

    mastered = [
        e for e in timeline if e.kind is TimelineEventKind.MASTERED
    ]
    if mastered:
        latest = mastered[-1]
        paragraphs.append(
            f"Sustained evidence supports mastery signals on "
            f"{latest.topic_title}."
        )

    if len(paragraphs) == 1 and len(packages) >= 2:
        paragraphs.append(
            f"Across {len(packages)} sittings, your educational story is "
            "taking shape from honest practice — not from scores."
        )

    return tuple(paragraphs[:5])

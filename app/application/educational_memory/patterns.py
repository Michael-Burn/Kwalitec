"""Longitudinal educational patterns from sitting memory (KWP-011).

Detects recurring patterns from Evidence Packages + intelligence snapshots.
Does not invent scores — counts evidence-backed repetitions only.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from app.application.educational_memory.dto import (
    PATTERN_TITLES,
    LongitudinalPattern,
    PatternKind,
)
from app.application.educational_memory.snapshot import snapshot_from_package
from app.application.learning_strategy.dto import StrategyEvidenceInput


def detect_longitudinal_patterns(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> tuple[LongitudinalPattern, ...]:
    """Detect recurring educational patterns across a learner's sittings."""
    ordered = _chronological(packages, student_id=student_id)
    if len(ordered) < 2:
        return ()

    patterns: list[LongitudinalPattern] = []

    prereq_topics: list[str] = []
    mismatch_topics: list[str] = []
    recovery_successes: list[str] = []
    consolidation_topics: list[str] = []
    advance_without_reinforce = 0
    reinforce_early = 0
    strong_finishes = 0
    partial_finishes = 0
    retention_then_strong = 0
    retention_signals = 0

    for idx, package in enumerate(ordered):
        snap = snapshot_from_package(package)
        practice = StrategyEvidenceInput.from_opaque(package)
        topic = str(package.get("topic_title") or "").strip() or "a topic"
        strategy_action = str((snap.strategy if snap else {}).get("action") or "")
        diag_cat = str((snap.diagnostics if snap else {}).get("category") or "")
        calibration = str((snap.strategy if snap else {}).get("calibration") or "")
        eff_verdict = str(
            (snap.effectiveness if snap else {}).get("verdict") or ""
        )
        prior_kind = str(
            (snap.prior_intervention if snap else {}).get("kind") or ""
        )

        if diag_cat == "prerequisite_weakness":
            prereq_topics.append(topic)
        if diag_cat == "confidence_mismatch" or calibration in {
            "over_confident",
            "under_confident",
        }:
            mismatch_topics.append(topic)
        if strategy_action == "consolidate_understanding":
            consolidation_topics.append(topic)
        if (
            prior_kind == "recovery" and eff_verdict == "effective"
        ) or (
            strategy_action == "recover_prior_knowledge"
            and _is_strong(practice)
        ):
            recovery_successes.append(topic)

        if idx < max(1, len(ordered) // 2):
            if strategy_action in {
                "immediate_reinforcement",
                "consolidate_understanding",
                "repeat_practice",
            }:
                reinforce_early += 1
        else:
            if strategy_action in {
                "advance_topic",
                "increase_challenge",
                "maintain_current_pace",
            }:
                advance_without_reinforce += 1

        if practice.finish_verdict == "yes" and _is_strong(practice):
            strong_finishes += 1
        if practice.finish_verdict in {"partially", "no"}:
            partial_finishes += 1

        if practice.retention_risk or strategy_action == "recover_prior_knowledge":
            retention_signals += 1
            if idx + 1 < len(ordered):
                nxt = StrategyEvidenceInput.from_opaque(ordered[idx + 1])
                same = (
                    str(ordered[idx + 1].get("topic_title") or "").strip().lower()
                    == topic.lower()
                )
                if same and _is_strong(nxt):
                    retention_then_strong += 1

    patterns.extend(
        _pattern_if(
            PatternKind.REPEATED_PREREQUISITE_WEAKNESS,
            prereq_topics,
            (
                "Evidence repeatedly pointed to prerequisite gaps across "
                f"{len(set(prereq_topics))} topic(s)."
            ),
            min_count=2,
        )
    )
    patterns.extend(
        _pattern_if(
            PatternKind.REPEATED_CONFIDENCE_MISMATCH,
            mismatch_topics,
            (
                "Confidence and performance have mismatched more than once — "
                "a pattern worth watching gently."
            ),
            min_count=2,
        )
    )
    patterns.extend(
        _pattern_if(
            PatternKind.REPEATED_SUCCESSFUL_RECOVERIES,
            recovery_successes,
            (
                "You have successfully recovered understanding after difficulty "
                f"on {len(set(recovery_successes))} topic(s)."
            ),
            min_count=2,
        )
    )
    patterns.extend(
        _pattern_if(
            PatternKind.REPEATED_CONSOLIDATION,
            consolidation_topics,
            (
                "Consolidation has been a recurring next step — evidence of "
                "careful, durable learning."
            ),
            min_count=2,
        )
    )

    if reinforce_early >= 2 and advance_without_reinforce >= 2:
        patterns.append(
            LongitudinalPattern(
                kind=PatternKind.INCREASING_INDEPENDENCE,
                title=PATTERN_TITLES[PatternKind.INCREASING_INDEPENDENCE],
                narrative=(
                    "Earlier sittings often needed reinforcement; recent "
                    "evidence shows more independent progress."
                ),
                occurrence_count=advance_without_reinforce,
                evidence_codes=("early_reinforce", "later_advance"),
            )
        )

    if strong_finishes >= 3 and strong_finishes > partial_finishes:
        patterns.append(
            LongitudinalPattern(
                kind=PatternKind.IMPROVING_CONSISTENCY,
                title=PATTERN_TITLES[PatternKind.IMPROVING_CONSISTENCY],
                narrative=(
                    f"You completed {strong_finishes} strong sittings with "
                    "honest finishes — consistency is improving."
                ),
                occurrence_count=strong_finishes,
                evidence_codes=("strong_finishes",),
            )
        )

    if retention_signals >= 1 and retention_then_strong >= 1:
        patterns.append(
            LongitudinalPattern(
                kind=PatternKind.LONG_TERM_RETENTION_IMPROVEMENTS,
                title=PATTERN_TITLES[
                    PatternKind.LONG_TERM_RETENTION_IMPROVEMENTS
                ],
                narrative=(
                    "After retention risk signals, later sittings showed "
                    "stronger performance — retention is improving."
                ),
                occurrence_count=retention_then_strong,
                evidence_codes=("retention_then_strong",),
            )
        )

    return tuple(patterns)


def _pattern_if(
    kind: PatternKind,
    topics: list[str],
    narrative: str,
    *,
    min_count: int,
) -> list[LongitudinalPattern]:
    if len(topics) < min_count:
        return []
    unique = tuple(dict.fromkeys(topics))
    return [
        LongitudinalPattern(
            kind=kind,
            title=PATTERN_TITLES[kind],
            narrative=narrative,
            occurrence_count=len(topics),
            topics=unique[:8],
            evidence_codes=(kind.value,),
        )
    ]


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


def _is_strong(practice: StrategyEvidenceInput) -> bool:
    scored = practice.practice_correct + practice.practice_incorrect
    if scored <= 0:
        return False
    return practice.practice_correct >= practice.practice_incorrect and scored >= 2


def pattern_topic_counts(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
) -> Counter[str]:
    """Helper for founder analytics — diagnostic category frequencies."""
    counts: Counter[str] = Counter()
    for package in packages:
        if not isinstance(package, dict):
            continue
        snap = snapshot_from_package(package)
        if snap is None:
            continue
        cat = str(snap.diagnostics.get("category") or "")
        if cat:
            counts[cat] += 1
    return counts

"""Educational Memory metrics for Founder observability (KWP-011).

Longitudinal aggregates over Evidence Packages + intelligence snapshots.
Does not mutate Strategy, Diagnostics, Difficulty, Effectiveness, Evidence,
Progress, Twin, or Session runtime.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from app.application.educational_memory.milestones import detect_learning_milestones
from app.application.educational_memory.patterns import (
    detect_longitudinal_patterns,
    pattern_topic_counts,
)
from app.application.educational_memory.snapshot import snapshot_from_package
from app.application.educational_memory.timeline import build_learning_timeline
from app.application.learning_strategy.dto import StrategyEvidenceInput


@dataclass(frozen=True)
class EducationalMemoryMetricsSnapshot:
    """Founder-facing longitudinal educational memory summary."""

    sittings_with_memory: int = 0
    sittings_total: int = 0
    snapshot_coverage: float = 0.0
    timeline_entry_count: int = 0
    timeline_completeness: float = 0.0
    pattern_counts: dict[str, int] = field(default_factory=dict)
    milestone_counts: dict[str, int] = field(default_factory=dict)
    repeated_misconception_categories: dict[str, int] = field(default_factory=dict)
    average_recovery_duration_sittings: float = 0.0
    average_mastery_duration_sittings: float = 0.0
    retention_recovery_rate: float = 0.0
    recommendation_persistence_rate: float = 0.0
    learners_with_journey: int = 0
    growth_trajectory_labels: tuple[str, ...] = ()

    def to_opaque(self) -> dict[str, Any]:
        return {
            "sittings_with_memory": self.sittings_with_memory,
            "sittings_total": self.sittings_total,
            "snapshot_coverage": round(self.snapshot_coverage, 4),
            "timeline_entry_count": self.timeline_entry_count,
            "timeline_completeness": round(self.timeline_completeness, 4),
            "pattern_counts": dict(self.pattern_counts),
            "milestone_counts": dict(self.milestone_counts),
            "repeated_misconception_categories": dict(
                self.repeated_misconception_categories
            ),
            "average_recovery_duration_sittings": round(
                self.average_recovery_duration_sittings, 4
            ),
            "average_mastery_duration_sittings": round(
                self.average_mastery_duration_sittings, 4
            ),
            "retention_recovery_rate": round(self.retention_recovery_rate, 4),
            "recommendation_persistence_rate": round(
                self.recommendation_persistence_rate, 4
            ),
            "learners_with_journey": self.learners_with_journey,
            "growth_trajectory_labels": list(self.growth_trajectory_labels),
        }


class EducationalMemoryMetrics:
    """Compute longitudinal memory metrics from persisted packages."""

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    ) -> EducationalMemoryMetricsSnapshot:
        rows = [p for p in packages if isinstance(p, dict)]
        total = len(rows)
        if total == 0:
            return EducationalMemoryMetricsSnapshot()

        with_snap = 0
        with_strategy = 0
        by_student: dict[str, list[dict[str, Any]]] = {}
        for package in rows:
            snap = snapshot_from_package(package)
            if snap is not None:
                with_snap += 1
                if snap.strategy or snap.student_sitting_report:
                    with_strategy += 1
            sid = str(package.get("student_id") or "").strip() or "_unknown"
            by_student.setdefault(sid, []).append(package)

        timeline = build_learning_timeline(rows)
        # Completeness: meaningful events beyond raw sitting spine.
        meaningful = [
            e
            for e in timeline
            if e.kind.value != "sitting_recorded"
        ]
        completeness = len(meaningful) / max(1, total)

        pattern_counts: Counter[str] = Counter()
        milestone_counts: Counter[str] = Counter()
        trajectories: list[str] = []
        recovery_spans: list[int] = []
        mastery_spans: list[int] = []
        retention_starts = 0
        retention_recoveries = 0
        learners_with_journey = 0

        for sid, student_rows in by_student.items():
            student_rows.sort(key=lambda p: str(p.get("created_at") or ""))
            patterns = detect_longitudinal_patterns(
                student_rows, student_id=sid if sid != "_unknown" else ""
            )
            milestones = detect_learning_milestones(
                student_rows, student_id=sid if sid != "_unknown" else ""
            )
            if len(student_rows) >= 2:
                learners_with_journey += 1
            for pattern in patterns:
                pattern_counts[pattern.kind.value] += 1
                if pattern.kind.value in {
                    "increasing_independence",
                    "improving_consistency",
                    "long_term_retention_improvements",
                }:
                    trajectories.append(pattern.title)
            for milestone in milestones:
                milestone_counts[milestone.kind.value] += 1

            recovery_spans.extend(_recovery_spans(student_rows))
            mastery_spans.extend(_mastery_spans(student_rows))
            r_start, r_ok = _retention_stats(student_rows)
            retention_starts += r_start
            retention_recoveries += r_ok

        misconception = dict(pattern_topic_counts(rows))
        # Focus on categories that look like misconceptions / weaknesses.
        repeated = {
            k: v
            for k, v in misconception.items()
            if k
            in {
                "prerequisite_weakness",
                "conceptual_misunderstanding",
                "formula_recall",
                "calculation_accuracy",
                "confidence_mismatch",
            }
            and v >= 2
        }

        return EducationalMemoryMetricsSnapshot(
            sittings_with_memory=with_snap,
            sittings_total=total,
            snapshot_coverage=with_snap / total,
            timeline_entry_count=len(timeline),
            timeline_completeness=min(1.0, completeness),
            pattern_counts=dict(pattern_counts),
            milestone_counts=dict(milestone_counts),
            repeated_misconception_categories=repeated,
            average_recovery_duration_sittings=(
                sum(recovery_spans) / len(recovery_spans) if recovery_spans else 0.0
            ),
            average_mastery_duration_sittings=(
                sum(mastery_spans) / len(mastery_spans) if mastery_spans else 0.0
            ),
            retention_recovery_rate=(
                retention_recoveries / retention_starts if retention_starts else 0.0
            ),
            recommendation_persistence_rate=with_strategy / total,
            learners_with_journey=learners_with_journey,
            growth_trajectory_labels=tuple(dict.fromkeys(trajectories))[:8],
        )

    @classmethod
    def from_store(cls, store: Any) -> EducationalMemoryMetricsSnapshot:
        from app.services.educational_yield_metrics import list_evidence_packages

        return cls.from_packages(list_evidence_packages(store))


def _recovery_spans(packages: list[dict[str, Any]]) -> list[int]:
    """Sittings from recovery recommendation to strong subsequent finish."""
    spans: list[int] = []
    pending_from: int | None = None
    for idx, package in enumerate(packages):
        snap = snapshot_from_package(package)
        action = str((snap.strategy if snap else {}).get("action") or "")
        practice = StrategyEvidenceInput.from_opaque(package)
        if action == "recover_prior_knowledge" and pending_from is None:
            pending_from = idx
        if pending_from is not None and idx > pending_from and _is_strong(practice):
            spans.append(idx - pending_from)
            pending_from = None
    return spans


def _mastery_spans(packages: list[dict[str, Any]]) -> list[int]:
    """Sittings from first topic contact to first advance/strong pair."""
    by_topic: dict[str, int] = {}
    spans: list[int] = []
    for idx, package in enumerate(packages):
        topic = str(package.get("topic_title") or "").strip().lower()
        if not topic:
            continue
        if topic not in by_topic:
            by_topic[topic] = idx
        practice = StrategyEvidenceInput.from_opaque(package)
        if practice.progress_advanced and _is_strong(practice):
            start = by_topic[topic]
            spans.append(max(1, idx - start + 1))
            # Only count first mastery span per topic.
            by_topic[topic] = idx  # prevent re-trigger noise; still ok
    return spans


def _retention_stats(packages: list[dict[str, Any]]) -> tuple[int, int]:
    starts = 0
    recoveries = 0
    for idx, package in enumerate(packages):
        practice = StrategyEvidenceInput.from_opaque(package)
        snap = snapshot_from_package(package)
        action = str((snap.strategy if snap else {}).get("action") or "")
        if not (practice.retention_risk or action == "recover_prior_knowledge"):
            continue
        starts += 1
        topic = str(package.get("topic_title") or "").strip().lower()
        for later in packages[idx + 1 :]:
            if str(later.get("topic_title") or "").strip().lower() != topic:
                continue
            if _is_strong(StrategyEvidenceInput.from_opaque(later)):
                recoveries += 1
            break
    return starts, recoveries


def _is_strong(practice: StrategyEvidenceInput) -> bool:
    scored = practice.practice_correct + practice.practice_incorrect
    if scored <= 0:
        return False
    return practice.practice_correct >= practice.practice_incorrect and scored >= 2

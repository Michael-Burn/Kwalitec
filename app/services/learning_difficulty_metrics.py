"""Learning Difficulty metrics for Founder observability (KWP-009).

Aggregates educational load / pacing insights over persisted Evidence Packages.
Does not change Evidence Authority, Twin, Progress, Strategy, Diagnostics,
or Session runtime.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

from app.application.learning_difficulty.dto import (
    EducationalPacing,
    LoadRecommendation,
    ObservedDifficulty,
)
from app.application.learning_difficulty.engine import LearningDifficultyEngine


@dataclass(frozen=True)
class LearningDifficultyMetricsSnapshot:
    """Founder-facing difficulty / load distribution and topic trends."""

    sittings_evaluated: int = 0
    recommendation_counts: dict[str, int] = field(default_factory=dict)
    pacing_counts: dict[str, int] = field(default_factory=dict)
    observed_difficulty_counts: dict[str, int] = field(default_factory=dict)
    # Topics generating highest average load (topic → avg load points).
    highest_load_topics: tuple[tuple[str, float], ...] = ()
    # Average reinforcement sessions by topic.
    average_reinforcement_by_topic: dict[str, float] = field(default_factory=dict)
    # Pacing trend rates.
    slow_pacing_rate: float = 0.0
    maintain_pacing_rate: float = 0.0
    accelerate_pacing_rate: float = 0.0
    hold_pacing_rate: float = 0.0
    # Recovery after difficult topics.
    recovery_after_difficult_rate: float = 0.0
    consolidation_rate: float = 0.0
    reduce_length_rate: float = 0.0
    average_load_points: float = 0.0

    def to_opaque(self) -> dict[str, Any]:
        return {
            "sittings_evaluated": self.sittings_evaluated,
            "recommendation_counts": dict(self.recommendation_counts),
            "pacing_counts": dict(self.pacing_counts),
            "observed_difficulty_counts": dict(self.observed_difficulty_counts),
            "highest_load_topics": [
                {"topic": t, "average_load": round(v, 2)}
                for t, v in self.highest_load_topics
            ],
            "average_reinforcement_by_topic": {
                k: round(v, 2) for k, v in self.average_reinforcement_by_topic.items()
            },
            "slow_pacing_rate": round(self.slow_pacing_rate, 4),
            "maintain_pacing_rate": round(self.maintain_pacing_rate, 4),
            "accelerate_pacing_rate": round(self.accelerate_pacing_rate, 4),
            "hold_pacing_rate": round(self.hold_pacing_rate, 4),
            "recovery_after_difficult_rate": round(
                self.recovery_after_difficult_rate, 4
            ),
            "consolidation_rate": round(self.consolidation_rate, 4),
            "reduce_length_rate": round(self.reduce_length_rate, 4),
            "average_load_points": round(self.average_load_points, 2),
        }


class LearningDifficultyMetrics:
    """Compute difficulty / load trends from persisted sitting packages."""

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
        *,
        engine: LearningDifficultyEngine | None = None,
        top_n: int = 8,
    ) -> LearningDifficultyMetricsSnapshot:
        difficulty_engine = engine or LearningDifficultyEngine()
        rec_counts: Counter[str] = Counter()
        pacing_counts: Counter[str] = Counter()
        observed_counts: Counter[str] = Counter()
        load_by_topic: dict[str, list[int]] = defaultdict(list)
        reinforcement_by_topic: dict[str, list[int]] = defaultdict(list)
        evaluated = 0
        recovered = 0
        difficult_sittings = 0
        load_total = 0

        for raw in packages:
            if not isinstance(raw, dict):
                continue
            profile = difficulty_engine.evaluate_opaque(raw)
            evaluated += 1
            rec_counts[profile.recommendation.value] += 1
            pacing_counts[profile.educational_pacing.value] += 1
            observed_counts[profile.observed_difficulty.value] += 1
            load_total += profile.load_points
            topic = (profile.topic_title or str(raw.get("topic_title") or "")).strip()
            if topic:
                load_by_topic[topic].append(profile.load_points)
                reinforcement_by_topic[topic].append(
                    int(raw.get("reinforcement_session_count") or 0)
                )

            is_difficult = profile.observed_difficulty in {
                ObservedDifficulty.DEMANDING,
                ObservedDifficulty.VERY_DEMANDING,
            }
            if is_difficult:
                difficult_sittings += 1
                if (
                    raw.get("recovered_after_difficult")
                    or raw.get("recovered_after_misses")
                    or "recovery" in profile.evidence_codes
                ):
                    recovered += 1

        if evaluated == 0:
            return LearningDifficultyMetricsSnapshot()

        avg_load_topics = sorted(
            (
                (topic, sum(vals) / len(vals))
                for topic, vals in load_by_topic.items()
                if vals
            ),
            key=lambda item: item[1],
            reverse=True,
        )[:top_n]

        avg_reinforcement = {
            topic: sum(vals) / len(vals)
            for topic, vals in reinforcement_by_topic.items()
            if vals
        }

        def _pacing_rate(pacing: EducationalPacing) -> float:
            return pacing_counts.get(pacing.value, 0) / evaluated

        def _rec_rate(rec: LoadRecommendation) -> float:
            return rec_counts.get(rec.value, 0) / evaluated

        return LearningDifficultyMetricsSnapshot(
            sittings_evaluated=evaluated,
            recommendation_counts=dict(rec_counts),
            pacing_counts=dict(pacing_counts),
            observed_difficulty_counts=dict(observed_counts),
            highest_load_topics=tuple(avg_load_topics),
            average_reinforcement_by_topic=avg_reinforcement,
            slow_pacing_rate=_pacing_rate(EducationalPacing.SLOW),
            maintain_pacing_rate=_pacing_rate(EducationalPacing.MAINTAIN),
            accelerate_pacing_rate=_pacing_rate(EducationalPacing.ACCELERATE),
            hold_pacing_rate=_pacing_rate(EducationalPacing.HOLD),
            recovery_after_difficult_rate=(
                recovered / difficult_sittings if difficult_sittings else 0.0
            ),
            consolidation_rate=_rec_rate(
                LoadRecommendation.TAKE_CONSOLIDATION_SESSION
            ),
            reduce_length_rate=_rec_rate(
                LoadRecommendation.REDUCE_SESSION_LENGTH
            ),
            average_load_points=load_total / evaluated,
        )

    @classmethod
    def from_store(cls, store: Any) -> LearningDifficultyMetricsSnapshot:
        packages: list[dict[str, Any]] = []
        list_fn = getattr(store, "list_evidence_packages", None)
        if callable(list_fn):
            raw_list = list_fn()
            if isinstance(raw_list, list | tuple):
                packages = [p for p in raw_list if isinstance(p, dict)]
        elif hasattr(store, "evidence_packages"):
            raw_list = store.evidence_packages
            if isinstance(raw_list, list | tuple):
                packages = [p for p in raw_list if isinstance(p, dict)]
        return cls.from_packages(packages)

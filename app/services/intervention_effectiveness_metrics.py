"""Intervention effectiveness metrics for Founder observability (KWP-010).

Aggregates whether prior Strategy / Difficulty recommendations improved
subsequent sitting outcomes. Replays consecutive same-topic Evidence
Packages — does not mutate Strategy, Diagnostics, Difficulty, Evidence,
Progress, Twin, or Session runtime.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from app.application.intervention_effectiveness.dto import (
    EFFECTIVENESS_VERDICT_LABELS,
    EffectivenessVerdict,
    InterventionKind,
    prior_from_sitting,
)
from app.application.intervention_effectiveness.engine import (
    InterventionEffectivenessEngine,
)
from app.application.learning_difficulty.engine import LearningDifficultyEngine
from app.application.learning_strategy.engine import LearningStrategyEngine


@dataclass(frozen=True)
class InterventionEffectivenessMetricsSnapshot:
    """Founder-facing aggregate intervention outcome summary."""

    pairs_evaluated: int = 0
    verdict_counts: dict[str, int] = field(default_factory=dict)
    kind_counts: dict[str, int] = field(default_factory=dict)
    # Most / least effective by kind (kind → effective rate among evaluated).
    most_effective: tuple[tuple[str, float], ...] = ()
    least_effective: tuple[tuple[str, float], ...] = ()
    # Named product questions.
    consolidation_effective_rate: float = 0.0
    reinforcement_effective_rate: float = 0.0
    reduce_length_effective_rate: float = 0.0
    increase_spacing_effective_rate: float = 0.0
    challenge_success_rate: float = 0.0
    recovery_after_consolidation_rate: float = 0.0
    overall_effective_rate: float = 0.0
    overall_partial_rate: float = 0.0
    overall_ineffective_rate: float = 0.0
    insufficient_rate: float = 0.0

    def to_opaque(self) -> dict[str, Any]:
        return {
            "pairs_evaluated": self.pairs_evaluated,
            "verdict_counts": dict(self.verdict_counts),
            "kind_counts": dict(self.kind_counts),
            "most_effective": [
                {"kind": k, "effective_rate": round(r, 4)}
                for k, r in self.most_effective
            ],
            "least_effective": [
                {"kind": k, "effective_rate": round(r, 4)}
                for k, r in self.least_effective
            ],
            "consolidation_effective_rate": round(
                self.consolidation_effective_rate, 4
            ),
            "reinforcement_effective_rate": round(
                self.reinforcement_effective_rate, 4
            ),
            "reduce_length_effective_rate": round(
                self.reduce_length_effective_rate, 4
            ),
            "increase_spacing_effective_rate": round(
                self.increase_spacing_effective_rate, 4
            ),
            "challenge_success_rate": round(self.challenge_success_rate, 4),
            "recovery_after_consolidation_rate": round(
                self.recovery_after_consolidation_rate, 4
            ),
            "overall_effective_rate": round(self.overall_effective_rate, 4),
            "overall_partial_rate": round(self.overall_partial_rate, 4),
            "overall_ineffective_rate": round(self.overall_ineffective_rate, 4),
            "insufficient_rate": round(self.insufficient_rate, 4),
            "verdict_labels": {
                k: EFFECTIVENESS_VERDICT_LABELS[EffectivenessVerdict(k)]
                for k in self.verdict_counts
                if k in {v.value for v in EffectivenessVerdict}
            },
        }


class InterventionEffectivenessMetrics:
    """Compute intervention outcome trends from persisted sitting packages."""

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
        *,
        engine: InterventionEffectivenessEngine | None = None,
        strategy_engine: LearningStrategyEngine | None = None,
        difficulty_engine: LearningDifficultyEngine | None = None,
        top_n: int = 5,
    ) -> InterventionEffectivenessMetricsSnapshot:
        eff_engine = engine or InterventionEffectivenessEngine()
        strat_engine = strategy_engine or LearningStrategyEngine()
        diff_engine = difficulty_engine or LearningDifficultyEngine()

        ordered = [p for p in packages if isinstance(p, dict)]
        verdict_counts: Counter[str] = Counter()
        kind_counts: Counter[str] = Counter()
        # kind → [effective_count, decisive_count] (excludes insufficient)
        kind_effective: dict[str, list[int]] = {}
        consolidation_decisive = 0
        consolidation_good = 0
        pairs = 0

        for i in range(len(ordered) - 1):
            prior_pkg = ordered[i]
            next_pkg = ordered[i + 1]
            prior_topic = str(prior_pkg.get("topic_title") or "").strip().lower()
            next_topic = str(next_pkg.get("topic_title") or "").strip().lower()
            # Prefer same-topic pairs; allow empty topic match for thin packages.
            if prior_topic and next_topic and prior_topic != next_topic:
                continue

            # If subsequent already carries an explicit prior_intervention, use it.
            if isinstance(next_pkg.get("prior_intervention"), dict):
                report = eff_engine.evaluate_opaque(next_pkg)
            else:
                advice = strat_engine.evaluate_opaque(prior_pkg)
                profile = diff_engine.evaluate_opaque(prior_pkg)
                prior = prior_from_sitting(
                    strategy_action=advice.action,
                    load_recommendation=profile.recommendation,
                    topic_title=str(prior_pkg.get("topic_title") or ""),
                    practice_correct=int(prior_pkg.get("practice_correct") or 0),
                    practice_incorrect=int(
                        prior_pkg.get("practice_incorrect") or 0
                    ),
                    practice_attempted=int(
                        prior_pkg.get("practice_attempted") or 0
                    ),
                    session_duration_minutes=_optional_int(
                        prior_pkg.get("session_duration_minutes")
                        or prior_pkg.get("actual_duration_minutes")
                    ),
                    finish_verdict=_finish(prior_pkg),
                    progress_advanced=bool(prior_pkg.get("progress_advanced")),
                    source="metrics_replay",
                )
                report = eff_engine.evaluate_opaque(next_pkg, prior=prior)

            pairs += 1
            verdict_counts[report.verdict.value] += 1
            kind_counts[report.intervention_kind.value] += 1

            if report.verdict is not EffectivenessVerdict.INSUFFICIENT_EVIDENCE:
                bucket = kind_effective.setdefault(
                    report.intervention_kind.value, [0, 0]
                )
                bucket[1] += 1
                if report.verdict is EffectivenessVerdict.EFFECTIVE:
                    bucket[0] += 1
                elif report.verdict is EffectivenessVerdict.PARTIALLY_EFFECTIVE:
                    # Count partial as half toward ranking (stored as +0 via rate)
                    pass

            if report.intervention_kind is InterventionKind.CONSOLIDATION:
                if report.verdict is not EffectivenessVerdict.INSUFFICIENT_EVIDENCE:
                    consolidation_decisive += 1
                    if report.verdict in {
                        EffectivenessVerdict.EFFECTIVE,
                        EffectivenessVerdict.PARTIALLY_EFFECTIVE,
                    }:
                        consolidation_good += 1

        if pairs == 0:
            return InterventionEffectivenessMetricsSnapshot()

        rates: list[tuple[str, float]] = []
        for kind, (good, total) in kind_effective.items():
            if total <= 0:
                continue
            rates.append((kind, good / total))
        rates.sort(key=lambda item: item[1], reverse=True)
        most = tuple(rates[:top_n])
        least = tuple(sorted(rates, key=lambda item: item[1])[:top_n])

        def _rate(verdict: EffectivenessVerdict) -> float:
            return verdict_counts.get(verdict.value, 0) / pairs

        def _kind_eff(kind: InterventionKind) -> float:
            bucket = kind_effective.get(kind.value)
            if not bucket or bucket[1] == 0:
                return 0.0
            return bucket[0] / bucket[1]

        return InterventionEffectivenessMetricsSnapshot(
            pairs_evaluated=pairs,
            verdict_counts=dict(verdict_counts),
            kind_counts=dict(kind_counts),
            most_effective=most,
            least_effective=least,
            consolidation_effective_rate=_kind_eff(
                InterventionKind.CONSOLIDATION
            ),
            reinforcement_effective_rate=_kind_eff(
                InterventionKind.REINFORCEMENT
            ),
            reduce_length_effective_rate=_kind_eff(
                InterventionKind.REDUCE_SESSION_LENGTH
            ),
            increase_spacing_effective_rate=_kind_eff(
                InterventionKind.INCREASE_SPACING
            ),
            challenge_success_rate=_kind_eff(
                InterventionKind.INCREASE_CHALLENGE
            ),
            recovery_after_consolidation_rate=(
                consolidation_good / consolidation_decisive
                if consolidation_decisive
                else 0.0
            ),
            overall_effective_rate=_rate(EffectivenessVerdict.EFFECTIVE),
            overall_partial_rate=_rate(
                EffectivenessVerdict.PARTIALLY_EFFECTIVE
            ),
            overall_ineffective_rate=_rate(EffectivenessVerdict.INEFFECTIVE),
            insufficient_rate=_rate(
                EffectivenessVerdict.INSUFFICIENT_EVIDENCE
            ),
        )

    @classmethod
    def from_store(cls, store: Any) -> InterventionEffectivenessMetricsSnapshot:
        from app.services.educational_yield_metrics import list_evidence_packages

        packages = list_evidence_packages(store)
        return cls.from_packages(packages)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _finish(package: dict[str, Any]) -> str:
    review = package.get("finish_review")
    if isinstance(review, dict):
        return str(review.get("verdict") or "").strip().lower()
    return str(package.get("finish_verdict") or "").strip().lower()

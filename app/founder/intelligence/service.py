"""Founder Intelligence (V2-021) — advisory journey-level signals.

Non-authoritative over student Learning Mode. Surfaces inactive journeys,
stalled completion, reflection gaps, and recommendation thrash from
Experience projection documents and V1 continuity metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FounderIntelligenceSignal:
    """One advisory operational signal for Founders."""

    code: str
    severity: str
    title: str
    detail: str
    learner_id: str = ""
    count: int = 1


@dataclass(frozen=True)
class FounderIntelligenceSnapshot:
    """Advisory Founder Intelligence projection (no mutations)."""

    signals: tuple[FounderIntelligenceSignal, ...] = field(default_factory=tuple)
    inactive_journeys: int = 0
    stalled_completions: int = 0
    reflection_gaps: int = 0
    recommendation_thrash: int = 0
    dual_run_label: str = "dual-run"
    notes: tuple[str, ...] = field(default_factory=tuple)


class FounderIntelligenceService:
    """Build advisory journey-level Founder Intelligence signals."""

    def build(
        self,
        *,
        experience_store: Any | None = None,
        dual_run_label: str = "dual-run",
    ) -> FounderIntelligenceSnapshot:
        signals: list[FounderIntelligenceSignal] = []
        inactive = 0
        stalled = 0
        reflections = 0
        thrash = 0

        if experience_store is not None:
            journey_ids = experience_store.journey.list_ids()
            for learner_id in journey_ids:
                doc = experience_store.get(experience_store.journey, learner_id) or {}
                status = str(
                    doc.get("status") or doc.get("status_label") or ""
                ).lower()
                sessions_completed = int(doc.get("sessions_completed") or 0)
                if "inactive" in status or "stalled" in status:
                    inactive += 1
                    signals.append(
                        FounderIntelligenceSignal(
                            code="inactive_journey",
                            severity="warning",
                            title="Inactive journey",
                            detail=(
                                f"Learner {learner_id} journey marked "
                                "inactive/stalled."
                            ),
                            learner_id=str(learner_id),
                        )
                    )
                if sessions_completed == 0 and "progress" in status:
                    stalled += 1
                    signals.append(
                        FounderIntelligenceSignal(
                            code="stalled_completion",
                            severity="info",
                            title="Stalled completion",
                            detail=(
                                f"Learner {learner_id} has no completed "
                                "sessions yet."
                            ),
                            learner_id=str(learner_id),
                        )
                    )

            for learner_id in experience_store.sessions.list_ids():
                doc = (
                    experience_store.get(experience_store.sessions, learner_id) or {}
                )
                if doc.get("reflection_pending") or doc.get("reflection_deferred"):
                    reflections += 1
                    signals.append(
                        FounderIntelligenceSignal(
                            code="reflection_gap",
                            severity="info",
                            title="Reflection gap",
                            detail=(
                                f"Session {learner_id} has pending/deferred "
                                "reflection."
                            ),
                            learner_id=str(doc.get("student_id") or ""),
                        )
                    )

            for learner_id in experience_store.adaptive.list_ids():
                doc = (
                    experience_store.get(experience_store.adaptive, learner_id) or {}
                )
                history = doc.get("decision_history") or doc.get("thrash_count") or 0
                if isinstance(history, list) and len(history) >= 5:
                    thrash += 1
                    signals.append(
                        FounderIntelligenceSignal(
                            code="recommendation_thrash",
                            severity="warning",
                            title="Recommendation thrash",
                            detail=(
                                f"Learner {learner_id} has frequent "
                                "recommendation churn."
                            ),
                            learner_id=str(learner_id),
                            count=len(history),
                        )
                    )
                elif isinstance(history, int) and history >= 5:
                    thrash += 1
                    signals.append(
                        FounderIntelligenceSignal(
                            code="recommendation_thrash",
                            severity="warning",
                            title="Recommendation thrash",
                            detail=(
                                f"Learner {learner_id} thrash_count={history}."
                            ),
                            learner_id=str(learner_id),
                            count=history,
                        )
                    )

        notes = (
            "Founder Intelligence is advisory only.",
            "It must not mutate journeys, Twin state, or Adaptive decisions.",
            f"Dual-run posture: {dual_run_label}.",
        )
        return FounderIntelligenceSnapshot(
            signals=tuple(signals),
            inactive_journeys=inactive,
            stalled_completions=stalled,
            reflection_gaps=reflections,
            recommendation_thrash=thrash,
            dual_run_label=dual_run_label,
            notes=notes,
        )

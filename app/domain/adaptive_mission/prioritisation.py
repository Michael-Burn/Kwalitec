"""Deterministic mission candidate prioritisation.

Ranks educational decisions already present on the Twin / Learning Graph.
Never invents educational inferences or uses randomness.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from app.domain.adaptive_mission.mission_priority import (
    MissionPriority,
    MissionPriorityScore,
    priority_from_score,
)
from app.domain.learning_graph.graph_traversal import RecoveryPath
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.student_digital_twin.knowledge_gap import GapSeverity, KnowledgeGap
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.observation import Observation
from app.domain.student_digital_twin.recommendation import (
    Recommendation,
    RecommendationPriority,
)

_GAP_POINTS = {
    GapSeverity.CRITICAL: 40.0,
    GapSeverity.HIGH: 32.0,
    GapSeverity.MEDIUM: 22.0,
    GapSeverity.LOW: 12.0,
}

_REC_POINTS = {
    RecommendationPriority.CRITICAL: 30.0,
    RecommendationPriority.HIGH: 24.0,
    RecommendationPriority.MEDIUM: 16.0,
    RecommendationPriority.LOW: 8.0,
}


@dataclass(frozen=True)
class MissionCandidate:
    """A prioritisation candidate derived from Twin / Graph decisions."""

    candidate_id: str
    concept_id: str
    concept_title: str
    recommendation: Recommendation | None
    gap: KnowledgeGap | None
    recovery_path: RecoveryPath | None
    priority_score: MissionPriorityScore
    evidence_ids: tuple[str, ...] = ()

    @property
    def priority(self) -> MissionPriority:
        return self.priority_score.priority


@dataclass(frozen=True)
class PrioritisationResult:
    """Deterministic ranking of mission candidates for one day."""

    candidates: tuple[MissionCandidate, ...]
    selected: MissionCandidate | None
    explanation: str

    @property
    def ranked_concept_ids(self) -> tuple[str, ...]:
        return tuple(c.concept_id for c in self.candidates)


def prioritise_candidates(
    *,
    recommendations: tuple[Recommendation, ...],
    gaps: tuple[KnowledgeGap, ...],
    learning_state: LearningState,
    observations: tuple[Observation, ...] = (),
    learning_graph: LearningGraph | None = None,
    computed_at: datetime | None = None,
) -> PrioritisationResult:
    """Rank candidates from educational decisions (no reasoning performed)."""
    gaps_by_id = {g.gap_id: g for g in gaps}
    gaps_by_concept = {g.concept_id: g for g in gaps}
    recent = _recently_studied_concepts(observations, computed_at=computed_at)

    candidates: list[MissionCandidate] = []
    seen_concepts: set[str] = set()

    active_recs = tuple(
        r for r in recommendations if (r.status or "active") == "active"
    )
    ordered_recs = sorted(
        active_recs,
        key=lambda r: (
            -_REC_POINTS.get(r.priority, 0.0),
            r.recommendation_id,
        ),
    )

    for rec in ordered_recs:
        concept_id = (rec.curriculum_entity_id or "").strip()
        if not concept_id or concept_id in seen_concepts:
            continue
        seen_concepts.add(concept_id)
        gap = None
        if rec.related_gap_id:
            gap = gaps_by_id.get(rec.related_gap_id)
        if gap is None:
            gap = gaps_by_concept.get(concept_id)
        recovery = _recovery_for(concept_id, learning_graph)
        score = _score_candidate(
            recommendation=rec,
            gap=gap,
            learning_state=learning_state,
            recovery=recovery,
            recently_studied=concept_id in recent,
        )
        evidence = tuple(
            dict.fromkeys(
                list(rec.supporting_evidence)
                + list(gap.supporting_evidence if gap else ())
            )
        )
        candidates.append(
            MissionCandidate(
                candidate_id=f"cand-{rec.recommendation_id}",
                concept_id=concept_id,
                concept_title=_title_for(rec, gap, concept_id),
                recommendation=rec,
                gap=gap,
                recovery_path=recovery,
                priority_score=score,
                evidence_ids=evidence,
            )
        )

    for gap in sorted(
        gaps,
        key=lambda g: (-_GAP_POINTS.get(g.severity, 0.0), g.gap_id),
    ):
        if gap.concept_id in seen_concepts:
            continue
        seen_concepts.add(gap.concept_id)
        recovery = _recovery_for(gap.concept_id, learning_graph)
        score = _score_candidate(
            recommendation=None,
            gap=gap,
            learning_state=learning_state,
            recovery=recovery,
            recently_studied=gap.concept_id in recent,
        )
        candidates.append(
            MissionCandidate(
                candidate_id=f"cand-{gap.gap_id}",
                concept_id=gap.concept_id,
                concept_title=gap.concept_title or gap.concept_id,
                recommendation=None,
                gap=gap,
                recovery_path=recovery,
                priority_score=score,
                evidence_ids=tuple(gap.supporting_evidence),
            )
        )

    ranked = tuple(
        sorted(
            candidates,
            key=lambda c: (
                -c.priority_score.score,
                c.concept_id,
                c.candidate_id,
            ),
        )
    )
    selected = ranked[0] if ranked else None
    if selected is None:
        explanation = (
            "No educational decisions available for mission prioritisation. "
            "Run Educational Reasoning before generating a mission."
        )
    else:
        explanation = (
            f"Selected {selected.concept_id!r} "
            f"(score={selected.priority_score.score:.1f}, "
            f"priority={selected.priority.value}): "
            f"{selected.priority_score.explanation}"
        )
    return PrioritisationResult(
        candidates=ranked,
        selected=selected,
        explanation=explanation,
    )


def _score_candidate(
    *,
    recommendation: Recommendation | None,
    gap: KnowledgeGap | None,
    learning_state: LearningState,
    recovery: RecoveryPath | None,
    recently_studied: bool,
) -> MissionPriorityScore:
    gap_points = _GAP_POINTS.get(gap.severity, 0.0) if gap else 0.0
    rec_points = (
        _REC_POINTS.get(recommendation.priority, 0.0) if recommendation else 0.0
    )

    # Prefer missions when readiness is lower (more educational urgency).
    readiness = float(learning_state.exam_readiness or 0.0)
    readiness_points = round((1.0 - readiness) * 12.0, 4)

    # Positive momentum slightly boosts impact of practice over recovery.
    momentum = float(learning_state.momentum or 0.0)
    momentum_points = round(momentum * 6.0, 4)

    # Low confidence increases priority of recovery / reinforcement.
    confidence = float(learning_state.confidence or 0.0)
    if gap is not None:
        confidence = min(confidence, float(gap.confidence or confidence))
    confidence_points = round((1.0 - confidence) * 8.0, 4)

    # Shorter recovery paths are more actionable for a single daily session.
    recovery_path_points = 0.0
    if recovery is not None and recovery.concept_ids:
        # Prefer 1–3 hop recoveries; deeper chains still matter but score less.
        hops = max(0, recovery.length - 1)
        recovery_path_points = max(2.0, 10.0 - hops * 2.0)

    # Avoid repeating the same concept studied very recently (deterministic).
    recent_history_points = -8.0 if recently_studied else 4.0

    score = (
        gap_points
        + rec_points
        + readiness_points
        + momentum_points
        + confidence_points
        + recovery_path_points
        + recent_history_points
    )
    priority = priority_from_score(score)
    parts = [
        f"gap={gap_points:.1f}",
        f"recommendation={rec_points:.1f}",
        f"readiness={readiness_points:.1f}",
        f"momentum={momentum_points:.1f}",
        f"confidence={confidence_points:.1f}",
        f"recovery={recovery_path_points:.1f}",
        f"history={recent_history_points:.1f}",
    ]
    explanation = (
        "Deterministic priority from Twin decisions and Learning Graph "
        f"structure ({'; '.join(parts)})."
    )
    return MissionPriorityScore(
        score=round(score, 4),
        priority=priority,
        gap_severity_points=gap_points,
        recommendation_points=rec_points,
        readiness_points=readiness_points,
        momentum_points=momentum_points,
        confidence_points=confidence_points,
        recovery_path_points=recovery_path_points,
        recent_history_points=recent_history_points,
        explanation=explanation,
    )


def _recovery_for(
    concept_id: str,
    learning_graph: LearningGraph | None,
) -> RecoveryPath | None:
    if learning_graph is None:
        return None
    if learning_graph.get_node(concept_id) is None and not learning_graph.edges:
        return None
    return learning_graph.recovery_path(concept_id)


def _recently_studied_concepts(
    observations: tuple[Observation, ...],
    *,
    computed_at: datetime | None,
    window_hours: int = 36,
) -> set[str]:
    if not observations:
        return set()
    anchor = computed_at or max(
        (o.recorded_at for o in observations if o.recorded_at is not None),
        default=None,
    )
    if anchor is None:
        return set()
    cutoff = anchor - timedelta(hours=window_hours)
    recent: set[str] = set()
    for obs in observations:
        if obs.recorded_at is None or obs.recorded_at < cutoff:
            continue
        entity = (obs.curriculum_entity_id or "").strip()
        if entity:
            recent.add(entity)
    return recent


def _title_for(
    rec: Recommendation,
    gap: KnowledgeGap | None,
    concept_id: str,
) -> str:
    if gap and gap.concept_title:
        return gap.concept_title
    if rec.title:
        return rec.title
    return concept_id

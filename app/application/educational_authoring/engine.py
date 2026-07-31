"""Educational Authoring Engine — Educational Experience Phase 2 (KWP-015).

Transforms Curriculum, Objectives, Knowledge Graph relationships, and
Educational Intelligence signals into Learning Episodes and Mission
composition.

Owns educational composition only. Never modifies Strategy, Diagnostics,
Difficulty, Evidence, Progress, Forecast, Memory, Knowledge Architecture
graphs, Adaptive Workspace engines, or Mission Runtime.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.educational_authoring.composition import compose_mission
from app.application.educational_authoring.dto import (
    AuthoringContext,
    EducationalAuthoringSnapshot,
    LearningEpisode,
    MissionComposition,
)
from app.application.educational_authoring.episode import build_learning_episode
from app.application.educational_authoring.guidance import scrub
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.value_objects.dependency_type import DependencyType

logger = logging.getLogger(__name__)

_engine: EducationalAuthoringEngine | None = None


class EducationalAuthoringEngine:
    """Deterministic educational composition over curriculum-aligned inputs."""

    AUTHORITY_ID = "educational_authoring_engine"
    AUTHORITY_VERSION = "1.0.0"

    def __init__(self, graph: CurriculumGraph | None = None) -> None:
        self._graph = graph

    @property
    def graph(self) -> CurriculumGraph | None:
        return self._graph

    def with_graph(self, graph: CurriculumGraph | None) -> EducationalAuthoringEngine:
        return EducationalAuthoringEngine(graph)

    def author_episode(self, context: AuthoringContext) -> LearningEpisode:
        """Compose a single Learning Episode."""
        enriched = self._enrich_from_graph(context)
        return build_learning_episode(enriched)

    def author_mission(self, context: AuthoringContext) -> MissionComposition:
        """Compose a full Mission arc (episodes + tomorrow + extra study)."""
        enriched = self._enrich_from_graph(context)
        return compose_mission(enriched)

    def author_from_topic(
        self,
        *,
        topic_id: str = "",
        topic_title: str = "",
        topic_code: str = "",
        objective_text: str = "",
        objective_ids: tuple[str, ...] = (),
        concept_titles: tuple[str, ...] = (),
        estimated_effort_minutes: int = 0,
        difficulty_band: str = "",
        student_pace_factor: float = 1.0,
        previous_evidence_minutes: int = 0,
        weak_topic: bool = False,
        available_minutes: int | None = None,
        tomorrow_topic_id: str = "",
        tomorrow_topic_title: str = "",
        tomorrow_topic_code: str = "",
        tomorrow_effort_minutes: int = 0,
        recently_strengthened_titles: tuple[str, ...] = (),
        revision_available: bool = False,
        mission_instance_id: str = "",
        subject_code: str = "",
    ) -> MissionComposition:
        """Convenience entry for Adaptive Workspace / Home composition."""
        context = AuthoringContext(
            topic_id=topic_id,
            topic_title=topic_title,
            topic_code=topic_code,
            objective_text=objective_text,
            objective_ids=objective_ids,
            concept_titles=concept_titles,
            estimated_effort_minutes=estimated_effort_minutes,
            difficulty_band=difficulty_band,
            student_pace_factor=student_pace_factor,
            previous_evidence_minutes=previous_evidence_minutes,
            weak_topic=weak_topic,
            available_minutes=available_minutes,
            tomorrow_topic_id=tomorrow_topic_id,
            tomorrow_topic_title=tomorrow_topic_title,
            tomorrow_topic_code=tomorrow_topic_code,
            tomorrow_effort_minutes=tomorrow_effort_minutes,
            recently_strengthened_titles=recently_strengthened_titles,
            revision_available=revision_available,
            mission_instance_id=mission_instance_id,
            subject_code=subject_code,
        )
        return self.author_mission(context)

    def snapshot(
        self,
        composition: MissionComposition | None = None,
        *,
        subject_label: str = "",
        event_counts: dict[str, int] | None = None,
    ) -> EducationalAuthoringSnapshot:
        """Founder / diagnostics snapshot of authored output."""
        if composition is None or not composition.has_composition:
            return EducationalAuthoringSnapshot(
                subject_label=subject_label,
                event_counts=dict(event_counts or {}),
            )
        kinds: list[str] = []
        for ep in composition.episodes:
            for act in ep.activities:
                kinds.append(act.kind.value)
        return EducationalAuthoringSnapshot(
            episode_count=len(composition.episodes),
            total_duration_minutes=composition.total_duration_minutes,
            activity_kinds=tuple(dict.fromkeys(kinds)),
            has_tomorrow_preview=bool(
                composition.tomorrow_preview
                and composition.tomorrow_preview.has_preview
            ),
            extra_study_kinds=tuple(o.kind.value for o in composition.extra_study),
            alignment_codes=composition.alignment_codes,
            subject_label=subject_label,
            event_counts=dict(event_counts or {}),
        )

    def _enrich_from_graph(self, context: AuthoringContext) -> AuthoringContext:
        """Fill prerequisite / successor / foundation titles from KA graph."""
        graph = self._graph
        if graph is None:
            return context

        topic_id = (context.topic_id or "").strip()
        title = scrub(context.topic_title)
        if not topic_id and title:
            for node in graph.nodes():
                if node.name.strip().lower() == title.lower():
                    topic_id = node.topic_id.value
                    break
        if not topic_id or not graph.has_topic(topic_id):
            return context

        node = graph.get_node(topic_id)
        resolved_title = scrub(node.name if node else title) or title
        effort = context.estimated_effort_minutes
        difficulty = context.difficulty_band
        if node is not None:
            if effort <= 0:
                effort = int(node.estimated_effort_minutes or 0)
            if not difficulty:
                difficulty = str(node.difficulty.value if node.difficulty else "")

        prereq_titles = context.prerequisite_titles or tuple(
            _node_title(graph, p.value) for p in graph.find_prerequisites(topic_id)
        )
        foundation_titles = context.foundation_titles or tuple(
            _node_title(graph, n.value)
            for n in graph.neighbours(
                topic_id,
                dependency_type=DependencyType.FOUNDATION,
                direction="out",
            )
        )
        # Soft high-dependency foundations also inform educational context.
        if not foundation_titles:
            foundation_titles = tuple(
                _node_title(graph, n.value)
                for n in graph.neighbours(
                    topic_id,
                    dependency_type=DependencyType.HIGH_DEPENDENCY,
                    direction="out",
                )
            )
        successor_titles = context.successor_titles or tuple(
            _node_title(graph, s.value) for s in graph.find_successors(topic_id)[:4]
        )

        tomorrow_id = (context.tomorrow_topic_id or "").strip()
        tomorrow_title = scrub(context.tomorrow_topic_title)
        tomorrow_effort = context.tomorrow_effort_minutes
        if not tomorrow_title and successor_titles:
            tomorrow_title = successor_titles[0]
            if not tomorrow_id:
                successors = graph.find_successors(topic_id)
                if successors:
                    tomorrow_id = successors[0].value
        if tomorrow_id and graph.has_topic(tomorrow_id) and tomorrow_effort <= 0:
            tnode = graph.get_node(tomorrow_id)
            if tnode is not None:
                tomorrow_effort = int(tnode.estimated_effort_minutes or 0)
                if not tomorrow_title:
                    tomorrow_title = scrub(tnode.name)

        concept_titles = context.concept_titles
        if not concept_titles:
            # Ordered concept focus from foundations → topic (no fabrication).
            concepts = list(foundation_titles[:2]) + list(prereq_titles[:2])
            if resolved_title:
                concepts.append(resolved_title)
            concept_titles = tuple(dict.fromkeys(c for c in concepts if c))

        return AuthoringContext(
            topic_id=topic_id,
            topic_title=resolved_title,
            topic_code=context.topic_code,
            objective_text=context.objective_text,
            objective_ids=context.objective_ids,
            concept_titles=concept_titles,
            prerequisite_titles=tuple(t for t in prereq_titles if t),
            successor_titles=tuple(t for t in successor_titles if t),
            foundation_titles=tuple(t for t in foundation_titles if t),
            estimated_effort_minutes=effort,
            difficulty_band=difficulty,
            student_pace_factor=context.student_pace_factor,
            previous_evidence_minutes=context.previous_evidence_minutes,
            weak_topic=context.weak_topic,
            available_minutes=context.available_minutes,
            tomorrow_topic_id=tomorrow_id,
            tomorrow_topic_title=tomorrow_title,
            tomorrow_topic_code=context.tomorrow_topic_code,
            tomorrow_effort_minutes=tomorrow_effort,
            recently_strengthened_titles=context.recently_strengthened_titles,
            revision_available=context.revision_available,
            mission_instance_id=context.mission_instance_id,
            subject_code=context.subject_code,
        )


def _node_title(graph: CurriculumGraph, topic_id: str) -> str:
    node = graph.get_node(topic_id)
    return scrub(node.name if node else topic_id)


def get_educational_authoring_engine(
    graph: CurriculumGraph | None = None,
) -> EducationalAuthoringEngine:
    """Process-local Educational Authoring engine (optional graph)."""
    global _engine
    if graph is not None:
        return EducationalAuthoringEngine(graph)
    if _engine is None:
        _engine = EducationalAuthoringEngine()
    return _engine


def reset_educational_authoring_engine() -> None:
    """Test helper — clear process-local engine."""
    global _engine
    _engine = None


def authoring_context_from_mapping(data: dict[str, Any] | None) -> AuthoringContext:
    """Build AuthoringContext from a plain mapping (tests / adapters)."""
    raw = data or {}
    available = raw.get("available_minutes")
    return AuthoringContext(
        topic_id=str(raw.get("topic_id") or ""),
        topic_title=str(raw.get("topic_title") or ""),
        topic_code=str(raw.get("topic_code") or ""),
        objective_text=str(raw.get("objective_text") or ""),
        objective_ids=tuple(str(x) for x in (raw.get("objective_ids") or ())),
        concept_titles=tuple(str(x) for x in (raw.get("concept_titles") or ())),
        prerequisite_titles=tuple(
            str(x) for x in (raw.get("prerequisite_titles") or ())
        ),
        successor_titles=tuple(str(x) for x in (raw.get("successor_titles") or ())),
        foundation_titles=tuple(str(x) for x in (raw.get("foundation_titles") or ())),
        estimated_effort_minutes=int(raw.get("estimated_effort_minutes") or 0),
        difficulty_band=str(raw.get("difficulty_band") or ""),
        student_pace_factor=float(raw.get("student_pace_factor") or 1.0),
        previous_evidence_minutes=int(raw.get("previous_evidence_minutes") or 0),
        weak_topic=bool(raw.get("weak_topic") or False),
        available_minutes=int(available) if available is not None else None,
        tomorrow_topic_id=str(raw.get("tomorrow_topic_id") or ""),
        tomorrow_topic_title=str(raw.get("tomorrow_topic_title") or ""),
        tomorrow_topic_code=str(raw.get("tomorrow_topic_code") or ""),
        tomorrow_effort_minutes=int(raw.get("tomorrow_effort_minutes") or 0),
        recently_strengthened_titles=tuple(
            str(x) for x in (raw.get("recently_strengthened_titles") or ())
        ),
        revision_available=bool(raw.get("revision_available") or False),
        mission_instance_id=str(raw.get("mission_instance_id") or ""),
        subject_code=str(raw.get("subject_code") or ""),
    )

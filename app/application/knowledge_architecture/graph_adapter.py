"""Build CurriculumGraph from certified learner packages / topic specs (KWP-014).

Reuses GraphBuilder and existing topic prerequisite_ids. Does not invent
topic metadata or migrate Educational Intelligence logic.
"""

from __future__ import annotations

from typing import Any

from app.domain.curriculum.entities.dependency import Dependency
from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.graph.graph_builder import GraphBuilder
from app.domain.curriculum.graph.graph_node import GraphNode
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_difficulty import TopicDifficulty


def graph_from_topic_specs(
    topics: list[dict[str, Any]] | tuple[dict[str, Any], ...],
) -> CurriculumGraph:
    """Build a CurriculumGraph from lightweight topic dictionaries.

    Expected keys per topic: ``topic_id``, ``title`` / ``name``, optional
    ``difficulty``, ``estimated_minutes``, ``prerequisite_ids``.
    Soft links may appear as ``revision_with``, ``foundation_of``,
    ``extension_of``, ``high_dependency_on``, ``optional_reinforcement``.
    """
    nodes: list[Topic] = []
    deps: list[Dependency] = []
    dep_i = 0
    seen_ids: set[str] = set()

    for raw in topics:
        if not isinstance(raw, dict):
            continue
        tid = str(raw.get("topic_id") or raw.get("id") or "").strip()
        title = str(raw.get("title") or raw.get("name") or tid).strip()
        if not tid or tid in seen_ids:
            continue
        seen_ids.add(tid)
        difficulty = _difficulty(raw.get("difficulty"))
        minutes = int(raw.get("estimated_minutes") or raw.get("minutes") or 0)
        nodes.append(
            Topic.create(
                tid,
                title,
                difficulty=difficulty,
                estimated_effort_minutes=max(0, minutes),
            )
        )

    id_set = {t.topic_id.value for t in nodes}

    for raw in topics:
        if not isinstance(raw, dict):
            continue
        tid = str(raw.get("topic_id") or raw.get("id") or "").strip()
        if tid not in id_set:
            continue
        for prereq in tuple(raw.get("prerequisite_ids") or ()):
            pid = str(prereq).strip()
            if pid and pid in id_set and pid != tid:
                dep_i += 1
                deps.append(
                    Dependency.create(
                        f"req-{dep_i}",
                        tid,
                        pid,
                        DependencyType.REQUIRES,
                        rationale="Certified syllabus prerequisite",
                    )
                )
        dep_i = _soft_links(
            deps,
            dep_i,
            tid,
            id_set,
            raw.get("revision_with"),
            DependencyType.REVISION,
            "Frequently revised together",
        )
        dep_i = _soft_links(
            deps,
            dep_i,
            tid,
            id_set,
            raw.get("foundation_of") or raw.get("foundation_ids"),
            DependencyType.FOUNDATION,
            "Foundation relationship",
        )
        dep_i = _soft_links(
            deps,
            dep_i,
            tid,
            id_set,
            raw.get("extension_of") or raw.get("extension_ids"),
            DependencyType.EXTENSION,
            "Extension relationship",
        )
        dep_i = _soft_links(
            deps,
            dep_i,
            tid,
            id_set,
            raw.get("high_dependency_on"),
            DependencyType.HIGH_DEPENDENCY,
            "High dependency",
        )
        dep_i = _soft_links(
            deps,
            dep_i,
            tid,
            id_set,
            raw.get("optional_reinforcement"),
            DependencyType.OPTIONAL,
            "Optional reinforcement",
        )

    return GraphBuilder().build_from_topics(nodes, dependencies=deps)


def graph_from_learner_package(package: dict[str, Any] | None) -> CurriculumGraph:
    """Project a certified published package into a topic CurriculumGraph.

    Reuses EducationalArtefactDeriver topic prerequisite_ids — no new
    curriculum authorship.
    """
    if not isinstance(package, dict) or not package:
        return CurriculumGraph()
    try:
        from app.domain.educational_engine_foundation.derivation import (
            EducationalArtefactDeriver,
        )

        bundle = EducationalArtefactDeriver().derive(package)
    except Exception:  # noqa: BLE001 — soft-fail empty graph
        return CurriculumGraph()

    specs: list[dict[str, Any]] = []
    for topic in bundle.topics:
        specs.append(
            {
                "topic_id": topic.topic_id,
                "title": topic.title,
                "difficulty": topic.difficulty or "foundational",
                "estimated_minutes": int(topic.estimated_minutes or 0),
                "prerequisite_ids": tuple(topic.prerequisite_ids or ()),
            }
        )
    return graph_from_topic_specs(specs)


def graph_from_curriculum_graph(graph: CurriculumGraph) -> CurriculumGraph:
    """Identity helper — accept an already-built CurriculumGraph."""
    return graph


def ensure_topic_node(
    graph: CurriculumGraph,
    topic_id: str,
    title: str,
    *,
    difficulty: str = "foundational",
) -> None:
    """Add a missing topic node when wiring overlays (tests / soft fill)."""
    if graph.has_topic(topic_id):
        return
    graph.add_topic(
        GraphNode.create(
            topic_id,
            title or topic_id,
            difficulty=_difficulty(difficulty),
        )
    )


def _soft_links(
    deps: list[Dependency],
    dep_i: int,
    source_id: str,
    id_set: set[str],
    raw_targets: Any,
    dependency_type: DependencyType,
    rationale: str,
) -> int:
    if raw_targets is None:
        return dep_i
    if isinstance(raw_targets, str | bytes):
        targets = (str(raw_targets),)
    else:
        targets = tuple(raw_targets)
    for target in targets:
        tid = str(target).strip()
        if not tid or tid not in id_set or tid == source_id:
            continue
        dep_i += 1
        deps.append(
            Dependency.create(
                f"{dependency_type.value}-{dep_i}",
                source_id,
                tid,
                dependency_type,
                rationale=rationale,
            )
        )
    return dep_i


def _difficulty(raw: Any) -> TopicDifficulty:
    text = str(raw or "foundational").strip().lower()
    try:
        return TopicDifficulty(text)
    except ValueError:
        return TopicDifficulty.FOUNDATIONAL

"""Curriculum pathways — ordered educational routes (KWP-014).

Derives from Curriculum LearningPath entities and REQUIRES topology.
Curriculum-specific only — no AI generation.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import CurriculumPathway
from app.domain.curriculum.entities.curriculum import Curriculum
from app.domain.curriculum.entities.learning_path import LearningPath
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph


def pathways_from_curriculum(
    curriculum: Curriculum | None,
    graph: CurriculumGraph,
) -> tuple[CurriculumPathway, ...]:
    """Project named LearningPath entities plus a default topological path."""
    paths: list[CurriculumPathway] = []
    if curriculum is not None:
        for path in curriculum.learning_paths:
            paths.append(_from_learning_path(path, graph))
    if not paths:
        topo = _topological_pathway(graph)
        if topo is not None:
            paths.append(topo)
    return tuple(paths)


def pathways_from_graph(
    graph: CurriculumGraph,
    *,
    named_paths: list[LearningPath] | tuple[LearningPath, ...] | None = None,
) -> tuple[CurriculumPathway, ...]:
    """Build pathways from optional named paths or topological order."""
    paths: list[CurriculumPathway] = []
    for path in named_paths or ():
        paths.append(_from_learning_path(path, graph))
    if not paths:
        topo = _topological_pathway(graph)
        if topo is not None:
            paths.append(topo)
    return tuple(paths)


def pathway_containing(
    pathways: tuple[CurriculumPathway, ...] | list[CurriculumPathway],
    topic_id: str,
) -> CurriculumPathway | None:
    """Return the first pathway that includes ``topic_id``."""
    tid = (topic_id or "").strip()
    if not tid:
        return None
    for path in pathways:
        if tid in path.topic_ids:
            return path
    return None


def chain_from_topic(
    graph: CurriculumGraph,
    topic_id: str,
    *,
    max_depth: int = 8,
) -> CurriculumPathway | None:
    """Build a local chain: prerequisites → topic → successors (deterministic)."""
    tid = (topic_id or "").strip()
    if not tid or not graph.has_topic(tid):
        return None
    ancestors = list(graph.all_prerequisites(tid, transitive=True))
    # Order ancestors by topological position when possible.
    try:
        topo = {t.value: i for i, t in enumerate(graph.topological_ordering())}
        ancestors.sort(key=lambda t: topo.get(t.value, 10_000))
    except ValueError:
        ancestors.sort(key=lambda t: t.value)

    successors = list(graph.find_successors(tid))
    chain_ids = [a.value for a in ancestors[-max_depth:]] + [tid]
    for succ in successors[: max(0, max_depth - 1)]:
        if succ.value not in chain_ids:
            chain_ids.append(succ.value)

    titles = [_title(graph, x) for x in chain_ids]
    return CurriculumPathway(
        path_id=f"chain:{tid}",
        name=f"Pathway through {_title(graph, tid)}",
        topic_ids=tuple(chain_ids),
        topic_titles=tuple(titles),
        description="Curriculum dependency chain from published relationships.",
    )


def _from_learning_path(
    path: LearningPath, graph: CurriculumGraph
) -> CurriculumPathway:
    ids = tuple(t.value for t in path.topic_ids)
    titles = tuple(_title(graph, tid) for tid in ids)
    return CurriculumPathway(
        path_id=path.path_id,
        name=path.name,
        topic_ids=ids,
        topic_titles=titles,
        description=(path.description or "").strip(),
    )


def _topological_pathway(graph: CurriculumGraph) -> CurriculumPathway | None:
    if graph.topic_count() == 0:
        return None
    try:
        ordered = graph.topological_ordering()
    except ValueError:
        ordered = tuple(n.topic_id for n in graph.nodes())
    ids = tuple(t.value for t in ordered)
    return CurriculumPathway(
        path_id="topo:syllabus",
        name="Syllabus study order",
        topic_ids=ids,
        topic_titles=tuple(_title(graph, tid) for tid in ids),
        description="Deterministic topological order under prerequisites.",
    )


def _title(graph: CurriculumGraph, topic_id: str) -> str:
    node = graph.get_node(topic_id)
    return node.name if node else topic_id

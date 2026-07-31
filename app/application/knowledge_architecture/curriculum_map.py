"""Curriculum Map — visual learning map projection (KWP-014).

Students see where today's topic sits inside the qualification with
completed / current / future / weak-prerequisite highlights.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import (
    MAP_STATUS_TITLES,
    CurriculumMap,
    CurriculumMapNode,
    CurriculumPathway,
    LearnerGraphContext,
    MapTopicStatus,
)
from app.application.knowledge_architecture.pathways import (
    chain_from_topic,
    pathway_containing,
    pathways_from_graph,
)
from app.application.knowledge_architecture.prerequisite_reasoning import (
    why_topic_matters,
)
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph


def build_curriculum_map(
    graph: CurriculumGraph,
    *,
    context: LearnerGraphContext | None = None,
    subject_label: str = "",
    pathways: tuple[CurriculumPathway, ...] | None = None,
) -> CurriculumMap:
    """Project a student Curriculum Map from curriculum structure + learner overlay."""
    if graph.topic_count() == 0:
        return CurriculumMap(
            subject_label=subject_label,
            empty_reason=(
                "Your curriculum map appears when syllabus topics are available."
            ),
            has_map=False,
        )

    ctx = context or LearnerGraphContext()
    current = (ctx.current_topic_id or "").strip()
    if current and not graph.has_topic(current):
        current = ""

    path_set = pathways if pathways is not None else pathways_from_graph(graph)
    active_path = pathway_containing(path_set, current) if current else None
    if active_path is None and current:
        active_path = chain_from_topic(graph, current)
    if active_path is None and path_set:
        active_path = path_set[0]

    try:
        ordered = graph.topological_ordering()
    except ValueError:
        ordered = tuple(n.topic_id for n in graph.nodes())

    # Prefer pathway order when available.
    display_ids: list[str] = []
    if active_path is not None:
        display_ids.extend(active_path.topic_ids)
    for tid in ordered:
        if tid.value not in display_ids:
            display_ids.append(tid.value)

    nodes: list[CurriculumMapNode] = []
    for tid in display_ids:
        if not graph.has_topic(tid):
            continue
        node = graph.get_node(tid)
        title = node.name if node else tid
        difficulty = node.difficulty.value if node else "foundational"
        status = _status(tid, ctx, graph)
        prereq_titles = tuple(
            _title(graph, p.value) for p in graph.find_prerequisites(tid)
        )
        nodes.append(
            CurriculumMapNode(
                topic_id=tid,
                title=title,
                status=status,
                status_label=MAP_STATUS_TITLES[status],
                difficulty=difficulty,
                prerequisite_titles=prereq_titles,
                is_current=tid == current,
            )
        )

    current_title = ""
    why = ""
    if current:
        current_title = _title(graph, current)
        why = why_topic_matters(graph, current, context=ctx)

    edge_count = graph.edge_count()
    return CurriculumMap(
        subject_label=subject_label,
        current_topic_id=current,
        current_topic_title=current_title,
        nodes=tuple(nodes),
        pathway=active_path,
        why_current_matters=why,
        node_count=len(nodes),
        edge_count=edge_count,
        has_map=True,
    )


def _status(
    topic_id: str,
    ctx: LearnerGraphContext,
    graph: CurriculumGraph,
) -> MapTopicStatus:
    if topic_id == (ctx.current_topic_id or "").strip():
        return MapTopicStatus.CURRENT
    if topic_id in ctx.weak_topic_ids:
        # Weak prerequisite of current?
        current = (ctx.current_topic_id or "").strip()
        if current and graph.has_topic(current):
            prereqs = {p.value for p in graph.all_prerequisites(current)}
            if topic_id in prereqs:
                return MapTopicStatus.WEAK_PREREQUISITE
        return MapTopicStatus.ATTENTION
    if topic_id in ctx.completed_topic_ids:
        return MapTopicStatus.COMPLETED
    current = (ctx.current_topic_id or "").strip()
    if current and graph.has_topic(current):
        prereqs = {p.value for p in graph.all_prerequisites(current)}
        if topic_id in prereqs and topic_id not in ctx.completed_topic_ids:
            return MapTopicStatus.WEAK_PREREQUISITE
    return MapTopicStatus.FUTURE


def _title(graph: CurriculumGraph, topic_id: str) -> str:
    node = graph.get_node(topic_id)
    return node.name if node else topic_id

"""Difficulty propagation through prerequisite links (KWP-014).

Example: repeated weakness in Interest Theory increases educational
attention on Annuities, Loans, and Bonds before deterioration appears.

Uses CurriculumGraph successors — does not redesign Learning Difficulty.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import (
    DifficultyAttention,
    LearnerGraphContext,
)
from app.application.knowledge_architecture.guidance import scrub
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph


def propagate_difficulty_attention(
    graph: CurriculumGraph,
    *,
    context: LearnerGraphContext | None = None,
    source_topic_id: str = "",
    max_successors: int = 6,
) -> DifficultyAttention:
    """Propagate educational attention from a weak topic to its dependents."""
    ctx = context or LearnerGraphContext()
    source = (source_topic_id or "").strip()
    if not source:
        # Prefer the weak topic with the most dependents.
        best = ""
        best_count = -1
        for wid in sorted(ctx.weak_topic_ids):
            if not graph.has_topic(wid):
                continue
            count = len(graph.find_successors(wid))
            if count > best_count:
                best = wid
                best_count = count
        source = best

    if not source or not graph.has_topic(source):
        return DifficultyAttention(
            source_topic_id="",
            source_title="",
            has_attention=False,
        )

    source_node = graph.get_node(source)
    source_title = source_node.name if source_node else source
    if source not in ctx.weak_topic_ids and not source_topic_id:
        return DifficultyAttention(
            source_topic_id=source,
            source_title=source_title,
            has_attention=False,
        )

    direct = list(graph.find_successors(source))
    transitive = [
        s
        for s in graph.all_successors(source, transitive=True)
        if s not in direct
    ]
    ordered = direct + transitive
    attention_ids = [s.value for s in ordered[:max_successors]]
    # Skip already-completed successors when many exist — still surface some.
    incomplete = [
        tid for tid in attention_ids if tid not in ctx.completed_topic_ids
    ]
    if incomplete:
        attention_ids = incomplete
    titles = [_title(graph, tid) for tid in attention_ids]
    if not attention_ids:
        return DifficultyAttention(
            source_topic_id=source,
            source_title=source_title,
            has_attention=False,
        )

    if len(titles) == 1:
        focus_list = titles[0]
    elif len(titles) == 2:
        focus_list = f"{titles[0]} and {titles[1]}"
    else:
        focus_list = ", ".join(titles[:-1]) + f", and {titles[-1]}"

    guidance = scrub(
        f"Repeated weakness in {source_title} increases educational attention "
        f"on {focus_list} before deterioration appears."
    )
    return DifficultyAttention(
        source_topic_id=source,
        source_title=source_title,
        attention_topic_ids=tuple(attention_ids),
        attention_titles=tuple(titles),
        guidance=guidance,
        has_attention=True,
    )


def _title(graph: CurriculumGraph, topic_id: str) -> str:
    node = graph.get_node(topic_id)
    return node.name if node else topic_id

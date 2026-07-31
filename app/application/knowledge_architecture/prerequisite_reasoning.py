"""Prerequisite reasoning — explain why a topic matters (KWP-014).

Produces curriculum-grounded explanations such as:
"Bayes relies heavily on Conditional Probability. Strengthening
Conditional Probability is expected to improve your understanding of Bayes."

Never fabricates relationships outside the CurriculumGraph.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import (
    LearnerGraphContext,
    PrerequisiteExplanation,
)
from app.application.knowledge_architecture.guidance import scrub
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.value_objects.dependency_type import DependencyType


def explain_topic(
    graph: CurriculumGraph,
    topic_id: str,
    *,
    context: LearnerGraphContext | None = None,
) -> PrerequisiteExplanation:
    """Explain why ``topic_id`` matters using explicit graph relationships."""
    tid = (topic_id or "").strip()
    if not tid or not graph.has_topic(tid):
        return PrerequisiteExplanation(
            topic_id=tid,
            topic_title="",
            explanation="",
            has_explanation=False,
        )

    node = graph.get_node(tid)
    title = node.name if node else tid
    prereqs = graph.find_prerequisites(tid)
    high_deps = graph.neighbours(
        tid,
        dependency_type=DependencyType.HIGH_DEPENDENCY,
        direction="out",
    )
    foundations = graph.neighbours(
        tid,
        dependency_type=DependencyType.FOUNDATION,
        direction="out",
    )
    successors = graph.find_successors(tid)

    relies_titles: list[str] = []
    relies_ids: list[str] = []
    codes: list[str] = []

    # Prefer high-dependency / foundation when present; else hard prereqs.
    primary = tuple(high_deps) or tuple(foundations) or tuple(prereqs)
    for related in primary:
        related_node = graph.get_node(related)
        related_title = related_node.name if related_node else related.value
        relies_titles.append(related_title)
        relies_ids.append(related.value)
        codes.append(f"relies:{related.value}")

    strengthens_titles: list[str] = []
    for succ in successors[:4]:
        succ_node = graph.get_node(succ)
        strengthens_titles.append(succ_node.name if succ_node else succ.value)

    ctx = context or LearnerGraphContext()
    recently = {
        str(x).strip().lower() for x in ctx.recently_strengthened_ids if str(x).strip()
    }

    if not relies_titles and not strengthens_titles:
        explanation = (
            f"{title} is part of your syllabus pathway. "
            "Continue studying it in published order."
        )
        return PrerequisiteExplanation(
            topic_id=tid,
            topic_title=title,
            explanation=scrub(explanation),
            has_explanation=True,
            relationship_codes=("syllabus_position",),
        )

    parts: list[str] = []
    if relies_titles:
        if len(relies_titles) == 1:
            foundation = relies_titles[0]
            parts.append(f"{title} relies heavily on {foundation}.")
            parts.append(
                f"Strengthening {foundation} is expected to improve "
                f"your understanding of {title}."
            )
            if foundation.lower() in recently or any(
                r.lower() in recently for r in relies_ids
            ):
                parts.append(
                    f"Today's topic builds directly on {foundation}, "
                    "which you strengthened recently."
                )
        else:
            listed = ", ".join(relies_titles[:-1]) + f", and {relies_titles[-1]}"
            parts.append(f"{title} builds on {listed}.")
            parts.append(
                "Strengthening those foundations is expected to improve "
                f"your understanding of {title}."
            )

    if strengthens_titles and not parts:
        nxt = strengthens_titles[0]
        parts.append(
            f"{title} unlocks later work such as {nxt}."
        )
    elif strengthens_titles and len(parts) < 3:
        nxt = strengthens_titles[0]
        parts.append(f"It also prepares you for {nxt}.")

    return PrerequisiteExplanation(
        topic_id=tid,
        topic_title=title,
        explanation=scrub(" ".join(parts)),
        relies_on=tuple(relies_titles),
        strengthens=tuple(strengthens_titles),
        relationship_codes=tuple(codes) or ("prerequisite",),
        has_explanation=True,
    )


def why_topic_matters(
    graph: CurriculumGraph,
    topic_id: str,
    *,
    context: LearnerGraphContext | None = None,
) -> str:
    """Short curriculum-grounded answer to 'Why does this topic matter?'."""
    return explain_topic(graph, topic_id, context=context).explanation

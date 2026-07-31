"""Deterministic revision path engine (KWP-014).

Paths derive from existing curriculum relationships plus Educational
Intelligence signals (weak topics, recovery, exam proximity, mastery).
Does not redesign Strategy / Diagnostics / Difficulty / Memory engines.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import (
    REVISION_PATH_TITLES,
    LearnerGraphContext,
    RevisionPathKind,
    RevisionPathway,
)
from app.application.knowledge_architecture.guidance import scrub
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.services.revision_path_service import RevisionPathService
from app.domain.curriculum.value_objects.dependency_type import DependencyType


def generate_revision_paths(
    graph: CurriculumGraph,
    *,
    context: LearnerGraphContext | None = None,
    seed_topic_id: str = "",
    limit: int = 4,
) -> tuple[RevisionPathway, ...]:
    """Generate deterministic revision pathways for the learner context."""
    ctx = context or LearnerGraphContext()
    seed = (seed_topic_id or ctx.current_topic_id or "").strip()
    paths: list[RevisionPathway] = []

    weak_path = _weak_prerequisite_path(graph, ctx, seed)
    if weak_path is not None:
        paths.append(weak_path)

    recovery_path = _recovery_path(graph, ctx, seed)
    if recovery_path is not None:
        paths.append(recovery_path)

    exam_path = _exam_revision_path(graph, ctx, seed)
    if exam_path is not None:
        paths.append(exam_path)

    mastery_path = _mastery_reinforcement_path(graph, ctx, seed)
    if mastery_path is not None:
        paths.append(mastery_path)

    return tuple(paths[: max(0, limit)])


def _weak_prerequisite_path(
    graph: CurriculumGraph,
    ctx: LearnerGraphContext,
    seed: str,
) -> RevisionPathway | None:
    focus = seed
    if not focus or not graph.has_topic(focus):
        # Prefer a weak topic that has dependents.
        for wid in sorted(ctx.weak_topic_ids):
            if graph.has_topic(wid):
                focus = wid
                break
    if not focus or not graph.has_topic(focus):
        return None

    missing = [
        p
        for p in graph.all_prerequisites(focus, transitive=True)
        if p.value in ctx.weak_topic_ids or p.value not in ctx.completed_topic_ids
    ]
    # Prefer weak prerequisites first.
    weak_first = [p for p in missing if p.value in ctx.weak_topic_ids]
    other = [p for p in missing if p.value not in ctx.weak_topic_ids]
    ordered = weak_first + other
    if not ordered and focus not in ctx.weak_topic_ids:
        return None
    ids = [p.value for p in ordered] + (
        [focus] if focus not in {p.value for p in ordered} else []
    )
    if not ids:
        return None
    titles = [_title(graph, i) for i in ids]
    kind = RevisionPathKind.WEAK_PREREQUISITE
    return RevisionPathway(
        kind=kind,
        title=REVISION_PATH_TITLES[kind],
        topic_ids=tuple(ids),
        topic_titles=tuple(titles),
        rationale=scrub(
            "Strengthen weak prerequisites before continuing on the dependent topic."
        ),
        seed_topic_id=focus,
        evidence_codes=("weak_prerequisite", "requires"),
    )


def _recovery_path(
    graph: CurriculumGraph,
    ctx: LearnerGraphContext,
    seed: str,
) -> RevisionPathway | None:
    weak = sorted(x for x in ctx.weak_topic_ids if graph.has_topic(x))
    if not weak:
        return None
    focus = seed if seed in weak else weak[0]
    service = RevisionPathService(graph)
    try:
        cluster = service.recommended_review_sequence(
            focus, completed=set(ctx.completed_topic_ids)
        )
    except ValueError:
        cluster = ()
    ids = [t.value for t in cluster] if cluster else [focus]
    # Ensure weak topics appear early.
    weak_set = set(weak)
    ids = sorted(ids, key=lambda i: (0 if i in weak_set else 1, i))
    titles = [_title(graph, i) for i in ids]
    kind = RevisionPathKind.RECOVERY
    return RevisionPathway(
        kind=kind,
        title=REVISION_PATH_TITLES[kind],
        topic_ids=tuple(ids),
        topic_titles=tuple(titles),
        rationale=scrub(
            "Recover understanding along revision links and prerequisite support."
        ),
        seed_topic_id=focus,
        evidence_codes=("recovery", "revision"),
    )


def _exam_revision_path(
    graph: CurriculumGraph,
    ctx: LearnerGraphContext,
    seed: str,
) -> RevisionPathway | None:
    days = ctx.days_to_exam
    if days is None or days > 21:
        return None
    try:
        topo = graph.topological_ordering()
    except ValueError:
        topo = tuple(n.topic_id for n in graph.nodes())
    # Near exam: prioritise incomplete / weak topics late in the syllabus.
    incomplete = [
        t
        for t in topo
        if t.value not in ctx.completed_topic_ids or t.value in ctx.weak_topic_ids
    ]
    if seed and graph.has_topic(seed):
        seed_first = [t for t in incomplete if t.value == seed]
        rest = [t for t in incomplete if t.value != seed]
        incomplete = seed_first + rest
    ids = [t.value for t in incomplete[:8]]
    if not ids:
        return None
    titles = [_title(graph, i) for i in ids]
    kind = RevisionPathKind.EXAM_REVISION
    return RevisionPathway(
        kind=kind,
        title=REVISION_PATH_TITLES[kind],
        topic_ids=tuple(ids),
        topic_titles=tuple(titles),
        rationale=scrub(
            "Exam revision path prioritises remaining and weak syllabus topics."
        ),
        seed_topic_id=seed or (ids[0] if ids else ""),
        evidence_codes=("exam_proximity", "syllabus_order"),
    )


def _mastery_reinforcement_path(
    graph: CurriculumGraph,
    ctx: LearnerGraphContext,
    seed: str,
) -> RevisionPathway | None:
    focus = seed if seed and graph.has_topic(seed) else ""
    if not focus:
        for tid in sorted(ctx.completed_topic_ids):
            if graph.has_topic(tid):
                focus = tid
                break
    if not focus:
        return None

    # Completed prerequisites + optional/revision neighbours + focus.
    prereqs = [
        p.value
        for p in graph.find_prerequisites(focus)
        if p.value in ctx.completed_topic_ids
    ]
    revision = [
        n.value
        for n in graph.neighbours(
            focus, dependency_type=DependencyType.REVISION, direction="both"
        )
    ]
    optional = [
        n.value
        for n in graph.neighbours(
            focus, dependency_type=DependencyType.OPTIONAL, direction="out"
        )
    ]
    ids: list[str] = []
    for tid in prereqs + revision + optional + [focus]:
        if tid not in ids:
            ids.append(tid)
    if len(ids) < 2 and focus not in ctx.completed_topic_ids:
        return None
    titles = [_title(graph, i) for i in ids]
    kind = RevisionPathKind.MASTERY_REINFORCEMENT
    return RevisionPathway(
        kind=kind,
        title=REVISION_PATH_TITLES[kind],
        topic_ids=tuple(ids),
        topic_titles=tuple(titles),
        rationale=scrub(
            "Reinforce mastery by revisiting foundations and linked topics together."
        ),
        seed_topic_id=focus,
        evidence_codes=("mastery", "reinforcement"),
    )


def _title(graph: CurriculumGraph, topic_id: str) -> str:
    node = graph.get_node(topic_id)
    return node.name if node else topic_id

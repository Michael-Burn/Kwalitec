"""EQ-001-derived QualitySnapshot computation for EducationalNode graphs.

Replaces Phase A placeholder metrics with measurable educational vectors
compatible with RegressionGuard lexicographic gates.
Phase C adds evidence_quality and concept-aware granularity.
"""

from __future__ import annotations

from collections import Counter

from app.domain.curriculum_intelligence.content_role import (
    NON_CURRICULUM_ROLES,
    ContentRole,
)
from app.domain.curriculum_intelligence.evidence import evidence_grade_weight
from app.domain.curriculum_intelligence.generation import (
    EducationalNode,
    QualitySnapshot,
)

_CHAPTER_KINDS = frozenset({"chapter", "module"})
_SECTION_KINDS = frozenset({"section"})
_TOPIC_KINDS = frozenset({"topic", "subtopic", "concept"})
_OBJECTIVE_KINDS = frozenset({"learning_objective", "objective"})
_HIERARCHY_KINDS = (
    _CHAPTER_KINDS
    | _SECTION_KINDS
    | _TOPIC_KINDS
    | _OBJECTIVE_KINDS
    | {"subject"}
)
_REPORT_KINDS = frozenset({"coverage_report", "certification_report"})

_NOISE_ROLES = frozenset(r.value for r in NON_CURRICULUM_ROLES)


def compute_quality_snapshot(
    nodes: tuple[EducationalNode, ...] | list[EducationalNode],
    *,
    rejected_count: int | None = None,
    expected_chapters: int = 5,
    coverage_override: float | None = None,
) -> QualitySnapshot:
    """Build a QualitySnapshot from EducationalNode Curriculum Memory.

    Metrics follow EQ-001 audit intent + EI-001C evidence grading:
    - noise = front-matter / non-curriculum contamination in the *active* set
    - hierarchy = role-chain integrity + chapter-count proximity to syllabus
    - duplicates = duplicate-title rate among active hierarchy nodes
    - granularity = topic/concept coherence (rewards consolidation of fragments)
    - confidence = mean confidence of active *educational* nodes (noise roles
      excluded so Gen2 noise elimination is not punished for dropping chrome)
    - coverage = educational share + objective density (or Gen 6 override)
    - evidence_quality = mean Evidence Grade weight on active educational nodes
    """
    all_nodes = tuple(nodes)
    active = [n for n in all_nodes if n.active and n.kind not in _REPORT_KINDS]
    inactive = [n for n in all_nodes if not n.active]
    rejected = rejected_count if rejected_count is not None else len(inactive)

    chapters = sum(1 for n in active if n.kind in _CHAPTER_KINDS)
    sections = sum(1 for n in active if n.kind in _SECTION_KINDS)
    topics = sum(1 for n in active if n.kind in _TOPIC_KINDS)
    objectives = sum(1 for n in active if n.kind in _OBJECTIVE_KINDS)
    hierarchy_nodes = [n for n in active if n.kind in _HIERARCHY_KINDS]
    hier_total = max(len(hierarchy_nodes), 1)

    contaminated = sum(1 for n in active if (n.role or "") in _NOISE_ROLES)
    noise = round(contaminated / max(len(active), 1), 4) if active else 0.0

    title_counts = Counter(
        n.title.strip().lower() for n in hierarchy_nodes if n.title.strip()
    )
    dupes = sum(1 for _t, c in title_counts.items() if c > 1)
    duplicates = round(dupes / hier_total, 4)

    by_id = {n.node_id: n for n in active}
    orphan_refs = 0
    parent_ok = 0
    checked_parents = 0
    for node in hierarchy_nodes:
        if not node.parent_node_id:
            continue
        checked_parents += 1
        parent = by_id.get(node.parent_node_id)
        if parent is None or not parent.active:
            orphan_refs += 1
            continue
        if _parent_kind_ok(node.kind, parent.kind):
            parent_ok += 1

    chapter_proximity = 1.0 - min(
        abs(chapters - expected_chapters) / max(expected_chapters, 1), 1.0
    )
    if checked_parents:
        parent_integrity = parent_ok / checked_parents
    else:
        parent_integrity = 1.0 if hierarchy_nodes else 0.0
    orphan_penalty = orphan_refs / hier_total
    hierarchy = round(
        max(
            0.0,
            0.55 * parent_integrity
            + 0.35 * chapter_proximity
            - 0.45 * orphan_penalty,
        ),
        4,
    )

    # Granularity: prefer coherent concept density; reward duplicate reduction
    # and merge/split lineage signals over raw topic-count targets.
    merge_signals = sum(
        1
        for n in active
        if any(
            k == "concept_action" and v in {"merge", "split"}
            for k, v in n.attributes
        )
    )
    if topics == 0:
        granularity = 0.0 if chapters == 0 else 0.3
    elif 2 <= topics <= 250:
        base = 0.85 if topics < 10 else 0.9
        granularity = min(0.98, base + 0.02 * min(merge_signals, 5) - 0.3 * duplicates)
    else:
        granularity = max(0.0, 1.0 - (topics - 250) / 5000)
    granularity = round(max(0.0, granularity), 4)

    educational_active = [
        n
        for n in active
        if (n.role or ContentRole.EDUCATIONAL.value) not in _NOISE_ROLES
    ]
    # Confidence is scored on retained educational nodes only. Including
    # non-curriculum chrome inflated Gen1 means and falsely rejected Gen2
    # noise elimination when high-confidence front-matter was removed.
    confidence_nodes = educational_active or active
    confidences = [n.confidence.score for n in confidence_nodes]
    mean_conf = (
        round(sum(confidences) / len(confidences), 4) if confidences else 0.0
    )
    low_share = (
        round(sum(1 for c in confidences if c < 0.6) / len(confidences), 4)
        if confidences
        else 0.0
    )
    edu_share = len(educational_active) / max(len(active), 1) if active else 0.0
    obj_presence = min(objectives / max(expected_chapters * 10, 1), 1.0)
    coverage = round(0.65 * edu_share + 0.35 * obj_presence, 4)
    if coverage_override is not None:
        # Gen 6: blend syllabus completeness with structural educational share.
        coverage = round(0.7 * coverage_override + 0.3 * edu_share, 4)
    if not active:
        coverage = 0.0

    grade_weights = [
        evidence_grade_weight(n.evidence_grade)
        for n in educational_active
        if n.evidence_grade is not None
    ]
    if grade_weights:
        evidence_quality = round(sum(grade_weights) / len(grade_weights), 4)
    else:
        # Pre-grading generations: infer A for syllabus-ref nodes, else mid.
        inferred = []
        for n in educational_active:
            if n.lineage.syllabus_refs:
                inferred.append(1.0)
            elif n.provenance_id:
                inferred.append(0.75)
            else:
                inferred.append(0.25)
        evidence_quality = (
            round(sum(inferred) / len(inferred), 4) if inferred else 0.0
        )

    return QualitySnapshot(
        coverage=coverage,
        hierarchy=hierarchy,
        duplicates=duplicates,
        noise=noise,
        granularity=granularity,
        confidence=mean_conf,
        active_node_count=len(active),
        rejected_node_count=rejected,
        low_confidence_share=low_share,
        chapters=chapters,
        sections=sections,
        topics=topics,
        objectives=objectives,
        evidence_quality=evidence_quality,
    )


def _parent_kind_ok(child_kind: str, parent_kind: str) -> bool:
    """Subject → Chapter → Section → Topic/Concept → Learning Objective."""
    allowed: dict[str, frozenset[str]] = {
        "chapter": frozenset({"subject"}),
        "module": frozenset({"subject"}),
        "section": frozenset({"chapter", "module", "subject"}),
        "topic": frozenset({"section", "chapter", "module", "subject"}),
        "concept": frozenset({"section", "chapter", "module", "subject", "topic"}),
        "subtopic": frozenset({"topic", "concept", "section", "chapter", "module"}),
        "learning_objective": frozenset(
            {"topic", "subtopic", "concept", "section", "chapter", "module"}
        ),
        "objective": frozenset(
            {"topic", "subtopic", "concept", "section", "chapter", "module"}
        ),
    }
    parents = allowed.get(child_kind)
    if parents is None:
        return True
    return parent_kind in parents

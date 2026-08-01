"""UX-001 / KWP-014 — Student Curriculum Map presentation.

Projects certified learner hierarchy plus Knowledge Architecture map
highlights (completed / current / future / weak prerequisites).
No new educational reasoning authority — navigation and structure only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from flask import url_for


_SYLLABUS_SORT = re.compile(r"^(\d+(?:\.\d+)*)")


def _syllabus_display_sort_key(title: str) -> tuple:
    """Order titles by leading syllabus code when present (EV-001 TB-011)."""
    text = (title or "").strip()
    match = _SYLLABUS_SORT.match(text)
    if match:
        parts = tuple(int(part) for part in match.group(1).split("."))
        return (0, parts, text.lower())
    return (1, (), text.lower())


@dataclass(frozen=True)
class KnowledgeGraphNodeView:
    node_id: str
    title: str
    kind: str
    parent_id: str
    difficulty: str
    estimated_minutes: int
    objective_ids: tuple[str, ...]
    prerequisite_ids: tuple[str, ...]
    progress_label: str
    is_current: bool = False
    map_status: str = ""
    children: tuple[KnowledgeGraphNodeView, ...] = ()


@dataclass(frozen=True)
class CurriculumMapHighlight:
    """One highlighted topic on the Curriculum Map strip."""

    topic_id: str
    title: str
    status_label: str
    status: str
    is_current: bool = False


@dataclass(frozen=True)
class StudentKnowledgeGraphPage:
    page_title: str
    page_question: str
    subject_label: str
    certified_source: str
    roots: tuple[KnowledgeGraphNodeView, ...]
    selected: KnowledgeGraphNodeView | None
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    home_href: str
    node_count: int
    edge_count: int
    # KWP-014 Curriculum Map enrichments
    why_current_matters: str = ""
    pathway_titles: tuple[str, ...] = ()
    map_highlights: tuple[CurriculumMapHighlight, ...] = ()
    weak_prerequisite_titles: tuple[str, ...] = ()


class StudentKnowledgeGraphPresentationService:
    """Build a Curriculum Map from certified learner graph + KA overlay."""

    def build(
        self,
        *,
        subject_code: str = "",
        examination_label: str = "",
        current_topic_id: str = "",
        completed_topic_ids: tuple[str, ...] = (),
        weak_topic_ids: tuple[str, ...] = (),
    ) -> StudentKnowledgeGraphPage:
        home_href = url_for("student.home")
        empty = StudentKnowledgeGraphPage(
            page_title="Curriculum Map",
            page_question="Where does today's topic sit in my qualification?",
            subject_label=examination_label or subject_code or "",
            certified_source="",
            roots=(),
            selected=None,
            empty_reason=(
                "Your curriculum map appears when a certified syllabus "
                "is published for your exam."
            ),
            empty_action_label="Return Home",
            empty_action_href=home_href,
            home_href=home_href,
            node_count=0,
            edge_count=0,
        )

        code = (subject_code or "").strip().upper()
        if not code and examination_label:
            token = examination_label.strip().split()[0]
            code = token.strip("·,").upper()
        if not code:
            return empty

        try:
            from app.application.curriculum_intelligence import (
                certified_learning_service as cls,
            )

            service = cls.CertifiedLearningService()
            package = service.load_package(code)
            graph = service.knowledge_graph(package)
            provenance = service.provenance(package)
        except Exception:  # noqa: BLE001 — presentation soft-fail
            return empty

        completed = {str(x).strip() for x in completed_topic_ids if str(x).strip()}
        weak = {str(x).strip() for x in weak_topic_ids if str(x).strip()}
        current = (current_topic_id or "").strip()
        by_parent: dict[str, list] = {}
        nodes_by_id = {n.node_id: n for n in graph.nodes}
        for node in graph.nodes:
            parent = (node.parent_node_id or "").strip()
            by_parent.setdefault(parent, []).append(node)

        def _kind_value(node) -> str:
            return str(node.kind.value if hasattr(node.kind, "value") else node.kind)

        def _map_status(
            node_id: str,
            kind: str,
            *,
            parent_id: str = "",
            children_statuses: tuple[str, ...] = (),
        ) -> tuple[str, str]:
            if node_id == current:
                return "Current", "current"
            if node_id in weak:
                return "Weak prerequisite", "weak_prerequisite"
            if node_id in completed:
                return "Completed", "completed"
            # Learning objectives inherit Study Progress from their parent topic
            # so Completed topics never show all children as "Not started".
            if kind in {"learning_objective", "objective"}:
                if parent_id and parent_id in completed:
                    return "Included in completed topic", "completed"
                if parent_id and parent_id == current:
                    return "In progress with topic", "current"
                return "Not started", "future"
            # Section / chapter roll-up from children (EV-001 TB-006).
            if children_statuses:
                if children_statuses and all(s == "completed" for s in children_statuses):
                    return "Completed", "completed"
                if any(s in {"completed", "current"} for s in children_statuses):
                    return "In progress", "current"
            return "Future", "future"

        def _build(node, depth: int = 0) -> KnowledgeGraphNodeView | None:
            from app.application.student_baseline.topics import is_non_syllabus_title

            title = (node.title or "").strip()
            if title and is_non_syllabus_title(title):
                return None
            kids_raw = by_parent.get(node.node_id, [])
            children: tuple[KnowledgeGraphNodeView, ...] = ()
            if depth < 2:
                built_kids = [
                    child
                    for child in (_build(c, depth + 1) for c in kids_raw[:40])
                    if child is not None
                ]
                built_kids.sort(key=lambda c: _syllabus_display_sort_key(c.title or ""))
                children = tuple(built_kids)
            kind_raw = _kind_value(node)
            progress, status = _map_status(
                node.node_id,
                kind_raw,
                parent_id=(node.parent_node_id or "").strip(),
                children_statuses=tuple(c.map_status for c in children),
            )
            return KnowledgeGraphNodeView(
                node_id=node.node_id,
                title=node.title,
                kind=kind_raw,
                parent_id=(node.parent_node_id or ""),
                difficulty=(node.difficulty or "").strip(),
                estimated_minutes=int(node.estimated_minutes or 0),
                objective_ids=tuple(node.objective_ids or ()),
                prerequisite_ids=tuple(node.prerequisite_ids or ()),
                progress_label=progress,
                is_current=node.node_id == current,
                map_status=status,
                children=children,
            )

        roots_raw = by_parent.get("", [])
        if not roots_raw:
            roots_raw = [
                n
                for n in graph.nodes
                if not n.parent_node_id or n.parent_node_id not in nodes_by_id
            ]
        roots = tuple(
            root for root in (_build(n) for n in roots_raw[:30]) if root is not None
        )

        selected = None
        if current and current in nodes_by_id:
            selected = _build(nodes_by_id[current], depth=2)

        source = "Certified curriculum"
        if provenance.subject_code or provenance.version_label:
            source = (
                f"Certified · {provenance.subject_code or code}"
                + (
                    f" · {provenance.version_label}"
                    if provenance.version_label
                    else ""
                )
            )
        elif provenance.status:
            source = f"Certified · {provenance.status}"

        why = ""
        pathway_titles: tuple[str, ...] = ()
        map_highlights: list[CurriculumMapHighlight] = []
        weak_titles: list[str] = []
        try:
            from app.application.knowledge_architecture import (
                KnowledgeArchitectureEngine,
                LearnerGraphContext,
            )
            from app.application.student_baseline.topics import is_non_syllabus_title

            engine = KnowledgeArchitectureEngine.from_learner_package(package)
            ctx = LearnerGraphContext(
                completed_topic_ids=frozenset(completed),
                weak_topic_ids=frozenset(weak),
                current_topic_id=current,
            )
            cmap = engine.curriculum_map(
                context=ctx,
                subject_label=examination_label or provenance.subject_code or code,
            )
            why = cmap.why_current_matters or ""
            if cmap.pathway is not None:
                pathway_titles = tuple(
                    title
                    for title in cmap.pathway.topic_titles
                    if not is_non_syllabus_title(title)
                )
            for node in cmap.nodes[:24]:
                if is_non_syllabus_title(node.title or ""):
                    continue
                map_highlights.append(
                    CurriculumMapHighlight(
                        topic_id=node.topic_id,
                        title=node.title,
                        status_label=node.status_label,
                        status=node.status.value,
                        is_current=node.is_current,
                    )
                )
                if node.status.value == "weak_prerequisite":
                    weak_titles.append(node.title)
        except Exception:  # noqa: BLE001
            pass

        return StudentKnowledgeGraphPage(
            page_title="Curriculum Map",
            page_question="Where does today's topic sit in my qualification?",
            subject_label=examination_label or provenance.subject_code or code,
            certified_source=source,
            roots=roots,
            selected=selected,
            empty_reason="",
            empty_action_label="",
            empty_action_href=home_href,
            home_href=home_href,
            node_count=len(graph.nodes),
            edge_count=len(graph.edges),
            why_current_matters=why,
            pathway_titles=pathway_titles,
            map_highlights=tuple(map_highlights),
            weak_prerequisite_titles=tuple(weak_titles),
        )

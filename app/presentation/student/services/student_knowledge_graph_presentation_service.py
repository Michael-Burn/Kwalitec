"""UX-001 — Student Knowledge Graph presentation (minimal hierarchy UI).

Projects LearnerKnowledgeGraph from certified published curriculum.
No new educational reasoning — navigation and progress indicators only.
"""

from __future__ import annotations

from dataclasses import dataclass

from flask import url_for


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
    children: tuple[KnowledgeGraphNodeView, ...] = ()


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


class StudentKnowledgeGraphPresentationService:
    """Build a minimal interactive hierarchy from certified learner graph."""

    def build(
        self,
        *,
        subject_code: str = "",
        examination_label: str = "",
        current_topic_id: str = "",
        completed_topic_ids: tuple[str, ...] = (),
    ) -> StudentKnowledgeGraphPage:
        home_href = url_for("student.home")
        empty = StudentKnowledgeGraphPage(
            page_title="Knowledge Map",
            page_question="How does my syllabus fit together?",
            subject_label=examination_label or subject_code or "",
            certified_source="",
            roots=(),
            selected=None,
            empty_reason=(
                "Your knowledge map appears when a certified syllabus "
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
            # Best-effort: first token of exam label (e.g. "CS1 · …").
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
        current = (current_topic_id or "").strip()
        by_parent: dict[str, list] = {}
        nodes_by_id = {n.node_id: n for n in graph.nodes}
        for node in graph.nodes:
            parent = (node.parent_node_id or "").strip()
            by_parent.setdefault(parent, []).append(node)

        def _progress(node_id: str, kind: str) -> str:
            if node_id == current:
                return "Current"
            if node_id in completed:
                return "Complete"
            if kind in {"learning_objective", "objective"}:
                return "Not started"
            return ""

        def _build(node, depth: int = 0) -> KnowledgeGraphNodeView:
            kids_raw = by_parent.get(node.node_id, [])
            # Cap depth for calm UI — chapters → topics → objectives.
            children = ()
            if depth < 2:
                children = tuple(_build(c, depth + 1) for c in kids_raw[:40])
            return KnowledgeGraphNodeView(
                node_id=node.node_id,
                title=node.title,
                kind=str(node.kind.value if hasattr(node.kind, "value") else node.kind),
                parent_id=(node.parent_node_id or ""),
                difficulty=(node.difficulty or "").strip(),
                estimated_minutes=int(node.estimated_minutes or 0),
                objective_ids=tuple(node.objective_ids or ()),
                prerequisite_ids=tuple(node.prerequisite_ids or ()),
                progress_label=_progress(node.node_id, str(node.kind)),
                is_current=node.node_id == current,
                children=children,
            )

        roots_raw = by_parent.get("", [])
        if not roots_raw:
            # Fallback: top-level chapters/sections with no resolved parent.
            roots_raw = [
                n
                for n in graph.nodes
                if not n.parent_node_id or n.parent_node_id not in nodes_by_id
            ]
        roots = tuple(_build(n) for n in roots_raw[:30])

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

        return StudentKnowledgeGraphPage(
            page_title="Knowledge Map",
            page_question="How does my syllabus fit together?",
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
        )

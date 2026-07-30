"""EI-002B — Build learner-facing knowledge graph from certified curriculum."""

from __future__ import annotations

from typing import Any

from app.domain.curriculum_intelligence.certified_learning import (
    CertifiedNodeKind,
    CurriculumProvenanceRef,
    LearnerGraphEdge,
    LearnerGraphNode,
    LearnerKnowledgeGraph,
)
from app.domain.educational_engine_foundation.derivation import (
    EducationalArtefactDeriver,
)

_KIND_MAP = {
    "subject": CertifiedNodeKind.SUBJECT,
    "chapter": CertifiedNodeKind.CHAPTER,
    "module": CertifiedNodeKind.CHAPTER,
    "section": CertifiedNodeKind.SECTION,
    "topic": CertifiedNodeKind.TOPIC,
    "subtopic": CertifiedNodeKind.TOPIC,
    "concept": CertifiedNodeKind.CONCEPT,
    "learning_objective": CertifiedNodeKind.LEARNING_OBJECTIVE,
    "objective": CertifiedNodeKind.LEARNING_OBJECTIVE,
}


def extract_provenance(package: dict[str, Any]) -> CurriculumProvenanceRef:
    """Read certification provenance from a published package dict."""
    cert = package.get("certification") if isinstance(package, dict) else None
    cert = cert if isinstance(cert, dict) else {}
    structure = package.get("structure") if isinstance(package, dict) else None
    structure = structure if isinstance(structure, dict) else {}
    subject = str(package.get("subject_code") or "").strip().upper()
    version = str(package.get("version_label") or "").strip()
    identity = f"{subject}:{version}" if subject and version else subject
    return CurriculumProvenanceRef(
        chain_id=str(
            cert.get("chain_id") or structure.get("ei_chain_id") or ""
        ).strip(),
        snapshot_id=str(
            cert.get("snapshot_id")
            or structure.get("ei_certified_snapshot_id")
            or ""
        ).strip(),
        authority=str(
            cert.get("authority") or structure.get("curriculum_authority") or ""
        ).strip(),
        status=str(
            cert.get("status") or structure.get("ei_certification_status") or ""
        ).strip(),
        subject_code=subject,
        version_label=version,
        curriculum_identity=identity,
    )


def assert_certified_package(package: dict[str, Any]) -> CurriculumProvenanceRef:
    """Refuse packages that are not certified (or legacy migration)."""
    provenance = extract_provenance(package)
    authority = provenance.authority.lower()
    status = provenance.status.lower()
    if not provenance.authority and not provenance.status:
        # Pre-EI packages remain readable during migration (authority empty).
        return provenance
    if authority in {
        "certified_snapshot",
        "legacy_cip_fallback",
        "legacy_or_unspecified",
    }:
        return provenance
    if status in {"certified", "certified_with_warnings"}:
        return provenance
    if authority.startswith("legacy"):
        return provenance
    raise ValueError(
        "Student learning refuses non-certified curriculum authority="
        f"{provenance.authority!r} status={provenance.status!r}"
    )


class LearnerKnowledgeGraphBuilder:
    """Construct a learner-facing graph from a certified published package.

    Reuses EducationalArtefactDeriver — no new educational reasoning.
    Node identifiers are the stable ids projected from certified snapshots.
    """

    def __init__(self, deriver: EducationalArtefactDeriver | None = None) -> None:
        self._deriver = deriver or EducationalArtefactDeriver()

    def build(self, package: dict[str, Any]) -> LearnerKnowledgeGraph:
        provenance = assert_certified_package(package)
        bundle = self._deriver.derive(package)
        nodes: list[LearnerGraphNode] = []
        edges: list[LearnerGraphEdge] = []
        edge_i = 0

        for section in bundle.sections:
            nodes.append(
                LearnerGraphNode(
                    node_id=section.section_id,
                    title=section.title,
                    kind=CertifiedNodeKind.CHAPTER,
                )
            )
        for topic in bundle.topics:
            nodes.append(
                LearnerGraphNode(
                    node_id=topic.topic_id,
                    title=topic.title,
                    kind=CertifiedNodeKind.TOPIC,
                    parent_node_id=topic.section_id,
                    difficulty=topic.difficulty,
                    estimated_minutes=topic.estimated_minutes,
                    objective_ids=topic.learning_objective_ids,
                    prerequisite_ids=topic.prerequisite_ids,
                )
            )
            if topic.section_id:
                edge_i += 1
                edges.append(
                    LearnerGraphEdge(
                        edge_id=f"e{edge_i}",
                        relation="parent_of",
                        from_node_id=topic.section_id,
                        to_node_id=topic.topic_id,
                    )
                )
            for prereq in topic.prerequisite_ids:
                edge_i += 1
                edges.append(
                    LearnerGraphEdge(
                        edge_id=f"e{edge_i}",
                        relation="requires",
                        from_node_id=topic.topic_id,
                        to_node_id=prereq,
                    )
                )
        for objective in bundle.objectives:
            nodes.append(
                LearnerGraphNode(
                    node_id=objective.objective_id,
                    title=objective.text,
                    kind=CertifiedNodeKind.LEARNING_OBJECTIVE,
                    parent_node_id=objective.topic_id,
                    difficulty="",
                    estimated_minutes=objective.estimated_minutes,
                )
            )
            edge_i += 1
            edges.append(
                LearnerGraphEdge(
                    edge_id=f"e{edge_i}",
                    relation="learning_objective_of",
                    from_node_id=objective.objective_id,
                    to_node_id=objective.topic_id,
                )
            )
            edge_i += 1
            edges.append(
                LearnerGraphEdge(
                    edge_id=f"e{edge_i}",
                    relation="parent_of",
                    from_node_id=objective.topic_id,
                    to_node_id=objective.objective_id,
                )
            )

        for a, b in bundle.prerequisite_edges:
            if not any(
                e.from_node_id == a and e.to_node_id == b and e.relation == "requires"
                for e in edges
            ):
                edge_i += 1
                edges.append(
                    LearnerGraphEdge(
                        edge_id=f"e{edge_i}",
                        relation="requires",
                        from_node_id=a,
                        to_node_id=b,
                    )
                )

        return LearnerKnowledgeGraph(
            curriculum_identity=bundle.curriculum_identity,
            provenance=provenance,
            nodes=tuple(nodes),
            edges=tuple(edges),
        )

    @staticmethod
    def kind_for(raw_kind: str) -> CertifiedNodeKind:
        return _KIND_MAP.get((raw_kind or "").strip().lower(), CertifiedNodeKind.TOPIC)

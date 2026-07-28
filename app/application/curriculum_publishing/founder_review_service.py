"""Founder Review Workflow — inspect draft editions without student exposure."""

from __future__ import annotations

import json
from typing import Any

from app.application.curriculum_publishing.dto import (
    EditionInspection,
    EditionSummary,
    HierarchyNode,
    NodeInspection,
)
from app.application.curriculum_publishing.edition_graph_loader import (
    EditionGraphLoader,
    node_kind_for_stable_id,
)
from app.application.curriculum_publishing.exceptions import (
    NodeNotFoundError,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.curriculum_publishing.review_state import (
    NodeReviewStatus,
    ReviewStatus,
)
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgNodeProvenance,
    CkgNodeReviewState,
    CkgValidationReport,
)


class FounderReviewService:
    """Read-side Founder review of draft (and historical) CKG editions.

    Draft editions are never exposed to student-facing systems from this service.
    """

    def __init__(self, loader: EditionGraphLoader | None = None) -> None:
        self._loader = loader or EditionGraphLoader()

    def list_draft_editions(
        self, *, subject_code: str | None = None
    ) -> list[EditionSummary]:
        """List editions in draft publication state."""
        query = CkgGraphEdition.query.filter_by(
            publication_state=PublicationState.DRAFT.value
        )
        if subject_code:
            query = query.filter_by(subject_code=subject_code.upper())
        rows = query.order_by(
            CkgGraphEdition.subject_code.asc(),
            CkgGraphEdition.edition_label.desc(),
        ).all()
        return [self._summary(r) for r in rows]

    def list_editions(
        self,
        *,
        subject_code: str | None = None,
        publication_state: str | None = None,
    ) -> list[EditionSummary]:
        """List editions with optional filters (Founder history views)."""
        query = CkgGraphEdition.query
        if subject_code:
            query = query.filter_by(subject_code=subject_code.upper())
        if publication_state:
            query = query.filter_by(publication_state=publication_state)
        rows = query.order_by(
            CkgGraphEdition.subject_code.asc(),
            CkgGraphEdition.updated_at.desc(),
        ).all()
        return [self._summary(r) for r in rows]

    def inspect_edition(self, edition_id: str) -> EditionInspection:
        """Full inspection payload: hierarchy, validation, review summary."""
        edition = self._loader.require_edition(edition_id)
        snapshot = self._loader.structural_snapshot(edition_id)
        hierarchy = self._build_hierarchy(snapshot)
        validation = self.get_validation_report(edition_id)
        review_summary = self._review_summary(edition_id)
        return EditionInspection(
            edition=self._summary(edition),
            hierarchy=hierarchy,
            node_count=len(snapshot.get("nodes", [])),
            edge_count=len(snapshot.get("edges", [])),
            validation_report=validation,
            review_summary=review_summary,
            source_cmp_ref=edition.source_cmp_ref,
            source_syllabus_ref=edition.source_syllabus_ref,
        )

    def get_validation_report(self, edition_id: str) -> dict[str, Any] | None:
        """Latest stored validation report for the edition."""
        self._loader.require_edition(edition_id)
        row = (
            CkgValidationReport.query.filter_by(edition_id=edition_id)
            .order_by(CkgValidationReport.created_at.desc())
            .first()
        )
        if row is None:
            return None
        payload = json.loads(row.report_json or "{}")
        payload["report_id"] = row.report_id
        payload["passed"] = row.passed
        payload["issue_count"] = row.issue_count
        return payload

    def get_provenance(
        self, edition_id: str, stable_id: str | None = None
    ) -> list[dict[str, Any]]:
        """Provenance rows for an edition (optionally one node)."""
        self._loader.require_edition(edition_id)
        query = CkgNodeProvenance.query.filter_by(edition_id=edition_id)
        if stable_id:
            query = query.filter_by(stable_id=stable_id)
        rows = query.order_by(CkgNodeProvenance.stable_id.asc()).all()
        return [
            {
                "stable_id": r.stable_id,
                "source_document_id": r.source_document_id,
                "document_kind": r.document_kind,
                "page_number": r.page_number,
                "structural_path": r.structural_path,
                "section_heading": r.section_heading,
                "paragraph_or_table_ref": r.paragraph_or_table_ref,
                "confidence": r.confidence,
                "extraction_method": r.extraction_method,
                "notes": r.notes,
            }
            for r in rows
        ]

    def get_confidence_summary(self, edition_id: str) -> dict[str, Any]:
        """Extraction confidence distribution for Founder review."""
        rows = self.get_provenance(edition_id)
        bands = {
            "highly_reliable": 0,
            "review_recommended": 0,
            "manual_confirmation": 0,
        }
        scores: list[int] = []
        for row in rows:
            score = int(row["confidence"])
            scores.append(score)
            if score >= 99:
                bands["highly_reliable"] += 1
            elif score >= 90:
                bands["review_recommended"] += 1
            else:
                bands["manual_confirmation"] += 1
        return {
            "edition_id": edition_id,
            "node_count": len(rows),
            "bands": bands,
            "min_confidence": min(scores) if scores else None,
            "max_confidence": max(scores) if scores else None,
            "avg_confidence": (
                round(sum(scores) / len(scores), 1) if scores else None
            ),
        }

    def search_nodes(
        self, edition_id: str, query: str, *, limit: int = 50
    ) -> list[NodeInspection]:
        """Search curriculum nodes by stable id or title/statement text."""
        snapshot = self._loader.structural_snapshot(edition_id)
        needle = (query or "").strip().lower()
        if not needle:
            return []
        reviews = self._review_map(edition_id)
        provenance = {
            p["stable_id"]: p for p in self.get_provenance(edition_id)
        }
        hits: list[NodeInspection] = []
        for node in snapshot.get("nodes", []):
            hay = (
                f"{node.get('stable_id', '')} {node.get('title', '')} "
                f"{node.get('code', '')}"
            ).lower()
            meta = node.get("metadata") or {}
            if "statement" in meta:
                hay += f" {meta['statement']}".lower()
            if needle not in hay:
                continue
            sid = node["stable_id"]
            prov = provenance.get(sid)
            hits.append(
                NodeInspection(
                    stable_id=sid,
                    kind=node.get("kind", node_kind_for_stable_id(sid)),
                    title=node.get("title", ""),
                    metadata=dict(meta),
                    review_status=reviews.get(
                        sid, NodeReviewStatus.PENDING.value
                    ),
                    confidence=prov["confidence"] if prov else None,
                    provenance=prov,
                )
            )
            if len(hits) >= limit:
                break
        return hits

    def navigate_hierarchy(self, edition_id: str) -> HierarchyNode | None:
        """Return the containment hierarchy tree."""
        snapshot = self._loader.structural_snapshot(edition_id)
        return self._build_hierarchy(snapshot)

    def inspect_node(self, edition_id: str, stable_id: str) -> NodeInspection:
        """Inspect a single node with review + provenance."""
        snapshot = self._loader.structural_snapshot(edition_id)
        match = next(
            (
                n
                for n in snapshot.get("nodes", [])
                if n.get("stable_id") == stable_id
            ),
            None,
        )
        if match is None:
            raise NodeNotFoundError(
                f"Node {stable_id} not found in edition {edition_id}"
            )
        reviews = self._review_map(edition_id)
        prov_rows = self.get_provenance(edition_id, stable_id)
        prov = prov_rows[0] if prov_rows else None
        return NodeInspection(
            stable_id=stable_id,
            kind=match.get("kind", node_kind_for_stable_id(stable_id)),
            title=match.get("title", ""),
            metadata=dict(match.get("metadata") or {}),
            review_status=reviews.get(
                stable_id, NodeReviewStatus.PENDING.value
            ),
            confidence=prov["confidence"] if prov else None,
            provenance=prov,
        )

    def _summary(self, edition: CkgGraphEdition) -> EditionSummary:
        return EditionSummary(
            edition_id=edition.edition_id,
            subject_code=edition.subject_code,
            edition_label=edition.edition_label,
            title=edition.title,
            publication_state=edition.publication_state,
            validation_status=edition.validation_status,
            review_status=getattr(
                edition, "review_status", ReviewStatus.PENDING.value
            )
            or ReviewStatus.PENDING.value,
            provider=edition.provider,
            published_at=(
                edition.published_at.isoformat()
                if getattr(edition, "published_at", None)
                else None
            ),
            approved_by=getattr(edition, "approved_by", None),
        )

    def _review_map(self, edition_id: str) -> dict[str, str]:
        rows = CkgNodeReviewState.query.filter_by(edition_id=edition_id).all()
        return {r.stable_id: r.status for r in rows}

    def _review_summary(self, edition_id: str) -> dict[str, int]:
        summary = {
            NodeReviewStatus.PENDING.value: 0,
            NodeReviewStatus.APPROVED.value: 0,
            NodeReviewStatus.REJECTED.value: 0,
        }
        ids = self._loader.collect_stable_ids(edition_id)
        reviews = self._review_map(edition_id)
        for sid in ids:
            status = reviews.get(sid, NodeReviewStatus.PENDING.value)
            summary[status] = summary.get(status, 0) + 1
        return summary

    def _build_hierarchy(
        self, snapshot: dict[str, Any]
    ) -> HierarchyNode | None:
        nodes = snapshot.get("nodes", [])
        by_id = {n["stable_id"]: n for n in nodes}
        children_map: dict[str, list[str]] = {}
        subject_id: str | None = None
        for node in nodes:
            kind = node.get("kind")
            if kind == "subject":
                subject_id = node["stable_id"]
                continue
            parent = node.get("parent_stable_id")
            if parent:
                children_map.setdefault(parent, []).append(node["stable_id"])

        # Prefer containment edges for structural ordering when present.
        for edge in snapshot.get("edges", []):
            if edge.get("relationship_type") != "contains":
                continue
            parent = edge["from_stable_id"]
            child = edge["to_stable_id"]
            bucket = children_map.setdefault(parent, [])
            if child not in bucket:
                bucket.append(child)

        if subject_id is None:
            return None

        def build(sid: str) -> HierarchyNode:
            node = by_id.get(sid, {"stable_id": sid, "kind": "unknown", "title": ""})
            child_ids = sorted(
                children_map.get(sid, []),
                key=lambda cid: (
                    (by_id.get(cid) or {}).get("metadata", {}).get(
                        "display_order", 0
                    ),
                    cid,
                ),
            )
            # Only recurse structural children in hierarchy view.
            structural_kinds = {
                "subject",
                "topic",
                "section",
                "subsection",
                "learning_objective",
            }
            kids = [
                build(cid)
                for cid in child_ids
                if (by_id.get(cid) or {}).get("kind") in structural_kinds
            ]
            return HierarchyNode(
                stable_id=sid,
                kind=node.get("kind", "unknown"),
                title=node.get("title", ""),
                children=tuple(kids),
            )

        return build(subject_id)

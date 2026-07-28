"""Edition Comparison — structured diffs for Founder UI consumption."""

from __future__ import annotations

from typing import Any

from app.application.curriculum_publishing.dto import (
    ComparisonChange,
    EditionComparison,
)
from app.application.curriculum_publishing.edition_graph_loader import (
    EditionGraphLoader,
)
from app.application.curriculum_publishing.edition_snapshot_service import (
    EditionSnapshotService,
)
from app.application.curriculum_publishing.exceptions import EditionNotFoundError

_HIERARCHY_KINDS = frozenset(
    {"subject", "topic", "section", "subsection"}
)
_LO_KIND = "learning_objective"
_OBJECT_KINDS = frozenset(
    {
        "definition",
        "formula",
        "worked_example",
        "practice_exercise",
        "reading_reference",
        "syllabus_outcome",
    }
)
_META_KEYS = (
    "difficulty",
    "estimated_study_minutes",
    "cognitive_level",
    "learning_type",
    "statement",
    "body",
    "notation",
    "summary",
    "title",
)


class EditionComparisonService:
    """Compare two editions via live graphs and/or stored snapshots."""

    def __init__(
        self,
        *,
        loader: EditionGraphLoader | None = None,
        snapshots: EditionSnapshotService | None = None,
    ) -> None:
        self._loader = loader or EditionGraphLoader()
        self._snapshots = snapshots or EditionSnapshotService(self._loader)

    def compare(
        self,
        left_edition_id: str,
        right_edition_id: str,
        *,
        left_snapshot_id: str | None = None,
        right_snapshot_id: str | None = None,
    ) -> EditionComparison:
        """Return structured comparison suitable for future Founder UI."""
        left = self._resolve_payload(left_edition_id, left_snapshot_id)
        right = self._resolve_payload(right_edition_id, right_snapshot_id)

        left_nodes = {n["stable_id"]: n for n in left.get("nodes", [])}
        right_nodes = {n["stable_id"]: n for n in right.get("nodes", [])}
        left_edges = self._edge_index(left.get("edges", []))
        right_edges = self._edge_index(right.get("edges", []))

        hierarchy: list[ComparisonChange] = []
        los: list[ComparisonChange] = []
        objects: list[ComparisonChange] = []
        metadata: list[ComparisonChange] = []

        all_ids = sorted(set(left_nodes) | set(right_nodes))
        for sid in all_ids:
            ln = left_nodes.get(sid)
            rn = right_nodes.get(sid)
            if ln is None and rn is not None:
                change = ComparisonChange(
                    category=self._category_for_kind(rn.get("kind", "")),
                    change_type="added",
                    stable_id=sid,
                    detail=f"Added {rn.get('kind')} {sid}",
                    after=self._node_brief(rn),
                )
                self._bucket(change, hierarchy, los, objects)
            elif rn is None and ln is not None:
                change = ComparisonChange(
                    category=self._category_for_kind(ln.get("kind", "")),
                    change_type="removed",
                    stable_id=sid,
                    detail=f"Removed {ln.get('kind')} {sid}",
                    before=self._node_brief(ln),
                )
                self._bucket(change, hierarchy, los, objects)
            elif ln is not None and rn is not None:
                if ln.get("parent_stable_id") != rn.get("parent_stable_id"):
                    hierarchy.append(
                        ComparisonChange(
                            category="hierarchy",
                            change_type="moved",
                            stable_id=sid,
                            detail=f"Parent changed for {sid}",
                            before=ln.get("parent_stable_id"),
                            after=rn.get("parent_stable_id"),
                        )
                    )
                left_meta = ln.get("metadata") or {}
                right_meta = rn.get("metadata") or {}
                for key in _META_KEYS:
                    lv = left_meta.get(key, ln.get(key))
                    rv = right_meta.get(key, rn.get(key))
                    if key == "title":
                        lv = lv if lv is not None else ln.get("title")
                        rv = rv if rv is not None else rn.get("title")
                    if lv != rv and (lv is not None or rv is not None):
                        # LO statement treated as LO change category too.
                        category = (
                            "learning_objective"
                            if ln.get("kind") == _LO_KIND and key == "statement"
                            else "metadata"
                        )
                        target = los if category == "learning_objective" else metadata
                        target.append(
                            ComparisonChange(
                                category=category,
                                change_type="modified",
                                stable_id=sid,
                                detail=f"{key} changed on {sid}",
                                before=lv,
                                after=rv,
                            )
                        )

        prereq: list[ComparisonChange] = []
        all_edge_keys = sorted(set(left_edges) | set(right_edges))
        for key in all_edge_keys:
            rel, frm, to = key
            if rel != "requires":
                continue
            le = left_edges.get(key)
            re = right_edges.get(key)
            if le is None and re is not None:
                prereq.append(
                    ComparisonChange(
                        category="prerequisite",
                        change_type="added",
                        stable_id=frm,
                        detail=f"Prerequisite added {frm} → {to}",
                        after={"from": frm, "to": to},
                    )
                )
            elif re is None and le is not None:
                prereq.append(
                    ComparisonChange(
                        category="prerequisite",
                        change_type="removed",
                        stable_id=frm,
                        detail=f"Prerequisite removed {frm} → {to}",
                        before={"from": frm, "to": to},
                    )
                )

        return EditionComparison(
            left_edition_id=left_edition_id,
            right_edition_id=right_edition_id,
            hierarchy_changes=tuple(hierarchy),
            learning_objective_changes=tuple(los),
            prerequisite_changes=tuple(prereq),
            educational_object_changes=tuple(objects),
            metadata_changes=tuple(metadata),
        )

    def _resolve_payload(
        self, edition_id: str, snapshot_id: str | None
    ) -> dict[str, Any]:
        if snapshot_id:
            payload = self._snapshots.load_payload(snapshot_id)
            if not payload:
                raise EditionNotFoundError(f"Snapshot not found: {snapshot_id}")
            return payload

        # Prefer latest snapshot when live nodes are gone (archived editions).
        subject = self._loader.subject_for_edition(edition_id)
        if subject is None:
            latest = self._snapshots.latest_for_edition(edition_id)
            if latest is None:
                # Still validate edition exists.
                self._loader.require_edition(edition_id)
                return {
                    "edition_id": edition_id,
                    "nodes": [],
                    "edges": [],
                }
            return self._snapshots.load_payload(latest.snapshot_id)

        return self._loader.structural_snapshot(edition_id)

    @staticmethod
    def _edge_index(
        edges: list[dict[str, Any]],
    ) -> dict[tuple[str, str, str], dict[str, Any]]:
        out: dict[tuple[str, str, str], dict[str, Any]] = {}
        for edge in edges:
            key = (
                edge.get("relationship_type", ""),
                edge.get("from_stable_id", ""),
                edge.get("to_stable_id", ""),
            )
            out[key] = edge
        return out

    @staticmethod
    def _category_for_kind(kind: str) -> str:
        if kind in _HIERARCHY_KINDS:
            return "hierarchy"
        if kind == _LO_KIND:
            return "learning_objective"
        if kind in _OBJECT_KINDS:
            return "educational_object"
        return "metadata"

    @staticmethod
    def _bucket(
        change: ComparisonChange,
        hierarchy: list[ComparisonChange],
        los: list[ComparisonChange],
        objects: list[ComparisonChange],
    ) -> None:
        if change.category == "hierarchy":
            hierarchy.append(change)
        elif change.category == "learning_objective":
            los.append(change)
        elif change.category == "educational_object":
            objects.append(change)

    @staticmethod
    def _node_brief(node: dict[str, Any]) -> dict[str, Any]:
        return {
            "stable_id": node.get("stable_id"),
            "kind": node.get("kind"),
            "title": node.get("title"),
            "parent_stable_id": node.get("parent_stable_id"),
        }

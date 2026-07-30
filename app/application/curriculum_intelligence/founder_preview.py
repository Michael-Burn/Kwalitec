"""Founder Preview interfaces for certified curriculum snapshots (EI-001D).

No UI changes. Preview consumes certified snapshots only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.curriculum_intelligence.certification import (
    CertifiedCurriculumSnapshot,
)
from app.domain.curriculum_intelligence.generation import (
    CertificationOutcome,
    EducationalNode,
)


@dataclass(frozen=True)
class FounderPreviewStructure:
    """Projection of a certified snapshot for future Founder Preview UI."""

    chain_id: str
    snapshot_id: str
    certification_status: CertificationOutcome
    quality_score: float
    warnings: tuple[str, ...]
    section_ids: tuple[str, ...]
    topic_ids: tuple[str, ...]
    objective_ids: tuple[str, ...]
    section_titles: tuple[tuple[str, str], ...]
    topic_titles: tuple[tuple[str, str], ...]
    objective_rows: tuple[tuple[str, str, str], ...]
    topic_section_refs: tuple[tuple[str, str], ...]
    source: str = "certified_snapshot"
    preview_eligible: bool = False


_SECTION_KINDS = frozenset({"chapter", "module", "section"})
_TOPIC_KINDS = frozenset({"topic", "subtopic", "concept"})
_OBJECTIVE_KINDS = frozenset({"learning_objective", "objective"})


class CertifiedSnapshotPreviewPort(ABC):
    """Port for loading certified snapshots into Founder Preview."""

    @abstractmethod
    def get_certified_for_workspace(
        self, workspace_id: str
    ) -> CertifiedCurriculumSnapshot | None:
        """Return the latest preview-eligible certified snapshot, if any."""

    @abstractmethod
    def project(
        self, certified: CertifiedCurriculumSnapshot
    ) -> FounderPreviewStructure:
        """Project a certified snapshot into Founder Preview structure."""


class CertifiedSnapshotPreviewService(CertifiedSnapshotPreviewPort):
    """Default projection — certified snapshots only; rejects NOT_CERTIFIED."""

    def __init__(
        self,
        *,
        loader: CertifiedSnapshotLoader | None = None,
    ) -> None:
        self._loader = loader

    def get_certified_for_workspace(
        self, workspace_id: str
    ) -> CertifiedCurriculumSnapshot | None:
        if self._loader is None:
            return None
        certified = self._loader.load_for_workspace(workspace_id)
        if certified is None or not certified.is_preview_eligible:
            return None
        return certified

    def project(
        self, certified: CertifiedCurriculumSnapshot
    ) -> FounderPreviewStructure:
        if not certified.is_preview_eligible:
            raise ValueError(
                "Founder Preview refuses NOT_CERTIFIED snapshots "
                f"(status={certified.outcome.value})."
            )
        active = certified.snapshot.active_nodes()
        sections = [n for n in active if n.kind in _SECTION_KINDS]
        topics = [n for n in active if n.kind in _TOPIC_KINDS]
        objectives = [n for n in active if n.kind in _OBJECTIVE_KINDS]
        section_ids = tuple(n.node_id for n in sections)
        topic_ids = tuple(n.node_id for n in topics)
        objective_ids = tuple(n.node_id for n in objectives)
        section_set = set(section_ids)
        topic_section_refs = tuple(
            (t.node_id, t.parent_node_id)
            for t in topics
            if t.parent_node_id and t.parent_node_id in section_set
        )
        # Topics may parent under sections that are chapters; also allow
        # parent walk one level for concept→section via topic parent.
        by_id = {n.node_id: n for n in active}
        resolved_refs: list[tuple[str, str]] = list(topic_section_refs)
        for topic in topics:
            if any(tid == topic.node_id for tid, _ in resolved_refs):
                continue
            parent = by_id.get(topic.parent_node_id or "")
            if parent is not None and parent.kind in _SECTION_KINDS:
                resolved_refs.append((topic.node_id, parent.node_id))
            elif parent is not None and parent.parent_node_id in section_set:
                resolved_refs.append((topic.node_id, parent.parent_node_id))

        return FounderPreviewStructure(
            chain_id=certified.chain_id,
            snapshot_id=certified.snapshot_id,
            certification_status=certified.outcome,
            quality_score=certified.certification.quality_score,
            warnings=certified.certification.warnings,
            section_ids=section_ids,
            topic_ids=topic_ids,
            objective_ids=objective_ids,
            section_titles=tuple((n.node_id, n.title) for n in sections),
            topic_titles=tuple((n.node_id, n.title) for n in topics),
            objective_rows=tuple(
                (n.node_id, n.title, n.parent_node_id or "") for n in objectives
            ),
            topic_section_refs=tuple(resolved_refs),
            source="certified_snapshot",
            preview_eligible=True,
        )


class CertifiedSnapshotLoader(ABC):
    """Loads a CertifiedCurriculumSnapshot for a Studio workspace."""

    @abstractmethod
    def load_for_workspace(
        self, workspace_id: str
    ) -> CertifiedCurriculumSnapshot | None:
        """Return certified snapshot bound to workspace, if present."""


def project_nodes_to_preview_rows(
    nodes: tuple[EducationalNode, ...],
) -> dict[str, tuple]:
    """Helper used by structure prep dual-read tests."""
    active = [n for n in nodes if n.active]
    return {
        "sections": tuple(
            (n.node_id, n.title) for n in active if n.kind in _SECTION_KINDS
        ),
        "topics": tuple(
            (n.node_id, n.title) for n in active if n.kind in _TOPIC_KINDS
        ),
        "objectives": tuple(
            (n.node_id, n.title, n.parent_node_id or "")
            for n in active
            if n.kind in _OBJECTIVE_KINDS
        ),
    }

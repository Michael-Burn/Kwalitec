"""Knowledge Architecture metrics for Founder observability (KWP-014).

Curriculum coverage, dependency bottlenecks, difficult prerequisite chains,
recovery path usage, revision pathway usage, and knowledge-graph completeness.
Does not mutate Evidence, Progress, EI engines, Memory, Twin, or Session.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.application.knowledge_architecture.dto import (
    KnowledgeArchitectureSnapshot,
)
from app.application.knowledge_architecture.engine import (
    KnowledgeArchitectureEngine,
)


@dataclass(frozen=True)
class KnowledgeArchitectureMetricsSnapshot:
    """Founder-facing curriculum knowledge architecture summary."""

    node_count: int = 0
    edge_count: int = 0
    prerequisite_edge_count: int = 0
    revision_edge_count: int = 0
    pathway_count: int = 0
    revision_paths_generated: int = 0
    completeness_ratio: float = 0.0
    curriculum_coverage_ratio: float = 0.0
    bottleneck_topic_ids: tuple[str, ...] = ()
    difficult_chain_lengths: tuple[int, ...] = ()
    recovery_path_count: int = 0
    revision_pathway_usage: int = 0
    curriculum_map_opens: int = 0
    subject_label: str = ""
    event_counts: dict[str, int] = field(default_factory=dict)

    def to_opaque(self) -> dict[str, Any]:
        return {
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "prerequisite_edge_count": self.prerequisite_edge_count,
            "revision_edge_count": self.revision_edge_count,
            "pathway_count": self.pathway_count,
            "revision_paths_generated": self.revision_paths_generated,
            "completeness_ratio": round(self.completeness_ratio, 4),
            "curriculum_coverage_ratio": round(self.curriculum_coverage_ratio, 4),
            "bottleneck_topic_ids": list(self.bottleneck_topic_ids),
            "difficult_chain_lengths": list(self.difficult_chain_lengths),
            "recovery_path_count": self.recovery_path_count,
            "revision_pathway_usage": self.revision_pathway_usage,
            "curriculum_map_opens": self.curriculum_map_opens,
            "subject_label": self.subject_label,
            "event_counts": dict(self.event_counts),
        }


class KnowledgeArchitectureMetrics:
    """Aggregate knowledge-architecture analytics for Platform Intelligence."""

    MAP_OPEN_EVENTS = frozenset(
        {
            "knowledge_map_opened",
            "curriculum_map_opened",
        }
    )
    REVISION_PATH_EVENTS = frozenset(
        {
            "revision_pathway_used",
            "revision_opened",
        }
    )

    @classmethod
    def from_engine(
        cls,
        engine: KnowledgeArchitectureEngine,
        *,
        completed_topic_ids: set[str] | frozenset[str] | None = None,
        event_counts: list[tuple[str, int]] | dict[str, int] | None = None,
        subject_label: str = "",
    ) -> KnowledgeArchitectureMetricsSnapshot:
        """Build founder snapshot from an engine + optional telemetry."""
        snap = engine.snapshot(subject_label=subject_label)
        return cls.from_architecture_snapshot(
            snap,
            engine=engine,
            completed_topic_ids=completed_topic_ids,
            event_counts=event_counts,
        )

    @classmethod
    def from_architecture_snapshot(
        cls,
        snap: KnowledgeArchitectureSnapshot,
        *,
        engine: KnowledgeArchitectureEngine | None = None,
        completed_topic_ids: set[str] | frozenset[str] | None = None,
        event_counts: list[tuple[str, int]] | dict[str, int] | None = None,
    ) -> KnowledgeArchitectureMetricsSnapshot:
        if event_counts is None:
            event_map: dict[str, int] = {}
        elif isinstance(event_counts, dict):
            event_map = {str(k): int(v) for k, v in event_counts.items()}
        else:
            event_map = {str(k): int(v) for k, v in event_counts}

        map_opens = sum(
            event_map.get(e, 0) for e in cls.MAP_OPEN_EVENTS
        )
        revision_usage = sum(
            event_map.get(e, 0) for e in cls.REVISION_PATH_EVENTS
        )

        coverage = 0.0
        if snap.node_count > 0 and completed_topic_ids is not None:
            coverage = len(completed_topic_ids) / snap.node_count

        chain_lengths: tuple[int, ...] = ()
        if engine is not None:
            chains = engine.difficult_prerequisite_chains(limit=5)
            chain_lengths = tuple(len(c) for c in chains)

        recovery_count = len(snap.common_recovery_path_ids)

        return KnowledgeArchitectureMetricsSnapshot(
            node_count=snap.node_count,
            edge_count=snap.edge_count,
            prerequisite_edge_count=snap.prerequisite_edge_count,
            revision_edge_count=snap.revision_edge_count,
            pathway_count=snap.pathway_count,
            revision_paths_generated=snap.revision_paths_generated,
            completeness_ratio=snap.completeness_ratio,
            curriculum_coverage_ratio=coverage,
            bottleneck_topic_ids=snap.bottleneck_topic_ids,
            difficult_chain_lengths=chain_lengths,
            recovery_path_count=recovery_count,
            revision_pathway_usage=revision_usage,
            curriculum_map_opens=map_opens,
            subject_label=snap.subject_label,
            event_counts=event_map,
        )

    @classmethod
    def from_telemetry(
        cls,
        *,
        engine: KnowledgeArchitectureEngine | None = None,
        completed_topic_ids: set[str] | frozenset[str] | None = None,
        subject_label: str = "",
    ) -> KnowledgeArchitectureMetricsSnapshot:
        """Load presentation telemetry and combine with an engine snapshot."""
        counts: dict[str, int] = {}
        try:
            from app.services.presentation_telemetry_service import (
                PresentationTelemetryService,
            )

            raw = PresentationTelemetryService.count_by_type()
            if isinstance(raw, dict):
                counts = {str(k): int(v) for k, v in raw.items()}
            else:
                counts = {str(k): int(v) for k, v in raw}
        except Exception:  # noqa: BLE001
            counts = {}

        if engine is None:
            return KnowledgeArchitectureMetricsSnapshot(
                curriculum_map_opens=sum(
                    counts.get(e, 0) for e in cls.MAP_OPEN_EVENTS
                ),
                revision_pathway_usage=sum(
                    counts.get(e, 0) for e in cls.REVISION_PATH_EVENTS
                ),
                event_counts=counts,
                subject_label=subject_label,
            )
        return cls.from_engine(
            engine,
            completed_topic_ids=completed_topic_ids,
            event_counts=counts,
            subject_label=subject_label,
        )

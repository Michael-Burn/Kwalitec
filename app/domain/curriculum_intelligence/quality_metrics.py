"""Pipeline quality metrics contracts (CIP-002)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineQualityMetrics:
    """Aggregate quality snapshot for one pipeline job / document."""

    metrics_id: str
    document_id: int
    pipeline_job_id: str
    workspace_id: str
    extraction_success_rate: float
    parser_success_rate: float
    mean_mapping_confidence: float
    graph_completeness: float
    graph_consistency: float
    entities_requiring_review: int
    founder_approvals: int
    founder_corrections: int
    entity_count: int
    relation_count: int
    validation_error_count: int
    created_at_iso: str

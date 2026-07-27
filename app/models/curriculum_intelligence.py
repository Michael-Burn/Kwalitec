"""ORM models for Curriculum Intelligence Pipeline (CIP-001 / CIP-002 / CIP-003).

CIP-001: processing jobs, extraction, structural parse, curriculum entities,
and knowledge-graph relations.

CIP-002: provenance, confidence, review, validation, audit, quality metrics.

CIP-003: embedding metadata, local vector payloads, retrieval logs.

PDF bytes remain in DocumentStorage — never here. Vector technology details
live only in infrastructure adapters (local vector table is adapter-owned).
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class CipProcessingJob(db.Model):
    """Durable CIP job for one foundation document."""

    __tablename__ = "cip_processing_jobs"
    __table_args__ = (
        db.Index("ix_cip_jobs_document_status", "document_id", "status"),
        db.Index("ix_cip_jobs_workspace", "workspace_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    document_id: int = db.Column(
        db.Integer,
        db.ForeignKey("studio_foundation_documents.id"),
        nullable=False,
        index=True,
    )
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    subject_code: str = db.Column(db.String(64), nullable=False, default="")
    kind: str = db.Column(db.String(64), nullable=False, default="")
    storage_key: str = db.Column(db.String(1024), nullable=False, default="")
    status: str = db.Column(db.String(64), nullable=False, default="queued", index=True)
    checkpoint_stage: str | None = db.Column(db.String(64), nullable=True)
    attempt_count: int = db.Column(db.Integer, nullable=False, default=0)
    cancel_requested: bool = db.Column(db.Boolean, nullable=False, default=False)
    last_error: str | None = db.Column(db.Text, nullable=True)
    diagnostics_json: str = db.Column(db.Text, nullable=False, default="{}")
    started_at: datetime | None = db.Column(db.DateTime, nullable=True)
    finished_at: datetime | None = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    events = db.relationship(
        "CipProcessingEvent",
        back_populates="job",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="CipProcessingEvent.id",
    )

    def __repr__(self) -> str:
        return f"<CipProcessingJob {self.job_id} status={self.status}>"


class CipProcessingEvent(db.Model):
    """Append-only stage transition / diagnostic event for a CIP job."""

    __tablename__ = "cip_processing_events"
    __table_args__ = (db.Index("ix_cip_events_job_stage", "job_id", "stage"),)

    id: int = db.Column(db.Integer, primary_key=True)
    event_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    job_id: str = db.Column(
        db.String(64),
        db.ForeignKey("cip_processing_jobs.job_id"),
        nullable=False,
        index=True,
    )
    stage: str = db.Column(db.String(64), nullable=False)
    event_type: str = db.Column(db.String(64), nullable=False, default="stage")
    status: str = db.Column(db.String(32), nullable=False, default="started")
    message: str = db.Column(db.String(512), nullable=False, default="")
    diagnostics_json: str = db.Column(db.Text, nullable=False, default="{}")
    error_message: str | None = db.Column(db.Text, nullable=True)
    started_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    finished_at: datetime | None = db.Column(db.DateTime, nullable=True)
    duration_ms: int | None = db.Column(db.Integer, nullable=True)

    job = db.relationship("CipProcessingJob", back_populates="events")

    def __repr__(self) -> str:
        return f"<CipProcessingEvent {self.event_id} stage={self.stage}>"


class CipExtractedDocument(db.Model):
    """Extraction root — separate from curriculum business entities."""

    __tablename__ = "cip_extracted_documents"

    id: int = db.Column(db.Integer, primary_key=True)
    extraction_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    document_id: int = db.Column(
        db.Integer,
        db.ForeignKey("studio_foundation_documents.id"),
        nullable=False,
        index=True,
    )
    job_id: str = db.Column(db.String(64), nullable=False, index=True)
    page_count: int = db.Column(db.Integer, nullable=False, default=0)
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    diagnostics_json: str = db.Column(db.Text, nullable=False, default="[]")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    pages = db.relationship(
        "CipExtractedPage",
        back_populates="document",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="CipExtractedPage.page_number",
    )


class CipExtractedPage(db.Model):
    """One extracted PDF page."""

    __tablename__ = "cip_extracted_pages"
    __table_args__ = (
        db.UniqueConstraint(
            "extraction_id",
            "page_number",
            name="uq_cip_extracted_pages_extraction_page",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    extraction_id: str = db.Column(
        db.String(64),
        db.ForeignKey("cip_extracted_documents.extraction_id"),
        nullable=False,
        index=True,
    )
    page_number: int = db.Column(db.Integer, nullable=False)
    width: float | None = db.Column(db.Float, nullable=True)
    height: float | None = db.Column(db.Float, nullable=True)
    raw_text: str = db.Column(db.Text, nullable=False, default="")

    document = db.relationship("CipExtractedDocument", back_populates="pages")
    blocks = db.relationship(
        "CipExtractedBlock",
        back_populates="page",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="CipExtractedBlock.order_index",
    )


class CipExtractedBlock(db.Model):
    """Paragraph / heading / table / image block on a page."""

    __tablename__ = "cip_extracted_blocks"
    __table_args__ = (db.Index("ix_cip_blocks_page_order", "page_id", "order_index"),)

    id: int = db.Column(db.Integer, primary_key=True)
    block_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    page_id: int = db.Column(
        db.Integer,
        db.ForeignKey("cip_extracted_pages.id"),
        nullable=False,
        index=True,
    )
    kind: str = db.Column(db.String(32), nullable=False, default="paragraph")
    text: str = db.Column(db.Text, nullable=False, default="")
    order_index: int = db.Column(db.Integer, nullable=False, default=0)
    bbox_json: str | None = db.Column(db.Text, nullable=True)
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")

    page = db.relationship("CipExtractedPage", back_populates="blocks")


class CipStructuralNode(db.Model):
    """Hierarchical educational structure node."""

    __tablename__ = "cip_structural_nodes"
    __table_args__ = (
        db.Index("ix_cip_struct_parse_parent", "parse_id", "parent_node_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    node_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    parse_id: str = db.Column(db.String(64), nullable=False, index=True)
    document_id: int = db.Column(db.Integer, nullable=False, index=True)
    parent_node_id: str | None = db.Column(db.String(64), nullable=True, index=True)
    kind: str = db.Column(db.String(64), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    text: str = db.Column(db.Text, nullable=False, default="")
    level: int = db.Column(db.Integer, nullable=False, default=0)
    source_page: int | None = db.Column(db.Integer, nullable=True)
    source_block_ids_json: str = db.Column(db.Text, nullable=False, default="[]")
    confidence: float = db.Column(db.Float, nullable=False, default=1.0)
    needs_review: bool = db.Column(db.Boolean, nullable=False, default=False)
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CipCurriculumEntity(db.Model):
    """Mapped curriculum knowledge entity (CIP graph node payload)."""

    __tablename__ = "cip_curriculum_entities"
    __table_args__ = (
        db.Index("ix_cip_entities_doc_kind", "document_id", "kind"),
        db.Index("ix_cip_entities_parent", "parent_entity_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    entity_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    map_id: str = db.Column(db.String(64), nullable=False, index=True)
    document_id: int = db.Column(db.Integer, nullable=False, index=True)
    kind: str = db.Column(db.String(64), nullable=False)
    title: str = db.Column(db.String(512), nullable=False, default="")
    body: str = db.Column(db.Text, nullable=False, default="")
    parent_entity_id: str | None = db.Column(db.String(64), nullable=True)
    version_label: str = db.Column(db.String(64), nullable=False, default="")
    source_pages_json: str = db.Column(db.Text, nullable=False, default="[]")
    structural_node_id: str | None = db.Column(db.String(64), nullable=True)
    confidence: float = db.Column(db.Float, nullable=False, default=1.0)
    needs_review: bool = db.Column(db.Boolean, nullable=False, default=False)
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CipKnowledgeRelation(db.Model):
    """Directed knowledge-graph edge between curriculum entities."""

    __tablename__ = "cip_knowledge_relations"
    __table_args__ = (
        db.Index(
            "ix_cip_relations_from_to",
            "from_entity_id",
            "to_entity_id",
            "relation_type",
        ),
        db.Index("ix_cip_relations_document", "document_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    relation_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    graph_id: str = db.Column(db.String(64), nullable=False, index=True)
    document_id: int = db.Column(db.Integer, nullable=False)
    relation_type: str = db.Column(db.String(64), nullable=False)
    from_entity_id: str = db.Column(db.String(64), nullable=False, index=True)
    to_entity_id: str = db.Column(db.String(64), nullable=False, index=True)
    confidence: float = db.Column(db.Float, nullable=False, default=1.0)
    needs_review: bool = db.Column(db.Boolean, nullable=False, default=False)
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


# ---------------------------------------------------------------------------
# CIP-002 — Provenance, confidence, review, validation, audit, metrics
# ---------------------------------------------------------------------------


class CipProvenanceRecord(db.Model):
    """Immutable provenance for one curriculum entity or relation."""

    __tablename__ = "cip_provenance_records"
    __table_args__ = (
        db.Index("ix_cip_prov_subject", "subject_kind", "subject_id"),
        db.Index("ix_cip_prov_document", "source_document_id"),
        db.Index("ix_cip_prov_job", "pipeline_job_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    provenance_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    subject_kind: str = db.Column(db.String(32), nullable=False)
    subject_id: str = db.Column(db.String(64), nullable=False)
    source_document_id: int = db.Column(db.Integer, nullable=False)
    source_version_label: str = db.Column(db.String(64), nullable=False, default="")
    source_pages_csv: str = db.Column(db.String(512), nullable=False, default="")
    source_paragraphs_csv: str = db.Column(db.String(512), nullable=False, default="")
    source_block_ids_csv: str = db.Column(db.Text, nullable=False, default="")
    parser_version: str = db.Column(db.String(64), nullable=False, default="")
    mapper_version: str = db.Column(db.String(64), nullable=False, default="")
    graph_builder_version: str = db.Column(db.String(64), nullable=False, default="")
    pipeline_job_id: str = db.Column(db.String(64), nullable=False, default="")
    extraction_id: str = db.Column(db.String(64), nullable=False, default="")
    parse_id: str = db.Column(db.String(64), nullable=False, default="")
    map_id: str = db.Column(db.String(64), nullable=False, default="")
    graph_id: str = db.Column(db.String(64), nullable=False, default="")
    chain_stage: str = db.Column(db.String(64), nullable=False, default="")
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    evidence = db.relationship(
        "CipProvenanceEvidence",
        back_populates="provenance",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="CipProvenanceEvidence.id",
    )


class CipProvenanceEvidence(db.Model):
    """Supporting evidence rows for a provenance record."""

    __tablename__ = "cip_provenance_evidence"
    __table_args__ = (db.Index("ix_cip_prov_ev_prov", "provenance_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    evidence_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    provenance_id: str = db.Column(
        db.String(64),
        db.ForeignKey("cip_provenance_records.provenance_id"),
        nullable=False,
    )
    page_number: int | None = db.Column(db.Integer, nullable=True)
    paragraph_index: int | None = db.Column(db.Integer, nullable=True)
    block_id: str | None = db.Column(db.String(64), nullable=True)
    excerpt: str = db.Column(db.Text, nullable=False, default="")
    evidence_role: str = db.Column(db.String(64), nullable=False, default="source")

    provenance = db.relationship("CipProvenanceRecord", back_populates="evidence")


class CipConfidenceRecord(db.Model):
    """Explainable confidence score for an entity or relation."""

    __tablename__ = "cip_confidence_records"
    __table_args__ = (
        db.Index("ix_cip_conf_subject", "subject_kind", "subject_id"),
        db.Index("ix_cip_conf_needs_review", "needs_review"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    confidence_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    subject_kind: str = db.Column(db.String(32), nullable=False)
    subject_id: str = db.Column(db.String(64), nullable=False)
    score: float = db.Column(db.Float, nullable=False, default=0.0)
    band: str = db.Column(db.String(32), nullable=False, default="very_low")
    reason: str = db.Column(db.String(512), nullable=False, default="")
    needs_review: bool = db.Column(db.Boolean, nullable=False, default=False)
    review_threshold: float = db.Column(db.Float, nullable=False, default=0.6)
    provenance_id: str | None = db.Column(db.String(64), nullable=True)
    document_id: int = db.Column(db.Integer, nullable=False, default=0, index=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    factors = db.relationship(
        "CipConfidenceFactor",
        back_populates="confidence",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="CipConfidenceFactor.id",
    )


class CipConfidenceFactor(db.Model):
    """Named contribution factor for a confidence record."""

    __tablename__ = "cip_confidence_factors"
    __table_args__ = (db.Index("ix_cip_conf_fac_conf", "confidence_id"),)

    id: int = db.Column(db.Integer, primary_key=True)
    factor_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    confidence_id: str = db.Column(
        db.String(64),
        db.ForeignKey("cip_confidence_records.confidence_id"),
        nullable=False,
    )
    code: str = db.Column(db.String(64), nullable=False, default="")
    label: str = db.Column(db.String(256), nullable=False, default="")
    weight: float = db.Column(db.Float, nullable=False, default=0.0)
    contribution: float = db.Column(db.Float, nullable=False, default=0.0)
    detail: str = db.Column(db.String(512), nullable=False, default="")

    confidence = db.relationship("CipConfidenceRecord", back_populates="factors")


class CipReviewRecord(db.Model):
    """Append-only Founder review decision."""

    __tablename__ = "cip_review_records"
    __table_args__ = (
        db.Index("ix_cip_review_subject", "subject_kind", "subject_id"),
        db.Index("ix_cip_review_status", "review_status"),
        db.Index("ix_cip_review_workspace", "workspace_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    review_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    subject_kind: str = db.Column(db.String(32), nullable=False)
    subject_id: str = db.Column(db.String(64), nullable=False)
    document_id: int = db.Column(db.Integer, nullable=False, index=True)
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    decision: str = db.Column(db.String(32), nullable=False)
    review_status: str = db.Column(db.String(32), nullable=False)
    verification_status: str = db.Column(db.String(32), nullable=False)
    actor_id: str = db.Column(db.String(128), nullable=False, default="")
    reason: str = db.Column(db.Text, nullable=False, default="")
    suggested_learning_objective: str = db.Column(
        db.String(128), nullable=False, default=""
    )
    remap_target_id: str = db.Column(db.String(64), nullable=False, default="")
    confidence_at_review: float = db.Column(db.Float, nullable=False, default=0.0)
    pipeline_job_id: str = db.Column(db.String(64), nullable=False, default="")
    provenance_id: str | None = db.Column(db.String(64), nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CipValidationReport(db.Model):
    """Validation report root for one graph snapshot."""

    __tablename__ = "cip_validation_reports"
    __table_args__ = (
        db.Index("ix_cip_val_report_document", "document_id"),
        db.Index("ix_cip_val_report_graph", "graph_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    report_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    document_id: int = db.Column(db.Integer, nullable=False)
    graph_id: str = db.Column(db.String(64), nullable=False, default="")
    map_id: str = db.Column(db.String(64), nullable=False, default="")
    pipeline_job_id: str = db.Column(db.String(64), nullable=False, default="")
    issue_count: int = db.Column(db.Integer, nullable=False, default=0)
    error_count: int = db.Column(db.Integer, nullable=False, default=0)
    warning_count: int = db.Column(db.Integer, nullable=False, default=0)
    passed: bool = db.Column(db.Boolean, nullable=False, default=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

    issues = db.relationship(
        "CipValidationIssue",
        back_populates="report",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="CipValidationIssue.id",
    )


class CipValidationIssue(db.Model):
    """One finding within a validation report."""

    __tablename__ = "cip_validation_issues"
    __table_args__ = (
        db.Index("ix_cip_val_issue_report", "report_id"),
        db.Index("ix_cip_val_issue_kind", "kind"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    issue_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    report_id: str = db.Column(
        db.String(64),
        db.ForeignKey("cip_validation_reports.report_id"),
        nullable=False,
    )
    kind: str = db.Column(db.String(64), nullable=False)
    severity: str = db.Column(db.String(32), nullable=False, default="warning")
    message: str = db.Column(db.String(512), nullable=False, default="")
    subject_kind: str = db.Column(db.String(32), nullable=False, default="")
    subject_id: str = db.Column(db.String(64), nullable=False, default="")
    related_ids_csv: str = db.Column(db.Text, nullable=False, default="")
    document_id: int | None = db.Column(db.Integer, nullable=True)

    report = db.relationship("CipValidationReport", back_populates="issues")


class CipAuditEvent(db.Model):
    """Append-only CIP audit trail event."""

    __tablename__ = "cip_audit_events"
    __table_args__ = (
        db.Index("ix_cip_audit_action", "action"),
        db.Index("ix_cip_audit_subject", "subject_kind", "subject_id"),
        db.Index("ix_cip_audit_workspace", "workspace_id"),
        db.Index("ix_cip_audit_job", "pipeline_job_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    event_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    action: str = db.Column(db.String(64), nullable=False)
    actor_id: str = db.Column(db.String(128), nullable=False, default="")
    subject_kind: str = db.Column(db.String(32), nullable=False, default="")
    subject_id: str = db.Column(db.String(64), nullable=False, default="")
    document_id: int | None = db.Column(db.Integer, nullable=True)
    pipeline_job_id: str = db.Column(db.String(64), nullable=False, default="")
    document_version: str = db.Column(db.String(64), nullable=False, default="")
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    message: str = db.Column(db.String(512), nullable=False, default="")
    attributes_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


class CipQualityMetrics(db.Model):
    """Pipeline quality metrics snapshot."""

    __tablename__ = "cip_quality_metrics"
    __table_args__ = (
        db.Index("ix_cip_metrics_document", "document_id"),
        db.Index("ix_cip_metrics_workspace", "workspace_id"),
        db.Index("ix_cip_metrics_job", "pipeline_job_id"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    metrics_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    document_id: int = db.Column(db.Integer, nullable=False)
    pipeline_job_id: str = db.Column(db.String(64), nullable=False, default="")
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    extraction_success_rate: float = db.Column(db.Float, nullable=False, default=0.0)
    parser_success_rate: float = db.Column(db.Float, nullable=False, default=0.0)
    mean_mapping_confidence: float = db.Column(db.Float, nullable=False, default=0.0)
    graph_completeness: float = db.Column(db.Float, nullable=False, default=0.0)
    graph_consistency: float = db.Column(db.Float, nullable=False, default=0.0)
    entities_requiring_review: int = db.Column(db.Integer, nullable=False, default=0)
    founder_approvals: int = db.Column(db.Integer, nullable=False, default=0)
    founder_corrections: int = db.Column(db.Integer, nullable=False, default=0)
    entity_count: int = db.Column(db.Integer, nullable=False, default=0)
    relation_count: int = db.Column(db.Integer, nullable=False, default=0)
    validation_error_count: int = db.Column(db.Integer, nullable=False, default=0)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)


# ---------------------------------------------------------------------------
# CIP-003 — Embedding metadata, local vector store, retrieval logs
# ---------------------------------------------------------------------------


class CipEmbeddingRecord(db.Model):
    """Metadata for one educational-entity embedding (no vector payload)."""

    __tablename__ = "cip_embedding_records"
    __table_args__ = (
        db.Index("ix_cip_embed_entity", "entity_id"),
        db.Index("ix_cip_embed_document", "document_id"),
        db.Index("ix_cip_embed_workspace", "workspace_id"),
        db.Index("ix_cip_embed_status", "status"),
        db.UniqueConstraint(
            "entity_id",
            "embedding_version",
            name="uq_cip_embed_entity_ver",
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    embedding_id: str = db.Column(
        db.String(64), nullable=False, unique=True, index=True
    )
    entity_id: str = db.Column(db.String(64), nullable=False)
    entity_kind: str = db.Column(db.String(64), nullable=False, default="")
    document_id: int = db.Column(db.Integer, nullable=False, default=0)
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    vector_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    model_name: str = db.Column(db.String(128), nullable=False, default="")
    embedding_version: str = db.Column(db.String(32), nullable=False, default="1")
    dimensions: int = db.Column(db.Integer, nullable=False, default=0)
    status: str = db.Column(db.String(32), nullable=False, default="pending")
    content_fingerprint: str = db.Column(db.String(64), nullable=False, default="")
    provenance_id: str | None = db.Column(db.String(64), nullable=True)
    graph_id: str = db.Column(db.String(64), nullable=False, default="")
    job_id: str = db.Column(db.String(64), nullable=False, default="")
    error_message: str = db.Column(db.Text, nullable=False, default="")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )


class CipLocalVectorEntry(db.Model):
    """Infrastructure-owned local vector payload (LocalVectorStoreAdapter only)."""

    __tablename__ = "cip_local_vector_entries"
    __table_args__ = (db.Index("ix_cip_local_vec_dims", "dimensions"),)

    id: int = db.Column(db.Integer, primary_key=True)
    vector_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    dimensions: int = db.Column(db.Integer, nullable=False, default=0)
    vector_json: str = db.Column(db.Text, nullable=False, default="[]")
    metadata_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )


class CipRetrievalLog(db.Model):
    """Append-only retrieval request log for diagnostics and auditability."""

    __tablename__ = "cip_retrieval_logs"
    __table_args__ = (
        db.Index("ix_cip_retrieval_workspace", "workspace_id"),
        db.Index("ix_cip_retrieval_profile", "profile"),
        db.Index("ix_cip_retrieval_created", "created_at"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    log_id: str = db.Column(db.String(64), nullable=False, unique=True, index=True)
    workspace_id: str = db.Column(db.String(128), nullable=False, default="")
    profile: str = db.Column(db.String(64), nullable=False, default="")
    intent: str = db.Column(db.String(64), nullable=False, default="")
    query_text: str = db.Column(db.Text, nullable=False, default="")
    document_id: int | None = db.Column(db.Integer, nullable=True)
    result_count: int = db.Column(db.Integer, nullable=False, default=0)
    top_entity_ids_csv: str = db.Column(db.Text, nullable=False, default="")
    diagnostics_json: str = db.Column(db.Text, nullable=False, default="{}")
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=_utc_now)

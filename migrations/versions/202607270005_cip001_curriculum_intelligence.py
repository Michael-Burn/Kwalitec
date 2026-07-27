"""CIP-001 curriculum intelligence pipeline tables.

Revision ID: 202607270005
Revises: 202607270004
Create Date: 2026-07-27 14:00:00.000000

Normalised tables for processing jobs, extraction, structural parse,
curriculum entities, and knowledge-graph relations. No PDF bytes. No embeddings.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270005"
down_revision: Union[str, None] = "202607270004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cip_processing_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("storage_key", sa.String(length=1024), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("checkpoint_stage", sa.String(length=64), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("cancel_requested", sa.Boolean(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("diagnostics_json", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["studio_foundation_documents.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id"),
    )
    op.create_index("ix_cip_processing_jobs_job_id", "cip_processing_jobs", ["job_id"])
    op.create_index(
        "ix_cip_processing_jobs_document_id", "cip_processing_jobs", ["document_id"]
    )
    op.create_index(
        "ix_cip_processing_jobs_status", "cip_processing_jobs", ["status"]
    )
    op.create_index("ix_cip_jobs_document_status", "cip_processing_jobs", ["document_id", "status"])
    op.create_index("ix_cip_jobs_workspace", "cip_processing_jobs", ["workspace_id"])

    op.create_table(
        "cip_processing_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("stage", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("message", sa.String(length=512), nullable=False),
        sa.Column("diagnostics_json", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["job_id"], ["cip_processing_jobs.job_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    op.create_index(
        "ix_cip_processing_events_event_id", "cip_processing_events", ["event_id"]
    )
    op.create_index(
        "ix_cip_processing_events_job_id", "cip_processing_events", ["job_id"]
    )
    op.create_index(
        "ix_cip_events_job_stage", "cip_processing_events", ["job_id", "stage"]
    )

    op.create_table(
        "cip_extracted_documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("extraction_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("diagnostics_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["studio_foundation_documents.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("extraction_id"),
    )
    op.create_index(
        "ix_cip_extracted_documents_extraction_id",
        "cip_extracted_documents",
        ["extraction_id"],
    )
    op.create_index(
        "ix_cip_extracted_documents_document_id",
        "cip_extracted_documents",
        ["document_id"],
    )
    op.create_index(
        "ix_cip_extracted_documents_job_id", "cip_extracted_documents", ["job_id"]
    )

    op.create_table(
        "cip_extracted_pages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("extraction_id", sa.String(length=64), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("width", sa.Float(), nullable=True),
        sa.Column("height", sa.Float(), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["extraction_id"], ["cip_extracted_documents.extraction_id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "extraction_id",
            "page_number",
            name="uq_cip_extracted_pages_extraction_page",
        ),
    )
    op.create_index(
        "ix_cip_extracted_pages_extraction_id",
        "cip_extracted_pages",
        ["extraction_id"],
    )

    op.create_table(
        "cip_extracted_blocks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("block_id", sa.String(length=64), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("bbox_json", sa.Text(), nullable=True),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["page_id"], ["cip_extracted_pages.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("block_id"),
    )
    op.create_index(
        "ix_cip_extracted_blocks_block_id", "cip_extracted_blocks", ["block_id"]
    )
    op.create_index(
        "ix_cip_extracted_blocks_page_id", "cip_extracted_blocks", ["page_id"]
    )
    op.create_index(
        "ix_cip_blocks_page_order", "cip_extracted_blocks", ["page_id", "order_index"]
    )

    op.create_table(
        "cip_structural_nodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.String(length=64), nullable=False),
        sa.Column("parse_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("parent_node_id", sa.String(length=64), nullable=True),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("source_page", sa.Integer(), nullable=True),
        sa.Column("source_block_ids_json", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("node_id"),
    )
    op.create_index(
        "ix_cip_structural_nodes_node_id", "cip_structural_nodes", ["node_id"]
    )
    op.create_index(
        "ix_cip_structural_nodes_parse_id", "cip_structural_nodes", ["parse_id"]
    )
    op.create_index(
        "ix_cip_structural_nodes_document_id", "cip_structural_nodes", ["document_id"]
    )
    op.create_index(
        "ix_cip_structural_nodes_parent_node_id",
        "cip_structural_nodes",
        ["parent_node_id"],
    )
    op.create_index(
        "ix_cip_struct_parse_parent",
        "cip_structural_nodes",
        ["parse_id", "parent_node_id"],
    )

    op.create_table(
        "cip_curriculum_entities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("map_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("parent_entity_id", sa.String(length=64), nullable=True),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("source_pages_json", sa.Text(), nullable=False),
        sa.Column("structural_node_id", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entity_id"),
    )
    op.create_index(
        "ix_cip_curriculum_entities_entity_id", "cip_curriculum_entities", ["entity_id"]
    )
    op.create_index(
        "ix_cip_curriculum_entities_map_id", "cip_curriculum_entities", ["map_id"]
    )
    op.create_index(
        "ix_cip_curriculum_entities_document_id",
        "cip_curriculum_entities",
        ["document_id"],
    )
    op.create_index(
        "ix_cip_entities_doc_kind", "cip_curriculum_entities", ["document_id", "kind"]
    )
    op.create_index(
        "ix_cip_entities_parent", "cip_curriculum_entities", ["parent_entity_id"]
    )

    op.create_table(
        "cip_knowledge_relations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("relation_id", sa.String(length=64), nullable=False),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=64), nullable=False),
        sa.Column("from_entity_id", sa.String(length=64), nullable=False),
        sa.Column("to_entity_id", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("attributes_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("relation_id"),
    )
    op.create_index(
        "ix_cip_knowledge_relations_relation_id",
        "cip_knowledge_relations",
        ["relation_id"],
    )
    op.create_index(
        "ix_cip_knowledge_relations_graph_id", "cip_knowledge_relations", ["graph_id"]
    )
    op.create_index(
        "ix_cip_knowledge_relations_from_entity_id",
        "cip_knowledge_relations",
        ["from_entity_id"],
    )
    op.create_index(
        "ix_cip_knowledge_relations_to_entity_id",
        "cip_knowledge_relations",
        ["to_entity_id"],
    )
    op.create_index(
        "ix_cip_relations_from_to",
        "cip_knowledge_relations",
        ["from_entity_id", "to_entity_id", "relation_type"],
    )
    op.create_index(
        "ix_cip_relations_document", "cip_knowledge_relations", ["document_id"]
    )


def downgrade() -> None:
    op.drop_table("cip_knowledge_relations")
    op.drop_table("cip_curriculum_entities")
    op.drop_table("cip_structural_nodes")
    op.drop_table("cip_extracted_blocks")
    op.drop_table("cip_extracted_pages")
    op.drop_table("cip_extracted_documents")
    op.drop_table("cip_processing_events")
    op.drop_table("cip_processing_jobs")

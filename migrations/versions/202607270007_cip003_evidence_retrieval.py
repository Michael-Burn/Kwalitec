"""CIP-003 embedding metadata, local vector store, and retrieval logs.

Revision ID: 202607270007
Revises: 202607270006
Create Date: 2026-07-27 18:00:00.000000

Additive CIP-003 schema. Does not alter CIP-001/CIP-002 tables.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270007"
down_revision: Union[str, None] = "202607270006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cip_embedding_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("embedding_id", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("entity_kind", sa.String(length=64), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("vector_id", sa.String(length=64), nullable=False),
        sa.Column("model_name", sa.String(length=128), nullable=False),
        sa.Column("embedding_version", sa.String(length=32), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("content_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("provenance_id", sa.String(length=64), nullable=True),
        sa.Column("graph_id", sa.String(length=64), nullable=False),
        sa.Column("job_id", sa.String(length=64), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "entity_id", "embedding_version", name="uq_cip_embed_entity_ver"
        ),
    )
    op.create_index(
        "ix_cip_embedding_records_embedding_id",
        "cip_embedding_records",
        ["embedding_id"],
        unique=True,
    )
    op.create_index(
        "ix_cip_embed_entity", "cip_embedding_records", ["entity_id"], unique=False
    )
    op.create_index(
        "ix_cip_embed_document",
        "cip_embedding_records",
        ["document_id"],
        unique=False,
    )
    op.create_index(
        "ix_cip_embed_workspace",
        "cip_embedding_records",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_cip_embed_status", "cip_embedding_records", ["status"], unique=False
    )
    op.create_index(
        "ix_cip_embedding_records_vector_id",
        "cip_embedding_records",
        ["vector_id"],
        unique=True,
    )

    op.create_table(
        "cip_local_vector_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vector_id", sa.String(length=64), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("vector_json", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cip_local_vector_entries_vector_id",
        "cip_local_vector_entries",
        ["vector_id"],
        unique=True,
    )
    op.create_index(
        "ix_cip_local_vec_dims",
        "cip_local_vector_entries",
        ["dimensions"],
        unique=False,
    )

    op.create_table(
        "cip_retrieval_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("log_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=128), nullable=False),
        sa.Column("profile", sa.String(length=64), nullable=False),
        sa.Column("intent", sa.String(length=64), nullable=False),
        sa.Column("query_text", sa.Text(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("result_count", sa.Integer(), nullable=False),
        sa.Column("top_entity_ids_csv", sa.Text(), nullable=False),
        sa.Column("diagnostics_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cip_retrieval_logs_log_id",
        "cip_retrieval_logs",
        ["log_id"],
        unique=True,
    )
    op.create_index(
        "ix_cip_retrieval_workspace",
        "cip_retrieval_logs",
        ["workspace_id"],
        unique=False,
    )
    op.create_index(
        "ix_cip_retrieval_profile",
        "cip_retrieval_logs",
        ["profile"],
        unique=False,
    )
    op.create_index(
        "ix_cip_retrieval_created",
        "cip_retrieval_logs",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_cip_retrieval_created", table_name="cip_retrieval_logs")
    op.drop_index("ix_cip_retrieval_profile", table_name="cip_retrieval_logs")
    op.drop_index("ix_cip_retrieval_workspace", table_name="cip_retrieval_logs")
    op.drop_index("ix_cip_retrieval_logs_log_id", table_name="cip_retrieval_logs")
    op.drop_table("cip_retrieval_logs")

    op.drop_index("ix_cip_local_vec_dims", table_name="cip_local_vector_entries")
    op.drop_index(
        "ix_cip_local_vector_entries_vector_id", table_name="cip_local_vector_entries"
    )
    op.drop_table("cip_local_vector_entries")

    op.drop_index(
        "ix_cip_embedding_records_vector_id", table_name="cip_embedding_records"
    )
    op.drop_index("ix_cip_embed_status", table_name="cip_embedding_records")
    op.drop_index("ix_cip_embed_workspace", table_name="cip_embedding_records")
    op.drop_index("ix_cip_embed_document", table_name="cip_embedding_records")
    op.drop_index("ix_cip_embed_entity", table_name="cip_embedding_records")
    op.drop_index(
        "ix_cip_embedding_records_embedding_id", table_name="cip_embedding_records"
    )
    op.drop_table("cip_embedding_records")

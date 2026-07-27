"""Add curriculum document file metadata columns (Phase 1 upload).

Revision ID: 202607270004
Revises: 202607270003
Create Date: 2026-07-27 12:40:00.000000

Extends studio_foundation_documents with filename / size / checksum /
storage_key / versioning / processing_stage. Does not store PDF bytes.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270004"
down_revision: Union[str, None] = "202607270003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("studio_foundation_documents", schema=None) as batch_op:
        batch_op.add_column(sa.Column("workspace_id", sa.String(length=128), nullable=True))
        batch_op.add_column(
            sa.Column("original_filename", sa.String(length=512), nullable=True)
        )
        batch_op.add_column(
            sa.Column("content_type", sa.String(length=128), nullable=True)
        )
        batch_op.add_column(sa.Column("byte_size", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column("checksum_sha256", sa.String(length=64), nullable=True)
        )
        batch_op.add_column(
            sa.Column("storage_key", sa.String(length=1024), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "version_number",
                sa.Integer(),
                nullable=False,
                server_default="1",
            )
        )
        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("1"),
            )
        )
        batch_op.add_column(
            sa.Column(
                "processing_stage",
                sa.String(length=64),
                nullable=True,
                server_default="uploaded",
            )
        )
        batch_op.create_index(
            "ix_studio_foundation_documents_workspace_id",
            ["workspace_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_documents_checksum_sha256",
            ["checksum_sha256"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_documents_is_active",
            ["is_active"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_documents_workspace_kind_active",
            ["workspace_id", "kind", "is_active"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("studio_foundation_documents", schema=None) as batch_op:
        batch_op.drop_index("ix_studio_foundation_documents_workspace_kind_active")
        batch_op.drop_index("ix_studio_foundation_documents_is_active")
        batch_op.drop_index("ix_studio_foundation_documents_checksum_sha256")
        batch_op.drop_index("ix_studio_foundation_documents_workspace_id")
        batch_op.drop_column("processing_stage")
        batch_op.drop_column("is_active")
        batch_op.drop_column("version_number")
        batch_op.drop_column("storage_key")
        batch_op.drop_column("checksum_sha256")
        batch_op.drop_column("byte_size")
        batch_op.drop_column("content_type")
        batch_op.drop_column("original_filename")
        batch_op.drop_column("workspace_id")

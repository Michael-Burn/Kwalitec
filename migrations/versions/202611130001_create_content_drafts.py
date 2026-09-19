"""Create content_drafts table for Founder Console content lifecycle.

Revision ID: 202611130001
Revises: 202611120001
Create Date: 2026-09-19 13:00:00.000000

Foundational draft/lifecycle store for educational package authoring.
Drafts are never on the student package resolution path.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "202611130001"
down_revision: str | None = "202611120001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "content_drafts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.String(length=36), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("canonical_topic_id", sa.String(length=36), nullable=True),
        sa.Column("topic_code", sa.String(length=128), nullable=False),
        sa.Column("objective_id", sa.String(length=128), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("lifecycle_status", sa.String(length=32), nullable=False),
        sa.Column("created_by", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("ai_assisted", sa.Boolean(), nullable=False),
        sa.Column("ai_proposed_json", sa.Text(), nullable=True),
        sa.Column("human_edited_json", sa.Text(), nullable=True),
        sa.Column("approved_by", sa.String(length=128), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("live_package_id", sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(
            ["canonical_topic_id"],
            ["canonical_curriculum_topic.canonical_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "content_id",
            "revision",
            name="uq_content_drafts_content_revision",
        ),
    )
    with op.batch_alter_table("content_drafts", schema=None) as batch_op:
        batch_op.create_index(
            "ix_content_drafts_content_id",
            ["content_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_content_drafts_lifecycle_status",
            ["lifecycle_status"],
            unique=False,
        )
        batch_op.create_index(
            "ix_content_drafts_subject_id",
            ["subject_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_content_drafts_canonical_topic_id",
            ["canonical_topic_id"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("content_drafts", schema=None) as batch_op:
        batch_op.drop_index("ix_content_drafts_canonical_topic_id")
        batch_op.drop_index("ix_content_drafts_subject_id")
        batch_op.drop_index("ix_content_drafts_lifecycle_status")
        batch_op.drop_index("ix_content_drafts_content_id")
    op.drop_table("content_drafts")

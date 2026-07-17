"""Create Founder Vision Journal tables (V1SP-001D).

Revision ID: 202607170002
Revises: 202607170001
Create Date: 2026-07-17 19:00:00.000000

V1SP-001D — Founder Vision Journal.

Stores structured vision entries, status history, relationships, and
promotion placeholders. Does not modify educational tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607170002"
down_revision: str | None = "202607170001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "vision_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column(
            "potential_value",
            sa.String(length=32),
            nullable=False,
            server_default="medium",
        ),
        sa.Column("expected_impact", sa.Text(), nullable=False),
        sa.Column(
            "target_version",
            sa.String(length=32),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
            server_default="vision",
        ),
        sa.Column(
            "tags_csv",
            sa.String(length=500),
            nullable=False,
            server_default="",
        ),
        sa.Column("author_user_id", sa.Integer(), nullable=False),
        sa.Column("future_milestone", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["author_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("vision_entries", schema=None) as batch_op:
        batch_op.create_index("ix_vision_entries_title", ["title"], unique=False)
        batch_op.create_index(
            "ix_vision_entries_potential_value", ["potential_value"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_target_version", ["target_version"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_category", ["category"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_status", ["status"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_author_user_id", ["author_user_id"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_created_at", ["created_at"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_updated_at", ["updated_at"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entries_deleted_at", ["deleted_at"], unique=False
        )

    op.create_table(
        "vision_entry_status_transitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("from_status", sa.String(length=32), nullable=True),
        sa.Column("to_status", sa.String(length=32), nullable=False),
        sa.Column("changed_by_user_id", sa.Integer(), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("transitioned_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["changed_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["entry_id"], ["vision_entries.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table(
        "vision_entry_status_transitions", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_vision_entry_status_transitions_entry_id",
            ["entry_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_vision_entry_status_transitions_transitioned_at",
            ["transitioned_at"],
            unique=False,
        )

    op.create_table(
        "vision_entry_relations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("from_entry_id", sa.Integer(), nullable=False),
        sa.Column("to_entry_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["from_entry_id"], ["vision_entries.id"]),
        sa.ForeignKeyConstraint(["to_entry_id"], ["vision_entries.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "from_entry_id",
            "to_entry_id",
            "relation_type",
            name="uq_vision_relation",
        ),
    )
    with op.batch_alter_table("vision_entry_relations", schema=None) as batch_op:
        batch_op.create_index(
            "ix_vision_entry_relations_from_entry_id",
            ["from_entry_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_vision_entry_relations_to_entry_id",
            ["to_entry_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_vision_entry_relations_relation_type",
            ["relation_type"],
            unique=False,
        )

    op.create_table(
        "vision_entry_promotions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("placeholder_ref", sa.String(length=200), nullable=False),
        sa.Column("notes", sa.String(length=1000), nullable=True),
        sa.Column("promoted_by_user_id", sa.Integer(), nullable=False),
        sa.Column("promoted_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["entry_id"], ["vision_entries.id"]),
        sa.ForeignKeyConstraint(["promoted_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("vision_entry_promotions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_vision_entry_promotions_entry_id", ["entry_id"], unique=False
        )
        batch_op.create_index(
            "ix_vision_entry_promotions_promoted_at",
            ["promoted_at"],
            unique=False,
        )


def downgrade() -> None:
    op.drop_table("vision_entry_promotions")
    op.drop_table("vision_entry_relations")
    op.drop_table("vision_entry_status_transitions")
    op.drop_table("vision_entries")

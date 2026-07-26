"""PRD-001 Phase A — Analytics event store tables.

Revision ID: 202607240001
Revises: 202607230002
Create Date: 2026-07-24 00:00:00.000000

Append-only analytics_events, analytics_outbox, and analytics_audit_log.
Does not alter educational schema, Twin, EducationalState, or Evidence tables.
Feature flag ANALYTICS_EVENTS_V1 remains off by default — no runtime emits.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607240001"
down_revision: Union[str, None] = "202607230002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analytics_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("row_hmac", sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
        sa.UniqueConstraint(
            "user_id",
            "event_type",
            "idempotency_key",
            name="uq_analytics_events_idempotency",
        ),
    )
    with op.batch_alter_table("analytics_events", schema=None) as batch_op:
        batch_op.create_index(
            "ix_analytics_events_event_id", ["event_id"], unique=True
        )
        batch_op.create_index(
            "ix_analytics_events_event_type", ["event_type"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_events_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_events_correlation_id",
            ["correlation_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_analytics_events_occurred_at", ["occurred_at"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_events_created_at", ["created_at"], unique=False
        )

    op.create_table(
        "analytics_outbox",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("outbox_id", sa.String(length=64), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("outbox_id"),
        sa.UniqueConstraint(
            "user_id",
            "event_type",
            "idempotency_key",
            name="uq_analytics_outbox_idempotency",
        ),
    )
    with op.batch_alter_table("analytics_outbox", schema=None) as batch_op:
        batch_op.create_index(
            "ix_analytics_outbox_outbox_id", ["outbox_id"], unique=True
        )
        batch_op.create_index(
            "ix_analytics_outbox_event_id", ["event_id"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_outbox_event_type", ["event_type"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_outbox_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_outbox_status", ["status"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_outbox_created_at", ["created_at"], unique=False
        )

    op.create_table(
        "analytics_audit_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("audit_id", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("detail_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("audit_id"),
    )
    with op.batch_alter_table("analytics_audit_log", schema=None) as batch_op:
        batch_op.create_index(
            "ix_analytics_audit_log_audit_id", ["audit_id"], unique=True
        )
        batch_op.create_index(
            "ix_analytics_audit_log_action", ["action"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_audit_log_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_analytics_audit_log_created_at", ["created_at"], unique=False
        )


def downgrade() -> None:
    op.drop_table("analytics_audit_log")
    op.drop_table("analytics_outbox")
    op.drop_table("analytics_events")

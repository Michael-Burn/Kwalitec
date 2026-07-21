"""Add BR-004 product persistence tables.

Revision ID: 202607200002
Revises: 202607200001
Create Date: 2026-07-20
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "202607200002"
down_revision = "202607200001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "eos_user_accounts",
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("password_changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("row_version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_eos_user_accounts")),
        sa.UniqueConstraint("email", name=op.f("uq_eos_user_accounts_email")),
    )
    op.create_index(
        op.f("ix_eos_user_accounts_email"),
        "eos_user_accounts",
        ["email"],
        unique=True,
    )

    op.create_table(
        "eos_auth_tokens",
        sa.Column("token_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=128), nullable=False),
        sa.Column("purpose", sa.String(length=64), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("token_id", name=op.f("pk_eos_auth_tokens")),
        sa.UniqueConstraint(
            "purpose",
            "token_hash",
            name="uq_eos_auth_tokens_purpose_token_hash",
        ),
    )
    op.create_index(
        op.f("ix_eos_auth_tokens_user_id"),
        "eos_auth_tokens",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "eos_onboarding_sessions",
        sa.Column("onboarding_id", sa.String(length=128), nullable=False),
        sa.Column("student_id", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("current_step", sa.String(length=64), nullable=False),
        sa.Column("payloads", sa.JSON(), nullable=False),
        sa.Column("saved_steps", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("row_version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "onboarding_id", name=op.f("pk_eos_onboarding_sessions")
        ),
    )
    op.create_index(
        op.f("ix_eos_onboarding_sessions_student_id"),
        "eos_onboarding_sessions",
        ["student_id"],
        unique=False,
    )

    op.create_table(
        "eos_session_checkpoints",
        sa.Column("session_id", sa.String(length=128), nullable=False),
        sa.Column("events", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("row_version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "session_id", name=op.f("pk_eos_session_checkpoints")
        ),
    )


def downgrade() -> None:
    op.drop_table("eos_session_checkpoints")
    op.drop_index(
        op.f("ix_eos_onboarding_sessions_student_id"),
        table_name="eos_onboarding_sessions",
    )
    op.drop_table("eos_onboarding_sessions")
    op.drop_index(op.f("ix_eos_auth_tokens_user_id"), table_name="eos_auth_tokens")
    op.drop_table("eos_auth_tokens")
    op.drop_index(op.f("ix_eos_user_accounts_email"), table_name="eos_user_accounts")
    op.drop_table("eos_user_accounts")

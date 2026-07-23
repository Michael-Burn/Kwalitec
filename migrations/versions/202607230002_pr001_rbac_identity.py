"""PR-001 RBAC and account capabilities.

Revision ID: 202607230002
Revises: 202607230001
Create Date: 2026-07-23 20:00:00.000000

Adds durable ``user_roles`` and ``user_capabilities`` tables so one User
identity can hold multiple roles and portal permissions. Does not alter
educational schema.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607230002"
down_revision: Union[str, None] = "202607230001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "role", name="uq_user_roles_user_role"),
    )
    with op.batch_alter_table("user_roles", schema=None) as batch_op:
        batch_op.create_index("ix_user_roles_user_id", ["user_id"], unique=False)
        batch_op.create_index("ix_user_roles_role", ["role"], unique=False)

    op.create_table(
        "user_capabilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("capability", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "capability", name="uq_user_capabilities_user_cap"
        ),
    )
    with op.batch_alter_table("user_capabilities", schema=None) as batch_op:
        batch_op.create_index(
            "ix_user_capabilities_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_user_capabilities_capability", ["capability"], unique=False
        )


def downgrade() -> None:
    op.drop_table("user_capabilities")
    op.drop_table("user_roles")

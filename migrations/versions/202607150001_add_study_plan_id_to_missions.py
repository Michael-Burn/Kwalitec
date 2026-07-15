"""Add study_plan_id to missions for recommendation integrity (IA-001).

Revision ID: 202607150001
Revises: 202607130002
Create Date: 2026-07-15 08:00:00.000000
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607150001"
down_revision: str | None = "202607130002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("missions") as batch_op:
        batch_op.add_column(
            sa.Column(
                "study_plan_id",
                sa.Integer(),
                nullable=True,
                comment="Active study plan this mission was generated for",
            )
        )
        batch_op.create_foreign_key(
            "fk_missions_study_plan_id",
            "study_plans",
            ["study_plan_id"],
            ["id"],
        )
        batch_op.create_index(
            "ix_missions_user_date_study_plan",
            ["user_id", "mission_date", "study_plan_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("missions") as batch_op:
        batch_op.drop_index("ix_missions_user_date_study_plan")
        batch_op.drop_constraint("fk_missions_study_plan_id", type_="foreignkey")
        batch_op.drop_column("study_plan_id")

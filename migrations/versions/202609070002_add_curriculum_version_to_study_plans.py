"""Add curriculum_version to study_plans

Revision ID: 202609070002
Revises: 202609070001
Create Date: 2026-09-07 14:20:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "202609070002"
down_revision = "202609070001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.add_column(
            sa.Column(
                "curriculum_version",
                sa.String(20),
                nullable=True,
                default=None,
                comment="Curriculum version this plan was created against",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.drop_column("curriculum_version")
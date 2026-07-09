"""Add curriculum_topic_code to study_plans

Revision ID: 202609070003
Revises: 202609070002
Create Date: 2026-09-07 14:40:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "202609070003"
down_revision = "202609070002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.add_column(
            sa.Column(
                "curriculum_topic_code",
                sa.String(50),
                nullable=True,
                default=None,
                comment="Official curriculum topic code currently being studied (e.g., 'CS1-A')",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.drop_column("curriculum_topic_code")
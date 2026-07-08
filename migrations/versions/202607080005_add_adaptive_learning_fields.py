"""Add adaptive learning fields to topic_progress

Revision ID: 202607080005
Revises: 202607080004
Create Date: 2026-07-08 16:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "202607080005"
down_revision = "202607080004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add adaptive learning columns to topic_progress using batch mode for SQLite compatibility
    with op.batch_alter_table("topic_progress") as batch_op:
        batch_op.add_column(
            sa.Column(
                "mastery_score",
                sa.Float(),
                nullable=False,
                server_default="0.0",
                comment="Calculated mastery score from 0 to 100",
            ),
        )
        batch_op.add_column(
            sa.Column(
                "average_accuracy",
                sa.Float(),
                nullable=True,
                comment="Average accuracy across all study attempts (0-100)",
            ),
        )
        batch_op.add_column(
            sa.Column(
                "average_confidence",
                sa.Float(),
                nullable=True,
                comment="Average numeric confidence derived from confidence levels",
            ),
        )
        batch_op.add_column(
            sa.Column(
                "next_review_date",
                sa.Date(),
                nullable=True,
                comment="Scheduled date for the next review of this topic",
            ),
        )
        batch_op.add_column(
            sa.Column(
                "current_stage",
                sa.String(50),
                nullable=False,
                server_default="Not Started",
                comment="Learning stage: Not Started, Learning, Practising, Mastered, Needs Review",
            ),
        )


def downgrade() -> None:
    with op.batch_alter_table("topic_progress") as batch_op:
        batch_op.drop_column("current_stage")
        batch_op.drop_column("next_review_date")
        batch_op.drop_column("average_confidence")
        batch_op.drop_column("average_accuracy")
        batch_op.drop_column("mastery_score")
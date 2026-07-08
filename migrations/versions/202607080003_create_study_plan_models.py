"""Create study plan models

Revision ID: 202607080003
Revises: 202607080002
Create Date: 2026-07-08 11:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "202607080003"
down_revision = "202607080002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create study_plans table
    op.create_table(
        "study_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exam_name", sa.String(length=255), nullable=False),
        sa.Column("exam_sitting", sa.String(length=100), nullable=False),
        sa.Column("exam_date", sa.Date(), nullable=False),
        sa.Column("weekday_study_minutes", sa.Integer(), nullable=False),
        sa.Column("weekend_study_minutes", sa.Integer(), nullable=False),
        sa.Column("current_stage", sa.String(length=255), nullable=False),
        sa.Column("study_preference", sa.String(length=50), nullable=False, server_default="Mixed"),
        sa.Column("target_grade", sa.String(length=50), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create week_plans table
    op.create_table(
        "week_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("week_number", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("week_plans")
    op.drop_table("study_plans")

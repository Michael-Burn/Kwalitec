"""Create curriculum, learning, and topic_progress models

Revision ID: 202607080004
Revises: 202607080003
Create Date: 2026-07-08 14:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "202607080004"
down_revision = "202607080003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create curricula table first (needed for FK below)
    op.create_table(
        "curricula",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exam_name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Add curriculum_id to study_plans (references curricula which now exists)
    # Use batch mode for SQLite compatibility
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.add_column(
            sa.Column(
                "curriculum_id",
                sa.Integer(),
                nullable=True,
                comment="Associated curriculum for structured syllabus",
            ),
        )
        batch_op.create_foreign_key(
            "fk_study_plans_curriculum_id",
            "curricula",
            ["curriculum_id"],
            ["id"],
        )

    # Create topics table (self-referential FK via parent_topic_id)
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("curriculum_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_topic_id", sa.Integer(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "syllabus_weight",
            sa.Float(),
            nullable=False,
            server_default="1.0",
            comment="Relative importance (0.5 = half, 1.0 = normal, 2.0 = double)",
        ),
        sa.Column(
            "recommended_minutes",
            sa.Integer(),
            nullable=False,
            comment="Suggested study time in minutes",
        ),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["curriculum_id"], ["curricula.id"]),
        sa.ForeignKeyConstraint(["parent_topic_id"], ["topics.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create topic_progress table
    op.create_table(
        "topic_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column(
            "confidence",
            sa.String(length=50),
            nullable=False,
            server_default="Not Started",
            comment="Not Started, Low, Medium, High, Mastered",
        ),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("last_reviewed", sa.DateTime(), nullable=True),
        sa.Column("revision_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create study_attempts table
    op.create_table(
        "study_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column(
            "topic_id",
            sa.Integer(),
            nullable=True,
            comment="Associated topic from curriculum, if any",
        ),
        sa.Column("study_date", sa.Date(), nullable=False),
        sa.Column(
            "duration_minutes",
            sa.Integer(),
            nullable=True,
            comment="Time spent studying (reported by student)",
        ),
        sa.Column(
            "questions_attempted",
            sa.Integer(),
            nullable=True,
            comment="Total questions/problems attempted",
        ),
        sa.Column(
            "questions_correct",
            sa.Integer(),
            nullable=True,
            comment="Number of questions answered correctly",
        ),
        sa.Column(
            "confidence_before",
            sa.String(length=50),
            nullable=True,
            comment="Confidence level before studying",
        ),
        sa.Column(
            "confidence_after",
            sa.String(length=50),
            nullable=True,
            comment="Confidence level after studying",
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
            comment="Student's reflection on the learning session",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"]),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create learning_objectives table
    op.create_table(
        "learning_objectives",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=False,
            comment="What students should be able to do (e.g., 'Solve linear equations')",
        ),
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create mistakes table
    op.create_table(
        "mistakes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("study_attempt_id", sa.Integer(), nullable=False),
        sa.Column(
            "topic_id",
            sa.Integer(),
            nullable=True,
            comment="Associated topic for analysis",
        ),
        sa.Column(
            "mistake_type",
            sa.String(length=100),
            nullable=True,
            comment="Category: Calculation, Concept, Misconception, Careless, etc.",
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
            comment="What the student did wrong",
        ),
        sa.Column(
            "correct_solution",
            sa.Text(),
            nullable=True,
            comment="The correct approach or answer",
        ),
        sa.Column(
            "resolved",
            sa.Boolean(),
            nullable=False,
            server_default="0",
            comment="Whether student understands the correct solution",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["study_attempt_id"], ["study_attempts.id"]),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("mistakes")
    op.drop_table("learning_objectives")
    op.drop_table("study_attempts")
    op.drop_table("topic_progress")
    op.drop_table("topics")
    with op.batch_alter_table("study_plans") as batch_op:
        batch_op.drop_constraint("fk_study_plans_curriculum_id", type_="foreignkey")
        batch_op.drop_column("curriculum_id")
    op.drop_table("curricula")

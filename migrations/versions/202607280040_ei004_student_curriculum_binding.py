"""EI-004 Student Curriculum Binding — instance + node state tables.

Revision ID: 202607280040
Revises: 202607280030
Create Date: 2026-07-28 23:00:00.000000

Additive: sci_student_curriculum_instances, sci_curriculum_node_states.

Does not alter CKG node tables, V1/V2 curriculum engine, Twin, missions,
or recommendation schema.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607280040"
down_revision: str | tuple[str, ...] | None = "202607280030"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sci_student_curriculum_instances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instance_id", sa.String(length=64), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=32), nullable=False),
        sa.Column("edition_id", sa.String(length=64), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["edition_id"],
            ["ckg_graph_editions.edition_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("instance_id", name="uq_sci_instances_instance_id"),
    )
    op.create_index(
        "ix_sci_student_curriculum_instances_instance_id",
        "sci_student_curriculum_instances",
        ["instance_id"],
        unique=True,
    )
    op.create_index(
        "ix_sci_student_curriculum_instances_student_id",
        "sci_student_curriculum_instances",
        ["student_id"],
    )
    op.create_index(
        "ix_sci_student_curriculum_instances_subject_code",
        "sci_student_curriculum_instances",
        ["subject_code"],
    )
    op.create_index(
        "ix_sci_student_curriculum_instances_edition_id",
        "sci_student_curriculum_instances",
        ["edition_id"],
    )
    op.create_index(
        "ix_sci_student_curriculum_instances_is_active",
        "sci_student_curriculum_instances",
        ["is_active"],
    )
    op.create_index(
        "ix_sci_instances_student_subject_active",
        "sci_student_curriculum_instances",
        ["student_id", "subject_code", "is_active"],
    )
    op.create_index(
        "ix_sci_instances_edition",
        "sci_student_curriculum_instances",
        ["edition_id"],
    )

    op.create_table(
        "sci_curriculum_node_states",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instance_id", sa.String(length=64), nullable=False),
        sa.Column("node_stable_id", sa.String(length=256), nullable=False),
        sa.Column("node_kind", sa.String(length=64), nullable=False),
        sa.Column("mastery", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("revision_status", sa.String(length=32), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("total_study_time_minutes", sa.Integer(), nullable=False),
        sa.Column("last_interaction_at", sa.DateTime(), nullable=True),
        sa.Column("completion_status", sa.String(length=32), nullable=False),
        sa.Column("evidence_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["instance_id"],
            ["sci_student_curriculum_instances.instance_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "instance_id",
            "node_stable_id",
            name="uq_sci_node_states_instance_stable",
        ),
    )
    op.create_index(
        "ix_sci_curriculum_node_states_instance_id",
        "sci_curriculum_node_states",
        ["instance_id"],
    )
    op.create_index(
        "ix_sci_curriculum_node_states_node_stable_id",
        "sci_curriculum_node_states",
        ["node_stable_id"],
    )
    op.create_index(
        "ix_sci_curriculum_node_states_completion_status",
        "sci_curriculum_node_states",
        ["completion_status"],
    )
    op.create_index(
        "ix_sci_node_states_completion",
        "sci_curriculum_node_states",
        ["instance_id", "completion_status"],
    )
    op.create_index(
        "ix_sci_node_states_kind",
        "sci_curriculum_node_states",
        ["instance_id", "node_kind"],
    )


def downgrade() -> None:
    op.drop_index("ix_sci_node_states_kind", table_name="sci_curriculum_node_states")
    op.drop_index(
        "ix_sci_node_states_completion", table_name="sci_curriculum_node_states"
    )
    op.drop_index(
        "ix_sci_curriculum_node_states_completion_status",
        table_name="sci_curriculum_node_states",
    )
    op.drop_index(
        "ix_sci_curriculum_node_states_node_stable_id",
        table_name="sci_curriculum_node_states",
    )
    op.drop_index(
        "ix_sci_curriculum_node_states_instance_id",
        table_name="sci_curriculum_node_states",
    )
    op.drop_table("sci_curriculum_node_states")

    op.drop_index(
        "ix_sci_instances_edition",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_index(
        "ix_sci_instances_student_subject_active",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_index(
        "ix_sci_student_curriculum_instances_is_active",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_index(
        "ix_sci_student_curriculum_instances_edition_id",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_index(
        "ix_sci_student_curriculum_instances_subject_code",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_index(
        "ix_sci_student_curriculum_instances_student_id",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_index(
        "ix_sci_student_curriculum_instances_instance_id",
        table_name="sci_student_curriculum_instances",
    )
    op.drop_table("sci_student_curriculum_instances")

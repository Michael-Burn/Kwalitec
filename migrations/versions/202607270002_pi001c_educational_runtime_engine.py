"""Create Educational Runtime Engine tables (PI-001C).

Revision ID: 202607270002
Revises: 202607270001
Create Date: 2026-07-27 09:00:00.000000

Additive student-runtime tables for curriculum-driven enrolment, study-plan
instances, mission instances, and immutable educational events. Does not alter
JSON Runtime A (StudyPlan / Mission / TopicProgress) schema.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270002"
down_revision: Union[str, None] = "202607270001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "runtime_enrolments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enrolment_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("curriculum_identity", sa.String(length=128), nullable=False),
        sa.Column("published_package_id", sa.Integer(), nullable=False),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("exam_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["published_package_id"], ["published_curriculum_packages.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "curriculum_identity",
            name="uq_runtime_enrolments_user_curriculum",
        ),
        sa.UniqueConstraint("enrolment_id"),
    )
    with op.batch_alter_table("runtime_enrolments", schema=None) as batch_op:
        batch_op.create_index(
            "ix_runtime_enrolments_enrolment_id", ["enrolment_id"], unique=True
        )
        batch_op.create_index(
            "ix_runtime_enrolments_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_runtime_enrolments_subject_code", ["subject_code"], unique=False
        )
        batch_op.create_index(
            "ix_runtime_enrolments_curriculum_identity",
            ["curriculum_identity"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolments_published_package_id",
            ["published_package_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolments_user_subject",
            ["user_id", "subject_code"],
            unique=False,
        )

    op.create_table(
        "runtime_study_plan_instances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("plan_instance_id", sa.String(length=64), nullable=False),
        sa.Column("enrolment_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("curriculum_identity", sa.String(length=128), nullable=False),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("current_topic_id", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["enrolment_id"], ["runtime_enrolments.enrolment_id"]
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plan_instance_id"),
    )
    with op.batch_alter_table(
        "runtime_study_plan_instances", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_runtime_study_plan_instances_plan_instance_id",
            ["plan_instance_id"],
            unique=True,
        )
        batch_op.create_index(
            "ix_runtime_study_plan_instances_enrolment_id",
            ["enrolment_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_study_plan_instances_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_runtime_study_plan_instances_curriculum_identity",
            ["curriculum_identity"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_study_plan_user_status",
            ["user_id", "status"],
            unique=False,
        )

    op.create_table(
        "runtime_mission_instances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mission_instance_id", sa.String(length=64), nullable=False),
        sa.Column("plan_instance_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("curriculum_identity", sa.String(length=128), nullable=False),
        sa.Column("template_id", sa.String(length=128), nullable=False),
        sa.Column("topic_id", sa.String(length=128), nullable=False),
        sa.Column("topic_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("task_descriptions_json", sa.Text(), nullable=False),
        sa.Column("mission_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["plan_instance_id"],
            ["runtime_study_plan_instances.plan_instance_id"],
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "plan_instance_id",
            "mission_date",
            name="uq_runtime_mission_plan_date",
        ),
        sa.UniqueConstraint("mission_instance_id"),
    )
    with op.batch_alter_table("runtime_mission_instances", schema=None) as batch_op:
        batch_op.create_index(
            "ix_runtime_mission_instances_mission_instance_id",
            ["mission_instance_id"],
            unique=True,
        )
        batch_op.create_index(
            "ix_runtime_mission_instances_plan_instance_id",
            ["plan_instance_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_mission_instances_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_runtime_mission_instances_topic_id", ["topic_id"], unique=False
        )
        batch_op.create_index(
            "ix_runtime_mission_user_date",
            ["user_id", "mission_date"],
            unique=False,
        )

    op.create_table(
        "runtime_educational_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("enrolment_id", sa.String(length=64), nullable=True),
        sa.Column("plan_instance_id", sa.String(length=64), nullable=True),
        sa.Column("curriculum_identity", sa.String(length=128), nullable=False),
        sa.Column("topic_id", sa.String(length=128), nullable=True),
        sa.Column("mission_instance_id", sa.String(length=64), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    with op.batch_alter_table("runtime_educational_events", schema=None) as batch_op:
        batch_op.create_index(
            "ix_runtime_educational_events_event_id", ["event_id"], unique=True
        )
        batch_op.create_index(
            "ix_runtime_educational_events_event_type",
            ["event_type"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_educational_events_user_id", ["user_id"], unique=False
        )
        batch_op.create_index(
            "ix_runtime_educational_events_enrolment_id",
            ["enrolment_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_educational_events_plan_instance_id",
            ["plan_instance_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_educational_events_occurred_at",
            ["occurred_at"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_events_user_curriculum",
            ["user_id", "curriculum_identity"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_events_plan_type",
            ["plan_instance_id", "event_type"],
            unique=False,
        )


def downgrade() -> None:
    op.drop_table("runtime_educational_events")
    op.drop_table("runtime_mission_instances")
    op.drop_table("runtime_study_plan_instances")
    op.drop_table("runtime_enrolments")

"""Create runtime enrolment routing audit table (PI-002A).

Revision ID: 202607270003
Revises: 202607270002
Create Date: 2026-07-27 10:00:00.000000

Additive audit table for Founder → Student runtime selection. Does not
alter Runtime A StudyPlan schema or Runtime C enrolment tables.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270003"
down_revision: Union[str, None] = "202607270002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "runtime_enrolment_routing_audits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("audit_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("category_code", sa.String(length=64), nullable=False),
        sa.Column("runtime_authority", sa.String(length=64), nullable=False),
        sa.Column("decision_reason", sa.String(length=128), nullable=False),
        sa.Column("published_package_id", sa.Integer(), nullable=True),
        sa.Column("curriculum_identity", sa.String(length=128), nullable=True),
        sa.Column("enrolment_id", sa.String(length=64), nullable=True),
        sa.Column("study_plan_id", sa.Integer(), nullable=True),
        sa.Column("flags_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("audit_id"),
    )
    with op.batch_alter_table(
        "runtime_enrolment_routing_audits", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_audit_id",
            ["audit_id"],
            unique=True,
        )
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_user_id",
            ["user_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_subject_code",
            ["subject_code"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_runtime_authority",
            ["runtime_authority"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_enrolment_id",
            ["enrolment_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_study_plan_id",
            ["study_plan_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_enrolment_routing_audits_created_at",
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_routing_audit_user",
            ["user_id", "created_at"],
            unique=False,
        )
        batch_op.create_index(
            "ix_runtime_routing_audit_subject",
            ["subject_code", "runtime_authority"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "runtime_enrolment_routing_audits", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_runtime_routing_audit_subject")
        batch_op.drop_index("ix_runtime_routing_audit_user")
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_created_at"
        )
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_study_plan_id"
        )
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_enrolment_id"
        )
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_runtime_authority"
        )
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_subject_code"
        )
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_user_id"
        )
        batch_op.drop_index(
            "ix_runtime_enrolment_routing_audits_audit_id"
        )
    op.drop_table("runtime_enrolment_routing_audits")

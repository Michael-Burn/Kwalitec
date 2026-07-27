"""Create Founder Curriculum Studio foundation tables (PI-001A).

Revision ID: 202607270001
Revises: 202607260001
Create Date: 2026-07-27 08:30:00.000000

Durable subject / version / document / audit / published-package tables
for founder-operated curriculum onboarding. Does not alter student
Curriculum / Topic / Section educational schema.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "202607270001"
down_revision: Union[str, None] = "202607260001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "studio_foundation_subjects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subject_code"),
    )
    with op.batch_alter_table("studio_foundation_subjects", schema=None) as batch_op:
        batch_op.create_index(
            "ix_studio_foundation_subjects_subject_code",
            ["subject_code"],
            unique=True,
        )

    op.create_table(
        "studio_foundation_versions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("stage", sa.String(length=64), nullable=False),
        sa.Column("publication_state", sa.String(length=64), nullable=False),
        sa.Column("processing_state", sa.String(length=64), nullable=True),
        sa.Column("ingestion_job_id", sa.String(length=128), nullable=True),
        sa.Column("parsed_structure_json", sa.Text(), nullable=True),
        sa.Column("validation_report_json", sa.Text(), nullable=True),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.String(length=128), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["studio_foundation_subjects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "subject_id",
            "version_label",
            name="uq_studio_foundation_versions_subject_label",
        ),
    )
    with op.batch_alter_table("studio_foundation_versions", schema=None) as batch_op:
        batch_op.create_index(
            "ix_studio_foundation_versions_subject_id",
            ["subject_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_versions_publication_state",
            ["publication_state"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_versions_ingestion_job_id",
            ["ingestion_job_id"],
            unique=False,
        )

    op.create_table(
        "studio_foundation_documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("reference", sa.String(length=1024), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("structure_json", sa.Text(), nullable=True),
        sa.Column("uploaded_by", sa.String(length=128), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["version_id"],
            ["studio_foundation_versions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("studio_foundation_documents", schema=None) as batch_op:
        batch_op.create_index(
            "ix_studio_foundation_documents_version_id",
            ["version_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_documents_version_kind",
            ["version_id", "kind"],
            unique=False,
        )

    op.create_table(
        "studio_foundation_audit_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("version_id", sa.Integer(), nullable=True),
        sa.Column("stage", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("message", sa.String(length=512), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    with op.batch_alter_table(
        "studio_foundation_audit_events", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_studio_foundation_audit_events_event_id",
            ["event_id"],
            unique=True,
        )
        batch_op.create_index(
            "ix_studio_foundation_audit_events_subject_code",
            ["subject_code"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_audit_events_version_id",
            ["version_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_audit_events_stage",
            ["stage"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_audit_events_created_at",
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            "ix_studio_foundation_audit_subject_version",
            ["subject_code", "version_id"],
            unique=False,
        )

    op.create_table(
        "published_curriculum_packages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=64), nullable=False),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("package_json", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("published_by", sa.String(length=128), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=False),
        sa.Column("source_ingestion_job_id", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("version_id"),
        sa.UniqueConstraint(
            "subject_code",
            "version_label",
            name="uq_published_curriculum_packages_code_label",
        ),
    )
    with op.batch_alter_table(
        "published_curriculum_packages", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_published_curriculum_packages_subject_code",
            ["subject_code"],
            unique=False,
        )
        batch_op.create_index(
            "ix_published_curriculum_packages_is_active",
            ["is_active"],
            unique=False,
        )
        batch_op.create_index(
            "ix_published_curriculum_packages_active",
            ["subject_code", "is_active"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "published_curriculum_packages", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_published_curriculum_packages_active")
        batch_op.drop_index("ix_published_curriculum_packages_is_active")
        batch_op.drop_index("ix_published_curriculum_packages_subject_code")
    op.drop_table("published_curriculum_packages")

    with op.batch_alter_table(
        "studio_foundation_audit_events", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_studio_foundation_audit_subject_version")
        batch_op.drop_index("ix_studio_foundation_audit_events_created_at")
        batch_op.drop_index("ix_studio_foundation_audit_events_stage")
        batch_op.drop_index("ix_studio_foundation_audit_events_version_id")
        batch_op.drop_index("ix_studio_foundation_audit_events_subject_code")
        batch_op.drop_index("ix_studio_foundation_audit_events_event_id")
    op.drop_table("studio_foundation_audit_events")

    with op.batch_alter_table("studio_foundation_documents", schema=None) as batch_op:
        batch_op.drop_index("ix_studio_foundation_documents_version_kind")
        batch_op.drop_index("ix_studio_foundation_documents_version_id")
    op.drop_table("studio_foundation_documents")

    with op.batch_alter_table("studio_foundation_versions", schema=None) as batch_op:
        batch_op.drop_index("ix_studio_foundation_versions_ingestion_job_id")
        batch_op.drop_index("ix_studio_foundation_versions_publication_state")
        batch_op.drop_index("ix_studio_foundation_versions_subject_id")
    op.drop_table("studio_foundation_versions")

    with op.batch_alter_table("studio_foundation_subjects", schema=None) as batch_op:
        batch_op.drop_index("ix_studio_foundation_subjects_subject_code")
    op.drop_table("studio_foundation_subjects")

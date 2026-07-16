"""Create Founder Research Command Centre tables for RIP-003.

Revision ID: 202607160003
Revises: 202607160002
Create Date: 2026-07-16 08:00:00.000000

RIP-003 — Founder Research Command Centre.

Adds workflow status, transition history, founder notes, and product
findings. Does not modify educational tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607160003"
down_revision: str | None = "202607160002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("research_feedback_submissions", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "workflow_status",
                sa.String(length=32),
                nullable=False,
                server_default="new",
            )
        )
        batch_op.create_index(
            "ix_research_feedback_submissions_workflow_status",
            ["workflow_status"],
            unique=False,
        )

    op.create_table(
        "research_feedback_status_transitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("from_status", sa.String(length=32), nullable=True),
        sa.Column("to_status", sa.String(length=32), nullable=False),
        sa.Column("reviewer_user_id", sa.Integer(), nullable=False),
        sa.Column("rationale", sa.String(length=500), nullable=True),
        sa.Column("transitioned_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["reviewer_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["research_feedback_submissions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table(
        "research_feedback_status_transitions", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_research_feedback_status_transitions_submission_id",
            ["submission_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_feedback_status_transitions_transitioned_at",
            ["transitioned_at"],
            unique=False,
        )

    op.create_table(
        "research_founder_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.Column("founder_user_id", sa.Integer(), nullable=False),
        sa.Column("note_text", sa.String(length=1000), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["founder_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["research_feedback_submissions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("research_founder_notes", schema=None) as batch_op:
        batch_op.create_index(
            "ix_research_founder_notes_submission_id",
            ["submission_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_founder_notes_created_at",
            ["created_at"],
            unique=False,
        )

    op.create_table(
        "research_product_findings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=1000), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("feature_area", sa.String(length=64), nullable=False),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
            server_default="new",
        ),
        sa.Column("target_release", sa.String(length=32), nullable=True),
        sa.Column("notes", sa.String(length=2000), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("research_product_findings", schema=None) as batch_op:
        batch_op.create_index(
            "ix_research_product_findings_severity",
            ["severity"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_product_findings_feature_area",
            ["feature_area"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_product_findings_status",
            ["status"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_product_findings_created_at",
            ["created_at"],
            unique=False,
        )

    op.create_table(
        "research_product_finding_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("finding_id", sa.Integer(), nullable=False),
        sa.Column("submission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["finding_id"], ["research_product_findings.id"]),
        sa.ForeignKeyConstraint(
            ["submission_id"], ["research_feedback_submissions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "finding_id", "submission_id", name="uq_finding_submission"
        ),
    )
    with op.batch_alter_table(
        "research_product_finding_links", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_research_product_finding_links_finding_id",
            ["finding_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_product_finding_links_submission_id",
            ["submission_id"],
            unique=False,
        )

    op.create_table(
        "research_product_finding_status_transitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("finding_id", sa.Integer(), nullable=False),
        sa.Column("from_status", sa.String(length=32), nullable=True),
        sa.Column("to_status", sa.String(length=32), nullable=False),
        sa.Column("reviewer_user_id", sa.Integer(), nullable=False),
        sa.Column("rationale", sa.String(length=500), nullable=True),
        sa.Column("transitioned_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["finding_id"], ["research_product_findings.id"]),
        sa.ForeignKeyConstraint(["reviewer_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table(
        "research_product_finding_status_transitions", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_research_product_finding_status_transitions_finding_id",
            ["finding_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_research_product_finding_status_transitions_transitioned_at",
            ["transitioned_at"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "research_product_finding_status_transitions", schema=None
    ) as batch_op:
        batch_op.drop_index(
            "ix_research_product_finding_status_transitions_transitioned_at"
        )
        batch_op.drop_index(
            "ix_research_product_finding_status_transitions_finding_id"
        )
    op.drop_table("research_product_finding_status_transitions")

    with op.batch_alter_table(
        "research_product_finding_links", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_research_product_finding_links_submission_id")
        batch_op.drop_index("ix_research_product_finding_links_finding_id")
    op.drop_table("research_product_finding_links")

    with op.batch_alter_table("research_product_findings", schema=None) as batch_op:
        batch_op.drop_index("ix_research_product_findings_created_at")
        batch_op.drop_index("ix_research_product_findings_status")
        batch_op.drop_index("ix_research_product_findings_feature_area")
        batch_op.drop_index("ix_research_product_findings_severity")
    op.drop_table("research_product_findings")

    with op.batch_alter_table("research_founder_notes", schema=None) as batch_op:
        batch_op.drop_index("ix_research_founder_notes_created_at")
        batch_op.drop_index("ix_research_founder_notes_submission_id")
    op.drop_table("research_founder_notes")

    with op.batch_alter_table(
        "research_feedback_status_transitions", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_research_feedback_status_transitions_transitioned_at")
        batch_op.drop_index("ix_research_feedback_status_transitions_submission_id")
    op.drop_table("research_feedback_status_transitions")

    with op.batch_alter_table("research_feedback_submissions", schema=None) as batch_op:
        batch_op.drop_index("ix_research_feedback_submissions_workflow_status")
        batch_op.drop_column("workflow_status")

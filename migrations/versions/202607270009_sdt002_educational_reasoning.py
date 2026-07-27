"""SDT-002 Educational Reasoning Engine metadata tables.

Revision ID: 202607270009
Revises: 202607270008
Create Date: 2026-07-27 22:00:00.000000

Additive reasoning-history schema. Does not alter SDT-001 Twin inference tables.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "202607270009"
down_revision: str | None = "202607270008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "educational_reasoning_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("triggered_by", sa.String(length=128), nullable=False),
        sa.Column("observation_ids_json", sa.Text(), nullable=False),
        sa.Column("curriculum_evidence_ids_json", sa.Text(), nullable=False),
        sa.Column("retrieval_log_ids_json", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("engine_version", sa.String(length=64), nullable=False),
        sa.Column("rule_count", sa.Integer(), nullable=False),
        sa.Column("decision_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_educational_reasoning_runs_run_id",
        "educational_reasoning_runs",
        ["run_id"],
        unique=True,
    )
    op.create_index(
        "ix_educational_reasoning_runs_twin_id",
        "educational_reasoning_runs",
        ["twin_id"],
        unique=False,
    )
    op.create_index(
        "ix_err_runs_twin_created",
        "educational_reasoning_runs",
        ["twin_id", "created_at"],
        unique=False,
    )

    op.create_table(
        "educational_rule_executions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("execution_id", sa.String(length=64), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("rule_code", sa.String(length=64), nullable=False),
        sa.Column("rule_name", sa.String(length=128), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("inputs_json", sa.Text(), nullable=False),
        sa.Column("outputs_json", sa.Text(), nullable=False),
        sa.Column("explanation_summary", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["educational_reasoning_runs.run_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_educational_rule_executions_execution_id",
        "educational_rule_executions",
        ["execution_id"],
        unique=True,
    )
    op.create_index(
        "ix_err_exec_run",
        "educational_rule_executions",
        ["run_id"],
        unique=False,
    )
    op.create_index(
        "ix_err_exec_rule",
        "educational_rule_executions",
        ["rule_code"],
        unique=False,
    )
    op.create_index(
        "ix_educational_rule_executions_twin_id",
        "educational_rule_executions",
        ["twin_id"],
        unique=False,
    )

    op.create_table(
        "reasoning_explanations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("explanation_id", sa.String(length=64), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("rule_code", sa.String(length=64), nullable=False),
        sa.Column("decision_id", sa.String(length=64), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("observation_ids_json", sa.Text(), nullable=False),
        sa.Column("curriculum_evidence_ids_json", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["educational_reasoning_runs.run_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_reasoning_explanations_explanation_id",
        "reasoning_explanations",
        ["explanation_id"],
        unique=True,
    )
    op.create_index(
        "ix_err_expl_run",
        "reasoning_explanations",
        ["run_id"],
        unique=False,
    )
    op.create_index(
        "ix_err_expl_rule",
        "reasoning_explanations",
        ["rule_code"],
        unique=False,
    )
    op.create_index(
        "ix_reasoning_explanations_twin_id",
        "reasoning_explanations",
        ["twin_id"],
        unique=False,
    )
    op.create_index(
        "ix_reasoning_explanations_decision_id",
        "reasoning_explanations",
        ["decision_id"],
        unique=False,
    )

    op.create_table(
        "decision_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("decision_id", sa.String(length=64), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("twin_id", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("rule_code", sa.String(length=64), nullable=False),
        sa.Column("subject_ref", sa.String(length=128), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("explanation_summary", sa.Text(), nullable=False),
        sa.Column("observation_ids_json", sa.Text(), nullable=False),
        sa.Column("curriculum_evidence_ids_json", sa.Text(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["educational_reasoning_runs.run_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_decision_records_decision_id",
        "decision_records",
        ["decision_id"],
        unique=True,
    )
    op.create_index(
        "ix_err_dec_run",
        "decision_records",
        ["run_id"],
        unique=False,
    )
    op.create_index(
        "ix_err_dec_twin",
        "decision_records",
        ["twin_id"],
        unique=False,
    )
    op.create_index(
        "ix_err_dec_kind",
        "decision_records",
        ["kind"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("decision_records")
    op.drop_table("reasoning_explanations")
    op.drop_table("educational_rule_executions")
    op.drop_table("educational_reasoning_runs")

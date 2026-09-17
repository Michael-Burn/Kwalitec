"""Create canonical curriculum identity tables and seed active CS1 maps.

Revision ID: 202609160001
Revises: 202609150002
Create Date: 2026-09-16 18:00:00.000000

Additive identity-layer plumbing only. Does not alter coverage formulas,
published packages, or existing topic rows. Seeds opaque UUID registry and
alias maps for the active CS1 syllabus when Stage A topics are already present.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

import sqlalchemy as sa
from alembic import op

revision: str = "202609160001"
down_revision: str | None = "202609150002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SEED_PATH = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "curriculum"
    / "data"
    / "identity"
    / "cs1_2026_1_canonical_seed.json"
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def upgrade() -> None:
    op.create_table(
        "canonical_curriculum_topic",
        sa.Column("canonical_id", sa.String(length=36), nullable=False),
        sa.Column("curriculum_version", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("canonical_id"),
    )
    with op.batch_alter_table("canonical_curriculum_topic", schema=None) as batch_op:
        batch_op.create_index(
            "ix_canonical_curriculum_topic_version",
            ["curriculum_version"],
            unique=False,
        )

    op.create_table(
        "curriculum_topic_identity_map",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("canonical_id", sa.String(length=36), nullable=True),
        sa.Column("source_system", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("source_version", sa.String(length=128), nullable=False),
        sa.Column("mapping_status", sa.String(length=64), nullable=False),
        sa.Column("mapping_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["canonical_id"],
            ["canonical_curriculum_topic.canonical_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "source_system",
            "source_id",
            "source_version",
            name="uq_curriculum_topic_identity_map_source",
        ),
    )
    with op.batch_alter_table(
        "curriculum_topic_identity_map", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_curriculum_topic_identity_map_canonical",
            ["canonical_id"],
            unique=False,
        )

    _seed_from_json(op.get_bind())


def _seed_from_json(connection: sa.Connection) -> None:
    """Insert registry + maps using the migration connection (no Flask app)."""
    seed = json.loads(_SEED_PATH.read_text(encoding="utf-8"))
    curriculum_version = str(seed["curriculum_version"])
    stage_a_version = str(seed.get("stage_a_source_version") or "IFoA CS1:2026")
    exam_name = str(seed.get("exam_name") or "IFoA CS1")
    stage_a_curriculum_version = str(seed.get("stage_a_version") or "2026")
    now = _utc_now()

    canon = sa.table(
        "canonical_curriculum_topic",
        sa.column("canonical_id", sa.String),
        sa.column("curriculum_version", sa.String),
        sa.column("title", sa.String),
        sa.column("status", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )
    imap = sa.table(
        "curriculum_topic_identity_map",
        sa.column("canonical_id", sa.String),
        sa.column("source_system", sa.String),
        sa.column("source_id", sa.String),
        sa.column("source_version", sa.String),
        sa.column("mapping_status", sa.String),
        sa.column("mapping_notes", sa.Text),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )

    for entry in seed["topics"]:
        canonical_id = str(entry["canonical_id"])
        title = str(entry["title"])
        published_id = str(entry["published_source_id"])
        syllabus_code = str(entry["syllabus_code"])

        exists = connection.execute(
            sa.select(canon.c.canonical_id).where(
                canon.c.canonical_id == canonical_id
            )
        ).first()
        if exists is None:
            connection.execute(
                sa.insert(canon).values(
                    canonical_id=canonical_id,
                    curriculum_version=curriculum_version,
                    title=title,
                    status="active",
                    created_at=now,
                    updated_at=now,
                )
            )

        for source_system in ("published_content", "study_event"):
            _insert_map_if_absent(
                connection,
                imap,
                canonical_id=canonical_id,
                source_system=source_system,
                source_id=published_id,
                source_version=curriculum_version,
                mapping_status="exact",
                mapping_notes=(
                    f"Explicit CS1 {syllabus_code} map to active published "
                    f"topic_id {published_id}."
                ),
                now=now,
            )

    # Stage A exact maps by title when the curriculum already exists.
    curr = connection.execute(
        sa.text(
            "SELECT id FROM curricula WHERE exam_name = :exam "
            "AND version = :ver AND active = 1 LIMIT 1"
        ),
        {"exam": exam_name, "ver": stage_a_curriculum_version},
    ).first()
    if curr is not None:
        curriculum_id = curr[0]
        for entry in seed["topics"]:
            title = str(entry["title"])
            canonical_id = str(entry["canonical_id"])
            syllabus_code = str(entry["syllabus_code"])
            matches = connection.execute(
                sa.text(
                    "SELECT id FROM topics WHERE curriculum_id = :cid "
                    "AND name = :name AND active = 1 "
                    "AND section_id IS NOT NULL"
                ),
                {"cid": curriculum_id, "name": title},
            ).fetchall()
            if len(matches) != 1:
                continue
            topic_id = matches[0][0]
            _insert_map_if_absent(
                connection,
                imap,
                canonical_id=canonical_id,
                source_system="stage_a_database",
                source_id=str(topic_id),
                source_version=stage_a_version,
                mapping_status="exact",
                mapping_notes=(
                    f"Explicit title match for CS1 {syllabus_code} to ORM "
                    f"topic id={topic_id}."
                ),
                now=now,
            )

        for name in list(seed.get("orphan_topic_names") or []):
            matches = connection.execute(
                sa.text(
                    "SELECT id FROM topics WHERE curriculum_id = :cid "
                    "AND name = :name AND active = 1 "
                    "AND section_id IS NULL"
                ),
                {"cid": curriculum_id, "name": name},
            ).fetchall()
            if len(matches) != 1:
                continue
            topic_id = matches[0][0]
            _insert_map_if_absent(
                connection,
                imap,
                canonical_id=None,
                source_system="stage_a_database",
                source_id=str(topic_id),
                source_version=stage_a_version,
                mapping_status="obsolete_no_equivalent",
                mapping_notes=(
                    f"Orphan historical topic {name!r} (ORM id={topic_id}) "
                    "has no equivalent on the active CS1:2026.1 syllabus. "
                    "Left unmapped to current coverage pending separate "
                    "deliberate review."
                ),
                now=now,
            )


def _insert_map_if_absent(
    connection: sa.Connection,
    imap: sa.Table,
    *,
    canonical_id: str | None,
    source_system: str,
    source_id: str,
    source_version: str,
    mapping_status: str,
    mapping_notes: str,
    now: datetime,
) -> None:
    exists = connection.execute(
        sa.select(imap.c.source_id).where(
            imap.c.source_system == source_system,
            imap.c.source_id == source_id,
            imap.c.source_version == source_version,
        )
    ).first()
    if exists is not None:
        return
    connection.execute(
        sa.insert(imap).values(
            canonical_id=canonical_id,
            source_system=source_system,
            source_id=source_id,
            source_version=source_version,
            mapping_status=mapping_status,
            mapping_notes=mapping_notes,
            created_at=now,
            updated_at=now,
        )
    )


def downgrade() -> None:
    op.drop_table("curriculum_topic_identity_map")
    op.drop_table("canonical_curriculum_topic")

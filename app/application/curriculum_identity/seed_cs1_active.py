"""Load and apply the fixed CS1 active-syllabus identity seed."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
    ACTIVE_CS1_STAGE_A_SOURCE_VERSION,
    MAPPING_EXACT,
    MAPPING_OBSOLETE_NO_EQUIVALENT,
    SOURCE_PUBLISHED_CONTENT,
    SOURCE_STAGE_A_DATABASE,
    SOURCE_STUDY_EVENT,
    STATUS_ACTIVE,
)
from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.curriculum_identity import (
    CanonicalCurriculumTopic,
    CurriculumTopicIdentityMap,
)

logger = logging.getLogger(__name__)

_SEED_PATH = (
    Path(__file__).resolve().parents[2]
    / "curriculum"
    / "data"
    / "identity"
    / "cs1_2026_1_canonical_seed.json"
)


def load_cs1_active_seed() -> dict[str, Any]:
    """Return the committed CS1:2026.1 canonical identity seed document."""
    return json.loads(_SEED_PATH.read_text(encoding="utf-8"))


def seed_cs1_active_identity_layer(*, require_stage_a: bool = False) -> dict[str, int]:
    """Idempotently populate registry + maps for the active CS1 syllabus.

    Always writes the 14 canonical rows and published-content / study-event
    exact maps from the fixed seed file. Stage A maps are written by exact
    title lookup on the active ``IFoA CS1`` / ``2026`` curriculum (sectioned
    topics only). Orphan ``T0``/``T1``/``T2`` rows are mapped as
    ``obsolete_no_equivalent`` when present.

    Args:
        require_stage_a: When True, raise if any of the 14 Stage A exact maps
            cannot be resolved uniquely by title.

    Returns:
        Counts of rows inserted this call (canonical, maps, orphans).
    """
    seed = load_cs1_active_seed()
    curriculum_version = str(seed["curriculum_version"])
    stage_a_version = str(
        seed.get("stage_a_source_version") or ACTIVE_CS1_STAGE_A_SOURCE_VERSION
    )
    topics = list(seed["topics"])
    if curriculum_version != ACTIVE_CS1_CURRICULUM_VERSION:
        raise ValueError(
            f"Unexpected seed curriculum_version {curriculum_version!r}; "
            f"expected {ACTIVE_CS1_CURRICULUM_VERSION!r}"
        )
    if len(topics) != 14:
        raise ValueError(f"CS1 active seed must list 14 topics; got {len(topics)}")

    inserted_canonical = 0
    inserted_maps = 0
    for entry in topics:
        canonical_id = str(entry["canonical_id"])
        title = str(entry["title"])
        published_id = str(entry["published_source_id"])
        syllabus_code = str(entry["syllabus_code"])

        if db.session.get(CanonicalCurriculumTopic, canonical_id) is None:
            db.session.add(
                CanonicalCurriculumTopic(
                    canonical_id=canonical_id,
                    curriculum_version=curriculum_version,
                    title=title,
                    status=STATUS_ACTIVE,
                )
            )
            inserted_canonical += 1

        for source_system in (SOURCE_PUBLISHED_CONTENT, SOURCE_STUDY_EVENT):
            inserted_maps += _upsert_map(
                canonical_id=canonical_id,
                source_system=source_system,
                source_id=published_id,
                source_version=curriculum_version,
                mapping_status=MAPPING_EXACT,
                mapping_notes=(
                    f"Explicit CS1 {syllabus_code} map to active published "
                    f"topic_id {published_id}."
                ),
            )

    stage_a_mapped = _seed_stage_a_exact_maps(
        topics=topics,
        stage_a_version=stage_a_version,
        exam_name=str(seed.get("exam_name") or "IFoA CS1"),
        stage_a_curriculum_version=str(seed.get("stage_a_version") or "2026"),
        require_stage_a=require_stage_a,
    )
    inserted_maps += stage_a_mapped

    orphan_inserted = _seed_orphan_maps(
        orphan_names=list(seed.get("orphan_topic_names") or []),
        stage_a_version=stage_a_version,
        exam_name=str(seed.get("exam_name") or "IFoA CS1"),
        stage_a_curriculum_version=str(seed.get("stage_a_version") or "2026"),
    )
    inserted_maps += orphan_inserted

    db.session.commit()
    return {
        "canonical_inserted": inserted_canonical,
        "maps_inserted": inserted_maps,
        "stage_a_exact_inserted": stage_a_mapped,
        "orphan_inserted": orphan_inserted,
    }


def _upsert_map(
    *,
    canonical_id: str | None,
    source_system: str,
    source_id: str,
    source_version: str,
    mapping_status: str,
    mapping_notes: str,
) -> int:
    existing = CurriculumTopicIdentityMap.query.filter_by(
        source_system=source_system,
        source_id=source_id,
        source_version=source_version,
    ).first()
    if existing is not None:
        return 0
    db.session.add(
        CurriculumTopicIdentityMap(
            canonical_id=canonical_id,
            source_system=source_system,
            source_id=source_id,
            source_version=source_version,
            mapping_status=mapping_status,
            mapping_notes=mapping_notes,
        )
    )
    return 1


def _seed_stage_a_exact_maps(
    *,
    topics: list[dict[str, Any]],
    stage_a_version: str,
    exam_name: str,
    stage_a_curriculum_version: str,
    require_stage_a: bool,
) -> int:
    curriculum = (
        Curriculum.query.filter_by(
            exam_name=exam_name,
            version=stage_a_curriculum_version,
            active=True,
        ).first()
    )
    if curriculum is None:
        message = (
            f"No active Stage A curriculum {exam_name!r} "
            f"version={stage_a_curriculum_version!r} for identity seed."
        )
        if require_stage_a:
            raise RuntimeError(message)
        logger.warning(message)
        return 0

    inserted = 0
    missing: list[str] = []
    for entry in topics:
        title = str(entry["title"])
        canonical_id = str(entry["canonical_id"])
        syllabus_code = str(entry["syllabus_code"])
        matches = (
            Topic.query.filter_by(curriculum_id=curriculum.id, name=title, active=True)
            .filter(Topic.section_id.isnot(None))
            .all()
        )
        if len(matches) != 1:
            missing.append(
                f"{syllabus_code} title={title!r} matches={len(matches)}"
            )
            continue
        topic = matches[0]
        inserted += _upsert_map(
            canonical_id=canonical_id,
            source_system=SOURCE_STAGE_A_DATABASE,
            source_id=str(topic.id),
            source_version=stage_a_version,
            mapping_status=MAPPING_EXACT,
            mapping_notes=(
                f"Explicit title match for CS1 {syllabus_code} to ORM topic "
                f"id={topic.id}."
            ),
        )

    if missing:
        message = (
            "Stage A identity seed incomplete; unresolved topics: "
            + "; ".join(missing)
        )
        if require_stage_a:
            raise RuntimeError(message)
        logger.warning(message)
    return inserted


def _seed_orphan_maps(
    *,
    orphan_names: list[str],
    stage_a_version: str,
    exam_name: str,
    stage_a_curriculum_version: str,
) -> int:
    curriculum = (
        Curriculum.query.filter_by(
            exam_name=exam_name,
            version=stage_a_curriculum_version,
            active=True,
        ).first()
    )
    if curriculum is None:
        return 0

    inserted = 0
    for name in orphan_names:
        matches = (
            Topic.query.filter_by(curriculum_id=curriculum.id, name=name, active=True)
            .filter(Topic.section_id.is_(None))
            .all()
        )
        if len(matches) != 1:
            continue
        topic = matches[0]
        inserted += _upsert_map(
            canonical_id=None,
            source_system=SOURCE_STAGE_A_DATABASE,
            source_id=str(topic.id),
            source_version=stage_a_version,
            mapping_status=MAPPING_OBSOLETE_NO_EQUIVALENT,
            mapping_notes=(
                f"Orphan historical topic {name!r} (ORM id={topic.id}) has no "
                "equivalent on the active CS1:2026.1 syllabus. Left unmapped "
                "to current coverage pending separate deliberate review."
            ),
        )
    return inserted

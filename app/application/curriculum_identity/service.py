"""Canonical curriculum identity resolution and new-evidence firewall."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
    MAPPING_EXACT,
    MAPPING_OBSOLETE_NO_EQUIVALENT,
    SOURCE_PUBLISHED_CONTENT,
    SOURCE_STAGE_A_DATABASE,
    SOURCE_STUDY_EVENT,
    STATUS_ACTIVE,
    UNKNOWN_CURRICULUM_IDENTITY,
)
from app.application.curriculum_identity.seed_cs1_active import (
    seed_cs1_active_identity_layer,
)
from app.models.curriculum_identity import (
    CanonicalCurriculumTopic,
    CurriculumTopicIdentityMap,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResolvedCurriculumIdentity:
    """Result of resolving a source alias to a canonical curriculum topic."""

    canonical_id: str
    curriculum_version: str
    title: str
    mapping_status: str
    source_system: str
    source_id: str
    source_version: str


class CurriculumIdentityService:
    """Resolve source aliases and firewall new educational event topic ids.

    Does not compute mastery, readiness, coverage, or scheduling.
    """

    @staticmethod
    def ensure_active_cs1_populated(*, require_stage_a: bool = True) -> dict[str, int]:
        """Idempotently seed the active CS1 identity layer."""
        return seed_cs1_active_identity_layer(require_stage_a=require_stage_a)

    @staticmethod
    def resolve(
        *,
        source_system: str,
        source_id: str,
        source_version: str,
    ) -> ResolvedCurriculumIdentity | None:
        """Resolve one source alias to a canonical topic, if mapped and active."""
        token = (source_id or "").strip()
        if not token or token == UNKNOWN_CURRICULUM_IDENTITY:
            return None

        row = CurriculumTopicIdentityMap.query.filter_by(
            source_system=source_system,
            source_id=token,
            source_version=source_version,
        ).first()
        if row is None or row.canonical_id is None:
            return None
        if row.mapping_status == MAPPING_OBSOLETE_NO_EQUIVALENT:
            return None

        canonical = CanonicalCurriculumTopic.query.filter_by(
            canonical_id=row.canonical_id
        ).first()
        if canonical is None or canonical.status != STATUS_ACTIVE:
            return None

        return ResolvedCurriculumIdentity(
            canonical_id=canonical.canonical_id,
            curriculum_version=canonical.curriculum_version,
            title=canonical.title,
            mapping_status=row.mapping_status,
            source_system=row.source_system,
            source_id=row.source_id,
            source_version=row.source_version,
        )

    @staticmethod
    def apply_event_topic_firewall(
        topic_id: str | None,
        curriculum_identity: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> tuple[str | None, dict[str, Any]]:
        """Firewall a new educational event's topic_id.

        Events with no topic_id pass through unchanged. When the identity map
        has no rows for this curriculum_identity, topic_ids also pass through
        unchanged (unmapped versions are out of scope for this first step).
        Resolvable published or study-event aliases are kept. Unresolvable
        non-empty topic_ids become UNKNOWN_CURRICULUM_IDENTITY; the original
        value is preserved under payload['unresolved_topic_id'].

        Returns:
            (possibly rewritten topic_id, payload dict to persist).
        """
        out_payload: dict[str, Any] = dict(payload or {})
        if topic_id is None:
            return None, out_payload

        token = str(topic_id).strip()
        if not token:
            return None, out_payload
        if token == UNKNOWN_CURRICULUM_IDENTITY:
            return UNKNOWN_CURRICULUM_IDENTITY, out_payload

        curriculum_identity = (curriculum_identity or "").strip()
        if not curriculum_identity:
            return token, out_payload

        # Soft enable: only enforce when this curriculum version is mapped.
        mapped_version = CurriculumTopicIdentityMap.query.filter(
            CurriculumTopicIdentityMap.source_system.in_(
                (SOURCE_STUDY_EVENT, SOURCE_PUBLISHED_CONTENT)
            ),
            CurriculumTopicIdentityMap.source_version == curriculum_identity,
            CurriculumTopicIdentityMap.mapping_status == MAPPING_EXACT,
        ).first()
        if mapped_version is None:
            return token, out_payload

        for source_system in (SOURCE_STUDY_EVENT, SOURCE_PUBLISHED_CONTENT):
            resolved = CurriculumIdentityService.resolve(
                source_system=source_system,
                source_id=token,
                source_version=curriculum_identity,
            )
            if resolved is not None:
                return token, out_payload

        out_payload["unresolved_topic_id"] = token
        logger.warning(
            "curriculum_identity_firewall unknown topic_id=%s "
            "curriculum_identity=%s",
            token,
            curriculum_identity,
        )
        return UNKNOWN_CURRICULUM_IDENTITY, out_payload

    @staticmethod
    def merge_firewall_into_payload_json(
        payload_json: str | None,
        firewall_payload: dict[str, Any],
    ) -> str:
        """Merge firewall payload keys into an existing payload_json string."""
        try:
            base = json.loads(payload_json or "{}")
        except (TypeError, ValueError):
            base = {}
        if not isinstance(base, dict):
            base = {}
        base.update(firewall_payload)
        return json.dumps(base)

    @staticmethod
    def active_registry_count(
        curriculum_version: str = ACTIVE_CS1_CURRICULUM_VERSION,
    ) -> int:
        return CanonicalCurriculumTopic.query.filter_by(
            curriculum_version=curriculum_version,
            status=STATUS_ACTIVE,
        ).count()

    @staticmethod
    def exact_map_count(
        *,
        source_system: str,
        source_version: str,
    ) -> int:
        return CurriculumTopicIdentityMap.query.filter_by(
            source_system=source_system,
            source_version=source_version,
            mapping_status=MAPPING_EXACT,
        ).count()

    @staticmethod
    def chain_for_published(
        published_source_id: str,
        *,
        curriculum_version: str = ACTIVE_CS1_CURRICULUM_VERSION,
    ) -> dict[str, Any]:
        """Build a validation chain dict across the three schemes for one topic."""
        published = CurriculumIdentityService.resolve(
            source_system=SOURCE_PUBLISHED_CONTENT,
            source_id=published_source_id,
            source_version=curriculum_version,
        )
        if published is None:
            raise RuntimeError(
                f"No published_content map for {published_source_id!r} "
                f"version={curriculum_version!r}"
            )

        study = CurriculumIdentityService.resolve(
            source_system=SOURCE_STUDY_EVENT,
            source_id=published_source_id,
            source_version=curriculum_version,
        )
        if study is None:
            raise RuntimeError(
                f"No study_event map for {published_source_id!r} "
                f"version={curriculum_version!r}"
            )
        if study.canonical_id != published.canonical_id:
            raise RuntimeError(
                f"study_event/published canonical mismatch for "
                f"{published_source_id!r}: {study.canonical_id} vs "
                f"{published.canonical_id}"
            )

        stage_rows = CurriculumTopicIdentityMap.query.filter_by(
            canonical_id=published.canonical_id,
            source_system=SOURCE_STAGE_A_DATABASE,
            mapping_status=MAPPING_EXACT,
        ).all()
        if len(stage_rows) != 1:
            raise RuntimeError(
                f"Expected one Stage A exact map for canonical "
                f"{published.canonical_id}; got {len(stage_rows)}"
            )
        stage = stage_rows[0]

        return {
            "published_source_id": published_source_id,
            "study_event_source_id": published_source_id,
            "stage_a_source_id": stage.source_id,
            "stage_a_source_version": stage.source_version,
            "canonical_id": published.canonical_id,
            "curriculum_version": published.curriculum_version,
            "title": published.title,
            "mapping_status": published.mapping_status,
            "study_event_mapping_status": study.mapping_status,
            "stage_a_mapping_status": stage.mapping_status,
        }

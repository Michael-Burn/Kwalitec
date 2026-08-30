"""Canonical published topic id resolution (ADR-027 Phase 2 Stage 1).

Joins ORM topic titles to Runtime C artefact topic titles from published
curriculum package DB rows via EducationalEngineFoundationService.
Does not add topics.official_id and does not read package authoring trees.

ORM rows are duck-typed (``name`` / ``id``) so this application module stays
free of ``app.models`` imports.
"""

from __future__ import annotations

import re
from typing import Any, Protocol

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)

_NODE_PREFIX = "node-"
_PURE_INT = re.compile(r"^[0-9]+$")


class TopicNameId(Protocol):
    """Minimal ORM Topic shape for title join (no models import)."""

    name: str
    id: int


class CanonicalTopicId:
    """Resolve Twin keys to published curriculum string topic ids."""

    def __init__(
        self,
        *,
        foundation: EducationalEngineFoundationService | None = None,
    ) -> None:
        self._foundation = foundation or EducationalEngineFoundationService()

    def resolve_from_runtime_topic_id(
        self,
        topic_id: str,
        *,
        subject_code: str,
    ) -> str | None:
        """Validate or map a Runtime C / session topic id to published form.

        Returns None for blank, node- style, unresolved, or pure-int keys
        that cannot be mapped through artefacts.
        """
        token = (topic_id or "").strip()
        if not token:
            return None
        if token.lower().startswith(_NODE_PREFIX):
            return None
        if _PURE_INT.fullmatch(token):
            return None

        artefacts = self._load_artefacts(subject_code)
        if artefacts is None:
            return None

        published_ids = self._published_topic_ids(artefacts)
        if token in published_ids:
            return token

        by_code = self._topic_id_by_code(artefacts)
        mapped = by_code.get(token)
        if mapped is not None:
            return mapped
        return None

    def resolve_from_orm_topic(
        self,
        topic: TopicNameId,
        *,
        subject_code: str,
    ) -> str | None:
        """Map an ORM Topic-like row to published id via artefact title join.

        Matches ``topic.name`` exactly to artefact ``topics[].title``.
        Returns None when the active published package is missing or no
        title match exists.
        """
        if topic is None:
            return None
        name = (getattr(topic, "name", None) or "").strip()
        if not name:
            return None

        artefacts = self._load_artefacts(subject_code)
        if artefacts is None:
            return None

        for raw in artefacts.topics:
            if not isinstance(raw, dict):
                continue
            title = str(raw.get("title") or "").strip()
            published = str(raw.get("topic_id") or "").strip()
            if title == name and published:
                return published
        return None

    def orm_topic_id_for_published(
        self,
        published_topic_id: str,
        *,
        subject_code: str,
        topics: list[Any] | tuple[Any, ...] | None = None,
    ) -> int | None:
        """Reverse join: published id -> ORM topics.id via title.

        When ``topics`` is omitted, callers must supply the candidate ORM
        rows (Stage 1 does not invent a global curriculum scan).
        """
        token = (published_topic_id or "").strip()
        if not token or topics is None:
            return None
        artefacts = self._load_artefacts(subject_code)
        if artefacts is None:
            return None
        title = self._title_for_topic_id(artefacts, token)
        if not title:
            return None
        for row in topics:
            if (getattr(row, "name", None) or "").strip() == title:
                oid = getattr(row, "id", None)
                return int(oid) if oid is not None else None
        return None

    @staticmethod
    def is_hygienic_twin_key(topic_id: str) -> bool:
        """True when ``topic_id`` is acceptable as a Twin map key."""
        token = (topic_id or "").strip()
        if not token:
            return False
        if token.lower().startswith(_NODE_PREFIX):
            return False
        if _PURE_INT.fullmatch(token):
            return False
        return True

    def _load_artefacts(
        self, subject_code: str
    ) -> EducationalArtefactSnapshot | None:
        code = (subject_code or "").strip()
        if not code:
            return None
        return self._foundation.derive_active(code)

    @staticmethod
    def _published_topic_ids(
        artefacts: EducationalArtefactSnapshot,
    ) -> set[str]:
        ids: set[str] = set()
        progress = artefacts.progress_model
        if progress is not None:
            for tid in progress.topic_ids:
                token = str(tid).strip()
                if token:
                    ids.add(token)
        for raw in artefacts.topics:
            if isinstance(raw, dict):
                token = str(raw.get("topic_id") or "").strip()
                if token:
                    ids.add(token)
        return ids

    @staticmethod
    def _topic_id_by_code(
        artefacts: EducationalArtefactSnapshot,
    ) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for raw in artefacts.topics:
            if not isinstance(raw, dict):
                continue
            published = str(raw.get("topic_id") or "").strip()
            code = str(raw.get("code") or "").strip()
            if published and code and code not in mapping:
                mapping[code] = published
        progress = artefacts.progress_model
        if progress is not None:
            for raw in progress.topics:
                if not isinstance(raw, dict):
                    continue
                published = str(raw.get("topic_id") or "").strip()
                code = str(raw.get("topic_code") or raw.get("code") or "").strip()
                if published and code and code not in mapping:
                    mapping[code] = published
        return mapping

    @staticmethod
    def _title_for_topic_id(
        artefacts: EducationalArtefactSnapshot,
        topic_id: str,
    ) -> str | None:
        for raw in artefacts.topics:
            if not isinstance(raw, dict):
                continue
            if str(raw.get("topic_id") or "").strip() != topic_id:
                continue
            title = str(raw.get("title") or "").strip()
            return title or None
        return None


def artefact_topic_index(
    artefacts: EducationalArtefactSnapshot | None,
) -> dict[str, dict[str, Any]]:
    """Index artefact topics by published topic_id (test/helper utility)."""
    if artefacts is None:
        return {}
    out: dict[str, dict[str, Any]] = {}
    for raw in artefacts.topics:
        if isinstance(raw, dict):
            tid = str(raw.get("topic_id") or "").strip()
            if tid:
                out[tid] = raw
    return out

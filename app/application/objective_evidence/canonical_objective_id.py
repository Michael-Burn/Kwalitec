"""Canonical published learning-objective id resolution (OEA Phase 1).

Preserves LO-level identity. Never collapses an LO code or objective id
into a parent topic id (the opposite of ``CanonicalTopicId``).

Backed by EducationalEngineFoundationService artefacts that already expose
``objective_id``, ``code``, and ``topic_id``. Does not modify
``CanonicalTopicId``.
"""

from __future__ import annotations

import re

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)

_NODE_PREFIX = "node-"
_PURE_INT = re.compile(r"^[0-9]+$")


class CanonicalObjectiveId:
    """Resolve LO codes and published objective ids to published objective ids."""

    def __init__(
        self,
        *,
        foundation: EducationalEngineFoundationService | None = None,
    ) -> None:
        self._foundation = foundation or EducationalEngineFoundationService()

    def resolve(
        self,
        token: str,
        *,
        subject_code: str,
    ) -> str | None:
        """Resolve a published objective id or syllabus LO code.

        Accepts published ``objective_id`` values (e.g. ``CS1-B-T01-LO04``)
        and LO-level syllabus codes / numbers (e.g. ``2.1.4``).

        Returns None for blank, node- style, pure-int, unresolved, or
        topic-only tokens that are not LO identities.
        """
        raw = (token or "").strip()
        if not raw:
            return None
        if raw.lower().startswith(_NODE_PREFIX):
            return None
        if _PURE_INT.fullmatch(raw):
            return None

        artefacts = self._load_artefacts(subject_code)
        if artefacts is None:
            return None

        by_id = self._objective_ids(artefacts)
        if raw in by_id:
            return raw

        by_code = self._objective_id_by_code(artefacts)
        return by_code.get(raw)

    def resolve_from_code(
        self,
        code: str,
        *,
        subject_code: str,
    ) -> str | None:
        """Map a syllabus LO code (e.g. ``2.1.4``) to published ``objective_id``."""
        return self.resolve(code, subject_code=subject_code)

    def resolve_from_objective_id(
        self,
        objective_id: str,
        *,
        subject_code: str,
    ) -> str | None:
        """Validate a published ``objective_id`` against active artefacts."""
        token = (objective_id or "").strip()
        if not token:
            return None
        artefacts = self._load_artefacts(subject_code)
        if artefacts is None:
            return None
        if token in self._objective_ids(artefacts):
            return token
        return None

    def resolve_from_topic_focus_lo(
        self,
        topic_focus_lo: str,
        *,
        subject_code: str,
    ) -> str | None:
        """Map a package ``topic_focus_lo`` code to published ``objective_id``.

        Package JSON stores LO focus as a syllabus code (e.g. ``2.1.4``).
        This is the runtime path from package → code → objective_id.
        """
        return self.resolve_from_code(
            topic_focus_lo,
            subject_code=subject_code,
        )

    def _load_artefacts(
        self, subject_code: str
    ) -> EducationalArtefactSnapshot | None:
        code = (subject_code or "").strip()
        if not code:
            return None
        return self._foundation.derive_active(code)

    @staticmethod
    def _objective_ids(artefacts: EducationalArtefactSnapshot) -> set[str]:
        ids: set[str] = set()
        for raw in artefacts.objectives:
            if not isinstance(raw, dict):
                continue
            token = str(raw.get("objective_id") or "").strip()
            if token:
                ids.add(token)
        return ids

    @staticmethod
    def _objective_id_by_code(
        artefacts: EducationalArtefactSnapshot,
    ) -> dict[str, str]:
        """Map syllabus LO codes (and objective numbers) to objective ids."""
        mapping: dict[str, str] = {}
        for raw in artefacts.objectives:
            if not isinstance(raw, dict):
                continue
            oid = str(raw.get("objective_id") or "").strip()
            if not oid:
                continue
            for field in ("code", "number"):
                token = str(raw.get(field) or "").strip()
                if token and token not in mapping:
                    mapping[token] = oid
        return mapping

"""Resolve genuine practiced Twin keys from package return_targets.

Campaign revision packages (e.g. CR-R1) remount mission ``topic_id`` /
``topic_code`` onto a tip-surrogate topic for mission generation only
(PX-B-005). Evidence writers must not treat that surrogate as practiced
identity. When the certified package names real ``return_targets``, those
targets are the practiced curriculum, resolved with the same LO→published
Twin-key mapping Policy V1 already uses for block weakness scoring.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from app.application.adaptive_decision.policy_v1 import (
    _resolve_return_target_twin_key,
)
from app.application.student_twin.canonical_topic_id import CanonicalTopicId

logger = logging.getLogger(__name__)

SOURCE_RETURN_TARGETS = "return_targets"
SOURCE_NONE = "none"


@dataclass(frozen=True)
class PracticedTwinKeyResolution:
    """Outcome of resolving package return_targets to Twin published keys.

    ``twin_keys`` is order-preserving and de-duplicated. When the package
    exposes non-empty return_targets but none resolve, ``unresolved`` is
    True and callers must skip tip-surrogate attribution rather than guess.
    """

    twin_keys: tuple[str, ...]
    return_targets: tuple[str, ...]
    source: str
    unresolved: bool
    educational_package_id: str = ""

    @property
    def has_return_targets(self) -> bool:
        return bool(self.return_targets)


def load_package_return_targets(package_id: str) -> tuple[str, ...]:
    """Return authored return_targets for a certified educational package."""
    pid = (package_id or "").strip()
    if not pid:
        return ()
    try:
        from app.application.educational_packages.loader import find_package_by_id

        pack = find_package_by_id(pid)
    except Exception:  # noqa: BLE001 — fail-open to empty
        logger.debug(
            "practiced_identity package lookup failed package=%s",
            pid,
            exc_info=True,
        )
        return ()
    if pack is None:
        return ()
    return tuple(
        str(t).strip()
        for t in (pack.return_targets or ())
        if str(t or "").strip()
    )


def package_subject_code(package_id: str, *, fallback: str = "") -> str:
    """Subject owning the package's return_targets, else ``fallback``."""
    pid = (package_id or "").strip()
    if pid:
        try:
            from app.application.educational_packages.loader import find_package_by_id

            pack = find_package_by_id(pid)
            if pack is not None:
                subject = str(getattr(pack, "subject_id", "") or "").strip()
                if subject:
                    return subject
        except Exception:  # noqa: BLE001
            logger.debug(
                "practiced_identity subject lookup failed package=%s",
                pid,
                exc_info=True,
            )
    return (fallback or "").strip()


def resolve_practiced_twin_keys(
    *,
    educational_package_id: str | None,
    subject_code: str,
    canonical: CanonicalTopicId | None = None,
) -> PracticedTwinKeyResolution:
    """Map package return_targets to unique Twin published topic keys.

    Reuses Policy V1's ``_resolve_return_target_twin_key`` without changing
    weakness scoring. Packages without return_targets yield ``source=none``
    so callers can keep their ordinary single-topic path.
    """
    pack_id = (educational_package_id or "").strip()
    targets = load_package_return_targets(pack_id)
    if not targets:
        return PracticedTwinKeyResolution(
            twin_keys=(),
            return_targets=(),
            source=SOURCE_NONE,
            unresolved=False,
            educational_package_id=pack_id,
        )

    resolve_subject = package_subject_code(pack_id, fallback=subject_code)
    resolver = canonical or CanonicalTopicId()
    keys: list[str] = []
    seen: set[str] = set()
    for raw in targets:
        pub = _resolve_return_target_twin_key(
            raw, subject_code=resolve_subject, canonical=resolver
        )
        if not pub or pub in seen:
            continue
        seen.add(pub)
        keys.append(pub)

    if not keys:
        logger.info(
            "practiced_identity return_targets_unresolved package=%s "
            "subject=%s targets=%s",
            pack_id,
            resolve_subject,
            list(targets),
        )
        return PracticedTwinKeyResolution(
            twin_keys=(),
            return_targets=targets,
            source=SOURCE_RETURN_TARGETS,
            unresolved=True,
            educational_package_id=pack_id,
        )

    return PracticedTwinKeyResolution(
        twin_keys=tuple(keys),
        return_targets=targets,
        source=SOURCE_RETURN_TARGETS,
        unresolved=False,
        educational_package_id=pack_id,
    )


def educational_package_id_from_session_metadata(
    metadata: dict[str, Any] | None,
) -> str:
    """Read educational package id from evidence-package session_metadata."""
    if not isinstance(metadata, dict):
        return ""
    return str(metadata.get("educational_package_id") or "").strip()


def subject_code_from_curriculum_identity(curriculum_identity: str) -> str:
    """Extract subject code from ``CS1:edition`` / ``CS1`` identity forms."""
    raw = (curriculum_identity or "").strip()
    if not raw:
        return ""
    return raw.split(":", 1)[0].strip()


def syllabus_code_for_twin_key(
    twin_key: str,
    *,
    subject_code: str,
    canonical: CanonicalTopicId | None = None,
) -> str | None:
    """Map a published Twin topic id back to its syllabus topic code."""
    del canonical  # reserved for callers that already hold a CanonicalTopicId
    token = (twin_key or "").strip()
    subject = (subject_code or "").strip()
    if not token or not subject:
        return None
    try:
        from app.application.educational_engine_foundation.service import (
            EducationalEngineFoundationService,
        )

        artefacts = EducationalEngineFoundationService().derive_active(subject)
    except Exception:  # noqa: BLE001
        return None
    if artefacts is None:
        return None
    for raw in artefacts.topics or ():
        if not isinstance(raw, dict):
            continue
        if str(raw.get("topic_id") or "").strip() != token:
            continue
        code = str(raw.get("code") or raw.get("topic_code") or "").strip()
        if code:
            return code
    return None

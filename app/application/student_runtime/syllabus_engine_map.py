"""Map Runtime C syllabus identity to Curriculum Engine / SQL exam identity.

Runtime C uses Studio ``subject_code`` + ``version_label`` (e.g. ``CS1`` /
``2027.1``). The Curriculum Engine and SQL ``Curriculum`` rows use
``exam_name`` + on-disk version (e.g. ``IFoA CS1`` / ``2026``).

This helper is catalogue-driven via ``CurriculumRepository.list_exams()`` —
case-insensitive paper match — and never invents syllabus structure.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.curriculum.models import CurriculumDefinition
from app.curriculum.repository import CurriculumRepository

logger = logging.getLogger(__name__)

# Distinct marker for tests / ops when Studio version ≠ on-disk engine version.
VERSION_MISMATCH_FALLBACK_MARKER = "version mismatch fallback used"


@dataclass(frozen=True)
class EngineSyllabusIdentity:
    """Engine / SQL curriculum coordinates for a Runtime C subject."""

    exam_name: str
    version: str
    organisation: str
    paper: str
    version_mismatch_fallback: bool = False


def map_runtime_syllabus_to_engine(
    subject_code: str | None,
    version_label: str | None = None,
    *,
    repo: CurriculumRepository | None = None,
) -> EngineSyllabusIdentity | None:
    """Map Runtime C ``(subject_code, version_label)`` to engine exam identity.

    Matching:
    - Paper equals ``subject_code`` (case-insensitive) via ``list_exams()``.
    - Version: prefer exact match to ``version_label`` among discoverable
      versions; otherwise fall back to the latest discoverable version for
      that org/paper and set ``version_mismatch_fallback`` (logged distinctly).

    Args:
        subject_code: Runtime C / Studio subject (e.g. ``"CS1"``).
        version_label: Studio version label (e.g. ``"2027.1"``); may not
            match on-disk engine years.
        repo: Optional CurriculumRepository (tests may inject).

    Returns:
        EngineSyllabusIdentity when mappable, else ``None``.
    """
    paper_key = (subject_code or "").strip()
    if not paper_key:
        return None

    catalogue = repo or CurriculumRepository()
    discovered = catalogue.list_exams()
    match: tuple[str, str, list[str]] | None = None
    for organisation, paper, versions in discovered:
        if (paper or "").strip().lower() == paper_key.lower():
            match = (organisation, paper, list(versions or ()))
            break

    if match is None:
        return None

    organisation, paper, versions = match
    if not versions:
        return None

    label = (version_label or "").strip()
    sorted_versions = sorted(versions)
    if label and label in versions:
        engine_version = label
        used_fallback = False
    else:
        engine_version = sorted_versions[-1]
        used_fallback = True

    try:
        engine_curriculum = catalogue.load_auto(
            organisation, paper, engine_version
        )
    except Exception:
        logger.exception(
            "syllabus_engine_map load_auto failed org=%s paper=%s version=%s",
            organisation,
            paper,
            engine_version,
        )
        return None

    if isinstance(engine_curriculum, CurriculumDefinition):
        exam_name = (
            f"{engine_curriculum.provider} {engine_curriculum.exam_code}"
        )
        org_out = str(engine_curriculum.provider)
        paper_out = str(engine_curriculum.exam_code)
    else:
        exam_name = (
            f"{engine_curriculum.organisation} {engine_curriculum.paper}"
        )
        org_out = str(engine_curriculum.organisation)
        paper_out = str(engine_curriculum.paper)

    identity = EngineSyllabusIdentity(
        exam_name=exam_name,
        version=engine_version,
        organisation=org_out,
        paper=paper_out,
        version_mismatch_fallback=used_fallback,
    )

    if used_fallback:
        logger.warning(
            "%s subject_code=%s version_label=%r -> exam=%s version=%s",
            VERSION_MISMATCH_FALLBACK_MARKER,
            paper_key,
            version_label,
            identity.exam_name,
            identity.version,
        )

    return identity

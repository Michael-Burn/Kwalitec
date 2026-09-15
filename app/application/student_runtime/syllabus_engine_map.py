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
    - Version: prefer exact match to ``version_label``, then a leading-year
      stem match (Studio ``2027.1`` to engine ``2027``). If the catalogue
      has exactly one version and neither matched, use that version and set
      ``version_mismatch_fallback`` (logged distinctly). Never pick
      lexicographic latest among multiple unmatched years.

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
    engine_version, used_fallback = _select_engine_version(label, versions)
    if engine_version is None:
        logger.warning(
            "syllabus_engine_map unmatched version subject_code=%s "
            "version_label=%r available=%s",
            paper_key,
            version_label,
            sorted(versions),
        )
        return None

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


def _year_stem(version_label: str) -> str:
    """Leading four-digit year from a Studio-style version label, else empty."""
    text = (version_label or "").strip()
    if len(text) >= 4 and text[:4].isdigit():
        return text[:4]
    return ""


def _select_engine_version(
    label: str, versions: list[str]
) -> tuple[str | None, bool]:
    """Choose an on-disk engine year without silent latest-among-many fallback.

    Returns ``(version, used_fallback)``. ``used_fallback`` is True only when
    the catalogue has a single unambiguous year and the requested label did
    not exact-match or stem-match it.
    """
    available = [str(v).strip() for v in versions if str(v).strip()]
    if not available:
        return None, False
    if label and label in available:
        return label, False
    stem = _year_stem(label)
    if stem and stem in available:
        return stem, False
    unique = sorted(set(available))
    if len(unique) == 1:
        return unique[0], True
    return None, False

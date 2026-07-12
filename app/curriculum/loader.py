"""Curriculum loader — reads JSON files from disk and constructs dataclass models.

All file I/O and deserialisation lives here.  The rest of the engine
never touches the file system directly.

Supports both V1 (flat) and V2 (hierarchical) formats with automatic detection.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from app.curriculum.exceptions import CurriculumLoadError
from app.curriculum.models import (
    Curriculum,
    CurriculumDefinition,
    LearningObjectiveDefinition,
    LearningOutcome,
    SectionDefinition,
    Topic,
    TopicDefinition,
)
from app.curriculum.schemas import detect_format, validate_instance

# Directory layout convention:
#   data/{organisation_lower}/{paper_lower}/{version}.json
_DATA_ROOT = Path(__file__).parent / "data"


# ═══════════════════════════════════════════════════════════════════════════════
# Date Parsing
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_date(raw: object) -> date:
    """Convert an ISO-8601 string or None to a ``date``."""
    if raw is None:
        return date(2099, 12, 31)
    if isinstance(raw, (datetime, date)):
        return date(raw.year, raw.month, raw.day)  # type: ignore[arg-type]
    if isinstance(raw, str):
        return date.fromisoformat(raw)
    raise CurriculumLoadError("", f"Cannot parse date from {raw!r}")


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Model Builders
# ═══════════════════════════════════════════════════════════════════════════════

def _build_learning_outcome(raw: dict[str, Any]) -> LearningOutcome:
    """Build a V1 LearningOutcome from a dict."""
    return LearningOutcome(
        id=raw["id"],
        code=raw["code"],
        description=raw["description"],
        suggested_revision_days=raw.get("suggested_revision_days", 14),
    )


def _build_topic(raw: dict[str, Any]) -> Topic:
    """Build a V1 Topic from a dict."""
    return Topic(
        id=raw["id"],
        code=raw["code"],
        title=raw["title"],
        description=raw["description"],
        weighting=float(raw["weighting"]),
        estimated_hours=float(raw["estimated_hours"]),
        difficulty=raw.get("difficulty", "intermediate"),
        prerequisites=raw.get("prerequisites", []),
        learning_outcomes=[
            _build_learning_outcome(lo) for lo in raw.get("learning_outcomes", [])
        ],
    )


def _build_curriculum_v1(data: dict[str, Any]) -> Curriculum:
    """Build a V1 Curriculum from a validated dict."""
    topics = [_build_topic(t) for t in data["topics"]]

    total_weight = sum(t.weighting for t in topics)
    total_hours = sum(t.estimated_hours for t in topics)

    return Curriculum(
        organisation=data["organisation"],
        examination=data["examination"],
        paper=data["paper"],
        syllabus_version=data["syllabus_version"],
        effective_from=_parse_date(data["effective_from"]),
        effective_to=_parse_date(data.get("effective_to")),
        total_weight=total_weight,
        estimated_total_hours=total_hours,
        topics=topics,
        metadata=data.get("metadata", {}),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Model Builders
# ═══════════════════════════════════════════════════════════════════════════════

def _build_learning_objective(raw: dict[str, Any]) -> LearningObjectiveDefinition:
    """Build a V2 LearningObjectiveDefinition from a dict."""
    metadata_raw = raw.get("metadata") or {}
    metadata = {
        str(key): str(value)
        for key, value in metadata_raw.items()
        if value is not None
    }
    return LearningObjectiveDefinition(
        id=raw["id"],
        topic_id=raw["topic_id"],
        code=raw["code"],
        description=raw["description"],
        cognitive_level=raw["cognitive_level"],
        estimated_minutes=int(raw["estimated_minutes"]),
        learning_type=raw["learning_type"],
        display_order=int(raw.get("display_order", 1)),
        metadata=metadata,
    )


def _build_topic_v2(raw: dict[str, Any]) -> TopicDefinition:
    """Build a V2 TopicDefinition from a dict."""
    return TopicDefinition(
        id=raw["id"],
        section_id=raw["section_id"],
        code=raw["code"],
        title=raw["title"],
        description=raw["description"],
        estimated_minutes=int(raw["estimated_minutes"]),
        difficulty=raw["difficulty"],
        display_order=int(raw.get("display_order", 1)),
        learning_objectives=[
            _build_learning_objective(lo) for lo in raw.get("learning_objectives", [])
        ],
    )


def _build_section(raw: dict[str, Any]) -> SectionDefinition:
    """Build a V2 SectionDefinition from a dict."""
    return SectionDefinition(
        id=raw["id"],
        code=raw["code"],
        title=raw["title"],
        description=raw["description"],
        exam_weight=float(raw["exam_weight"]),
        estimated_hours=float(raw["estimated_hours"]),
        difficulty=raw.get("difficulty", "intermediate"),
        display_order=int(raw.get("display_order", 1)),
        topics=[_build_topic_v2(t) for t in raw.get("topics", [])],
    )


def _build_curriculum_v2(data: dict[str, Any]) -> CurriculumDefinition:
    """Build a V2 CurriculumDefinition from a validated dict."""
    sections = [_build_section(s) for s in data["sections"]]

    total_hours = sum(s.estimated_hours for s in sections)

    return CurriculumDefinition(
        exam_code=data["exam_code"],
        exam_name=data["exam_name"],
        provider=data["provider"],
        version=data["version"],
        effective_date=_parse_date(data["effective_date"]),
        superseded_date=_parse_date(data.get("superseded_date")),
        total_estimated_hours=total_hours,
        description=data.get("description", ""),
        sections=sections,
        metadata=data.get("metadata", {}),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Unified Loader API
# ═══════════════════════════════════════════════════════════════════════════════

def load_from_dict(data: dict[str, Any], version: str | None = None) -> Curriculum | CurriculumDefinition:
    """Build a curriculum from an already-deserialised dict.

    Automatically detects V1 or V2 format if version is not specified.

    Args:
        data: The deserialised curriculum dictionary.
        version: Optional format version ("v1" or "v2"). If None, auto-detects.

    Returns:
        A Curriculum (V1) or CurriculumDefinition (V2) instance.

    Raises:
        CurriculumLoadError: If validation fails.
    """
    # Detect format if not specified
    if version is None:
        try:
            version = detect_format(data)
        except ValueError as e:
            raise CurriculumLoadError("<dict>", str(e)) from e

    # Validate against appropriate schema
    schema_errors = validate_instance(data, version)
    if schema_errors:
        raise CurriculumLoadError("<dict>", "; ".join(schema_errors))

    # Build appropriate model
    if version == "v1":
        return _build_curriculum_v1(data)
    elif version == "v2":
        return _build_curriculum_v2(data)
    else:
        raise CurriculumLoadError("<dict>", f"Unsupported curriculum version: {version}")


def load_from_json(path: Path | str, version: str | None = None) -> Curriculum | CurriculumDefinition:
    """Read a JSON file from disk and return a Curriculum or CurriculumDefinition.

    Args:
        path: Path to the JSON file.
        version: Optional format version ("v1" or "v2"). If None, auto-detects.

    Returns:
        A Curriculum (V1) or CurriculumDefinition (V2) instance.

    Raises:
        CurriculumLoadError: If the file cannot be read or parsed.
    """
    path = Path(path)
    try:
        raw_text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError, UnicodeDecodeError) as exc:
        raise CurriculumLoadError(str(path), str(exc)) from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise CurriculumLoadError(str(path), f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise CurriculumLoadError(str(path), "Top-level JSON must be an object")

    return load_from_dict(data, version)


def load_curriculum(
    organisation: str,
    paper: str,
    version: str,
) -> Curriculum:
    """Load a V1 curriculum using the standard directory convention.

    This function maintains backwards compatibility with existing code.
    For V2 curricula, use load_curriculum_v2() instead.

    Args:
        organisation: Examining body (e.g., 'ifoa').
        paper: Paper code (e.g., 'cs1').
        version: Syllabus version year (e.g., '2026').

    Returns:
        A Curriculum instance (V1 format).
    """
    file_path = (
        _DATA_ROOT
        / organisation.lower()
        / paper.lower()
        / f"{version}.json"
    )
    result = load_from_json(file_path, version="v1")
    # Type narrowing: we know this is V1
    assert isinstance(result, Curriculum)
    return result


def load_curriculum_v2(
    provider: str,
    exam_code: str,
    version: str,
) -> CurriculumDefinition:
    """Load a V2 curriculum using the standard directory convention.

    Args:
        provider: Examining body (e.g., 'ifoa').
        exam_code: Exam code (e.g., 'cs1').
        version: Syllabus version year (e.g., '2026').

    Returns:
        A CurriculumDefinition instance (V2 format).
    """
    file_path = (
        _DATA_ROOT
        / provider.lower()
        / exam_code.lower()
        / f"{version}.json"
    )
    result = load_from_json(file_path, version="v2")
    # Type narrowing: we know this is V2
    assert isinstance(result, CurriculumDefinition)
    return result


def discover_curricula() -> list[tuple[str, str, list[str]]]:
    """Walk the data directory and return every available curriculum.

    Returns:
        List of (organisation, paper, [versions]) tuples.
    """
    result: list[tuple[str, str, list[str]]] = []
    if not _DATA_ROOT.exists():
        return result

    for org_dir in sorted(_DATA_ROOT.iterdir()):
        if not org_dir.is_dir():
            continue
        organisation = org_dir.name.upper()
        for paper_dir in sorted(org_dir.iterdir()):
            if not paper_dir.is_dir():
                continue
            paper = paper_dir.name.upper()
            versions = sorted(
                p.stem for p in paper_dir.glob("*.json") if p.is_file()
            )
            if versions:
                result.append((organisation, paper, versions))
    return result

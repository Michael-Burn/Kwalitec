"""Curriculum loader — reads JSON files from disk and constructs dataclass models.

All file I/O and deserialisation lives here.  The rest of the engine
never touches the file system directly.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from app.curriculum.exceptions import CurriculumLoadError
from app.curriculum.models import Curriculum, LearningOutcome, Topic
from app.curriculum.schemas import validate_instance

# Directory layout convention:
#   data/{organisation_lower}/{paper_lower}/{version}.json
_DATA_ROOT = Path(__file__).parent / "data"


def _parse_date(raw: object) -> date:
    """Convert an ISO-8601 string or None to a ``date``."""
    if raw is None:
        return date(2099, 12, 31)
    if isinstance(raw, (datetime, date)):
        return date(raw.year, raw.month, raw.day)  # type: ignore[arg-type]
    if isinstance(raw, str):
        return date.fromisoformat(raw)
    raise CurriculumLoadError("", f"Cannot parse date from {raw!r}")


def _build_learning_outcome(raw: dict[str, Any]) -> LearningOutcome:
    return LearningOutcome(
        id=raw["id"],
        code=raw["code"],
        description=raw["description"],
        suggested_revision_days=raw.get("suggested_revision_days", 14),
    )


def _build_topic(raw: dict[str, Any]) -> Topic:
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


def load_from_dict(data: dict[str, Any]) -> Curriculum:
    """Build a ``Curriculum`` from an already-deserialised dict."""
    schema_errors = validate_instance(data)
    if schema_errors:
        raise CurriculumLoadError("<dict>", "; ".join(schema_errors))

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


def load_from_json(path: Path | str) -> Curriculum:
    """Read a JSON file from disk and return a ``Curriculum``."""
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

    return load_from_dict(data)


def load_curriculum(
    organisation: str,
    paper: str,
    version: str,
) -> Curriculum:
    """Load a curriculum using the standard directory convention."""
    file_path = (
        _DATA_ROOT
        / organisation.lower()
        / paper.lower()
        / f"{version}.json"
    )
    return load_from_json(file_path)


def discover_curricula() -> list[tuple[str, str, list[str]]]:
    """Walk the data directory and return every available curriculum."""
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

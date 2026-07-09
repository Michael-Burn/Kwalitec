"""JSON Schema definition for curriculum data files.

This module provides the canonical JSON Schema (Draft 2020-12) that every
curriculum file MUST validate against before being loaded into the engine.

The schema is designed to be extensible — additional metadata keys can be
added in the future without breaking existing files.
"""

from __future__ import annotations

import re
from typing import Any


def get_schema() -> dict[str, Any]:
    """Return the JSON Schema that curriculum files must conform to."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://kwalitec.dev/schemas/curriculum-v1.json",
        "title": "Kwalitec Curriculum",
        "description": "A versioned, structured representation of an examination syllabus.",
        "type": "object",
        "required": [
            "organisation",
            "examination",
            "paper",
            "syllabus_version",
            "effective_from",
            "topics",
        ],
        "properties": {
            "organisation": {
                "type": "string",
                "description": "Examining body (e.g. IFoA, CAA, SOA).",
                "minLength": 1,
            },
            "examination": {
                "type": "string",
                "description": "Overall qualification name.",
                "minLength": 1,
            },
            "paper": {
                "type": "string",
                "description": "Paper code (e.g. CS1, CM1).",
                "minLength": 1,
            },
            "syllabus_version": {
                "type": "string",
                "description": "Syllabus year (e.g. 2026).",
                "pattern": r"^\d{4}$",
            },
            "effective_from": {
                "type": "string",
                "format": "date",
                "description": "Date the syllabus becomes effective.",
            },
            "effective_to": {
                "type": ["string", "null"],
                "format": "date",
                "description": "Date the syllabus is superseded, or null.",
            },
            "metadata": {
                "type": "object",
                "description": "Arbitrary key-value metadata.",
                "additionalProperties": {"type": "string"},
            },
            "topics": {
                "type": "array",
                "description": "Ordered list of topics.",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "code",
                        "title",
                        "description",
                        "weighting",
                        "estimated_hours",
                        "difficulty",
                        "prerequisites",
                        "learning_outcomes",
                    ],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Unique topic identifier.",
                            "minLength": 1,
                        },
                        "code": {
                            "type": "string",
                            "description": "Human-readable topic code.",
                            "minLength": 1,
                        },
                        "title": {
                            "type": "string",
                            "minLength": 1,
                        },
                        "description": {
                            "type": "string",
                        },
                        "weighting": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                        },
                        "estimated_hours": {
                            "type": "number",
                            "minimum": 0,
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["foundational", "intermediate", "advanced"],
                        },
                        "prerequisites": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "learning_outcomes": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": [
                                    "id",
                                    "code",
                                    "description",
                                ],
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "minLength": 1,
                                    },
                                    "code": {
                                        "type": "string",
                                        "minLength": 1,
                                    },
                                    "description": {
                                        "type": "string",
                                    },
                                    "suggested_revision_days": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "default": 14,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }


def validate_instance(instance: dict[str, Any]) -> list[str]:
    """Validate a curriculum dict against the schema.

    Returns a list of error messages (empty = valid).  This is a lightweight
    inline validator that covers the most important constraints without
    requiring an external JSON Schema library.

    Args:
        instance: The deserialised curriculum dict.

    Returns:
        A list of human-readable error strings.
    """
    errors: list[str] = []
    schema = get_schema()

    # --- required top-level keys ---
    for key in schema["required"]:
        if key not in instance:
            errors.append(f"Missing required field: {key}")

    if errors:
        return errors

    # --- syllabus_version pattern ---
    sv = instance.get("syllabus_version", "")
    if not re.fullmatch(r"^\d{4}$", str(sv)):
        errors.append(
            f"syllabus_version must be a 4-digit year, got '{sv}'"
        )

    # --- topics array ---
    topics = instance.get("topics", [])
    if not isinstance(topics, list) or len(topics) == 0:
        errors.append("topics must be a non-empty array")
        return errors

    topic_ids: set[str] = set()
    lo_codes: set[str] = set()

    for i, topic in enumerate(topics):
        prefix = f"topics[{i}]"

        if not isinstance(topic, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        # Required topic fields
        for key in ["id", "code", "title", "weighting", "estimated_hours", "difficulty"]:
            if key not in topic:
                errors.append(f"{prefix}: missing required field '{key}'")

        tid = topic.get("id")
        if isinstance(tid, str):
            if tid in topic_ids:
                errors.append(f"{prefix}: duplicate topic id '{tid}'")
            topic_ids.add(tid)

        weighting = topic.get("weighting")
        if isinstance(weighting, (int, float)):
            if weighting < 0 or weighting > 100:
                errors.append(
                    f"{prefix}: weighting {weighting} is not in range 0–100"
                )

        hours = topic.get("estimated_hours")
        if isinstance(hours, (int, float)) and hours < 0:
            errors.append(
                f"{prefix}: estimated_hours {hours} must be >= 0"
            )

        difficulty = topic.get("difficulty")
        if difficulty not in (None, "foundational", "intermediate", "advanced"):
            errors.append(
                f"{prefix}: difficulty '{difficulty}' is not valid "
                "(must be foundational, intermediate, or advanced)"
            )

        los = topic.get("learning_outcomes", [])
        if not isinstance(los, list) or len(los) == 0:
            errors.append(f"{prefix}: learning_outcomes must be a non-empty array")
        else:
            for j, lo in enumerate(los):
                lop = f"{prefix}.learning_outcomes[{j}]"
                if not isinstance(lo, dict):
                    errors.append(f"{lop}: must be an object")
                    continue
                for key in ["id", "code", "description"]:
                    if key not in lo:
                        errors.append(f"{lop}: missing required field '{key}'")
                loc = lo.get("code")
                if isinstance(loc, str):
                    if loc in lo_codes:
                        errors.append(f"{lop}: duplicate learning outcome code '{loc}'")
                    lo_codes.add(loc)

    return errors
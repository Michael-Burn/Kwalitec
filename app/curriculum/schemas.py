"""JSON Schema definitions for curriculum data files.

This module provides JSON Schema validators for both V1 (flat) and V2 (hierarchical)
curriculum formats. Each curriculum file is validated against the appropriate schema
before being loaded into the engine.

The schemas are designed to be extensible — additional metadata keys can be
added in the future without breaking existing files.
"""

from __future__ import annotations

import re
from typing import Any


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Schema (Legacy Format)
# ═══════════════════════════════════════════════════════════════════════════════

def get_v1_schema() -> dict[str, Any]:
    """Return the V1 JSON Schema that curriculum files must conform to."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://kwalitec.dev/schemas/curriculum-v1.json",
        "title": "Kwalitec Curriculum V1",
        "description": "A versioned, structured representation of an examination syllabus (legacy format).",
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


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Schema (Canonical Hierarchical Format)
# ═══════════════════════════════════════════════════════════════════════════════

def get_v2_schema() -> dict[str, Any]:
    """Return the V2 JSON Schema that curriculum files must conform to."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://kwalitec.dev/schemas/curriculum-v2.json",
        "title": "Kwalitec Curriculum V2",
        "description": "A versioned, hierarchical representation of an examination syllabus.",
        "type": "object",
        "required": [
            "exam_code",
            "exam_name",
            "provider",
            "version",
            "effective_date",
            "sections",
        ],
        "properties": {
            "exam_code": {
                "type": "string",
                "description": "Unique exam identifier (e.g., 'CS1', 'CM1')",
                "pattern": "^[A-Z]{2}[0-9]$",
                "minLength": 3,
                "maxLength": 3,
            },
            "exam_name": {
                "type": "string",
                "description": "Full examination name (e.g., 'Actuarial Statistics')",
                "minLength": 1,
            },
            "provider": {
                "type": "string",
                "description": "Examining body (e.g., 'IFoA', 'CAA', 'SOA')",
                "minLength": 1,
            },
            "version": {
                "type": "string",
                "description": "Syllabus version year (e.g., '2026')",
                "pattern": r"^\d{4}$",
            },
            "effective_date": {
                "type": "string",
                "format": "date",
                "description": "Date the syllabus becomes effective (ISO 8601: YYYY-MM-DD)",
            },
            "superseded_date": {
                "type": ["string", "null"],
                "format": "date",
                "description": "Date the syllabus is superseded, or null if current",
            },
            "total_estimated_hours": {
                "type": "number",
                "minimum": 0,
                "description": "Total recommended study hours for the entire exam",
            },
            "description": {
                "type": "string",
                "description": "Overall exam description and objectives",
            },
            "sections": {
                "type": "array",
                "description": "Ordered list of syllabus sections",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "code",
                        "title",
                        "description",
                        "exam_weight",
                        "estimated_hours",
                        "display_order",
                        "topics",
                    ],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Stable section identifier (e.g., 'CS1-A')",
                            "pattern": r"^[A-Z]{2}[0-9]-[A-Z]$",
                        },
                        "code": {
                            "type": "string",
                            "description": "Official section code (e.g., 'CS1-A')",
                            "minLength": 1,
                        },
                        "title": {
                            "type": "string",
                            "description": "Section title",
                            "minLength": 1,
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed section description",
                        },
                        "exam_weight": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Assessment weighting percentage (e.g., 25.0 for 25%)",
                        },
                        "estimated_hours": {
                            "type": "number",
                            "minimum": 0,
                            "description": "Recommended study hours for this section",
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["foundational", "intermediate", "advanced"],
                            "description": "Overall section difficulty level",
                        },
                        "display_order": {
                            "type": "integer",
                            "minimum": 1,
                            "description": "Sequential display order (1-based)",
                        },
                        "topics": {
                            "type": "array",
                            "description": "Ordered list of topics within this section",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": [
                                    "id",
                                    "section_id",
                                    "code",
                                    "title",
                                    "description",
                                    "estimated_minutes",
                                    "difficulty",
                                    "display_order",
                                    "learning_objectives",
                                ],
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "description": "Stable topic identifier (e.g., 'CS1-A-T01')",
                                        "pattern": r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$",
                                    },
                                    "section_id": {
                                        "type": "string",
                                        "description": "Parent section identifier (e.g., 'CS1-A')",
                                        "pattern": r"^[A-Z]{2}[0-9]-[A-Z]$",
                                    },
                                    "code": {
                                        "type": "string",
                                        "description": "Official topic code (e.g., 'CS1-A.1')",
                                        "minLength": 1,
                                    },
                                    "title": {
                                        "type": "string",
                                        "description": "Topic title",
                                        "minLength": 1,
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "Detailed topic description",
                                    },
                                    "estimated_minutes": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "description": "Estimated study time in minutes",
                                    },
                                    "difficulty": {
                                        "type": "string",
                                        "enum": ["foundational", "intermediate", "advanced"],
                                        "description": "Topic difficulty level",
                                    },
                                    "display_order": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "description": "Sequential display order within section (1-based)",
                                    },
                                    "learning_objectives": {
                                        "type": "array",
                                        "description": "Ordered list of learning objectives",
                                        "minItems": 1,
                                        "items": {
                                            "type": "object",
                                            "required": [
                                                "id",
                                                "topic_id",
                                                "code",
                                                "description",
                                                "cognitive_level",
                                                "estimated_minutes",
                                                "learning_type",
                                                "display_order",
                                            ],
                                            "properties": {
                                                "id": {
                                                    "type": "string",
                                                    "description": "Stable learning objective identifier (e.g., 'CS1-A-T01-LO01')",
                                                    "pattern": r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}$",
                                                },
                                                "topic_id": {
                                                    "type": "string",
                                                    "description": "Parent topic identifier (e.g., 'CS1-A-T01')",
                                                    "pattern": r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$",
                                                },
                                                "code": {
                                                    "type": "string",
                                                    "description": "Official learning objective code (e.g., 'CS1-A.1.1')",
                                                    "minLength": 1,
                                                },
                                                "description": {
                                                    "type": "string",
                                                    "description": "Learning objective description (measurable outcome)",
                                                },
                                                "cognitive_level": {
                                                    "type": "string",
                                                    "enum": ["remember", "understand", "apply", "analyze", "evaluate", "create"],
                                                    "description": "Bloom's taxonomy cognitive level",
                                                },
                                                "estimated_minutes": {
                                                    "type": "integer",
                                                    "minimum": 0,
                                                    "description": "Estimated study time in minutes",
                                                },
                                                "learning_type": {
                                                    "type": "string",
                                                    "enum": ["concept", "procedure", "problem_solving", "application", "analysis"],
                                                    "description": "Type of learning outcome",
                                                },
                                                "display_order": {
                                                    "type": "integer",
                                                    "minimum": 1,
                                                    "description": "Sequential display order within topic (1-based)",
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "metadata": {
                "type": "object",
                "description": "Arbitrary key-value metadata for future extensibility",
                "additionalProperties": {
                    "type": "string"
                },
            },
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Unified Schema API
# ═══════════════════════════════════════════════════════════════════════════════

def get_schema(version: str = "v1") -> dict[str, Any]:
    """Return the JSON Schema for the specified curriculum version.
    
    Args:
        version: Curriculum format version ("v1" or "v2").
    
    Returns:
        The JSON Schema dictionary.
    
    Raises:
        ValueError: If version is not "v1" or "v2".
    """
    if version == "v1":
        return get_v1_schema()
    elif version == "v2":
        return get_v2_schema()
    else:
        raise ValueError(f"Unknown schema version: {version}. Must be 'v1' or 'v2'.")


def detect_format(data: dict[str, Any]) -> str:
    """Detect whether a curriculum dict is V1 or V2 format.
    
    Args:
        data: The deserialized curriculum dictionary.
    
    Returns:
        "v1" if the data is in V1 format, "v2" if in V2 format.
    
    Raises:
        ValueError: If the format cannot be determined.
    """
    # V2 format has 'sections' and 'exam_code'
    if "sections" in data and "exam_code" in data:
        return "v2"
    # V1 format has 'topics' and 'organisation'
    elif "topics" in data and "organisation" in data:
        return "v1"
    else:
        raise ValueError(
            "Cannot determine curriculum format. "
            "Expected either V1 keys (organisation, examination, paper, topics) "
            "or V2 keys (exam_code, exam_name, provider, sections)."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Validation (Legacy)
# ═══════════════════════════════════════════════════════════════════════════════

def validate_v1_instance(instance: dict[str, Any]) -> list[str]:
    """Validate a V1 curriculum dict against the schema.

    Returns a list of error messages (empty = valid).

    Args:
        instance: The deserialised V1 curriculum dict.

    Returns:
        A list of human-readable error strings.
    """
    errors: list[str] = []
    schema = get_v1_schema()

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


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Validation (Canonical Format)
# ═══════════════════════════════════════════════════════════════════════════════

def validate_v2_instance(instance: dict[str, Any]) -> list[str]:
    """Validate a V2 curriculum dict against the schema.

    Returns a list of error messages (empty = valid).

    Args:
        instance: The deserialised V2 curriculum dict.

    Returns:
        A list of human-readable error strings.
    """
    errors: list[str] = []
    schema = get_v2_schema()

    # --- required top-level keys ---
    for key in schema["required"]:
        if key not in instance:
            errors.append(f"Missing required field: {key}")

    if errors:
        return errors

    # --- version pattern ---
    version = instance.get("version", "")
    if not re.fullmatch(r"^\d{4}$", str(version)):
        errors.append(f"version must be a 4-digit year, got '{version}'")

    # --- exam_code pattern ---
    exam_code = instance.get("exam_code", "")
    if not re.fullmatch(r"^[A-Z]{2}[0-9]$", str(exam_code)):
        errors.append(
            f"exam_code must match pattern [A-Z]{{2}}[0-9] (e.g., 'CS1'), got '{exam_code}'"
        )

    # --- sections array ---
    sections = instance.get("sections", [])
    if not isinstance(sections, list) or len(sections) == 0:
        errors.append("sections must be a non-empty array")
        return errors

    section_ids: set[str] = set()
    topic_ids: set[str] = set()
    lo_ids: set[str] = set()
    lo_codes: set[str] = set()
    total_weight = 0.0

    for i, section in enumerate(sections):
        prefix = f"sections[{i}]"

        if not isinstance(section, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        # Required section fields
        for key in ["id", "code", "title", "description", "exam_weight", "estimated_hours", "display_order", "topics"]:
            if key not in section:
                errors.append(f"{prefix}: missing required field '{key}'")

        # Section ID pattern
        sid = section.get("id")
        if isinstance(sid, str):
            if not re.fullmatch(r"^[A-Z]{2}[0-9]-[A-Z]$", sid):
                errors.append(f"{prefix}: id '{sid}' does not match pattern [A-Z]{{2}}[0-9]-[A-Z]")
            if sid in section_ids:
                errors.append(f"{prefix}: duplicate section id '{sid}'")
            section_ids.add(sid)

        # Section code uniqueness
        scode = section.get("code")
        if isinstance(scode, str):
            # Note: codes can repeat across sections, but we track for now
            pass

        # Exam weight
        weight = section.get("exam_weight")
        if isinstance(weight, (int, float)):
            if weight < 0 or weight > 100:
                errors.append(f"{prefix}: exam_weight {weight} is not in range 0–100")
            else:
                total_weight += weight

        # Estimated hours
        hours = section.get("estimated_hours")
        if isinstance(hours, (int, float)) and hours < 0:
            errors.append(f"{prefix}: estimated_hours {hours} must be >= 0")

        # Difficulty
        difficulty = section.get("difficulty")
        if difficulty not in (None, "foundational", "intermediate", "advanced"):
            errors.append(
                f"{prefix}: difficulty '{difficulty}' is not valid "
                "(must be foundational, intermediate, or advanced)"
            )

        # Topics
        topics = section.get("topics", [])
        if not isinstance(topics, list) or len(topics) == 0:
            errors.append(f"{prefix}: topics must be a non-empty array")
            continue

        for j, topic in enumerate(topics):
            tprefix = f"{prefix}.topics[{j}]"

            if not isinstance(topic, dict):
                errors.append(f"{tprefix}: must be an object")
                continue

            # Required topic fields
            for key in ["id", "section_id", "code", "title", "description", "estimated_minutes", "difficulty", "display_order", "learning_objectives"]:
                if key not in topic:
                    errors.append(f"{tprefix}: missing required field '{key}'")

            # Topic ID pattern
            tid = topic.get("id")
            if isinstance(tid, str):
                if not re.fullmatch(r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$", tid):
                    errors.append(f"{tprefix}: id '{tid}' does not match pattern [A-Z]{{2}}[0-9]-[A-Z]-T[0-9]{{2}}")
                if tid in topic_ids:
                    errors.append(f"{tprefix}: duplicate topic id '{tid}'")
                topic_ids.add(tid)

            # Section ID reference
            tsid = topic.get("section_id")
            if isinstance(tsid, str) and isinstance(sid, str):
                if tsid != sid:
                    errors.append(f"{tprefix}: section_id '{tsid}' does not match parent section id '{sid}'")

            # Estimated minutes
            mins = topic.get("estimated_minutes")
            if isinstance(mins, int) and mins < 0:
                errors.append(f"{tprefix}: estimated_minutes {mins} must be >= 0")

            # Topic difficulty
            tdiff = topic.get("difficulty")
            if tdiff not in (None, "foundational", "intermediate", "advanced"):
                errors.append(
                    f"{tprefix}: difficulty '{tdiff}' is not valid "
                    "(must be foundational, intermediate, or advanced)"
                )

            # Learning objectives
            los = topic.get("learning_objectives", [])
            if not isinstance(los, list) or len(los) == 0:
                errors.append(f"{tprefix}: learning_objectives must be a non-empty array")
                continue

            for k, lo in enumerate(los):
                loprefix = f"{tprefix}.learning_objectives[{k}]"

                if not isinstance(lo, dict):
                    errors.append(f"{loprefix}: must be an object")
                    continue

                # Required LO fields
                for key in ["id", "topic_id", "code", "description", "cognitive_level", "estimated_minutes", "learning_type", "display_order"]:
                    if key not in lo:
                        errors.append(f"{loprefix}: missing required field '{key}'")

                # LO ID pattern
                lid = lo.get("id")
                if isinstance(lid, str):
                    if not re.fullmatch(r"^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}$", lid):
                        errors.append(f"{loprefix}: id '{lid}' does not match pattern [A-Z]{{2}}[0-9]-[A-Z]-T[0-9]{{2}}-LO[0-9]{{2}}")
                    if lid in lo_ids:
                        errors.append(f"{loprefix}: duplicate learning objective id '{lid}'")
                    lo_ids.add(lid)

                # Topic ID reference
                ltid = lo.get("topic_id")
                if isinstance(ltid, str) and isinstance(tid, str):
                    if ltid != tid:
                        errors.append(f"{loprefix}: topic_id '{ltid}' does not match parent topic id '{tid}'")

                # LO code uniqueness
                lcode = lo.get("code")
                if isinstance(lcode, str):
                    if lcode in lo_codes:
                        errors.append(f"{loprefix}: duplicate learning objective code '{lcode}'")
                    lo_codes.add(lcode)

                # Cognitive level
                cog = lo.get("cognitive_level")
                if cog not in (None, "remember", "understand", "apply", "analyze", "evaluate", "create"):
                    errors.append(
                        f"{loprefix}: cognitive_level '{cog}' is not valid "
                        "(must be remember, understand, apply, analyze, evaluate, or create)"
                    )

                # Learning type
                ltype = lo.get("learning_type")
                if ltype not in (None, "concept", "procedure", "problem_solving", "application", "analysis"):
                    errors.append(
                        f"{loprefix}: learning_type '{ltype}' is not valid "
                        "(must be concept, procedure, problem_solving, application, or analysis)"
                    )

                # Estimated minutes
                lmins = lo.get("estimated_minutes")
                if isinstance(lmins, int) and lmins < 0:
                    errors.append(f"{loprefix}: estimated_minutes {lmins} must be >= 0")

    # Check total weight ≈ 100
    if abs(total_weight - 100.0) > 5.0:
        errors.append(
            f"Total section weight {total_weight:.1f}% is outside acceptable range (95–105%)"
        )

    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# Unified Validation API
# ═══════════════════════════════════════════════════════════════════════════════

def validate_instance(instance: dict[str, Any], version: str | None = None) -> list[str]:
    """Validate a curriculum dict against the appropriate schema.

    This function automatically detects the curriculum format (V1 or V2) if
    version is not specified.

    Args:
        instance: The deserialised curriculum dict.
        version: Optional format version ("v1" or "v2"). If None, auto-detects.

    Returns:
        A list of human-readable error strings (empty = valid).
    """
    if version is None:
        try:
            version = detect_format(instance)
        except ValueError as e:
            return [str(e)]

    if version == "v1":
        return validate_v1_instance(instance)
    elif version == "v2":
        return validate_v2_instance(instance)
    else:
        return [f"Unknown curriculum version: {version}"]
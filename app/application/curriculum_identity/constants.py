"""Constants for the canonical curriculum identity layer."""

from __future__ import annotations

UNKNOWN_CURRICULUM_IDENTITY = "UNKNOWN_CURRICULUM_IDENTITY"

SOURCE_PUBLISHED_CONTENT = "published_content"
SOURCE_STAGE_A_DATABASE = "stage_a_database"
SOURCE_STUDY_EVENT = "study_event"

SOURCE_SYSTEMS = frozenset(
    {
        SOURCE_PUBLISHED_CONTENT,
        SOURCE_STAGE_A_DATABASE,
        SOURCE_STUDY_EVENT,
    }
)

MAPPING_EXACT = "exact"
MAPPING_DEFENSIBLE_BUT_CHANGED = "defensible_but_changed"
MAPPING_AMBIGUOUS = "ambiguous"
MAPPING_OBSOLETE_NO_EQUIVALENT = "obsolete_no_equivalent"

MAPPING_STATUSES = frozenset(
    {
        MAPPING_EXACT,
        MAPPING_DEFENSIBLE_BUT_CHANGED,
        MAPPING_AMBIGUOUS,
        MAPPING_OBSOLETE_NO_EQUIVALENT,
    }
)

STATUS_ACTIVE = "active"

ACTIVE_CS1_CURRICULUM_VERSION = "CS1:2026.1"
ACTIVE_CS1_STAGE_A_SOURCE_VERSION = "IFoA CS1:2026"

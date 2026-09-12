"""F2a — Mixed practice claim honesty.

Revision-lifecycle recommendations must not claim a mixed-topic or
interleaved practice mechanism. Classic within-session interleaving stays
closed under EF-001; live revision missions are single-purpose templates,
not a mixed-topic practice engine.
"""

from __future__ import annotations

from pathlib import Path

SRC = (
    Path(__file__).resolve().parents[1]
    / "app/services/recommendation_service.py"
).read_text(encoding="utf-8")


def test_revision_lifecycle_copy_does_not_claim_mixed_practice():
    assert "Mixed practice consolidates" not in SRC
    assert "Complete a mixed-topic practice set" not in SRC
    assert "Build exam fluency across the full syllabus." not in SRC
    assert "Complete a revision practice session" in SRC
    assert "Revision practice consolidates " in SRC
    assert "completed topics rather than advancing unread material." in SRC
    assert "Maintain fluency on material you have already covered." in SRC

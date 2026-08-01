"""Certified guidance enforcement (PB-002 F7).

Subjects with live publication_approved packages must never silently fall
back to LO-shell Reading. When no package resolves, withhold honestly.
"""

from __future__ import annotations

from functools import lru_cache

WITHHOLD_STUDENT_COPY = (
    "Kwalitec publishes only educationally certified CMP partnership guidance. "
    "Certified guidance for Study {code} is not yet available, so we will not "
    "start a session that would downgrade educational quality. Your syllabus "
    "position is saved. Continue studying this topic in your CMP until "
    "certified guidance is published."
)


def withhold_message(*, topic_code: str = "") -> str:
    """Student-facing copy when certified guidance is unavailable."""
    code = (topic_code or "").strip() or "this topic"
    return WITHHOLD_STUDENT_COPY.format(code=code)


@lru_cache(maxsize=16)
def certified_guidance_enforced(subject_id: str) -> bool:
    """True when this subject has ≥1 publication_approved package on disk."""
    from app.application.educational_packages.loader import EducationalPackageLoader

    sid = (subject_id or "").strip().upper()
    if not sid:
        return False
    return any(
        p.subject_id.upper() == sid
        for p in EducationalPackageLoader().all_approved()
    )


def reset_certified_guidance_cache() -> None:
    """Clear enforcement cache (tests)."""
    certified_guidance_enforced.cache_clear()

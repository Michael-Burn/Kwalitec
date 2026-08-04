"""Package-bound student chrome helpers (PX-003 / PX-B-001 · PX-B-002).

Resolves display titles and after-completion lines from educational_package_id
first. Never drives student Home / Finish chrome from topic_title_keywords alone.
Does not change package selection policy.
"""

from __future__ import annotations

from app.application.educational_packages.loader import (
    find_package_by_id,
    packages_for_subject,
)
from app.application.educational_packages.models import CertifiedEducationalPackage
from app.application.educational_packages.selection import (
    resolve_active_educational_package,
)


def resolve_package_for_student_chrome(
    *,
    educational_package_id: str = "",
    subject_id: str = "",
    syllabus_topic_code: str = "",
    completed_package_ids: frozenset[str] | set[str] | None = None,
    last_completed_package_id: str = "",
) -> CertifiedEducationalPackage | None:
    """Resolve the package whose display identity should drive student chrome.

    Order:
    1. Explicit educational_package_id (mission / sitting binding)
    2. Campaign selection via completed journey state
    3. Unique topic_code match only (never shared-code first-match; never
       title-keyword alone)
    """
    pid = (educational_package_id or "").strip()
    if pid:
        pack = find_package_by_id(pid)
        if pack is not None:
            return pack

    subject = (subject_id or "").strip()
    code = (syllabus_topic_code or "").strip()
    last_id = (last_completed_package_id or "").strip()
    if subject and (completed_package_ids is not None or last_id):
        pack = resolve_active_educational_package(
            subject_id=subject,
            syllabus_topic_code=code,
            completed_package_ids=completed_package_ids,
            last_completed_package_id=last_id,
        )
        if pack is not None:
            return pack

    if not code:
        return None
    candidates = packages_for_subject(subject) if subject else ()
    if not candidates:
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        candidates = EducationalPackageLoader().all_approved()
    matches = [p for p in candidates if p.topic_code == code]
    if len(matches) == 1:
        return matches[0]
    return None


def display_title_for_package_id(package_id: str) -> str | None:
    """Return certified display_title for an exact package id, if any."""
    pack = find_package_by_id(package_id)
    if pack is None:
        return None
    title = (pack.display_title or "").strip()
    return title or None


def expected_benefit_for_package_id(package_id: str) -> str | None:
    """Return certified expected_benefit for an exact package id, if any."""
    pack = find_package_by_id(package_id)
    if pack is None:
        return None
    benefit = (pack.expected_benefit or "").strip()
    return benefit or None

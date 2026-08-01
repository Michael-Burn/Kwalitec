"""Student-facing Tomorrow Preview chrome from approved package metadata (RO1-R1).

Presentation / composition helpers only. Does not change package selection for
session substance delivery — that remains PB-002 / Runtime. Never infers the
next study day solely from shared topic_code first-match or title keywords.
"""

from __future__ import annotations

from app.application.educational_packages.loader import find_package_by_id
from app.application.educational_packages.models import CertifiedEducationalPackage
from app.application.educational_packages.selection import (
    entry_package_for_topic,
    packages_for_subject,
    resolve_active_educational_package,
)


def format_tomorrow_preview_text(
    pack: CertifiedEducationalPackage,
    *,
    next_recommendation: str = "",
) -> str:
    """Render approved package tomorrow_preview fields for Finish / summary chrome."""
    tomorrow = pack.tomorrow
    if tomorrow.student_facing:
        return tomorrow.student_facing.strip()
    if tomorrow.continuity_line:
        label = tomorrow.next_topic_title or next_recommendation
        if label:
            code = tomorrow.next_topic_code
            prefix = f"Tomorrow: {code} — {label}." if code else f"Tomorrow: {label}."
            return f"{prefix} {tomorrow.continuity_line}".strip()
        return tomorrow.continuity_line.strip()
    if tomorrow.next_topic_title:
        code = tomorrow.next_topic_code
        if code:
            return f"Tomorrow: {code} — {tomorrow.next_topic_title}."
        return f"Tomorrow: {tomorrow.next_topic_title}."
    return ""


def resolve_package_for_tomorrow_chrome(
    *,
    educational_package_id: str = "",
    subject_id: str = "",
    syllabus_topic_code: str = "",
    topic_title: str = "",  # retained for call-site compatibility; unused
    completed_package_ids: frozenset[str] | set[str] | None = None,
    last_completed_package_id: str = "",
    prefer_completed_package: bool = False,
) -> CertifiedEducationalPackage | None:
    """Resolve the package whose tomorrow_preview should drive student chrome.

    Order:
    1. Explicit educational_package_id (sitting / mission binding)
    2. When prefer_completed_package (day-complete Home): last completed pack
    3. Campaign selection via tomorrow_preview / campaign_day chain
    4. Unique topic_code match only (never shared-code first-match; never
       title-keyword alone)
    """
    del topic_title  # unused — title keywords must not drive tomorrow chrome
    pid = (educational_package_id or "").strip()
    if pid:
        pack = find_package_by_id(pid)
        if pack is not None:
            return pack

    last_id = (last_completed_package_id or "").strip()
    if prefer_completed_package and last_id:
        pack = find_package_by_id(last_id)
        if pack is not None:
            return pack

    subject = (subject_id or "").strip()
    code = (syllabus_topic_code or "").strip()
    # Campaign selection only when journey state exists — never cold-start
    # entry_package_for_topic on shared codes (that reintroduces first-match).
    if subject and (completed_package_ids is not None or last_id):
        pack = resolve_active_educational_package(
            subject_id=subject,
            syllabus_topic_code=code,
            completed_package_ids=completed_package_ids,
            last_completed_package_id=last_id,
        )
        if pack is not None:
            return pack

    # Unique code only — shared codes without journey state stay unresolved
    # rather than returning the first sibling day package.
    if not code:
        return None
    if subject:
        candidates = packages_for_subject(subject)
    else:
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        candidates = EducationalPackageLoader().all_approved()
    matches = [p for p in candidates if p.topic_code == code]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1 and completed_package_ids is not None:
        # Journey-aware entry among remaining siblings.
        return entry_package_for_topic(
            [p for p in matches if p.package_id not in completed_package_ids],
            code,
        )
    return None

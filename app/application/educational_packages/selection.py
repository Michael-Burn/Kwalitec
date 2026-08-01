"""Select the next publication_approved package on the student journey (PB-002 F8).

Resolves multi-day shared topic_codes and campaign revision days (CA-R1 / CB-R1)
from completed package ids + tomorrow_preview — without redesigning Runtime C
syllabus progress derivation.
"""

from __future__ import annotations

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_package_by_id,
    packages_for_subject,
)
from app.application.educational_packages.models import CertifiedEducationalPackage

# Campaign day order for Alpha → Beta → Gamma → Delta → Epsilon → Zeta continuity (EP-001).
_CAMPAIGN_DAY_ORDER: dict[str, int] = {
    "CA-D1": 1,
    "CA-D2": 2,
    "CA-D3": 3,
    "CA-R1": 4,
    "CB-D1": 5,
    "CB-D2": 6,
    "CB-D3": 7,
    "CB-R1": 8,
    "CG-D1": 9,
    "CG-D2": 10,
    "CG-D3": 11,
    "CG-D4": 12,
    "CG-R1": 13,
    # Campaign Delta / CS1-003 (RO-002) — Trust Front mid-spine 4.1→4.2→5.1
    "CD-D1": 14,
    "CD-D2": 15,
    "CD-D3": 16,
    "CD-D4": 17,
    "CD-D5": 18,
    "CD-R1": 19,
    "CD-D6": 20,
    "CD-D7": 21,
    "CD-D8": 22,
    "CD-D9": 23,
    "CD-D10": 24,
    "CD-D11": 25,
    "CD-D12": 26,
    "CD-D13": 27,
    "CD-D14": 28,
    "CD-D15": 29,
    "CD-R2": 30,
    "CD-D16": 31,
    "CD-D17": 32,
    "CD-D18": 33,
    "CD-D19": 34,
    "CD-D20": 35,
    "CD-D21": 36,
    "CD-D22": 37,
    "CD-D23": 38,
    "CD-D24": 39,
    "CD-R3": 40,
    # Campaign Epsilon / CS1-005 (RO-003) — Continuity Front into 2.2
    "CE-D1": 41,
    "CE-D2": 42,
    "CE-D3": 43,
    "CE-D4": 44,
    "CE-R1": 45,
    # Campaign Zeta / CS1-006 (RO-004) — Continuity Front into 2.3
    "CZ-D1": 46,
    "CZ-D2": 47,
    "CZ-R1": 48,
}


def campaign_day_sort_key(pack: CertifiedEducationalPackage) -> tuple:
    """Stable sort: campaign day sequence, then package id."""
    day = (pack.campaign_day or "").strip().upper()
    return (_CAMPAIGN_DAY_ORDER.get(day, 99), pack.package_id)


def resolve_active_educational_package(
    *,
    subject_id: str,
    syllabus_topic_code: str = "",
    completed_package_ids: frozenset[str] | set[str] | None = None,
    last_completed_package_id: str = "",
) -> CertifiedEducationalPackage | None:
    """Next sitting package for an authorised student journey."""
    completed = frozenset(
        str(pid).strip()
        for pid in (completed_package_ids or ())
        if str(pid).strip()
    )
    approved = [
        p
        for p in packages_for_subject(subject_id)
        if p.package_id not in completed
    ]
    if not approved:
        return None

    last_id = (last_completed_package_id or "").strip()
    last = find_package_by_id(last_id) if last_id else None
    if last is not None:
        nxt = resolve_package_successor(last, approved)
        if nxt is not None:
            return nxt

    return entry_package_for_topic(approved, syllabus_topic_code)


def resolve_package_successor(
    last: CertifiedEducationalPackage,
    candidates: list[CertifiedEducationalPackage]
    | tuple[CertifiedEducationalPackage, ...],
) -> CertifiedEducationalPackage | None:
    """Follow tomorrow_preview.next_topic_code into the next uncompleted pack."""
    code = (last.tomorrow.next_topic_code or "").strip()
    if not code:
        return None
    matches = [
        p
        for p in candidates
        if p.topic_code == code or p.campaign_day == code
    ]
    if not matches:
        return None
    return min(matches, key=campaign_day_sort_key)


def entry_package_for_topic(
    candidates: list[CertifiedEducationalPackage]
    | tuple[CertifiedEducationalPackage, ...],
    syllabus_topic_code: str,
) -> CertifiedEducationalPackage | None:
    """First uncompleted package for a syllabus topic code (cold / realign)."""
    code = (syllabus_topic_code or "").strip()
    if not code:
        return None
    # Revision / campaign-day codes are chain-only — not Baseline cold starts.
    if code.upper() in _CAMPAIGN_DAY_ORDER and not code[0].isdigit():
        return None
    matches = [p for p in candidates if p.topic_code == code]
    if not matches:
        return None
    return min(matches, key=campaign_day_sort_key)


def should_suppress_topic_completed(
    pack: CertifiedEducationalPackage,
    *,
    completed_package_ids: frozenset[str] | set[str] | None = None,
) -> bool:
    """True while the package chain still owes a same-leaf or revision day."""
    completed = frozenset(completed_package_ids or ()) | {pack.package_id}
    remaining = [
        p
        for p in packages_for_subject(pack.subject_id)
        if p.package_id not in completed
    ]
    nxt = resolve_package_successor(pack, remaining)
    if nxt is None:
        return False
    if (nxt.mode or "").strip().lower() == "revision":
        return True
    if nxt.topic_code == pack.topic_code:
        return True
    return False


def reset_selection_caches() -> None:
    """Clear loader caches used by selection (tests)."""
    EducationalPackageLoader._load_all.cache_clear()

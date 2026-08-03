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

# Campaign day order for Alpha → … → Nu → Xi continuity (EP-001).
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
    # Campaign Eta / CS1-007 (RO-005) — Continuity Front into 2.4
    "CH-D1": 49,
    "CH-D2": 50,
    "CH-R1": 51,
    # Campaign Theta / CS1-008 (RO-006) — Continuity Front into 2.5
    "CT-D1": 52,
    "CT-D2": 53,
    "CT-R1": 54,
    # Campaign Iota / CS1-009 (RO-007) — Continuity Front into 2.6
    "CI-D1": 55,
    "CI-D2": 56,
    "CI-D3": 57,
    "CI-D4": 58,
    "CI-D5": 59,
    "CI-D6": 60,
    "CI-R1": 61,
    # Campaign Kappa / CS1-010 (RO-008) — Continuity Front into 3.1
    "CK-D1": 62,
    "CK-D2": 63,
    "CK-D3": 64,
    "CK-D4": 65,
    "CK-D5": 66,
    "CK-D6": 67,
    "CK-R1": 68,
    # Campaign Lambda / CS1-011 (RO-009) — Continuity Front into 3.2
    "CL-D1": 69,
    "CL-D2": 70,
    "CL-D3": 71,
    "CL-D4": 72,
    "CL-D5": 73,
    "CL-D6": 74,
    "CL-D7": 75,
    "CL-D8": 76,
    "CL-R1": 77,
    # Campaign Mu / CS1-012 (RO-010) — Continuity Front into 3.3
    "CM-D1": 78,
    "CM-D2": 79,
    "CM-D3": 80,
    "CM-D4": 81,
    "CM-D5": 82,
    "CM-R1": 83,
    # Campaign Nu / CS1-013 (RO-011) — Continuity Front join into 4.1
    "CN-D1": 84,
    "CN-D2": 85,
    "CN-D3": 86,
    "CN-D4": 87,
    "CN-D5": 88,
    "CN-R1": 89,
    # Campaign Xi / CS1-014 (RO-012) — Continuity Front join into 4.2
    "CX-D1": 90,
    "CX-D2": 91,
    "CX-D3": 92,
    "CX-D4": 93,
    "CX-D5": 94,
    "CX-D6": 95,
    "CX-D7": 96,
    "CX-D8": 97,
    "CX-D9": 98,
    "CX-D10": 99,
    "CX-R1": 100,
    # Campaign Omicron / CS1-015 (RO-013) — Continuity Front join into 5.1
    "CO-D1": 101,
    "CO-D2": 102,
    "CO-D3": 103,
    "CO-D4": 104,
    "CO-D5": 105,
    "CO-D6": 106,
    "CO-D7": 107,
    "CO-D8": 108,
    "CO-D9": 109,
    "CO-R1": 110,
}


def campaign_day_sort_key(pack: CertifiedEducationalPackage) -> tuple:
    """Stable sort: campaign day sequence, then package id."""
    day = (pack.campaign_day or "").strip().upper()
    return (_CAMPAIGN_DAY_ORDER.get(day, 999), pack.package_id)


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
    # RO-011 Continuity Front join: Nu shares topic_code 4.1 with Trust Front
    # Delta. When the journey last day is Mu/Nu, prefer the CN chain so
    # CM-R1 → CN-D1…CN-R1 is not diverted onto CD-D1… mid-chain.
    last_day = (last.campaign_day or "").strip().upper()
    if last_day.startswith(("CM-", "CN-")):
        cn_matches = [
            p
            for p in matches
            if (p.campaign_day or "").strip().upper().startswith("CN-")
        ]
        if cn_matches:
            return min(cn_matches, key=campaign_day_sort_key)
    # RO-012 Continuity Front join: Xi shares topic_code 4.2 with Trust Front
    # Delta. When the journey last day is Nu/Xi, prefer the CX chain so
    # CN-R1 → CX-D1…CX-R1 is not diverted onto CD-D6… mid-chain.
    if last_day.startswith(("CN-", "CX-")):
        cx_matches = [
            p
            for p in matches
            if (p.campaign_day or "").strip().upper().startswith("CX-")
        ]
        if cx_matches:
            return min(cx_matches, key=campaign_day_sort_key)
    # RO-013 Continuity Front join: Omicron shares topic_code 5.1 with Trust
    # Front Delta. When the journey last day is Xi/Omicron, prefer the CO
    # chain so CX-R1 → CO-D1…CO-R1 is not diverted onto CD-D16… mid-chain.
    if last_day.startswith(("CX-", "CO-")):
        co_matches = [
            p
            for p in matches
            if (p.campaign_day or "").strip().upper().startswith("CO-")
        ]
        if co_matches:
            return min(co_matches, key=campaign_day_sort_key)
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

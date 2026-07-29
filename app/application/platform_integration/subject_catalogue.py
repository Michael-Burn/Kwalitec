"""Subject Catalogue read model (PX-002 / PX-001 design).

Student-facing projection of Ready / Coming Soon subjects.
Does not redesign Educational Intelligence, CKG, or enrolment authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.curriculum_studio_foundation.dto import PublishedPackageSnapshot
from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
    PublishedSubjectDiscoveryService,
)
from app.services import examination_catalogue as catalogue
from app.services.subject_support_service import (
    SubjectSupportService,
    SupportStatus,
)

# Canonical Coming Soon copy (PX-001 Updated Student Flow).
COMING_SOON_MESSAGE = (
    "This subject’s verified curriculum is still under preparation. "
    "It will become available when publishing is complete. "
    "You cannot start studying this exam yet."
)


class CatalogueAvailability(str, Enum):
    """Student-facing catalogue availability (PX-001)."""

    READY = "ready"
    COMING_SOON = "coming_soon"


@dataclass(frozen=True)
class SubjectCatalogueEntry:
    """One Subject Catalogue card for student discovery."""

    subject_key: str
    name: str
    organisation: str
    paper: str
    availability: CatalogueAvailability
    availability_label: str
    status_label: str
    current_published_edition: str
    version: str
    release_date: datetime | None
    release_date_label: str
    selectable: bool
    preparation_message: str
    explanation: str

    @property
    def is_ready(self) -> bool:
        return self.availability is CatalogueAvailability.READY


class SubjectCatalogueService:
    """Project student Subject Catalogue entries from support + publication."""

    def __init__(
        self,
        *,
        discovery: PublishedSubjectDiscoveryService | None = None,
        authority: PublishedCurriculumAuthority | None = None,
    ) -> None:
        self._discovery = discovery or PublishedSubjectDiscoveryService()
        self._authority = authority or PublishedCurriculumAuthority()

    def list_entries(
        self, *, include_coming_soon: bool = True
    ) -> tuple[SubjectCatalogueEntry, ...]:
        """Return catalogue entries for student Choose Exam.

        Ready subjects are always included. Coming Soon may be included for
        roadmap honesty. Unavailable / Not Supported subjects are omitted.
        """
        entries: list[SubjectCatalogueEntry] = []
        seen: set[str] = set()

        for category in self._discovery.augmented_categories():
            if category.free_text_subject:
                continue
            statuses = SubjectSupportService.paper_statuses_for_category(
                category.code
            )
            for paper in category.papers:
                info = statuses.get(paper.code)
                if info is None:
                    continue
                if info.status is SupportStatus.NOT_SUPPORTED:
                    continue
                if (
                    info.status is SupportStatus.COMING_SOON
                    and not include_coming_soon
                ):
                    continue
                if category.code == PUBLISHED_CATEGORY_CODE:
                    entry = self._from_published(paper.code)
                else:
                    entry = self._from_support(category.code, paper.code)
                if entry is None or entry.subject_key in seen:
                    continue
                entries.append(entry)
                seen.add(entry.subject_key)

        return tuple(
            sorted(
                entries,
                key=lambda e: (
                    0 if e.is_ready else 1,
                    e.name.lower(),
                    e.subject_key,
                ),
            )
        )

    def get_entry(self, subject_key: str) -> SubjectCatalogueEntry | None:
        key = (subject_key or "").strip()
        if not key:
            return None
        for entry in self.list_entries(include_coming_soon=True):
            if entry.subject_key == key:
                return entry
        return None

    def parse_subject_key(self, subject_key: str) -> tuple[str, str] | None:
        """Split ``ORG:PAPER`` into organisation and paper codes."""
        raw = (subject_key or "").strip()
        if ":" not in raw:
            return None
        org, paper = raw.split(":", 1)
        org = org.strip()
        paper = paper.strip()
        if not org or not paper:
            return None
        return org, paper

    def _from_support(self, org: str, paper: str) -> SubjectCatalogueEntry:
        info = SubjectSupportService.resolve(org, paper)
        display = catalogue.format_exam_name(org, paper)
        edition = ""
        version = ""
        release: datetime | None = None
        status_label = "Published" if info.allows_plan_creation else "Under preparation"

        if info.status is SupportStatus.SUPPORTED:
            version = (
                _latest_curriculum_version(org, paper) or "Verified Curriculum"
            )
            edition = f"{display} · {version}" if version else display
            availability = CatalogueAvailability.READY
            selectable = True
            prep = ""
        else:
            availability = CatalogueAvailability.COMING_SOON
            selectable = False
            prep = COMING_SOON_MESSAGE
            edition = "Verified Curriculum under preparation"
            status_label = "Under preparation"

        return SubjectCatalogueEntry(
            subject_key=f"{org}:{paper}",
            name=display,
            organisation=org,
            paper=paper,
            availability=availability,
            availability_label=(
                "Ready"
                if availability is CatalogueAvailability.READY
                else "Coming Soon"
            ),
            status_label=status_label,
            current_published_edition=edition,
            version=version,
            release_date=release,
            release_date_label=_format_release(release),
            selectable=selectable,
            preparation_message=prep,
            explanation=info.explanation,
        )

    def _from_published(self, subject_code: str) -> SubjectCatalogueEntry | None:
        code = (subject_code or "").strip().upper()
        if not code:
            return None
        info = SubjectSupportService.resolve(PUBLISHED_CATEGORY_CODE, code)
        offer = self._discovery.get_offer(code)
        title = offer.title if offer else code
        package = self._active_package(code)
        release = _coerce_release(
            package.published_at if package is not None else None
        )
        version = (
            offer.version_label
            if offer is not None
            else (package.version_label if package is not None else "")
        )
        edition = (
            f"{title} · {version}" if version else title
        )

        if info.allows_plan_creation:
            availability = CatalogueAvailability.READY
            selectable = True
            prep = ""
            status_label = "Published"
        elif package is not None:
            # Published package exists — Founder Ready signal even when enrolment
            # is still gated. Students discover Ready; plan creation may wait.
            availability = CatalogueAvailability.READY
            selectable = False
            prep = (
                "This subject’s verified curriculum is Ready. "
                "Enrolment opens when student access is enabled."
            )
            status_label = "Published"
        else:
            availability = CatalogueAvailability.COMING_SOON
            selectable = False
            prep = COMING_SOON_MESSAGE
            status_label = "Under preparation"

        return SubjectCatalogueEntry(
            subject_key=f"{PUBLISHED_CATEGORY_CODE}:{code}",
            name=title,
            organisation=PUBLISHED_CATEGORY_CODE,
            paper=code,
            availability=availability,
            availability_label=(
                "Ready"
                if availability is CatalogueAvailability.READY
                else "Coming Soon"
            ),
            status_label=status_label,
            current_published_edition=edition,
            version=version,
            release_date=release,
            release_date_label=_format_release(release),
            selectable=selectable,
            preparation_message=prep,
            explanation=info.explanation if not selectable else (
                f"{title} is Ready. You can enrol and begin your Study Plan."
            ),
        )

    def _active_package(
        self, subject_code: str
    ) -> PublishedPackageSnapshot | None:
        for package in self._authority.list_published():
            if (
                package.is_active
                and package.subject_code.strip().upper() == subject_code
            ):
                return package
        return None


def _latest_curriculum_version(org: str, paper: str) -> str:
    from app.services.curriculum_engine_service import CurriculumEngineService

    versions = CurriculumEngineService().list_supported_versions(org, paper)
    if not versions:
        return ""
    return max(versions)


def _coerce_release(value: Any) -> datetime | None:
    """Normalise authority / ORM release timestamps to datetime.

    ``PublishedCurriculumAuthority`` contractually projects ``published_at``
    as an ISO-8601 string. ORM rows and older call sites may still supply
    ``datetime``. Accept either; never assume a single runtime type.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _format_release(value: Any) -> str:
    """Format a release timestamp for student catalogue display."""
    coerced = _coerce_release(value)
    if coerced is None:
        return ""
    return coerced.strftime("%d %b %Y")

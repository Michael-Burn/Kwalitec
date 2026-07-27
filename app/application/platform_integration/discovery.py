"""Published subject discovery for the student catalogue (PI-002A).

Surfaces active PublishedCurriculumPackage rows when discovery is enabled.
Never exposes draft / processing / review Studio versions.
"""

from __future__ import annotations

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.platform_integration.dto import PublishedSubjectOffer
from app.application.platform_integration.flags import (
    FounderStudentBridgeFlags,
    resolve_founder_student_bridge_flags,
)
from app.models.curriculum_studio_foundation import StudioFoundationSubject
from app.services import examination_catalogue as catalogue
from app.services.examination_catalogue import ExaminationCategory, Paper

# Virtual examining-body code for founder-published subjects.
PUBLISHED_CATEGORY_CODE = "Published"

_PUBLISHED_CATEGORY = ExaminationCategory(
    code=PUBLISHED_CATEGORY_CODE,
    name="Published Curriculum",
    description=(
        "Subjects published by founders through Curriculum Studio. "
        "Enrolment uses the curriculum-driven educational runtime when enabled."
    ),
    papers=[],
    sittings=["Custom"],
    targets=["Pass", "Strong Pass"],
    free_text_subject=False,
)


class PublishedSubjectDiscoveryService:
    """List founder-published subjects for student discovery."""

    def __init__(
        self,
        *,
        authority: PublishedCurriculumAuthority | None = None,
        flags: FounderStudentBridgeFlags | None = None,
    ) -> None:
        self._authority = authority or PublishedCurriculumAuthority()
        self._flags = flags

    def _resolve_flags(self) -> FounderStudentBridgeFlags:
        return self._flags or resolve_founder_student_bridge_flags()

    def discovery_enabled(self) -> bool:
        return self._resolve_flags().ENABLE_PUBLISHED_SUBJECT_DISCOVERY

    def list_active_offers(self) -> tuple[PublishedSubjectOffer, ...]:
        """Return active published packages as discovery offers.

        Empty when discovery is disabled — drafts are never included.
        """
        if not self.discovery_enabled():
            return ()

        offers: list[PublishedSubjectOffer] = []
        seen: set[str] = set()
        for package in self._authority.list_published():
            if not package.is_active:
                continue
            code = package.subject_code.strip().upper()
            if code in seen:
                continue
            seen.add(code)
            title = self._subject_title(code)
            offers.append(
                PublishedSubjectOffer(
                    subject_code=code,
                    title=title,
                    version_label=package.version_label,
                    package_id=package.package_id,
                    curriculum_identity=f"{code}:{package.version_label}",
                )
            )
        return tuple(sorted(offers, key=lambda o: o.subject_code))

    def get_offer(self, subject_code: str) -> PublishedSubjectOffer | None:
        code = (subject_code or "").strip().upper()
        if not code:
            return None
        for offer in self.list_active_offers():
            if offer.subject_code == code:
                return offer
        return None

    def is_published_category(self, category_code: str | None) -> bool:
        return (category_code or "").strip() == PUBLISHED_CATEGORY_CODE

    def augmented_categories(self) -> list[ExaminationCategory]:
        """Catalogue categories plus the Published category when discovery is on.

        Does not mutate the static examination catalogue.
        """
        categories = list(catalogue.get_categories())
        if not self.discovery_enabled():
            return categories
        offers = self.list_active_offers()
        if not offers:
            # Still expose the category so founders can verify the surface;
            # step 2 will show an empty/unsupported state.
            return [*categories, _PUBLISHED_CATEGORY]
        papers = [
            Paper(
                code=offer.subject_code,
                name=offer.subject_code,
                description=(
                    f"{offer.title} — published {offer.version_label}"
                ),
            )
            for offer in offers
        ]
        published = ExaminationCategory(
            code=_PUBLISHED_CATEGORY.code,
            name=_PUBLISHED_CATEGORY.name,
            description=_PUBLISHED_CATEGORY.description,
            papers=papers,
            sittings=list(_PUBLISHED_CATEGORY.sittings),
            targets=list(_PUBLISHED_CATEGORY.targets),
            free_text_subject=False,
        )
        return [*categories, published]

    def get_category(self, code: str) -> ExaminationCategory | None:
        """Resolve a category including the virtual Published category."""
        if self.is_published_category(code) and self.discovery_enabled():
            for category in self.augmented_categories():
                if category.code == PUBLISHED_CATEGORY_CODE:
                    return category
            return _PUBLISHED_CATEGORY
        return catalogue.get_category(code)

    def get_paper_choices(self, category_code: str) -> list[tuple[str, str]]:
        if self.is_published_category(category_code):
            category = self.get_category(category_code)
            if not category:
                return []
            return [(p.code, p.name) for p in category.papers]
        return catalogue.get_paper_choices(category_code)

    def get_category_choices(self) -> list[tuple[str, str]]:
        return [(c.code, c.name) for c in self.augmented_categories()]

    @staticmethod
    def _subject_title(subject_code: str) -> str:
        row = StudioFoundationSubject.query.filter_by(
            subject_code=subject_code
        ).first()
        if row is not None and (row.title or "").strip():
            return row.title.strip()
        return subject_code

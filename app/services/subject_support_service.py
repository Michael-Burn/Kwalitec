"""Supported Subject Integrity (PTP-001).

Determines whether an examination can produce a real Version 1 study plan
before a student invests planning time.

Support is a product trust surface:
- Supported — full syllabus is available; plan creation proceeds normally.
- Coming Soon — a planned examination that is not yet ready; explain and stop.
- Not Supported — outside Version 1; explain, stop, and offer supported options.

Curriculum discovery (on-disk syllabus JSON) is the source of truth for
*Supported*. Product announcement lists distinguish Coming Soon from Not
Supported without exposing loader internals to students.

Governing refs:
- PRODUCT_TRUST_PROGRAMME.md PTP-001
- BLIND_INTERNAL_ALPHA_REVIEW_V2.md hollow-subject trap
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.services import examination_catalogue as catalogue
from app.services.curriculum_engine_service import CurriculumEngineService


class SupportStatus(str, Enum):
    """Product-facing examination support state."""

    SUPPORTED = "supported"
    COMING_SOON = "coming_soon"
    NOT_SUPPORTED = "not_supported"


# IFoA papers announced for expansion but without a Version 1 syllabus yet.
# Presence of on-disk curriculum overrides this list (see resolve).
_COMING_SOON_PAPERS: dict[str, frozenset[str]] = {
    "IFoA": frozenset(
        {
            "CS2",
            "CM2",
            "CB1",
            "CB3",
            "CP1",
            "CP2",
            "CP3",
            "SP",
            "SA",
        }
    ),
}

_STATUS_LABELS = {
    SupportStatus.SUPPORTED: "Supported",
    SupportStatus.COMING_SOON: "Coming Soon",
    SupportStatus.NOT_SUPPORTED: "Not Supported",
}


@dataclass(frozen=True)
class SubjectSupportInfo:
    """Student-safe support verdict for one examination selection."""

    status: SupportStatus
    organisation: str
    paper: str
    label: str
    title: str
    explanation: str
    allows_plan_creation: bool
    alternatives: tuple[tuple[str, str], ...] = ()

    @property
    def is_supported(self) -> bool:
        return self.status is SupportStatus.SUPPORTED


@dataclass(frozen=True)
class CategorySupportSummary:
    """High-level support hint for an examining body on wizard step 1."""

    organisation: str
    status: SupportStatus
    label: str
    hint: str
    supported_paper_codes: tuple[str, ...] = ()


class SubjectSupportService:
    """Resolve examination support status for the study-plan wizard."""

    @staticmethod
    def list_supported_examinations() -> list[tuple[str, str]]:
        """Return Version 1 supported (organisation, paper) pairs.

        Discovery is curriculum-driven: any on-disk syllabus counts as
        Supported. Ordered by organisation then paper for stable display.
        """
        engine = CurriculumEngineService()
        found = {
            (org.upper(), paper.upper()): (org, paper)
            for org, paper, _versions in engine.list_supported_exams()
        }
        return sorted(
            found.values(),
            key=lambda pair: (pair[0].upper(), pair[1].upper()),
        )

    @staticmethod
    def has_curriculum(organisation: str, paper: str) -> bool:
        """Return True when a loadable syllabus exists for the pair."""
        if not organisation or not paper:
            return False
        engine = CurriculumEngineService()
        versions = engine.list_supported_versions(organisation, paper)
        if not versions:
            return False
        version = max(versions)
        return engine.curriculum_exists(organisation, paper, version)

    @classmethod
    def resolve(
        cls,
        organisation: str | None,
        paper: str | None,
        *,
        free_text_subject: bool = False,
    ) -> SubjectSupportInfo:
        """Determine support status for a category + paper/subject choice.

        Args:
            organisation: Examining body code (e.g. ``"IFoA"``).
            paper: Paper code or free-text subject label.
            free_text_subject: True when the category collects free text.

        Returns:
            A :class:`SubjectSupportInfo` with student-safe messaging.
        """
        org = (organisation or "").strip()
        paper_code = (paper or "").strip()
        alternatives = cls._supported_alternative_labels()

        if free_text_subject or not org:
            return SubjectSupportInfo(
                status=SupportStatus.NOT_SUPPORTED,
                organisation=org,
                paper=paper_code,
                label=_STATUS_LABELS[SupportStatus.NOT_SUPPORTED],
                title="This examination is not supported yet",
                explanation=(
                    "Kwalitec builds study plans from a full official syllabus. "
                    "Custom or free-text subjects are not available in Version 1, "
                    "so a full plan cannot be created for this choice."
                ),
                allows_plan_creation=False,
                alternatives=alternatives,
            )

        if cls.has_curriculum(org, paper_code):
            display = catalogue.format_exam_name(org, paper_code)
            return SubjectSupportInfo(
                status=SupportStatus.SUPPORTED,
                organisation=org,
                paper=paper_code,
                label=_STATUS_LABELS[SupportStatus.SUPPORTED],
                title=f"{display} is supported",
                explanation=(
                    "Kwalitec has the official syllabus for this paper and can "
                    "build a complete study plan around it."
                ),
                allows_plan_creation=True,
                alternatives=(),
            )

        coming_soon = _COMING_SOON_PAPERS.get(org, frozenset())
        if paper_code in coming_soon:
            display = catalogue.format_exam_name(org, paper_code)
            return SubjectSupportInfo(
                status=SupportStatus.COMING_SOON,
                organisation=org,
                paper=paper_code,
                label=_STATUS_LABELS[SupportStatus.COMING_SOON],
                title=f"{display} is coming soon",
                explanation=(
                    f"{display} is on Kwalitec's roadmap, but the full syllabus "
                    "is not available yet. Creating a plan now would produce an "
                    "incomplete study plan, so plan creation is paused for this "
                    "paper until it is ready."
                ),
                allows_plan_creation=False,
                alternatives=alternatives,
            )

        if paper_code:
            display = catalogue.format_exam_name(org, paper_code)
            subject_phrase = display
        else:
            subject_phrase = org or "This examination"

        return SubjectSupportInfo(
            status=SupportStatus.NOT_SUPPORTED,
            organisation=org,
            paper=paper_code,
            label=_STATUS_LABELS[SupportStatus.NOT_SUPPORTED],
            title=f"{subject_phrase} is not supported",
            explanation=(
                f"{subject_phrase} is not available in Version 1. Kwalitec only "
                "creates full study plans for examinations that have a complete "
                "syllabus ready. Please choose a supported paper instead."
            ),
            allows_plan_creation=False,
            alternatives=alternatives,
        )

    @classmethod
    def allows_plan_creation(
        cls,
        organisation: str | None,
        paper: str | None,
        *,
        free_text_subject: bool = False,
    ) -> bool:
        """Return True only when study-plan creation may proceed."""
        return cls.resolve(
            organisation, paper, free_text_subject=free_text_subject
        ).allows_plan_creation

    @classmethod
    def paper_statuses_for_category(
        cls, category_code: str
    ) -> dict[str, SubjectSupportInfo]:
        """Map each catalogue paper code to its support verdict."""
        category = catalogue.get_category(category_code)
        if not category:
            return {}
        if category.free_text_subject:
            return {
                "": cls.resolve(category_code, "", free_text_subject=True),
            }
        return {
            paper.code: cls.resolve(category_code, paper.code)
            for paper in category.papers
        }

    @classmethod
    def category_summary(cls, category_code: str) -> CategorySupportSummary:
        """Summarise support for an examining body (wizard step 1)."""
        category = catalogue.get_category(category_code)
        if not category:
            return CategorySupportSummary(
                organisation=category_code or "",
                status=SupportStatus.NOT_SUPPORTED,
                label=_STATUS_LABELS[SupportStatus.NOT_SUPPORTED],
                hint="Not available in Version 1.",
            )

        if category.free_text_subject:
            return CategorySupportSummary(
                organisation=category.code,
                status=SupportStatus.NOT_SUPPORTED,
                label=_STATUS_LABELS[SupportStatus.NOT_SUPPORTED],
                hint="Custom subjects are not available in Version 1.",
            )

        statuses = cls.paper_statuses_for_category(category.code)
        supported = tuple(
            code
            for code, info in statuses.items()
            if info.status is SupportStatus.SUPPORTED
        )
        coming_soon = any(
            info.status is SupportStatus.COMING_SOON for info in statuses.values()
        )

        if supported and (coming_soon or len(supported) < len(statuses)):
            names = ", ".join(supported)
            return CategorySupportSummary(
                organisation=category.code,
                status=SupportStatus.SUPPORTED,
                label="Partially Supported",
                hint=f"Version 1 supports {names}. Other papers are Coming Soon.",
                supported_paper_codes=supported,
            )
        if supported:
            return CategorySupportSummary(
                organisation=category.code,
                status=SupportStatus.SUPPORTED,
                label=_STATUS_LABELS[SupportStatus.SUPPORTED],
                hint="Full study plans are available for these papers.",
                supported_paper_codes=supported,
            )
        if coming_soon:
            return CategorySupportSummary(
                organisation=category.code,
                status=SupportStatus.COMING_SOON,
                label=_STATUS_LABELS[SupportStatus.COMING_SOON],
                hint="These papers are on the roadmap but not ready yet.",
            )
        return CategorySupportSummary(
            organisation=category.code,
            status=SupportStatus.NOT_SUPPORTED,
            label=_STATUS_LABELS[SupportStatus.NOT_SUPPORTED],
            hint="Not available in Version 1.",
        )

    @classmethod
    def category_summaries(cls) -> dict[str, CategorySupportSummary]:
        """Return support summaries keyed by category code."""
        return {
            category.code: cls.category_summary(category.code)
            for category in catalogue.get_categories()
        }

    @classmethod
    def _supported_alternative_labels(cls) -> tuple[tuple[str, str], ...]:
        """Return (code, display name) for student-facing alternatives."""
        alternatives: list[tuple[str, str]] = []
        for org, paper in cls.list_supported_examinations():
            display = catalogue.format_exam_name(org, paper)
            description = catalogue.get_paper_description(org, paper)
            label = f"{display} — {description}" if description else display
            alternatives.append((f"{org}:{paper}", label))
        return tuple(alternatives)

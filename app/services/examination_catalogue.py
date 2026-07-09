"""Examination catalogue for the Study Plan Wizard.

A deterministic, data-driven catalogue of examination categories, their
papers/subjects, sittings, and target result labels.  This module keeps all
exam-specific knowledge out of routes and templates so the wizard can be
extended by editing a single Python file.

No AI, no heuristics — just structured data.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────────────────────────
# Data structures
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Paper:
    """A paper or subject within an examination category."""

    code: str
    name: str
    description: str = ""


@dataclass(frozen=True)
class ExaminationCategory:
    """An examination category (e.g. IFoA, CFA, University)."""

    code: str
    name: str
    description: str
    papers: list[Paper] = field(default_factory=list)
    sittings: list[str] = field(default_factory=list)
    targets: list[str] = field(default_factory=list)
    free_text_subject: bool = False
    """When True the wizard collects a free-text subject instead of a paper."""


# ─────────────────────────────────────────────────────────────────────────────
# Catalogue
# ─────────────────────────────────────────────────────────────────────────────


_IFOA_PAPERS = [
    Paper("CS1", "CS1", "Actuarial Statistics 1"),
    Paper("CS2", "CS2", "Risk Modelling and Survival Analysis"),
    Paper("CM1", "CM1", "Actuarial Mathematics 1"),
    Paper("CM2", "CM2", "Loss Reserving and Financial Engineering"),
    Paper("CB1", "CB1", "Business Finance"),
    Paper("CB2", "CB2", "Business Economics"),
    Paper("CB3", "CB3", "Business Management"),
    Paper("CP1", "CP1", "Actuarial Practice 1"),
    Paper("CP2", "CP2", "Modelling Practice"),
    Paper("CP3", "CP3", "Communications Practice"),
    Paper("SP", "SP papers", "Specialist Principles — choose your SP paper"),
    Paper("SA", "SA papers", "Specialist Advanced — choose your SA paper"),
]

_CFA_LEVELS = [
    Paper("Level I", "Level I", "Foundation of investment tools"),
    Paper("Level II", "Level II", "Asset valuation and applications"),
    Paper("Level III", "Level III", "Portfolio management and wealth planning"),
]

_ACCA_PAPERS = [
    Paper("AB", "Accountant in Business (AB)", "Foundations level"),
    Paper("MA", "Management Accounting (MA)", "Foundations level"),
    Paper("FA", "Financial Accounting (FA)", "Foundations level"),
    Paper("LW", "Corporate and Business Law (LW)", "Applied Knowledge"),
    Paper("PM", "Performance Management (PM)", "Applied Skills"),
    Paper("TX", "Taxation (TX)", "Applied Skills"),
    Paper("FR", "Financial Reporting (FR)", "Applied Skills"),
    Paper("AA", "Audit and Assurance (AA)", "Applied Skills"),
    Paper("FM", "Financial Management (FM)", "Applied Skills"),
    Paper("SBR", "Strategic Business Reporting (SBR)", "Strategic Professional"),
    Paper("SBL", "Strategic Business Leader (SBL)", "Strategic Professional"),
    Paper("AFM", "Advanced Financial Management (AFM)", "Strategic Professional — options"),
    Paper("APM", "Advanced Performance Management (APM)", "Strategic Professional — options"),
    Paper("ATX", "Advanced Taxation (ATX)", "Strategic Professional — options"),
    Paper("AAA", "Advanced Audit and Assurance (AAA)", "Strategic Professional — options"),
]

_CIMA_PAPERS = [
    Paper("BA1", "BA1 Fundamentals of Business Economics", "Certificate level"),
    Paper("BA2", "BA2 Fundamentals of Management Accounting", "Certificate level"),
    Paper("BA3", "BA3 Fundamentals of Financial Accounting", "Certificate level"),
    Paper("BA4", "BA4 Fundamentals of Technology and Finance", "Certificate level"),
    Paper("E1", "E1 Managing Finance in a Digital World", "Operational level"),
    Paper("P1", "P1 Management Accounting", "Operational level"),
    Paper("F1", "F1 Financial Reporting", "Operational level"),
    Paper("E2", "E2 Project and Relationship Management", "Management level"),
    Paper("P2", "P2 Advanced Management Accounting", "Management level"),
    Paper("F2", "F2 Advanced Financial Reporting", "Management level"),
    Paper("E3", "E3 Strategic Management", "Strategic level"),
    Paper("P3", "P3 Risk and Control Strategy", "Strategic level"),
    Paper("F3", "F3 Financial Strategy", "Strategic level"),
    Paper("SCS", "Strategic Case Study", "Strategic level case study"),
]

_ALEVEL_PAPERS = [
    Paper("Mathematics", "Mathematics", "A-Level Mathematics"),
    Paper("Further Maths", "Further Mathematics", "A-Level Further Mathematics"),
    Paper("Physics", "Physics", "A-Level Physics"),
    Paper("Chemistry", "Chemistry", "A-Level Chemistry"),
    Paper("Biology", "Biology", "A-Level Biology"),
    Paper("Economics", "Economics", "A-Level Economics"),
    Paper("English Literature", "English Literature", "A-Level English Literature"),
    Paper("History", "History", "A-Level History"),
    Paper("Psychology", "Psychology", "A-Level Psychology"),
    Paper("Computer Science", "Computer Science", "A-Level Computer Science"),
    Paper("Other", "Other subject", "Enter your own subject"),
]

_GCSE_PAPERS = [
    Paper("Mathematics", "Mathematics", "GCSE Mathematics"),
    Paper("English Language", "English Language", "GCSE English Language"),
    Paper("English Literature", "English Literature", "GCSE English Literature"),
    Paper("Sciences", "Sciences (Combined/Triple)", "GCSE Sciences"),
    Paper("Physics", "Physics", "GCSE Physics"),
    Paper("Chemistry", "Chemistry", "GCSE Chemistry"),
    Paper("Biology", "Biology", "GCSE Biology"),
    Paper("History", "History", "GCSE History"),
    Paper("Geography", "Geography", "GCSE Geography"),
    Paper("Computer Science", "Computer Science", "GCSE Computer Science"),
    Paper("Other", "Other subject", "Enter your own subject"),
]

_CAMBRIDGE_PAPERS = [
    Paper("Mathematics", "Mathematics (STEP/MAT)", "Cambridge admissions mathematics"),
    Paper("Natural Sciences", "Natural Sciences", "Cambridge NatSci admissions"),
    Paper("Engineering", "Engineering", "Cambridge Engineering admissions"),
    Paper("Economics", "Economics", "Cambridge Economics admissions"),
    Paper("Law", "Law (LNAT)", "Cambridge Law admissions"),
    Paper("Medicine", "Medicine (BMAT)", "Cambridge Medicine admissions"),
    Paper("Other", "Other course", "Enter your own course"),
]

_OXFORD_PAPERS = [
    Paper("Mathematics", "Mathematics (MAT)", "Oxford admissions mathematics"),
    Paper("Physics", "Physics (PAT)", "Oxford admissions physics"),
    Paper("Engineering", "Engineering (PAT)", "Oxford Engineering admissions"),
    Paper("Economics", "Economics & Management", "Oxford Economics admissions"),
    Paper("Law", "Law (LNAT)", "Oxford Law admissions"),
    Paper("Medicine", "Medicine (BMAT)", "Oxford Medicine admissions"),
    Paper("Other", "Other course", "Enter your own course"),
]


_CATALOGUE: dict[str, ExaminationCategory] = {
    "IFoA": ExaminationCategory(
        code="IFoA",
        name="IFoA",
        description="Institute and Faculty of Actuaries professional examinations.",
        papers=_IFOA_PAPERS,
        sittings=["April 2027", "September 2027", "April 2028", "September 2028"],
        targets=["Pass", "Strong Pass"],
    ),
    "CFA": ExaminationCategory(
        code="CFA",
        name="CFA",
        description="Chartered Financial Analyst programme — global investment professionals.",
        papers=_CFA_LEVELS,
        sittings=["February 2027", "May 2027", "August 2027", "November 2027"],
        targets=["Pass", "Strong Pass", "Top 10%"],
    ),
    "ACCA": ExaminationCategory(
        code="ACCA",
        name="ACCA",
        description="Association of Chartered Certified Accountants professional qualification.",
        papers=_ACCA_PAPERS,
        sittings=["March 2027", "June 2027", "September 2027", "December 2027"],
        targets=["Pass", "Strong Pass", "Distinction"],
    ),
    "CIMA": ExaminationCategory(
        code="CIMA",
        name="CIMA",
        description="Chartered Institute of Management Accountants professional qualification.",
        papers=_CIMA_PAPERS,
        sittings=["February 2027", "May 2027", "August 2027", "November 2027"],
        targets=["Pass", "Strong Pass", "Distinction"],
    ),
    "University": ExaminationCategory(
        code="University",
        name="University",
        description="University or college examinations and coursework.",
        papers=[],
        sittings=["Semester 1 2027", "Semester 2 2027", "Summer 2027", "January 2028"],
        targets=["First Class", "Upper Second", "Lower Second", "Pass"],
        free_text_subject=True,
    ),
    "A-Level": ExaminationCategory(
        code="A-Level",
        name="A-Level",
        description="Advanced Level qualifications — UK pre-university examinations.",
        papers=_ALEVEL_PAPERS,
        sittings=["June 2027", "November 2027", "June 2028"],
        targets=["A*", "A", "B", "C", "D", "E"],
    ),
    "GCSE": ExaminationCategory(
        code="GCSE",
        name="GCSE",
        description="General Certificate of Secondary Education — UK qualifications.",
        papers=_GCSE_PAPERS,
        sittings=["June 2027", "November 2027", "June 2028"],
        targets=["9", "8", "7", "6", "5", "4", "3"],
    ),
    "Cambridge": ExaminationCategory(
        code="Cambridge",
        name="Cambridge",
        description="University of Cambridge admissions tests and interviews.",
        papers=_CAMBRIDGE_PAPERS,
        sittings=["November 2026", "June 2027"],
        targets=["Offer", "Strong Offer"],
    ),
    "Oxford": ExaminationCategory(
        code="Oxford",
        name="Oxford",
        description="University of Oxford admissions tests and interviews.",
        papers=_OXFORD_PAPERS,
        sittings=["November 2026", "June 2027"],
        targets=["Offer", "Strong Offer"],
    ),
    "Other": ExaminationCategory(
        code="Other",
        name="Other",
        description="Any other examination not listed above.",
        papers=[],
        sittings=["Custom"],
        targets=["Pass", "Strong Pass", "Distinction"],
        free_text_subject=True,
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────


def get_categories() -> list[ExaminationCategory]:
    """Return all examination categories in display order."""
    return list(_CATALOGUE.values())


def get_category(code: str) -> ExaminationCategory | None:
    """Return a single examination category by its code, or None."""
    return _CATALOGUE.get(code)


def get_category_choices() -> list[tuple[str, str]]:
    """Return (code, name) tuples suitable for WTForms RadioField choices."""
    return [(c.code, c.name) for c in _CATALOGUE.values()]


def get_paper_choices(category_code: str) -> list[tuple[str, str]]:
    """Return (code, name) tuples for the papers of a given category.

    Returns an empty list when the category uses free-text subjects.
    """
    category = get_category(category_code)
    if not category:
        return []
    return [(p.code, p.name) for p in category.papers]


def get_sitting_choices(category_code: str) -> list[tuple[str, str]]:
    """Return (value, label) tuples for sittings of a given category."""
    category = get_category(category_code)
    if not category or not category.sittings:
        return [("Custom", "Custom")]
    return [(s, s) for s in category.sittings]


def get_target_choices(category_code: str) -> list[tuple[str, str]]:
    """Return (value, label) tuples for target results of a given category."""
    category = get_category(category_code)
    if not category or not category.targets:
        return [("Pass", "Pass"), ("Strong Pass", "Strong Pass")]
    return [(t, t) for t in category.targets]


def is_free_text_subject(category_code: str) -> bool:
    """Return True when the category collects a free-text subject."""
    category = get_category(category_code)
    return bool(category and category.free_text_subject)


def format_exam_name(category_code: str, paper_or_subject: str) -> str:
    """Combine a category and paper/subject into a single exam name string.

    This keeps the existing ``StudyPlan.exam_name`` column compatible without
    schema changes.  Examples:
        - ("IFoA", "CS1") -> "IFoA CS1"
        - ("University", "Actuarial Science") -> "University: Actuarial Science"
    """
    category = get_category(category_code)
    if category and category.free_text_subject:
        return f"{category_code}: {paper_or_subject}"
    return f"{category_code} {paper_or_subject}".strip()


def parse_exam_name(exam_name: str) -> tuple[str, str]:
    """Split a stored exam name back into (category_code, paper_or_subject).

    Best-effort inverse of :func:`format_exam_name`.  Returns ("", "") when the
    format is unrecognised.
    """
    if not exam_name:
        return "", ""
    for code in _CATALOGUE:
        if exam_name.startswith(code + " "):
            return code, exam_name[len(code) + 1:]
        if exam_name.startswith(code + ": "):
            return code, exam_name[len(code) + 2:]
    return "", exam_name


def get_paper_description(category_code: str, paper_code: str) -> str:
    """Return the human-readable description for a paper, or empty string."""
    category = get_category(category_code)
    if not category:
        return ""
    for paper in category.papers:
        if paper.code == paper_code:
            return paper.description
    return ""
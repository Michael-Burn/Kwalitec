"""RR-001A Authentic Supported Syllabus regression tests.

Founder observation (FC-001): selecting CS1 surfaced generic placeholder
titles such as "Topic A1" / "Topic B1" instead of the official IFoA syllabus.

Root cause: non-official placeholder curriculum fixtures had been dropped into
the production syllabus directory (``app/curriculum/data/ifoa/...``). Because
study-plan / wizard version discovery selects ``max(versions)`` and
``import_curricula`` imports every discovered version, a student selecting CS1
resolved to a placeholder "future" version.

These tests fail-closed against re-pollution of the Supported syllabus: only
the three Version 1 papers (CS1, CM1, CB2) may be discoverable, every
Supported paper must expose recognisable official titles, and no student-facing
syllabus title may be a generic placeholder.

Scope guard: this is product-trust data hygiene only. It asserts nothing about
ordering, weightings, relationships, or learning logic.
"""

from __future__ import annotations

from app.services.curriculum_engine_service import CurriculumEngineService
from app.services.subject_support_service import SubjectSupportService

# Generic placeholder fragments that must never reach a student as a syllabus
# title. These are the exact shapes seen in the removed test fixtures.
_PLACEHOLDER_TITLE_FRAGMENTS = (
    "topic a1",
    "topic b1",
    "section a",
    "section b",
    "test topic",
    "test exam",
    "multi-section exam",
    "actuarial statistics v2",
    "section alpha",
    "section beta",
    "alpha topic",
    "beta topic",
)

# The only examinations that may be Supported in Version 1.
_EXPECTED_SUPPORTED = {("IFOA", "CS1"), ("IFOA", "CM1"), ("IFOA", "CB2")}


def _latest_version(org: str, paper: str) -> str:
    engine = CurriculumEngineService()
    versions = engine.list_supported_versions(org, paper)
    assert versions, f"No syllabus version discovered for {org} {paper}"
    return max(versions)


def _all_titles(org: str, paper: str) -> list[str]:
    """Every student-facing section and topic title for the latest version."""
    engine = CurriculumEngineService()
    curriculum = engine.load_auto(
        org.lower(), paper.lower(), _latest_version(org, paper)
    )
    titles: list[str] = []
    for section in curriculum.sections:
        titles.append(section.title)
        for topic in section.topics:
            titles.append(topic.title)
    return titles


class TestSupportedSyllabusIsClean:
    def test_only_version1_papers_are_supported(self):
        supported = SubjectSupportService.list_supported_examinations()
        found = {(o.upper(), p.upper()) for o, p in supported}
        assert found == _EXPECTED_SUPPORTED, (
            "Supported syllabus set drifted from CS1/CM1/CB2 — a placeholder or "
            f"non-official curriculum may have been added. Found: {sorted(found)}"
        )

    def test_no_phantom_exam_appears(self):
        supported = SubjectSupportService.list_supported_examinations()
        papers = {p.upper() for _o, p in supported}
        assert "CS9" not in papers, "Phantom test exam CS9 leaked into Supported list"

    def test_cs1_resolves_to_official_version(self):
        assert _latest_version("IFoA", "CS1") == "2026"


class TestSupportedTitlesAreOfficial:
    def test_no_placeholder_titles_in_supported_papers(self):
        for org, paper in (("IFoA", "CS1"), ("IFoA", "CM1"), ("IFoA", "CB2")):
            for title in _all_titles(org, paper):
                lowered = title.lower()
                for fragment in _PLACEHOLDER_TITLE_FRAGMENTS:
                    assert fragment not in lowered, (
                        f"{org} {paper} exposes placeholder title '{title}' "
                        f"(matched '{fragment}')"
                    )

    def test_cs1_shows_recognisable_official_topics(self):
        titles = " ".join(_all_titles("IFoA", "CS1")).lower()
        # Signature CS1 syllabus content a student would immediately recognise.
        assert "data analysis" in titles
        assert "bayesian statistics" in titles
        assert "regression" in titles

    def test_cm1_shows_recognisable_official_topics(self):
        titles = " ".join(_all_titles("IFoA", "CM1")).lower()
        assert "interest rate" in titles

    def test_cb2_shows_recognisable_official_topics(self):
        titles = " ".join(_all_titles("IFoA", "CB2")).lower()
        assert "economic" in titles

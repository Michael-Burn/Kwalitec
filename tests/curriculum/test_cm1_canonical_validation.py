"""CM1 and CB2 syllabi are no longer shipped.

Preserves a fail-closed check so the removed bundles are not reintroduced
under ``app/curriculum/data/ifoa/`` without an intentional product decision.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.curriculum.exceptions import CurriculumError
from app.curriculum.loader import discover_curricula
from app.curriculum.repository import CurriculumRepository

_DATA_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "curriculum" / "data" / "ifoa"
)


class TestRemovedSyllabiStayGone:
    def test_cm1_and_cb2_json_absent(self) -> None:
        assert not (_DATA_ROOT / "cm1").exists()
        assert not (_DATA_ROOT / "cb2").exists()
        assert (_DATA_ROOT / "cs1" / "2026.json").is_file()

    def test_discovery_excludes_cm1_and_cb2(self) -> None:
        papers = {
            (org.upper(), paper.upper()) for org, paper, _v in discover_curricula()
        }
        assert ("IFOA", "CS1") in papers
        assert ("IFOA", "CM1") not in papers
        assert ("IFOA", "CB2") not in papers

    def test_load_auto_rejects_cm1_and_cb2(self) -> None:
        repo = CurriculumRepository()
        for paper in ("cm1", "cb2"):
            with pytest.raises(CurriculumError):
                repo.load_auto("ifoa", paper, "2026")

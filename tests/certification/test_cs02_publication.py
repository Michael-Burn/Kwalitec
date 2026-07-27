"""CS-02: Curriculum publication certification."""

from __future__ import annotations

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from tests.certification.pi001d_helpers import STANDARD_STRUCTURE


class TestCurriculumPublication:
    """Certify published package integrity and authority safety."""

    def _publish(self, code: str, version_label: str = "2027.1") -> None:
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject(code, title=f"Pub {code}", actor_id="f")
        ver = foundation.create_version(code, version_label, actor_id="f")
        for kind in ("cmp", "syllabus"):
            foundation.upload_document(
                ver.version_id,
                kind=kind,
                reference=f"ref://{kind}/{code.lower()}",
                structure=STANDARD_STRUCTURE,
                actor_id="f",
            )
        foundation.process_curriculum(ver.version_id, actor_id="f")
        foundation.validate_curriculum(ver.version_id, actor_id="f")
        foundation.founder_review(ver.version_id, actor_id="f")
        foundation.publish_curriculum(ver.version_id, actor_id="f")

    def test_cs02_1_package_contains_complete_structure(self, ctx):
        self._publish("PUB1")
        authority = PublishedCurriculumAuthority()
        pkg = authority.get_active("PUB1")
        structure = pkg.package.get("structure", {})
        assert len(structure.get("sections", [])) >= 1
        assert len(structure.get("topics", [])) >= 1
        assert len(structure.get("objectives", [])) >= 1

    def test_cs02_2_authority_only_returns_published(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("DRF1", title="Draft Only", actor_id="f")
        ver = foundation.create_version("DRF1", "2027.1", actor_id="f")
        for kind in ("cmp", "syllabus"):
            foundation.upload_document(
                ver.version_id,
                kind=kind,
                reference=f"ref://{kind}/drf1",
                structure=STANDARD_STRUCTURE,
                actor_id="f",
            )
        foundation.process_curriculum(ver.version_id, actor_id="f")

        authority = PublishedCurriculumAuthority()
        assert authority.get_active("DRF1") is None

    def test_cs02_3_version_deactivation(self, ctx):
        foundation = CurriculumStudioFoundationService()
        authority = PublishedCurriculumAuthority()

        foundation.create_subject("DEA1", title="Deactivation", actor_id="f")
        for label in ("2027.1", "2027.2"):
            ver = foundation.create_version("DEA1", label, actor_id="f")
            for kind in ("cmp", "syllabus"):
                foundation.upload_document(
                    ver.version_id,
                    kind=kind,
                    reference=f"ref://{kind}/dea1/{label}",
                    structure=STANDARD_STRUCTURE,
                    actor_id="f",
                )
            foundation.process_curriculum(ver.version_id, actor_id="f")
            foundation.validate_curriculum(ver.version_id, actor_id="f")
            foundation.founder_review(ver.version_id, actor_id="f")
            foundation.publish_curriculum(ver.version_id, actor_id="f")

        active = authority.get_active("DEA1")
        assert active is not None
        assert active.version_label == "2027.2"

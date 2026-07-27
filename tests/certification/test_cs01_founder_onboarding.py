"""CS-01: Founder onboarding certification."""

from __future__ import annotations

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from tests.certification.pi001d_helpers import STANDARD_STRUCTURE


class TestFounderOnboarding:
    """Certify the complete founder onboarding lifecycle."""

    def test_cs01_1_create_subject(self, ctx):
        foundation = CurriculumStudioFoundationService()
        subject = foundation.create_subject("FO01", title="Founder Test", actor_id="f")
        assert subject.subject_code == "FO01"
        assert subject.title == "Founder Test"

    def test_cs01_2_upload_documents(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("FO02", title="Doc Upload", actor_id="f")
        version = foundation.create_version("FO02", "2027.1", actor_id="f")

        doc1 = foundation.upload_document(
            version.version_id,
            kind="cmp",
            reference="ref://cmp/fo02",
            structure=STANDARD_STRUCTURE,
            actor_id="f",
        )
        doc2 = foundation.upload_document(
            version.version_id,
            kind="syllabus",
            reference="ref://syllabus/fo02",
            structure=STANDARD_STRUCTURE,
            actor_id="f",
        )
        assert doc1 is not None
        assert doc2 is not None

    def test_cs01_3_process_curriculum(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("FO03", title="Process", actor_id="f")
        version = foundation.create_version("FO03", "2027.1", actor_id="f")
        foundation.upload_document(
            version.version_id,
            kind="cmp",
            reference="ref://cmp/fo03",
            structure=STANDARD_STRUCTURE,
            actor_id="f",
        )
        foundation.upload_document(
            version.version_id,
            kind="syllabus",
            reference="ref://syllabus/fo03",
            structure=STANDARD_STRUCTURE,
            actor_id="f",
        )
        result = foundation.process_curriculum(version.version_id, actor_id="f")
        assert result is not None

    def test_cs01_4_to_6_full_lifecycle_to_publish(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("FO04", title="Full Lifecycle", actor_id="f")
        version = foundation.create_version("FO04", "2027.1", actor_id="f")
        for kind in ("cmp", "syllabus"):
            foundation.upload_document(
                version.version_id,
                kind=kind,
                reference=f"ref://{kind}/fo04",
                structure=STANDARD_STRUCTURE,
                actor_id="f",
            )
        foundation.process_curriculum(version.version_id, actor_id="f")
        foundation.validate_curriculum(version.version_id, actor_id="f")
        foundation.founder_review(version.version_id, actor_id="f")
        foundation.publish_curriculum(version.version_id, actor_id="f")

        authority = PublishedCurriculumAuthority()
        package = authority.get_active("FO04")
        assert package is not None
        assert package.package is not None

    def test_cs01_7_subject_agnostic(self, ctx):
        """Two different subjects publish independently."""
        foundation = CurriculumStudioFoundationService()
        authority = PublishedCurriculumAuthority()

        for code in ("AGN1", "AGN2"):
            foundation.create_subject(code, title=f"Agnostic {code}", actor_id="f")
            ver = foundation.create_version(code, "2027.1", actor_id="f")
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

        assert authority.get_active("AGN1") is not None
        assert authority.get_active("AGN2") is not None
        assert (
            authority.get_active("AGN1").package
            != authority.get_active("AGN2").package
        )

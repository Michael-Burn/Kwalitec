"""EE-001 — Student Subject Catalogue projection tests."""

from __future__ import annotations

import os
from datetime import datetime

from app.application.curriculum_studio_foundation.dto import PublishedPackageSnapshot
from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
    PublishedSubjectDiscoveryService,
)
from app.application.platform_integration.subject_catalogue import (
    CatalogueAvailability,
    SubjectCatalogueService,
    _coerce_release,
    _format_release,
)
from tests.application.platform_integration.helpers import (
    bridge_flags,
    publish_subject,
)


class TestFormatReleaseCoercion:
    """Projection must accept authority strings and ORM datetimes."""

    def test_iso_string_formats(self):
        assert _format_release("2026-07-29T10:15:30") == "29 Jul 2026"

    def test_iso_string_with_z_formats(self):
        assert _format_release("2026-07-29T10:15:30Z") == "29 Jul 2026"

    def test_datetime_formats(self):
        assert _format_release(datetime(2026, 1, 5, 12, 0, 0)) == "05 Jan 2026"

    def test_none_and_blank_are_empty(self):
        assert _format_release(None) == ""
        assert _format_release("") == ""
        assert _format_release("   ") == ""

    def test_unparseable_string_does_not_raise(self):
        assert _format_release("not-a-date") == ""

    def test_coerce_returns_datetime_for_iso_string(self):
        coerced = _coerce_release("2026-07-29T10:15:30")
        assert isinstance(coerced, datetime)
        assert coerced.year == 2026
        assert coerced.month == 7
        assert coerced.day == 29


class TestPublishedSubjectDiscoveryProjection:
    def test_published_ready_subject_appears_with_metadata(self, ctx):
        publish_subject("CS1V", title="CS1 Validation", version_label="2026.1")
        discovery = PublishedSubjectDiscoveryService(flags=bridge_flags())
        service = SubjectCatalogueService(discovery=discovery)
        os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
        try:
            entries = service.list_entries()
        finally:
            os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)

        entry = next(e for e in entries if e.paper == "CS1V")
        assert entry.availability is CatalogueAvailability.READY
        assert entry.availability_label == "Ready"
        assert entry.version == "2026.1"
        assert entry.release_date is not None
        assert isinstance(entry.release_date, datetime)
        assert entry.release_date_label
        assert entry.subject_key == f"{PUBLISHED_CATEGORY_CODE}:CS1V"
        assert entry.name == "CS1 Validation"

    def test_authority_string_published_at_does_not_500(self, ctx, monkeypatch):
        """Reproduce EV-001 failure mode: authority supplies ISO string."""

        class _Authority:
            def list_published(self, subject_code=None):
                return (
                    PublishedPackageSnapshot(
                        package_id=1,
                        subject_code="CS1V",
                        version_id=1,
                        version_label="2026.1",
                        is_active=True,
                        published_by="founder",
                        published_at="2026-07-29T14:22:01.123456",
                        package={},
                    ),
                )

        from app.services.subject_support_service import (
            SubjectSupportInfo,
            SupportStatus,
        )

        monkeypatch.setattr(
            "app.application.platform_integration.subject_catalogue."
            "SubjectSupportService.resolve",
            lambda org, paper, **kwargs: SubjectSupportInfo(
                status=SupportStatus.SUPPORTED,
                organisation=org,
                paper=paper,
                label="Ready",
                title="CS1V is Ready",
                explanation="Ready",
                allows_plan_creation=True,
                alternatives=(),
            ),
        )

        discovery = PublishedSubjectDiscoveryService(
            authority=_Authority(),
            flags=bridge_flags(),
        )
        service = SubjectCatalogueService(
            discovery=discovery,
            authority=_Authority(),
        )
        entry = service._from_published("CS1V")
        assert entry is not None
        assert entry.availability_label == "Ready"
        assert entry.version == "2026.1"
        assert entry.release_date_label == "29 Jul 2026"
        assert isinstance(entry.release_date, datetime)

    def test_choose_exam_renders_published_subject(self, logged_in_client, ctx):
        publish_subject("CS1V", title="CS1 Validation", version_label="2026.1")
        os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
        try:
            response = logged_in_client.get("/study-plan/wizard/1")
        finally:
            os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)
        assert response.status_code == 200
        body = response.data.decode("utf-8")
        assert "CS1V" in body
        assert "Ready" in body
        assert "2026.1" in body


class TestCatalogueRegressionHidden:
    """Non-Ready lifecycle states must not appear as Ready catalogue cards."""

    def test_draft_subject_hidden(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("DRFT", title="Draft Only", actor_id="founder")
        foundation.create_version("DRFT", "2026.1", actor_id="founder")
        discovery = PublishedSubjectDiscoveryService(flags=bridge_flags())
        service = SubjectCatalogueService(discovery=discovery)
        os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
        try:
            keys = {e.subject_key for e in service.list_entries()}
        finally:
            os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)
        assert f"{PUBLISHED_CATEGORY_CODE}:DRFT" not in keys

    def test_incomplete_subject_hidden(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("INC1", title="Incomplete", actor_id="founder")
        version = foundation.create_version("INC1", "2026.1", actor_id="founder")
        # Documents uploaded but never processed / validated / published.
        foundation.upload_document(
            version.version_id,
            kind="cmp",
            reference="ref://cmp/inc1",
            structure={"entries": []},
            actor_id="founder",
        )
        discovery = PublishedSubjectDiscoveryService(flags=bridge_flags())
        service = SubjectCatalogueService(discovery=discovery)
        os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
        try:
            keys = {e.subject_key for e in service.list_entries()}
        finally:
            os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)
        assert f"{PUBLISHED_CATEGORY_CODE}:INC1" not in keys

    def test_validated_but_unpublished_hidden(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("VAL1", title="Validated Only", actor_id="founder")
        version = foundation.create_version("VAL1", "2026.1", actor_id="founder")
        from tests.application.platform_integration.helpers import STANDARD_STRUCTURE

        foundation.upload_document(
            version.version_id,
            kind="cmp",
            reference="ref://cmp/val1",
            structure=STANDARD_STRUCTURE,
            actor_id="founder",
        )
        foundation.upload_document(
            version.version_id,
            kind="syllabus",
            reference="ref://syllabus/val1",
            structure=STANDARD_STRUCTURE,
            actor_id="founder",
        )
        foundation.process_curriculum(version.version_id, actor_id="founder")
        foundation.validate_curriculum(version.version_id, actor_id="founder")
        discovery = PublishedSubjectDiscoveryService(flags=bridge_flags())
        service = SubjectCatalogueService(discovery=discovery)
        os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
        try:
            keys = {e.subject_key for e in service.list_entries()}
        finally:
            os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)
        assert f"{PUBLISHED_CATEGORY_CODE}:VAL1" not in keys

    def test_validation_failure_hidden(self, ctx):
        foundation = CurriculumStudioFoundationService()
        foundation.create_subject("FAIL1", title="Fail Validate", actor_id="founder")
        version = foundation.create_version("FAIL1", "2026.1", actor_id="founder")
        # Empty structures — process may succeed or fail; never publish.
        foundation.upload_document(
            version.version_id,
            kind="cmp",
            reference="ref://cmp/fail1",
            structure={"entries": []},
            actor_id="founder",
        )
        foundation.upload_document(
            version.version_id,
            kind="syllabus",
            reference="ref://syllabus/fail1",
            structure={"entries": []},
            actor_id="founder",
        )
        try:
            foundation.process_curriculum(version.version_id, actor_id="founder")
            foundation.validate_curriculum(version.version_id, actor_id="founder")
        except Exception:
            pass
        discovery = PublishedSubjectDiscoveryService(flags=bridge_flags())
        service = SubjectCatalogueService(discovery=discovery)
        os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
        try:
            keys = {e.subject_key for e in service.list_entries()}
        finally:
            os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)
        assert f"{PUBLISHED_CATEGORY_CODE}:FAIL1" not in keys

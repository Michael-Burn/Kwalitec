"""PX-002 Product Experience Implementation regression tests."""

from __future__ import annotations

from app.application.platform_integration.subject_catalogue import (
    COMING_SOON_MESSAGE,
    CatalogueAvailability,
    SubjectCatalogueService,
)
from app.founder.dashboard.nav import COMMAND_CENTRE_NAV
from app.presentation.product_language import FOUNDER_PRIMARY_NAV_LABELS
from app.services.subject_support_service import SubjectSupportService


class TestSubjectCatalogue:
    def test_ready_subjects_are_selectable(self):
        entries = SubjectCatalogueService().list_entries()
        ready = [e for e in entries if e.availability is CatalogueAvailability.READY]
        assert ready
        assert all(e.selectable for e in ready)
        assert any(e.paper == "CS1" for e in ready)

    def test_coming_soon_not_selectable(self):
        entries = SubjectCatalogueService().list_entries(include_coming_soon=True)
        coming = [
            e for e in entries if e.availability is CatalogueAvailability.COMING_SOON
        ]
        assert coming
        assert all(not e.selectable for e in coming)
        assert all(COMING_SOON_MESSAGE[:40] in e.preparation_message for e in coming)

    def test_catalogue_omits_unavailable(self):
        entries = SubjectCatalogueService().list_entries()
        keys = {e.subject_key for e in entries}
        assert "CFA:Level I" not in keys

    def test_ready_label_from_support_service(self):
        info = SubjectSupportService.resolve("IFoA", "CS1")
        assert info.label == "Ready"


class TestFounderNavigation:
    def test_primary_nav_is_curriculum_authority(self):
        labels = [item.label for item in COMMAND_CENTRE_NAV]
        assert labels == list(FOUNDER_PRIMARY_NAV_LABELS)
        assert "Content" not in labels
        assert labels.index("Subjects") < labels.index("Curriculum Studio")


class TestStudentSurfaces:
    def test_choose_exam_has_no_upload_language(self, logged_in_client):
        response = logged_in_client.get("/study-plan/wizard/1")
        assert response.status_code == 200
        body = response.data.decode("utf-8").lower()
        for forbidden in (
            "upload cmp",
            "upload syllabus",
            "curriculum studio",
            "knowledge graph",
            "published curriculum",
            "extraction",
        ):
            assert forbidden not in body

    def test_founder_hubs_render(self, client, ctx, app):
        from tests.presentation.curriculum_studio.helpers import (
            login_founder,
            wire_studio,
        )

        wire_studio(app)
        login_founder(client, app)
        for path in (
            "/console/studio/subjects",
            "/console/studio/review-queue",
            "/console/studio/publishing",
            "/console/studio/versions",
            "/console/studio/quality",
        ):
            response = client.get(path)
            assert response.status_code == 200, path
            assert b"Curriculum Authority" in response.data

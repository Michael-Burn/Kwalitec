"""V1SP-001D Founder Vision Journal tests."""

from __future__ import annotations

import json

from app.extensions import db
from app.models.user import User
from app.models.vision_journal import VisionEntry, VisionEntryPromotion
from app.services.vision_journal_service import (
    SORT_HIGHEST_VALUE,
    VisionJournalService,
    VisionSearchFilters,
)


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def _login_founder(client, app) -> User:
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    founder = _make_user("founder@kwalitec.example")
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    return founder


def _entry_payload(**overrides) -> dict:
    data = {
        "title": "Learning Confidence Engine",
        "description": "Estimate learner confidence from evidence.",
        "reason": "Students need trustable next-step signals.",
        "potential_value": "high",
        "expected_impact": "Clearer study decisions.",
        "target_version": "version_2",
        "category": "Educational Intelligence",
        "status": "vision",
        "tags": "AI, Twin, Learning Objects",
        "future_milestone": "",
        "submit": "Save",
    }
    data.update(overrides)
    return data


class TestVisionJournalService:
    def test_create_edit_archive_and_status_history(self, ctx, app) -> None:
        founder = _make_user("founder@kwalitec.example")
        entry = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Revision Workspace",
            description="Dedicated revision surface.",
            reason="Lifecycle completion needs a home.",
            potential_value="critical",
            expected_impact="Stronger exam readiness.",
            target_version="version_1_x",
            category="Revision",
            tags=["Revision", "Dashboard"],
        )
        assert entry.status == "vision"
        assert len(entry.status_transitions) == 1
        assert entry.tags == ["Revision", "Dashboard"]

        updated = VisionJournalService.update_entry(
            entry.id,
            changed_by_user_id=founder.id,
            title=entry.title,
            description=entry.description,
            reason=entry.reason,
            potential_value="critical",
            expected_impact=entry.expected_impact,
            target_version="version_1_x",
            category="Revision",
            tags=["Revision"],
            status="validated",
            status_note="Validated in Internal Alpha",
        )
        assert updated is not None
        assert updated.status == "validated"
        assert len(updated.status_transitions) == 2
        assert updated.status_transitions[-1].from_status == "vision"

        archived = VisionJournalService.archive_entry(
            entry.id, changed_by_user_id=founder.id
        )
        assert archived is not None
        assert archived.status == "archived"
        assert archived.deleted_at is None

    def test_search_filters_sorting_and_tags(self, ctx, app) -> None:
        founder = _make_user("founder@kwalitec.example")
        VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Alpha Twin",
            description="Digital twin sketch",
            reason="Long-term intelligence",
            potential_value="exploratory",
            expected_impact="Personalisation",
            target_version="future",
            category="Student Digital Twin",
            tags=["Twin", "AI"],
            status="vision",
        )
        VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Performance Budget",
            description="Keep dashboard fast",
            reason="Trust requires speed",
            potential_value="critical",
            expected_impact="Lower friction",
            target_version="version_1_x",
            category="Performance",
            tags=["Performance", "Infrastructure"],
            status="planned",
        )

        tagged = VisionJournalService.search(
            VisionSearchFilters(tag="Twin")
        )
        assert len(tagged) == 1
        assert tagged[0].title == "Alpha Twin"

        filtered = VisionJournalService.search(
            VisionSearchFilters(
                category="Performance",
                status="planned",
                target_version="version_1_x",
            )
        )
        assert len(filtered) == 1

        by_value = VisionJournalService.search(sort=SORT_HIGHEST_VALUE)
        assert by_value[0].potential_value == "critical"

        queried = VisionJournalService.search(
            VisionSearchFilters(query="dashboard")
        )
        assert len(queried) == 1
        assert "Performance" in queried[0].title

    def test_relationships_promotion_and_export(self, ctx, app) -> None:
        founder = _make_user("founder@kwalitec.example")
        a = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Learning Object Model",
            description="Canonical learning objects",
            reason="Shared curriculum atoms",
            potential_value="high",
            expected_impact="Reusable content",
            target_version="version_2",
            category="Educational Intelligence",
            tags=["Learning Objects"],
        )
        b = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Learning Confidence Engine",
            description="Confidence from evidence",
            reason="Explainable next steps",
            potential_value="high",
            expected_impact="Better missions",
            target_version="version_2",
            category="Educational Intelligence",
            tags=["AI"],
        )
        rel = VisionJournalService.add_relation(
            from_entry_id=b.id,
            to_entry_id=a.id,
            relation_type="depends_on",
            created_by_user_id=founder.id,
        )
        assert rel is not None
        related = VisionJournalService.list_related(b.id)
        assert len(related) == 1

        promo = VisionJournalService.promote_to_development(
            b.id,
            promoted_by_user_id=founder.id,
            notes="Ready for architecture brief",
        )
        assert promo is not None
        assert promo.placeholder_ref.startswith("ARCH-PLACEHOLDER-")
        refreshed = VisionJournalService.get_entry(b.id)
        assert refreshed is not None
        assert refreshed.status == "in_development"
        assert VisionEntryPromotion.query.count() == 1

        md = VisionJournalService.export_markdown()
        assert "# Kwalitec Vision Journal" in md
        assert "Learning Confidence Engine" in md
        payload = json.loads(VisionJournalService.export_json())
        assert len(payload) == 2
        csv_body = VisionJournalService.export_csv()
        assert "title" in csv_body.splitlines()[0]
        assert "Learning Object Model" in csv_body

    def test_soft_delete_hides_from_search(self, ctx, app) -> None:
        founder = _make_user("founder@kwalitec.example")
        entry = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Temporary Idea",
            description="Will be removed",
            reason="Test",
            potential_value="low",
            expected_impact="None",
            target_version="unknown",
            category="Other",
        )
        VisionJournalService.soft_delete_entry(
            entry.id, changed_by_user_id=founder.id
        )
        assert VisionJournalService.get_entry(entry.id) is None
        assert VisionJournalService.search() == []
        hidden = VisionJournalService.get_entry(entry.id, include_deleted=True)
        assert hidden is not None
        assert hidden.is_deleted
        assert hidden.status == "archived"

    def test_overview_widgets(self, ctx, app) -> None:
        founder = _make_user("founder@kwalitec.example")
        VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Awaiting Idea",
            description="Needs validation",
            reason="Research",
            potential_value="medium",
            expected_impact="Clarity",
            target_version="version_2",
            category="Research",
            status="research",
        )
        planned = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Planned Idea",
            description="Next release",
            reason="Roadmap",
            potential_value="high",
            expected_impact="Delivery",
            target_version="version_1_x",
            category="Operations",
            status="planned",
        )
        VisionJournalService.promote_to_development(
            planned.id, promoted_by_user_id=founder.id
        )
        widgets = VisionJournalService.overview_widgets()
        assert any(e.title == "Awaiting Idea" for e in widgets.awaiting_validation)
        assert widgets.recent_entries
        assert widgets.recently_promoted


class TestVisionJournalRoutes:
    def test_founder_only_access(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        student = _make_user("student@kwalitec.example")
        client.post(
            "/auth/login",
            data={"email": student.email, "password": "password123"},
            follow_redirects=True,
        )
        for path in (
            "/founder/vision",
            "/founder/vision/new",
            "/founder/vision/timeline",
            "/founder/vision/export/json",
        ):
            assert client.get(path).status_code == 403

    def test_create_edit_archive_via_http(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        create = client.post(
            "/founder/vision/new",
            data=_entry_payload(),
            follow_redirects=True,
        )
        assert create.status_code == 200
        assert b"Learning Confidence Engine" in create.data
        entry = VisionEntry.query.filter_by(author_user_id=founder.id).one()

        edit = client.post(
            f"/founder/vision/{entry.id}/edit",
            data=_entry_payload(
                title="Learning Confidence Engine v2",
                status="validated",
            ),
            follow_redirects=True,
        )
        assert edit.status_code == 200
        assert b"Learning Confidence Engine v2" in edit.data
        assert VisionJournalService.get_entry(entry.id).status == "validated"

        detail = client.get(f"/founder/vision/{entry.id}")
        assert detail.status_code == 200
        assert b"Promote to Development" in detail.data
        assert b"Timeline" in detail.data

        archive = client.post(
            f"/founder/vision/{entry.id}",
            data={"archive-submit": "Archive"},
            follow_redirects=True,
        )
        assert archive.status_code == 200
        assert VisionJournalService.get_entry(entry.id).status == "archived"

    def test_search_filters_export_and_nav(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Security Hardening",
            description="CSP and secrets",
            reason="Trust",
            potential_value="high",
            expected_impact="Safer Founder ops",
            target_version="version_1_x",
            category="Security",
            tags=["Security", "Founder"],
            status="planned",
        )
        listed = client.get("/founder/vision?category=Security&status=planned")
        assert listed.status_code == 200
        assert b"Security Hardening" in listed.data
        assert b"Vision Journal" in listed.data

        overview = client.get("/founder/")
        assert overview.status_code == 200
        body = overview.get_data(as_text=True)
        assert "Vision Journal" in body
        assert "Awaiting validation" in body or "Recent" in body
        assert "Operational Health" in body

        export_json = client.get("/founder/vision/export/json")
        assert export_json.status_code == 200
        assert export_json.mimetype == "application/json"
        assert b"Security Hardening" in export_json.data

        export_md = client.get("/founder/vision/export/markdown")
        assert export_md.status_code == 200
        assert b"# Kwalitec Vision Journal" in export_md.data

        export_csv = client.get("/founder/vision/export/csv")
        assert export_csv.status_code == 200
        assert b"Security Hardening" in export_csv.data

    def test_relationships_and_promotion_http(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        base = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Learning Object Model",
            description="Base model",
            reason="Foundation",
            potential_value="high",
            expected_impact="Reuse",
            target_version="version_2",
            category="Educational Intelligence",
        )
        dependent = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Learning Confidence Engine",
            description="Depends on objects",
            reason="Intelligence",
            potential_value="high",
            expected_impact="Guidance",
            target_version="version_2",
            category="Educational Intelligence",
        )
        link = client.post(
            f"/founder/vision/{dependent.id}",
            data={
                "rel-to_entry_id": str(base.id),
                "rel-relation_type": "depends_on",
                "rel-submit": "Add link",
            },
            follow_redirects=True,
        )
        assert link.status_code == 200
        assert b"Learning Object Model" in link.data
        assert b"depends on" in link.data

        promote = client.post(
            f"/founder/vision/{dependent.id}",
            data={
                "promo-placeholder_ref": "ARCH-LOM-CONFIDENCE",
                "promo-notes": "Trace to architecture",
                "promo-submit": "Promote to Development",
            },
            follow_redirects=True,
        )
        assert promote.status_code == 200
        assert b"ARCH-LOM-CONFIDENCE" in promote.data
        entry = VisionJournalService.get_entry(dependent.id)
        assert entry is not None
        assert entry.status == "in_development"
        assert entry.promotions[0].placeholder_ref == "ARCH-LOM-CONFIDENCE"

    def test_student_workflows_unaffected(self, client, ctx, app) -> None:
        student = _make_user("student@kwalitec.example")
        client.post(
            "/auth/login",
            data={"email": student.email, "password": "password123"},
            follow_redirects=True,
        )
        dashboard = client.get("/dashboard/")
        assert dashboard.status_code == 200
        assert b"Vision Journal" not in dashboard.data

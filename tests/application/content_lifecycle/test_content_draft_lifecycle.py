"""Tests for ContentDraft model and ContentDraftService lifecycle rules."""

from __future__ import annotations

import json

import pytest

from app.application.content_lifecycle import (
    STATUS_APPROVED,
    STATUS_DRAFT,
    STATUS_READY_FOR_REVIEW,
    STATUS_REJECTED,
    ContentDraftService,
    IllegalLifecycleTransitionError,
)
from app.extensions import db
from app.models.content_draft import ContentDraft


def _minimal_payload(**overrides):
    base = {
        "package_id": "DRAFT-TEST-PKG",
        "subject_id": "CS1",
        "topic_code": "2.1.3",
        "status": "draft",
        "knowledge_checks": [],
    }
    base.update(overrides)
    return base


def test_create_draft_revision_one(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(),
        created_by="founder@example.com",
        topic_code="2.1.3",
        objective_id="CS1-B-T01-LO03",
    )
    db.session.commit()

    assert draft.id is not None
    assert draft.revision == 1
    assert draft.lifecycle_status == STATUS_DRAFT
    assert draft.content_id
    assert json.loads(draft.payload_json)["package_id"] == "DRAFT-TEST-PKG"
    assert draft.created_by == "founder@example.com"
    assert draft.approved_by is None
    assert draft.approved_at is None


def test_lifecycle_status_transitions(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(),
        created_by="founder",
    )
    service.transition_status(draft, STATUS_READY_FOR_REVIEW)
    assert draft.lifecycle_status == STATUS_READY_FOR_REVIEW

    service.transition_status(
        draft, STATUS_APPROVED, approved_by="reviewer@example.com"
    )
    assert draft.lifecycle_status == STATUS_APPROVED
    assert draft.approved_by == "reviewer@example.com"
    assert draft.approved_at is not None


def test_reject_from_ready_for_review(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(),
        created_by="founder",
    )
    service.transition_status(draft, STATUS_READY_FOR_REVIEW)
    service.transition_status(draft, STATUS_REJECTED)
    assert draft.lifecycle_status == STATUS_REJECTED


def test_illegal_transition_raises(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(),
        created_by="founder",
    )
    with pytest.raises(IllegalLifecycleTransitionError):
        service.transition_status(draft, STATUS_APPROVED)


def test_apply_edit_in_place_for_draft(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(display_title="Before"),
        created_by="founder",
    )
    content_id = draft.content_id
    updated = service.apply_edit(
        draft,
        payload=_minimal_payload(display_title="After"),
        human_edited={"display_title": "After"},
    )
    db.session.commit()

    assert updated.id == draft.id
    assert updated.revision == 1
    assert updated.content_id == content_id
    assert json.loads(updated.payload_json)["display_title"] == "After"
    assert updated.lifecycle_status == STATUS_DRAFT
    assert ContentDraft.query.filter_by(content_id=content_id).count() == 1


def test_apply_edit_on_approved_creates_new_revision(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(display_title="Approved body"),
        created_by="founder",
        objective_id="CS1-B-T01-LO03",
    )
    service.transition_status(draft, STATUS_READY_FOR_REVIEW)
    service.transition_status(
        draft, STATUS_APPROVED, approved_by="reviewer"
    )
    approved_id = draft.id
    approved_payload = draft.payload_json
    content_id = draft.content_id

    successor = service.apply_edit(
        draft,
        payload=_minimal_payload(display_title="Edited successor"),
        edited_by="editor",
    )
    db.session.commit()

    approved = db.session.get(ContentDraft, approved_id)
    assert approved is not None
    assert approved.lifecycle_status == STATUS_APPROVED
    assert approved.revision == 1
    assert approved.payload_json == approved_payload
    assert json.loads(approved.payload_json)["display_title"] == "Approved body"

    assert successor.id != approved_id
    assert successor.content_id == content_id
    assert successor.revision == 2
    assert successor.lifecycle_status == STATUS_DRAFT
    assert successor.approved_by is None
    assert successor.approved_at is None
    assert json.loads(successor.payload_json)["display_title"] == "Edited successor"
    assert ContentDraft.query.filter_by(content_id=content_id).count() == 2


def test_provenance_fields_persist(app, ctx):
    service = ContentDraftService()
    draft = service.create_draft(
        subject_id="CS1",
        payload=_minimal_payload(),
        created_by="author",
        ai_assisted=True,
        ai_proposed={"prompt": "draft me an MCQ"},
        human_edited={"prompt": "human rewrite"},
        live_package_id="CS1-EP001-PKG-EXAMPLE",
    )
    db.session.commit()

    assert draft.ai_assisted is True
    assert json.loads(draft.ai_proposed_json)["prompt"] == "draft me an MCQ"
    assert json.loads(draft.human_edited_json)["prompt"] == "human rewrite"
    assert draft.live_package_id == "CS1-EP001-PKG-EXAMPLE"

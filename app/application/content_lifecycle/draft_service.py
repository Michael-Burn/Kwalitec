"""Write API for educational content drafts with revision enforcement.

Editing an approved draft always creates a new revision row. Approved
payload columns are never updated in place. This module does not publish
content to the student runtime.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.application.content_lifecycle.statuses import (
    EDITABLE_STATUSES,
    LAWFUL_TRANSITIONS,
    STATUS_APPROVED,
    STATUS_DRAFT,
)
from app.extensions import db
from app.models.content_draft import ContentDraft


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class ContentLifecycleError(Exception):
    """Base error for content draft lifecycle operations."""


class IllegalLifecycleTransitionError(ContentLifecycleError):
    """Raised when a status transition is not lawful."""


class ApprovedContentImmutableError(ContentLifecycleError):
    """Raised when an in-place mutation of an approved draft is attempted."""


class ContentDraftService:
    """Create, edit, and transition content drafts with enforced rules."""

    def create_draft(
        self,
        *,
        subject_id: str,
        payload: dict[str, Any] | str,
        created_by: str,
        topic_code: str = "",
        objective_id: str = "",
        canonical_topic_id: str | None = None,
        content_id: str | None = None,
        ai_assisted: bool = False,
        ai_proposed: dict[str, Any] | str | None = None,
        human_edited: dict[str, Any] | str | None = None,
        live_package_id: str | None = None,
    ) -> ContentDraft:
        """Create revision 1 of a new content draft in ``draft`` status."""
        draft = ContentDraft(
            content_id=(content_id or str(uuid.uuid4())).strip(),
            revision=1,
            subject_id=(subject_id or "").strip(),
            canonical_topic_id=canonical_topic_id,
            topic_code=(topic_code or "").strip(),
            objective_id=(objective_id or "").strip(),
            payload_json=_as_json_text(payload),
            lifecycle_status=STATUS_DRAFT,
            created_by=(created_by or "").strip(),
            created_at=_utc_now(),
            updated_at=_utc_now(),
            ai_assisted=bool(ai_assisted),
            ai_proposed_json=_optional_json_text(ai_proposed),
            human_edited_json=_optional_json_text(human_edited),
            live_package_id=(live_package_id or None),
        )
        db.session.add(draft)
        db.session.flush()
        return draft

    def transition_status(
        self,
        draft: ContentDraft,
        new_status: str,
        *,
        approved_by: str | None = None,
    ) -> ContentDraft:
        """Apply a lawful lifecycle status transition.

        Approving records ``approved_by`` / ``approved_at``. Does not publish.
        """
        target = (new_status or "").strip().lower()
        current = (draft.lifecycle_status or "").strip().lower()
        allowed = LAWFUL_TRANSITIONS.get(current, frozenset())
        if target not in allowed:
            raise IllegalLifecycleTransitionError(
                f"Cannot transition content draft {draft.content_id} "
                f"revision {draft.revision} from {current!r} to {target!r}."
            )
        draft.lifecycle_status = target
        draft.updated_at = _utc_now()
        if target == STATUS_APPROVED:
            draft.approved_by = (approved_by or "").strip() or None
            draft.approved_at = _utc_now()
        db.session.flush()
        return draft

    def apply_edit(
        self,
        draft: ContentDraft,
        *,
        payload: dict[str, Any] | str | None = None,
        topic_code: str | None = None,
        objective_id: str | None = None,
        canonical_topic_id: str | None = None,
        ai_assisted: bool | None = None,
        ai_proposed: dict[str, Any] | str | None = None,
        human_edited: dict[str, Any] | str | None = None,
        edited_by: str = "",
    ) -> ContentDraft:
        """Edit draft payload/identity fields with revision enforcement.

        Editable statuses are updated in place. An approved draft always
        yields a new revision row in ``draft`` status; the approved row is
        left unchanged.
        """
        status = (draft.lifecycle_status or "").strip().lower()
        if status == STATUS_APPROVED:
            return self._create_successor_revision(
                draft,
                payload=payload,
                topic_code=topic_code,
                objective_id=objective_id,
                canonical_topic_id=canonical_topic_id,
                ai_assisted=ai_assisted,
                ai_proposed=ai_proposed,
                human_edited=human_edited,
                edited_by=edited_by,
            )
        if status not in EDITABLE_STATUSES:
            raise ApprovedContentImmutableError(
                f"Cannot mutate content draft {draft.content_id} "
                f"revision {draft.revision} in status {status!r}."
            )
        self._apply_fields_in_place(
            draft,
            payload=payload,
            topic_code=topic_code,
            objective_id=objective_id,
            canonical_topic_id=canonical_topic_id,
            ai_assisted=ai_assisted,
            ai_proposed=ai_proposed,
            human_edited=human_edited,
        )
        draft.updated_at = _utc_now()
        db.session.flush()
        return draft

    def _create_successor_revision(
        self,
        approved: ContentDraft,
        *,
        payload: dict[str, Any] | str | None,
        topic_code: str | None,
        objective_id: str | None,
        canonical_topic_id: str | None,
        ai_assisted: bool | None,
        ai_proposed: dict[str, Any] | str | None,
        human_edited: dict[str, Any] | str | None,
        edited_by: str,
    ) -> ContentDraft:
        """Insert a new draft revision; leave the approved row untouched."""
        next_revision = int(approved.revision) + 1
        successor = ContentDraft(
            content_id=approved.content_id,
            revision=next_revision,
            subject_id=approved.subject_id,
            canonical_topic_id=(
                canonical_topic_id
                if canonical_topic_id is not None
                else approved.canonical_topic_id
            ),
            topic_code=(
                topic_code
                if topic_code is not None
                else approved.topic_code
            ),
            objective_id=(
                objective_id
                if objective_id is not None
                else approved.objective_id
            ),
            payload_json=(
                _as_json_text(payload)
                if payload is not None
                else approved.payload_json
            ),
            lifecycle_status=STATUS_DRAFT,
            created_by=(edited_by or approved.created_by or "").strip(),
            created_at=_utc_now(),
            updated_at=_utc_now(),
            ai_assisted=(
                bool(ai_assisted)
                if ai_assisted is not None
                else bool(approved.ai_assisted)
            ),
            ai_proposed_json=(
                _optional_json_text(ai_proposed)
                if ai_proposed is not None
                else approved.ai_proposed_json
            ),
            human_edited_json=(
                _optional_json_text(human_edited)
                if human_edited is not None
                else approved.human_edited_json
            ),
            live_package_id=approved.live_package_id,
            approved_by=None,
            approved_at=None,
        )
        db.session.add(successor)
        db.session.flush()
        return successor

    @staticmethod
    def _apply_fields_in_place(
        draft: ContentDraft,
        *,
        payload: dict[str, Any] | str | None,
        topic_code: str | None,
        objective_id: str | None,
        canonical_topic_id: str | None,
        ai_assisted: bool | None,
        ai_proposed: dict[str, Any] | str | None,
        human_edited: dict[str, Any] | str | None,
    ) -> None:
        if payload is not None:
            draft.payload_json = _as_json_text(payload)
        if topic_code is not None:
            draft.topic_code = topic_code.strip()
        if objective_id is not None:
            draft.objective_id = objective_id.strip()
        if canonical_topic_id is not None:
            draft.canonical_topic_id = canonical_topic_id or None
        if ai_assisted is not None:
            draft.ai_assisted = bool(ai_assisted)
        if ai_proposed is not None:
            draft.ai_proposed_json = _optional_json_text(ai_proposed)
        if human_edited is not None:
            draft.human_edited_json = _optional_json_text(human_edited)


def _as_json_text(value: dict[str, Any] | str) -> str:
    if isinstance(value, str):
        text = value.strip()
        return text if text else "{}"
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _optional_json_text(
    value: dict[str, Any] | str | None,
) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return json.dumps(value, ensure_ascii=False, sort_keys=True)

"""Founder Vision Journal service (V1SP-001D).

Business logic for structured product vision entries: create, update,
search, filter, sort, relationships, promotion placeholders, and export.
Does not write educational evidence or Twin state.
"""

from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import or_

from app.extensions import db
from app.models.user import User
from app.models.vision_journal import (
    POTENTIAL_VALUE_RANK,
    POTENTIAL_VALUES,
    RELATION_TYPES,
    TARGET_VERSION_LABELS,
    TARGET_VERSIONS,
    VISION_CATEGORIES,
    VISION_STATUS_LABELS,
    VISION_STATUSES,
    VisionEntry,
    VisionEntryPromotion,
    VisionEntryRelation,
    VisionEntryStatusTransition,
)

SORT_NEWEST = "newest"
SORT_OLDEST = "oldest"
SORT_RECENTLY_UPDATED = "recently_updated"
SORT_TARGET_VERSION = "target_version"
SORT_STATUS = "status"
SORT_CATEGORY = "category"
SORT_HIGHEST_VALUE = "highest_potential_value"

SORT_OPTIONS: tuple[str, ...] = (
    SORT_NEWEST,
    SORT_OLDEST,
    SORT_RECENTLY_UPDATED,
    SORT_TARGET_VERSION,
    SORT_STATUS,
    SORT_CATEGORY,
    SORT_HIGHEST_VALUE,
)

SORT_LABELS: dict[str, str] = {
    SORT_NEWEST: "Newest",
    SORT_OLDEST: "Oldest",
    SORT_RECENTLY_UPDATED: "Recently Updated",
    SORT_TARGET_VERSION: "Target Version",
    SORT_STATUS: "Status",
    SORT_CATEGORY: "Category",
    SORT_HIGHEST_VALUE: "Highest Potential Value",
}

AWAITING_VALIDATION_STATUSES = frozenset({"vision", "research"})
PLANNED_STATUSES = frozenset({"planned", "validated"})
NEXT_VERSION_TARGETS = frozenset({"version_1_x", "version_2"})


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.strip().lower())
    slug = slug.strip("-") or "vision-entry"
    return slug[:80]


@dataclass(frozen=True)
class VisionSearchFilters:
    """Combined search / filter criteria for the Vision Journal."""

    query: str | None = None
    category: str | None = None
    status: str | None = None
    target_version: str | None = None
    tag: str | None = None
    author_user_id: int | None = None
    include_deleted: bool = False


@dataclass(frozen=True)
class VisionOverviewWidgets:
    """Compact Overview widgets for the Founder Command Centre."""

    recent_entries: tuple[VisionEntry, ...]
    awaiting_validation: tuple[VisionEntry, ...]
    planned_next_version: tuple[VisionEntry, ...]
    recently_promoted: tuple[tuple[VisionEntry, VisionEntryPromotion], ...]


@dataclass(frozen=True)
class TimelineEvent:
    """One chronological event for the Vision Journal timeline."""

    occurred_at: datetime
    kind: str
    entry_id: int
    entry_title: str
    detail: str


class VisionJournalService:
    """CRUD, search, relationships, promotion, and export for vision entries."""

    @staticmethod
    def create_entry(
        *,
        author_user_id: int,
        title: str,
        description: str,
        reason: str,
        potential_value: str,
        expected_impact: str,
        target_version: str,
        category: str,
        tags: list[str] | None = None,
        status: str = "vision",
        future_milestone: str | None = None,
    ) -> VisionEntry:
        """Create a vision entry and record the initial status transition."""
        VisionJournalService._validate_enums(
            potential_value=potential_value,
            target_version=target_version,
            category=category,
            status=status,
        )
        now = _utc_now()
        entry = VisionEntry(
            title=title.strip(),
            description=description.strip(),
            reason=reason.strip(),
            potential_value=potential_value,
            expected_impact=expected_impact.strip(),
            target_version=target_version,
            category=category,
            status=status,
            author_user_id=author_user_id,
            future_milestone=(future_milestone or "").strip() or None,
            created_at=now,
            updated_at=now,
        )
        entry.tags = tags or []
        db.session.add(entry)
        db.session.flush()
        db.session.add(
            VisionEntryStatusTransition(
                entry_id=entry.id,
                from_status=None,
                to_status=status,
                changed_by_user_id=author_user_id,
                note="Created",
                transitioned_at=now,
            )
        )
        db.session.commit()
        return entry

    @staticmethod
    def update_entry(
        entry_id: int,
        *,
        changed_by_user_id: int,
        title: str,
        description: str,
        reason: str,
        potential_value: str,
        expected_impact: str,
        target_version: str,
        category: str,
        tags: list[str] | None = None,
        status: str | None = None,
        future_milestone: str | None = None,
        status_note: str | None = None,
    ) -> VisionEntry | None:
        """Update fields; append status history when status changes."""
        entry = VisionJournalService.get_entry(entry_id)
        if entry is None:
            return None
        VisionJournalService._validate_enums(
            potential_value=potential_value,
            target_version=target_version,
            category=category,
            status=status or entry.status,
        )
        now = _utc_now()
        entry.title = title.strip()
        entry.description = description.strip()
        entry.reason = reason.strip()
        entry.potential_value = potential_value
        entry.expected_impact = expected_impact.strip()
        entry.target_version = target_version
        entry.category = category
        entry.tags = tags or []
        entry.future_milestone = (future_milestone or "").strip() or None
        if status is not None and status != entry.status:
            db.session.add(
                VisionEntryStatusTransition(
                    entry_id=entry.id,
                    from_status=entry.status,
                    to_status=status,
                    changed_by_user_id=changed_by_user_id,
                    note=(status_note or "").strip() or None,
                    transitioned_at=now,
                )
            )
            entry.status = status
        entry.updated_at = now
        db.session.commit()
        return entry

    @staticmethod
    def archive_entry(
        entry_id: int, *, changed_by_user_id: int, note: str | None = None
    ) -> VisionEntry | None:
        """Soft-archive an entry via status workflow (preferred over delete)."""
        return VisionJournalService.transition_status(
            entry_id,
            to_status="archived",
            changed_by_user_id=changed_by_user_id,
            note=note or "Archived",
        )

    @staticmethod
    def soft_delete_entry(
        entry_id: int, *, changed_by_user_id: int
    ) -> VisionEntry | None:
        """Soft-delete an entry; prefers archival first when still active."""
        entry = VisionJournalService.get_entry(entry_id, include_deleted=True)
        if entry is None or entry.is_deleted:
            return None
        now = _utc_now()
        if entry.status != "archived":
            db.session.add(
                VisionEntryStatusTransition(
                    entry_id=entry.id,
                    from_status=entry.status,
                    to_status="archived",
                    changed_by_user_id=changed_by_user_id,
                    note="Soft-deleted",
                    transitioned_at=now,
                )
            )
            entry.status = "archived"
        entry.deleted_at = now
        entry.updated_at = now
        db.session.commit()
        return entry

    @staticmethod
    def transition_status(
        entry_id: int,
        *,
        to_status: str,
        changed_by_user_id: int,
        note: str | None = None,
    ) -> VisionEntry | None:
        """Change status and append an immutable history row."""
        if to_status not in VISION_STATUSES:
            raise ValueError(f"Invalid status: {to_status}")
        entry = VisionJournalService.get_entry(entry_id)
        if entry is None:
            return None
        if entry.status == to_status:
            return entry
        now = _utc_now()
        db.session.add(
            VisionEntryStatusTransition(
                entry_id=entry.id,
                from_status=entry.status,
                to_status=to_status,
                changed_by_user_id=changed_by_user_id,
                note=(note or "").strip() or None,
                transitioned_at=now,
            )
        )
        entry.status = to_status
        entry.updated_at = now
        db.session.commit()
        return entry

    @staticmethod
    def get_entry(
        entry_id: int, *, include_deleted: bool = False
    ) -> VisionEntry | None:
        """Return a single entry by id, or None."""
        entry = db.session.get(VisionEntry, entry_id)
        if entry is None:
            return None
        if entry.is_deleted and not include_deleted:
            return None
        return entry

    @staticmethod
    def search(
        filters: VisionSearchFilters | None = None,
        *,
        sort: str = SORT_NEWEST,
        limit: int = 200,
    ) -> list[VisionEntry]:
        """Search and filter entries. Responsive for hundreds of rows."""
        filters = filters or VisionSearchFilters()
        sort = sort if sort in SORT_OPTIONS else SORT_NEWEST
        q = VisionEntry.query
        if not filters.include_deleted:
            q = q.filter(VisionEntry.deleted_at.is_(None))
        if filters.category:
            q = q.filter(VisionEntry.category == filters.category)
        if filters.status:
            q = q.filter(VisionEntry.status == filters.status)
        if filters.target_version:
            q = q.filter(VisionEntry.target_version == filters.target_version)
        if filters.author_user_id is not None:
            q = q.filter(VisionEntry.author_user_id == filters.author_user_id)
        if filters.tag:
            tag = filters.tag.strip()
            q = q.filter(VisionEntry.tags_csv.ilike(f"%{tag}%"))
        if filters.query:
            term = filters.query.strip()
            if term:
                like = f"%{term}%"
                q = q.filter(
                    or_(
                        VisionEntry.title.ilike(like),
                        VisionEntry.description.ilike(like),
                        VisionEntry.category.ilike(like),
                        VisionEntry.status.ilike(like),
                        VisionEntry.target_version.ilike(like),
                        VisionEntry.tags_csv.ilike(like),
                    )
                )
        entries = q.all()
        entries = VisionJournalService._sort_entries(entries, sort)
        return entries[:limit]

    @staticmethod
    def add_relation(
        *,
        from_entry_id: int,
        to_entry_id: int,
        relation_type: str,
        created_by_user_id: int,
    ) -> VisionEntryRelation | None:
        """Link two entries. No dependency validation."""
        if relation_type not in RELATION_TYPES:
            raise ValueError(f"Invalid relation type: {relation_type}")
        if from_entry_id == to_entry_id:
            raise ValueError("Cannot relate an entry to itself")
        source = VisionJournalService.get_entry(from_entry_id)
        target = VisionJournalService.get_entry(to_entry_id)
        if source is None or target is None:
            return None
        existing = VisionEntryRelation.query.filter_by(
            from_entry_id=from_entry_id,
            to_entry_id=to_entry_id,
            relation_type=relation_type,
        ).first()
        if existing is not None:
            return existing
        relation = VisionEntryRelation(
            from_entry_id=from_entry_id,
            to_entry_id=to_entry_id,
            relation_type=relation_type,
            created_by_user_id=created_by_user_id,
            created_at=_utc_now(),
        )
        db.session.add(relation)
        source.updated_at = _utc_now()
        db.session.commit()
        return relation

    @staticmethod
    def remove_relation(relation_id: int) -> bool:
        """Remove a relationship link."""
        relation = db.session.get(VisionEntryRelation, relation_id)
        if relation is None:
            return False
        db.session.delete(relation)
        db.session.commit()
        return True

    @staticmethod
    def list_related(entry_id: int) -> list[VisionEntryRelation]:
        """Return outgoing and incoming relations for an entry."""
        return (
            VisionEntryRelation.query.filter(
                or_(
                    VisionEntryRelation.from_entry_id == entry_id,
                    VisionEntryRelation.to_entry_id == entry_id,
                )
            )
            .order_by(VisionEntryRelation.created_at.asc())
            .all()
        )

    @staticmethod
    def promote_to_development(
        entry_id: int,
        *,
        promoted_by_user_id: int,
        notes: str | None = None,
        placeholder_ref: str | None = None,
    ) -> VisionEntryPromotion | None:
        """Create a promotion placeholder for future architecture linkage.

        Does not create implementation work — only traceability.
        """
        entry = VisionJournalService.get_entry(entry_id)
        if entry is None:
            return None
        now = _utc_now()
        ref = (placeholder_ref or "").strip()
        if not ref:
            ref = f"ARCH-PLACEHOLDER-{entry.id}-{_slugify(entry.title)}"
        promotion = VisionEntryPromotion(
            entry_id=entry.id,
            placeholder_ref=ref,
            notes=(notes or "").strip() or None,
            promoted_by_user_id=promoted_by_user_id,
            promoted_at=now,
        )
        db.session.add(promotion)
        if entry.status not in {
            "in_development",
            "implemented",
            "rejected",
            "archived",
        }:
            db.session.add(
                VisionEntryStatusTransition(
                    entry_id=entry.id,
                    from_status=entry.status,
                    to_status="in_development",
                    changed_by_user_id=promoted_by_user_id,
                    note="Promoted to Development (placeholder)",
                    transitioned_at=now,
                )
            )
            entry.status = "in_development"
        entry.updated_at = now
        db.session.commit()
        return promotion

    @staticmethod
    def build_timeline(*, limit: int = 100) -> list[TimelineEvent]:
        """Chronological timeline of creations and status changes."""
        events: list[TimelineEvent] = []
        entries = (
            VisionEntry.query.filter(VisionEntry.deleted_at.is_(None))
            .order_by(VisionEntry.created_at.desc())
            .limit(limit)
            .all()
        )
        entry_ids = [e.id for e in entries]
        by_id = {e.id: e for e in entries}
        for entry in entries:
            status_label = VISION_STATUS_LABELS.get(entry.status, entry.status)
            events.append(
                TimelineEvent(
                    occurred_at=entry.created_at,
                    kind="created",
                    entry_id=entry.id,
                    entry_title=entry.title,
                    detail=f"Created as {status_label}",
                )
            )
        if entry_ids:
            transitions = (
                VisionEntryStatusTransition.query.filter(
                    VisionEntryStatusTransition.entry_id.in_(entry_ids),
                    VisionEntryStatusTransition.from_status.isnot(None),
                )
                .order_by(VisionEntryStatusTransition.transitioned_at.desc())
                .limit(limit)
                .all()
            )
            for tr in transitions:
                entry = by_id.get(tr.entry_id)
                if entry is None:
                    continue
                from_label = VISION_STATUS_LABELS.get(
                    tr.from_status or "", tr.from_status or "—"
                )
                to_label = VISION_STATUS_LABELS.get(tr.to_status, tr.to_status)
                events.append(
                    TimelineEvent(
                        occurred_at=tr.transitioned_at,
                        kind="status",
                        entry_id=entry.id,
                        entry_title=entry.title,
                        detail=f"{from_label} → {to_label}",
                    )
                )
        events.sort(key=lambda e: e.occurred_at, reverse=True)
        return events[:limit]

    @staticmethod
    def overview_widgets(*, limit: int = 5) -> VisionOverviewWidgets:
        """Compact strategic widgets for Founder Overview."""
        recent = VisionJournalService.search(
            VisionSearchFilters(), sort=SORT_NEWEST, limit=limit
        )
        awaiting = (
            VisionEntry.query.filter(
                VisionEntry.deleted_at.is_(None),
                VisionEntry.status.in_(AWAITING_VALIDATION_STATUSES),
            )
            .order_by(VisionEntry.updated_at.desc())
            .limit(limit)
            .all()
        )
        planned = (
            VisionEntry.query.filter(
                VisionEntry.deleted_at.is_(None),
                VisionEntry.status.in_(PLANNED_STATUSES),
                VisionEntry.target_version.in_(NEXT_VERSION_TARGETS),
            )
            .order_by(VisionEntry.updated_at.desc())
            .limit(limit)
            .all()
        )
        promotions = (
            VisionEntryPromotion.query.order_by(
                VisionEntryPromotion.promoted_at.desc()
            )
            .limit(limit)
            .all()
        )
        recently_promoted: list[tuple[VisionEntry, VisionEntryPromotion]] = []
        entry_ids = [promo.entry_id for promo in promotions]
        entries_by_id: dict[int, VisionEntry] = {}
        if entry_ids:
            entries_by_id = {
                entry.id: entry
                for entry in VisionEntry.query.filter(
                    VisionEntry.id.in_(entry_ids)
                ).all()
            }
        for promo in promotions:
            entry = entries_by_id.get(promo.entry_id)
            if entry is not None and not entry.is_deleted:
                recently_promoted.append((entry, promo))
        return VisionOverviewWidgets(
            recent_entries=tuple(recent),
            awaiting_validation=tuple(awaiting),
            planned_next_version=tuple(planned),
            recently_promoted=tuple(recently_promoted),
        )

    @staticmethod
    def export_json(filters: VisionSearchFilters | None = None) -> str:
        """Export matching entries as JSON."""
        entries = VisionJournalService.search(filters, limit=10_000)
        payload = [
            VisionJournalService._entry_dict(e) for e in entries
        ]
        return json.dumps(payload, indent=2, default=str)

    @staticmethod
    def export_csv(filters: VisionSearchFilters | None = None) -> str:
        """Export matching entries as CSV."""
        entries = VisionJournalService.search(filters, limit=10_000)
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=[
                "id",
                "title",
                "description",
                "reason",
                "potential_value",
                "expected_impact",
                "target_version",
                "category",
                "status",
                "tags",
                "author_user_id",
                "future_milestone",
                "created_at",
                "updated_at",
            ],
        )
        writer.writeheader()
        for entry in entries:
            writer.writerow(
                {
                    "id": entry.id,
                    "title": entry.title,
                    "description": entry.description,
                    "reason": entry.reason,
                    "potential_value": entry.potential_value,
                    "expected_impact": entry.expected_impact,
                    "target_version": entry.target_version,
                    "category": entry.category,
                    "status": entry.status,
                    "tags": entry.tags_csv,
                    "author_user_id": entry.author_user_id,
                    "future_milestone": entry.future_milestone or "",
                    "created_at": entry.created_at.isoformat(),
                    "updated_at": entry.updated_at.isoformat(),
                }
            )
        return buffer.getvalue()

    @staticmethod
    def export_markdown(filters: VisionSearchFilters | None = None) -> str:
        """Export matching entries as Markdown."""
        entries = VisionJournalService.search(filters, limit=10_000)
        lines = [
            "# Kwalitec Vision Journal",
            "",
            f"Exported: {_utc_now().isoformat()}Z",
            f"Entries: {len(entries)}",
            "",
        ]
        for entry in entries:
            author = db.session.get(User, entry.author_user_id)
            author_label = (
                author.email if author else f"user:{entry.author_user_id}"
            )
            status_label = VISION_STATUS_LABELS.get(entry.status, entry.status)
            version_label = TARGET_VERSION_LABELS.get(
                entry.target_version, entry.target_version
            )
            lines.extend(
                [
                    f"## {entry.title}",
                    "",
                    f"- **Status:** {status_label}",
                    f"- **Category:** {entry.category}",
                    f"- **Target Version:** {version_label}",
                    f"- **Potential Value:** {entry.potential_value}",
                    f"- **Tags:** {entry.tags_csv or '—'}",
                    f"- **Author:** {author_label}",
                    f"- **Created:** {entry.created_at.isoformat()}",
                    f"- **Updated:** {entry.updated_at.isoformat()}",
                    "",
                    "### Description",
                    "",
                    entry.description,
                    "",
                    "### Reason",
                    "",
                    entry.reason,
                    "",
                    "### Expected Impact",
                    "",
                    entry.expected_impact,
                    "",
                    "---",
                    "",
                ]
            )
        return "\n".join(lines)

    @staticmethod
    def list_authors() -> list[tuple[int, str]]:
        """Distinct authors with at least one non-deleted entry."""
        rows = (
            db.session.query(VisionEntry.author_user_id, User.email)
            .join(User, User.id == VisionEntry.author_user_id)
            .filter(VisionEntry.deleted_at.is_(None))
            .distinct()
            .order_by(User.email.asc())
            .all()
        )
        return [(int(uid), str(email)) for uid, email in rows]

    @staticmethod
    def _entry_dict(entry: VisionEntry) -> dict:
        return {
            "id": entry.id,
            "title": entry.title,
            "description": entry.description,
            "reason": entry.reason,
            "potential_value": entry.potential_value,
            "expected_impact": entry.expected_impact,
            "target_version": entry.target_version,
            "category": entry.category,
            "status": entry.status,
            "tags": entry.tags,
            "author_user_id": entry.author_user_id,
            "future_milestone": entry.future_milestone,
            "created_at": entry.created_at.isoformat(),
            "updated_at": entry.updated_at.isoformat(),
        }

    @staticmethod
    def _sort_entries(entries: list[VisionEntry], sort: str) -> list[VisionEntry]:
        if sort == SORT_OLDEST:
            return sorted(entries, key=lambda e: e.created_at)
        if sort == SORT_RECENTLY_UPDATED:
            return sorted(entries, key=lambda e: e.updated_at, reverse=True)
        if sort == SORT_TARGET_VERSION:
            order = {v: i for i, v in enumerate(TARGET_VERSIONS)}
            return sorted(
                entries,
                key=lambda e: (order.get(e.target_version, 99), e.title.lower()),
            )
        if sort == SORT_STATUS:
            order = {s: i for i, s in enumerate(VISION_STATUSES)}
            return sorted(
                entries,
                key=lambda e: (order.get(e.status, 99), e.title.lower()),
            )
        if sort == SORT_CATEGORY:
            return sorted(entries, key=lambda e: (e.category.lower(), e.title.lower()))
        if sort == SORT_HIGHEST_VALUE:
            return sorted(
                entries,
                key=lambda e: (
                    -POTENTIAL_VALUE_RANK.get(e.potential_value, 0),
                    e.title.lower(),
                ),
            )
        # Newest (default)
        return sorted(entries, key=lambda e: e.created_at, reverse=True)

    @staticmethod
    def _validate_enums(
        *,
        potential_value: str,
        target_version: str,
        category: str,
        status: str,
    ) -> None:
        if potential_value not in POTENTIAL_VALUES:
            raise ValueError(f"Invalid potential_value: {potential_value}")
        if target_version not in TARGET_VERSIONS:
            raise ValueError(f"Invalid target_version: {target_version}")
        if category not in VISION_CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        if status not in VISION_STATUSES:
            raise ValueError(f"Invalid status: {status}")

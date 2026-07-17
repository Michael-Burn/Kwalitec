"""ORM models for the Founder Vision Journal (V1SP-001D).

Structured strategic memory for product ideas before architecture or
implementation. Founder-only; independent of educational evidence and
student learning algorithms.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


VISION_CATEGORIES: tuple[str, ...] = (
    "Educational Intelligence",
    "Student Experience",
    "Founder Experience",
    "Analytics",
    "Student Digital Twin",
    "Assessment",
    "Revision",
    "Infrastructure",
    "Security",
    "Performance",
    "Brand",
    "Research",
    "Operations",
    "Other",
)

VISION_STATUSES: tuple[str, ...] = (
    "vision",
    "research",
    "validated",
    "planned",
    "in_development",
    "implemented",
    "rejected",
    "archived",
)

VISION_STATUS_LABELS: dict[str, str] = {
    "vision": "Vision",
    "research": "Research",
    "validated": "Validated",
    "planned": "Planned",
    "in_development": "In Development",
    "implemented": "Implemented",
    "rejected": "Rejected",
    "archived": "Archived",
}

TARGET_VERSIONS: tuple[str, ...] = (
    "version_1_x",
    "version_2",
    "version_3",
    "future",
    "unknown",
)

TARGET_VERSION_LABELS: dict[str, str] = {
    "version_1_x": "Version 1.x",
    "version_2": "Version 2",
    "version_3": "Version 3",
    "future": "Future",
    "unknown": "Unknown",
}

POTENTIAL_VALUES: tuple[str, ...] = (
    "critical",
    "high",
    "medium",
    "low",
    "exploratory",
)

POTENTIAL_VALUE_LABELS: dict[str, str] = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
    "exploratory": "Exploratory",
}

POTENTIAL_VALUE_RANK: dict[str, int] = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "exploratory": 1,
}

RELATION_TYPES: tuple[str, ...] = ("depends_on", "related_to")

RELATION_TYPE_LABELS: dict[str, str] = {
    "depends_on": "depends on",
    "related_to": "related to",
}

EXAMPLE_TAGS: tuple[str, ...] = (
    "AI",
    "Twin",
    "Learning Objects",
    "Revision",
    "Dashboard",
    "UX",
    "Mobile",
    "Founder",
    "Performance",
    "Infrastructure",
    "Security",
    "Analytics",
)


class VisionEntry(db.Model):
    """One structured Founder Vision Journal entry."""

    __tablename__ = "vision_entries"

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False, index=True)
    description: str = db.Column(db.Text, nullable=False)
    reason: str = db.Column(db.Text, nullable=False)
    potential_value: str = db.Column(
        db.String(32), nullable=False, default="medium", index=True
    )
    expected_impact: str = db.Column(db.Text, nullable=False)
    target_version: str = db.Column(
        db.String(32), nullable=False, default="unknown", index=True
    )
    category: str = db.Column(db.String(64), nullable=False, index=True)
    status: str = db.Column(
        db.String(32), nullable=False, default="vision", index=True
    )
    tags_csv: str = db.Column(db.String(500), nullable=False, default="")
    author_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    future_milestone: str | None = db.Column(db.String(200), nullable=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    deleted_at: datetime | None = db.Column(db.DateTime, nullable=True, index=True)

    author = db.relationship("User", foreign_keys=[author_user_id])
    status_transitions = db.relationship(
        "VisionEntryStatusTransition",
        back_populates="entry",
        lazy=True,
        order_by="VisionEntryStatusTransition.transitioned_at",
        cascade="all, delete-orphan",
    )
    outgoing_relations = db.relationship(
        "VisionEntryRelation",
        foreign_keys="VisionEntryRelation.from_entry_id",
        back_populates="from_entry",
        lazy=True,
        cascade="all, delete-orphan",
    )
    incoming_relations = db.relationship(
        "VisionEntryRelation",
        foreign_keys="VisionEntryRelation.to_entry_id",
        back_populates="to_entry",
        lazy=True,
        cascade="all, delete-orphan",
    )
    promotions = db.relationship(
        "VisionEntryPromotion",
        back_populates="entry",
        lazy=True,
        order_by="VisionEntryPromotion.promoted_at",
        cascade="all, delete-orphan",
    )

    @property
    def tags(self) -> list[str]:
        """Parse comma-separated tags into a normalised list."""
        if not self.tags_csv or not self.tags_csv.strip():
            return []
        return [
            part.strip()
            for part in self.tags_csv.split(",")
            if part.strip()
        ]

    @tags.setter
    def tags(self, values: list[str] | tuple[str, ...] | None) -> None:
        cleaned: list[str] = []
        seen: set[str] = set()
        for raw in values or ():
            tag = str(raw).strip()
            if not tag:
                continue
            key = tag.casefold()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(tag)
        self.tags_csv = ", ".join(cleaned)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def __repr__(self) -> str:
        return f"<VisionEntry id={self.id} title={self.title!r} status={self.status}>"


class VisionEntryStatusTransition(db.Model):
    """Append-only status history for a vision entry."""

    __tablename__ = "vision_entry_status_transitions"

    id: int = db.Column(db.Integer, primary_key=True)
    entry_id: int = db.Column(
        db.Integer,
        db.ForeignKey("vision_entries.id"),
        nullable=False,
        index=True,
    )
    from_status: str | None = db.Column(db.String(32), nullable=True)
    to_status: str = db.Column(db.String(32), nullable=False)
    changed_by_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    note: str | None = db.Column(db.String(500), nullable=True)
    transitioned_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    entry = db.relationship("VisionEntry", back_populates="status_transitions")
    changed_by = db.relationship("User", foreign_keys=[changed_by_user_id])

    def __repr__(self) -> str:
        return (
            f"<VisionEntryStatusTransition id={self.id} "
            f"entry={self.entry_id} {self.from_status}->{self.to_status}>"
        )


class VisionEntryRelation(db.Model):
    """Optional link between vision entries (no dependency validation)."""

    __tablename__ = "vision_entry_relations"

    id: int = db.Column(db.Integer, primary_key=True)
    from_entry_id: int = db.Column(
        db.Integer,
        db.ForeignKey("vision_entries.id"),
        nullable=False,
        index=True,
    )
    to_entry_id: int = db.Column(
        db.Integer,
        db.ForeignKey("vision_entries.id"),
        nullable=False,
        index=True,
    )
    relation_type: str = db.Column(db.String(32), nullable=False, index=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now
    )
    created_by_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )

    from_entry = db.relationship(
        "VisionEntry",
        foreign_keys=[from_entry_id],
        back_populates="outgoing_relations",
    )
    to_entry = db.relationship(
        "VisionEntry",
        foreign_keys=[to_entry_id],
        back_populates="incoming_relations",
    )
    created_by = db.relationship("User", foreign_keys=[created_by_user_id])

    __table_args__ = (
        db.UniqueConstraint(
            "from_entry_id",
            "to_entry_id",
            "relation_type",
            name="uq_vision_relation",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<VisionEntryRelation {self.from_entry_id} "
            f"{self.relation_type} {self.to_entry_id}>"
        )


class VisionEntryPromotion(db.Model):
    """Placeholder linking a journal entry to future architecture work.

    Does not create implementation tickets — only establishes traceability.
    """

    __tablename__ = "vision_entry_promotions"

    id: int = db.Column(db.Integer, primary_key=True)
    entry_id: int = db.Column(
        db.Integer,
        db.ForeignKey("vision_entries.id"),
        nullable=False,
        index=True,
    )
    placeholder_ref: str = db.Column(db.String(200), nullable=False)
    notes: str | None = db.Column(db.String(1000), nullable=True)
    promoted_by_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    promoted_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    entry = db.relationship("VisionEntry", back_populates="promotions")
    promoted_by = db.relationship("User", foreign_keys=[promoted_by_user_id])

    def __repr__(self) -> str:
        return (
            f"<VisionEntryPromotion id={self.id} entry={self.entry_id} "
            f"ref={self.placeholder_ref!r}>"
        )

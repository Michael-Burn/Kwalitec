"""Identity RBAC persistence — roles and portal capabilities (PR-001)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC)


class UserRole(db.Model):
    """Role assignment for a single User identity."""

    __tablename__ = "user_roles"
    __table_args__ = (
        db.UniqueConstraint("user_id", "role", name="uq_user_roles_user_role"),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: str = db.Column(db.String(64), nullable=False, index=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now
    )

    user = db.relationship("User", back_populates="role_assignments")


class UserCapability(db.Model):
    """Portal capability assignment for a single User identity."""

    __tablename__ = "user_capabilities"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "capability", name="uq_user_capabilities_user_cap"
        ),
    )

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    capability: str = db.Column(db.String(64), nullable=False, index=True)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now
    )

    user = db.relationship("User", back_populates="capability_assignments")

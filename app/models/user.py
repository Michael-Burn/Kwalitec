"""User model for authentication."""

from __future__ import annotations

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """Application user suitable for Flask-Login.

    The application is initially designed for a single user. This model keeps
    the foundation compatible with future authentication improvements without
    implementing registration yet.
    """

    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    email: str = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(255), nullable=False)
    is_active_user: bool = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships — declared explicitly with back_populates matching child-side declarations
    subjects = db.relationship("Subject", back_populates="user", lazy=True)
    missions = db.relationship("Mission", back_populates="user", lazy=True)
    study_plans = db.relationship("StudyPlan", back_populates="user", lazy=True)
    study_attempts = db.relationship("StudyAttempt", back_populates="user", lazy=True)
    topic_progress = db.relationship("TopicProgress", back_populates="user", lazy=True)
    decisions = db.relationship("Decision", back_populates="user", lazy=True)

    def set_password(self, password: str) -> None:
        """Hash and store a plaintext password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Validate a plaintext password against the stored password hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self) -> bool:  # type: ignore[override]
        """Return whether this user is active for Flask-Login."""
        return self.is_active_user


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """Load a user by ID for Flask-Login sessions."""
    if not user_id.isdigit():
        return None

    return db.session.get(User, int(user_id))
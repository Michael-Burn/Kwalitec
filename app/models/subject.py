"""Subject model for organizing missions."""

from __future__ import annotations

from datetime import datetime

from app.extensions import db


class Subject(db.Model):
    """Subject that groups related missions.
    
    A user can have many subjects, and each subject can have many missions.
    Subjects are used to organize and categorize learning areas.
    """

    __tablename__ = "subjects"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name: str = db.Column(db.String(255), nullable=False)
    colour: str = db.Column(db.String(7), default="#007bff")  # Hex color code
    active: bool = db.Column(db.Boolean, default=True, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="subjects")
    missions = db.relationship(
        "Mission",
        back_populates="subject",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Subject {self.name}>"
"""SQLAlchemy persistence model for teaching-plan ↔ episode bindings."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class TeachingPlanModel(Base):
    """Persistence row for plan identity ↔ learning-episode coordination."""

    __tablename__ = "eos_teaching_plans"

    plan_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    episode_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
        index=True,
    )

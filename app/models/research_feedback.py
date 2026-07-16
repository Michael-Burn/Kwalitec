"""ORM models for Research Intelligence product check-ins (RIP-001).

Stores structured product-experience feedback and contribution records.
Independent of Educational Evidence, Twin state, and learning algorithms.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.extensions import db


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class ResearchFeedbackSubmission(db.Model):
    """One completed Daily Reflection & Product Check-in submission.

    Captures structured ratings, optional free-text with classification,
    and study context for later Founder Intelligence (RIP-003). Does not
    mutate educational state.
    """

    __tablename__ = "research_feedback_submissions"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    submitted_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    product_version: str = db.Column(db.String(32), nullable=False)

    study_plan_id: int | None = db.Column(
        db.Integer, db.ForeignKey("study_plans.id"), nullable=True
    )
    mission_id: int | None = db.Column(
        db.Integer, db.ForeignKey("missions.id"), nullable=True
    )

    experience_rating: str = db.Column(db.String(32), nullable=False)
    feature_helped_most: str = db.Column(db.String(64), nullable=False)
    friction_area: str = db.Column(db.String(64), nullable=False)
    confidence_rating: str = db.Column(db.String(32), nullable=False)
    return_intent: str = db.Column(db.String(32), nullable=False)

    free_text: str | None = db.Column(db.String(300), nullable=True)
    classification: str | None = db.Column(db.String(32), nullable=True)

    submission_source: str = db.Column(db.String(32), nullable=False)

    workflow_status: str = db.Column(
        db.String(32), nullable=False, default="new", index=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("research_feedback_submissions", lazy=True),
    )
    contribution = db.relationship(
        "ResearchContribution",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan",
    )
    status_transitions = db.relationship(
        "ResearchFeedbackStatusTransition",
        back_populates="submission",
        lazy=True,
        order_by="ResearchFeedbackStatusTransition.transitioned_at",
    )
    founder_notes = db.relationship(
        "ResearchFounderNote",
        back_populates="submission",
        lazy=True,
        order_by="ResearchFounderNote.created_at",
    )
    finding_links = db.relationship(
        "ResearchProductFindingLink",
        back_populates="submission",
        lazy=True,
    )

    def __repr__(self) -> str:
        return (
            f"<ResearchFeedbackSubmission id={self.id} "
            f"user={self.user_id} source={self.submission_source}>"
        )


class ResearchContribution(db.Model):
    """Durable unit of recognised student help toward product improvement.

    Created one-for-one with each completed Product Check-in.
    Badges belong to RIP-002 and are not modelled here.
    """

    __tablename__ = "research_contributions"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    submission_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_feedback_submissions.id"),
        nullable=False,
        unique=True,
    )
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    user = db.relationship(
        "User",
        backref=db.backref("research_contributions", lazy=True),
    )
    submission = db.relationship(
        "ResearchFeedbackSubmission", back_populates="contribution"
    )

    def __repr__(self) -> str:
        return (
            f"<ResearchContribution id={self.id} "
            f"user={self.user_id} submission={self.submission_id}>"
        )


class ResearchContributorBadge(db.Model):
    """Contributor recognition badge awarded to a student (RIP-002).

    Automatic badges follow check-in thresholds. Product Shaper and
    Founder's Circle are Founder-awarded only.
    """

    __tablename__ = "research_contributor_badges"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    badge_slug: str = db.Column(db.String(32), nullable=False, index=True)
    awarded_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    trigger_contribution_id: int | None = db.Column(
        db.Integer,
        db.ForeignKey("research_contributions.id"),
        nullable=True,
    )
    trigger_submission_id: int | None = db.Column(
        db.Integer,
        db.ForeignKey("research_feedback_submissions.id"),
        nullable=True,
    )
    awarded_by_user_id: int | None = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref("research_contributor_badges", lazy=True),
    )
    awarded_by = db.relationship(
        "User",
        foreign_keys=[awarded_by_user_id],
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "badge_slug", name="uq_user_badge_slug"),
    )

    def __repr__(self) -> str:
        return (
            f"<ResearchContributorBadge id={self.id} "
            f"user={self.user_id} badge={self.badge_slug}>"
        )


class ResearchFeedbackReview(db.Model):
    """Founder review marks on a Product Check-in submission (RIP-002).

    Helpful and Insightful are qualitative signals for RIP-003.
    Only Implemented contributes toward Product Shaper recognition.
    """

    __tablename__ = "research_feedback_reviews"

    id: int = db.Column(db.Integer, primary_key=True)
    submission_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_feedback_submissions.id"),
        nullable=False,
        unique=True,
    )
    founder_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    is_helpful: bool = db.Column(db.Boolean, nullable=False, default=False)
    is_insightful: bool = db.Column(db.Boolean, nullable=False, default=False)
    is_implemented: bool = db.Column(db.Boolean, nullable=False, default=False)
    reviewed_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    submission = db.relationship(
        "ResearchFeedbackSubmission",
        backref=db.backref("founder_review", uselist=False),
    )
    founder = db.relationship("User", foreign_keys=[founder_user_id])

    def __repr__(self) -> str:
        return (
            f"<ResearchFeedbackReview id={self.id} "
            f"submission={self.submission_id} implemented={self.is_implemented}>"
        )


WORKFLOW_STATUSES: tuple[str, ...] = (
    "new",
    "under_review",
    "accepted",
    "planned",
    "implemented",
    "released",
    "verified",
    "rejected",
    "clarification_requested",
)

SEVERITY_CHOICES: tuple[str, ...] = (
    "Critical",
    "High",
    "Medium",
    "Low",
    "Enhancement",
    "Version 2",
)

FEATURE_AREA_CHOICES: tuple[str, ...] = (
    "Study Session",
    "Dashboard",
    "Analytics",
    "Study Plan",
    "Recommendations",
    "Navigation",
    "Settings",
    "Onboarding",
    "Performance",
    "Research Experience",
    "Other",
)

FINDING_STATUSES: tuple[str, ...] = (
    "new",
    "under_review",
    "accepted",
    "planned",
    "implemented",
    "released",
    "verified",
)


class ResearchFeedbackStatusTransition(db.Model):
    """Append-only workflow history for a feedback submission (RIP-003)."""

    __tablename__ = "research_feedback_status_transitions"

    id: int = db.Column(db.Integer, primary_key=True)
    submission_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_feedback_submissions.id"),
        nullable=False,
        index=True,
    )
    from_status: str | None = db.Column(db.String(32), nullable=True)
    to_status: str = db.Column(db.String(32), nullable=False)
    reviewer_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    rationale: str | None = db.Column(db.String(500), nullable=True)
    transitioned_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    submission = db.relationship(
        "ResearchFeedbackSubmission", back_populates="status_transitions"
    )
    reviewer = db.relationship("User", foreign_keys=[reviewer_user_id])

    def __repr__(self) -> str:
        return (
            f"<ResearchFeedbackStatusTransition id={self.id} "
            f"submission={self.submission_id} {self.from_status}->{self.to_status}>"
        )


class ResearchFounderNote(db.Model):
    """Internal Founder note on a feedback submission (RIP-003)."""

    __tablename__ = "research_founder_notes"

    id: int = db.Column(db.Integer, primary_key=True)
    submission_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_feedback_submissions.id"),
        nullable=False,
        index=True,
    )
    founder_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    note_text: str = db.Column(db.String(1000), nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    submission = db.relationship(
        "ResearchFeedbackSubmission", back_populates="founder_notes"
    )
    founder = db.relationship("User", foreign_keys=[founder_user_id])

    def __repr__(self) -> str:
        return (
            f"<ResearchFounderNote id={self.id} submission={self.submission_id}>"
        )


class ResearchProductFinding(db.Model):
    """Founder-authored product finding linked to feedback (RIP-003)."""

    __tablename__ = "research_product_findings"

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False)
    summary: str = db.Column(db.String(1000), nullable=False)
    severity: str = db.Column(db.String(32), nullable=False, index=True)
    feature_area: str = db.Column(db.String(64), nullable=False, index=True)
    status: str = db.Column(
        db.String(32), nullable=False, default="new", index=True
    )
    target_release: str | None = db.Column(db.String(32), nullable=True)
    notes: str | None = db.Column(db.String(2000), nullable=True)
    created_by_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )
    updated_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    created_by = db.relationship("User", foreign_keys=[created_by_user_id])
    feedback_links = db.relationship(
        "ResearchProductFindingLink",
        back_populates="finding",
        lazy=True,
        cascade="all, delete-orphan",
    )
    status_transitions = db.relationship(
        "ResearchProductFindingStatusTransition",
        back_populates="finding",
        lazy=True,
        order_by="ResearchProductFindingStatusTransition.transitioned_at",
    )

    def __repr__(self) -> str:
        return f"<ResearchProductFinding id={self.id} title={self.title!r}>"


class ResearchProductFindingLink(db.Model):
    """Many-to-many link between findings and feedback submissions."""

    __tablename__ = "research_product_finding_links"

    id: int = db.Column(db.Integer, primary_key=True)
    finding_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_product_findings.id"),
        nullable=False,
        index=True,
    )
    submission_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_feedback_submissions.id"),
        nullable=False,
        index=True,
    )

    finding = db.relationship(
        "ResearchProductFinding", back_populates="feedback_links"
    )
    submission = db.relationship(
        "ResearchFeedbackSubmission", back_populates="finding_links"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "finding_id", "submission_id", name="uq_finding_submission"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<ResearchProductFindingLink finding={self.finding_id} "
            f"submission={self.submission_id}>"
        )


class ResearchProductFindingStatusTransition(db.Model):
    """Append-only status history for a product finding (RIP-003)."""

    __tablename__ = "research_product_finding_status_transitions"

    id: int = db.Column(db.Integer, primary_key=True)
    finding_id: int = db.Column(
        db.Integer,
        db.ForeignKey("research_product_findings.id"),
        nullable=False,
        index=True,
    )
    from_status: str | None = db.Column(db.String(32), nullable=True)
    to_status: str = db.Column(db.String(32), nullable=False)
    reviewer_user_id: int = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    rationale: str | None = db.Column(db.String(500), nullable=True)
    transitioned_at: datetime = db.Column(
        db.DateTime, nullable=False, default=_utc_now, index=True
    )

    finding = db.relationship(
        "ResearchProductFinding", back_populates="status_transitions"
    )
    reviewer = db.relationship("User", foreign_keys=[reviewer_user_id])

    def __repr__(self) -> str:
        return (
            f"<ResearchProductFindingStatusTransition id={self.id} "
            f"finding={self.finding_id} {self.from_status}->{self.to_status}>"
        )

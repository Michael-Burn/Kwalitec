"""Console global search (CONSOLE-001).

Future-ready discovery across Console domains. Presentation-only aggregation —
does not change educational behaviour, Twin state, or recommendation math.
"""

from __future__ import annotations

from dataclasses import dataclass

from flask import url_for
from sqlalchemy import or_

from app.extensions import db
from app.models.research_feedback import (
    ResearchFeedbackSubmission,
    ResearchProductFinding,
)
from app.models.user import User
from app.models.vision_journal import VisionEntry


@dataclass(frozen=True)
class ConsoleSearchHit:
    """One discoverable Console object."""

    domain: str
    title: str
    detail: str
    href: str


@dataclass(frozen=True)
class ConsoleSearchResult:
    """Grouped Console search response."""

    query: str
    hits: tuple[ConsoleSearchHit, ...]
    domains_searched: tuple[str, ...]


_DOMAINS: tuple[str, ...] = (
    "Students",
    "Support",
    "Content",
    "Platform",
    "Assessments",
    "Topics",
    "Questions",
)


class ConsoleSearchService:
    """Search Console operational objects by free-text query."""

    @staticmethod
    def search(query: str, *, limit_per_domain: int = 8) -> ConsoleSearchResult:
        """Return ranked hits across Console domains.

        Args:
            query: Free-text query (empty yields no hits).
            limit_per_domain: Cap per domain group.

        Returns:
            ConsoleSearchResult with zero or more hits.
        """
        q = (query or "").strip()
        if not q:
            return ConsoleSearchResult(
                query="",
                hits=(),
                domains_searched=_DOMAINS,
            )

        pattern = f"%{q}%"
        hits: list[ConsoleSearchHit] = []
        hits.extend(ConsoleSearchService._students(pattern, limit_per_domain))
        hits.extend(ConsoleSearchService._support(pattern, q, limit_per_domain))
        hits.extend(ConsoleSearchService._platform(pattern, limit_per_domain))
        # Content / Assessments / Topics / Questions reserved for future adapters.
        return ConsoleSearchResult(
            query=q,
            hits=tuple(hits),
            domains_searched=_DOMAINS,
        )

    @staticmethod
    def _students(pattern: str, limit: int) -> list[ConsoleSearchHit]:
        rows = (
            db.session.execute(
                db.select(User)
                .where(User.email.ilike(pattern))
                .order_by(User.email.asc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        return [
            ConsoleSearchHit(
                domain="Students",
                title=user.email,
                detail="Console participant",
                href=url_for("founder_dashboard.participants"),
            )
            for user in rows
        ]

    @staticmethod
    def _support(
        pattern: str, raw_query: str, limit: int
    ) -> list[ConsoleSearchHit]:
        hits: list[ConsoleSearchHit] = []
        submissions = (
            db.session.execute(
                db.select(ResearchFeedbackSubmission)
                .where(
                    or_(
                        ResearchFeedbackSubmission.feature_helped_most.ilike(
                            pattern
                        ),
                        ResearchFeedbackSubmission.friction_area.ilike(pattern),
                        ResearchFeedbackSubmission.experience_rating.ilike(
                            pattern
                        ),
                    )
                )
                .order_by(ResearchFeedbackSubmission.id.desc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        for sub in submissions:
            hits.append(
                ConsoleSearchHit(
                    domain="Support",
                    title=f"Check-in #{sub.id}",
                    detail=(sub.feature_helped_most or sub.friction_area or "")[
                        :120
                    ],
                    href=url_for(
                        "founder_dashboard.feedback", submission=sub.id
                    ),
                )
            )

        findings = (
            db.session.execute(
                db.select(ResearchProductFinding)
                .where(
                    or_(
                        ResearchProductFinding.title.ilike(pattern),
                        ResearchProductFinding.summary.ilike(pattern),
                    )
                )
                .order_by(ResearchProductFinding.id.desc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        for finding in findings:
            hits.append(
                ConsoleSearchHit(
                    domain="Support",
                    title=finding.title or f"Finding #{finding.id}",
                    detail=(finding.summary or "")[:120],
                    href=url_for(
                        "founder_dashboard.finding_detail",
                        finding_id=finding.id,
                    ),
                )
            )

        # Numeric id shortcuts for support objects.
        if raw_query.isdigit():
            sid = int(raw_query)
            sub = db.session.get(ResearchFeedbackSubmission, sid)
            if sub is not None:
                hits.insert(
                    0,
                    ConsoleSearchHit(
                        domain="Support",
                        title=f"Check-in #{sub.id}",
                        detail="Exact id match",
                        href=url_for(
                            "founder_dashboard.feedback", submission=sub.id
                        ),
                    ),
                )
            finding = db.session.get(ResearchProductFinding, sid)
            if finding is not None:
                hits.insert(
                    0,
                    ConsoleSearchHit(
                        domain="Support",
                        title=finding.title or f"Finding #{finding.id}",
                        detail="Exact id match",
                        href=url_for(
                            "founder_dashboard.finding_detail",
                            finding_id=finding.id,
                        ),
                    ),
                )
        return hits[: limit * 2]

    @staticmethod
    def _platform(pattern: str, limit: int) -> list[ConsoleSearchHit]:
        entries = (
            db.session.execute(
                db.select(VisionEntry)
                .where(
                    VisionEntry.deleted_at.is_(None),
                    or_(
                        VisionEntry.title.ilike(pattern),
                        VisionEntry.description.ilike(pattern),
                    ),
                )
                .order_by(VisionEntry.id.desc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        return [
            ConsoleSearchHit(
                domain="Platform",
                title=entry.title,
                detail=(entry.description or "")[:120],
                href=url_for(
                    "founder_dashboard.vision_entry", entry_id=entry.id
                ),
            )
            for entry in entries
        ]

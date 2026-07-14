"""FounderWeeklyBriefBuilder — assemble reporting cargo (FOS-007).

Constructs sections via templates and populates metadata.
No decision making. No scoring. Construction only.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from app.founder.briefing.config import RECOMMENDATION_VERSION, REPORT_VERSION
from app.founder.briefing.dto.validation import BriefingValidationError
from app.founder.briefing.models import BriefMetadata, FounderWeeklyBrief
from app.founder.briefing.providers import SectionTemplateProvider
from app.founder.briefing.validators import FounderWeeklyBriefValidator
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import RecommendationSet


class FounderWeeklyBriefBuilder:
    """Assemble an immutable FounderWeeklyBrief from state + recommendations."""

    def __init__(
        self,
        *,
        sections: SectionTemplateProvider | None = None,
        validator: FounderWeeklyBriefValidator | None = None,
        clock: Callable[[], datetime] | None = None,
        report_version: str = REPORT_VERSION,
        recommendation_version: str = RECOMMENDATION_VERSION,
    ) -> None:
        self._sections = sections or SectionTemplateProvider()
        self._validator = validator or FounderWeeklyBriefValidator(
            expected_report_version=report_version,
        )
        self._clock = clock or (lambda: datetime.now(UTC))
        self._report_version = report_version
        self._recommendation_version = recommendation_version

    def build(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
        *,
        generated_at: datetime | None = None,
        validate: bool = True,
    ) -> FounderWeeklyBrief:
        """Assemble and optionally validate a weekly briefing.

        Args:
            state: Immutable FounderOperationalState (FOS-005).
            recommendation_set: Immutable RecommendationSet (FOS-006).
            generated_at: Optional fixed timestamp (tests / replay).
            validate: When True, run structural validation and raise on failure.

        Returns:
            Immutable FounderWeeklyBrief.

        Raises:
            BriefingValidationError: When validate=True and validation fails.
            ValueError: When a section template returns an unexpected title/order.
        """
        stamp = generated_at or self._clock()
        sections = self._sections.build_sections(state, recommendation_set)
        by_order = {section.order: section for section in sections}

        metadata = BriefMetadata(
            generated_at=stamp,
            snapshot_version=state.snapshot_version,
            report_version=self._report_version,
        )

        brief = FounderWeeklyBrief(
            week=state.internal_alpha.current_week,
            generated_at=stamp,
            snapshot_version=state.snapshot_version,
            recommendation_version=self._recommendation_version,
            executive_summary=by_order[1],
            engineering_summary=by_order[2],
            internal_alpha_summary=by_order[3],
            capability_summary=by_order[4],
            release_summary=by_order[5],
            priorities=by_order[6],
            recommendations=by_order[7],
            risks=by_order[8],
            next_week_focus=by_order[9],
            metadata=metadata,
        )

        if validate:
            report = self._validator.validate(
                brief,
                state=state,
                recommendation_set=recommendation_set,
            )
            if not report.ok:
                raise BriefingValidationError(report)

        return brief

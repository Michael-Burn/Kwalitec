"""FounderWeeklyBriefingService — briefing coordinator (FOS-007).

Responsibilities:
1. Receive FounderOperationalState
2. Receive RecommendationSet
3. Build briefing
4. Validate briefing
5. Export outputs (when output_dir is provided)
6. Return immutable report

Coordinator only — no decision making, no AI, no subsystem access.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from app.founder.briefing.builders import FounderWeeklyBriefBuilder
from app.founder.briefing.dto import BriefingResult, BriefingValidationError
from app.founder.briefing.exporters import WeeklyBriefExportBundle
from app.founder.briefing.models import FounderWeeklyBrief
from app.founder.briefing.providers import SectionTemplateProvider
from app.founder.briefing.validators import FounderWeeklyBriefValidator
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import RecommendationSet


class FounderWeeklyBriefingService:
    """Produce an immutable FounderWeeklyBrief from state + recommendations."""

    def __init__(
        self,
        *,
        builder: FounderWeeklyBriefBuilder | None = None,
        validator: FounderWeeklyBriefValidator | None = None,
        exporters: WeeklyBriefExportBundle | None = None,
        sections: SectionTemplateProvider | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        resolved_sections = sections or SectionTemplateProvider()
        resolved_validator = validator or FounderWeeklyBriefValidator()
        self._builder = builder or FounderWeeklyBriefBuilder(
            sections=resolved_sections,
            validator=resolved_validator,
            clock=clock,
        )
        self._validator = resolved_validator
        self._exporters = exporters or WeeklyBriefExportBundle()

    def generate(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
        *,
        generated_at: datetime | None = None,
        output_dir: Path | str | None = None,
    ) -> BriefingResult:
        """Build, validate, optionally export, and return the weekly briefing.

        Args:
            state: Immutable FounderOperationalState (sole factual snapshot).
            recommendation_set: Immutable RecommendationSet (sole advisory input).
            generated_at: Optional fixed timestamp (tests / replay).
            output_dir: When set, write Markdown and JSON exports.

        Returns:
            BriefingResult with immutable FounderWeeklyBrief and optional exports.

        Raises:
            BriefingValidationError: When the assembled briefing fails validation.
        """
        # Build with validate=False so the service owns the raise path once.
        brief = self._builder.build(
            state,
            recommendation_set,
            generated_at=generated_at,
            validate=False,
        )
        report = self._validator.validate(
            brief,
            state=state,
            recommendation_set=recommendation_set,
        )
        if not report.ok:
            raise BriefingValidationError(report)

        exports = None
        if output_dir is not None:
            exports = self._exporters.export_all(output_dir, brief)

        return BriefingResult(brief=brief, exports=exports)

    def generate_brief(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
        *,
        generated_at: datetime | None = None,
        output_dir: Path | str | None = None,
    ) -> FounderWeeklyBrief:
        """Convenience wrapper returning only the immutable briefing."""
        return self.generate(
            state,
            recommendation_set,
            generated_at=generated_at,
            output_dir=output_dir,
        ).brief

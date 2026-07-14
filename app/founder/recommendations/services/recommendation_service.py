"""FounderRecommendationService — recommendation coordinator (FOS-006).

Responsibilities:
1. Receive FounderOperationalState
2. Execute RecommendationEngine
3. Validate RecommendationSet
4. Return immutable recommendations

Advisory only — no release automation, no AI, no subsystem re-queries.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import datetime

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.dto.validation import (
    RecommendationValidationError,
)
from app.founder.recommendations.evaluators import RecommendationEngine
from app.founder.recommendations.models import RecommendationSet
from app.founder.recommendations.providers import TemplateProvider
from app.founder.recommendations.rules import RecommendationRule
from app.founder.recommendations.validators import RecommendationSetValidator


class FounderRecommendationService:
    """Produce an immutable RecommendationSet from an operational snapshot."""

    def __init__(
        self,
        *,
        engine: RecommendationEngine | None = None,
        validator: RecommendationSetValidator | None = None,
        rules: Sequence[RecommendationRule] | None = None,
        templates: TemplateProvider | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        resolved_templates = templates or TemplateProvider()
        self._engine = engine or RecommendationEngine(
            rules=rules,
            templates=resolved_templates,
            clock=clock,
        )
        self._validator = validator or RecommendationSetValidator(
            templates=resolved_templates,
        )

    def recommend(self, state: FounderOperationalState) -> RecommendationSet:
        """Generate and validate recommendations for ``state``.

        Args:
            state: Immutable FounderOperationalState (sole input).

        Returns:
            Immutable RecommendationSet sorted by priority.

        Raises:
            RecommendationValidationError: When the assembled set fails
                structural validation.
            UnknownTemplateError: When a rule emits an unregistered template.
        """
        recommendation_set = self._engine.evaluate(state)
        report = self._validator.validate(recommendation_set)
        if not report.ok:
            raise RecommendationValidationError(report)
        return recommendation_set

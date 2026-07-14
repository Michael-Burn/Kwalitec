"""Section template provider for Founder Weekly Briefing (FOS-007)."""

from __future__ import annotations

from collections.abc import Sequence

from app.founder.briefing.config import SECTION_SPECS
from app.founder.briefing.models import BriefSection
from app.founder.briefing.providers.protocols import SectionBuilder
from app.founder.briefing.templates import SECTION_BUILDERS
from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.models import RecommendationSet


class SectionTemplateProvider:
    """Resolve and invoke predefined section template builders."""

    def __init__(
        self,
        *,
        builders: Sequence[SectionBuilder] | None = None,
        section_specs: tuple[tuple[int, str], ...] = SECTION_SPECS,
    ) -> None:
        self._builders: tuple[SectionBuilder, ...] = tuple(
            builders if builders is not None else SECTION_BUILDERS
        )
        self._section_specs = section_specs
        if len(self._builders) != len(self._section_specs):
            raise ValueError(
                "section builders count must match SECTION_SPECS "
                f"({len(self._builders)} != {len(self._section_specs)})"
            )

    def build_sections(
        self,
        state: FounderOperationalState,
        recommendation_set: RecommendationSet,
    ) -> tuple[BriefSection, ...]:
        """Build every Version 1 section in canonical order."""
        sections: list[BriefSection] = []
        for builder, (order, expected_title) in zip(
            self._builders, self._section_specs, strict=True
        ):
            section = builder(state, recommendation_set, order=order)
            if section.title != expected_title:
                raise ValueError(
                    f"section builder returned title {section.title!r}, "
                    f"expected {expected_title!r}"
                )
            if section.order != order:
                raise ValueError(
                    f"section {expected_title!r} order {section.order} "
                    f"!= expected {order}"
                )
            sections.append(section)
        return tuple(sections)

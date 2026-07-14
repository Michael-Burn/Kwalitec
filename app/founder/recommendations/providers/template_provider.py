"""Template provider — resolve template ids to wording (FOS-006)."""

from __future__ import annotations

from collections.abc import Mapping

from app.founder.recommendations.templates.catalog import (
    RECOMMENDATION_TEMPLATES,
    RecommendationTemplate,
)


class UnknownTemplateError(KeyError):
    """Raised when a rule references an unregistered template id."""

    def __init__(self, template_id: str) -> None:
        self.template_id = template_id
        super().__init__(f"unknown recommendation template: {template_id!r}")


class TemplateProvider:
    """Lookup predefined recommendation templates by id."""

    def __init__(
        self,
        templates: Mapping[str, RecommendationTemplate] | None = None,
    ) -> None:
        self._templates = dict(templates or RECOMMENDATION_TEMPLATES)

    def has(self, template_id: str) -> bool:
        """Return True when ``template_id`` is registered."""
        return template_id in self._templates

    def get(self, template_id: str) -> RecommendationTemplate:
        """Return the template for ``template_id``.

        Raises:
            UnknownTemplateError: When the id is not registered.
        """
        try:
            return self._templates[template_id]
        except KeyError as exc:
            raise UnknownTemplateError(template_id) from exc

    def known_ids(self) -> frozenset[str]:
        """Return the set of registered template ids."""
        return frozenset(self._templates)

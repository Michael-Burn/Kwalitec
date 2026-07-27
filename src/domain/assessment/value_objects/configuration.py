"""Assessment configuration and metadata value objects.

Architecture Source
    knowledge/product/AP-002/ASSESSMENT_LIFECYCLE.md
    knowledge/product/AP-002/QUESTION_MODEL.md
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from domain.assessment.enums import HintPolicy, RetryPolicy
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)


@dataclass(frozen=True, slots=True)
class AssessmentConfiguration(EducationalValueObject):
    """Session / instrument delivery configuration (evidence goals, not marks)."""

    time_budget_seconds: int | None = None
    hint_policy: HintPolicy = HintPolicy.AVAILABLE
    retry_policy: RetryPolicy = RetryPolicy.LIMITED
    max_retries: int | None = 1
    allow_pause: bool = True
    invite_confidence: bool = True
    require_confidence: bool = False
    one_item_at_a_time: bool = True

    def _validate(self) -> None:
        if self.time_budget_seconds is not None and (
            not isinstance(self.time_budget_seconds, int)
            or isinstance(self.time_budget_seconds, bool)
            or self.time_budget_seconds <= 0
        ):
            raise AssessmentInvariantViolation(
                "time_budget_seconds must be a positive integer when provided",
                invariant="AssessmentConfiguration.time_budget_seconds.range",
            )
        if not isinstance(self.hint_policy, HintPolicy):
            raise AssessmentInvariantViolation(
                "hint_policy must be a HintPolicy",
                invariant="AssessmentConfiguration.hint_policy.type",
            )
        if not isinstance(self.retry_policy, RetryPolicy):
            raise AssessmentInvariantViolation(
                "retry_policy must be a RetryPolicy",
                invariant="AssessmentConfiguration.retry_policy.type",
            )
        if self.retry_policy is RetryPolicy.LIMITED:
            if self.max_retries is None or (
                not isinstance(self.max_retries, int)
                or isinstance(self.max_retries, bool)
                or self.max_retries < 0
            ):
                raise AssessmentInvariantViolation(
                    "max_retries must be a non-negative integer "
                    "when retry_policy is limited",
                    invariant="AssessmentConfiguration.max_retries.required",
                )
        if self.require_confidence and not self.invite_confidence:
            raise AssessmentInvariantViolation(
                "require_confidence implies invite_confidence",
                invariant="AssessmentConfiguration.confidence.consistent",
            )


@dataclass(frozen=True, slots=True)
class AssessmentMetadata(EducationalValueObject):
    """Immutable audit / catalogue metadata for instruments and sessions."""

    version: str
    title: str
    description: str | None = None
    author_id: str | None = None
    locale: str | None = None
    tags: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = MappingProxyType({})

    def _validate(self) -> None:
        object.__setattr__(
            self, "version", require_identity_value(self.version, "version")
        )
        object.__setattr__(self, "title", require_non_empty_text(self.title, "title"))
        if self.description is not None:
            object.__setattr__(
                self,
                "description",
                require_non_empty_text(self.description, "description"),
            )
        if self.author_id is not None:
            object.__setattr__(
                self,
                "author_id",
                require_identity_value(self.author_id, "author_id"),
            )
        if self.locale is not None:
            object.__setattr__(
                self, "locale", require_non_empty_text(self.locale, "locale")
            )
        cleaned_tags: list[str] = []
        for tag in self.tags or ():
            cleaned_tags.append(require_non_empty_text(str(tag), "tag"))
        object.__setattr__(self, "tags", tuple(cleaned_tags))
        object.__setattr__(
            self, "attributes", MappingProxyType(dict(self.attributes or {}))
        )

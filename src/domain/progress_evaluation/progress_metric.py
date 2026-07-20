"""ProgressMetric — named explainable progress measurement.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Progress Metric
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.enums import ProgressMetricCode


@dataclass(frozen=True, slots=True)
class ProgressMetric(EducationalValueObject):
    """Immutable named progress measurement with an educational explanation.

    ``value_millipoints`` is a signed integer scale (−1000…1000) so metrics stay
    deterministic and free of floating-point drift. Qualitative ``band`` carries
    the human-readable classification for the report.
    """

    code: ProgressMetricCode
    label: str
    value_millipoints: int
    band: str
    explanation: str

    def _validate(self) -> None:
        if not isinstance(self.code, ProgressMetricCode):
            raise EducationalInvariantViolation(
                "code must be a ProgressMetricCode",
                invariant="ProgressMetric.code.type",
            )
        object.__setattr__(
            self,
            "label",
            require_non_empty_text(self.label, "label"),
        )
        if not isinstance(self.value_millipoints, int) or isinstance(
            self.value_millipoints, bool
        ):
            raise EducationalInvariantViolation(
                "value_millipoints must be an integer",
                invariant="ProgressMetric.value_millipoints.type",
            )
        if self.value_millipoints < -1000 or self.value_millipoints > 1000:
            raise EducationalInvariantViolation(
                "value_millipoints must be between -1000 and 1000 inclusive",
                invariant="ProgressMetric.value_millipoints.range",
            )
        object.__setattr__(
            self,
            "band",
            require_non_empty_text(self.band, "band"),
        )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )

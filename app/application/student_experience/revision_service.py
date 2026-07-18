"""RevisionService — Revision experience from Adaptive Decision only."""

from __future__ import annotations

from typing import Any

from app.application.student_experience._snapshots import revision_snapshot
from app.application.student_experience.dto.revision_snapshot import RevisionSnapshot
from app.application.student_experience.exceptions import (
    PortUnavailable,
    RevisionError,
)
from app.application.student_experience.explanation_service import (
    ExplanationService,
)
from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.domain.student_experience.recommendation_explanation import (
    translate_to_student_language,
)
from app.domain.student_experience.revision_projection import (
    RevisionOption,
    RevisionProjection,
)


class RevisionService:
    """Project Revision from Adaptive Decision outputs only.

    Does not calculate revision priority or educational ROI.
    """

    def __init__(
        self,
        *,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        explanation: ExplanationService | None = None,
    ) -> None:
        self._adaptive = adaptive_decision
        self._explanation = explanation or ExplanationService(
            adaptive_decision=adaptive_decision
        )

    def revision(self, student_id: str) -> RevisionSnapshot:
        """Build the Revision projection for ``student_id``."""
        sid = _require_id(student_id)
        port = self._require_adaptive()
        options = port.get_revision_options(sid)
        if not options:
            return revision_snapshot(RevisionProjection.create(sid))

        primary_raw, *rest = options
        try:
            primary = _option(primary_raw, self._explanation, is_primary=True)
            alternatives = tuple(
                _option(raw, self._explanation, is_primary=False) for raw in rest
            )
            projection = RevisionProjection.create(
                sid, primary=primary, alternatives=alternatives
            )
        except ValueError as exc:
            raise RevisionError(str(exc)) from exc
        return revision_snapshot(projection)

    def _require_adaptive(self) -> AdaptiveDecisionPort:
        if self._adaptive is None or not self._adaptive.is_available():
            raise PortUnavailable("adaptive_decision port unavailable")
        return self._adaptive


def _option(
    raw: dict[str, Any],
    explanation_service: ExplanationService,
    *,
    is_primary: bool,
) -> RevisionOption:
    expl_payload = raw.get("explanation")
    explanation = None
    if isinstance(expl_payload, dict):
        explanation = explanation_service.from_opaque(expl_payload)
    elif raw.get("rationale") or raw.get("expected_benefit"):
        explanation = explanation_service.from_opaque(raw)
    return RevisionOption.create(
        str(raw.get("option_id") or raw.get("id") or raw.get("decision_id") or "rev"),
        translate_to_student_language(
            str(raw.get("topic_title") or raw.get("title") or "Revision")
        ),
        priority_label=translate_to_student_language(
            str(raw.get("priority_label") or raw.get("priority_band") or "")
        ),
        estimated_study_minutes=_optional_int(raw.get("estimated_minutes")),
        expected_benefit=translate_to_student_language(
            str(
                raw.get("expected_benefit")
                or raw.get("expected_educational_benefit")
                or ""
            )
        ),
        explanation=explanation,
        is_primary=is_primary,
    )


def _require_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RevisionError("student_id must be a non-empty string")
    return value.strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)

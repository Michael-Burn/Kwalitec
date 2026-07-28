"""RevisionService — Revision experience (Preferred Authority when available).

VP-001 / RI-001: prefer Educational Intelligence Experience Models via
Runtime Integration. Adaptive Decision remains Temporary compatibility.
Does not calculate revision priority or educational ROI.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.educational_state import EducationalStateService
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

logger = logging.getLogger(__name__)


class RevisionService:
    """Project Revision from Preferred Authority or Adaptive Decision.

    Does not calculate revision priority or educational ROI.
    """

    def __init__(
        self,
        *,
        adaptive_decision: AdaptiveDecisionPort | None = None,
        explanation: ExplanationService | None = None,
        educational_state: EducationalStateService | None = None,
    ) -> None:
        self._adaptive = adaptive_decision
        self._educational_state = educational_state
        self._explanation = explanation or ExplanationService(
            adaptive_decision=adaptive_decision
        )

    def revision(self, student_id: str) -> RevisionSnapshot:
        """Build the Revision projection for ``student_id``."""
        sid = _require_id(student_id)
        options = self._options_for(sid)
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

    def _options_for(self, student_id: str) -> list[dict[str, Any]]:
        ei_options = _try_educational_intelligence_revision(student_id)
        if ei_options is not None:
            return ei_options
        if self._educational_state is not None:
            state = self._educational_state.load(student_id)
            if not state.adaptive_available:
                raise PortUnavailable("adaptive_decision port unavailable")
            return list(state.revision_options)
        port = self._require_adaptive()
        return list(port.get_revision_options(student_id) or ())

    def _require_adaptive(self) -> AdaptiveDecisionPort:
        if self._adaptive is None or not self._adaptive.is_available():
            raise PortUnavailable("adaptive_decision port unavailable")
        return self._adaptive


def _try_educational_intelligence_revision(
    student_id: str,
) -> list[dict[str, Any]] | None:
    """Return Revision Planner options from RIS when Preferred Authority wins."""
    try:
        user_id = int(str(student_id).strip())
    except (TypeError, ValueError):
        return None
    try:
        from app.application.runtime_integration import (
            AuthoritySource,
            build_runtime_integration_service,
            map_revision_entry,
        )
        from app.application.runtime_integration.dto import IntegrationSurface

        result = build_runtime_integration_service().resolve_for_surface(
            user_id,
            IntegrationSurface.REVISION_PLANNER,
            runtime_a_fallback=lambda _sid, _surface: None,
        )
        if result.authority is not AuthoritySource.EDUCATIONAL_INTELLIGENCE:
            return None
        if result.experience is None:
            return None
        mapped = map_revision_entry(result.experience.surfaces.revision_entry)
        return [
            {
                "option_id": mapped.get("decision_id") or mapped.get("experience_id"),
                "decision_id": mapped.get("decision_id"),
                "title": mapped.get("entry_title") or mapped.get("title"),
                "topic_title": mapped.get("entry_title") or mapped.get("title"),
                "priority_label": mapped.get("urgency") or "Priority revision",
                "estimated_minutes": mapped.get("estimated_minutes"),
                "expected_benefit": mapped.get("expected_outcome") or "",
                "rationale": mapped.get("educational_why") or mapped.get("summary"),
                "explanation": {
                    "rationale": mapped.get("educational_why") or "",
                    "expected_benefit": mapped.get("expected_outcome") or "",
                    "source_authority": mapped.get("source_authority"),
                },
                "authority": mapped.get("authority"),
                "source_authority": mapped.get("source_authority"),
            }
        ]
    except Exception:  # noqa: BLE001 — Temporary compatibility
        logger.debug(
            "VP-001 revision Preferred Authority unavailable for student=%s",
            student_id,
            exc_info=True,
        )
        return None


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

"""ExplanationService — student-safe recommendation explanations."""

from __future__ import annotations

from typing import Any

from app.application.student_experience._snapshots import explanation_snapshot
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.exceptions import (
    ExplanationError,
    PortUnavailable,
)
from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.domain.student_experience.recommendation_explanation import (
    RecommendationExplanation,
    build_explanation,
    translate_to_student_language,
)


class ExplanationService:
    """Translate Adaptive Decision evidence into student explanations.

    Owns presentation wording only. Never calculates educational signals.
    """

    def __init__(
        self, *, adaptive_decision: AdaptiveDecisionPort | None = None
    ) -> None:
        self._adaptive = adaptive_decision

    def explain_recommendation(
        self,
        student_id: str,
        *,
        decision_id: str | None = None,
        fallback: dict[str, Any] | None = None,
    ) -> ExplanationSnapshot:
        """Build today's recommendation explanation for ``student_id``."""
        payload = fallback
        if payload is None:
            port = self._require_adaptive()
            payload = port.get_decision_explanation(
                student_id, decision_id=decision_id
            )
        if not payload:
            raise ExplanationError(
                f"no explanation available for student {student_id!r}"
            )
        domain = self.from_opaque(payload)
        snap = explanation_snapshot(domain)
        assert snap is not None
        return snap

    def from_opaque(self, payload: dict[str, Any]) -> RecommendationExplanation:
        """Map an opaque Adaptive Decision explanation payload."""
        topic = str(
            payload.get("topic_title")
            or payload.get("title")
            or payload.get("topic")
            or ""
        )
        reason_codes = payload.get("reason_codes") or payload.get("reasons") or ()
        evidence = (
            payload.get("evidence_points")
            or payload.get("evidence_considered")
            or payload.get("evidence_phrases")
            or ()
        )
        return build_explanation(
            topic_title=translate_to_student_language(topic),
            reason_codes=tuple(str(c) for c in reason_codes),
            evidence_phrases=tuple(
                translate_to_student_language(str(p)) for p in evidence
            ),
            expected_benefit=str(
                payload.get("expected_benefit")
                or payload.get("expected_educational_benefit")
                or ""
            ),
            priority_band=str(
                payload.get("priority_band") or payload.get("priority") or ""
            ),
            confidence=str(payload.get("confidence") or ""),
        )

    def _require_adaptive(self) -> AdaptiveDecisionPort:
        if self._adaptive is None or not self._adaptive.is_available():
            raise PortUnavailable("adaptive_decision port unavailable")
        return self._adaptive

"""ExplanationService — student-safe recommendation explanations.

EP-006.2: prefer authored Runtime A MES fields; reason-code synthesis is
fallback only when the payload is schema-incomplete.

EP-008.1: map trust fields (coherence, refusal, timeliness, completion loop)
from authored fragments — presentation composition only.
"""

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
from app.application.student_experience.recommendation_trust import (
    compose_completion_loop_line,
    compose_timeliness_line,
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

    def from_opaque(
        self,
        payload: dict[str, Any],
        *,
        exam_countdown_days: int | None = None,
    ) -> RecommendationExplanation:
        """Map an opaque Adaptive Decision / Runtime A explanation payload.

        When authored MES keys are present (``why_recommended``, supporting
        evidence, next action, …), pass them through. Reason-code re-narration
        applies only for incomplete / cold-start payloads.
        """
        view = _flatten_explanation_payload(payload)
        topic = str(
            view.get("topic_title")
            or view.get("title")
            or view.get("topic")
            or ""
        )
        evidence = _evidence_phrases(view)
        confidence = str(
            view.get("confidence_level")
            or view.get("confidence")
            or view.get("confidence_label")
            or ""
        )
        next_action = str(
            view.get("suggested_next_action")
            or view.get("next_action")
            or ""
        )
        review_point = str(view.get("review_point") or "")
        confidence_basis = str(
            view.get("confidence_basis")
            or view.get("confidence_rationale")
            or ""
        )
        authored_why = str(view.get("why_recommended") or "").strip()
        authored_summary = str(
            view.get("summary")
            or view.get("explanation_summary")
            or ""
        ).strip()
        plan_coherence = str(view.get("plan_coherence") or "").strip()
        plan_coherence_label = str(
            view.get("plan_coherence_label") or ""
        ).strip()
        honest_refusal = bool(view.get("honest_refusal"))
        authored_reason = str(view.get("reason") or "").strip()
        category = str(view.get("category") or "").strip()

        # Schema-complete or authored-why path: no reason-code rewrite.
        if authored_why or _looks_schema_complete(view) or honest_refusal:
            reason_codes: tuple[str, ...] = ()
        else:
            reason_codes = tuple(
                str(c)
                for c in (
                    view.get("reason_codes") or view.get("reasons") or ()
                )
            )

        timeliness = compose_timeliness_line(
            reason=authored_reason,
            why_recommended=authored_why,
            category=category,
            plan_coherence_label=plan_coherence_label,
            plan_coherence=plan_coherence,
            exam_countdown_days=exam_countdown_days,
            honest_refusal=honest_refusal,
        )
        completion_loop = compose_completion_loop_line(
            review_point=review_point
        )

        return build_explanation(
            topic_title=translate_to_student_language(topic),
            reason_codes=reason_codes,
            evidence_phrases=evidence,
            expected_benefit=str(
                view.get("expected_benefit")
                or view.get("expected_educational_benefit")
                or ""
            ),
            priority_band=str(
                view.get("priority_band") or view.get("priority") or ""
            ),
            confidence=confidence,
            suggested_next_action=next_action,
            review_point=review_point,
            confidence_basis=confidence_basis,
            why_recommended=authored_why,
            summary=authored_summary,
            plan_coherence=plan_coherence,
            plan_coherence_label=plan_coherence_label,
            honest_refusal=honest_refusal,
            timeliness_line=timeliness,
            completion_loop_line=completion_loop,
        )

    def _require_adaptive(self) -> AdaptiveDecisionPort:
        if self._adaptive is None or not self._adaptive.is_available():
            raise PortUnavailable("adaptive_decision port unavailable")
        return self._adaptive


def _flatten_explanation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Merge nested ``explanation`` dict under top-level keys (top wins)."""
    nested = payload.get("explanation")
    if not isinstance(nested, dict):
        return dict(payload)
    merged = {**nested}
    for key, value in payload.items():
        if key == "explanation":
            continue
        if value is None or value == "" or value == () or value == []:
            continue
        merged[key] = value
    if "honest_refusal" in payload:
        merged["honest_refusal"] = bool(payload.get("honest_refusal"))
    return merged


def _evidence_phrases(view: dict[str, Any]) -> tuple[str, ...]:
    raw = (
        view.get("supporting_evidence")
        or view.get("evidence_points")
        or view.get("evidence_considered")
        or view.get("evidence_phrases")
        or view.get("observed_facts")
        or ()
    )
    if isinstance(raw, str):
        text = raw.strip()
        return (translate_to_student_language(text),) if text else ()
    return tuple(
        translate_to_student_language(str(p))
        for p in raw
        if str(p).strip()
    )


def _looks_schema_complete(view: dict[str, Any]) -> bool:
    """True when the explanation payload carries the full authored schema.

    Mirrors ``app.services.recommendation_quality.has_complete_explanation_schema``
    (a pure dict predicate) inline — presentation composition must not import
    services.
    """
    if _has_complete_explanation_schema(view):
        return True
    return bool(
        str(view.get("why_recommended") or "").strip()
        and (
            view.get("supporting_evidence")
            or view.get("suggested_next_action")
            or view.get("next_action")
        )
    )


def _has_complete_explanation_schema(row: dict[str, Any]) -> bool:
    """True when a recommendation row carries the mandatory explanation schema."""
    if not isinstance(row, dict):
        return False
    if row.get("honest_refusal"):
        return all(
            str(row.get(key) or "").strip()
            for key in (
                "title",
                "reason",
                "confidence_level",
                "why_recommended",
                "suggested_next_action",
            )
        )
    required = (
        "title",
        "reason",
        "expected_benefit",
        "confidence_level",
        "why_recommended",
        "suggested_next_action",
        "supporting_evidence",
        "explanation_schema_version",
    )
    for key in required:
        value = row.get(key)
        if value is None:
            return False
        if isinstance(value, list | tuple) and len(value) == 0:
            return False
        if isinstance(value, str) and not value.strip():
            return False
    return True

"""Unified Runtime A presentation adapter (EP-002.8).

Selects a single communication source per ``source_authority``:

* Schema-complete readiness / recommendation / planning surfaces → pass-through
  fields already authorised by ``ReadinessService`` / ``RecommendationService``
  / ``PlanningService`` (EP-003.1 / EP-003.2 / EP-003.3)
* Twin-served surfaces → projection fields already authorised by Consumer Chain
* Legacy / fail-open → ``EducationalExplainabilityService`` (EIP-003 adapter)

Does not evaluate readiness, generate plans, or invent educational certainty.
"""

from __future__ import annotations

from typing import Any

from app.application.student_experience.dto.readiness_explanation_snapshot import (
    ReadinessExplanationSnapshot,
)
from app.application.student_experience.readiness_explanation import (
    bind_readiness_surface_port,
    readiness_explanation_from_narrative,
)
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
    MissionNarrative,
    ReadinessNarrative,
)

SOURCE_AUTHORITY_LEGACY = "legacy"
SOURCE_AUTHORITY_STUDY_INSIGHTS = "study_insights"
SOURCE_AUTHORITY_READINESS_INTELLIGENCE = "readiness_intelligence"
SOURCE_AUTHORITY_DAILY_STUDY_PLAN = "daily_study_plan"

_TWIN_MISSION_REASON_FALLBACK = "Projected from Twin daily study plan"
_TWIN_MISSION_PURPOSE_FALLBACK = "Follow today's Adaptive Study Planner focus"


def _authority(surface: dict[str, Any] | None) -> str:
    if not isinstance(surface, dict):
        return SOURCE_AUTHORITY_LEGACY
    return str(surface.get("source_authority") or SOURCE_AUTHORITY_LEGACY).strip() or (
        SOURCE_AUTHORITY_LEGACY
    )


def _driver_evidence(drivers: Any) -> list[str]:
    """Student-safe driver labels (prefer ``label`` over internal ids)."""
    if not isinstance(drivers, list):
        return []
    lines: list[str] = []
    for driver in drivers:
        if isinstance(driver, str) and driver.strip():
            lines.append(driver.strip())
            continue
        if not isinstance(driver, dict):
            continue
        label = str(
            driver.get("label") or driver.get("driver_id") or ""
        ).strip()
        if not label:
            continue
        label = label.replace("_", " ")
        value = driver.get("value")
        if value is None:
            lines.append(label)
            continue
        try:
            pct = int(round(float(value)))
            lines.append(f"{label} (~{pct}%)")
        except (TypeError, ValueError):
            lines.append(label)
    return lines


def _action_texts(actions: Any) -> list[str]:
    if not isinstance(actions, list):
        return []
    texts: list[str] = []
    for action in actions:
        if isinstance(action, str) and action.strip():
            texts.append(action.strip())
            continue
        if not isinstance(action, dict):
            continue
        for key in ("title", "action", "text", "label"):
            value = action.get(key)
            if value is not None and str(value).strip():
                texts.append(str(value).strip())
                break
    return texts


class RuntimeAPresentationAdapter:
    """Constitutionally governed presentation selection for Runtime A HTTP."""

    @staticmethod
    def topic_rows(
        surface: dict[str, Any] | None,
        *,
        weak_key: str = "weakest_topics",
        strong_key: str = "strongest_topics",
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Return topic highlight rows without re-narrating Twin areas."""
        surface = surface if isinstance(surface, dict) else {}
        weak = list(surface.get(weak_key) or [])
        strong = list(surface.get(strong_key) or [])
        if _authority(surface) == SOURCE_AUTHORITY_READINESS_INTELLIGENCE:
            return weak, strong
        return (
            EducationalExplainabilityService.enrich_topic_rows(weak),
            EducationalExplainabilityService.enrich_topic_rows(strong),
        )

    @staticmethod
    def readiness_narrative(
        surface: dict[str, Any] | None,
    ) -> ReadinessNarrative:
        """Compose readiness speech from schema-complete surface, Twin, or EIP-003.

        EP-003.2: when ``ReadinessService`` already attached the mandatory
        explanation schema, presentation must not re-evaluate or invent drivers.
        """
        surface = surface if isinstance(surface, dict) else {}
        from app.services.readiness_quality import (
            has_complete_readiness_explanation_schema,
        )

        if has_complete_readiness_explanation_schema(surface):
            return RuntimeAPresentationAdapter._schema_readiness_narrative(surface)

        raw_readiness = surface.get("readiness")
        readiness = raw_readiness if isinstance(raw_readiness, dict) else {}
        if _authority(surface) != SOURCE_AUTHORITY_READINESS_INTELLIGENCE:
            return EducationalExplainabilityService.explain_composite_readiness(
                readiness
            )
        return RuntimeAPresentationAdapter._twin_readiness_narrative(surface)

    @staticmethod
    def _schema_readiness_narrative(surface: dict[str, Any]) -> ReadinessNarrative:
        """Pass-through student speech from ReadinessService quality schema."""
        from app.services.product_communication_service import (
            ProductCommunicationService,
        )

        raw_readiness = surface.get("readiness")
        readiness = raw_readiness if isinstance(raw_readiness, dict) else {}
        score_raw = readiness.get("score")
        try:
            score = float(score_raw) if score_raw is not None else None
        except (TypeError, ValueError):
            score = None

        if surface.get("honest_refusal") or score is None:
            explanation = str(
                surface.get("explanation_summary")
                or surface.get("why_this_estimate")
                or ProductCommunicationService.READINESS_UNAVAILABLE
            ).strip()
            evidence_list = [
                str(item).strip()
                for item in (surface.get("supporting_evidence") or [])
                if str(item).strip()
            ]
            evidence = " ".join(evidence_list) or str(
                surface.get("why_this_estimate") or ""
            ).strip()
            drivers = tuple(_driver_evidence(surface.get("readiness_drivers"))[:4])
            return ReadinessNarrative(
                label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
                percentage=None,
                explanation=explanation,
                evidence_basis=evidence
                or ProductCommunicationService.READINESS_UNAVAILABLE_BASIS,
                can_estimate=False,
                is_estimate=True,
                readiness_drivers=drivers,
                review_point=str(surface.get("review_point") or "").strip(),
                expected_benefit=str(surface.get("expected_benefit") or "").strip(),
                supporting_evidence=tuple(evidence_list[:5]),
                suggested_next_action=str(
                    surface.get("suggested_next_action") or ""
                ).strip(),
                why_this_estimate=str(surface.get("why_this_estimate") or "").strip(),
                confidence_label=str(surface.get("confidence_level") or "").strip(),
                confidence_basis=str(surface.get("confidence_basis") or "").strip(),
            )

        why = str(
            surface.get("why_this_estimate")
            or surface.get("explanation_summary")
            or ""
        ).strip()
        explanation = why
        if not explanation:
            explanation = (
                f"Estimated readiness is about {int(round(score))}%. "
                "This is a provisional study-preparation judgement."
            )
        next_action = str(surface.get("suggested_next_action") or "").strip()
        if next_action and next_action not in explanation:
            explanation = f"{explanation} Suggested focus: {next_action}."

        evidence_parts = [
            str(item).strip()
            for item in (surface.get("supporting_evidence") or [])
            if str(item).strip()
        ]
        drivers = tuple(_driver_evidence(surface.get("readiness_drivers"))[:4])
        confidence = str(surface.get("confidence_level") or "").strip()
        if confidence:
            evidence_parts.append(f"Confidence level: {confidence}.")
        change = str(surface.get("change_reasoning") or "").strip()
        if change:
            evidence_parts.append(change)
        evidence_parts.append(
            ProductCommunicationService.ESTIMATED_READINESS_SELF_REPORT
        )
        review_point = str(surface.get("review_point") or "").strip()

        return ReadinessNarrative(
            label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
            percentage=float(int(round(score))),
            explanation=explanation,
            evidence_basis=" ".join(evidence_parts),
            can_estimate=True,
            is_estimate=True,
            readiness_drivers=drivers,
            review_point=review_point,
            expected_benefit=str(surface.get("expected_benefit") or "").strip(),
            supporting_evidence=tuple(
                str(item).strip()
                for item in (surface.get("supporting_evidence") or [])
                if str(item).strip()
            )[:5],
            suggested_next_action=next_action,
            why_this_estimate=why,
            confidence_label=confidence,
            confidence_basis=str(surface.get("confidence_basis") or "").strip(),
        )

    @staticmethod
    def _twin_readiness_narrative(surface: dict[str, Any]) -> ReadinessNarrative:
        from app.services.product_communication_service import (
            ProductCommunicationService,
        )

        raw_readiness = surface.get("readiness")
        readiness = raw_readiness if isinstance(raw_readiness, dict) else {}
        score_raw = readiness.get("score")
        try:
            score = float(score_raw) if score_raw is not None else None
        except (TypeError, ValueError):
            score = None

        if score is None:
            return ReadinessNarrative(
                label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
                percentage=None,
                explanation=ProductCommunicationService.READINESS_UNAVAILABLE,
                evidence_basis=(
                    "Twin readiness assessment did not supply a score. "
                    + ProductCommunicationService.READINESS_UNAVAILABLE_BASIS
                ),
                can_estimate=False,
                is_estimate=True,
            )

        driver_lines = _driver_evidence(surface.get("readiness_drivers"))
        confidence = str(
            surface.get("confidence_level")
            or readiness.get("confidence_level")
            or ""
        ).strip()
        actions = _action_texts(surface.get("recommended_next_actions"))

        evidence_parts = [
            "Based on Twin readiness intelligence drivers"
            + (f": {'; '.join(driver_lines)}." if driver_lines else "."),
        ]
        if confidence:
            evidence_parts.append(f"Confidence level: {confidence}.")
        evidence_parts.append(
            ProductCommunicationService.ESTIMATED_READINESS_SELF_REPORT
        )

        explanation = (
            f"Estimated readiness is about {int(round(score))}%. "
            "This is a provisional study-preparation judgement from readiness "
            "intelligence — not proof that the syllabus is fully understood."
        )
        if actions:
            explanation = f"{explanation} Suggested focus: {actions[0]}."

        return ReadinessNarrative(
            label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
            percentage=float(int(round(score))),
            explanation=explanation,
            evidence_basis=" ".join(evidence_parts),
            can_estimate=True,
            is_estimate=True,
            readiness_drivers=tuple(driver_lines[:4]),
            review_point=str(surface.get("review_point") or "").strip(),
            expected_benefit=str(surface.get("expected_benefit") or "").strip(),
            supporting_evidence=tuple(driver_lines[:4]),
            suggested_next_action=actions[0] if actions else "",
            why_this_estimate=explanation,
            confidence_label=confidence,
            confidence_basis=str(surface.get("confidence_basis") or "").strip(),
        )

    @staticmethod
    def enrich_recommendations_if_needed(
        recommendations: list[dict[str, Any]] | None,
        *,
        today_recommendation: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
        """Enrich legacy recommendation rows; pass through schema-complete rows.

        EP-003.1: when ``RecommendationService`` already attached the mandatory
        explanation schema, presentation must not re-narrate or re-rank.
        Study Insights projections remain pass-through.

        EP-004.2: personalisation evidence fields (``personalisation_applied``,
        ``personalisation_factors``, session sizing notes) are authored by
        RecommendationService and must pass through unchanged. Presentation
        must not inspect the Personal Learning Profile or invent ranking.
        """
        from app.services.recommendation_quality import has_complete_explanation_schema

        rows = list(recommendations or [])
        study_insights_active = bool(
            rows and rows[0].get("source_authority") == SOURCE_AUTHORITY_STUDY_INSIGHTS
        )
        schema_complete = bool(
            rows and all(has_complete_explanation_schema(row) for row in rows)
        )
        if study_insights_active or schema_complete:
            return today_recommendation, rows

        enrich = EducationalExplainabilityService.enrich_recommendations
        enriched_today = None
        if today_recommendation:
            if has_complete_explanation_schema(today_recommendation):
                enriched_today = today_recommendation
            else:
                enriched = enrich([today_recommendation])
                enriched_today = enriched[0] if enriched else None
        return enriched_today, enrich(rows)

    @staticmethod
    def mission_narrative(
        *,
        today_mission: Any,
        mission_surface: dict[str, Any] | None,
        exam_name: str | None = None,
        completed_topics: int | None = None,
        total_topics: int | None = None,
        syllabus_coverage_pct: float | None = None,
        is_revision: bool = False,
    ) -> MissionNarrative | None:
        """Build mission narrative from schema-complete plan, Twin, or EIP-003.

        EP-003.3: when ``PlanningService`` already attached the mandatory
        explanation schema, presentation must not re-plan or invent rationale.

        EP-004.3: personalisation evidence fields (``personalisation_applied``,
        ``personalisation_factors``, session sizing notes) are authored by
        PlanningService and must pass through unchanged. Presentation must not
        inspect the Personal Learning Profile or invent plan adaptations.
        """
        if today_mission is None:
            return None

        surface = mission_surface if isinstance(mission_surface, dict) else {}
        from app.services.planning_quality import has_complete_plan_explanation_schema

        if has_complete_plan_explanation_schema(surface):
            return RuntimeAPresentationAdapter._schema_mission_narrative(
                today_mission=today_mission,
                mission_surface=surface,
                is_revision=is_revision,
            )

        if _authority(surface) == SOURCE_AUTHORITY_DAILY_STUDY_PLAN:
            return RuntimeAPresentationAdapter._twin_mission_narrative(
                today_mission=today_mission,
                mission_surface=surface,
            )

        return EducationalExplainabilityService.build_mission_narrative(
            mission_title=today_mission.title,
            mission_status=today_mission.status,
            exam_name=exam_name,
            completed_topics=completed_topics,
            total_topics=total_topics,
            syllabus_coverage_pct=syllabus_coverage_pct,
            is_revision=is_revision,
        )

    @staticmethod
    def _schema_mission_narrative(
        *,
        today_mission: Any,
        mission_surface: dict[str, Any],
        is_revision: bool = False,
    ) -> MissionNarrative:
        """Pass-through student speech from PlanningService quality schema.

        EIP-003 / IA-004: even pass-through surfaces must keep the Learning
        Mode / Current Learning Topic story that anchors the student's
        educational mental model. Presentation only appends this fixed
        framing sentence — it never re-plans or overrides authored fields.
        """
        title = (
            str(getattr(today_mission, "title", "") or "").strip()
            or "Today's focus"
        )
        judgement = str(mission_surface.get("judgement") or "").strip()
        if not str(getattr(today_mission, "title", "") or "").strip() and judgement:
            prefix = "Today's plan: "
            title = (
                judgement.removeprefix(prefix).strip()
                if judgement.startswith(prefix)
                else judgement
            ) or title
        why = str(
            mission_surface.get("why_this_plan")
            or mission_surface.get("explanation_summary")
            or _TWIN_MISSION_REASON_FALLBACK
        ).strip()
        is_consolidation = (not is_revision) and title.lower().startswith(
            "consolidate"
        )
        if is_revision:
            mode_sentence = (
                "In Revision Mode, today's mission consolidates the completed "
                "syllabus — not new Current Learning Topic coverage."
            )
        elif is_consolidation:
            mode_sentence = (
                "In Learning Mode, today's mission is a disclosed consolidation "
                "checkpoint on a weak covered topic — not continued forward "
                "syllabus progress, and not Revision Mode."
            )
        else:
            mode_sentence = (
                "In Learning Mode, today's mission follows your Current "
                "Learning Topic in this study plan."
            )
        why_with_mode = f"{why} {mode_sentence}".strip()
        next_action = str(
            mission_surface.get("suggested_next_action")
            or mission_surface.get("next_action")
            or title
        ).strip()
        evidence = [
            str(item).strip()
            for item in (mission_surface.get("supporting_evidence") or [])
            if str(item).strip()
        ]
        if is_revision:
            evidence.append(
                "Study Progress advances one syllabus topic at a time in "
                "Revision Mode."
            )
        elif is_consolidation:
            evidence.append(
                "This Learning Mode consolidation checkpoint revisits covered "
                "material; it does not advance new Current Learning Topic coverage."
            )
        else:
            evidence.append(
                "Study Progress advances one syllabus topic at a time in "
                "Learning Mode."
            )
        confidence = str(mission_surface.get("confidence_level") or "").strip()
        estimates: list[str] = []
        if confidence:
            estimates.append(confidence)
        change = str(mission_surface.get("change_reasoning") or "").strip()
        if change:
            estimates.append(change)
        if is_revision:
            estimates.append(
                "Revision consolidates completed material — it does not invent "
                "Estimated Knowledge."
            )
        elif is_consolidation:
            estimates.append(
                "Consolidation checkpoints reinforce weak Estimated Knowledge "
                "on covered topics before returning to Current Learning Topic."
            )
        else:
            estimates.append(
                "Estimated Knowledge is separate from Study Progress and "
                "grows from practice results over time."
            )
        plan_drivers = tuple(
            _driver_evidence(mission_surface.get("plan_drivers"))[:3]
        )
        review_point = str(mission_surface.get("review_point") or "").strip()
        expected_benefit = str(
            mission_surface.get("expected_benefit") or ""
        ).strip()

        return MissionNarrative(
            topic_title=title,
            educational_purpose=why_with_mode,
            reason_for_selection=why_with_mode,
            educational_position=str(
                mission_surface.get("judgement") or "Authorised study plan for today"
            ).strip(),
            next_action=next_action,
            observed_facts=tuple(evidence[:6]),
            estimates=tuple(estimates[:4]),
            plan_drivers=plan_drivers,
            review_point=review_point,
            expected_benefit=expected_benefit,
        )

    @staticmethod
    def _twin_mission_narrative(
        *,
        today_mission: Any,
        mission_surface: dict[str, Any],
    ) -> MissionNarrative:
        slots = mission_surface.get("today_missions_slots") or []
        primary_reason = ""
        observed: list[str] = []
        if slots and isinstance(slots[0], dict):
            primary_reason = str(slots[0].get("reason") or "").strip()
        for slot in slots:
            if not isinstance(slot, dict):
                continue
            topic = str(
                slot.get("topic_name") or slot.get("topic_id") or ""
            ).strip()
            if topic:
                observed.append(f"Planned focus: {topic}")
            reason = str(slot.get("reason") or "").strip()
            if reason and reason not in observed:
                observed.append(reason)

        title = (
            str(getattr(today_mission, "title", "") or "").strip() or "Today's focus"
        )
        reason = primary_reason or _TWIN_MISSION_REASON_FALLBACK
        purpose = primary_reason or _TWIN_MISSION_PURPOSE_FALLBACK

        return MissionNarrative(
            topic_title=title,
            educational_purpose=purpose,
            reason_for_selection=reason,
            educational_position="Twin Adaptive Study Planner focus for today",
            next_action=title,
            observed_facts=tuple(observed[:6]),
            estimates=(),
        )


class _RuntimeAReadinessSurfaceAdapter:
    """Default ReadinessSurfacePort — Runtime A dashboard surface pass-through.

    EP-006.4 composition: fetches the same ReadinessService surface Analytics
    uses, maps it via RuntimeAPresentationAdapter, then delegates DTO shaping
    back to the application layer (``readiness_explanation_from_narrative``).
    """

    def load_readiness_explanation(
        self, user_id: int
    ) -> ReadinessExplanationSnapshot | None:
        from app.services.readiness_quality import (
            has_complete_readiness_explanation_schema,
        )
        from app.services.readiness_service import ReadinessService

        surface = ReadinessService.get_dashboard_readiness_surface(user_id)
        if not isinstance(surface, dict) or not surface:
            return None
        narrative = RuntimeAPresentationAdapter.readiness_narrative(surface)
        return readiness_explanation_from_narrative(
            narrative,
            schema_complete=has_complete_readiness_explanation_schema(surface),
        )


bind_readiness_surface_port(_RuntimeAReadinessSurfaceAdapter())

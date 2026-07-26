"""Recommendation Engine service.

Generates structured, deterministic recommendations using:
- AdaptiveLearningService (mastery, weak topics, review scheduling)
- ReadinessService (exam readiness, coverage, streaks)

All logic is explainable and completely deterministic. No AI or external APIs.

Supporting service classes (BurnoutMonitor, ExamTimeline, MissionOptimizer)
have been extracted into their own modules for maintainability.

EP-001.4: ``build_study_insights`` consumes EP-001.1 Canonical Learner State,
EP-001.2 planner outputs, and EP-001.3 readiness intelligence when Digital
Twin Foundation is enabled. Twin owns learner state; Planner owns planning;
Readiness owns evaluation; this service hosts insight *communication*.

EP-002.4: when Twin is ON in approved non-production environments,
``generate_recommendations`` may execute ``build_study_insights`` as a
fail-open diagnostic dual-run. Legacy recommendations remain the sole
student-facing authority on that method; dual-run never mutates returned
payloads.

EP-002.5: ``get_dashboard_recommendations`` may serve a Twin Study Insights
projection on dashboard/home when Cutover + Twin are ON in approved
non-production environments. Legacy remains the fail-open fallback.

EP-003.1: ``generate_recommendations`` applies the Recommendation Quality
contract (P-001.2 explanation schema, P-001.3 decision ladder, confidence,
plan coherence, honest refusal). Ranking and schema attachment remain this
service's authority; presentation adapters must not re-decide.

EP-004.2: ``generate_recommendations`` may consume Personal Learning Profile
attributes as optional evidence for bounded tie-break personalisation,
session-sizing guidance, and tip cadence. The profile never owns ranking;
Decision Framework ladder classes remain authoritative.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Any

from app.extensions import db
from app.models.decision import Decision
from app.services.burnout_monitor import BurnoutMonitor
from app.services.exam_timeline import ExamTimeline
from app.services.readiness_service import ReadinessService

logger = logging.getLogger(__name__)

CATEGORY_REVIEW = "Review"
CATEGORY_WEAK_TOPIC = "Weak Topic"
CATEGORY_NEW_TOPIC = "New Topic"
CATEGORY_MOCK_EXAM = "Mock Exam"
CATEGORY_REST = "Rest"
CATEGORY_REVISION = "Revision"
CATEGORY_EXAM_TECHNIQUE = "Exam Technique"

PRIORITY_CRITICAL = "Critical"
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"


class RecommendationService:
    """Deterministic recommendation engine.

    Consumes data from AdaptiveLearningService, ReadinessService, and
    AnalyticsService to produce structured, explainable recommendations.

    EP-001.4: ``build_study_insights`` packages student-facing guidance from
    Canonical Learner State (+ planner daily plan + readiness intelligence).
    It explains existing intelligence and does not introduce a parallel
    recommendation formula.

    EP-002.4: ``generate_recommendations`` may fail-open dual-run
    ``build_study_insights`` in non-production when Twin is ON. Dual-run is
    diagnostic only; legacy list remains student-facing authority.

    P2-MS009: optional ``advisory_injection`` may read EvidenceAdvisory
    inputs and document consideration for explainability. Advisory data is
    ignored for ranking / selection — Runtime A remains sole educational
    authority. This milestone adds the integration point only.

    P2-MS010: optional ``recovery_injection`` may read RecoveryPlanCandidate
    advisory placeholders and document consideration for explainability.
    Recovery candidates are ignored for ranking / selection — Runtime A
    remains sole educational authority. Architecture integration only.

    P2-MS011: optional ``simulation_service`` may run a parallel advisory
    decision simulation after production recommendations are generated.
    Simulation artefacts are operational only — production output returned
    to the student is never modified.

    P3-MS001: optional ``controlled_advisory`` may consume exactly one
    approved Evidence Advisory field under policy / flag / freshness /
    rollout governance. Influence is intentionally minimal (rationale
    annotation only) and fully explainable / reversible.

    P3-MS003: optional ``recommendation_policy`` may resolve declarative
    policy rules before recommendations are returned. Policy outputs are
    advisory to Runtime A (explainability attachment). Runtime A remains
    sole educational authority.

    P3-MS004: when the policy engine has weighting enabled
    (``ENABLE_POLICY_WEIGHTING``), Runtime A may apply exactly one approved,
    bounded weight adjustment from ``consistency_summary``. Fully
    explainable and reversible via the feature flag.

    P4-MS001: optional ``educational_trial`` may authorise policy weighting
    only for deterministic treatment cohorts under
    ``ENABLE_EDUCATIONAL_TRIALS``. Baseline cohorts retain baseline
    recommendations. Runtime A remains sole educational authority.

    EP-004.2: Personal Learning Profile attributes may inform bounded
    personalisation (tie-breaks, session sizing, cadence) when the profile
    flag is ON and attributes are available with sufficient confidence.
    Accept/dismiss remains preference history only — never mastery.
    """

    # ── Study Insights (EP-001.4) ─────────────────────────────────────

    @staticmethod
    def build_study_insights(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
        daily_plan: dict[str, Any] | None = None,
        readiness_intelligence: dict[str, Any] | None = None,
        include_planner: bool = True,
        include_readiness: bool = True,
    ) -> dict[str, Any] | None:
        """Build student-facing study insights from Twin + Planner + Readiness.

        When Digital Twin Foundation is unavailable (flag OFF or assemble
        failure), returns ``None`` so callers continue using legacy
        ``generate_recommendations``. Does not invent learner state, does
        not plan missions, and does not recalculate readiness scores.

        Args:
            user_id: The ID of the user.
            foundation: Optional injected ``StudentDigitalTwinFoundation``.
            canonical_state: Optional already-assembled
                ``CanonicalLearnerState`` (EP-002.2 shared DI).
            daily_plan: Optional injected EP-001.2 daily plan dict.
            readiness_intelligence: Optional injected EP-001.3 assessment dict.
            include_planner: When True and ``daily_plan`` is omitted, attempt
                ``PlanningService.build_daily_study_plan``.
            include_readiness: When True and ``readiness_intelligence`` is
                omitted, attempt ``ReadinessService.build_readiness_intelligence``.

        Returns:
            Serialisable study insight guidance dict, or None when Twin is
            unavailable.
        """
        from app.infrastructure.adapters.consumer_chain import (
            API_BUILD_STUDY_INSIGHTS,
            SERVICE_RECOMMENDATION,
            observe_build_api,
        )

        return observe_build_api(
            service_name=SERVICE_RECOMMENDATION,
            api_name=API_BUILD_STUDY_INSIGHTS,
            user_id=user_id,
            call=lambda: RecommendationService._build_study_insights_body(
                user_id,
                foundation=foundation,
                canonical_state=canonical_state,
                daily_plan=daily_plan,
                readiness_intelligence=readiness_intelligence,
                include_planner=include_planner,
                include_readiness=include_readiness,
            ),
        )

    @staticmethod
    def _build_study_insights_body(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
        daily_plan: dict[str, Any] | None = None,
        readiness_intelligence: dict[str, Any] | None = None,
        include_planner: bool = True,
        include_readiness: bool = True,
    ) -> dict[str, Any] | None:
        """Internal study-insights body (observability wraps the public API)."""
        twin_foundation = foundation
        if twin_foundation is None:
            twin_foundation = RecommendationService._resolve_twin_foundation()
        if twin_foundation is None or not getattr(
            twin_foundation, "is_enabled", lambda: False
        )():
            return None

        from app.infrastructure.adapters.consumer_chain import (
            API_BUILD_STUDY_INSIGHTS,
            SERVICE_RECOMMENDATION,
            assemble_shared_canonical_state,
        )
        from app.infrastructure.adapters.digital_twin.contracts import (
            AVAILABILITY_AVAILABLE,
        )
        from app.infrastructure.adapters.insight_recommendation import (
            build_canonical_insight_consumer,
            build_study_insight_assembler,
        )

        state = assemble_shared_canonical_state(
            twin_foundation,
            str(user_id),
            canonical_state=canonical_state,
            service_name=SERVICE_RECOMMENDATION,
            api_name=API_BUILD_STUDY_INSIGHTS,
        )
        plan_payload = daily_plan
        if plan_payload is None and include_planner:
            plan_payload = RecommendationService._resolve_daily_plan(
                user_id,
                foundation=twin_foundation,
                canonical_state=state,
            )

        readiness_payload = readiness_intelligence
        if readiness_payload is None and include_readiness:
            readiness_payload = RecommendationService._resolve_readiness_intelligence(
                user_id,
                foundation=twin_foundation,
                canonical_state=state,
                daily_plan=plan_payload,
            )

        inputs = build_canonical_insight_consumer().project(
            state,
            daily_plan=plan_payload,
            readiness_intelligence=readiness_payload,
        )
        if inputs.availability != AVAILABILITY_AVAILABLE:
            logger.debug(
                "Canonical Learner State unavailable for insights user %s (%s)",
                user_id,
                inputs.unavailable_reason,
            )
            return None

        guidance = build_study_insight_assembler().assemble(inputs)
        return guidance.to_dict()

    @staticmethod
    def _resolve_twin_foundation() -> object | None:
        """Resolve EP-001.1 Foundation when Digital Twin flag is ON."""
        from app.infrastructure.adapters.consumer_chain import (
            resolve_enabled_twin_foundation,
        )

        return resolve_enabled_twin_foundation()

    @staticmethod
    def _resolve_daily_plan(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
    ) -> dict[str, Any] | None:
        """Best-effort EP-001.2 daily plan for insight grounding."""
        try:
            from app.services.planning_service import PlanningService

            return PlanningService.build_daily_study_plan(
                user_id,
                foundation=foundation,
                canonical_state=canonical_state,
            )
        except Exception:  # noqa: BLE001
            logger.debug(
                "Planner outputs unavailable for insights user %s",
                user_id,
                exc_info=True,
            )
            return None

    @staticmethod
    def _resolve_readiness_intelligence(
        user_id: int,
        *,
        foundation: object | None = None,
        canonical_state: object | None = None,
        daily_plan: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Best-effort EP-001.3 readiness intelligence for insight grounding."""
        try:
            return ReadinessService.build_readiness_intelligence(
                user_id,
                foundation=foundation,
                canonical_state=canonical_state,
                daily_plan=daily_plan,
                include_planner=daily_plan is None,
            )
        except Exception:  # noqa: BLE001
            logger.debug(
                "Readiness intelligence unavailable for insights user %s",
                user_id,
                exc_info=True,
            )
            return None

    @staticmethod
    def generate_recommendations(
        user_id: int,
        limit: int = 5,
        *,
        advisory_injection: Any | None = None,
        recovery_injection: Any | None = None,
        simulation_service: Any | None = None,
        controlled_advisory: Any | None = None,
        recommendation_policy: Any | None = None,
        educational_trial: Any | None = None,
    ) -> list[dict]:
        """Generate the top N recommendations for a user.

        Args:
            user_id: Student user id.
            limit: Maximum recommendations to return.
            advisory_injection: Optional Runtime A Evidence Advisory
                injection point. When provided, advisory inputs may be read
                and documented; they do not influence recommendation output
                unless ``controlled_advisory`` explicitly activates a field
                or policy weighting is enabled.
            recovery_injection: Optional Runtime A Recovery Planner
                injection point. When provided, recovery candidates may be
                read and documented; they do not influence recommendation
                output.
            simulation_service: Optional DecisionSimulationService. When
                provided, runs a parallel comparison after production
                recommendations are computed; never alters returned output.
            controlled_advisory: Optional ControlledAdvisoryActivation.
                When provided and policy allows, applies minimal influence
                from the single approved advisory field.
            recommendation_policy: Optional RecommendationPolicyEngine.
                When provided, Runtime A consults applicable policy before
                returning recommendations and records explainability.
                When weighting is enabled on the engine, Runtime A may apply
                one bounded weight adjustment; Runtime A retains authority.
            educational_trial: Optional EducationalTrialService. When
                provided and enabled with an active trial, policy weighting
                is authorised only for treatment cohorts.
        """
        from app.services.learning_lifecycle_service import (
            LearningLifecycle,
            LearningLifecycleService,
        )

        legacy_started = time.perf_counter()

        # P2-MS009 integration point — document only; no behavioural change.
        if advisory_injection is not None:
            try:
                advisory_injection.prepare_for_recommendation(user_id)
            except Exception:
                logger.debug(
                    "evidence_advisory_injection_failed user_id=%s",
                    user_id,
                    exc_info=True,
                )

        # P2-MS010 integration point — document only; no behavioural change.
        if recovery_injection is not None:
            try:
                recovery_injection.prepare_for_recommendation(user_id)
            except Exception:
                logger.debug(
                    "recovery_injection_failed user_id=%s",
                    user_id,
                    exc_info=True,
                )

        # P3-MS003: request applicable policy before producing recommendations.
        # Decision is advisory; Runtime A retains final authority.
        policy_advisory = None
        if recommendation_policy is not None and advisory_injection is not None:
            policy_advisory = getattr(advisory_injection, "last_advisory", None)
        if recommendation_policy is not None:
            try:
                recommendation_policy.resolve_for_recommendation(
                    user_id, advisory=policy_advisory
                )
            except Exception:
                logger.debug(
                    "recommendation_policy_resolve_failed user_id=%s",
                    user_id,
                    exc_info=True,
                )

        lifecycle = LearningLifecycleService.resolve(user_id)
        if lifecycle.stage == LearningLifecycle.REVISION:
            recommendations = (
                RecommendationService._revision_lifecycle_recommendations(
                    user_id, limit=limit
                )
            )
            recommendations = RecommendationService._finalise_recommendations(
                user_id,
                recommendations,
                limit=limit,
                advisory_injection=advisory_injection,
                recovery_injection=recovery_injection,
                simulation_service=simulation_service,
                controlled_advisory=controlled_advisory,
                recommendation_policy=recommendation_policy,
                educational_trial=educational_trial,
                legacy_started=legacy_started,
            )
            return recommendations

        recommendations: list[dict] = []

        recommendations.extend(
            RecommendationService._review_backlog_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._weak_topic_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._curriculum_progression_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._mock_exam_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._burnout_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._revision_phase_recommendations(user_id)
        )
        recommendations.extend(
            RecommendationService._exam_technique_recommendations(user_id)
        )

        return RecommendationService._finalise_recommendations(
            user_id,
            recommendations,
            limit=limit,
            advisory_injection=advisory_injection,
            recovery_injection=recovery_injection,
            simulation_service=simulation_service,
            controlled_advisory=controlled_advisory,
            recommendation_policy=recommendation_policy,
            educational_trial=educational_trial,
            legacy_started=legacy_started,
        )

    @staticmethod
    def _finalise_recommendations(
        user_id: int,
        recommendations: list[dict],
        *,
        limit: int,
        advisory_injection: Any | None = None,
        recovery_injection: Any | None = None,
        simulation_service: Any | None = None,
        controlled_advisory: Any | None = None,
        recommendation_policy: Any | None = None,
        educational_trial: Any | None = None,
        legacy_started: float | None = None,
    ) -> list[dict]:
        """Apply EP-003.1 quality contract, then fail-open advisory hooks."""
        from app.services.recommendation_quality import apply_quality_contract

        profile_view = RecommendationService.consume_personal_learning_profile(
            user_id
        )
        result = apply_quality_contract(
            user_id,
            recommendations,
            limit=limit,
            profile_view=profile_view,
        )
        result = RecommendationService._apply_controlled_advisory(
            user_id,
            result,
            advisory_injection=advisory_injection,
            controlled_advisory=controlled_advisory,
        )
        result = RecommendationService._apply_recommendation_policy(
            user_id,
            result,
            advisory_injection=advisory_injection,
            recommendation_policy=recommendation_policy,
            educational_trial=educational_trial,
        )
        RecommendationService._run_decision_simulation(
            user_id,
            result,
            advisory_injection=advisory_injection,
            recovery_injection=recovery_injection,
            simulation_service=simulation_service,
            recommendation_policy=recommendation_policy,
            educational_trial=educational_trial,
        )
        latency_ms = None
        if legacy_started is not None:
            latency_ms = (time.perf_counter() - legacy_started) * 1000.0
        RecommendationService._maybe_study_insights_dual_run(
            user_id,
            result,
            legacy_latency_ms=latency_ms,
        )
        return result

    @staticmethod
    def _normalise_recommendation_schema(
        user_id: int,
        recommendations: list[dict],
        *,
        limit: int,
    ) -> list[dict]:
        """Ensure dashboard rows carry the mandatory explanation schema.

        Study Insights projections already own communication content; this
        only fills missing schema fields without re-ranking Twin authority.
        """
        from app.services.recommendation_quality import (
            apply_quality_contract,
            has_complete_explanation_schema,
        )

        if not recommendations:
            return apply_quality_contract(user_id, [], limit=limit)

        if all(has_complete_explanation_schema(row) for row in recommendations):
            return list(recommendations)[: max(1, int(limit))]

        # Twin-served rows: attach schema without changing Twin order.
        if recommendations and recommendations[0].get("source_authority") == (
            "study_insights"
        ):
            normalised = apply_quality_contract(
                user_id,
                recommendations,
                limit=max(len(recommendations), int(limit)),
            )
            # Preserve Twin presentation order by original titles when possible.
            by_title = {
                str(row.get("title") or ""): row for row in normalised
            }
            ordered: list[dict] = []
            for original in recommendations:
                title = str(original.get("title") or "")
                ordered.append(by_title.get(title) or original)
            return ordered[: max(1, int(limit))]

        return apply_quality_contract(user_id, recommendations, limit=limit)

    @staticmethod
    def _maybe_study_insights_dual_run(
        user_id: int,
        recommendations: list[dict],
        *,
        legacy_latency_ms: float | None = None,
    ) -> None:
        """EP-002.4 fail-open Study Insights dual-run (diagnostic only).

        Never mutates ``recommendations``. Eligibility is Twin ON +
        non-production ``APP_ENV``. Failures are swallowed.
        When EP-002.5 cutover is eligible or already active, dual-run is
        skipped so Twin executes at most once on the student path.
        """
        try:
            from app.infrastructure.adapters.consumer_chain.cutover import (
                is_cutover_active,
                is_study_insights_cutover_eligible,
            )

            if is_cutover_active() or is_study_insights_cutover_eligible():
                return

            from app.infrastructure.adapters.consumer_chain import (
                run_study_insights_dual_run,
            )

            run_study_insights_dual_run(
                user_id,
                recommendations,
                legacy_latency_ms=legacy_latency_ms,
            )
        except Exception:  # noqa: BLE001 — dual-run must never break student path
            logger.debug(
                "study_insights_dual_run_hook_failed user_id=%s",
                user_id,
                exc_info=True,
            )

    @staticmethod
    def get_dashboard_recommendations(
        user_id: int,
        limit: int = 5,
    ) -> list[dict]:
        """Dashboard/home recommendations with EP-002.5 gated Study Insights cutover.

        Eligible non-production requests may receive a Twin Study Insights
        projection. Otherwise returns legacy ``generate_recommendations``.
        Fail-open: Twin failures and blocking limitations fall back to legacy.
        Bridges and Founder paths should continue calling
        ``generate_recommendations`` directly.
        """
        from app.infrastructure.adapters.consumer_chain.cutover import (
            run_study_insights_http_cutover,
        )

        rows = run_study_insights_http_cutover(user_id, limit=limit)
        return RecommendationService._normalise_recommendation_schema(
            user_id, rows, limit=limit
        )

    @staticmethod
    def get_dashboard_today_recommendation(user_id: int) -> dict | None:
        """Single best dashboard recommendation (cutover-aware)."""
        recs = RecommendationService.get_dashboard_recommendations(user_id, limit=1)
        return recs[0] if recs else None

    @staticmethod
    def _apply_controlled_advisory(
        user_id: int,
        recommendations: list[dict],
        *,
        advisory_injection: Any | None = None,
        controlled_advisory: Any | None = None,
    ) -> list[dict]:
        """P3-MS001 controlled advisory consumption — minimal influence only.

        Failures are swallowed so activation never breaks the student path;
        disabling the flag restores prior behaviour immediately.
        """
        if controlled_advisory is None:
            return recommendations
        try:
            advisory = None
            if advisory_injection is not None:
                advisory = getattr(advisory_injection, "last_advisory", None)
            applied = controlled_advisory.apply_to_recommendations(
                user_id,
                recommendations,
                advisory=advisory,
            )
            if isinstance(applied, list):
                return applied
            return recommendations
        except Exception:
            logger.debug(
                "controlled_advisory_failed user_id=%s",
                user_id,
                exc_info=True,
            )
            return recommendations

    @staticmethod
    def _apply_recommendation_policy(
        user_id: int,
        recommendations: list[dict],
        *,
        advisory_injection: Any | None = None,
        recommendation_policy: Any | None = None,
        educational_trial: Any | None = None,
    ) -> list[dict]:
        """P3-MS003/004 recommendation policy — explainability + optional weight.

        Policy decisions are advisory. When weighting is disabled, ranking /
        priority / title / category are never changed. When weighting is
        enabled, Runtime A may apply exactly one bounded weight adjustment.

        P4-MS001: when an educational trial is enabled and active, weighting
        is authorised only for treatment cohorts (baseline retains unweighted
        recommendations). Failures are swallowed so policy never breaks the
        student path; disabling the trial flag restores prior behaviour.
        """
        if recommendation_policy is None:
            return recommendations
        try:
            advisory = None
            if advisory_injection is not None:
                advisory = getattr(advisory_injection, "last_advisory", None)

            weighting_authorised = True
            if educational_trial is not None and getattr(
                educational_trial, "is_enabled", lambda: False
            )():
                authorise = getattr(
                    educational_trial, "authorises_policy_weighting", None
                )
                if callable(authorise):
                    weighting_authorised = bool(authorise(str(user_id)))

            if weighting_authorised:
                applied = recommendation_policy.apply_to_recommendations(
                    user_id,
                    recommendations,
                    advisory=advisory,
                )
            else:
                # Baseline cohort: attach policy explainability without weight.
                applied = list(recommendations)
                if getattr(recommendation_policy, "is_enabled", lambda: False)():
                    decision = recommendation_policy.resolve_for_recommendation(
                        user_id, advisory=advisory
                    )
                    attach = getattr(
                        recommendation_policy, "attach_explainability", None
                    )
                    if callable(attach):
                        applied = attach(applied, decision)
                # Record denied weight path when weighting flag is on.
                if getattr(
                    recommendation_policy, "is_weighting_enabled", lambda: False
                )():
                    resolve_weight = getattr(
                        recommendation_policy, "resolve_weight_application", None
                    )
                    if callable(resolve_weight):
                        resolve_weight(
                            student_id=str(user_id),
                            advisory=advisory,
                            feature_flag_enabled=False,
                        )

            if educational_trial is not None and getattr(
                educational_trial, "is_enabled", lambda: False
            )():
                record = getattr(educational_trial, "record_policy_activation", None)
                if callable(record):
                    weight_app = getattr(
                        recommendation_policy, "last_weight_application", None
                    )
                    activated = bool(
                        weighting_authorised
                        and weight_app is not None
                        and getattr(weight_app, "applied", False)
                    )
                    rec_id = ""
                    if applied:
                        rec_id = str(
                            applied[0].get("id")
                            or applied[0].get("recommendation_id")
                            or ""
                        )
                    record(
                        str(user_id),
                        recommendation_id=rec_id,
                        activated=activated,
                    )

            if isinstance(applied, list):
                return applied
            return recommendations
        except Exception:
            logger.debug(
                "recommendation_policy_failed user_id=%s",
                user_id,
                exc_info=True,
            )
            return recommendations

    @staticmethod
    def _run_decision_simulation(
        user_id: int,
        production_recommendations: list[dict],
        *,
        advisory_injection: Any | None = None,
        recovery_injection: Any | None = None,
        simulation_service: Any | None = None,
        recommendation_policy: Any | None = None,
        educational_trial: Any | None = None,
    ) -> None:
        """P2-MS011 parallel simulation — operational artefacts only.

        Never mutates ``production_recommendations``. Failures are swallowed
        so simulation never affects the student-facing path.

        P3-MS004: when policy weighting is enabled, re-apply the same weight
        rule to a production mirror and flag divergence beyond tolerance
        (determinism / consistency check). Simulation generation remains
        available via DecisionSimulationService.

        P4-MS001: weight-mirror comparison runs only when the educational
        trial (if present) authorises treatment weighting for the student.
        """
        if simulation_service is None and recommendation_policy is None:
            return
        try:
            evidence_advisory = None
            if advisory_injection is not None:
                last = getattr(advisory_injection, "last_consideration", None)
                if last is not None and getattr(last, "considered", False):
                    # Prefer last advisory DTO when injection retained it.
                    evidence_advisory = getattr(
                        advisory_injection, "last_advisory", None
                    )
                    if evidence_advisory is None:
                        evidence_advisory = {
                            "advisory_id": getattr(last, "advisory_id", ""),
                            "source_description": getattr(
                                last, "source_description", ""
                            ),
                            "provenance_refs": dict(
                                getattr(last, "provenance_refs", {}) or {}
                            ),
                        }
                if evidence_advisory is None:
                    evidence_advisory = getattr(
                        advisory_injection, "last_advisory", None
                    )
            recovery_candidates = ()
            if recovery_injection is not None:
                candidate = getattr(recovery_injection, "last_candidate", None)
                if candidate is not None:
                    recovery_candidates = (candidate,)

            if simulation_service is not None:
                simulation_service.simulate_after_recommendations(
                    student_id=user_id,
                    production_recommendations=production_recommendations,
                    evidence_advisory=evidence_advisory,
                    recovery_candidates=recovery_candidates,
                )

            weighting_on = bool(
                recommendation_policy is not None
                and getattr(
                    recommendation_policy, "is_weighting_enabled", lambda: False
                )()
            )
            if educational_trial is not None and getattr(
                educational_trial, "is_enabled", lambda: False
            )():
                authorise = getattr(
                    educational_trial, "authorises_policy_weighting", None
                )
                if callable(authorise) and not authorise(str(user_id)):
                    weighting_on = False
            if weighting_on:
                from copy import deepcopy

                advisory = evidence_advisory
                if advisory is None and advisory_injection is not None:
                    advisory = getattr(advisory_injection, "last_advisory", None)
                # Deterministic mirror: strip weight artefacts, re-apply, compare.
                mirrored_source = [
                    deepcopy(dict(item)) for item in production_recommendations
                ]
                for row in mirrored_source:
                    row.pop("scoring_weight", None)
                    row.pop("policy_weight_application", None)
                mirrored = recommendation_policy.apply_weight_to_recommendations(
                    user_id,
                    mirrored_source,
                    advisory=advisory,
                )
                recommendation_policy.compare_weight_simulation(
                    production_recommendations,
                    mirrored,
                )
        except Exception:
            logger.debug(
                "decision_simulation_failed user_id=%s",
                user_id,
                exc_info=True,
            )

    @staticmethod
    def _revision_lifecycle_recommendations(
        user_id: int, *, limit: int = 5
    ) -> list[dict]:
        """Deterministic revision recommendations when syllabus coverage is complete.

        Suppresses unread-topic progression. Uses observed weak-topic and
        timeline signals only — no adaptive AI.
        """
        from app.services.learning_lifecycle_service import LearningLifecycleService

        recs: list[dict] = []
        weak_label = LearningLifecycleService.weakest_completed_topic_label(user_id)
        now = datetime.utcnow().isoformat()

        if weak_label:
            recs.append({
                "title": f"Review weakest topic: {weak_label}",
                "category": CATEGORY_REVISION,
                "priority": PRIORITY_HIGH,
                "reason": (
                    f"Your syllabus is complete. Revisiting {weak_label} "
                    "consolidates understanding where Estimated Knowledge "
                    "is comparatively lower."
                ),
                "expected_benefit": (
                    "Strengthen a weaker completed topic before the exam."
                ),
                "generated_at": now,
            })

        recs.append({
            "title": "Complete a mixed-topic practice set",
            "category": CATEGORY_REVISION,
            "priority": PRIORITY_HIGH,
            "reason": (
                "Syllabus coverage is complete. Mixed practice consolidates "
                "knowledge across topics rather than advancing unread material."
            ),
            "expected_benefit": (
                "Build exam fluency across the full syllabus."
            ),
            "generated_at": now,
        })

        recs.append({
            "title": "Recall important formulae",
            "category": CATEGORY_REVISION,
            "priority": PRIORITY_MEDIUM,
            "reason": (
                "In Revision Mode, retrieving key formulae without notes "
                "supports examination readiness."
            ),
            "expected_benefit": "Improve recall under exam conditions.",
            "generated_at": now,
        })

        recs.append({
            "title": "Complete one timed practice session",
            "category": CATEGORY_EXAM_TECHNIQUE,
            "priority": PRIORITY_MEDIUM,
            "reason": (
                "Timed practice builds pacing discipline once the syllabus "
                "has been completed studying."
            ),
            "expected_benefit": "Strengthen timing and exam technique.",
            "generated_at": now,
        })

        recs.extend(RecommendationService._burnout_recommendations(user_id))
        recs.extend(RecommendationService._mock_exam_recommendations(user_id))

        # EP-003.1 quality contract performs ladder ranking; preserve generator order.
        seen: set[str] = set()
        unique: list[dict] = []
        for rec in recs:
            if rec["title"] not in seen:
                seen.add(rec["title"])
                unique.append(rec)
        return unique[:limit]

    @staticmethod
    def generate_today_recommendation(user_id: int) -> dict | None:
        """Generate the single best recommendation for today."""
        recs = RecommendationService.generate_recommendations(user_id, limit=1)
        return recs[0] if recs else None

    # ── Rule Set Implementations ──────────────────────────────────────────

    @staticmethod
    def _review_backlog_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        backlog = ReadinessService.get_review_backlog(user_id)

        if backlog["topics_overdue"] > 0:
            recs.append({
                "title": f"Clear your review backlog ({backlog['topics_overdue']} overdue)",
                "category": CATEGORY_REVIEW,
                "priority": PRIORITY_CRITICAL,
                "reason": (
                    f"You have {backlog['topics_overdue']} topic(s) overdue for review. "
                    "Staying current on reviews helps protect Estimated Knowledge."
                ),
                "expected_benefit": (
                    "Restore retention on overdue topics and keep review rhythm steady."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
        elif backlog["topics_due_today"] > 0:
            recs.append({
                "title": f"Review {backlog['topics_due_today']} topic(s) due today",
                "category": CATEGORY_REVIEW,
                "priority": PRIORITY_HIGH,
                "reason": (
                    f"{backlog['topics_due_today']} topic(s) are scheduled for review today."
                ),
                "expected_benefit": (
                    "Maintain your review rhythm and keep topics from becoming overdue."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _weak_topic_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        weak_topics = ReadinessService.get_weakest_topics(user_id, limit=3)

        if not weak_topics:
            return recs

        critical_weak = [t for t in weak_topics if t["mastery_score"] < 30]
        if critical_weak:
            topic_names = ", ".join(t["topic_name"] for t in critical_weak[:2])
            recs.append({
                "title": f"Practise lower Estimated Knowledge: {topic_names}",
                "category": CATEGORY_WEAK_TOPIC,
                "priority": PRIORITY_CRITICAL,
                "reason": (
                    f"Your Estimated Knowledge for {topic_names} is below 30%. "
                    "These foundational areas may benefit from more practice before "
                    "you lean on them in later topics."
                ),
                "expected_benefit": (
                    "Strengthen foundational Estimated Knowledge through practice."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
            return recs

        moderate_weak = [t for t in weak_topics if t["mastery_score"] < 60]
        if moderate_weak:
            topic_names = ", ".join(t["topic_name"] for t in moderate_weak[:2])
            recs.append({
                "title": f"Improve Estimated Knowledge: {topic_names}",
                "category": CATEGORY_WEAK_TOPIC,
                "priority": PRIORITY_HIGH,
                "reason": (
                    f"Your Estimated Knowledge for {topic_names} is between 30-60%. "
                    "Targeted practice on lower-estimate areas often helps most."
                ),
                "expected_benefit": "Bring these topics into a stronger estimated range.",
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _curriculum_progression_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        coverage = ReadinessService.get_curriculum_coverage(user_id)

        if coverage["total_leaf_topics"] == 0:
            return recs

        next_topic_name = RecommendationService._next_incomplete_topic_label(user_id)

        if coverage["coverage_percentage"] < 30 and coverage["topics_not_started"] > 0:
            if next_topic_name:
                title = f"Study {next_topic_name}"
                reason = (
                    f"Your next syllabus topic is {next_topic_name}. "
                    f"You have only covered {coverage['coverage_percentage']:.0f}% "
                    "of the curriculum."
                )
            else:
                title = (
                    f"Explore new topics — {coverage['topics_not_started']} remaining"
                )
                reason = (
                    f"You have only covered {coverage['coverage_percentage']:.0f}% "
                    "of the curriculum. Broadening coverage is essential."
                )
            recs.append({
                "title": title,
                "category": CATEGORY_NEW_TOPIC,
                "priority": PRIORITY_HIGH,
                "reason": reason,
                "expected_benefit": (
                    "Increase syllabus coverage — Study Progress, not Estimated Knowledge."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        if 30 <= coverage["coverage_percentage"] < 70:
            if next_topic_name:
                title = f"Continue with {next_topic_name}"
                reason = (
                    f"Your curriculum coverage is at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    f"Next up: {next_topic_name}."
                )
            else:
                title = "Continue progressing through the curriculum"
                reason = (
                    f"Your curriculum coverage is at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    "Steady progression ensures comprehensive exam preparation."
                )
            recs.append({
                "title": title,
                "category": CATEGORY_NEW_TOPIC,
                "priority": PRIORITY_MEDIUM,
                "reason": reason,
                "expected_benefit": (
                    "Sustained curriculum progression builds broad knowledge."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        if coverage["coverage_percentage"] >= 70 and coverage["topics_not_started"] > 0:
            if next_topic_name:
                title = f"Complete {next_topic_name}"
                reason = (
                    f"You have excellent coverage at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    f"Remaining work includes {next_topic_name}."
                )
            else:
                title = (
                    f"Complete remaining {coverage['topics_not_started']} topics"
                )
                reason = (
                    f"You have excellent coverage at "
                    f"{coverage['coverage_percentage']:.0f}%. "
                    "Complete the full syllabus for no blind spots."
                )
            recs.append({
                "title": title,
                "category": CATEGORY_NEW_TOPIC,
                "priority": PRIORITY_LOW,
                "reason": reason,
                "expected_benefit": (
                    "Finish remaining syllabus topics so Study Progress is complete."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _next_incomplete_topic_label(user_id: int) -> str | None:
        """Return a display label for the user's next incomplete syllabus topic."""
        from app.services.curriculum_service import CurriculumService
        from app.services.planning_service import PlanningService
        from app.services.study_plan_service import StudyPlanService

        plan = StudyPlanService.get_user_active_plan(user_id)
        if plan is None or not plan.curriculum_id:
            return None
        curriculum = CurriculumService.get_curriculum_by_id(plan.curriculum_id)
        if curriculum is None:
            return None
        topic = CurriculumService.get_next_incomplete_topic(user_id, curriculum)
        if topic is None:
            return None
        topic_code = PlanningService._resolve_official_topic_code(plan, topic)
        return PlanningService._topic_study_label(topic, topic_code=topic_code)

    @staticmethod
    def _mock_exam_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        readiness = ReadinessService.get_overall_readiness(user_id)

        if readiness["total_topics"] == 0:
            return recs

        if readiness["score"] >= 60 and readiness["coverage_pct"] >= 50:
            recs.append({
                "title": "Take a mock exam this week",
                "category": CATEGORY_MOCK_EXAM,
                "priority": PRIORITY_MEDIUM,
                "reason": (
                    f"Estimated readiness is about {readiness['score']:.0f}% with "
                    f"{readiness['coverage_pct']:.0f}% syllabus coverage. "
                    "Mock exams can help reveal remaining gaps — estimates are not "
                    "exam outcome guarantees."
                ),
                "expected_benefit": (
                    "Reveal remaining gaps and build exam-day familiarity."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
        elif readiness["score"] >= 40:
            recs.append({
                "title": "Begin incorporating mock exam practice",
                "category": CATEGORY_MOCK_EXAM,
                "priority": PRIORITY_LOW,
                "reason": (
                    f"Estimated readiness is about {readiness['score']:.0f}%. "
                    "Introducing occasional mock exam sections builds familiarity."
                ),
                "expected_benefit": (
                    "Early exposure to exam-style questions builds familiarity."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _burnout_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        burnout = BurnoutMonitor.detect_burnout(user_id)

        if burnout["risk_level"] == "high":
            recs.append({
                "title": "Take a rest day — study pattern notice",
                "category": CATEGORY_REST,
                "priority": PRIORITY_CRITICAL,
                "reason": f"{burnout['explanation']} Taking a rest day now prevents longer forced breaks later.",
                "expected_benefit": (
                    "Recovery, clearer focus, and steadier progress over the week."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })
        elif burnout["risk_level"] == "moderate":
            recs.append({
                "title": "Consider a lighter study day",
                "category": CATEGORY_REST,
                "priority": PRIORITY_MEDIUM,
                "reason": f"{burnout['explanation']} A lighter day helps maintain momentum while recovering.",
                "expected_benefit": "Protect focus while keeping study momentum.",
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _revision_phase_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        timeline = ExamTimeline.get_timeline(user_id)

        if timeline is None:
            return recs

        days_remaining = timeline["days_remaining"]
        coverage = timeline["curriculum_coverage_pct"]

        if days_remaining <= 30 and days_remaining > 0 and coverage >= 50:
            recs.append({
                "title": f"Enter revision phase — {days_remaining} days until exam",
                "category": CATEGORY_REVISION,
                "priority": PRIORITY_HIGH if days_remaining <= 14 else PRIORITY_MEDIUM,
                "reason": (
                    f"With {days_remaining} days until your exam and {coverage:.0f}% "
                    "coverage, shift focus to consolidation and revision."
                ),
                "expected_benefit": (
                    "Focused revision in the final weeks maximises retention."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        if 14 <= days_remaining <= 45 and coverage >= 60:
            recs.append({
                "title": "Enter mock exam phase",
                "category": CATEGORY_MOCK_EXAM,
                "priority": PRIORITY_HIGH if days_remaining <= 21 else PRIORITY_MEDIUM,
                "reason": (
                    f"With {days_remaining} days remaining and {coverage:.0f}% coverage, "
                    "you should be in the mock exam phase."
                ),
                "expected_benefit": "Regular mock exams build stamina and reveal weak points.",
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    @staticmethod
    def _exam_technique_recommendations(user_id: int) -> list[dict]:
        recs: list[dict] = []
        timeline = ExamTimeline.get_timeline(user_id)

        if timeline is None:
            return recs

        if (
            timeline["days_remaining"] <= 60
            and timeline["days_remaining"] > 0
            and timeline["average_mastery_pct"] >= 40
        ):
            recs.append({
                "title": "Focus on exam technique and time management",
                "category": CATEGORY_EXAM_TECHNIQUE,
                "priority": (
                    PRIORITY_HIGH if timeline["days_remaining"] <= 30
                    else PRIORITY_MEDIUM
                ),
                "reason": (
                    f"With {timeline['days_remaining']} days until your exam, "
                    "exam technique becomes increasingly important."
                ),
                "expected_benefit": (
                    "Better exam technique can add 5-15% to your score."
                ),
                "generated_at": datetime.utcnow().isoformat(),
            })

        return recs

    # ── Decision Journal Methods ───────────────────────────────────────────

    @staticmethod
    def record_decision(
        user_id: int,
        recommendation: dict,
        accepted: bool = False,
        completed: bool = False,
        outcome_summary: str | None = None,
    ) -> Decision:
        """Record a user's decision about a recommendation.

        EIP-002: Accept / dismiss is preference history only. It must never
        create Educational Evidence of understanding or mutate Version 1
        Estimated Knowledge (Constitution Art. V §2; EL-006 / EL-008).
        """
        decision = Decision(
            user_id=user_id,
            recommendation_title=recommendation["title"],
            recommendation_category=recommendation["category"],
            recommendation_priority=recommendation["priority"],
            recommendation_reason=recommendation["reason"],
            recommendation_expected_benefit=recommendation["expected_benefit"],
            recommendation_generated_at=(
                datetime.fromisoformat(recommendation["generated_at"])
                if isinstance(recommendation["generated_at"], str)
                else recommendation["generated_at"]
            ),
            accepted=accepted,
            completed=completed,
            outcome_summary=outcome_summary,
        )
        db.session.add(decision)
        db.session.commit()
        logger.info(
            "Decision recorded for user %d: %s accepted=%s",
            user_id, recommendation["title"], accepted,
        )
        RecommendationService._emit_decision_feedback(
            user_id,
            accepted=accepted,
            recommendation=recommendation,
        )
        RecommendationService.consume_personal_learning_profile(user_id)
        return decision

    @staticmethod
    def _emit_decision_feedback(
        user_id: int,
        *,
        accepted: bool,
        recommendation: dict,
    ) -> None:
        """EP-003.4: emit preference-journal feedback (fail-open)."""
        try:
            from app.infrastructure.adapters.learning_feedback import (
                emit_recommendation_decision_feedback,
            )

            emit_recommendation_decision_feedback(
                user_id=user_id,
                accepted=accepted,
                recommendation_title=str(recommendation.get("title") or ""),
                recommendation_category=str(
                    recommendation.get("category") or ""
                ),
            )
        except Exception:  # noqa: BLE001 — feedback must never break decisions
            logger.debug(
                "learning_feedback_decision_emit_failed user_id=%s",
                user_id,
                exc_info=True,
            )

    @staticmethod
    def consume_personal_learning_profile(
        user_id: int,
        *,
        declared_session_minutes: int | None = None,
    ) -> dict | None:
        """EP-004.1/EP-004.2: optional Personal Learning Profile input (fail-open).

        Returns a stable consumer view of observed behavioural attributes.
        EP-004.2 may use available, confidence-gated attributes as evidence
        for bounded tie-breaks, session sizing, and cadence inside this
        service. The profile never owns ranking or educational authority.
        """
        try:
            from app.infrastructure.adapters.personal_learning_profile import (
                consume_personal_learning_profile,
            )

            return consume_personal_learning_profile(
                student_id=user_id,
                declared_session_minutes=declared_session_minutes,
            )
        except Exception:  # noqa: BLE001 — profile must never break decisions
            logger.debug(
                "personal_learning_profile_consume_failed user_id=%s",
                user_id,
                exc_info=True,
            )
            return None

    @staticmethod
    def get_decision_journal(user_id: int, limit: int = 20) -> list[Decision]:
        """Get the decision journal for a user."""
        return (
            Decision.query.filter_by(user_id=user_id)
            .order_by(Decision.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_decision_summary(user_id: int) -> dict:
        """Get summary statistics for the decision journal."""
        decisions = Decision.query.filter_by(user_id=user_id).all()
        total = len(decisions)

        if total == 0:
            return {
                "total_decisions": 0,
                "acceptance_rate": 0.0,
                "completion_rate": 0.0,
                "categories": {},
            }

        accepted = sum(1 for d in decisions if d.accepted)
        completed = sum(1 for d in decisions if d.completed)

        categories: dict[str, dict] = {}
        for d in decisions:
            cat = d.recommendation_category
            if cat not in categories:
                categories[cat] = {"total": 0, "accepted": 0, "completed": 0}
            categories[cat]["total"] += 1
            if d.accepted:
                categories[cat]["accepted"] += 1
            if d.completed:
                categories[cat]["completed"] += 1

        return {
            "total_decisions": total,
            "acceptance_rate": round((accepted / total) * 100, 1) if total > 0 else 0.0,
            "completion_rate": round((completed / total) * 100, 1) if total > 0 else 0.0,
            "categories": {
                cat: {
                    "total": data["total"],
                    "acceptance_rate": round((data["accepted"] / data["total"]) * 100, 1),
                    "completion_rate": round((data["completed"] / data["total"]) * 100, 1),
                }
                for cat, data in categories.items()
            },
        }


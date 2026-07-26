"""Daily Study Plan gated HTTP cutover (EP-002.7).

Eligible non-production dashboard/mission requests may receive a Twin
``build_daily_study_plan`` projection into the existing mission surface DTO.
Legacy ``generate_today_mission`` remains the fail-open fallback and the sole
Runtime A mission persistence authority.

MissionOptimizer remains quarantined — this module never calls it.
PlanningService remains the sole owner of study planning.
"""

from __future__ import annotations

import logging
import os
import re
import time
from contextvars import ContextVar
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_DAILY_STUDY_PLAN,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger(__name__)

_PRODUCTION_ENVS = frozenset({"production", "prod"})

_CUTOVER_ACTIVE: ContextVar[bool] = ContextVar(
    "ep0027_daily_plan_cutover_active", default=False
)

_REQUEST_CACHE_ATTR = "_ep0027_daily_plan_cutover_cache"

FALLBACK_TWIN_OFF = "twin_off"
FALLBACK_CUTOVER_FLAG_OFF = "cutover_flag_off"
FALLBACK_PRODUCTION_ENV = "production_env"
FALLBACK_CONFIGURATION = "configuration_failure"
FALLBACK_TWIN_UNAVAILABLE = "twin_unavailable"
FALLBACK_TWIN_EXCEPTION = "twin_exception"
FALLBACK_BLOCKING_LIMITATION = "blocking_limitation"
FALLBACK_PROJECTION_EMPTY = "projection_empty"

ALIGNMENT_ALIGNED = "aligned"
ALIGNMENT_MISMATCHED = "mismatched"
ALIGNMENT_TWIN_UNAVAILABLE = "twin_unavailable"
ALIGNMENT_LIMITATION_FALLBACK = "limitation_fallback"

BLOCKING_LIMITATION_CODES = frozenset(
    {
        "twin_foundation_flag_off",
        "canonical_learner_state_unavailable",
        "invalid_student_id",
    }
)

SOURCE_AUTHORITY_DAILY_STUDY_PLAN = "daily_study_plan"
SOURCE_AUTHORITY_LEGACY = "legacy"

_SLOT_PRIORITY = {"progression": 0, "weak": 1, "review": 2}


class MissionDisplayProxy:
    """Duck-types Mission for templates with a Twin title overlay.

    Proxies ORM identity / status / tasks for session continuity. Never writes
    to the database — Twin display authority only.
    """

    __slots__ = ("_mission", "_title_override")

    def __init__(self, mission: Any, *, title: str | None = None) -> None:
        self._mission = mission
        self._title_override = (title or "").strip() or None

    @property
    def title(self) -> str:
        if self._title_override:
            return self._title_override
        return str(getattr(self._mission, "title", "") or "")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._mission, name)


def is_daily_plan_cutover_active() -> bool:
    """True while a daily-plan cutover orchestration is in flight."""
    return bool(_CUTOVER_ACTIVE.get())


def is_daily_plan_cutover_eligible(
    *,
    environ: dict[str, str] | None = None,
) -> bool:
    """True when Twin + Daily Plan Cutover flags are ON and not production."""
    try:
        env = environ if environ is not None else os.environ
        flags = resolve_v2_feature_flags(environ=env)
        if not flags.ENABLE_DIGITAL_TWIN:
            return False
        if not flags.ENABLE_DAILY_PLAN_CUTOVER:
            return False
        flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
        app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
        return app_env not in _PRODUCTION_ENVS
    except Exception:  # noqa: BLE001 — configuration failure → ineligible
        logger.debug("daily_plan_cutover_eligibility_failed", exc_info=True)
        return False


def daily_plan_cutover_ineligibility_reason(
    *,
    environ: dict[str, str] | None = None,
) -> str | None:
    """Return a fallback reason when cutover must not be attempted, else None."""
    try:
        env = environ if environ is not None else os.environ
        flags = resolve_v2_feature_flags(environ=env)
        if not flags.ENABLE_DIGITAL_TWIN:
            return FALLBACK_TWIN_OFF
        if not flags.ENABLE_DAILY_PLAN_CUTOVER:
            return FALLBACK_CUTOVER_FLAG_OFF
        flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
        app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
        if app_env in _PRODUCTION_ENVS:
            return FALLBACK_PRODUCTION_ENV
        return None
    except Exception:  # noqa: BLE001
        return FALLBACK_CONFIGURATION


def _limitation_codes(twin_payload: Any) -> tuple[str, ...]:
    if not isinstance(twin_payload, dict):
        return ()
    codes_raw = twin_payload.get("limitations_codes") or twin_payload.get(
        "limitations"
    ) or ()
    if isinstance(codes_raw, str):
        return (codes_raw,) if codes_raw else ()
    return tuple(str(c) for c in codes_raw if c)


def has_daily_plan_blocking_limitation(twin_payload: Any) -> bool:
    """True when Twin daily plan must not be served to the student."""
    if not isinstance(twin_payload, dict):
        return True
    codes = set(_limitation_codes(twin_payload))
    if codes & BLOCKING_LIMITATION_CODES:
        return True
    availability = str(twin_payload.get("availability") or "").strip().lower()
    if availability and availability != "available":
        return True
    slots = twin_payload.get("today_missions") or []
    if not isinstance(slots, list) or not slots:
        return True
    return False


def _slot_topic_ids(slots: Any) -> tuple[str, ...]:
    if not isinstance(slots, list):
        return ()
    ids: list[str] = []
    seen: set[str] = set()
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        topic_id = str(slot.get("topic_id") or "").strip()
        if topic_id and topic_id not in seen:
            seen.add(topic_id)
            ids.append(topic_id)
    return tuple(ids)


def _primary_slot(slots: Any) -> dict[str, Any] | None:
    if not isinstance(slots, list) or not slots:
        return None
    ranked: list[tuple[int, int, dict[str, Any]]] = []
    for index, slot in enumerate(slots):
        if not isinstance(slot, dict):
            continue
        kind = str(slot.get("slot") or slot.get("kind") or "").strip().lower()
        ranked.append((_SLOT_PRIORITY.get(kind, 50), index, slot))
    if not ranked:
        return None
    ranked.sort(key=lambda item: (item[0], item[1]))
    return ranked[0][2]


def _title_from_slot(slot: dict[str, Any] | None) -> str | None:
    if not isinstance(slot, dict):
        return None
    topic_name = str(slot.get("topic_name") or "").strip()
    kind = str(slot.get("slot") or slot.get("kind") or "").strip().lower()
    if not topic_name:
        return None
    if kind == "review":
        return f"Review {topic_name}"
    if kind == "weak":
        return f"Strengthen {topic_name}"
    if kind == "progression":
        return f"Study {topic_name}"
    return topic_name


def _legacy_mission_text(legacy_mission: Any) -> str:
    if legacy_mission is None:
        return ""
    parts = [str(getattr(legacy_mission, "title", "") or "")]
    tasks = getattr(legacy_mission, "tasks", None) or []
    for task in tasks:
        parts.append(str(getattr(task, "title", "") or ""))
        parts.append(str(getattr(task, "description", "") or ""))
    return " ".join(parts).lower()


def _normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _topic_tokens_match(legacy_text: str, topic_id: str, topic_name: str) -> bool:
    haystack = _normalize_token(legacy_text)
    if not haystack:
        return False
    for candidate in (topic_id, topic_name):
        token = _normalize_token(candidate)
        if len(token) >= 3 and token in haystack:
            return True
    return False


def project_daily_plan_to_mission_surface(
    twin_payload: dict[str, Any],
    *,
    legacy_surface: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Project Twin daily study plan into dashboard/mission surface DTO."""
    if has_daily_plan_blocking_limitation(twin_payload):
        return None

    slots = list(twin_payload.get("today_missions") or [])
    primary = _primary_slot(slots)
    title = _title_from_slot(primary)
    if not title:
        return None

    legacy_mission = None
    if isinstance(legacy_surface, dict):
        legacy_mission = legacy_surface.get("today_mission")

    if legacy_mission is None:
        # No ORM mission to anchor session CTA — fail projection (fail-open).
        return None

    display = MissionDisplayProxy(legacy_mission, title=title)
    codes = list(_limitation_codes(twin_payload))
    workload = twin_payload.get("recommended_workload")
    if not isinstance(workload, dict):
        workload = {}

    return {
        "today_mission": display,
        "source_authority": SOURCE_AUTHORITY_DAILY_STUDY_PLAN,
        "daily_plan": twin_payload,
        "today_missions_slots": slots,
        "recommended_workload": workload,
        "topic_ordering": list(twin_payload.get("topic_ordering") or []),
        "revision_priorities": list(twin_payload.get("revision_priorities") or []),
        "limitations_codes": codes,
        "explainability": dict(twin_payload.get("explainability") or {}),
        "plan_date": twin_payload.get("plan_date"),
        "availability": twin_payload.get("availability"),
    }


def assess_daily_plan_semantic_alignment(
    *,
    legacy_surface: dict[str, Any],
    twin_payload: dict[str, Any] | None,
    served_twin: bool,
    fallback_reason: str | None,
) -> dict[str, Any]:
    """Semantic plan/mission alignment (topic / objective / sequence / workload)."""
    if fallback_reason in {
        FALLBACK_TWIN_UNAVAILABLE,
        FALLBACK_TWIN_EXCEPTION,
        FALLBACK_TWIN_OFF,
        FALLBACK_CUTOVER_FLAG_OFF,
        FALLBACK_PRODUCTION_ENV,
        FALLBACK_CONFIGURATION,
    }:
        status = ALIGNMENT_TWIN_UNAVAILABLE
    elif fallback_reason in {
        FALLBACK_BLOCKING_LIMITATION,
        FALLBACK_PROJECTION_EMPTY,
    }:
        status = ALIGNMENT_LIMITATION_FALLBACK
    elif not served_twin or twin_payload is None:
        status = ALIGNMENT_TWIN_UNAVAILABLE
    else:
        legacy_mission = legacy_surface.get("today_mission")
        legacy_text = _legacy_mission_text(legacy_mission)
        slots = twin_payload.get("today_missions") or []
        twin_ids = _slot_topic_ids(slots)
        primary = _primary_slot(slots)

        topic_ok = False
        if twin_ids:
            for slot in slots if isinstance(slots, list) else []:
                if not isinstance(slot, dict):
                    continue
                if _topic_tokens_match(
                    legacy_text,
                    str(slot.get("topic_id") or ""),
                    str(slot.get("topic_name") or ""),
                ):
                    topic_ok = True
                    break
        else:
            topic_ok = not legacy_text.strip()

        if isinstance(primary, dict):
            objective_ok = _topic_tokens_match(
                legacy_text,
                str(primary.get("topic_id") or ""),
                str(primary.get("topic_name") or ""),
            ) or bool(str(primary.get("reason") or "").strip())
        else:
            objective_ok = topic_ok

        ordering = twin_payload.get("topic_ordering") or []
        sequencing_ok = True
        if isinstance(ordering, list) and ordering:
            first = ordering[0] if isinstance(ordering[0], dict) else None
            if isinstance(first, dict):
                sequencing_ok = _topic_tokens_match(
                    legacy_text,
                    str(first.get("topic_id") or ""),
                    str(first.get("topic_name") or ""),
                ) or topic_ok

        workload = twin_payload.get("recommended_workload")
        workload_ok = isinstance(workload, dict) and (
            workload.get("recommended_minutes") is not None
            or workload.get("available_study_minutes") is not None
            or bool(workload)
        )

        agreed = topic_ok and objective_ok and sequencing_ok and workload_ok
        status = ALIGNMENT_ALIGNED if agreed else ALIGNMENT_MISMATCHED

        twin_ids_out = list(twin_ids)
        return {
            "alignment_status": status,
            "aligned": status == ALIGNMENT_ALIGNED,
            "mismatched": status == ALIGNMENT_MISMATCHED,
            "topic_agreement": topic_ok,
            "study_objective_agreement": objective_ok,
            "sequencing_agreement": sequencing_ok,
            "workload_agreement": workload_ok,
            "twin_topic_ids": twin_ids_out,
            "legacy_title": str(getattr(legacy_mission, "title", "") or ""),
        }

    twin_ids_out = list(_slot_topic_ids((twin_payload or {}).get("today_missions")))
    return {
        "alignment_status": status,
        "aligned": status == ALIGNMENT_ALIGNED,
        "mismatched": status == ALIGNMENT_MISMATCHED,
        "topic_agreement": False,
        "study_objective_agreement": False,
        "sequencing_agreement": False,
        "workload_agreement": False,
        "twin_topic_ids": twin_ids_out,
        "legacy_title": str(
            getattr(legacy_surface.get("today_mission"), "title", "") or ""
        ),
    }


def _build_legacy_surface(
    user_id: int,
    *,
    today: Any | None = None,
    generate_today_mission: Any | None = None,
    get_today_mission: Any | None = None,
) -> dict[str, Any]:
    from app.services.mission_service import MissionService
    from app.services.planning_service import PlanningService
    from app.services.study_plan_service import StudyPlanService

    generate = generate_today_mission or PlanningService.generate_today_mission
    fetch = get_today_mission or MissionService.get_today_mission

    mission = generate(user_id, today) if today is not None else generate(user_id)
    if mission is None:
        active_plan = StudyPlanService.get_user_active_plan(user_id)
        if active_plan is not None:
            mission = fetch(
                user_id,
                study_plan_id=active_plan.id,
            )
    return {
        "today_mission": mission,
        "source_authority": SOURCE_AUTHORITY_LEGACY,
        "daily_plan": None,
        "today_missions_slots": [],
        "recommended_workload": {},
        "topic_ordering": [],
        "revision_priorities": [],
        "limitations_codes": [],
        "explainability": {},
        "plan_date": None,
        "availability": None,
    }


def _request_cache_get(user_id: int) -> dict[str, Any] | None:
    try:
        from flask import g, has_request_context

        if not has_request_context():
            return None
        cache = getattr(g, _REQUEST_CACHE_ATTR, None)
        if not isinstance(cache, dict):
            return None
        cached = cache.get(user_id)
        if isinstance(cached, dict):
            return cached
        return None
    except Exception:  # noqa: BLE001
        return None


def _request_cache_set(user_id: int, surface: dict[str, Any]) -> None:
    try:
        from flask import g, has_request_context

        if not has_request_context():
            return
        cache = getattr(g, _REQUEST_CACHE_ATTR, None)
        if not isinstance(cache, dict):
            cache = {}
            setattr(g, _REQUEST_CACHE_ATTR, cache)
        cache[user_id] = surface
    except Exception:  # noqa: BLE001
        return


def run_daily_plan_http_cutover(
    user_id: int,
    *,
    today: Any | None = None,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    build_daily_study_plan: Any | None = None,
    generate_today_mission: Any | None = None,
    get_today_mission: Any | None = None,
    skip_request_dedupe: bool = False,
) -> dict[str, Any]:
    """Return Daily Study Plan projection or legacy mission surface (fail-open).

    Always returns a surface dict. Twin failures / blocking states fall back
    to legacy ``generate_today_mission``. Never calls MissionOptimizer.
    """
    env = environ if environ is not None else dict(os.environ)
    sink = telemetry or get_consumer_chain_telemetry()
    flags = resolve_v2_feature_flags(environ=env)
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
    ids = CorrelationContext.current()

    from app.services.planning_service import PlanningService

    twin_builder = build_daily_study_plan or PlanningService.build_daily_study_plan

    ineligible = daily_plan_cutover_ineligibility_reason(environ=env)
    if ineligible is not None:
        legacy_started = time.perf_counter()
        legacy = _build_legacy_surface(
            user_id,
            today=today,
            generate_today_mission=generate_today_mission,
            get_today_mission=get_today_mission,
        )
        legacy_latency_ms = (time.perf_counter() - legacy_started) * 1000.0
        alignment = assess_daily_plan_semantic_alignment(
            legacy_surface=legacy,
            twin_payload=None,
            served_twin=False,
            fallback_reason=ineligible,
        )
        _emit_and_record(
            sink=sink,
            user_id=user_id,
            flags=flags,
            app_env=app_env,
            correlation_id=ids.correlation_id or "",
            causation_id=ids.causation_id or "",
            cutover_attempted=False,
            cutover_served=False,
            fallback_reason=ineligible,
            alignment=alignment,
            limitation_codes=(),
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=None,
            twin_exception=False,
        )
        return legacy

    if not skip_request_dedupe:
        cached = _request_cache_get(user_id)
        if cached is not None:
            return cached

    token = _CUTOVER_ACTIVE.set(True)
    twin_payload: Any = None
    twin_latency_ms = 0.0
    twin_exception = False
    fallback_reason: str | None = None
    try:
        legacy_started = time.perf_counter()
        try:
            legacy = _build_legacy_surface(
                user_id,
                today=today,
                generate_today_mission=generate_today_mission,
                get_today_mission=get_today_mission,
            )
        except Exception:  # noqa: BLE001
            logger.exception("daily_plan_cutover_legacy_failed user_id=%s", user_id)
            legacy = {
                "today_mission": None,
                "source_authority": SOURCE_AUTHORITY_LEGACY,
                "daily_plan": None,
                "today_missions_slots": [],
                "recommended_workload": {},
                "topic_ordering": [],
                "revision_priorities": [],
                "limitations_codes": [],
                "explainability": {},
                "plan_date": None,
                "availability": None,
            }
        legacy_latency_ms = (time.perf_counter() - legacy_started) * 1000.0

        twin_started = time.perf_counter()
        try:
            if today is not None:
                twin_payload = twin_builder(user_id, today)
            else:
                twin_payload = twin_builder(user_id)
        except Exception:  # noqa: BLE001 — never break student path
            twin_exception = True
            twin_payload = None
            fallback_reason = FALLBACK_TWIN_EXCEPTION
            logger.debug(
                "daily_plan_cutover_twin_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        twin_latency_ms = (time.perf_counter() - twin_started) * 1000.0

        if fallback_reason is None and twin_payload is None:
            fallback_reason = FALLBACK_TWIN_UNAVAILABLE
        elif fallback_reason is None and has_daily_plan_blocking_limitation(
            twin_payload
        ):
            fallback_reason = FALLBACK_BLOCKING_LIMITATION

        projected: dict[str, Any] | None = None
        if fallback_reason is None and isinstance(twin_payload, dict):
            projected = project_daily_plan_to_mission_surface(
                twin_payload,
                legacy_surface=legacy,
            )
            if projected is None:
                fallback_reason = FALLBACK_PROJECTION_EMPTY

        if fallback_reason is None and projected is not None:
            served = projected
            cutover_served = True
        else:
            # Keep legacy ORM reference — never deepcopy SQLAlchemy missions.
            served = legacy
            cutover_served = False

        alignment = assess_daily_plan_semantic_alignment(
            legacy_surface=legacy if isinstance(legacy, dict) else {},
            twin_payload=twin_payload if isinstance(twin_payload, dict) else None,
            served_twin=cutover_served,
            fallback_reason=fallback_reason,
        )
        _emit_and_record(
            sink=sink,
            user_id=user_id,
            flags=flags,
            app_env=app_env,
            correlation_id=ids.correlation_id or "",
            causation_id=ids.causation_id or "",
            cutover_attempted=True,
            cutover_served=cutover_served,
            fallback_reason=fallback_reason,
            alignment=alignment,
            limitation_codes=_limitation_codes(twin_payload),
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=twin_latency_ms,
            twin_exception=twin_exception,
        )
        if not skip_request_dedupe:
            _request_cache_set(user_id, served)
        return served
    finally:
        _CUTOVER_ACTIVE.reset(token)


def _emit_and_record(
    *,
    sink: ConsumerChainTelemetry,
    user_id: int,
    flags: Any,
    app_env: str,
    correlation_id: str,
    causation_id: str,
    cutover_attempted: bool,
    cutover_served: bool,
    fallback_reason: str | None,
    alignment: dict[str, Any],
    limitation_codes: tuple[str, ...],
    legacy_latency_ms: float | None,
    twin_latency_ms: float | None,
    twin_exception: bool,
) -> None:
    payload = {
        "api_name": API_BUILD_DAILY_STUDY_PLAN,
        "student_id": str(user_id),
        "environment": app_env,
        "cutover_attempted": bool(cutover_attempted),
        "cutover_served": bool(cutover_served),
        "influences_student": bool(cutover_served),
        "fallback_reason": fallback_reason or "",
        "alignment_status": alignment.get("alignment_status") or "",
        "aligned": bool(alignment.get("aligned")),
        "mismatched": bool(alignment.get("mismatched")),
        "topic_agreement": bool(alignment.get("topic_agreement")),
        "study_objective_agreement": bool(
            alignment.get("study_objective_agreement")
        ),
        "sequencing_agreement": bool(alignment.get("sequencing_agreement")),
        "workload_agreement": bool(alignment.get("workload_agreement")),
        "twin_topic_ids": list(alignment.get("twin_topic_ids") or ()),
        "limitation_codes": list(limitation_codes),
        "legacy_latency_ms": (
            round(float(legacy_latency_ms), 3)
            if legacy_latency_ms is not None
            else None
        ),
        "twin_latency_ms": (
            round(float(twin_latency_ms), 3) if twin_latency_ms is not None else None
        ),
        "twin_enabled": bool(flags.ENABLE_DIGITAL_TWIN),
        "authority_enabled": bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        "cutover_enabled": bool(flags.ENABLE_DAILY_PLAN_CUTOVER),
        "twin_exception": bool(twin_exception),
        "correlation_id": correlation_id,
        "causation_id": causation_id,
    }
    try:
        sink.emit_cutover(
            **{
                k: v
                for k, v in payload.items()
                if k
                not in {
                    "topic_agreement",
                    "study_objective_agreement",
                    "sequencing_agreement",
                    "workload_agreement",
                }
            }
        )
    except Exception:  # noqa: BLE001
        logger.debug("daily_plan_cutover_telemetry_failed", exc_info=True)
    try:
        from app.infrastructure.adapters.consumer_chain import (
            daily_plan_cutover_health as _health,
        )

        _health.get_daily_plan_cutover_health_metrics().record(payload)
    except Exception:  # noqa: BLE001
        logger.debug("daily_plan_cutover_metrics_failed", exc_info=True)

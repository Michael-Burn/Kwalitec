"""Daily Study Plan dual-run diagnostics (EP-002.7).

Compares legacy mission surface (``generate_today_mission``) with Twin
``build_daily_study_plan``. Diagnostic only — never changes student UX.
Never calls MissionOptimizer.
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
from app.infrastructure.adapters.consumer_chain.dual_run import (
    fingerprint_payload,
    is_dual_run_diagnostics_eligible,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger(__name__)

_DUAL_RUN_ACTIVE: ContextVar[bool] = ContextVar(
    "ep0027_daily_plan_dual_run_active", default=False
)

_REQUEST_DEDUPE_ATTR = "_ep0027_daily_plan_dual_run_users"


def is_daily_plan_dual_run_active() -> bool:
    """True while a daily-plan dual-run comparison is in flight."""
    return bool(_DUAL_RUN_ACTIVE.get())


def _limitation_codes(twin_payload: Any) -> tuple[str, ...]:
    if not isinstance(twin_payload, dict):
        return ()
    codes_raw = twin_payload.get("limitations_codes") or twin_payload.get(
        "limitations"
    ) or ()
    if isinstance(codes_raw, str):
        return (codes_raw,) if codes_raw else ()
    return tuple(str(c) for c in codes_raw if c)


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


def _normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _legacy_mission_text(legacy_mission: Any) -> str:
    if legacy_mission is None:
        return ""
    parts = [str(getattr(legacy_mission, "title", "") or "")]
    tasks = getattr(legacy_mission, "tasks", None) or []
    for task in tasks:
        parts.append(str(getattr(task, "title", "") or ""))
        parts.append(str(getattr(task, "description", "") or ""))
    return " ".join(parts).lower()


def _topic_overlap(legacy_text: str, twin_payload: Any) -> bool:
    if not isinstance(twin_payload, dict):
        return False
    slots = twin_payload.get("today_missions") or []
    if not isinstance(slots, list) or not slots:
        return not legacy_text.strip()
    haystack = _normalize_token(legacy_text)
    for slot in slots:
        if not isinstance(slot, dict):
            continue
        for candidate in (
            str(slot.get("topic_id") or ""),
            str(slot.get("topic_name") or ""),
        ):
            token = _normalize_token(candidate)
            if len(token) >= 3 and token in haystack:
                return True
    return False


def _request_already_ran(user_id: int) -> bool:
    try:
        from flask import g, has_request_context

        if not has_request_context():
            return False
        seen = getattr(g, _REQUEST_DEDUPE_ATTR, None)
        if seen is None:
            seen = set()
            setattr(g, _REQUEST_DEDUPE_ATTR, seen)
        if user_id in seen:
            return True
        seen.add(user_id)
        return False
    except Exception:  # noqa: BLE001 — dual-run must never break student path
        return False


def _legacy_surface_fingerprint(legacy_surface: Any) -> str:
    if not isinstance(legacy_surface, dict):
        return fingerprint_payload(legacy_surface)
    mission = legacy_surface.get("today_mission")
    payload = {
        "source_authority": legacy_surface.get("source_authority"),
        "mission_id": getattr(mission, "id", None),
        "mission_title": getattr(mission, "title", None),
        "mission_status": getattr(mission, "status", None),
    }
    return fingerprint_payload(payload)


def compare_legacy_vs_daily_study_plan(
    *,
    legacy_surface: Any,
    twin_payload: Any,
    user_id: int,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    legacy_latency_ms: float | None = None,
    twin_latency_ms: float | None = None,
    twin_exception: bool = False,
) -> dict[str, Any] | None:
    """Compare legacy mission surface vs Twin daily plan; emit dual-run telemetry."""
    env = environ if environ is not None else dict(os.environ)
    if not is_dual_run_diagnostics_eligible(environ=env):
        return None

    flags = resolve_v2_feature_flags(environ=env)
    ids = CorrelationContext.current()
    legacy_fp = _legacy_surface_fingerprint(legacy_surface)
    twin_fp = fingerprint_payload(twin_payload)
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"

    legacy_mission = (
        legacy_surface.get("today_mission")
        if isinstance(legacy_surface, dict)
        else None
    )
    legacy_text = _legacy_mission_text(legacy_mission)
    codes = _limitation_codes(twin_payload)
    twin_ids = _slot_topic_ids(
        twin_payload.get("today_missions") if isinstance(twin_payload, dict) else []
    )

    topic_agreement = _topic_overlap(legacy_text, twin_payload)
    workload = (
        twin_payload.get("recommended_workload")
        if isinstance(twin_payload, dict)
        else None
    )
    workload_agreement = isinstance(workload, dict) and bool(workload)
    sequencing_agreement = topic_agreement
    study_objective_agreement = topic_agreement

    comparison: dict[str, Any] = {
        "api_name": API_BUILD_DAILY_STUDY_PLAN,
        "student_id": str(user_id),
        "legacy_fingerprint": legacy_fp,
        "build_fingerprint": twin_fp,
        "twin_fingerprint": twin_fp,
        "fingerprints_match": legacy_fp == twin_fp,
        "environment": app_env,
        "diagnostic_only": True,
        "influences_student": False,
        "legacy_latency_ms": (
            round(float(legacy_latency_ms), 3)
            if legacy_latency_ms is not None
            else None
        ),
        "twin_latency_ms": (
            round(float(twin_latency_ms), 3) if twin_latency_ms is not None else None
        ),
        "legacy_unavailable": legacy_mission is None,
        "twin_unavailable": twin_payload is None,
        "limitation_codes": list(codes),
        "topic_agreement": topic_agreement,
        "study_objective_agreement": study_objective_agreement,
        "sequencing_agreement": sequencing_agreement,
        "workload_agreement": workload_agreement,
        "twin_topic_ids": list(twin_ids),
        "legacy_title": str(getattr(legacy_mission, "title", "") or ""),
        "correlation_id": ids.correlation_id or "",
        "causation_id": ids.causation_id or "",
        "twin_enabled": bool(flags.ENABLE_DIGITAL_TWIN),
        "authority_enabled": bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        "twin_exception": bool(twin_exception),
    }

    sink = telemetry or get_consumer_chain_telemetry()
    sink.emit_dual_run(
        api_name=API_BUILD_DAILY_STUDY_PLAN,
        student_id=str(user_id),
        twin_enabled=bool(flags.ENABLE_DIGITAL_TWIN),
        authority_enabled=bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
        legacy_fingerprint=legacy_fp,
        build_fingerprint=twin_fp,
        fingerprints_match=legacy_fp == twin_fp,
        environment=app_env,
        legacy_latency_ms=comparison["legacy_latency_ms"],
        twin_latency_ms=comparison["twin_latency_ms"],
        legacy_unavailable=bool(comparison["legacy_unavailable"]),
        twin_unavailable=bool(comparison["twin_unavailable"]),
        limitation_codes=codes,
        confidence_level="",
        confidence_available=False,
        legacy_categories=(),
        twin_field_ids=twin_ids,
        correlation_id=ids.correlation_id or "",
        causation_id=ids.causation_id or "",
    )

    try:
        from app.infrastructure.adapters.consumer_chain import (
            daily_plan_dual_run_health as _health,
        )

        _health.get_daily_plan_dual_run_health_metrics().record(comparison)
    except Exception:  # noqa: BLE001
        logger.debug("daily_plan_dual_run_metrics_failed", exc_info=True)

    return comparison


def run_daily_plan_dual_run(
    user_id: int,
    legacy_surface: dict[str, Any],
    *,
    today: Any | None = None,
    legacy_latency_ms: float | None = None,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    build_daily_study_plan: Any | None = None,
    skip_request_dedupe: bool = False,
) -> dict[str, Any] | None:
    """Execute Twin ``build_daily_study_plan`` beside an already-computed surface.

    Fail-open: Twin errors are swallowed. Never mutates ``legacy_surface``.
    Never calls MissionOptimizer.
    """
    env = environ if environ is not None else dict(os.environ)
    if not is_dual_run_diagnostics_eligible(environ=env):
        return None
    if _DUAL_RUN_ACTIVE.get():
        return None
    if not skip_request_dedupe and _request_already_ran(user_id):
        return None

    token = _DUAL_RUN_ACTIVE.set(True)
    twin_payload: Any = None
    twin_latency_ms = 0.0
    twin_exception = False
    try:
        from app.services.planning_service import PlanningService

        builder = build_daily_study_plan or PlanningService.build_daily_study_plan
        started = time.perf_counter()
        try:
            if today is not None:
                twin_payload = builder(user_id, today)
            else:
                twin_payload = builder(user_id)
        except Exception:  # noqa: BLE001 — never affect student path
            twin_exception = True
            twin_payload = None
            logger.debug(
                "daily_plan_dual_run_twin_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        twin_latency_ms = (time.perf_counter() - started) * 1000.0

        return compare_legacy_vs_daily_study_plan(
            legacy_surface=legacy_surface,
            twin_payload=twin_payload,
            user_id=user_id,
            telemetry=telemetry,
            environ=env,
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=twin_latency_ms,
            twin_exception=twin_exception,
        )
    finally:
        _DUAL_RUN_ACTIVE.reset(token)

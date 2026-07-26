"""Study Insights gated HTTP cutover (EP-002.5).

Eligible non-production dashboard requests may receive a Twin
``build_study_insights`` projection. Legacy ``generate_recommendations``
remains the fail-open fallback. Never invents educational authority.
"""

from __future__ import annotations

import logging
import os
import re
import time
from contextvars import ContextVar
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_STUDY_INSIGHTS,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger(__name__)

_PRODUCTION_ENVS = frozenset({"production", "prod"})

# Nested cutover / dual-run coordination.
_CUTOVER_ACTIVE: ContextVar[bool] = ContextVar(
    "ep0025_study_insights_cutover_active", default=False
)

_REQUEST_CACHE_ATTR = "_ep0025_study_insights_cutover_cache"

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

_TOPIC_FIELD_KEYS: tuple[str, ...] = (
    "todays_key_focus",
    "greatest_risk",
    "recommended_next_action",
    "strongest_area",
)


def is_cutover_active() -> bool:
    """True while a cutover orchestration is in flight (dual-run should skip)."""
    return bool(_CUTOVER_ACTIVE.get())


def is_study_insights_cutover_eligible(
    *,
    environ: dict[str, str] | None = None,
) -> bool:
    """True when Twin + Cutover flags are ON and the process is not production."""
    try:
        env = environ if environ is not None else os.environ
        flags = resolve_v2_feature_flags(environ=env)
        if not flags.ENABLE_DIGITAL_TWIN:
            return False
        if not flags.ENABLE_STUDY_INSIGHTS_CUTOVER:
            return False
        flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
        app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
        return app_env not in _PRODUCTION_ENVS
    except Exception:  # noqa: BLE001 — configuration failure → ineligible
        logger.debug("study_insights_cutover_eligibility_failed", exc_info=True)
        return False


def cutover_ineligibility_reason(
    *,
    environ: dict[str, str] | None = None,
) -> str | None:
    """Return a fallback reason when cutover must not be attempted, else None."""
    try:
        env = environ if environ is not None else os.environ
        flags = resolve_v2_feature_flags(environ=env)
        if not flags.ENABLE_DIGITAL_TWIN:
            return FALLBACK_TWIN_OFF
        if not flags.ENABLE_STUDY_INSIGHTS_CUTOVER:
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


def has_blocking_limitation(twin_payload: Any) -> bool:
    """True when Twin guidance must not be served to the student."""
    if not isinstance(twin_payload, dict):
        return True
    codes = set(_limitation_codes(twin_payload))
    if codes & BLOCKING_LIMITATION_CODES:
        return True
    focus = twin_payload.get("todays_key_focus")
    next_action = twin_payload.get("recommended_next_action")
    if focus is None and next_action is None:
        return True
    if (
        "todays_key_focus_unavailable" in codes
        and "recommended_next_action_unavailable" in codes
    ):
        return True
    return False


def _field_as_dict(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        result = to_dict()
        return result if isinstance(result, dict) else None
    return None


def _field_text(field: dict[str, Any] | None, *, key: str = "message") -> str:
    if not field:
        return ""
    return str(field.get(key) or field.get("title") or "").strip()


def project_study_insights_to_recommendations(
    twin_payload: dict[str, Any],
    *,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Project Study Insights guidance into dashboard-compatible recommendation rows."""
    codes = list(_limitation_codes(twin_payload))
    generated_at = datetime.now(UTC).isoformat()
    rows: list[dict[str, Any]] = []

    focus = _field_as_dict(twin_payload.get("todays_key_focus"))
    next_action = _field_as_dict(twin_payload.get("recommended_next_action"))
    risk = _field_as_dict(twin_payload.get("greatest_risk"))
    strongest = _field_as_dict(twin_payload.get("strongest_area"))
    workload = _field_as_dict(twin_payload.get("workload_explanation"))
    readiness = _field_as_dict(twin_payload.get("readiness_explanation"))
    motivation = _field_as_dict(twin_payload.get("motivational_progress_summary"))

    advice_parts = [
        part
        for part in (
            _field_text(workload),
            _field_text(readiness),
            _field_text(motivation),
        )
        if part
    ]
    educational_advice = " ".join(advice_parts)

    if focus is not None or next_action is not None:
        title = _field_text(focus, key="title") or _field_text(
            next_action, key="title"
        ) or "Today's study focus"
        reason = _field_text(focus) or _field_text(next_action) or educational_advice
        next_step = _field_text(next_action) or _field_text(next_action, key="title")
        topic_id = None
        if focus and focus.get("topic_id"):
            topic_id = str(focus.get("topic_id"))
        elif next_action and next_action.get("topic_id"):
            topic_id = str(next_action.get("topic_id"))
        rows.append(
            {
                "title": title,
                "category": "Study Focus",
                "priority": "High",
                "reason": reason or title,
                "expected_benefit": (
                    "Follow Twin-grounded study guidance for today's focus."
                ),
                "next_action": next_step or None,
                "topic_id": topic_id,
                "observed_facts": tuple(
                    fact
                    for fact in (_field_text(focus), _field_text(next_action))
                    if fact
                ),
                "estimates": (),
                "educational_advice": educational_advice or reason or title,
                "limitations_codes": list(codes),
                "source_authority": "study_insights",
                "confidence_level": str(
                    twin_payload.get("confidence_level") or ""
                ).strip(),
                "generated_at": generated_at,
            }
        )

    if risk is not None:
        rows.append(
            {
                "title": _field_text(risk, key="title") or "Watch this risk",
                "category": "Study Risk",
                "priority": "High",
                "reason": _field_text(risk) or _field_text(risk, key="title"),
                "expected_benefit": (
                    "Address the greatest study risk while evidence supports it."
                ),
                "next_action": None,
                "topic_id": (
                    str(risk.get("topic_id")) if risk.get("topic_id") else None
                ),
                "observed_facts": (_field_text(risk),) if _field_text(risk) else (),
                "estimates": (),
                "educational_advice": _field_text(risk) or _field_text(
                    risk, key="title"
                ),
                "limitations_codes": list(codes),
                "source_authority": "study_insights",
                "confidence_level": str(
                    twin_payload.get("confidence_level") or ""
                ).strip(),
                "generated_at": generated_at,
            }
        )

    if strongest is not None and len(rows) < limit:
        rows.append(
            {
                "title": _field_text(strongest, key="title") or "Strongest area",
                "category": "Study Strength",
                "priority": "Low",
                "reason": _field_text(strongest) or _field_text(strongest, key="title"),
                "expected_benefit": "Build on a demonstrated strength.",
                "next_action": None,
                "topic_id": (
                    str(strongest.get("topic_id"))
                    if strongest.get("topic_id")
                    else None
                ),
                "observed_facts": (
                    (_field_text(strongest),) if _field_text(strongest) else ()
                ),
                "estimates": (),
                "educational_advice": _field_text(strongest)
                or _field_text(strongest, key="title"),
                "limitations_codes": list(codes),
                "source_authority": "study_insights",
                "confidence_level": str(
                    twin_payload.get("confidence_level") or ""
                ).strip(),
                "generated_at": generated_at,
            }
        )

    return rows[: max(1, int(limit))]


def _normalise_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _twin_topic_ids(twin_payload: dict[str, Any]) -> tuple[str, ...]:
    ids: list[str] = []
    seen: set[str] = set()
    for key in _TOPIC_FIELD_KEYS:
        field = _field_as_dict(twin_payload.get(key))
        if not field:
            continue
        topic_id = str(field.get("topic_id") or "").strip()
        if topic_id and topic_id not in seen:
            seen.add(topic_id)
            ids.append(topic_id)
    return tuple(ids)


def _legacy_text_blob(legacy_recommendations: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for row in legacy_recommendations:
        if not isinstance(row, dict):
            continue
        for key in ("title", "reason", "expected_benefit", "category"):
            value = row.get(key)
            if value:
                parts.append(str(value))
    return _normalise_token(" ".join(parts))


def assess_semantic_alignment(
    *,
    legacy_recommendations: list[dict[str, Any]],
    twin_payload: dict[str, Any] | None,
    served_twin: bool,
    fallback_reason: str | None,
) -> dict[str, Any]:
    """Lightweight topical alignment report (not fingerprint equality)."""
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
        topic_ids = _twin_topic_ids(twin_payload)
        blob = _legacy_text_blob(legacy_recommendations)
        if not topic_ids:
            # No topic ids — treat category/presence overlap as soft align when
            # legacy is also empty or Twin served actionable focus.
            status = (
                ALIGNMENT_ALIGNED
                if served_twin and (not legacy_recommendations or blob)
                else ALIGNMENT_MISMATCHED
            )
        else:
            matched = any(
                _normalise_token(topic_id) in blob
                or topic_id.lower() in blob
                for topic_id in topic_ids
            )
            # Also match bare topic tokens from titles on Twin fields.
            twin_titles = []
            for key in _TOPIC_FIELD_KEYS:
                field = _field_as_dict(twin_payload.get(key))
                if field:
                    twin_titles.append(_normalise_token(str(field.get("title") or "")))
            title_match = any(
                title and title in blob for title in twin_titles if title
            )
            status = (
                ALIGNMENT_ALIGNED if (matched or title_match) else ALIGNMENT_MISMATCHED
            )

    return {
        "alignment_status": status,
        "aligned": status == ALIGNMENT_ALIGNED,
        "mismatched": status == ALIGNMENT_MISMATCHED,
        "twin_topic_ids": list(_twin_topic_ids(twin_payload or {})),
        "legacy_row_count": len(legacy_recommendations),
    }


def _request_cache_get(user_id: int) -> list[dict[str, Any]] | None:
    """Return cached cutover rows for this user within the Flask request."""
    try:
        from flask import g, has_request_context

        if not has_request_context():
            return None
        cache = getattr(g, _REQUEST_CACHE_ATTR, None)
        if not isinstance(cache, dict):
            return None
        cached = cache.get(user_id)
        if isinstance(cached, list):
            return deepcopy(cached)
        return None
    except Exception:  # noqa: BLE001
        return None


def _request_cache_set(user_id: int, rows: list[dict[str, Any]]) -> None:
    try:
        from flask import g, has_request_context

        if not has_request_context():
            return
        cache = getattr(g, _REQUEST_CACHE_ATTR, None)
        if not isinstance(cache, dict):
            cache = {}
            setattr(g, _REQUEST_CACHE_ATTR, cache)
        cache[user_id] = deepcopy(list(rows))
    except Exception:  # noqa: BLE001
        return


def run_study_insights_http_cutover(
    user_id: int,
    *,
    limit: int = 5,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    build_study_insights: Any | None = None,
    generate_recommendations: Any | None = None,
    skip_request_dedupe: bool = False,
) -> list[dict[str, Any]]:
    """Return Study Insights projection or legacy recommendations (fail-open).

    Always returns a list. Twin failures / blocking states fall back to legacy.
    """
    env = environ if environ is not None else dict(os.environ)
    sink = telemetry or get_consumer_chain_telemetry()
    flags = resolve_v2_feature_flags(environ=env)
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
    ids = CorrelationContext.current()

    from app.services.recommendation_service import RecommendationService

    legacy_builder = (
        generate_recommendations or RecommendationService.generate_recommendations
    )
    twin_builder = build_study_insights or RecommendationService.build_study_insights

    ineligible = cutover_ineligibility_reason(environ=env)
    if ineligible is not None:
        legacy_started = time.perf_counter()
        legacy = list(legacy_builder(user_id, limit=limit) or [])
        legacy_latency_ms = (time.perf_counter() - legacy_started) * 1000.0
        alignment = assess_semantic_alignment(
            legacy_recommendations=legacy,
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

    # Eligible attempt — reuse request-scoped result for today + list calls.
    if not skip_request_dedupe:
        cached = _request_cache_get(user_id)
        if cached is not None:
            return cached[: max(1, int(limit))]

    # Build a full card set once per request so today (limit=1) and list
    # (limit=5) share the same Twin/legacy decision.
    build_limit = max(5, int(limit))

    token = _CUTOVER_ACTIVE.set(True)
    twin_payload: Any = None
    twin_latency_ms = 0.0
    twin_exception = False
    fallback_reason: str | None = None
    served: list[dict[str, Any]]
    try:
        legacy_started = time.perf_counter()
        try:
            legacy = list(legacy_builder(user_id, limit=build_limit) or [])
        except Exception:  # noqa: BLE001 — should not happen; still fail closed to []
            logger.exception(
                "study_insights_cutover_legacy_failed user_id=%s", user_id
            )
            legacy = []
        legacy_latency_ms = (time.perf_counter() - legacy_started) * 1000.0

        twin_started = time.perf_counter()
        try:
            twin_payload = twin_builder(user_id)
        except Exception:  # noqa: BLE001 — never break student path
            twin_exception = True
            twin_payload = None
            fallback_reason = FALLBACK_TWIN_EXCEPTION
            logger.debug(
                "study_insights_cutover_twin_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        twin_latency_ms = (time.perf_counter() - twin_started) * 1000.0

        if fallback_reason is None and twin_payload is None:
            fallback_reason = FALLBACK_TWIN_UNAVAILABLE
        elif fallback_reason is None and has_blocking_limitation(twin_payload):
            fallback_reason = FALLBACK_BLOCKING_LIMITATION

        projected: list[dict[str, Any]] = []
        if fallback_reason is None and isinstance(twin_payload, dict):
            projected = project_study_insights_to_recommendations(
                twin_payload, limit=build_limit
            )
            if not projected:
                fallback_reason = FALLBACK_PROJECTION_EMPTY

        if fallback_reason is None:
            served = projected
            cutover_served = True
        else:
            served = deepcopy(legacy)
            cutover_served = False

        alignment = assess_semantic_alignment(
            legacy_recommendations=legacy,
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
        return served[: max(1, int(limit))] if served else served
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
        "api_name": API_BUILD_STUDY_INSIGHTS,
        "student_id": str(user_id),
        "environment": app_env,
        "cutover_attempted": bool(cutover_attempted),
        "cutover_served": bool(cutover_served),
        "influences_student": bool(cutover_served),
        "fallback_reason": fallback_reason or "",
        "alignment_status": alignment.get("alignment_status") or "",
        "aligned": bool(alignment.get("aligned")),
        "mismatched": bool(alignment.get("mismatched")),
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
        "cutover_enabled": bool(flags.ENABLE_STUDY_INSIGHTS_CUTOVER),
        "twin_exception": bool(twin_exception),
        "correlation_id": correlation_id,
        "causation_id": causation_id,
    }
    try:
        sink.emit_cutover(**payload)
    except Exception:  # noqa: BLE001
        logger.debug("study_insights_cutover_telemetry_failed", exc_info=True)
    try:
        from app.infrastructure.adapters.consumer_chain.cutover_health import (
            get_study_insights_cutover_health_metrics,
        )

        get_study_insights_cutover_health_metrics().record(payload)
    except Exception:  # noqa: BLE001
        logger.debug("study_insights_cutover_metrics_failed", exc_info=True)

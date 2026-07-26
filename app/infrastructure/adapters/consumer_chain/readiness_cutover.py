"""Readiness Intelligence gated HTTP cutover (EP-002.6).

Eligible non-production dashboard/analytics requests may receive a Twin
``build_readiness_intelligence`` projection. Legacy readiness surface remains
the fail-open fallback. Never invents educational authority. Never wraps
``get_overall_readiness`` (collector recursion safety).
"""

from __future__ import annotations

import logging
import os
import time
from contextvars import ContextVar
from copy import deepcopy
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain.contracts import (
    API_BUILD_READINESS_INTELLIGENCE,
)
from app.infrastructure.adapters.consumer_chain.telemetry import (
    ConsumerChainTelemetry,
    get_consumer_chain_telemetry,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger(__name__)

_PRODUCTION_ENVS = frozenset({"production", "prod"})

_CUTOVER_ACTIVE: ContextVar[bool] = ContextVar(
    "ep0026_readiness_cutover_active", default=False
)

_REQUEST_CACHE_ATTR = "_ep0026_readiness_cutover_cache"

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

_SCORE_AGREEMENT_TOLERANCE = 10.0
SOURCE_AUTHORITY_READINESS_INTELLIGENCE = "readiness_intelligence"


def is_readiness_cutover_active() -> bool:
    """True while a readiness cutover orchestration is in flight."""
    return bool(_CUTOVER_ACTIVE.get())


def is_readiness_intelligence_cutover_eligible(
    *,
    environ: dict[str, str] | None = None,
) -> bool:
    """True when Twin + Readiness Cutover flags are ON and not production."""
    try:
        env = environ if environ is not None else os.environ
        flags = resolve_v2_feature_flags(environ=env)
        if not flags.ENABLE_DIGITAL_TWIN:
            return False
        if not flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER:
            return False
        flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
        app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
        return app_env not in _PRODUCTION_ENVS
    except Exception:  # noqa: BLE001 — configuration failure → ineligible
        logger.debug("readiness_cutover_eligibility_failed", exc_info=True)
        return False


def readiness_cutover_ineligibility_reason(
    *,
    environ: dict[str, str] | None = None,
) -> str | None:
    """Return a fallback reason when cutover must not be attempted, else None."""
    try:
        env = environ if environ is not None else os.environ
        flags = resolve_v2_feature_flags(environ=env)
        if not flags.ENABLE_DIGITAL_TWIN:
            return FALLBACK_TWIN_OFF
        if not flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER:
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


def has_readiness_blocking_limitation(twin_payload: Any) -> bool:
    """True when Twin readiness assessment must not be served to the student."""
    if not isinstance(twin_payload, dict):
        return True
    codes = set(_limitation_codes(twin_payload))
    if codes & BLOCKING_LIMITATION_CODES:
        return True
    availability = str(twin_payload.get("availability") or "").strip().lower()
    if availability and availability != "available":
        return True
    if twin_payload.get("readiness_score") is None:
        return True
    return False


def _driver_value(twin_payload: dict[str, Any], driver_id: str) -> float | None:
    drivers = twin_payload.get("readiness_drivers") or []
    if not isinstance(drivers, list):
        return None
    for driver in drivers:
        if not isinstance(driver, dict):
            continue
        if str(driver.get("driver_id") or "") != driver_id:
            continue
        value = driver.get("value")
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
    return None


def _area_to_topic_row(area: Any) -> dict[str, Any] | None:
    if not isinstance(area, dict):
        return None
    topic_id = str(area.get("topic_id") or "").strip()
    if not topic_id:
        return None
    mastery = area.get("mastery_score")
    try:
        mastery_score = float(mastery) if mastery is not None else 0.0
    except (TypeError, ValueError):
        mastery_score = 0.0
    return {
        "topic_id": topic_id,
        "topic_name": str(area.get("topic_name") or topic_id),
        "mastery_score": mastery_score,
        "stage": "",
        "revision_count": 0,
        "reason": str(area.get("reason") or ""),
    }


def project_readiness_intelligence_to_surface(
    twin_payload: dict[str, Any],
    *,
    legacy_surface: dict[str, Any] | None = None,
    weak_limit: int = 5,
    strong_limit: int = 5,
) -> dict[str, Any] | None:
    """Project Twin readiness assessment into dashboard/analytics surface DTO."""
    if twin_payload.get("readiness_score") is None:
        return None

    try:
        score = float(twin_payload["readiness_score"])
    except (TypeError, ValueError):
        return None

    legacy_readiness: dict[str, Any] = {}
    if isinstance(legacy_surface, dict) and isinstance(
        legacy_surface.get("readiness"), dict
    ):
        legacy_readiness = dict(legacy_surface["readiness"])

    coverage = _driver_value(twin_payload, "curriculum_coverage")
    mastery = _driver_value(twin_payload, "knowledge_strength")
    discipline = _driver_value(twin_payload, "mission_discipline")

    readiness = {
        "score": score,
        "coverage_pct": (
            coverage
            if coverage is not None
            else float(legacy_readiness.get("coverage_pct") or 0.0)
        ),
        "avg_mastery": (
            mastery
            if mastery is not None
            else float(legacy_readiness.get("avg_mastery") or 0.0)
        ),
        "review_discipline": (
            discipline
            if discipline is not None
            else float(legacy_readiness.get("review_discipline") or 0.0)
        ),
        "total_topics": int(legacy_readiness.get("total_topics") or 0),
        "topics_started": int(legacy_readiness.get("topics_started") or 0),
        "topics_mastered": int(legacy_readiness.get("topics_mastered") or 0),
        "source_authority": SOURCE_AUTHORITY_READINESS_INTELLIGENCE,
        "confidence_level": str(twin_payload.get("confidence_level") or "").strip(),
    }

    weakest: list[dict[str, Any]] = []
    for area in twin_payload.get("weakest_areas") or []:
        row = _area_to_topic_row(area)
        if row is not None:
            weakest.append(row)
        if len(weakest) >= max(0, int(weak_limit)):
            break

    strongest: list[dict[str, Any]] = []
    for area in twin_payload.get("strongest_areas") or []:
        row = _area_to_topic_row(area)
        if row is not None:
            strongest.append(row)
        if len(strongest) >= max(0, int(strong_limit)):
            break

    codes = list(_limitation_codes(twin_payload))
    return {
        "readiness": readiness,
        "weakest_topics": weakest,
        "strongest_topics": strongest,
        "source_authority": SOURCE_AUTHORITY_READINESS_INTELLIGENCE,
        "confidence_level": str(twin_payload.get("confidence_level") or "").strip(),
        "limitations_codes": codes,
        "readiness_drivers": list(twin_payload.get("readiness_drivers") or []),
        "recommended_next_actions": list(
            twin_payload.get("recommended_next_actions") or []
        ),
        "explainability": dict(twin_payload.get("explainability") or {}),
    }


def _topic_ids(rows: Any) -> tuple[str, ...]:
    if not isinstance(rows, list):
        return ()
    ids: list[str] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        topic_id = str(row.get("topic_id") or "").strip()
        if topic_id and topic_id not in seen:
            seen.add(topic_id)
            ids.append(topic_id)
    return tuple(ids)


def _score_agreement(legacy_score: float | None, twin_score: float | None) -> bool:
    if legacy_score is None and twin_score is None:
        return True
    if legacy_score is None or twin_score is None:
        return False
    return abs(float(legacy_score) - float(twin_score)) <= _SCORE_AGREEMENT_TOLERANCE


def assess_readiness_semantic_alignment(
    *,
    legacy_surface: dict[str, Any],
    twin_payload: dict[str, Any] | None,
    served_twin: bool,
    fallback_reason: str | None,
) -> dict[str, Any]:
    """Semantic readiness alignment (score / confidence / limitations / areas)."""
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
        legacy_readiness = legacy_surface.get("readiness") or {}
        try:
            legacy_score = (
                float(legacy_readiness["score"])
                if isinstance(legacy_readiness, dict)
                and legacy_readiness.get("score") is not None
                else None
            )
        except (TypeError, ValueError):
            legacy_score = None
        try:
            twin_score = (
                float(twin_payload["readiness_score"])
                if twin_payload.get("readiness_score") is not None
                else None
            )
        except (TypeError, ValueError):
            twin_score = None

        readiness_ok = _score_agreement(legacy_score, twin_score)
        legacy_areas = set(
            _topic_ids(legacy_surface.get("weakest_topics"))
            + _topic_ids(legacy_surface.get("strongest_topics"))
        )
        twin_areas = set(
            _topic_ids(twin_payload.get("weakest_areas"))
            + _topic_ids(twin_payload.get("strongest_areas"))
        )
        area_ok = bool(legacy_areas & twin_areas) or (
            not legacy_areas and not twin_areas
        )
        status = (
            ALIGNMENT_ALIGNED if (readiness_ok and area_ok) else ALIGNMENT_MISMATCHED
        )

    twin_score_out: float | None = None
    confidence = ""
    if isinstance(twin_payload, dict):
        confidence = str(twin_payload.get("confidence_level") or "").strip()
        if twin_payload.get("readiness_score") is not None:
            try:
                twin_score_out = float(twin_payload["readiness_score"])
            except (TypeError, ValueError):
                twin_score_out = None

    legacy_readiness = (
        legacy_surface.get("readiness")
        if isinstance(legacy_surface.get("readiness"), dict)
        else {}
    )
    try:
        legacy_score_out = (
            float(legacy_readiness["score"])
            if legacy_readiness.get("score") is not None
            else None
        )
    except (TypeError, ValueError):
        legacy_score_out = None

    return {
        "alignment_status": status,
        "aligned": status == ALIGNMENT_ALIGNED,
        "mismatched": status == ALIGNMENT_MISMATCHED,
        "readiness_agreement": _score_agreement(legacy_score_out, twin_score_out),
        "confidence_agreement": (
            bool(confidence) if twin_score_out is not None else True
        ),
        "limitation_agreement": status != ALIGNMENT_MISMATCHED
        or fallback_reason != FALLBACK_BLOCKING_LIMITATION,
        "legacy_score": legacy_score_out,
        "twin_score": twin_score_out,
        "confidence_level": confidence,
        "twin_topic_ids": list(
            _topic_ids((twin_payload or {}).get("weakest_areas"))
            + _topic_ids((twin_payload or {}).get("strongest_areas"))
        ),
        "legacy_row_count": len(legacy_surface.get("weakest_topics") or [])
        + len(legacy_surface.get("strongest_topics") or []),
    }


def _build_legacy_surface(
    user_id: int,
    *,
    weak_limit: int,
    strong_limit: int,
    get_overall_readiness: Any | None = None,
    get_weakest_topics: Any | None = None,
    get_strongest_topics: Any | None = None,
) -> dict[str, Any]:
    from app.services.readiness_service import ReadinessService

    overall = get_overall_readiness or ReadinessService.get_overall_readiness
    weakest = get_weakest_topics or ReadinessService.get_weakest_topics
    strongest = get_strongest_topics or ReadinessService.get_strongest_topics
    return {
        "readiness": dict(overall(user_id) or {}),
        "weakest_topics": list(weakest(user_id, limit=weak_limit) or []),
        "strongest_topics": list(strongest(user_id, limit=strong_limit) or []),
        "source_authority": "legacy",
        "confidence_level": "",
        "limitations_codes": [],
        "readiness_drivers": [],
        "recommended_next_actions": [],
        "explainability": {},
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
            return deepcopy(cached)
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
        cache[user_id] = deepcopy(surface)
    except Exception:  # noqa: BLE001
        return


def _trim_surface(
    surface: dict[str, Any],
    *,
    weak_limit: int,
    strong_limit: int,
) -> dict[str, Any]:
    trimmed = deepcopy(surface)
    trimmed["weakest_topics"] = list(trimmed.get("weakest_topics") or [])[
        : max(0, int(weak_limit))
    ]
    trimmed["strongest_topics"] = list(trimmed.get("strongest_topics") or [])[
        : max(0, int(strong_limit))
    ]
    return trimmed


def run_readiness_intelligence_http_cutover(
    user_id: int,
    *,
    weak_limit: int = 5,
    strong_limit: int = 5,
    telemetry: ConsumerChainTelemetry | None = None,
    environ: dict[str, str] | None = None,
    build_readiness_intelligence: Any | None = None,
    get_overall_readiness: Any | None = None,
    get_weakest_topics: Any | None = None,
    get_strongest_topics: Any | None = None,
    skip_request_dedupe: bool = False,
) -> dict[str, Any]:
    """Return Readiness Intelligence projection or legacy surface (fail-open).

    Always returns a surface dict. Twin failures / blocking states fall back
    to legacy getters.
    """
    env = environ if environ is not None else dict(os.environ)
    sink = telemetry or get_consumer_chain_telemetry()
    flags = resolve_v2_feature_flags(environ=env)
    flask_env = str(env.get("FLASK_ENV", "development")).strip().lower()
    app_env = str(env.get("APP_ENV", flask_env)).strip().lower() or "development"
    ids = CorrelationContext.current()

    from app.services.readiness_service import ReadinessService

    twin_builder = (
        build_readiness_intelligence or ReadinessService.build_readiness_intelligence
    )

    ineligible = readiness_cutover_ineligibility_reason(environ=env)
    if ineligible is not None:
        legacy_started = time.perf_counter()
        legacy = _build_legacy_surface(
            user_id,
            weak_limit=weak_limit,
            strong_limit=strong_limit,
            get_overall_readiness=get_overall_readiness,
            get_weakest_topics=get_weakest_topics,
            get_strongest_topics=get_strongest_topics,
        )
        legacy_latency_ms = (time.perf_counter() - legacy_started) * 1000.0
        alignment = assess_readiness_semantic_alignment(
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
            return _trim_surface(
                cached, weak_limit=weak_limit, strong_limit=strong_limit
            )

    build_weak = max(5, int(weak_limit))
    build_strong = max(5, int(strong_limit))

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
                weak_limit=build_weak,
                strong_limit=build_strong,
                get_overall_readiness=get_overall_readiness,
                get_weakest_topics=get_weakest_topics,
                get_strongest_topics=get_strongest_topics,
            )
        except Exception:  # noqa: BLE001
            logger.exception(
                "readiness_cutover_legacy_failed user_id=%s", user_id
            )
            legacy = {
                "readiness": {
                    "score": 0.0,
                    "coverage_pct": 0.0,
                    "avg_mastery": 0.0,
                    "review_discipline": 0.0,
                    "total_topics": 0,
                    "topics_started": 0,
                    "topics_mastered": 0,
                },
                "weakest_topics": [],
                "strongest_topics": [],
                "source_authority": "legacy",
                "confidence_level": "",
                "limitations_codes": [],
                "readiness_drivers": [],
                "recommended_next_actions": [],
                "explainability": {},
            }
        legacy_latency_ms = (time.perf_counter() - legacy_started) * 1000.0

        twin_started = time.perf_counter()
        try:
            twin_payload = twin_builder(user_id)
        except Exception:  # noqa: BLE001 — never break student path
            twin_exception = True
            twin_payload = None
            fallback_reason = FALLBACK_TWIN_EXCEPTION
            logger.debug(
                "readiness_cutover_twin_failed user_id=%s",
                user_id,
                exc_info=True,
            )
        twin_latency_ms = (time.perf_counter() - twin_started) * 1000.0

        if fallback_reason is None and twin_payload is None:
            fallback_reason = FALLBACK_TWIN_UNAVAILABLE
        elif fallback_reason is None and has_readiness_blocking_limitation(
            twin_payload
        ):
            fallback_reason = FALLBACK_BLOCKING_LIMITATION

        projected: dict[str, Any] | None = None
        if fallback_reason is None and isinstance(twin_payload, dict):
            projected = project_readiness_intelligence_to_surface(
                twin_payload,
                legacy_surface=legacy,
                weak_limit=build_weak,
                strong_limit=build_strong,
            )
            if projected is None:
                fallback_reason = FALLBACK_PROJECTION_EMPTY

        if fallback_reason is None and projected is not None:
            served = projected
            cutover_served = True
        else:
            served = deepcopy(legacy)
            cutover_served = False

        alignment = assess_readiness_semantic_alignment(
            legacy_surface=legacy,
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
        return _trim_surface(
            served, weak_limit=weak_limit, strong_limit=strong_limit
        )
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
        "api_name": API_BUILD_READINESS_INTELLIGENCE,
        "student_id": str(user_id),
        "environment": app_env,
        "cutover_attempted": bool(cutover_attempted),
        "cutover_served": bool(cutover_served),
        "influences_student": bool(cutover_served),
        "fallback_reason": fallback_reason or "",
        "alignment_status": alignment.get("alignment_status") or "",
        "aligned": bool(alignment.get("aligned")),
        "mismatched": bool(alignment.get("mismatched")),
        "readiness_agreement": bool(alignment.get("readiness_agreement")),
        "confidence_agreement": bool(alignment.get("confidence_agreement")),
        "limitation_agreement": bool(alignment.get("limitation_agreement")),
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
        "cutover_enabled": bool(flags.ENABLE_READINESS_INTELLIGENCE_CUTOVER),
        "twin_exception": bool(twin_exception),
        "correlation_id": correlation_id,
        "causation_id": causation_id,
    }
    try:
        sink.emit_cutover(**{
            k: v
            for k, v in payload.items()
            if k
            not in {
                "readiness_agreement",
                "confidence_agreement",
                "limitation_agreement",
            }
        })
    except Exception:  # noqa: BLE001
        logger.debug("readiness_cutover_telemetry_failed", exc_info=True)
    try:
        from app.infrastructure.adapters.consumer_chain import (
            readiness_cutover_health as _health,
        )

        _health.get_readiness_cutover_health_metrics().record(payload)
    except Exception:  # noqa: BLE001
        logger.debug("readiness_cutover_metrics_failed", exc_info=True)

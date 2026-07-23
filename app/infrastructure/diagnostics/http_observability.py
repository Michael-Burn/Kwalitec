"""HTTP request observability — correlation IDs, timing, presentation errors.

Wires Internal Alpha operational logging at the Flask boundary without
touching educational domain models.
"""

from __future__ import annotations

import logging
import time
from uuid import uuid4

from flask import Flask, g, request

from app.infrastructure.diagnostics.correlation import CorrelationContext

logger = logging.getLogger("kwalitec.observability")

CORRELATION_HEADER = "X-Correlation-ID"
REQUEST_ID_HEADER = "X-Request-ID"


def register_http_observability(app: Flask) -> None:
    """Attach before/after request hooks for correlation and timing."""

    @app.before_request
    def _alpha_observability_before():
        if _is_static_request():
            return None
        incoming = (
            (request.headers.get(CORRELATION_HEADER) or "").strip()
            or (request.headers.get(REQUEST_ID_HEADER) or "").strip()
        )
        tokens = CorrelationContext.set(correlation_id=incoming or None)
        g._alpha_correlation_tokens = tokens
        g.correlation_id = CorrelationContext.get_correlation_id()
        g._alpha_request_started = time.perf_counter()
        return None

    @app.after_request
    def _alpha_observability_after(response):
        if _is_static_request():
            return response
        correlation_id = getattr(g, "correlation_id", None) or ""
        if correlation_id:
            response.headers.setdefault(CORRELATION_HEADER, correlation_id)
            response.headers.setdefault(REQUEST_ID_HEADER, correlation_id)

        started = getattr(g, "_alpha_request_started", None)
        if started is not None:
            duration_ms = round((time.perf_counter() - started) * 1000, 1)
            logger.info(
                "http_request method=%s path=%s status=%s duration_ms=%s "
                "correlation_id=%s",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
                correlation_id or "-",
            )
            threshold = float(
                app.config.get("SLOW_REQUEST_THRESHOLD_MS", 1000) or 1000
            )
            if duration_ms >= threshold:
                logger.warning(
                    "slow_request method=%s path=%s status=%s duration_ms=%s "
                    "threshold_ms=%s correlation_id=%s",
                    request.method,
                    request.path,
                    response.status_code,
                    duration_ms,
                    threshold,
                    correlation_id or "-",
                )
        return response

    @app.teardown_request
    def _alpha_observability_teardown(exc):
        tokens = getattr(g, "_alpha_correlation_tokens", None)
        if tokens is not None:
            # Flask may invoke teardown more than once for the same context.
            g._alpha_correlation_tokens = None
            try:
                CorrelationContext.reset(tokens)
            except (RuntimeError, ValueError):
                pass
        if exc is not None and not _is_static_request():
            correlation_id = getattr(g, "correlation_id", None) or "-"
            logger.error(
                "presentation_error path=%s method=%s correlation_id=%s "
                "error=%s",
                request.path,
                request.method,
                correlation_id,
                exc.__class__.__name__,
            )


def allocate_error_reference_id() -> str:
    """Allocate a short user-facing error reference id."""
    existing = ""
    try:
        existing = CorrelationContext.get_correlation_id()
    except Exception:  # noqa: BLE001
        existing = ""
    if existing:
        return existing[:12].upper()
    return uuid4().hex[:12].upper()


def _is_static_request() -> bool:
    endpoint = request.endpoint or ""
    if endpoint == "static" or endpoint.endswith(".static"):
        return True
    path = request.path or ""
    return path.startswith("/static/")

"""GA-001 WS7 — observability validation (health, correlation, logs, telemetry)."""

from __future__ import annotations

import logging

from app.infrastructure.diagnostics.http_observability import (
    allocate_error_reference_id,
)
from app.services.presentation_telemetry_service import PresentationTelemetryService
from tests.ga.helpers import login_as, make_founder, make_student, wire_studio


class TestHealthObservability:
    def test_live_ready_details_contract(self, client) -> None:
        live = client.get("/health/live").get_json()
        assert live["status"] == "ok"
        assert "version" in live

        ready = client.get("/health/ready")
        assert ready.status_code in {200, 503}
        ready_body = ready.get_json()
        assert "ready" in ready_body
        assert "components" in ready_body

        details = client.get("/health/details")
        assert details.status_code in {200, 503}
        body = details.get_json()
        assert "dead_letters" in body
        assert "alerts" in body
        assert "slow_request_threshold_ms" in body["alerts"]


class TestCorrelationIds:
    def test_echoes_incoming_correlation_id(self, client) -> None:
        response = client.get(
            "/health/live",
            headers={"X-Correlation-ID": "ga-corr-12345"},
        )
        assert response.status_code == 200
        assert response.headers.get("X-Correlation-ID") == "ga-corr-12345"
        assert response.headers.get("X-Request-ID") == "ga-corr-12345"

    def test_generates_correlation_id_when_absent(self, client) -> None:
        response = client.get("/health/live")
        assert response.status_code == 200
        cid = response.headers.get("X-Correlation-ID")
        assert cid
        assert len(cid) >= 8


class TestSlowRequestLogging:
    def test_slow_request_emits_warning(self, app, client, caplog) -> None:
        # Negative threshold forces the slow_request branch for every timed request.
        app.config["SLOW_REQUEST_THRESHOLD_MS"] = -1
        with caplog.at_level(logging.WARNING):
            client.get("/health/live")
        messages = [record.getMessage() for record in caplog.records]
        assert any("slow_request" in message for message in messages), messages


class TestStructuredLogsAndTelemetry:
    def test_http_request_structured_log(self, client, caplog) -> None:
        with caplog.at_level(logging.INFO, logger="kwalitec.observability"):
            client.get("/health/live")
        assert any("http_request" in record.getMessage() for record in caplog.records)

    def test_telemetry_ingest(self, client, ctx) -> None:
        user = make_student("ga-telemetry@kwalitec.example")
        login_as(client, "ga-telemetry@kwalitec.example")
        response = client.post(
            "/alpha/telemetry",
            data={"event_type": "coach_opened", "surface": "home"},
        )
        assert response.status_code == 200
        assert response.get_json()["ok"] is True
        events = PresentationTelemetryService.recent(user_id=user.id, limit=5)
        assert any(event.event_type == "coach_opened" for event in events)


class TestPlatformIntelligenceAndReferences:
    def test_platform_intelligence_surface(self, client, ctx, app) -> None:
        make_founder("ga-obs-founder@kwalitec.example")
        wire_studio(app)
        app.config["FOUNDER_EMAILS"] = ""
        login_as(client, "ga-obs-founder@kwalitec.example")
        response = client.get("/console/alpha-observability")
        assert response.status_code == 200

    def test_error_reference_id_format(self) -> None:
        ref = allocate_error_reference_id()
        assert isinstance(ref, str)
        assert len(ref) >= 6

    def test_404_includes_reference(self, client) -> None:
        response = client.get("/definitely-not-a-real-ga-path-xyz")
        assert response.status_code == 404
        html = response.get_data(as_text=True).lower()
        assert "reference" in html or "not found" in html

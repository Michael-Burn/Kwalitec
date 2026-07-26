"""Analytics event validation (schema + privacy envelope checks)."""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.infrastructure.analytics.contracts import AnalyticsEvent
from app.infrastructure.analytics.registry import AnalyticsEventRegistry
from app.infrastructure.analytics.versioning import AnalyticsEventVersion

# PRD-001 §7.4 / §10 — hard reject above 8 KiB serialized payload+envelope body.
MAX_PAYLOAD_BYTES = 8 * 1024


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating an analytics event."""

    ok: bool
    errors: tuple[str, ...] = ()

    @classmethod
    def success(cls) -> ValidationResult:
        return cls(ok=True, errors=())

    @classmethod
    def failure(cls, *errors: str) -> ValidationResult:
        return cls(ok=False, errors=tuple(errors))


class AnalyticsEventValidator:
    """Validate envelope fields, allowlist membership, and size budget."""

    def __init__(self, registry: AnalyticsEventRegistry) -> None:
        self._registry = registry

    def validate(self, event: AnalyticsEvent) -> ValidationResult:
        """Return success or a list of validation errors (never raises)."""
        errors: list[str] = []

        if not (event.event_type or "").strip():
            errors.append("event_type is required")
        elif not self._registry.is_known(event.event_type):
            errors.append(f"unknown event_type: {event.event_type}")

        if event.user_id is None or int(event.user_id) < 1:
            errors.append("user_id must be a positive integer")

        if not (event.event_id or "").strip():
            errors.append("event_id is required")

        if not (event.idempotency_key or "").strip():
            errors.append("idempotency_key is required")

        try:
            AnalyticsEventVersion.coerce(event.schema_version)
        except ValueError:
            errors.append(f"unsupported schema_version: {event.schema_version}")

        registration = self._registry.get(event.event_type)
        if registration is not None:
            missing = [
                k
                for k in registration.required_payload_keys
                if k not in (event.payload or {})
            ]
            if missing:
                errors.append(f"payload missing required keys: {missing}")
            current = int(registration.current_version)
            if int(event.schema_version) > current:
                errors.append(
                    f"schema_version {int(event.schema_version)} newer than "
                    f"supported {current} for {event.event_type}"
                )

        # Reject free-text-ish oversized string values in payload (privacy).
        for key, value in (event.payload or {}).items():
            if isinstance(value, str) and len(value) > 512:
                errors.append(f"payload field too large: {key}")

        try:
            encoded = json.dumps(
                event.payload or {},
                separators=(",", ":"),
                sort_keys=True,
                default=str,
            ).encode("utf-8")
            if len(encoded) > MAX_PAYLOAD_BYTES:
                errors.append(
                    f"payload exceeds {MAX_PAYLOAD_BYTES} bytes "
                    f"({len(encoded)} bytes)"
                )
        except (TypeError, ValueError) as exc:
            errors.append(f"payload not JSON-serializable: {exc}")

        if errors:
            return ValidationResult.failure(*errors)
        return ValidationResult.success()

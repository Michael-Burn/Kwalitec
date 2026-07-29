"""Feature flags for the Founder → Student bridge (PI-002A).

Safe defaults keep Runtime A as the sole live enrolment path. Runtime C
discovery and enrolment are additive and must be enabled explicitly via
environment variables — no code change required for rollout.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _env_truthy(name: str, *, environ: dict[str, str] | None = None) -> bool:
    env = environ if environ is not None else os.environ
    return env.get(name, "").strip().lower() in _TRUTHY


def _parse_allowlist(
    raw: str | None,
) -> frozenset[str]:
    if not raw or not str(raw).strip():
        return frozenset()
    return frozenset(
        part.strip().upper()
        for part in str(raw).split(",")
        if part.strip()
    )


@dataclass(frozen=True)
class FounderStudentBridgeFlags:
    """Immutable rollout switches for PI-002A.

    Attributes:
        ENABLE_PUBLISHED_SUBJECT_DISCOVERY: Surface active published packages
            in the student subject catalogue / wizard.
        ENABLE_RUNTIME_C_ENROLMENT: Allow enrolment against Runtime C for
            subjects that routing selects.
        RUNTIME_C_SUBJECT_ALLOWLIST: Optional subject codes that may route
            to Runtime C even when selected from the legacy catalogue
            (empty = only the Published category routes to Runtime C).
    """

    ENABLE_PUBLISHED_SUBJECT_DISCOVERY: bool = False
    ENABLE_RUNTIME_C_ENROLMENT: bool = False
    RUNTIME_C_SUBJECT_ALLOWLIST: frozenset[str] = frozenset()

    @property
    def bridge_active(self) -> bool:
        """True when any bridge surface is enabled."""
        return (
            self.ENABLE_PUBLISHED_SUBJECT_DISCOVERY
            or self.ENABLE_RUNTIME_C_ENROLMENT
        )


def resolve_founder_student_bridge_flags(
    *,
    environ: dict[str, str] | None = None,
) -> FounderStudentBridgeFlags:
    """Resolve PI-002A flags from the process environment.

    Environment variables:
        ``KWALITEC_FOUNDER_STUDENT_BRIDGE`` — umbrella; enables discovery +
        Runtime C enrolment.
        ``KWALITEC_PUBLISHED_SUBJECT_DISCOVERY`` — discovery only.
        ``KWALITEC_RUNTIME_C_ENROLMENT`` — Runtime C enrolment only.
        ``KWALITEC_RUNTIME_C_SUBJECT_ALLOWLIST`` — comma-separated subject
        codes eligible for Runtime C when selected outside the Published
        category (still requires enrolment flag + active package).

    Development default: when APP_ENV is ``development`` and no bridge flags
    are set, enable discovery + enrolment so Founder publish → Ready is
    observable locally. Explicit empty environ (tests) and non-development
    environments keep safe defaults off.
    """
    env = environ if environ is not None else os.environ
    # Explicit empty mapping (unit tests) must keep safe defaults off.
    if environ is not None and not environ:
        return FounderStudentBridgeFlags()

    app_env = (
        env.get("APP_ENV") or env.get("FLASK_ENV") or "development"
    ).strip().lower()
    bridge_raw = env.get("KWALITEC_FOUNDER_STUDENT_BRIDGE")
    discovery_raw = env.get("KWALITEC_PUBLISHED_SUBJECT_DISCOVERY")
    enrolment_raw = env.get("KWALITEC_RUNTIME_C_ENROLMENT")
    any_explicit = any(
        v is not None and str(v).strip() != ""
        for v in (bridge_raw, discovery_raw, enrolment_raw)
    )
    development_default = app_env == "development" and not any_explicit

    umbrella = _env_truthy("KWALITEC_FOUNDER_STUDENT_BRIDGE", environ=env) or (
        development_default
    )
    discovery = (
        _env_truthy("KWALITEC_PUBLISHED_SUBJECT_DISCOVERY", environ=env)
        or umbrella
    )
    enrolment = (
        _env_truthy("KWALITEC_RUNTIME_C_ENROLMENT", environ=env) or umbrella
    )
    allowlist = _parse_allowlist(
        env.get("KWALITEC_RUNTIME_C_SUBJECT_ALLOWLIST")
    )
    return FounderStudentBridgeFlags(
        ENABLE_PUBLISHED_SUBJECT_DISCOVERY=discovery,
        ENABLE_RUNTIME_C_ENROLMENT=enrolment,
        RUNTIME_C_SUBJECT_ALLOWLIST=allowlist,
    )

"""Version 2 dual-run / cutover feature flags.

Environment-driven switches for coexistence until V2-020 retirement.
Safe defaults preserve Version 1 as the live educational path.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _env_truthy(name: str, *, environ: dict[str, str] | None = None) -> bool:
    env = environ if environ is not None else os.environ
    return env.get(name, "").strip().lower() in _TRUTHY


@dataclass(frozen=True)
class Version2FeatureFlags:
    """Immutable Version 2 rollout switches (ADR-007 dual-run).

    Attributes:
        ENABLE_STUDENT_EXPERIENCE: Expose /student and dashboard entry link.
        ENABLE_DURABLE_STORE: Persist Experience/Session docs via SQLAlchemy.
        SEED_DEMO_LEARNERS: Auto-seed demo opaque projections (dev/demo only).
        INJECT_PHASE_I_ENGINES: Wire opaque engine bridges into adapters.
        SOLE_RUNTIME: Route default home to /student (V2-020 gated cutover).
        ENABLE_FOUNDER_INTELLIGENCE: Show journey-level Founder Intelligence.
    """

    ENABLE_STUDENT_EXPERIENCE: bool = False
    ENABLE_DURABLE_STORE: bool = False
    SEED_DEMO_LEARNERS: bool = True
    INJECT_PHASE_I_ENGINES: bool = False
    SOLE_RUNTIME: bool = False
    ENABLE_FOUNDER_INTELLIGENCE: bool = False


def resolve_v2_feature_flags(
    *,
    environ: dict[str, str] | None = None,
) -> Version2FeatureFlags:
    """Resolve Version 2 flags from the process environment."""
    durable = _env_truthy("KWALITEC_V2_DURABLE_STORE", environ=environ)
    sole = _env_truthy("KWALITEC_V2_SOLE_RUNTIME", environ=environ)
    student = _env_truthy("KWALITEC_V2_STUDENT_EXPERIENCE", environ=environ) or sole
    # Production dual-run should not seed demo learners when durable store is on
    # unless explicitly requested.
    seed_explicit = environ.get("KWALITEC_V2_SEED_DEMO") if environ else None
    if seed_explicit is None and environ is None:
        seed_explicit = os.environ.get("KWALITEC_V2_SEED_DEMO")
    if seed_explicit is not None and str(seed_explicit).strip() != "":
        seed = str(seed_explicit).strip().lower() in _TRUTHY
    else:
        seed = not durable
    return Version2FeatureFlags(
        ENABLE_STUDENT_EXPERIENCE=student,
        ENABLE_DURABLE_STORE=durable,
        SEED_DEMO_LEARNERS=seed,
        INJECT_PHASE_I_ENGINES=_env_truthy(
            "KWALITEC_V2_INJECT_ENGINES", environ=environ
        )
        or durable,
        SOLE_RUNTIME=sole,
        ENABLE_FOUNDER_INTELLIGENCE=_env_truthy(
            "KWALITEC_V2_FOUNDER_INTELLIGENCE", environ=environ
        ),
    )


# Process default — resolved at import for convenience; prefer resolve_* in apps.
V2_FEATURE_FLAGS = resolve_v2_feature_flags()

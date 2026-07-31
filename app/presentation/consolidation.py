"""Legacy presentation redirects for sole-runtime Education OS.

READY FOR MIGRATION shells stay registered but send learners to the
canonical Student Experience when ``KWALITEC_V2_SOLE_RUNTIME`` is set.
Protected educational engines and V1 data paths are not deleted.

EP-007.1 — Student Journey Consolidation: helpers resolve the single
authoritative home endpoint so login, completion, and chrome never present
two competing homes under sole runtime.

RC-2026.07.29-03 — Student shell unification: ``layouts/base.html``
always routes student-facing templates into ``layouts/eos_student.html``.
Legacy workspace chrome and runtime shell switching are retired.
``SOLE_RUNTIME`` still governs home redirects only. Controllers and
engines unchanged.

Role-aware landing (UX-001 / FV-001B): Founder and Administrator Console
operators resolve ``canonical_home`` to the Kwalitec Console for bare
``/`` and login fallbacks. Dual-access users choose via Experience
Selection after login.

Student-journey completions (Baseline finalize, onboarding done, activate
plan, Start Session failure recovery) must use
``redirect_to_student_home`` — never yank a learner mid-flow into Console
because their account also has Founder access.
"""

from __future__ import annotations

from flask import redirect, url_for

from app.application.config import v2_flags as _v2_flags

# Canonical student journey entry (Education OS Home).
CANONICAL_HOME_ENDPOINT = "student.home"
# Legacy dual-run home (Learning Workspace Dashboard).
LEGACY_HOME_ENDPOINT = "dashboard.index"
# Kwalitec Console (Founder Operating System) home.
CONSOLE_HOME_ENDPOINT = "founder_dashboard.index"


def resolve_v2_feature_flags(*args, **kwargs):
    """Proxy so patches on this module or on ``v2_flags`` both apply."""
    return _v2_flags.resolve_v2_feature_flags(*args, **kwargs)


def is_sole_runtime() -> bool:
    """True when dual-home presentation is retired for this process."""
    return bool(resolve_v2_feature_flags().SOLE_RUNTIME)


def canonical_home_endpoint() -> str:
    """Return the authoritative home Flask endpoint for the current user/flags.

    Founder / Console users: ``founder_dashboard.index`` (Kwalitec Console).
    Under sole runtime (students): ``student.home`` (dual-home removed).
    Otherwise: ``dashboard.index`` (dual-run soak / Internal Alpha rollback).
    """
    if _current_user_is_founder():
        return CONSOLE_HOME_ENDPOINT
    if is_sole_runtime():
        return CANONICAL_HOME_ENDPOINT
    return LEGACY_HOME_ENDPOINT


def canonical_home_url(**values) -> str:
    """URL for the authoritative home (Console for founders, student otherwise)."""
    return url_for(canonical_home_endpoint(), **values)


def redirect_to_canonical_home(**values):
    """Redirect to the authoritative home for the current user and flag posture."""
    return redirect(canonical_home_url(**values))


def student_home_url(**values) -> str:
    """Always Student Experience Home — ignore Founder Console RBAC."""
    return url_for(CANONICAL_HOME_ENDPOINT, **values)


def redirect_to_student_home(**values):
    """Stay in Student Experience after a student-product action.

    Use after Baseline finalize, student onboarding, plan activation, and
    similar flows. Do not use ``redirect_to_canonical_home`` there — that
    sends dual-access Founders to Console.
    """
    return redirect(student_home_url(**values))


def _current_user_is_founder() -> bool:
    """Safe RBAC check — False outside a request or when unauthenticated."""
    try:
        from app.founder.dashboard.access import is_founder_user

        return bool(is_founder_user())
    except RuntimeError:
        return False


def redirect_if_sole_runtime(endpoint: str = CANONICAL_HOME_ENDPOINT, **values):
    """Return a redirect to the canonical surface when sole runtime is on.

    Returns None when dual-run / legacy default is active so callers continue.
    """
    if is_sole_runtime():
        return redirect(url_for(endpoint, **values))
    return None


def canonical_session_entry_endpoint() -> str:
    """Primary study-start surface for the current flag posture.

    Sole runtime: Student Home (session start is POST from Home).
    Dual-run: legacy mission hub (Dashboard → Missions path).
    """
    if is_sole_runtime():
        return CANONICAL_HOME_ENDPOINT
    return "mission.missions"


def canonical_session_entry_url(**values) -> str:
    """URL for the primary study-start / continue surface."""
    return url_for(canonical_session_entry_endpoint(), **values)

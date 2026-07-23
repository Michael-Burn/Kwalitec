"""Shared helpers and budgets for GA-001 readiness tests."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.extensions import db
from app.models.user import User
from app.security.capabilities import Capability
from app.security.roles import Role
from app.services.identity_service import IdentityService
from tests.operational.helpers import (
    login_founder,
    login_student,
    wire_session,
    wire_student,
    wire_studio,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

# Critical path surfaces for release-candidate validation (legacy production app).
GA_STUDENT_WORKFLOWS: tuple[tuple[str, str], ...] = (
    ("student_home", "/student/"),
    ("journey", "/student/journey"),
    ("revision_planner", "/student/revision"),
    ("history", "/student/history"),
    ("profile", "/student/profile"),
    ("dashboard", "/dashboard/"),
    ("missions", "/missions/"),
    ("study_plan", "/study-plan/"),
    ("analytics_readiness", "/analytics/"),
    ("settings", "/settings/"),
    ("support_help", "/alpha/help"),
    ("alpha_onboarding", "/alpha/onboarding"),
)

GA_CONSOLE_WORKFLOWS: tuple[tuple[str, str], ...] = (
    ("console_home", "/console/"),
    ("platform_intelligence", "/console/alpha-observability"),
    ("learning_signals", "/console/intelligence"),
    ("operational_health", "/console/operational-health"),
    ("evidence_gates", "/console/evidence-gates"),
    ("feedback", "/console/feedback"),
    ("releases", "/console/releases"),
    ("console_settings", "/console/settings"),
    ("studio", "/console/studio/"),
)

GA_HEALTH_ENDPOINTS = (
    "/health/live",
    "/health/ready",
    "/health",
    "/health/details",
)

# Soft HTTP budgets (ms) — conservative for CI runners.
GA_PERF_BUDGETS_MS: dict[str, float] = {
    "student_dashboard": 2500.0,
    "workspace_session": 2500.0,
    "journey": 2500.0,
    "console_home": 3500.0,
    "platform_intelligence": 3500.0,
    "health_live": 500.0,
    "health_ready": 1500.0,
}

# Soft SQL statement budgets for hot paths (SQLite test harness).
GA_SQL_BUDGETS: dict[str, int] = {
    "student_dashboard": 80,
    "journey": 80,
    "console_home": 120,
    "platform_intelligence": 120,
    "health_ready": 40,
}

REQUIRED_PRODUCTION_DOCS = (
    "docs/production/README.md",
    "docs/production/DEPLOYMENT.md",
    "docs/production/ENVIRONMENT.md",
    "docs/production/RUNBOOK.md",
    "docs/production/INCIDENT_RESPONSE.md",
    "docs/production/RELEASE_PROCESS.md",
    "docs/production/VERSIONING_POLICY.md",
    "docs/production/CONSOLE_OPERATIONS.md",
    "docs/production/BACKUP_AND_RECOVERY.md",
    "docs/production/ACCESSIBILITY_AUDIT.md",
)

REQUIRED_GA_DOCS = (
    "docs/ga/README.md",
    "docs/ga/RELEASE_CHECKLIST.md",
    "docs/ga/CERTIFICATION_REPORT.md",
    "docs/ga/SECURITY_REVIEW.md",
    "docs/ga/PERFORMANCE_BASELINE.md",
    "docs/ga/WORKFLOW_VALIDATION.md",
)

REQUIRED_GA_CHECKLIST_SECTIONS = (
    "Configuration",
    "Database",
    "Health",
    "Telemetry",
    "Background jobs",
    "Console",
    "Student portal",
    "Rollback",
)


@dataclass(frozen=True)
class TimedResult:
    """Outcome of a timed callable."""

    label: str
    duration_ms: float
    budget_ms: float
    value: Any = None

    @property
    def within_budget(self) -> bool:
        return self.duration_ms <= self.budget_ms


def time_call(label: str, fn: Callable[[], Any], budget_ms: float) -> TimedResult:
    started = time.perf_counter()
    value = fn()
    duration_ms = (time.perf_counter() - started) * 1000.0
    return TimedResult(
        label=label,
        duration_ms=duration_ms,
        budget_ms=budget_ms,
        value=value,
    )


def make_student(email: str = "ga-student@kwalitec.example") -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    user.alpha_onboarding_skipped = False
    db.session.add(user)
    db.session.commit()
    IdentityService.ensure_student_defaults(user)
    db.session.refresh(user)
    return user


def make_founder(email: str = "ga-founder@kwalitec.example") -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    IdentityService.ensure_founder_admin(user)
    db.session.refresh(user)
    assert Role.FOUNDER in user.get_roles()
    assert Capability.CONSOLE in user.get_capabilities()
    return user


def login_as(client, email: str, password: str = "password123") -> None:
    client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


__all__ = [
    "GA_CONSOLE_WORKFLOWS",
    "GA_HEALTH_ENDPOINTS",
    "GA_PERF_BUDGETS_MS",
    "GA_SQL_BUDGETS",
    "GA_STUDENT_WORKFLOWS",
    "REPO_ROOT",
    "REQUIRED_GA_CHECKLIST_SECTIONS",
    "REQUIRED_GA_DOCS",
    "REQUIRED_PRODUCTION_DOCS",
    "TimedResult",
    "login_as",
    "login_founder",
    "login_student",
    "make_founder",
    "make_student",
    "time_call",
    "wire_session",
    "wire_student",
    "wire_studio",
]

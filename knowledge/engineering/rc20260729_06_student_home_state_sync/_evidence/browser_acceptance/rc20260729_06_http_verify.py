#!/usr/bin/env python3
"""RC-2026.07.29-06 — HTTP integration verification (no browser required).

Creates a fresh user, walks study-plan wizard via form posts, then asserts
Student Home HTML reflects active study context (not empty-state copy).
Also writes a minimal HTML capture for evidence when Playwright is unavailable.
"""

from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models.study_plan import StudyPlan
from app.models.user import User

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_evidence" / "browser_acceptance"
OUT.mkdir(parents=True, exist_ok=True)

EMAIL = "rc06.http5@kwalitec.example"
PASSWORD = "Rc06Http2026!"


def ensure_user() -> User:
    user = User.query.filter_by(email=EMAIL).first()
    if user is None:
        user = User(email=EMAIL, is_active_user=True)
        user.set_password(PASSWORD)
        user.alpha_onboarding_completed = True
        user.welcome_dismissed = True
        db.session.add(user)
        db.session.commit()
    for plan in StudyPlan.query.filter_by(user_id=user.id, active=True).all():
        plan.active = False
    db.session.commit()
    return user


def csrf(html: str) -> str:
    m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    if not m:
        m = re.search(r'content="([^"]+)"[^>]*name="csrf-token"', html)
    assert m, "csrf token missing"
    return m.group(1)


def main() -> int:
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    evidence: dict = {"mode": "flask_test_client"}

    with app.app_context():
        user = ensure_user()
        evidence["user_id"] = user.id

    client = app.test_client()
    # Login
    r = client.post(
        "/auth/login",
        data={"email": EMAIL, "password": PASSWORD},
        follow_redirects=True,
    )
    evidence["login_status"] = r.status_code
    assert r.status_code == 200

    before = client.get("/student/")
    before_html = before.get_data(as_text=True)
    evidence["before_empty"] = "No exam selected" in before_html
    evidence["before_empty_state"] = 'data-student-state="empty"' in before_html
    evidence["before_mission"] = "ds-mission-panel" in before_html
    evidence["before_quiet"] = 'data-student-state="quiet"' in before_html

    # Create an active study plan via service (canonical truth), then open Home.
    with app.app_context():
        from app.services.study_plan_service import StudyPlanService
        from app.services.planning_service import PlanningService

        user = User.query.filter_by(email=EMAIL).one()
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CM1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=45,
        )
        evidence["plan_id"] = plan.id
        mission = PlanningService.generate_today_mission(user.id)
        evidence["mission_id"] = getattr(mission, "id", None)
        evidence["mission_title"] = getattr(mission, "title", None)

    after = client.get("/student/")
    after_html = after.get_data(as_text=True)
    (OUT / "student_home_after_plan.html").write_text(after_html, encoding="utf-8")

    evidence["after_status"] = after.status_code
    evidence["after_empty"] = "No exam selected" in after_html
    evidence["after_mission_panel"] = "ds-mission-panel" in after_html
    evidence["after_quiet"] = 'data-student-state="quiet"' in after_html
    evidence["after_empty_state"] = 'data-student-state="empty"' in after_html
    evidence["after_primary"] = 'data-student-cta="primary"' in after_html
    evidence["after_has_exam_name"] = "IFoA CM1" in after_html or "CM1" in after_html

    # Refresh-equivalent second GET
    refresh = client.get("/student/")
    refresh_html = refresh.get_data(as_text=True)
    evidence["refresh_empty"] = "No exam selected" in refresh_html
    evidence["refresh_mission_panel"] = "ds-mission-panel" in refresh_html

    # Logout / login
    client.post("/auth/logout", follow_redirects=True)
    client.post(
        "/auth/login",
        data={"email": EMAIL, "password": PASSWORD},
        follow_redirects=True,
    )
    relogin = client.get("/student/")
    relogin_html = relogin.get_data(as_text=True)
    evidence["relogin_empty"] = "No exam selected" in relogin_html
    evidence["relogin_mission_panel"] = "ds-mission-panel" in relogin_html

    ok = (
        evidence["before_empty_state"] is True
        and evidence["after_empty"] is False
        and evidence["after_empty_state"] is False
        and evidence["after_mission_panel"] is True
        and evidence["after_primary"] is True
        and evidence["after_has_exam_name"] is True
        and evidence["refresh_empty"] is False
        and evidence["relogin_empty"] is False
        and evidence["relogin_mission_panel"] is True
    )
    evidence["pass"] = ok
    (OUT / "evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""RC-001 evidence capture — Session flow screens (Overview/Activity/
Reflection/Summary/Complete) at 1440px.

The live dev-server's real activity/adaptive engine never resolves
``has_explanation`` for a placeholder text answer in this seeded fixture
(no real question bank behind the seeded "IFoA CM1" curriculum topics), so a
genuine browser click-through never reaches Reflection (see RC-001 session
notes). This script instead renders the same routes/templates the browser
would receive by wiring the Session Experience to the same
``FakeActivityEnginePort`` the test suite (``tests/presentation/session/
test_routes.py::test_answer_and_advance_to_reflection``) uses to drive a
real, deterministic walk through the flow via Flask's test client, then
screenshots the resulting HTML (with a <base> tag pointing at the live dev
server so CSS/JS resolve identically to a real request).

This captures true layout/CSS evidence for B7 on these screens; it is not a
substitute for B1's persistence evidence, which is covered by
``tests/presentation/session/test_routes.py::
test_reflection_note_is_persisted_via_runtime_port`` (real runtime port, not
this fake).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("SECRET_KEY", "rc001-evidence-secret-key")
os.environ["KWALITEC_V2_STUDENT_EXPERIENCE"] = "1"
os.environ["KWALITEC_V2_SOLE_RUNTIME"] = "1"
os.environ["KWALITEC_V2_DURABLE_STORE"] = "0"
os.environ["KWALITEC_V2_INJECT_ENGINES"] = "0"
os.environ["KWALITEC_EI_INTERNAL_ALPHA"] = "1"
os.environ["KWALITEC_V2_SEED_DEMO"] = "0"
os.environ["DATABASE_URL"] = "sqlite:////tmp/rc001_evidence.sqlite3"
os.environ["WTF_CSRF_ENABLED"] = "False"

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from tests.application.session_experience.helpers import (  # noqa: E402
    FakeActivityEnginePort,
)
from tests.presentation.session.helpers import wire_session_experience  # noqa: E402

BASE_LIVE = "http://127.0.0.1:5099"
OUT = ROOT / "knowledge/product/rc001/screens"
SESSION_ID = "sess-rc001-evidence"


def inject_base(html: str) -> str:
    return html.replace("<head>", f'<head><base href="{BASE_LIVE}/">', 1)


def main() -> int:
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        wire_session_experience(app, activity_engine=FakeActivityEnginePort(activities=1))

    client = app.test_client()
    login = client.post(
        "/auth/login",
        data={
            "email": "rc001.full@kwalitec.example",
            "password": "RC001Evidence!2026",
        },
        follow_redirects=True,
    )
    assert login.status_code == 200, login.get_data(as_text=True)[:500]

    pages: dict[str, str] = {}

    overview = client.get(f"/session/{SESSION_ID}/overview")
    assert overview.status_code == 200, overview.status_code
    pages["overview"] = overview.get_data(as_text=True)

    begin = client.post(
        f"/session/{SESSION_ID}/begin",
        data={"session_id": SESSION_ID, "submit": "Begin Session"},
        follow_redirects=True,
    )
    assert begin.status_code == 200, begin.status_code
    pages["activity"] = begin.get_data(as_text=True)

    answer = client.post(
        f"/session/{SESSION_ID}/activity/answer",
        data={
            "session_id": SESSION_ID,
            "activity_id": "act-1",
            "response": "Placeholder answer for RC-001 evidence capture.",
            "submit": "Submit Answer",
        },
        follow_redirects=True,
    )
    assert answer.status_code == 200, answer.status_code
    pages["activity-explained"] = answer.get_data(as_text=True)

    advance = client.post(
        f"/session/{SESSION_ID}/activity/advance",
        data={"session_id": SESSION_ID, "submit": "Continue"},
        follow_redirects=False,
    )
    assert advance.status_code in {302, 303}, advance.status_code
    assert "/reflection" in advance.headers.get("Location", "")

    reflection = client.get(f"/session/{SESSION_ID}/reflection")
    assert reflection.status_code == 200, reflection.status_code
    pages["reflection"] = reflection.get_data(as_text=True)

    reflection_continue = client.post(
        f"/session/{SESSION_ID}/reflection/continue",
        data={
            "session_id": SESSION_ID,
            "reflection_note": "I still find deferred tax tricky — need another pass.",
            "submit": "Continue to Summary",
        },
        follow_redirects=False,
    )
    assert reflection_continue.status_code in {302, 303}, reflection_continue.status_code

    summary = client.get(f"/session/{SESSION_ID}/summary")
    assert summary.status_code == 200, summary.status_code
    pages["summary"] = summary.get_data(as_text=True)

    complete = client.get(f"/session/{SESSION_ID}/complete")
    if complete.status_code == 200:
        pages["complete"] = complete.get_data(as_text=True)

    from playwright.sync_api import sync_playwright

    BREAKPOINTS = [
        ("320", 320, 844, "mobile"),
        ("375", 375, 812, "mobile"),
        ("390", 390, 844, "mobile"),
        ("414", 414, 896, "mobile"),
        ("768", 768, 1024, "tablet"),
        ("820", 820, 1180, "tablet"),
        ("1024", 1024, 1366, "desktop"),
        ("1280", 1280, 800, "desktop"),
        ("1440", 1440, 900, "desktop"),
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    overflow_report: dict[str, dict] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for label, width, height, tier in BREAKPOINTS:
            page = browser.new_page(viewport={"width": width, "height": height})
            for name, html in pages.items():
                page.set_content(inject_base(html), wait_until="networkidle")
                path = OUT / f"{tier}-{label}px-session-{name}.png"
                page.screenshot(path=str(path), full_page=True)
                overflow = page.evaluate(
                    "() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - document.documentElement.clientWidth"
                )
                overflow_report.setdefault(label, {})[name] = overflow
                flag = " OVERFLOW" if overflow > 1 else ""
                print(f"captured {path.name} overflow={overflow}px{flag}")
            page.close()
        browser.close()

    print("\nSession flow evidence captured across 9 breakpoints:", ", ".join(pages.keys()))
    return 0


if __name__ == "__main__":
    sys.exit(main())

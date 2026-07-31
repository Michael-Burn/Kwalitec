#!/usr/bin/env python3
"""RC-2026.07.29-08 — post-deploy visual evidence screenshots (production).

Captures Founder Console + Student OS surfaces in Light/Dark as required.
Credentials: ADMIN_EMAIL / ADMIN_PASSWORD from environment (never logged).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = (
    os.environ.get("KWALITEC_BASE_URL") or os.environ.get("APP_URL") or ""
).rstrip("/")
if not BASE_URL:
    raise SystemExit(
        "Set KWALITEC_BASE_URL or APP_URL to the production origin "
        "(e.g. https://app.example.com)."
    )
OUT_DIR = Path(__file__).resolve().parent
DESKTOP = {"width": 1440, "height": 900}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_theme(page, appearance: str) -> None:
    """Force light/dark via the product theme storage + attributes."""
    page.evaluate(
        """(appearance) => {
          try { localStorage.setItem('kwalitec-appearance', appearance); } catch (e) {}
          const root = document.documentElement;
          root.setAttribute('data-appearance', appearance);
          root.setAttribute('data-theme', appearance);
          root.setAttribute('data-bs-theme', appearance);
          root.style.colorScheme = appearance;
        }""",
        appearance,
    )
    page.wait_for_timeout(250)


def shot(page, name: str, evidence: dict) -> Path:
    path = OUT_DIR / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    evidence["shots"].append(
        {
            "name": name,
            "path": str(path.relative_to(OUT_DIR.parent.parent.parent.parent)),
            "url": page.url,
            "theme": page.evaluate(
                "() => document.documentElement.getAttribute('data-theme')"
            ),
            "title": page.title(),
            "h1": page.evaluate(
                "() => ((document.querySelector('h1')||{}).innerText||'').trim().slice(0,160)"
            ),
        }
    )
    print(f"captured {name} -> {path.name} ({page.url})")
    return path


def login(page, email: str, password: str) -> None:
    page.goto(f"{BASE_URL}/auth/login", wait_until="networkidle")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"], input[type="submit"]')
    page.wait_for_load_state("networkidle")
    if "/auth/login" in page.url:
        raise RuntimeError("Login failed — still on /auth/login")


def main() -> int:
    email = (os.environ.get("ADMIN_EMAIL") or "").strip()
    password = (os.environ.get("ADMIN_PASSWORD") or "").strip()
    if not email or not password:
        print("ADMIN_EMAIL and ADMIN_PASSWORD must be set", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    evidence: dict = {
        "captured_at": utc_now(),
        "base_url": BASE_URL,
        "commit_expected": "7577dfeaea46a6676c2315bacd4f6c471314ebbd",
        "viewport": DESKTOP,
        "shots": [],
        "errors": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=DESKTOP,
            device_scale_factor=1,
            color_scheme="light",
        )
        page = context.new_page()
        page.on(
            "pageerror",
            lambda err: evidence["errors"].append({"type": "pageerror", "msg": str(err)}),
        )

        try:
            login(page, email, password)

            # —— Founder Console Light ——
            page.goto(f"{BASE_URL}/console/", wait_until="networkidle")
            set_theme(page, "light")
            page.reload(wait_until="networkidle")
            set_theme(page, "light")
            shot(page, "01_founder_console_light", evidence)

            # —— Founder Console Dark ——
            set_theme(page, "dark")
            page.reload(wait_until="networkidle")
            set_theme(page, "dark")
            shot(page, "02_founder_console_dark", evidence)

            # Enter Student Experience / Student Home Light
            set_theme(page, "light")
            page.goto(f"{BASE_URL}/student/", wait_until="networkidle")
            set_theme(page, "light")
            page.reload(wait_until="networkidle")
            set_theme(page, "light")
            shot(page, "03_student_home_light", evidence)

            # Student Home Dark
            set_theme(page, "dark")
            page.reload(wait_until="networkidle")
            set_theme(page, "dark")
            shot(page, "04_student_home_dark", evidence)

            # Remaining Student OS surfaces (capture in light baseline)
            set_theme(page, "light")
            for name, path in (
                ("05_journey", "/student/journey"),
                ("06_history", "/student/history"),
                ("07_revision", "/student/revision"),
                ("08_settings", "/student/profile"),
                ("09_choose_exam", "/study-plan/"),
            ):
                page.goto(f"{BASE_URL}{path}", wait_until="networkidle")
                set_theme(page, "light")
                shot(page, name, evidence)

        except Exception as exc:
            evidence["errors"].append({"type": "fatal", "msg": str(exc)})
            print(f"FATAL: {exc}", file=sys.stderr)
            browser.close()
            (OUT_DIR / "evidence.json").write_text(
                json.dumps(evidence, indent=2), encoding="utf-8"
            )
            return 1

        browser.close()

    (OUT_DIR / "evidence.json").write_text(
        json.dumps(evidence, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# RC-2026.07.29-08 — Visual Evidence",
                "",
                f"Captured: `{evidence['captured_at']}`",
                f"Host: `{BASE_URL}`",
                f"Expected deploy tip: `{evidence['commit_expected']}`",
                f"Viewport: {DESKTOP['width']}×{DESKTOP['height']}",
                "",
                "## Screenshots",
                "",
                "| File | Surface |",
                "|------|---------|",
                "| `01_founder_console_light.png` | Founder Console (Light) |",
                "| `02_founder_console_dark.png` | Founder Console (Dark) |",
                "| `03_student_home_light.png` | Student Home (Light) |",
                "| `04_student_home_dark.png` | Student Home (Dark) |",
                "| `05_journey.png` | Journey |",
                "| `06_history.png` | History |",
                "| `07_revision.png` | Revision |",
                "| `08_settings.png` | Settings |",
                "| `09_choose_exam.png` | Choose Exam |",
                "",
                "Metadata: `evidence.json`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"done — {len(evidence['shots'])} screenshots in {OUT_DIR}")
    return 0 if not evidence["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

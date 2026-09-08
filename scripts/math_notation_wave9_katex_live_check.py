#!/usr/bin/env python3
"""Live KaTeX DOM check for representative Wave 9 worked examples.

Renders the same session-body + apply_math_markup path students see, then
loads KaTeX 0.16.11 (session/base.html versions) and katex-auto-render.js.

Usage (Chromium via Playwright available)::

    python scripts/math_notation_wave9_katex_live_check.py
"""

from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("SECRET_KEY", "wave9-katex-live-check")
os.environ.setdefault("WTF_CSRF_ENABLED", "False")

from app import create_app  # noqa: E402
from app.application.educational_packages.loader import (  # noqa: E402
    find_package_by_id,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import (  # noqa: E402
    substance_from_package,
)
from app.application.learning_session.educational_flow import (  # noqa: E402
    EducationalStage,
)
from app.presentation.session.content_sections import (  # noqa: E402
    parse_session_content_body,
    present_worked_example_content,
)
from app.presentation.session.math_markup import apply_math_markup  # noqa: E402
from tests.presentation.session.test_session_redesign import (  # noqa: E402
    _base_page,
    _render,
)

OUT = Path("/tmp/wave9_katex_live")
OUT.mkdir(parents=True, exist_ok=True)

PACKAGES = (
    ("CS1-EP001-PKG-2.1-POISSON-PROCESS", "poisson"),
    ("CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR", "prior-post"),
    ("CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION", "inv-gen"),
    ("CS1-EP001-PKG-REV-GLM-XI", "glm-rev"),
    ("CS1-CS1002-PKG-2.1-DISCRETE", "discrete"),
    ("CS1-EP001-PKG-2.1-SOFTWARE-GENERATION", "soft-gen"),
)

KATEX_JS = ROOT / "app/static/js/katex-auto-render.js"
(OUT / "katex-auto-render.js").write_text(KATEX_JS.read_text(encoding="utf-8"))


def main() -> int:
    reset_educational_package_cache()
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    report: list[dict] = []

    for pack_id, slug in PACKAGES:
        pack = find_package_by_id(pack_id)
        assert pack is not None, pack_id
        substance = substance_from_package(
            pack, curriculum_identity="CS1:wave9-live", topic_id=pack.topic_code
        )
        example = next(
            a
            for a in substance.activities
            if a.stage is EducationalStage.WORKED_EXAMPLE
        )
        presented = present_worked_example_content(
            parse_session_content_body(example.body)
        )
        study = apply_math_markup(
            _base_page(
                content_stage="worked_example",
                stage_position_label="Worked example",
                content_title="Worked example",
                content_intro_line=presented.intro_line,
                content_sections=presented.primary,
                content_sections_more=presented.more,
            )
        )
        with app.app_context():
            body = _render(app, study)
        # CDN URLs intentionally long (KaTeX 0.16.11, matches session/base.html).
        katex_css = (
            "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
        )
        katex_js = (
            "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
        )
        auto_js = (
            "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/"
            "auto-render.min.js"
        )
        page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>{pack_id}</title>
<link rel="stylesheet" href="{katex_css}" crossorigin="anonymous">
</head>
<body>
{body}
<script src="{katex_js}" crossorigin="anonymous"></script>
<script src="{auto_js}" crossorigin="anonymous"></script>
<script src="/katex-auto-render.js"></script>
</body></html>
"""
        (OUT / f"{slug}.html").write_text(page, encoding="utf-8")

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(OUT), **kwargs)

        def log_message(self, format, *args):  # noqa: A003
            return

    httpd = ThreadingHTTPServer(("127.0.0.1", 8772), Handler)
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    from playwright.sync_api import sync_playwright

    launch_candidates = [
        Path.home()
        / "Library/Caches/ms-playwright/chromium_headless_shell-1234"
        / "chrome-headless-shell-mac-arm64/chrome-headless-shell",
        Path.home()
        / "Library/Caches/ms-playwright/chromium_headless_shell-1234"
        / "chrome-headless-shell-mac-x64/chrome-headless-shell",
        Path.home()
        / "Library/Caches/ms-playwright/chromium-1234"
        / "chrome-mac-arm64/Google Chrome for Testing.app"
        / "Contents/MacOS/Google Chrome for Testing",
    ]
    launch_kwargs: dict = {"headless": True}
    for candidate in launch_candidates:
        if candidate.is_file():
            launch_kwargs["executable_path"] = str(candidate)
            break

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        for pack_id, slug in PACKAGES:
            url = f"http://127.0.0.1:8772/{slug}.html"
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(500)
            katex = page.locator(".katex").count()
            katex_html = page.locator(".katex-html").count()
            errors = page.locator(".katex-error").count()
            fracs = page.locator(".katex .mfrac, .katex .frac-line").count()
            sample = ""
            if katex_html:
                sample = page.locator(".katex-html").first.inner_text()[:120]
            row = {
                "package_id": pack_id,
                "url": url,
                "katex": katex,
                "katex_html": katex_html,
                "katex_error": errors,
                "frac_nodes": fracs,
                "sample": sample,
            }
            report.append(row)
            print(json.dumps(row, ensure_ascii=False))
            assert katex > 0, f"no .katex for {pack_id}"
            assert katex_html > 0, f"no .katex-html for {pack_id}"
            assert errors == 0, f"KaTeX errors for {pack_id}"
        browser.close()
    httpd.shutdown()
    print("LIVE_KATEX_OK", len(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

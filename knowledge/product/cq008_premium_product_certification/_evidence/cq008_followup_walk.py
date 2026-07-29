"""CQ-008 follow-up: workspace + session surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5001"
EMAIL = "cq008.founder@kwalitec.example"
PASSWORD = "Cq008Cert2026!"
OUT = Path(__file__).resolve().parent
SHOT = OUT / "screenshots"
results: dict = {"surfaces": {}, "notes": [], "errors": []}


def metrics(page, name: str) -> dict:
    data = page.evaluate(
        """() => {
        const h1 = [...document.querySelectorAll('h1')].map(el => el.textContent.trim());
        const primary = [...document.querySelectorAll(
          '.ds-btn--primary, button.btn.btn-primary, a.btn.btn-primary'
        )].filter(el => el.offsetParent !== null)
          .map(el => (el.innerText || el.value || '').trim().slice(0,80));
        const secondary = [...document.querySelectorAll(
          '.ds-btn--secondary, .ds-btn--ghost, .btn-outline-secondary'
        )].filter(el => el.offsetParent !== null).length;
        return {
          url: location.href,
          title: document.title,
          h1, h1Count: h1.length,
          primary, primaryCount: primary.length,
          secondaryCount: secondary,
          dsCss: [...document.styleSheets].some(s => (s.href||'').includes('design_system.css')),
          dsPage: !!document.querySelector('.ds-page'),
          empty: [...document.querySelectorAll('.ds-empty-operational')]
            .map(el => el.textContent.trim().slice(0,160)),
          stages: [...document.querySelectorAll('.ds-stage-indicator, [class*=stage]')]
            .map(el => el.textContent.trim().slice(0,120)).slice(0,8),
          headings: [...document.querySelectorAll('h1,h2,h3')]
            .map(el => el.tagName+': '+(el.textContent||'').trim().slice(0,80)).slice(0,16),
          nav: [...document.querySelectorAll('nav a, .console-sidebar a, .student-nav a, [role=navigation] a')]
            .filter(el => el.offsetParent !== null)
            .map(el => (el.innerText||'').trim()).filter(Boolean),
          hasDocUpload: !!document.querySelector('[class*=doc-upload], .progress-bar'),
          hasBootstrapProgress: !!document.querySelector('.progress, .progress-bar'),
          hasQcPrimary: !!document.querySelector('.qc-btn-primary, .session-btn-primary'),
          bodyTextSample: document.body.innerText.slice(0,500),
        };
      }"""
    )
    results["surfaces"][name] = data
    page.screenshot(path=str(SHOT / f"{name}.png"), full_page=True)
    return data


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="networkidle")
    page.fill("#email", EMAIL)
    page.fill("#password", PASSWORD)
    page.click("#submit")
    page.wait_for_load_state("networkidle")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1366, "height": 768}).new_page()
        login(page)
        results["notes"].append({"post_login": page.url})

        # Subjects + create subject if empty
        page.goto(f"{BASE}/console/studio/subjects", wait_until="networkidle")
        metrics(page, "10_subjects_detail")
        create = page.locator("#subject_code, input[name=subject_code]")
        if create.count():
            page.fill("#subject_code", "CQ8A")
            page.fill("#title", "CQ008 Certification Subject")
            page.click('button[type=submit].ds-btn--primary, input[type=submit].ds-btn--primary')
            page.wait_for_load_state("networkidle")
            metrics(page, "11_after_create")

        hrefs = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => e.getAttribute('href'))"
        )
        ws = [h for h in hrefs if h and "workspace" in h]
        results["notes"].append({"workspace_hrefs": ws[:10]})
        if ws:
            target = ws[0] if ws[0].startswith("http") else f"{BASE}{ws[0]}"
            page.goto(target, wait_until="networkidle")
            metrics(page, "12_workspace")
        else:
            # try open first row button
            open_btn = page.locator('a:has-text("Open"), button:has-text("Open")').first
            if open_btn.count():
                open_btn.click()
                page.wait_for_load_state("networkidle")
                metrics(page, "12_workspace")

        # Student journey deeper: choose exam Ready rows
        page.goto(f"{BASE}/study-plan/wizard/1", wait_until="networkidle")
        metrics(page, "13_choose_exam_detail")
        row = page.locator(".ds-exam-row__input").first
        if row.count():
            row.check(force=True)
            page.wait_for_timeout(300)
            page.click(".ds-btn--primary")
            page.wait_for_load_state("networkidle")
            metrics(page, "14_choose_exam_next")
            # continue quiet steps if present
            for i in range(4):
                if page.locator(".ds-btn--primary").count():
                    label = page.locator(".ds-btn--primary").first.inner_text()
                    results["notes"].append({"step": page.url, "primary": label})
                    if "Begin" in label or "Learning" in label:
                        page.click(".ds-btn--primary")
                        page.wait_for_load_state("networkidle")
                        metrics(page, "15_after_begin")
                        break
                    page.click(".ds-btn--primary")
                    page.wait_for_load_state("networkidle")
                    metrics(page, f"14b_step_{i}")
                else:
                    break

        # Student home after commitment
        page.goto(f"{BASE}/student/", wait_until="networkidle")
        metrics(page, "16_student_home_after")
        if page.locator(".ds-btn--primary").count():
            label = page.locator(".ds-btn--primary").first.inner_text()
            results["notes"].append({"student_primary": label})
            if "Start" in label or "Resume" in label or "Continue" in label:
                page.click(".ds-btn--primary")
                page.wait_for_load_state("networkidle")
                metrics(page, "17_session")

        # Session direct probe if URL known
        if "/session/" in page.url:
            metrics(page, "17_session_confirm")

        browser.close()

    (OUT / "live_certification_followup.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2)[:12000])


if __name__ == "__main__":
    main()

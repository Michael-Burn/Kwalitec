"""CQ-008 live premium certification walk — evidence only, no product changes."""

from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5001"
EMAIL = "cq008.founder@kwalitec.example"
PASSWORD = "Cq008Cert2026!"
OUT = Path(__file__).resolve().parent
SHOT = OUT / "screenshots"
SHOT.mkdir(parents=True, exist_ok=True)

results: dict = {
    "surfaces": {},
    "journeys": {},
    "a11y": {},
    "perf": {},
    "errors": [],
}


def metrics(page, name: str) -> dict:
    data = page.evaluate(
        """() => {
        const h1 = [...document.querySelectorAll('h1')].map(el => el.textContent.trim());
        const primary = [...document.querySelectorAll(
          '.ds-btn--primary, .btn-primary, button.btn.btn-primary, a.btn.btn-primary'
        )]
          .filter(el => el.offsetParent !== null)
          .map(el => (el.innerText || el.textContent || '').trim().slice(0,80));
        const dsCss = [...document.styleSheets].some(s => (s.href||'').includes('design_system.css'));
        const dsPage = !!document.querySelector('.ds-page, .ds-container, .ds-page-header');
        const legacyStat = !!document.querySelector(
          '.statistic-tile, .progress-ring, [class*="StatisticTile"]'
        );
        const bootstrapAlert = document.querySelectorAll('.alert').length;
        const navLinks = [...document.querySelectorAll(
          'nav a, .sidebar a, .console-nav a, .student-nav a, [role=navigation] a'
        )]
          .filter(el => el.offsetParent !== null)
          .map(el => (el.innerText||'').trim()).filter(Boolean);
        const headings = [...document.querySelectorAll('h1,h2,h3')].map(el => ({
          t: el.tagName, text: (el.textContent||'').trim().slice(0,100)
        }));
        const theme = document.documentElement.getAttribute('data-theme');
        const scroll = document.documentElement.scrollHeight
          > document.documentElement.clientHeight + 2;
        return {
          title: document.title,
          url: location.href,
          h1, h1Count: h1.length,
          primary, primaryCount: primary.length,
          dsCss, dsPage, legacyStat, bootstrapAlert,
          navLinks: [...new Set(navLinks)].slice(0,24),
          navCount: navLinks.length,
          headings: headings.slice(0,24),
          theme, scroll,
          clsSample: {
            hasLanding: !!document.querySelector('.landing-split, .landing-card'),
            hasDsBtn: !!document.querySelector('.ds-btn'),
            hasBootstrapBtn: !!document.querySelector('.btn.btn-primary'),
            hasDocUpload: !!document.querySelector(
              '.doc-upload, .doc-upload-card, [class*=doc-upload]'
            ),
            hasExamRow: !!document.querySelector('.ds-exam-row'),
            hasSessionShell: !!document.querySelector('.ds-session-shell'),
            hasConsoleShell: !!document.querySelector(
              '.console-layout, .console-sidebar, .founder-console'
            ),
            hasEosNav: !!document.querySelector(
              '.student-topbar, .eos-topbar, .student-nav'
            ),
          },
          fonts: getComputedStyle(document.body).fontFamily.slice(0,100),
        };
      }"""
    )
    results["surfaces"][name] = data
    page.screenshot(path=str(SHOT / f"{name}.png"), full_page=True)
    return data


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="networkidle")
    metrics(page, "00_public_signin")
    results["a11y"]["theme_controls"] = page.locator(
        '[data-theme-option], button:has-text("Light"), button:has-text("Dark")'
    ).count()
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"], input[type="submit"]')
    page.wait_for_load_state("networkidle")
    if "/alpha/onboarding" in page.url:
        for sel in [
            'button:has-text("Skip")',
            'a:has-text("Skip")',
            'button:has-text("Continue")',
            'button:has-text("Finish")',
            'button:has-text("Get started")',
        ]:
            loc = page.locator(sel)
            if loc.count():
                try:
                    loc.first.click(timeout=2000)
                    page.wait_for_load_state("networkidle")
                except Exception as exc:  # noqa: BLE001
                    results["errors"].append({"onboarding": str(exc)})
        if "/alpha/onboarding" in page.url:
            page.goto(f"{BASE}/student/", wait_until="networkidle")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()
        page.on(
            "pageerror",
            lambda e: results["errors"].append({"type": "pageerror", "msg": str(e)}),
        )

        t0 = time.time()
        login(page)
        results["journeys"]["post_login_url"] = page.url

        for path, name in [
            ("/console/", "01_founder_home"),
            ("/console/studio/subjects", "02_founder_subjects"),
        ]:
            try:
                resp = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=20000)
                m = metrics(page, name)
                m["http"] = resp.status if resp else None
            except Exception as exc:  # noqa: BLE001
                results["errors"].append({"surface": name, "error": str(exc)})

        subjects = results["surfaces"].get("02_founder_subjects", {})
        if subjects.get("http") in (404, None) or "02_founder_subjects" not in results["surfaces"]:
            for path in [
                "/console/subjects",
                "/curriculum-studio/subjects",
                "/founder/",
            ]:
                try:
                    resp = page.goto(
                        f"{BASE}{path}", wait_until="domcontentloaded", timeout=10000
                    )
                    if resp and resp.status < 400:
                        m = metrics(page, "02_founder_subjects")
                        m["http"] = resp.status
                        m["resolved_path"] = path
                        break
                except Exception as exc:  # noqa: BLE001
                    results["errors"].append({"subjects_alt": path, "error": str(exc)})

        try:
            hrefs = page.eval_on_selector_all(
                "a[href]", "els => els.map(e => e.getAttribute('href'))"
            )
            ws = [h for h in hrefs if h and "workspace" in h]
            if ws:
                target = ws[0] if ws[0].startswith("http") else f"{BASE}{ws[0]}"
                page.goto(target, wait_until="networkidle")
                metrics(page, "03_founder_workspace")
            else:
                results["journeys"]["workspace"] = "no workspace link on subjects"
        except Exception as exc:  # noqa: BLE001
            results["errors"].append({"surface": "workspace", "error": str(exc)})

        for path, name in [
            ("/student/", "04_student_home"),
            ("/study-plan/wizard/1", "05_choose_exam"),
        ]:
            try:
                resp = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=20000)
                m = metrics(page, name)
                m["http"] = resp.status if resp else None
                if m["http"] and m["http"] >= 500:
                    results["errors"].append(
                        {
                            "surface": name,
                            "http": m["http"],
                            "snippet": page.content()[:600],
                        }
                    )
            except Exception as exc:  # noqa: BLE001
                results["errors"].append({"surface": name, "error": str(exc)})

        try:
            page.goto(f"{BASE}/student/", wait_until="networkidle")
            primary = page.locator(".ds-btn--primary").first
            if primary.count():
                primary.click(timeout=4000)
                page.wait_for_load_state("networkidle")
                results["journeys"]["session_after_primary"] = page.url
                metrics(page, "06_study_session_or_next")
            else:
                results["journeys"]["session"] = "no primary on student home"
        except Exception as exc:  # noqa: BLE001
            results["errors"].append({"surface": "session", "error": str(exc)})

        page.goto(f"{BASE}/auth/logout", wait_until="domcontentloaded")
        page.goto(f"{BASE}/auth/login", wait_until="networkidle")
        for label in ["Dark", "Light", "System"]:
            btn = page.locator(
                f'button:has-text("{label}"), [data-theme-option="{label.lower()}"]'
            )
            if btn.count():
                btn.first.click()
                page.wait_for_timeout(250)
                results["a11y"][f"theme_{label}"] = page.evaluate(
                    "() => document.documentElement.getAttribute('data-theme')"
                )
        metrics(page, "07_signin_after_theme")

        page.keyboard.press("Tab")
        page.keyboard.press("Tab")
        results["a11y"]["focus_sample"] = page.evaluate(
            """() => ({
              tag: document.activeElement.tagName,
              name: document.activeElement.getAttribute('name'),
              text: (document.activeElement.innerText||'').slice(0,40)
            })"""
        )

        for w, h, label in [
            (390, 844, "mobile"),
            (768, 1024, "tablet"),
            (1366, 768, "laptop"),
        ]:
            page.set_viewport_size({"width": w, "height": h})
            page.goto(f"{BASE}/auth/login", wait_until="networkidle")
            results["perf"][f"signin_overflow_{label}"] = page.evaluate(
                "() => document.documentElement.scrollHeight"
                " - document.documentElement.clientHeight"
            )
            page.screenshot(path=str(SHOT / f"08_signin_{label}.png"), full_page=False)

        results["elapsed_s"] = round(time.time() - t0, 2)
        browser.close()

    (OUT / "live_certification.json").write_text(json.dumps(results, indent=2))
    summary = {
        name: {
            "url": s.get("url"),
            "http": s.get("http"),
            "h1": s.get("h1"),
            "h1Count": s.get("h1Count"),
            "primaryCount": s.get("primaryCount"),
            "primary": s.get("primary"),
            "dsCss": s.get("dsCss"),
            "dsPage": s.get("dsPage"),
            "legacyStat": s.get("legacyStat"),
            "bootstrapAlert": s.get("bootstrapAlert"),
            "navCount": s.get("navCount"),
            "clsSample": s.get("clsSample"),
            "scroll": s.get("scroll"),
        }
        for name, s in results["surfaces"].items()
    }
    print(json.dumps({"summary": summary, "journeys": results["journeys"], "a11y": results["a11y"], "perf": results["perf"], "errors": results["errors"][:20]}, indent=2))
    print("WROTE", OUT / "live_certification.json")


if __name__ == "__main__":
    main()

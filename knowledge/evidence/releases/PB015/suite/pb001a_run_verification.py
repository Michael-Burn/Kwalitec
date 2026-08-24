#!/usr/bin/env python3
"""PB-001A — LIVE Educational Delivery Verification (browserless).

Verification only. Does not modify educational content or Runtime.
"""
from __future__ import annotations

import http.cookiejar
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

BASE = "https://kwalitec.onrender.com"
ROOT = Path("/tmp/pb001a")
ACCT = ROOT / "accounts"
HTML = ROOT / "html"
EVID = ROOT / "evidence"
EXPECTED_COMMIT = "0d3fc72137ba0ea51d1baa522c52aa526cf04438"

# Certified markers expected from EC-001 remediated packages (local inventory)
EC001_MARKERS = [
    "Purpose of this reading",
    "Open your CMP",
    "Focus questions",
    "Misconception watch",
    "Out of scope today",
    "Return cue",
    "Worked-example",
    "Knowledge Checks",
]


def parse_input_attrs(tag_attrs: str) -> dict[str, str]:
    return {
        k.lower(): v
        for k, v in re.findall(r'([a-zA-Z_:][\w:.-]*)\s*=\s*"([^"]*)"', tag_attrs)
    }


def parse_radios(html: str) -> dict[str, list[str]]:
    radios: dict[str, list[str]] = {}
    for m in re.finditer(r"<input\b([^>]+)>", html, re.I):
        attrs = parse_input_attrs(m.group(1))
        if attrs.get("type", "").lower() != "radio":
            continue
        name, val = attrs.get("name"), attrs.get("value")
        if name is not None and val is not None:
            radios.setdefault(name, []).append(val)
    return radios


def parse_forms(html: str, default_path: str):
    forms = []
    for m in re.finditer(r"<form\b([^>]*)>(.*?)</form>", html, re.S | re.I):
        attrs = parse_input_attrs(m.group(1))
        action = attrs.get("action") or default_path
        method = (attrs.get("method") or "get").lower()
        if method != "post":
            continue
        if "logout" in action:
            continue
        forms.append((action, m.group(2)))
    return forms


class Client:
    def __init__(self, slug: str):
        self.slug = slug
        self.ctx = ssl._create_unverified_context()
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj),
            urllib.request.HTTPSHandler(context=self.ctx),
        )
        self.steps: list[dict] = []
        self.html_dir = HTML / slug
        self.html_dir.mkdir(parents=True, exist_ok=True)

    def log(self, step: str, ok=None, **kw):
        row = {"step": step, "ok": ok, **{k: v for k, v in kw.items() if k != "html"}}
        self.steps.append(row)
        flag = "PASS" if ok is True else ("FAIL" if ok is False else "INFO")
        print(
            f"  [{flag}] {self.slug}/{step}: " + json.dumps(row, default=str)[:360],
            flush=True,
        )
        return row

    def save(self, name: str, html: str):
        (self.html_dir / f"{name}.html").write_text(
            html, encoding="utf-8", errors="replace"
        )

    def title(self, html: str) -> str:
        m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""

    def csrf(self, html: str) -> str:
        m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
        if not m:
            m = re.search(r'value="([^"]+)"[^>]*name="csrf_token"', html)
        if not m:
            m = re.search(r'name="csrf-token" content="([^"]+)"', html)
        if not m:
            raise RuntimeError("csrf missing")
        return m.group(1)

    def textish(self, html: str) -> str:
        t = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
        t = re.sub(r"<style\b[^>]*>.*?</style>", " ", t, flags=re.I | re.S)
        t = re.sub(r"<[^>]+>", " ", t)
        return re.sub(r"\s+", " ", t).strip()

    def req(self, method: str, path: str, data=None):
        url = path if path.startswith("http") else BASE + path
        body = None
        hdrs = {"User-Agent": "PB001A-LiveDelivery/1.0"}
        if data is not None:
            body = urllib.parse.urlencode(data).encode()
            hdrs["Content-Type"] = "application/x-www-form-urlencoded"
        request = urllib.request.Request(url, data=body, headers=hdrs, method=method)
        try:
            with self.opener.open(request, timeout=180) as resp:
                return resp.status, resp.geturl(), resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return (
                e.code,
                e.geturl() if hasattr(e, "geturl") else url,
                e.read().decode("utf-8", "replace"),
            )

    def get(self, path: str):
        return self.req("GET", path)

    def post(self, path: str, data: dict):
        return self.req("POST", path, data)



    def flashes(self, html: str) -> list[str]:
        """Extract flash/alert messages from HTML."""
        import re as _re
        msgs = []
        for pat in (
            r'class="[^"]*flash[^"]*"[^>]*>(.*?)</',
            r'class="[^"]*alert[^"]*"[^>]*>(.*?)</',
            r'role="alert"[^>]*>(.*?)</',
        ):
            for mm in _re.finditer(pat, html, _re.S | _re.I):
                txt = _re.sub(r"<[^>]+>", "", mm.group(1))
                txt = _re.sub(r"\s+", " ", txt).strip()
                if txt:
                    msgs.append(txt)
        return msgs


def fingerprint(c: Client) -> dict:
    code, final, html = c.get("/health")
    try:
        data = json.loads(html)
    except json.JSONDecodeError:
        data = {}
    commit = data.get("commit")
    ok = commit == EXPECTED_COMMIT
    c.log(
        "fingerprint",
        ok,
        commit=commit,
        version=data.get("version"),
        status=code,
        final=final,
    )
    return data



def login(c: Client, email: str, password: str) -> bool:
    _, final, html = c.get("/auth/login")
    token = c.csrf(html)
    _, final, html = c.post(
        "/auth/login",
        {
            "csrf_token": token,
            "email": email,
            "password": password,
            "remember_me": "n",
            "submit": "Sign in",
        },
    )
    ok = "/auth/login" not in final or (
        "Invalid" not in html and "Welcome" in html
    )
    # Successful login usually leaves /auth/login
    ok = "/auth/login" not in final
    c.log("login", ok, final=final, title=c.title(html), email=email)
    c.save("login", html)
    return ok


def complete_onboarding(c: Client, final: str, html: str) -> tuple[str, str]:
    for i in range(8):
        if "onboarding" not in final.lower() and "onboarding" not in html.lower()[:2500]:
            break
        forms = parse_forms(html, urllib.parse.urlparse(final).path)
        if not forms:
            break
        action, body = forms[0]
        data = {"csrf_token": c.csrf(html)}
        radios = parse_radios(body) or parse_radios(html)
        for n, vs in radios.items():
            data[n] = vs[0]
        for n, inner in re.findall(
            r'<select[^>]*name="([^"]+)"(.*?)</select>', html, re.S | re.I
        ):
            vs = [v for v in re.findall(r'<option[^>]*value="([^"]+)"', inner) if v]
            if vs and n not in data:
                data[n] = vs[0]
        for n, v in re.findall(
            r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', html, re.I
        ):
            if n in data or n == "csrf_token":
                continue
            typ_m = re.search(rf'<input[^>]*name="{re.escape(n)}"[^>]*>', html, re.I)
            t = ""
            if typ_m:
                tm = re.search(r'type="([^"]+)"', typ_m.group(0), re.I)
                t = tm.group(1).lower() if tm else ""
            if t in ("radio", "checkbox", "submit"):
                continue
            if t == "hidden" and v:
                data[n] = v
            elif t == "number":
                data[n] = v or "0"
        path = action if action.startswith("/") else urllib.parse.urlparse(final).path
        _, final, html = c.post(path, data)
        c.log(f"onboarding_{i}", True, final=final, title=c.title(html))
        c.save(f"onboarding_{i}", html)
    return final, html


def enrol(
    c: Client,
    *,
    position_mode: str = "start",
    continue_code: str | None = None,
) -> tuple[str, str]:
    """Choose Exam → baseline. position_mode start|continue; optional continue_code."""
    _, final, html = c.get("/study-plan/wizard/1")
    c.save("wizard1_open", html)

    radios = re.findall(
        r'name="subject_key"[^>]*value="([^"]+)"|value="([^"]+)"[^>]*name="subject_key"',
        html,
    )
    vals = [a or b for a, b in radios]
    subject = None
    for prefer in ("Published:CS1", "CS1"):
        for v in vals:
            if prefer in v:
                subject = v
                break
        if subject:
            break
    if not subject and vals:
        subject = vals[0]
    c.log("wizard_subjects", bool(subject), subject=subject, radios=vals[:8])
    if not subject:
        return final, html

    _, final, html = c.post(
        "/study-plan/wizard/1",
        {"csrf_token": c.csrf(html), "subject_key": subject},
    )
    c.save("wizard1", html)

    if "/study-plan/wizard/2" in final or "exam_year" in html:
        d = date.today() + timedelta(days=200)
        data = {
            "csrf_token": c.csrf(html),
            "exam_sitting": "Custom",
            "exam_day": str(d.day),
            "exam_month": str(d.month),
            "exam_year": str(d.year),
        }
        _, final, html = c.post("/study-plan/wizard/2", data)
        c.save("wizard2", html)
        c.log("wizard_2", True, final=final, title=c.title(html))

    if (
        "/study-plan/wizard/3" in final
        or "preferred_session_minutes" in html
        or "weekday_study_minutes" in html
    ):
        data = {"csrf_token": c.csrf(html)}
        for n in ("weekday_study_minutes", "weekend_study_minutes"):
            if n in html:
                data[n] = "60"
        if "preferred_session_minutes" in html:
            sel = re.search(
                r'<select[^>]*name="preferred_session_minutes"(.*?)</select>',
                html,
                re.S | re.I,
            )
            if sel:
                vs = [v for v in re.findall(r'<option[^>]*value="([^"]+)"', sel.group(1)) if v]
                data["preferred_session_minutes"] = "60" if "60" in vs else (vs[0] if vs else "60")
            else:
                data["preferred_session_minutes"] = "60"
        path = urllib.parse.urlparse(final).path or "/study-plan/wizard/3"
        _, final, html = c.post(path, data)
        c.save("wizard3", html)
        c.log("wizard_3", True, final=final, title=c.title(html))

    for i in range(14):
        path = urllib.parse.urlparse(final).path
        if not path.startswith("/baseline"):
            break
        forms = parse_forms(html, path)
        if not forms:
            c.log(f"baseline_{i}_no_form", False, path=path)
            break
        action, body = forms[0]
        if not action.startswith("/"):
            action = (
                urllib.parse.urlparse(urllib.parse.urljoin(final, action)).path or path
            )
        data = {"csrf_token": c.csrf(html)}
        radios = parse_radios(body) or parse_radios(html)
        for n, vs in radios.items():
            if n == "experience":
                data[n] = "started" if "started" in vs else vs[0]
            elif n == "position_mode":
                if position_mode == "continue" and "continue" in vs:
                    data[n] = "continue"
                elif "start" in vs and position_mode == "start":
                    data[n] = "start"
                else:
                    data[n] = vs[0]
            elif n in ("continue_from", "curriculum_topic_code", "topic_code", "section"):
                if continue_code and continue_code in vs:
                    data[n] = continue_code
                elif continue_code:
                    # try fuzzy match
                    hit = next((v for v in vs if continue_code in v), None)
                    data[n] = hit or vs[0]
                else:
                    data[n] = vs[0]
            elif n == "learning_objective":
                data[n] = vs[0]
            elif n == "exam_history":
                data[n] = "never" if "never" in vs else vs[0]
            elif n == "confidence":
                data[n] = next((p for p in ("3", "medium", "somewhat") if p in vs), vs[0])
            else:
                data[n] = vs[0]
        for n, inner in re.findall(
            r'<select[^>]*name="([^"]+)"(.*?)</select>', html, re.S | re.I
        ):
            vs = [v for v in re.findall(r'<option[^>]*value="([^"]+)"', inner) if v]
            if not vs:
                continue
            if n not in data:
                if continue_code:
                    hit = next((v for v in vs if continue_code in v or v == continue_code), None)
                    data[n] = hit or vs[0]
                else:
                    data[n] = vs[0]
        for n, v in re.findall(
            r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', html, re.I
        ):
            if n in data or n == "csrf_token":
                continue
            typ_m = re.search(rf'<input[^>]*name="{re.escape(n)}"[^>]*>', html, re.I)
            t = ""
            if typ_m:
                tm = re.search(r'type="([^"]+)"', typ_m.group(0), re.I)
                t = tm.group(1).lower() if tm else ""
            if t in ("radio", "checkbox", "submit"):
                continue
            if t == "hidden" and v:
                data[n] = v
            elif t == "number":
                data[n] = v or "0"
            elif continue_code and n.lower() in (
                "continue_from",
                "curriculum_topic_code",
                "topic_code",
            ):
                data[n] = continue_code
        _, final, html = c.post(action, data)
        c.log(
            f"baseline_{i}",
            True,
            path=path,
            action=action,
            final=final,
            title=c.title(html),
            fields=sorted(k for k in data if k != "csrf_token"),
            posted={k: data[k] for k in data if k != "csrf_token"},
        )
        c.save(f"baseline_{i}", html)

    return final, html


def reach_reading(c: Client) -> dict:
    result = {
        "mission_present": False,
        "session_started": False,
        "reading_reached": False,
        "session_id": None,
        "mission_topic": None,
        "activity_title": None,
        "html_path": None,
    }
    _, final, html = c.get("/student/")
    c.save("home", html)
    text = c.textish(html)
    m = re.search(r"Study\s+([\d\.]+)\s*[—\-:]?\s*([^<\n]{0,80})", html)
    if m:
        result["mission_topic"] = f"{m.group(1)} {m.group(2).strip()}"
    mission_present = (
        'action="/student/session/start"' in html
        or bool(re.search(r'name="mission_id"', html))
        or bool(re.search(r"Today'?s Mission|Start today|Begin today'?s session", html, re.I))
    )
    result["mission_present"] = mission_present
    c.log(
        "home",
        True,
        final=final,
        title=c.title(html),
        mission=mission_present,
        mission_topic=result["mission_topic"],
        text_sample=text[:280],
    )
    if not mission_present:
        return result

    mid = re.search(r'name="mission_id"[^>]*value="([^"]+)"', html)
    data = {"csrf_token": c.csrf(html)}
    if mid:
        data["mission_id"] = mid.group(1)
    # include any hidden fields in start form
    form = re.search(
        r'<form[^>]*action="/student/session/start"[^>]*>(.*?)</form>', html, re.S | re.I
    )
    if form:
        for n, v in re.findall(
            r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', form.group(1), re.I
        ):
            if n not in data:
                data[n] = v
    _, final, html = c.post("/student/session/start", data)
    c.save("session_start", html)
    sid_m = re.search(r"/session/(lsr-[a-z0-9]+)", final)
    if not sid_m:
        sid_m = re.search(r"/session/(lsr-[a-z0-9]+)", html)
    if sid_m:
        result["session_id"] = sid_m.group(1)
        result["session_started"] = True
    c.log(
        "session_start",
        result["session_started"],
        final=final,
        title=c.title(html),
        session_id=result["session_id"],
    )

    # Activity 0 should be Reading
    # If overview, follow Continue / Start activity
    for i in range(4):
        path = urllib.parse.urlparse(final).path
        stage = None
        sm = re.search(r'data-session-stage="([^"]+)"', html)
        if sm:
            stage = sm.group(1)
        title_act = None
        tm = re.search(
            r'class="[^"]*ds-session-content__title[^"]*"[^>]*>(.*?)</',
            html,
            re.S | re.I,
        )
        if tm:
            title_act = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", tm.group(1))).strip()
        c.save(f"act_probe_{i}", html)
        is_reading = bool(
            stage
            and stage.lower() in ("read", "reading")
            or (title_act and re.search(r"Reading|Guided Reading|Read the material", title_act, re.I))
            or re.search(r"Reading · Activity|Guided Reading:", html, re.I)
        )
        c.log(
            f"act_probe_{i}",
            True,
            path=path,
            stage=stage,
            title_act=title_act,
            is_reading=is_reading,
        )
        if is_reading or (i == 0 and "/activity" in path):
            # If first activity page, treat as reading if stage missing but activity 1
            if is_reading or re.search(r"Activity 1 of|Reading", html, re.I):
                result["reading_reached"] = True
                result["activity_title"] = title_act
                result["html_path"] = str(c.html_dir / "reading.html")
                c.save("reading", html)
                break
        # Try advance/continue from overview
        forms = parse_forms(html, path)
        advanced = False
        for action, body in forms:
            if any(
                x in action
                for x in ("/continue", "/start", "/activity", "/advance", "/begin")
            ) or re.search(r"Continue|Begin|Start", body, re.I):
                data = {"csrf_token": c.csrf(html)}
                for n, v in re.findall(
                    r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', body, re.I
                ):
                    if n != "csrf_token":
                        data[n] = v
                _, final, html = c.post(action if action.startswith("/") else path, data)
                advanced = True
                break
        if not advanced:
            # follow activity link
            link = re.search(r'href="(/session/lsr-[^"]+/activity[^"]*)"', html)
            if link:
                _, final, html = c.get(link.group(1))
                advanced = True
        if not advanced:
            break

    if not result["reading_reached"] and result["session_started"]:
        # last chance: open activity URL
        sid = result["session_id"]
        _, final, html = c.get(f"/session/{sid}/activity")
        c.save("reading_fallback_url", html)
        tm = re.search(
            r'class="[^"]*ds-session-content__title[^"]*"[^>]*>(.*?)</',
            html,
            re.S | re.I,
        )
        title_act = (
            re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", tm.group(1))).strip()
            if tm
            else None
        )
        result["activity_title"] = title_act
        result["reading_reached"] = bool(
            re.search(r"Reading|Guided Reading|Read the material|Focus questions", html, re.I)
        )
        if result["reading_reached"]:
            c.save("reading", html)
            result["html_path"] = str(c.html_dir / "reading.html")
        c.log(
            "reading_direct",
            result["reading_reached"],
            title_act=title_act,
            final=final,
        )

    return result


def audit_reading_html(html: str, *, certified_snippets: dict | None = None) -> dict:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))

    body_m = re.search(
        r'class="[^"]*ds-session-content__body[^"]*"[^>]*>(.*?)</div>',
        html,
        re.S | re.I,
    )
    support_m = re.search(
        r'class="[^"]*ds-session-content__support[^"]*"[^>]*>(.*?)</div>',
        html,
        re.S | re.I,
    )
    title_m = re.search(
        r'class="[^"]*ds-session-content__title[^"]*"[^>]*>(.*?)</',
        html,
        re.S | re.I,
    )
    body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body_m.group(1) if body_m else ""))
    support = re.sub(
        r"\s+", " ", re.sub(r"<[^>]+>", " ", support_m.group(1) if support_m else "")
    )
    title = re.sub(
        r"\s+", " ", re.sub(r"<[^>]+>", " ", title_m.group(1) if title_m else "")
    )
    combined = f"{title} {body} {support} {plain}"

    is_fallback = bool(
        re.search(r"Learning objectives for this session", combined, re.I)
    ) and not bool(re.search(r"Guided Reading:", combined, re.I))
    is_guided = bool(re.search(r"Guided Reading:", combined, re.I))

    q = {
        "Q1_cmp_open": bool(
            re.search(r"Open your CMP|Open:.*CMP|\bCMP\b.*Syllabus", combined, re.I)
        ),
        "Q2_purpose": bool(
            re.search(r"Purpose of this reading|Purpose of this revision", combined, re.I)
        ),
        "Q3_attention": bool(
            re.search(r"Focus questions|Misconception watch|Annotation:", combined, re.I)
        ),
        "Q4_ignore": bool(
            re.search(r"Out of scope today|Ignore ", combined, re.I)
        ),
        "Q5_stop": bool(
            re.search(r"Stop:|You are finished|stop at|Come back when you", combined, re.I)
        ),
        "Q6_next": bool(
            re.search(
                r"Worked-example|Knowledge Checks|Immediate next activity",
                combined,
                re.I,
            )
        ),
    }
    markers_present = {m: (m.lower() in combined.lower() or m in combined) for m in EC001_MARKERS}

    snippet_hits = {}
    if certified_snippets:
        for key, val in certified_snippets.items():
            if not isinstance(val, str) or len(val) < 20:
                continue
            # use a distinctive 48-char window
            needle = val[:48]
            snippet_hits[key] = needle in combined

    cmp_refs_ok = bool(
        re.search(r"4\.2\.1|1\.1\.1|Syllabus\s+[\d\.]+|IFoA CS1", combined, re.I)
    )

    verdict_parts = [
        q["Q1_cmp_open"],
        q["Q2_purpose"],
        q["Q3_attention"],
        q["Q4_ignore"],
        q["Q5_stop"],
        q["Q6_next"],
        not is_fallback,
        is_guided or (q["Q1_cmp_open"] and not is_fallback),
    ]
    # For LIVE tip pre-EC001 package, Q2/Q6 may fail EC-001 bar even if guided reading present
    pass_ec001 = all(
        [
            q["Q1_cmp_open"],
            q["Q2_purpose"],
            q["Q3_attention"],
            q["Q4_ignore"],
            q["Q5_stop"],
            q["Q6_next"],
            not is_fallback,
        ]
    )

    return {
        "title": title[:200],
        "body_sample": body[:500],
        "support_sample": support[:400],
        "is_fallback_shell": is_fallback,
        "is_guided_reading": is_guided,
        "mentions_cmp": bool(re.search(r"\bCMP\b|Core Reading", combined, re.I)),
        "cmp_refs_present": cmp_refs_ok,
        "q_checks": q,
        "ec001_markers": markers_present,
        "certified_snippet_hits": snippet_hits,
        "verdict": "PASS" if pass_ec001 else "FAIL",
        "word_count_body": len(body.split()),
    }


def wait_login(slug: str, email: str, password: str, attempts: int = 12) -> Client | None:
    for i in range(attempts):
        c = Client(slug)
        try:
            if login(c, email, password):
                return c
        except Exception as e:
            c.log("login_error", False, error=str(e)[:200])
        time.sleep(10)
        print(f"  retry login {slug} attempt {i+1}", flush=True)
    return None


def main():
    EVID.mkdir(parents=True, exist_ok=True)
    HTML.mkdir(parents=True, exist_ok=True)

    password = (ACCT / "shared_pass.txt").read_text().strip()
    email11 = (ACCT / "study11.email").read_text().strip()
    email42 = (ACCT / "study42.email").read_text().strip()

    # Load certified snippets: EC-001 local (what programme claims) + LIVE tip (what is deployed)
    live_tip_pack = json.loads(
        Path("/tmp/pb001a/certified/4.2-glm-structure-LIVE-TIP.json").read_text()
    )
    ec001_pack = json.loads(
        Path("/tmp/pb001a/certified/4.2-glm-structure-EC001-LOCAL.json").read_text()
    )
    ec001_snippets = {
        "lead_line": ec001_pack["reading_guidance"]["lead_line"],
        "exit_line": ec001_pack["reading_guidance"]["exit_line"],
        "return_cue": ec001_pack["reading_guidance"]["return_cue"],
        "open_point": ec001_pack["reading_guidance"]["open_point"],
    }
    live_tip_snippets = {
        "lead_line": live_tip_pack["reading_guidance"]["lead_line"],
        "exit_line": live_tip_pack["reading_guidance"]["exit_line"],
        "return_cue": live_tip_pack["reading_guidance"]["return_cue"],
        "open_point": live_tip_pack["reading_guidance"]["open_point"],
    }

    report = {
        "programme": "PB-001A",
        "host": BASE,
        "expected_commit": EXPECTED_COMMIT,
        "packages": [],
        "deployment_note": {
            "ec001_content_on_live": False,
            "reason": (
                "EC-001 remediated reading_guidance exists only in the local working tree "
                "(uncommitted). LIVE tip 0d3fc721 still serves pre-EC-001 4.2 package copy."
            ),
        },
    }

    # Fingerprint via study11 client once ready
    print("=== Wait for provisioned users ===", flush=True)
    c11 = wait_login("study11", email11, password)
    if c11 is None:
        raise SystemExit("study11 login failed — provisioning incomplete")
    health = fingerprint(c11)
    report["live_commit"] = health.get("commit")
    report["live_version"] = health.get("version")

    # --- Package path A: Study 1.1 natural enrolment (no live publication_approved package) ---
    print("=== STUDY 1.1 natural path ===", flush=True)
    final, html = complete_onboarding(c11, *c11.get("/student/"))
    final, html = enrol(c11, position_mode="start")
    reach = reach_reading(c11)
    reading_html = ""
    if reach.get("html_path") and Path(reach["html_path"]).exists():
        reading_html = Path(reach["html_path"]).read_text(encoding="utf-8", errors="replace")
    elif (c11.html_dir / "reading.html").exists():
        reading_html = (c11.html_dir / "reading.html").read_text(
            encoding="utf-8", errors="replace"
        )
    audit11 = audit_reading_html(reading_html) if reading_html else {
        "verdict": "FAIL",
        "error": "Reading HTML not captured",
        "is_fallback_shell": True,
    }
    pkg11 = {
        "package_id": "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION",
        "live_published": False,
        "status_on_disk": "campaign_member_certified",
        "student_path": "Study 1.1 natural enrolment",
        "mission_topic": reach.get("mission_topic"),
        "reach": reach,
        "audit": audit11,
        "verdict": "FAIL",
        "verdict_reason": (
            "Not in LIVE publication_approved loader set; student receives fallback Reading shell"
            if audit11.get("is_fallback_shell")
            else "LIVE Reading does not match EC-001 certified 1.1 package"
        ),
    }
    # Override: catalogue package is NOT live published — delivery of certified package = FAIL
    if audit11.get("is_fallback_shell") or audit11.get("verdict") == "FAIL":
        pkg11["verdict"] = "FAIL"
    report["packages"].append(pkg11)
    (EVID / "study11_audit.json").write_text(json.dumps(pkg11, indent=2))
    print("STUDY11_VERDICT", pkg11["verdict"], flush=True)

    # --- Package path B: LIVE publication_approved 4.2 via baseline continue section 4 / 4.2 ---
    print("=== STUDY 4.2 via baseline continue ===", flush=True)
    c42 = wait_login("study42", email42, password)
    if c42 is None:
        raise SystemExit("study42 login failed")
    final, html = complete_onboarding(c42, *c42.get("/student/"))
    # Prefer continue at section 4 then hope first topic is 4.1; try leaf 4.2 if picker allows
    final, html = enrol(c42, position_mode="continue", continue_code="4")
    reach42 = reach_reading(c42)
    # If landed on 4.1 not 4.2, record honestly — may need leaf continue
    topic = (reach42.get("mission_topic") or "") + " " + (reach42.get("activity_title") or "")
    if "4.2" not in topic and "generalised" not in topic.lower() and "glm" not in topic.lower():
        print("  NOTE: section-4 continue did not land on 4.2; retry leaf 4.2 if possible", flush=True)
        # Save what we got; attempt a second reading of home for topic
        c42.save("home_after_section4", (c42.html_dir / "home.html").read_text() if (c42.html_dir / "home.html").exists() else "")

    reading_html42 = ""
    if (c42.html_dir / "reading.html").exists():
        reading_html42 = (c42.html_dir / "reading.html").read_text(
            encoding="utf-8", errors="replace"
        )
    audit42_ec001 = (
        audit_reading_html(reading_html42, certified_snippets=ec001_snippets)
        if reading_html42
        else {"verdict": "FAIL", "error": "Reading HTML not captured"}
    )
    audit42_live_tip = (
        audit_reading_html(reading_html42, certified_snippets=live_tip_snippets)
        if reading_html42
        else {"verdict": "FAIL", "error": "Reading HTML not captured"}
    )

    landed_42 = bool(
        re.search(r"4\.2|generalised linear|GLM", json.dumps(reach42) + reading_html42[:2000], re.I)
    )
    pkg42 = {
        "package_id": "CS1-EA005-PKG-4.2-GLM-STRUCTURE",
        "live_published": True,
        "status_on_disk": "publication_approved",
        "student_path": "Baseline continue-from section 4 / Reading",
        "mission_topic": reach42.get("mission_topic"),
        "landed_on_4_2": landed_42,
        "reach": reach42,
        "audit_vs_ec001_certified": audit42_ec001,
        "audit_vs_live_tip_package": audit42_live_tip,
        "verdict": "FAIL",
        "verdict_reason": "",
    }
    if not landed_42:
        pkg42["verdict"] = "FAIL"
        pkg42["verdict_reason"] = (
            "Could not reach topic 4.2 Reading on LIVE with baseline continue-from section 4; "
            f"observed mission={reach42.get('mission_topic')}"
        )
    elif audit42_ec001.get("verdict") == "PASS" and not audit42_ec001.get("is_fallback_shell"):
        pkg42["verdict"] = "PASS"
        pkg42["verdict_reason"] = "LIVE Reading matches EC-001 certified package markers"
    elif (
        not audit42_ec001.get("is_fallback_shell")
        and audit42_live_tip.get("certified_snippet_hits", {}).get("lead_line")
    ):
        pkg42["verdict"] = "FAIL"
        pkg42["verdict_reason"] = (
            "LIVE delivers the tip publication_approved package body (not fallback), "
            "but it does NOT match EC-001 certified remediated copy (EC-001 not deployed)"
        )
    else:
        pkg42["verdict"] = "FAIL"
        pkg42["verdict_reason"] = (
            "LIVE Reading for 4.2 failed EC-001 partnership checks and/or showed fallback shell"
        )

    report["packages"].append(pkg42)
    (EVID / "study42_audit.json").write_text(json.dumps(pkg42, indent=2))
    print("STUDY42_VERDICT", pkg42["verdict"], pkg42["verdict_reason"][:200], flush=True)

    # Catalogue packages not live-published — record NOT DELIVERED
    catalogue = [
        ("CS1-EP001-PKG-1.2-EDA-SUMMARIES", "1.2.1"),
        ("CS1-EP001-PKG-1.2-EDA-ASSOCIATION", "1.2.2"),
        ("CS1-EP001-PKG-REV-PURPOSE-EDA", "revision-alpha"),
        ("CS1-CS1002-PKG-1.2-PCA", "1.2.3"),
        ("CS1-CS1002-PKG-2.1-DISCRETE", "2.1.1"),
        ("CS1-CS1002-PKG-2.1-CONTINUOUS", "2.1.2"),
        ("CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS", "revision-beta"),
    ]
    for pid, topic in catalogue:
        report["packages"].append(
            {
                "package_id": pid,
                "live_published": False,
                "status_on_disk": "campaign_member_certified",
                "student_path": f"Not student-reachable as certified package (topic {topic})",
                "verdict": "FAIL",
                "verdict_reason": (
                    "Outside EA-006 live publication_approved loader; certified package "
                    "cannot be delivered on LIVE until Approver activation"
                ),
                "audit": None,
            }
        )

    report["summary"] = {
        "live_published_count": 1,
        "live_published_pass": sum(
            1
            for p in report["packages"]
            if p.get("live_published") and p.get("verdict") == "PASS"
        ),
        "live_published_fail": sum(
            1
            for p in report["packages"]
            if p.get("live_published") and p.get("verdict") == "FAIL"
        ),
        "catalogue_not_live_fail": sum(
            1 for p in report["packages"] if not p.get("live_published")
        ),
        "f1_f2_closable": False,
        "f1_f2_reason": (
            "Study 1.1 still serves fallback Reading shell; EC-001 certified catalogue "
            "packages are not LIVE-published; EC-001 remediated 4.2 copy is not on LIVE tip."
        ),
    }

    out = EVID / "pb001a_results.json"
    out.write_text(json.dumps(report, indent=2))
    print("WROTE", out, flush=True)
    print(json.dumps(report["summary"], indent=2), flush=True)
    (EVID / "steps_study11.json").write_text(json.dumps(c11.steps, indent=2))
    (EVID / "steps_study42.json").write_text(json.dumps(c42.steps, indent=2))


if __name__ == "__main__":
    main()

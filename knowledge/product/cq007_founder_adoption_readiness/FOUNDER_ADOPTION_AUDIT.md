# CQ-007 — Founder Adoption Audit

**Programme:** CQ-007 — Founder Adoption Readiness  
**Date:** 2026-07-28  
**Path audited:** Production sole-runtime (`KWALITEC_V2_SOLE_RUNTIME=1`) founder daily CS1 study OS  
**Method:** End-to-end code/template journey map; CQ-002–CQ-006 audits and completion reports; production flag posture (`render.yaml`); adoption lens — *would this stop daily use?*  
**Decision linked:** [`FOUNDER_ADOPTION_DECISION.md`](FOUNDER_ADOPTION_DECISION.md)

---

## Journey under assessment

```
Open Kwalitec
  → Understand today's mission
  → Begin studying
  → Complete a meaningful session
  → Leave knowing exactly what to do tomorrow
  → Return naturally the following day
```

Canonical sole-runtime path:

```
Login → (onboarding / Study Plan gates) → /student/ Home
  → POST /student/session/start (commitment + auto-begin)
  → /session/<id>/activity → Reflection → Summary → finish
  → Home (commitment reflection / day complete)
  → Next day: new mission OR Continue resume
```

---

## 1. Before studying

**Surfaces:** Auth login · Alpha onboarding · Study Plan wizard · Welcome modal · Student Home (`app/templates/student/home.html`) · MES / commitment / Mission Intelligence

### Strengths

- Sole-runtime production posture is live (`KWALITEC_V2_SOLE_RUNTIME=1` in `render.yaml`); student home resolves to `/student/`.
- Home presents today's mission with Why / Why now / benefit / Next and a single primary CTA (CQ-002 / CQ-005).
- One-click Start records commitment and auto-begins into Activity (CQ-002) — no mandatory Overview second Begin on the happy path.
- Empty Home offers Journey / Study Plan forward paths (CQ-002).
- Commitment confirm / “Not today” defer exist without streak shame (CQ-003 policy).
- Duration-aware mission labelling is present on the hero.

### Weaknesses

- Fresh-start hero can still stack many conditional MES / commitment / MI blocks before the CTA (CQ-002 F08 / CQ-003 H06 residual).
- `preferred_session_minutes` is not echoed at Home entry (CQ-003 H10).
- Welcome modal CTA navigates to Home entry, not session start (first-time only).
- Founder Console accounts land on Console, not Student Home — dogfood requires the student path explicitly.

### Adoption blockers

| ID | Issue | Stops daily use? | Class |
|---|---|---|---|
| A01 | Fresh-start hero density | No — primary CTA remains clear; slows scarce-time open | **Minor** |
| A02 | Preferred minutes not echoed | No — duration still shown | **Minor** |
| A03 | Founder Console ≠ student Home | No — operational dogfood setup constraint | **Constraint** |

### Commercial impact

Before-study friction is **Emerging, not Broken**. The founder can understand today's mission and start. Density and prefs echo remain Strong-band polish, not adoption stoppers.

---

## 2. During studying

**Surfaces:** Session Overview · Activity · Quick Check (Overview embed) · Reflection · Summary · Session chrome (`app/templates/session/`)

### Strengths

- Linear enforced flow with `resume_redirect_if_needed` — interrupt → resume restores active surface (workflow tests).
- Honest 4-step progress chrome (phantom Complete removed — CQ-002).
- Topic-threaded activity prompts and explanations (CQ-004); QC suppressed on Activity (CQ-004).
- Overview carries mission Why continuity (CQ-005).
- Session craft (secondary buttons, support, reflection framing) refined (CQ-006).
- Final activity CTA and completion headline give purposeful closure (CQ-004).

### Weaknesses

- Activity content remains **topic-threaded reflective scaffolds**, not syllabus-authored CS1 item banks (CQ-004 Known Limitation; V2 backlog territory for authored banks).
- Two-POST answer → advance loop still feels mechanical (CQ-004 residual).
- Mid-session brand link exits to Home without confirm (CQ-003 H07) — recoverable via Continue.
- Resume Continue still hops via Overview URL then redirects (CQ-003/CQ-004 S11).
- Auto-begin fail-open still lands on Overview + Start Session (rare).

### Adoption blockers

| ID | Issue | Stops daily use? | Class |
|---|---|---|---|
| A04 | Scaffolded practice vs exam-grade item banks | Stops **exclusive content** claim; does **not** stop daily OS use if textbooks/past papers accepted | **Constraint** (V1 scope) |
| A05 | Accidental Home exit mid-session | No — Continue resume works | **Minor** |
| A06 | Resume Overview redirect hop | No — one redirect; surface restored | **Minor** |
| A07 | Mechanical two-POST advance | No — usable; polish residual | **Minor** |

### Commercial impact

During-study is **usable every day** as a guided session OS. It is **not** yet a substitute for ActEd/CMP/past-paper practice depth. Commercial honesty requires stating that constraint; claiming exclusive educational content would overreach CR4/CR8.

---

## 3. After studying

**Surfaces:** Session Reflection · Summary completion card · Home commitment reflection · day-complete copy · Decision Journal / Timeline (optional)

### Strengths

- Summary “Next step” and completion headline close the session (CQ-004).
- Finish links commitment lifecycle; Home shows compact commitment reflection (CQ-004).
- Day-complete messaging points to tomorrow or Journey.
- Session reflection framed honestly (does not rate the student; separate from Journal).

### Weaknesses

- Double reflection family (session + Home commitment; Guided Reflection preview is presentation-only) still adds cognitive tax — mitigated, not eliminated.
- Finish flash remains generic (not topic-specific).
- History defers “why it mattered” narrative to Journal/Timeline (CQ-005 G08).

### Adoption blockers

| ID | Issue | Stops daily use? | Class |
|---|---|---|---|
| A08 | Double / multi-reflection surfaces | No — primary next step is clear | **Minor** |
| A09 | History narrative deferral | No — not on daily critical path | **Minor** |

### Commercial impact

Post-session closure is good enough for daily OS trust: the founder leaves knowing what happened and what comes next. Strong-band narrative polish remains for Founder Validation, not a blocker.

---

## 4. Returning the next day

**Surfaces:** Home resume / Continue · day_complete → new mission · Revision auto-begin · quick actions

### Strengths

- In-progress Home CTA is **Continue** with deep-link (no re-commitment POST) — CQ-003 Critical items closed.
- Resume hero is light; “Still on this because …” reconnection (CQ-003 / CQ-005).
- Workspace restore on session re-entry is strongly tested.
- Revision begin auto-enters Activity like Home (CQ-003).
- Next-day fresh start presents a new mission; no streak gamification (anti-shame policy).

### Weaknesses

- Fresh-start density returns on a new day (same A01).
- Resume still routes via Overview URL (A06).
- Dual-run / Runtime C / Unified Journey forks exist in codebase but are not production default (`SOLE_RUNTIME=1`; Unified Journey not set on Render).

### Adoption blockers

| ID | Issue | Stops daily use? | Class |
|---|---|---|---|
| A10 | Dual-run / flag forks if misconfigured | Would confuse if sole runtime off — **operational constraint**: keep production sole-runtime | **Constraint** |
| A11 | Next-day fresh-start density | Same as A01 — Minor | **Minor** |

### Commercial impact

Return-day continuity is one of the strongest CQ outcomes. Habit fit is Emerging and suitable for founder daily adoption under documented constraints.

---

## 5. Cross-cutting adoption verdict

| Stage | Ready for daily founder use? | Caps exclusive CS1 claim? |
|---|---|---|
| Before | Yes | Scarce-time polish only |
| During | Yes as OS | **Yes** — scaffolded practice depth |
| After | Yes | Narrative Strong-band open |
| Return | Yes | Density residual only |

**Overall audit:** The end-to-end loop is **real, tested, and operable every day** under sole runtime. No Critical or Major engineering blocker remains that would stop daily use. Exclusive CS1 preparation is realistic **as an operating system** only if the founder accepts that exam-grade practice content still comes from authorised materials alongside Kwalitec sessions.

---

**End of Founder Adoption Audit**

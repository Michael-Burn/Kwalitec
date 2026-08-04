# PX-002 — Premium Experience Success Metrics

**Programme:** PX-002 — Premium Experience Workstream Planning  
**Status:** Planning complete — **implementation not authorised**  
**Effective:** 2026-08-04  
**Authority:** `PREMIUM_QUALITY_ATTRIBUTES.md` · `PX001_PROGRAMME_CHARTER.md` · `PX002_WORKSTREAMS.md` · P-001.1 KSI · CQ-001 CRI  

**Rule:** Metrics measure Version 1 **experience quality**. They are not vanity counts (pageviews, time-on-site maximisation, streak theatre, pass-rate marketing). Educational usefulness remains governed by KSI / Progressive Confidence — PX metrics must not contradict educational honesty.

---

## 1. Purpose

Define measurable Version 1 quality metrics for Premium Experience so waves can exit with evidence instead of aspiration.

---

## 2. Metric design principles

1. **Observable** — screenshot, test, dogfood log, or instrumented event with clear definition.  
2. **Student-centred** — answers “can I trust and finish today’s study calmly?”  
3. **Non-vanity** — no metrics that reward engagement theatre or false precision.  
4. **Separable from education** — UX fail ≠ educational fail; educational PASS ≠ premium PASS.  
5. **Provisional vs validated** — dogfood/scorecard = provisional until cohort evidence exists.  
6. **Under-claim** — prefer Conditional over inflated PASS.

---

## 3. Metric catalogue

### M1 — Navigation trust

| Field | Detail |
|-------|--------|
| **Definition** | Student-visible Finish / Home / title chrome identity matches active package / journey state on Learning and Revision days. |
| **Measure** | % of audited sittings with package-path chrome match; soft-match keyword chrome = fail. |
| **Target (V1)** | **100%** on Founder dogfood primary path; **0** open S1 chrome IDs (001, 002) without waiver. |
| **Evidence** | Automated chrome tests + screenshots; PB soft-pass class cleared. |
| **Anti-vanity** | Not “nav click count.” |

### M2 — Duration & label consistency

| Field | Detail |
|-------|--------|
| **Definition** | Same study day shows one resolved duration (or explicit dual explanation); Profile exam label matches Plan when plan exists. |
| **Measure** | Cross-surface duration equality rate; Profile “Not set” with active plan exam = fail. |
| **Target (V1)** | **0** unexplained divergences on audited weekend + weekday fixtures; PX-B-035/054 Closed. |
| **Evidence** | Resolver tests + Profile/Plan screenshot pair. |
| **Anti-vanity** | Not “more duration widgets.” |

### M3 — Workflow completion honesty

| Field | Detail |
|-------|--------|
| **Definition** | Step chrome and completion behaviour match the authoritative happy path; Finish behaviour is intentional. |
| **Measure** | Phantom Complete step absent or reachable; dual-path confusion incidents on dogfood = 0 after **D-SESSION-PATH**. |
| **Target (V1)** | PX-B-014/015/016 Closed or waived with product note. |
| **Evidence** | Path checklist; confirm-modal test. |
| **Anti-vanity** | Not “sessions started” volume. |

### M4 — Revision continuity reliability

| Field | Detail |
|-------|--------|
| **Definition** | Natural tip-complete yields terminal Revision without force-regenerate; Revision presentation language fits retrieval. |
| **Measure** | Force-R1 required on natural path = fail; Q6 revision variant present. |
| **Target (V1)** | **0 / N** force-R1 on Rho-equivalent natural cohort (N≥5 personas or Founder chain). |
| **Evidence** | Automated regenerate test + PB-class simulation notes. |
| **Anti-vanity** | Not “revision minutes consumed.” |

### M5 — Accessibility readiness

| Field | Detail |
|-------|--------|
| **Definition** | Primary path is keyboard-complete; touch targets ≥44px on icon/nav; contrast AA on sidebar labels; reduced-motion honoured; automated a11y smoke + one AT pass recorded. |
| **Measure** | Checklist pass rate; CI axe critical issues on primary routes = 0 (or owned); AT pass filed. |
| **Target (V1)** | PX-B-023–030 Closed or Board risk-owned; **no** unscoped WCAG marketing claim. |
| **Evidence** | `PX002_TEST_STRATEGY.md` WS-06 pack. |
| **Anti-vanity** | Not “accessibility score 100” without scope. |

### M6 — Mobile quality

| Field | Detail |
|-------|--------|
| **Definition** | One deliberate mobile nav pattern; primary path usable on live phone and tablet. |
| **Measure** | Evidence pack exists; open S1 mobile unknowns = 0; mis-tap defects on primary CTA Closed or owned. |
| **Target (V1)** | PX-B-036/037 Closed; mobile Target on quality attributes. |
| **Evidence** | Device screenshots/video. |
| **Anti-vanity** | Not “mobile sessions %.” |

### M7 — Consistency (verbs & identity)

| Field | Detail |
|-------|--------|
| **Definition** | One start/continue/resume verb family; student-grade identity (no Internal Alpha theatre on student paths); no raw build metadata in default Settings. |
| **Measure** | Verb audit across Home/Mission/Session/Revision; identity string scan; diagnostic disclosure collapsed. |
| **Target (V1)** | PX-B-034, 038, 039, 043 Closed. |
| **Evidence** | Editorial checklist + tests. |
| **Anti-vanity** | Not “unique copy variants.” |

### M8 — Visual polish & composition

| Field | Detail |
|-------|--------|
| **Definition** | Home is one composition (heading, duration, reason, primary CTA); Analytics avoids false-precision KPI theatre; restrained motion present and optional. |
| **Measure** | Scorecard Target on Home composition; ≤4 KPIs/row; motion count 2–3 house patterns with reduced-motion. |
| **Target (V1)** | PX-B-010/011 Target; 018 Conditional acceptable if Nice to Have deferred with owner. |
| **Evidence** | Before/after screenshots; attributes scorecard. |
| **Anti-vanity** | Not “more panels / more animation.” |

### M9 — Loading & interactive readiness

| Field | Detail |
|-------|--------|
| **Definition** | Primary paths show coherent loading; controls do not appear actionable before ready; Continue Session recovers under load. |
| **Measure** | Blank-paint incidents on dogfood; premature control defects = 0 on audited inventory; contention recovery success rate in PB ops notes. |
| **Target (V1)** | Perceived performance ≥ Target vs attributes (improve from RP-001.4 score 3); PX-B-008/031/032/033 Closed or Conditional owned. |
| **Evidence** | Throttle dogfood; PB contention notes. |
| **Anti-vanity** | Not “optimistic UI that lies.” |

### M10 — Student confidence (experience)

| Field | Detail |
|-------|--------|
| **Definition** | Diligent Founder/dogfood judgment that the finished educational product *feels* trustworthy and calm enough for daily reliance — **experience confidence**, not exam-pass prediction. |
| **Measure** | Structured Founder ratings on: chrome trust, next-action clarity, emotional tone, help usefulness, celebration honesty (1–5); multi-week chrome-growth log without S1 reopen. |
| **Target (V1)** | Mean ≥ **4.0** on dogfood rubric **and** Premium scorecard PASS or Conditional with owned residuals (PX-B-053). |
| **Evidence** | WS-11 log + WS-12 scorecard. |
| **Anti-vanity** | Not NPS spam; not until-exam trust claim; not pass-rate. |

### M11 — Help & recovery dignity

| Field | Detail |
|-------|--------|
| **Definition** | Help Centre answers core how-do-I topics; auth recovery messaging honest; error Reference ID usable. |
| **Measure** | FAQ topic coverage checklist; recovery copy review; error-page guidance present. |
| **Target (V1)** | PX-B-042, 017 (UX/SLA), 020 Closed or owned. |
| **Evidence** | Help walkthrough; error screenshot. |
| **Anti-vanity** | Not “help article count.” |

### M12 — Motivation without punishment

| Field | Detail |
|-------|--------|
| **Definition** | Return-after-gap and diligence cues welcome without streak shame; milestones acknowledge arcs without pass promises. |
| **Measure** | Editorial review against MO-* / EJ honesty; zero guilt-primary CTAs on gap return. |
| **Target (V1)** | If Wave 7 ships: PX-B-044–047 Closed; if deferred: explicitly out of V1 premium floor (Nice to Have). |
| **Evidence** | Copy review sign-off. |
| **Anti-vanity** | Not streak length maximisation. |

---

## 4. Mapping metrics → workstreams

| Metric | Primary workstreams |
|--------|---------------------|
| M1 | WS-01 |
| M2 | WS-01 |
| M3 | WS-02 |
| M4 | WS-03 |
| M5 | WS-06 |
| M6 | WS-05 |
| M7 | WS-07 · WS-01 (verbs) |
| M8 | WS-04 · WS-10 |
| M9 | WS-08 · WS-09 · WS-02 (033) |
| M10 | WS-11 · WS-12 |
| M11 | WS-07 · WS-02 · WS-10 |
| M12 | WS-07 · WS-10 |

---

## 5. Wave exit metric gates

| Wave | Must move |
|------|-----------|
| 1 | M1, M2 |
| 2 | M4 |
| 3 | M3 (partial), M7, M11 (partial) |
| 4 | M5, M6 |
| 5 | M8 (Home), M9 (skeletons), M11 (Help) |
| 6 | M3 (unify), M9 (reliability/perf) |
| 7 | M8 (motion), M12 |
| 8 | M10 (certification) |

---

## 6. Relationship to KSI and CRI

| Framework | PX-002 posture |
|-----------|----------------|
| **KSI** | Experience craft may support **perceived** usefulness (especially K5 Motivation presentation, K7 Revision presentation, K8 explainability *presentation*). Planning ΔKSI = **0** until implementation validates category lifts. **No K2 claim** without recommendation checklist (PX must not change recommendations). |
| **CRI** | Implementation is expected to lift **CR5 Experience Cohesion**, **CR6 Premium Craft**, and maintain **CR7** via reliability work. Planning ΔCRI = **0**. Do not tag commercial launch from UX alone (CR9 last). |
| **Progressive Confidence** | Remains educational gate; PX metrics must not greenwash soft-fails. |

---

## 7. Explicit non-metrics (rejected)

- Daily active users / session length maximisation  
- Streak length as success  
- Pass-rate or “preparedness %” theatre  
- Animation count without reduced-motion  
- Number of microcopy variants  
- Raw Lighthouse score without student-path scope  
- Until-exam trust asserted from chrome alone  

Signed: Product Experience · PX-002 Success Metrics · 2026-08-04

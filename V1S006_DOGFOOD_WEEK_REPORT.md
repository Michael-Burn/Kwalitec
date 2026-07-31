# V1S-006 — Founder Live Dogfooding & Educational Evidence Collection

**Programme:** V1S-006 · Version 1 Stabilisation  
**Phase:** Exclusive CS1 live week (observation / evidence only)  
**Date:** 2026-07-31  
**Authority:** V1S-005 · `V1_RELEASE_CRITERIA.md` · Founder Version 1 Readiness  
**Nature:** No feature work · No architecture · No refactoring

---

## Executive Summary

Package readiness for exclusive CS1 dogfood is **READY** on the local dogfood environment (Runtime C enrolment ON, active published CS1 `2026.1`, routing reason `dogfood_curriculum_cutover`, founder user enrolled). Day 1 live study nevertheless **failed to complete a mission**: Session fell back to Runtime A because no Student Curriculum Instance (SCI) exists, and Educational Authoring’s `"xp"` scrub destroys verbs such as *Explain* / *exploratory* on Home.

**Verdict:** **HOLD — do not proceed to private beta.**  
Evidence is sufficient to decide **NO** on private beta today. The 5–7 consecutive live-day success bar is **NOT MET** (1 live day, Session blocked). Resume the exclusive week only after DF-013 and DF-014 are remediated in a separate programme.

Canonical registry: `app/services/dogfood_validation.py` · Founder board: `/founder/v1-readiness`.

---

## Mandatory first step — environment confirmation

| Check | Result | Evidence |
|---|---|---|
| Package readiness (CS1) | **READY** | `assess_dogfood_package_readiness("CS1").ready is True` |
| Runtime C enrolment flag | **ON** | `ENABLE_RUNTIME_C_ENROLMENT=True` (dev default + `.env`) |
| Published CS1 package | **Active** | `published_curriculum_packages` id=1, `2026.1`, `published_by=rr001` |
| Founder Runtime C enrol | **Active** | `runtime_enrolments` user_id=1 subject=CS1 status=active |
| Commercial Loop | **ON** (set for week) | `SR_COMMERCIAL_LOOP=1` added to local `.env` (documented) |
| Dogfood environment | **Local SQLite** | `instance/kwalitec.db`; Alembic note: db `202607300004` behind head `202607300005` |
| SCI for enrolled student | **MISSING** | `sci_student_curriculum_instances` count=**0** → Day 1 blocker |

---

## Daily Session Log

### Day 1 — 2026-07-31 · CS1 · `live_sitting` · **blocked**

| Field | Record |
|---|---|
| Date | 2026-07-31 |
| Duration | 55 minutes |
| Mission | Study 1.1 — Describe the purpose and function of data analysis (Home) |
| Completion | **blocked** — Session activity redirected to overview; no Sitting Report |
| Confidence before | 4/5 |
| Confidence after | 2/5 |
| Motivation before | 4/5 |
| Motivation after | 2/5 |
| Confusion points | `Elain`/`elain` instead of Explain; `eloratory`; title `Study 1 — .1`; 125 min Home vs ~24 min Session; Session label `Core methods` |
| Learning friction | DF-013, DF-014, DF-015, DF-016 (new) |
| Unexpected behaviour | `ri001_runtime_a_fallback` `no_active_sci`; Learning Journey TypeError |
| External resources used | None (Kwalitec only) |
| Workaround reasons | (1) Process/env Commercial Loop enabled and documented in `.env`; (2) Stopped at overview — **no silent workaround** to force completion |

#### Post-session validation

| Question | Answer |
|---|---|
| Did today's mission make sense? | Partial — Home arc clear; Session substance drifted |
| Did today's explanation help? | No — xp scrub + circular criteria |
| Was anything missing? | Yes — SCI binding; durable Session path; Learning Journey |
| Did I know what to do next? | Yes on Home; No after Session fallback |
| Would I willingly return tomorrow? | **No** until Session completes without Runtime A fallback and copy is readable |

### Days 2–7

**Not executed.** Consecutive-week bar requires Session to complete. Continuing while DF-014 is open would only accumulate blocked sittings.

---

## Educational Findings

1. **Home Adaptive Workspace arc works** when package + enrolment present: Morning Brief → Today's Mission → Learning Episode → Tomorrow Preview → Start Today's Session (primary CTA). No `strategy` / `runtime-c` / `coverage signal` leaks observed on Home.
2. **Episode prose is educationally damaged** by substring scrub of `"xp"` (`guidance.scrub`) — violates E1/E4 trust even when composition structure is present.
3. **Tomorrow continuity exists** but inherits scrub damage (`1.2 Complete eloratory data analysis`).
4. **Session does not reliably continue today's certified mission** without SCI — violates exclusive-week “only Kwalitec” usability and E8 dual-truth risk (Runtime A fallback telemetry).
5. **My Learning Journey is unavailable** (shell_vm TypeError) — breaks post-sitting narrative surface.
6. **Extra Study correctly absent** when Home duration fills available minutes (E7 observation holds on Day 1).

---

## Learning Friction Trends

### Resolved (unchanged from V1S-005 — no duplicates)

DF-001…DF-011 friction records remain in `LEARNING_FRICTION_REGISTER` (package gate, progress isolation, quiet episode, Syllabus naming, Home hierarchy, CTA honesty, archive wording, narrative, session stages, forecast QA, footer).

### Open (new discoveries — V1S-006)

| ID | Class | Priority | Status | Title |
|---|---|---|---|---|
| DF-013 | BUG | P0 | OPEN | Authoring scrub strips `xp` from educational prose |
| DF-014 | BUG | P0 | OPEN | Runtime C enrolment without SCI blocks Session |
| DF-015 | BUG | P1 | OPEN | My Learning Journey crashes (`shell_vm` call) |
| DF-016 | LEARNING FRICTION | P1 | OPEN | Topic title / duration / Session label mismatch |

### Deferred (unchanged)

DF-012 (loading skeleton) · DF-TD01 (RI-002 hard removal)

### Trend summary

| Metric | V1S-005 end | After Day 1 |
|---|---|---|
| Open P0 | 0 | **2** |
| Live sittings | 0 | 1 (blocked) |
| Live days | 0 | 1 / 5 required |
| Avg confidence (all sittings) | 3.0 | ~2.75 |
| Willingness to return tomorrow | Path clear | **No** |

---

## Behaviour Patterns

- Founder starts the day willing (confidence/motivation 4) when Home looks coherent.
- Session failure + mangled copy collapses both to 2 within one sitting.
- Without SCI, the product **looks** Runtime C on Home and **behaves** Runtime A on Session — the exact dual-truth risk V1S-005 claimed to isolate for Progress.
- Commercial Loop must be explicit in `.env` for dogfood; it was missing before Day 1 (now documented ON).

---

## Release Impact

| Gate / claim | Impact |
|---|---|
| Dogfooding GO | Reverts to **HOLD** despite package gate READY |
| Private beta | **NO-GO** — evidence says not yet |
| Production-ready / G1 | Unchanged FAIL / not claimed |
| E1–E4 live spot-check | **FAIL** on Day 1 (scrub + Session substance) |
| E8 dual truth | **At risk** — Runtime A fallback on Session |
| A3 dogfood authority | Package routing READY; Session SCI gap undermines student path |

---

## Updated Readiness

Founder `/founder/v1-readiness` now programme **V1S-006** with:

- Confidence / Motivation / Completion / Study Consistency / Learning Friction trends
- Package readiness READY
- Overall status: **HOLD — live week blocked (P0 friction)**

See `build_v1_readiness_snapshot()`.

---

## Recommendation

1. **Do not start private beta.**
2. Open a remediation programme (suggested **V1S-007**) limited to:
   - DF-013: word-boundary / whole-token scrub (never substring `xp`)
   - DF-014: create/bind SCI on Runtime C enrol; block Runtime A fallback for dogfood CS1
   - DF-015: fix `shell_vm` keyword call on Learning Journey
   - DF-016: verify after SCI fix; title digit drop if still present
3. Persist `SR_COMMERCIAL_LOOP=1` + Runtime C enrolment for the dogfood account.
4. Restart Days 1–7 only when Session completes Home→Activity→Sitting Report without Runtime A fallback and without undocumented workarounds.
5. Append each day as `evidence_kind=live_sitting` in `dogfood_validation.py`.

**Private beta decision from this evidence:** **NO — not yet.**

---

## Student Impact Assessment

| Lens | Assessment |
|---|---|
| Student problem | Cannot finish a real study day; prose is broken; journey page crashes |
| Student benefit | Honesty: blockers recorded before inviting others |
| Learning benefit | Confirms package gate alone is insufficient for exclusive study |
| Success metrics | 5–7 days NOT MET; private beta decision = NO |
| Risks | Declaring week complete with fabricated days; fixing code inside V1S-006 |
| Assumptions | Founder continues exclusive week after P0 remediation |

---

## Estimated KSI contribution

**ΔKSI = 0** (provisional). Observation only; validated KSI still requires a completed exclusive week after blockers clear.

---

## Evidence collected

- `app/services/dogfood_validation.py` (Day 1 `live_sitting`, DF-013…016)
- `app/services/v1_readiness_dashboard.py` / `v1_readiness.html` trends
- `tests/test_v1s006_dogfood_week.py`
- Live captures: `/tmp/v1s006_home.html`, `/tmp/v1s006_session.html`, `/tmp/v1s006_overview.html`
- DB: Runtime C enrolment present; SCI count 0; scrub unit check `Explain`→`Elain`

---

## Lessons learned for student value

Package readiness and Home composition can look “GO” while Session is unusable. Educational scrubbing that treats gamification tokens as substrings destroys ordinary English. Exclusive week evidence must include a finished Session, not only a composed Home.

---

## Explainability Review

**N/A for new intelligence.** Observation only; no recommendation ranking changes.

---

## Recommendation Quality Review

**N/A for ranking changes.** Primary CTA remained Start Today's Session; secondary honesty from V1S-005 held on Home.

---

## Version 1 readiness residual

Open: DF-013 · DF-014 · DF-015 · DF-016 · 5–7 live days · G1 KSI · RI-002 · mission package REMOVE · `src/` · DF-012 · Alembic head lag on local DB.

---

## CRI domains improved

None (evidence collection). **ΔCRI = 0** provisional.

---

## Remaining blockers

See Recommendation + Founder Remaining blockers.

---

## Provisional or validated

All scores and the private-beta **NO** decision are **provisional founder evidence** grounded in one live sitting — not validated KSI.

---

## Tests Executed

```
python3 -m pytest tests/test_v1s006_dogfood_week.py \
  tests/test_v1s005_dogfood_remediation.py \
  tests/test_v1s004_dogfood_validation.py -q
```

Outcome: **33 passed**. Ruff clean on touched modules.

## Migration Impact

**None** — no Alembic / schema changes in this programme. Local DB remains one revision behind head (environment note only).

## Files Created

- `V1S006_DOGFOOD_WEEK_REPORT.md`
- `tests/test_v1s006_dogfood_week.py`

## Files Modified

- `app/services/dogfood_validation.py`
- `app/services/v1_readiness_dashboard.py`
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`
- `tests/test_v1s005_dogfood_remediation.py`
- `V1_RELEASE_CRITERIA.md`
- Local `.env` (Commercial Loop + Runtime C — not for commit)

## Architecture Compliance

- Observation / Founder observability only — no educational algorithm changes.
- Curriculum V1/V2 loader singularity untouched.
- V1S-002 dogfood cutover retained; Day 1 exposed Session SCI gap under that cutover.

## Technical Debt

- DF-013 / DF-014 are new dogfood-blocking debt owned for next remediation.
- RI-002 remains deferred but is now implicated by live Session fallback.

## Known Limitations

1. Only Day 1 of 5–7 consecutive days executed.
2. Mission not completed — Session blocked.
3. No product fixes in V1S-006 by design.
4. Does not claim P-002.1 production-ready.

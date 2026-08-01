# EA-006 — Live Validation Report

**Programme:** Educational Excellence Programme EA-006 — Educational Package Publication  
**Date:** 2026-08-01  
**Package:** `CS1-EA005-PKG-4.2-GLM-STRUCTURE` · publication version `ea006-live-1.0.0`  
**Subject / node:** CS1 · 4.2 — Understand and use generalised linear models  
**Method:** Deterministic application-path validation of the published package against Mission Blueprint, Session Blueprint, Tutor Voice, CMP guidance, and EV-001 failure classes  

---

## 1. Validation scope

Validate that the published package:

1. Appears correctly in the live application educational pipeline  
2. Follows the Mission Blueprint  
3. Follows the Session Blueprint  
4. Uses the certified Tutor Voice  
5. Guides the student into the CMP  
6. Contains no placeholder content  
7. Contains no generic wording  
8. Preserves educational continuity  

**Environment:** Integrated application code path (substance planner, authoring composition, Home overlays, reflection, sitting tomorrow). Automated tests: `tests/application/educational_packages/test_ea006_publication.py` (7 passed).  

**Note:** Production host re-walk (https://kwalitec.onrender.com) requires deploy of this publication. Pre-deploy validation proves the student pathway consumes the certified pack when topic 4.2 is bound.

---

## 2. Pipeline appearance

| Surface | Expected | Observed |
|---------|----------|----------|
| Package loader | Resolves `4.2` / GLM title / `CS1-D-T02` | PASS — `find_educational_package` returns approved pack |
| Session substance | `source=educational_package` | PASS |
| Topic title in session | Real 4.2 title — never “Today’s topic” | PASS |
| Home display title | `Extend linear models into GLM structure` | PASS (presentation overlay) |
| Home why_now | Tutor brief after 4.1 → GLM structure | PASS |
| Reading activity | CMP open/stop/focus/exit packet | PASS |
| Knowledge Checks | Active Recall + Checkpoint | PASS — 2 scoreable practice items |
| Reflection | GLM chain stickiness harvest | PASS |
| Tomorrow Preview | 5.1 Bayesian continuity | PASS |

---

## 3. Mission Blueprint compliance

| Blueprint expectation | Evidence in live pack path |
|-----------------------|----------------------------|
| Decisive display title | `Extend linear models into GLM structure` |
| Learning objective | Explain GLM chain (family → η → link) |
| Prior bridge | 4.1 classical linear models → today non-Normal |
| Why now | Lawful next node + examiner link justification |
| Concept focus | Exponential family → linear predictor → link |
| Success criteria | Closed-book chain; family+link; CMP locus note |
| CMP scope | Open 4.2 setup; stop after first structural example |
| Tomorrow bridge | 5.1 priors/posteriors continuity |

**Verdict:** PASS — Mission Blueprint fields are the student-facing substance for 4.2.

---

## 4. Session Blueprint compliance

| Stage job | Live mapping |
|-----------|--------------|
| Guided Reading | Activity `act-read-1` — full Reading Guidance body + exit line |
| Structure / re-entry | Activity `act-example-1` — pause points + re-entry line |
| Knowledge Checks | `act-practice-1` Active Recall · `act-practice-2` Checkpoint |
| Reflection | Pack reflection prompt on matching topic |
| Wrap-up / Tomorrow | Pack wrap-up language · Tomorrow Preview 5.1 |

Advertised arc remains Read → Worked example → Practice inside the existing Session shell (**no new UI features**). Educational jobs of Guided Reading + two Knowledge Checks are preserved.

**Verdict:** PASS — Session Blueprint educational jobs delivered through the existing shell.

---

## 5. Tutor Voice

| Voice test | Result |
|------------|--------|
| Specific to GLM structure (not topic-swap generic) | PASS |
| No platform jargon (“twin”, “runtime”, “pipeline”) | PASS |
| Guides into CMP; does not paste CMP prose | PASS — Guidance Over Content |
| Honest Study Progress (not mastery theatre) | PASS — wrap-up denies Topic Complete |
| Continuity voice (4.1 → 4.2 → 5.1) | PASS |

**Verdict:** PASS — certified Tutor Voice from EA-005 retained.

---

## 6. CMP guidance

| Element | Present |
|---------|---------|
| Open point | CMP · Syllabus 4.2 GLM setup (4.2.1–4.2.3 centre) |
| Focus questions | 4 (η, exponential family, non-identity link, success link) |
| Misconception watch | 3 items |
| Stop condition | First structural worked example with non-identity link |
| Exit line / return cue | Present |
| Out of scope today | Deviance deep-dive, Bayesian, coding marathon, etc. |

**Verdict:** PASS — student is guided into the CMP, not given an empty shell.

---

## 7. Placeholder / generic wording audit

| Forbidden pattern | Present in pack path? |
|-------------------|------------------------|
| “Today’s topic” | No |
| “Strengthen today’s focus topic” | No |
| Syllabus-only Mission title as sole brief | No — display title + narrative |
| Empty reading body (LO list only) | No — full guidance packet |
| Cash-flow / unrelated practice seed | No — GLM Knowledge Checks |
| Interchangeable “highest-value next step” why_now | No — unique GLM why_now |

**Verdict:** PASS.

---

## 8. Educational continuity

```text
4.1 classical linear models (prior bridge)
        ↓
4.2 GLM structure Mission + Session (published pack)
        ↓
5.1 Bayesian foundations (Tomorrow Preview)
```

Mission tomorrow_bridge, Session Tomorrow Preparation, and sitting-report tomorrow line agree on **5.1**.

**Verdict:** PASS.

---

## 9. EV-001 failure class remediation (this package)

| Trust break | Pre-publication (EV-001) | Post-publication (this pack) |
|-------------|--------------------------|------------------------------|
| TB-001 placeholder topic | FAIL | Remediated for 4.2 |
| TB-002 syllabus-paste Mission | FAIL | Remediated for 4.2 |
| TB-007 empty reading | FAIL | Remediated for 4.2 |
| TB-004 generic explainability | FAIL on DJ pattern | Pack why_now unique (DJ system-wide boilerplate not claimed fixed) |
| TB-003 contaminant address topic | FAIL elsewhere | Unchanged — out of scope |
| TB-005 mastery theatre | FAIL system-wide | Pack language honest; system scoreboard out of scope |

**Student experience improvement (this package):** A diligent student on 4.2 now receives a tutor-grade Mission brief, CMP Reading Guidance, closed-book Knowledge Checks, topic-specific Reflection, and a coherent Tomorrow Preview — instead of a placeholder shell.

---

## 10. Live validation verdict

| Criterion | Result |
|-----------|--------|
| Appears in live educational pipeline | **PASS** |
| Mission Blueprint | **PASS** |
| Session Blueprint | **PASS** |
| Tutor Voice | **PASS** |
| Guides into CMP | **PASS** |
| No placeholders | **PASS** |
| No generic wording | **PASS** |
| Continuity preserved | **PASS** |

**Overall: PASS** (application-path validation). Production dogfood re-walk recommended after deploy; does not block EA-006 PASS for publication integration proof.

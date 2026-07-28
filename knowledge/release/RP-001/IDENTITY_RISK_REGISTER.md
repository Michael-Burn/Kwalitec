# RP-001.3 — Identity Risk Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.3 — Study Sensei Identity & Voice Certification  
**Date:** 2026-07-28  
**Status:** Active for Alpha identity / voice residual tracking  
**Related:** `STUDY_SENSEI_IDENTITY_AUDIT.md`, `JOURNEY_RISK_REGISTER.md`, `RISK_REGISTER.md`

---

## Purpose

Catalogue risks that undermine **one consistent Study Sensei identity**, including trust and educational consistency risks visible through language and presentation. No mitigations implemented in this package.

Severity: **Critical / High / Medium / Low**.  
Likelihood: **Likely / Possible / Unlikely** for Alpha cohort perception.

---

## Risk summary

| ID | Title | Severity | Likelihood | Certification impact |
|----|-------|----------|------------|----------------------|
| IR-01 | Dual narrator (Kwalitec vs Study Sensei) | High | Likely | Blocks unqualified identity Pass |
| IR-02 | Mission / Session / tip / Recommendation synonym storm | High | Likely | Blocks noun unity |
| IR-03 | False reflection affordances on Home | Critical | Likely | Surface Fail (SS-10); overlaps JR-06 |
| IR-04 | Multiple reflection systems without student map | High | Likely | Confusion / trust |
| IR-05 | “Why the system chose this” robotic chrome | Medium | Unlikely (flag OFF) | Fail if Runtime C enabled |
| IR-06 | Onboarding never names Study Sensei | Medium | Likely | First-session identity gap |
| IR-07 | Help FAQ lexicon lags ILE memory surfaces | Medium | Possible | Incomplete mental model |
| IR-08 | Explanation “tip” understates guidance | Medium | Possible | Tone drift |
| IR-09 | Dual chrome / dual OS atmosphere | Medium | Likely | Overlaps JR-02 / R-02 |
| IR-10 | Empty Home without Sensei waiting narrative | Medium | Possible | Overlaps JR-04 |
| IR-11 | Exam/test-adjacent Help phrasing | Medium | Possible | Anxiety residual |
| IR-12 | Profile notifications flag without push product | Low | Possible | Overlaps JR-20 |
| IR-13 | Streak language in legacy/settings export | Low | Possible | Engagement bleed |
| IR-14 | Journal empty mentions Quick Check while QC OFF | Low | Possible | Flag-scope honesty |
| IR-15 | Mission Intelligence + MES duplication | Medium | Possible | Overlaps JR-05 |
| IR-16 | No cohort voice validation | High | Certain (process) | Cert is code-audit only |
| IR-17 | Assessment flash brands Kwalitec not Sensei | Low | Possible | Secondary path |
| IR-18 | “Optimising for {axis}” engineering tone | Low | Possible | Mild robotic drift |
| IR-19 | Default benefit “strengthen your exam readiness” | Low | Possible | Mild overclaim if overused |
| IR-20 | Unified Journey nav lexicon (if enabled) | Medium | Unlikely (OFF) | Alternate identity map |

---

## Risk records

### IR-01 — Dual narrator (Kwalitec vs Study Sensei)

| Field | Detail |
|-------|--------|
| **Description** | Onboarding/Help/auth speak as **Kwalitec**; Journal/Timeline/Mission Intelligence speak as **Study Sensei**; Home often speaks as unnamed calm guidance. |
| **Educational risk** | Learner may not form a single mentor relationship — guidance feels like “the app” sometimes and “a Sensei” elsewhere. |
| **Trust risk** | Brand switching can feel like different authors wrote different screens. |
| **Evidence** | `alpha_onboarding_service.py`; Journal/Timeline DTOs; login flash. |
| **Mitigation direction** | Introduce Sensei once in onboarding; use Sensei on guidance/memory; reserve Kwalitec for product/Alpha/support. |
| **Status** | Open — docs only |

---

### IR-02 — Mission / Session / tip / Recommendation synonym storm

| Field | Detail |
|-------|--------|
| **Description** | Same daily focus called Today's Mission, Today's Session, Today's Recommendation, Mission tip, and tip. |
| **Educational risk** | Student cannot map “what I accepted” to “what I did” across Home → Session → Journal. |
| **Trust risk** | Looks like inconsistent product thinking. |
| **Evidence** | PX-002A vs ILE-004 vs `explanation_card.html` vs Journal empty copy. |
| **Mitigation direction** | Board-level noun decision; then Help/onboarding glossary; presentation tests. |
| **Status** | Open |

---

### IR-03 — False reflection affordances on Home

| Field | Detail |
|-------|--------|
| **Description** | “Done reflecting” / “Skip for today” appear as controls but do not save (presentation-only). |
| **Educational risk** | Student believes reflection closed the loop when nothing was recorded. |
| **Trust risk** | Direct Sensei honesty failure — Sensei must not fake listening. |
| **Evidence** | `home.html` reflection preview; JR-06. |
| **Mitigation direction** | Remove, disable clearly, or wire to real reflection — journey package residual. |
| **Status** | Open — **Critical** |

---

### IR-04 — Multiple reflection systems without student map

| Field | Detail |
|-------|--------|
| **Description** | Commitment reflection, ILE-005 journal reflection, session reflection, Home preview, research check-in. |
| **Educational risk** | Reflection loses educational meaning; becomes “another form.” |
| **Trust risk** | Optional-vs-required confusion; Check-in mistaken for Sensei. |
| **Evidence** | Audit SS-14 / SS-21; JR-08. |
| **Mitigation direction** | Short student-facing map in Help/onboarding (copy programme). |
| **Status** | Open |

---

### IR-05 — “Why the system chose this”

| Field | Detail |
|-------|--------|
| **Description** | Runtime C educational panel summary attributes choice to “the system.” |
| **Educational risk** | Undermines Study Sensei as human-professional guide metaphor. |
| **Trust risk** | Sounds algorithmic and cold. |
| **Evidence** | `educational_experience.html`; flag OFF. |
| **Mitigation direction** | Rename summary before any Runtime C enablement. |
| **Status** | Contained by flag |

---

### IR-06 — Onboarding never names Study Sensei

| Field | Detail |
|-------|--------|
| **Description** | Four orientation steps brand Kwalitec only. |
| **Educational risk** | Later Sensei-labelled Journal/Timeline feel like a different product module. |
| **Evidence** | `ONBOARDING_STEPS`. |
| **Mitigation direction** | One sentence introducing Study Sensei as how Kwalitec guides daily decisions. |
| **Status** | Open |

---

### IR-07 — Help FAQ lexicon lags ILE memory surfaces

| Field | Detail |
|-------|--------|
| **Description** | Help centres Session/Exam Readiness; weak coverage of Decision Journal, Educational Timeline, Mission Intelligence, Study Sensei. |
| **Educational risk** | Support path teaches an incomplete Alpha model. |
| **Evidence** | `help.html` popular topics. |
| **Mitigation direction** | Add FAQ entries for Journal/Timeline/Sensei; align Session/Mission wording. |
| **Status** | Open |

---

### IR-08 — Explanation “tip” understates guidance

| Field | Detail |
|-------|--------|
| **Description** | L2 disclosure labelled “Why this tip?” |
| **Educational risk** | Authorised Mission feels optional trivia. |
| **Evidence** | `explanation_card.html`. |
| **Mitigation direction** | “Why this guidance?” / “Why this Mission?” |
| **Status** | Open |

---

### IR-09 — Dual chrome / dual OS atmosphere

| Field | Detail |
|-------|--------|
| **Description** | V1 shell onboarding/wizard/help vs EOS student chrome. |
| **Educational risk** | Visual identity split amplifies voice split. |
| **Evidence** | JR-02; CAP-02/16/19/25. |
| **Status** | Accepted Alpha Stage 1 residual |

---

### IR-10 — Empty Home without Sensei waiting narrative

| Field | Detail |
|-------|--------|
| **Description** | Empty CTA states are product-generic; Mission Intelligence empty Sensei wait may be absent when `has_mission` false. |
| **Educational risk** | “What now?” without calm waiting explanation. |
| **Evidence** | Home empty branches; JR-04; MI empty compose strings. |
| **Status** | Open |

---

### IR-11 — Exam/test-adjacent Help phrasing

| Field | Detail |
|-------|--------|
| **Description** | “topics you're closest to being tested on” in Help. |
| **Educational risk** | Mild anxiety register vs AA anxiety-safe standard. |
| **Evidence** | `help.html`. |
| **Mitigation direction** | Prefer readiness / syllabus priority language. |
| **Status** | Open |

---

### IR-12 — Profile notifications without push product

| Field | Detail |
|-------|--------|
| **Description** | Notifications enabled/disabled display. |
| **Trust risk** | Implies push capability that Alpha lacks. |
| **Evidence** | Profile template; JR-20. |
| **Status** | Open |

---

### IR-13 — Streak language in legacy/settings export

| Field | Detail |
|-------|--------|
| **Description** | Weekly report / analytics still mention streaks; EOS educational cores forbid streak guilt. |
| **Educational risk** | Engagement bleed if students hit export/legacy views. |
| **Evidence** | Settings export lines; dashboard legacy. |
| **Status** | Contained for sole-runtime Home; residual elsewhere |

---

### IR-14 — Journal empty mentions Quick Check while QC OFF

| Field | Detail |
|-------|--------|
| **Description** | Empty Journal promises QC entries students may never see in Alpha. |
| **Trust risk** | Mild over-promise of surfaces. |
| **Evidence** | Decision Journal DTO empty_description. |
| **Status** | Open — Low |

---

### IR-15 — Mission Intelligence + MES duplication

| Field | Detail |
|-------|--------|
| **Description** | Same recommendation explained twice with overlapping labels. |
| **Educational risk** | Cognitive load; “which voice is authoritative?” |
| **Evidence** | Home hero + MI aside; JR-05. |
| **Status** | Watch cohort |

---

### IR-16 — No cohort voice validation

| Field | Detail |
|-------|--------|
| **Description** | RP-001.3 is a code/template audit only. |
| **Educational risk** | Perceived consistency may differ from engineer reading. |
| **Evidence** | Process gap; parallels JR-16. |
| **Status** | Open until Internal Alpha validation scripts include voice probes |

---

### IR-17 — Assessment flash brands Kwalitec

| Field | Detail |
|-------|--------|
| **Description** | “Thanks — that helps Kwalitec support you.” |
| **Educational risk** | Secondary path reinforces product narrator. |
| **Status** | Low — secondary Alpha surface |

---

### IR-18 — “Optimising for {axis}”

| Field | Detail |
|-------|--------|
| **Description** | Mission Intelligence metadata line. |
| **Educational risk** | Engineering register. |
| **Mitigation direction** | Prefer plain educational purpose already shown above. |
| **Status** | Open — Low |

---

### IR-19 — Default “strengthen your exam readiness”

| Field | Detail |
|-------|--------|
| **Description** | Fallback benefit string in recommendation explanation builder. |
| **Trust risk** | Mild certainty / exam outcome adjacency if overused when authored benefit missing. |
| **Evidence** | `recommendation_explanation.py` defaults. |
| **Status** | Open — Low |

---

### IR-20 — Unified Journey nav lexicon if enabled

| Field | Detail |
|-------|--------|
| **Description** | Today · Planning · Exam Readiness · Archive replaces Home · Journey · History. |
| **Educational risk** | Another full vocabulary map. |
| **Status** | Contained — flag OFF; delta cert required if enabled |

---

## Cross-links to journey / product risks

| Identity risk | Related journey / inventory risk |
|---------------|----------------------------------|
| IR-03 | JR-06 |
| IR-04 | JR-08 |
| IR-09 | JR-02 / R-02 |
| IR-10 | JR-04 |
| IR-12 | JR-20 / CAP-18 |
| IR-14 | JR-03 / flag honesty |
| IR-15 | JR-05 |
| IR-16 | JR-16 |

---

## Highest priority for a future voice package

1. IR-03 — false reflection affordances  
2. IR-01 — dual narrator  
3. IR-02 — Mission/Session/tip noun convergence  
4. IR-04 — reflection systems map  
5. IR-06 / IR-07 — onboarding + Help Sensei continuity  

---

**End of IDENTITY_RISK_REGISTER**

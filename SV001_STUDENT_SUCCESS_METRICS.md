# SV-001 — Student Success Metrics

**Programme:** Student Value Programme SV-001 — Student Value Validation  
**Document:** Student Success Metrics (Founder Validation + Private Beta)  
**Status:** Binding — measurement law for student-value claims  
**Effective:** 2026-08-01  
**Authority:** `SV001_DAILY_EDUCATIONAL_VALUE.md` · Educational Excellence (Frozen) · Educational Operations (Frozen) · CE-001 PASS · DSH-001 PASS  
**Nature:** Metrics definition only — **no** application instrumentation required in SV-001; **no** Runtime / SCI / Twin / recommendation / catalogue redesign  

---

## 1. Purpose

Define **objective student-success measures** so Founder Validation and later Private Beta can judge whether Kwalitec **genuinely improves the student’s study experience** — independent of editorial progress.

These metrics answer:

> Is each study day clearer, lighter on decisions, better for CMP craft, honestly stopped, achievable, return-worthy, and confidence-honest?

They do **not** answer:

> How much of the syllabus is certified, approved, or covered?

---

## 2. Metric families

| Family | Code | Audience | May claim student value? |
|--------|------|----------|-------------------------:|
| **Daily Educational Value** | DEV-* | Founder + Beta | **Yes — primary** |
| **Study-day success** | SS-* | Founder + Beta | **Yes** |
| **Longitudinal trust** | LT-* | Founder + Beta | **Yes** |
| **Honesty / anti-theatre** | HT-* | Founder + Beta | **Yes (gatekeepers)** |
| **Editorial / reliability (internal)** | ED-* | Editorial Board | **No** — context only |

---

## 3. Primary family — Daily Educational Value (DEV)

Defined fully in `SV001_DAILY_EDUCATIONAL_VALUE.md`. Summarised here for the metrics board.

| ID | Metric | Definition | Cadence | Target (Founder) | Target (Private Beta Stage 1) |
|----|--------|------------|---------|------------------|-------------------------------|
| **DEV-01** | DEV day score | Mean of D1–D7 (0–10) per study day | Per day | ≥ 7.0 on ≥ 80% of days in run | Cohort median ≥ 7.0 |
| **DEV-02** | DEV run score | Mean of DEV day scores across run | Per run / cohort window | ≥ 7.5 | ≥ 7.0 |
| **DEV-03** | Return-worthy rate | Share of days meeting return-worthy rules (R1–R4) | Per run | ≥ 80% | ≥ 70% |
| **DEV-04** | Trust floor | Mean of per-day min(D1…D7) | Per run | ≥ 5.5 | ≥ 5.0 |
| **DEV-05** | Dimension profile | Per-dimension means D1…D7 | Per run | No dimension mean < 6.0 | No dimension mean < 5.5 |

### 3.1 Dimension metrics (instrument)

| ID | Dimension | Question (student language) |
|----|-----------|------------------------------|
| **D1** | Direction clarity | Did you know exactly what to do? |
| **D2** | Decision-load relief | Did Kwalitec reduce decision fatigue? |
| **D3** | CMP craft | Did today’s Mission improve how you use the CMP? |
| **D4** | Stopping integrity | Did you stop at the correct point? |
| **D5** | Achievability | Did today’s work feel achievable? |
| **D6** | Return willingness | Would you willingly return tomorrow? |
| **D7** | Honest confidence | Did confidence rise without false confidence? |

Scoring: 0–10 integer or half-point; free-text “why” required for any score ≤ 5.

---

## 4. Study-day success metrics (SS)

Behavioural and completion measures that corroborate DEV. They are **supporting**, not vanity substitutes.

| ID | Metric | Definition | How measured (no new app required) | Success signal | Failure signal |
|----|--------|------------|------------------------------------|----------------|----------------|
| **SS-01** | Time-to-start | Minutes from opening Kwalitec to beginning authorised study work | Founder timer / beta self-report | ≤ 5 min typical | > 10 min hunting / deciding |
| **SS-02** | Plan invention rate | Share of days student invents own plan *despite* having a Mission | Journal flag | Near 0 when Mission present | Student routinely ignores Mission |
| **SS-03** | Sitting completion | Share of started days completed to Reflection / authorised wrap | Journal / session log | ≥ 90% Founder; ≥ 75% Beta | Frequent abandon mid-sitting |
| **SS-04** | Budget honesty | Actual study minutes vs stated day budget band | Timer vs package band | Within band ±15 min most days | Chronic overrun or underload guilt |
| **SS-05** | CMP open discipline | Student can state *why* CMP was opened and *when* to stop | End-of-day one-liner | Clear open/stop stated | “I just kept reading” |
| **SS-06** | Correct stop | Student stopped at authorised stop / wrap — not mid-fog or into next LO | Journal vs Mission stop | Match ≥ 85% days | Sprawl or premature fog-stop |
| **SS-07** | Next-day return | Student returns for next authorised day without product-caused dread | Calendar / journal | Return on schedule ≥ 80% Founder run | Skip attributed to yesterday’s product experience |

**Activity vanity ban:** Page views, raw minutes online, streak chrome, and click counts are **not** Student Success Metrics under SV-001.

---

## 5. Longitudinal trust metrics (LT)

Measured across a multi-day run (Founder Validation window or Beta Stage 1 window).

| ID | Metric | Definition | Success signal | Failure signal |
|----|--------|------------|----------------|----------------|
| **LT-01** | Willingness-to-continue | End-of-run answer: “Would you keep using Kwalitec as your primary evening director?” (0–10) | ≥ 8 Founder; cohort median ≥ 7 Beta | ≤ 5 |
| **LT-02** | Decision-fatigue trend | Slope of D2 across days 1…n | Stable or improving | Declining (product adds load as novelty fades) |
| **LT-03** | CMP craft trend | Slope of D3 across days | Improving or stable-high | Flat-low or declining |
| **LT-04** | Motivation stability | D5/D6 variance across run | Low variance; no cliff after “Golden” day | Spike-then-collapse |
| **LT-05** | Trust after day-N | End-of-run: “Do you trust Kwalitec to guide tomorrow?” (Y/N + why) | Yes with educational reason | No; or Yes from chrome only |
| **LT-06** | Replacement test | “Would you rather study tonight with CMP alone?” | Prefer Kwalitec+CMP most nights | Prefer solo CMP most nights |

LT metrics make template fatigue and orphan-excellence collapse visible — patterns DX-001 denied in inventory, which lived study must re-test.

---

## 6. Honesty / anti-theatre metrics (HT)

Gatekeeper metrics. A run can post high D6 and still **fail** SV if honesty fails.

| ID | Metric | Definition | Pass rule |
|----|--------|------------|-----------|
| **HT-01** | False-confidence incidents | Count of HF-05 (progress/readiness/journey misread as exam readiness) | **0** preferred; investigate any ≥ 1 |
| **HT-02** | Overclaim detection | Student can restate what today did **not** make them ready for | Student names a non-claim correctly ≥ 80% of days |
| **HT-03** | Dual-truth events | Conflicting “what now / how am I doing” surfaces in one sitting | **0** in Founder run |
| **HT-04** | Mastery-theatre resistance | Student rejects scoreboard-as-learning language when probed | Probe pass |
| **HT-05** | Confidence quality | Among days with D7 ≥ 7, student cites skill/evidence — not chrome | ≥ 90% of high-D7 days skill-cited |

**Law:** Rising confidence without HT pass is not student success.

---

## 7. Editorial / reliability metrics (ED) — internal only

Listed so teams do **not** confuse them with student success.

| ID | Metric | Owner programme | SV-001 role |
|----|--------|-----------------|-------------|
| **ED-01** | DSH (days) | DSH-001 | Reliability precondition — **not** DEV |
| **ED-02** | CIH (days) | DSH-001 | Founder planning only — never student value |
| **ED-03** | LO Coverage Rate (Published) | CE-001 | Inventory — **not** DEV |
| **ED-04** | Volume status / Approver | EO-001 | Shipping eligibility |
| **ED-05** | Gate CG / MG / Session gates | EA-003/004/008 | Certification eligibility |
| **ED-06** | DX Delivery Quality Index | DX-001 | Editorial delivery expectation |
| **ED-07** | Continuity Front LO | CE-001 / DSH-001 | Where dependence ends |

**Reporting rule:** ED metrics may appear on the same Founder dashboard **below** a hard visual/label break titled **Internal editorial metrics — not student value**.

---

## 8. Measurement modes

### 8.1 Founder Validation (near-term)

| Element | Rule |
|---------|------|
| Operator | Founder (or single designated validator) |
| Material | Released path preferred; Validation-mode walk of Approver-pending inventory allowed if labelled **non-student-reachable** |
| Instrument | Full scorecard in `SV001_FOUNDER_VALIDATION_SCORECARD.md` |
| Minimum run | Contiguous days covering at least one Learning→Learning bridge and one Revision day when inventory allows |
| Pass (Founder Validation educational value) | DEV-02 ≥ 7.5 **and** DEV-03 ≥ 80% **and** HT-01 = 0 **and** LT-01 ≥ 8 **and** LT-06 prefers Kwalitec |
| Claims allowed | “Founder Validation supports educational value of walked days” |
| Claims forbidden | Private Beta proof; exam readiness; DSH/CE as value |

### 8.2 Private Beta Stage 1 (future)

| Element | Rule |
|---------|------|
| Cohort | Serious professional-exam candidates (CS1 first) |
| Material | Student-reachable `approved` + `released` days only |
| Instrument | Same D1–D7 + SS/LT/HT; lightweight daily form |
| Window | Multi-week; report weekly DEV + return |
| Pass (Stage 1 student-success) | DEV-02 cohort median ≥ 7.0 **and** DEV-03 ≥ 70% **and** LT-01 median ≥ 7 **and** HT-01 rate near 0 **and** LT-06 majority prefer Kwalitec |
| Claims allowed | “Private Beta Stage 1 met student-success thresholds on released horizon” |
| Claims forbidden | Exam pass-rate proof; full CS1 companion; editorial coverage as student success |

### 8.3 Private Beta Stage 2+ (reserved)

Longer horizons, comparative study (Kwalitec+CMP vs CMP-alone weeks), and linkage toward Vision north-star measurement. **Out of scope for SV-001 definition** — thresholds to be set when Stage 1 passes and DSH supports longer runs.

---

## 9. Minimum evidence package

A student-value claim (Founder or Beta) must cite:

1. DEV day table (D1–D7 per day)  
2. DEV-01…DEV-05 summary  
3. SS corroboration (at least SS-01, SS-06, SS-07)  
4. LT-01, LT-05, LT-06  
5. HT-01…HT-05 outcomes  
6. Explicit **non-claim** list (what editorial metrics showed but were not used as value proof)  
7. Scope label: inventory Validation vs student-reachable released path  

Missing any of (1)–(6) ⇒ claim stays **provisional / incomplete**.

---

## 10. Dashboard field set (Founder)

### 10.1 Student value (primary)

| Field | Source |
|-------|--------|
| DEV run score | DEV-02 |
| Return-worthy rate | DEV-03 |
| Trust floor | DEV-04 |
| D1…D7 means | DEV-05 |
| Willingness-to-continue | LT-01 |
| False-confidence incidents | HT-01 |
| Prefer Kwalitec vs CMP alone | LT-06 |
| Next-day return rate | SS-07 |

### 10.2 Internal editorial (secondary, labelled)

| Field | Source |
|-------|--------|
| Opening DSH | ED-01 |
| CIH (planning only) | ED-02 |
| Published LO coverage | ED-03 |
| Continuity Front | ED-07 |
| DX index (last audit) | ED-06 |

No application UI is required by SV-001; this is the measurement contract for a future console.

---

## 11. Relationship to prior programmes

| Programme | Supplies | Does not supply |
|-----------|----------|-----------------|
| EA / EP / EO | Lawful, certified days | Lived student value |
| DX-001 | Delivery quality expectation | Lived DEV under fatigue |
| CE-001 | Coverage map | Day worth |
| DSH-001 | Dependable length | Day worth |
| P-001.1 KSI | Composite usefulness | Daily DEV instrument |
| **SV-001** | **DEV + Student Success Metrics** | Content, Runtime, ops redesign |

---

## 12. Anti-patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Reporting Approver signatures as student success | Seals enable days; they do not improve evenings |
| Equating DSH growth with happier study | Longer path ≠ better days |
| Using DX 8.8 as lived DEV | Editorial ≠ lived |
| Optimising streak / minutes | Vanity |
| High D6 with HT fail | Fake motivation |
| Beta claims on unreleased inventory | Reachability honesty |

---

**End of Student Success Metrics**

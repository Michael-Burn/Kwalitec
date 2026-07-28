# RR-001 — Alpha Remediation Register

**Programme:** RR-001 — Alpha Readiness Remediation Register  
**Work Packages:** RR-001.1 — Critical Findings Resolution · RR-001.2 — Premium Experience Remediation · **RR-001.3A — Educational Identity & Narrator Consistency**  
**Date:** 2026-07-28 (updated RR-001.3A)  
**Sources:** RP-001.1 Product Inventory · RP-001.2 End-to-End Journey · RP-001.3 Study Sensei Identity & Voice · **RP-001.4 Premium Experience Certification**  
**Status legend:** `Resolved` · `Open` · `Deferred` · `Contained` (process / flag / ops mitigation) · `Merged` (see canonical ID)

---

## Purpose

Single remediation register for every certification finding from RP-001.1–RP-001.3. Overlapping findings are deduplicated to a **canonical ID**. Severity reflects Alpha readiness impact after certification review (RR-001.1 elevates journey continuity defects that block honest Alpha claims).

---

## Severity scale

| Level | Meaning |
|-------|---------|
| Critical | Breaks trust, journey continuity, or honest Alpha claims on the default path — must be closed before RP-001.4 |
| High | Likely trust damage or false claim if unmanaged |
| Medium | Manageable with disclosure / later package |
| Low | Residual; monitor |

---

## Duplicate merges

| Canonical ID | Merged aliases | Rationale |
|--------------|----------------|-----------|
| **RR-C02** | JR-06, JR-PREVIEW, IR-03, SS-10 Fail | Same false Home reflection affordances |
| **RR-C03** | JR-07, JR-REV-01, DP-37, T-64 | Same unreachable revision acknowledgement under sole runtime |
| **RR-H01** | R-01, JR-17 | Same sole-runtime competing-homes integrity risk |
| **RR-H02** | R-02, JR-02, IR-09 | Dual chrome / dual OS atmosphere |
| **RR-H03** | R-03, JR-03, JR-18 (partial), IR-14 (partial) | Flag-scope honesty (QC / UJ / Runtime C claims) |
| **RR-H04** | R-04, JR-04, IR-10 | Empty Home / weak “what next?” |
| **RR-H05** | R-05, JR-05, IR-15 | MES + Mission Intelligence duplication |
| **RR-H06** | R-07, JR-20, IR-12 | Profile notifications without push product |
| **RR-H07** | R-09, JR-21 | ILE-005 migration required for reflection |
| **RR-H08** | R-16, JR-16, IR-16 | Cohort validation not executed |
| **RR-H09** | R-18, JR-12 | Defer does not change ranking |
| **RR-H10** | R-06, JR-13 | Thin Revision without adaptive authority |
| **RR-M01** | R-12, JR-08, IR-04 | Multiple reflection systems without student map |

---

## Critical findings (RR-001.1 mandatory)

| Canonical | Source IDs | Title | Severity | Status | Fix / evidence |
|-----------|------------|-------|----------|--------|----------------|
| **RR-C01** | JR-01, T-47, DP-22 | V2 session finish must complete Mission commitment lifecycle | Critical | **Resolved** | `app/presentation/session/views.py` `complete_and_return` → `RecommendationCommitmentService.mark_completed`; tests `test_commitment_completion_link.py` |
| **RR-C02** | JR-06, IR-03, SS-10 | Remove false interactive reflection controls on Home | Critical | **Resolved** | Removed “Done reflecting” / “Skip for today”; honest preview-only disclaimer; `test_rr001_1_critical_remediation.py` |
| **RR-C03** | JR-07, JR-REV-01 | Restore revision acknowledgement on sole-runtime journey | Critical | **Resolved** | EOS Home surfaces lifecycle ack + existing `dashboard.acknowledge_revision` POST; intentional reuse of V1SP-001A lifecycle service (no new educational capability) |
| **RR-C04** | R-01, JR-17 | Sole-runtime misconfiguration reintroduces competing homes | Critical | **Contained** | Operational: protect `KWALITEC_V2_SOLE_RUNTIME`; no product defect to code-fix in RR-001.1 |
| **RR-C05** | R-25 | Public registration accidentally exposed | Critical | **Contained** | Auth remains login/logout only; do not add public register |

**RR-001.1 gate:** No Critical *product defects* remain open. Operational Criticals (RR-C04, RR-C05) stay Contained under release ops discipline.

---

## High findings

| Canonical | Source IDs | Title | Status | Notes |
|-----------|------------|-------|--------|-------|
| RR-H01 | R-01 / JR-17 | Sole-runtime integrity | Contained | Same as RR-C04 |
| RR-H02 | R-02 / JR-02 / IR-09 / **XR-01** | Dual chrome | **Resolved** (RR-001.2) | EOS primitives on Help/Onboarding/Settings/Wizard + workspace CSS bridge; residual utility classes remain Low polish |
| RR-H03 | R-03 / JR-03 / JR-18 | Flag-scope honesty | Contained | QC / UJ / Runtime C remain OFF; inventory excludes |
| RR-H04 | R-04 / JR-04 / IR-10 / **XR-04** | Empty Home without recommendation | **Resolved** (presentation) / Contained (ops) | RR-001.2 honest empty + CTA; provisioning/briefing still ops |
| RR-H05 | R-05 / JR-05 / IR-15 / **XR-02** | MES + MI duplication / Home density | **Resolved** (RR-001.2) | MI disclosed; secondary subordinate; tertiary behind disclosure — MI content unchanged |
| RR-H06 | R-07 / JR-20 / IR-12 | Notifications copy honesty | Open | UI honesty package later |
| RR-H07 | R-09 / JR-21 | ILE-005 migration discipline | Contained | Release checklist |
| RR-H08 | R-16 / JR-16 / IR-16 | Cohort validation not run | Open | Execute Internal Alpha validation pack |
| RR-H09 | R-18 / JR-12 | Defer ≠ ranking change | Contained | Disclose preference-only (by design) |
| RR-H10 | R-06 / JR-13 | Thin Revision surface | Contained | Adaptive authority OFF disclosed |
| RR-H11 | IR-01 | Dual narrator (Kwalitec vs Study Sensei) | **Resolved** (RR-001.3A in-scope) | Handoff T04 + Home/Session Sensei naming; Help lag remains EGC-R03 |
| RR-H12 | IR-02 | Mission / Session / tip synonym storm | **Resolved** (RR-001.3A in-scope) | Lexicon on educational identity surfaces; Journal tip empty → EGC-R12 |
| RR-H13 | R-14 | Runtime C dual educational context | Contained | Flags OFF |
| RR-H14 | R-20 | Curriculum V1/V2 breakage via unrelated change | Contained | Architecture invariant + CI |

---

## Medium findings

| Canonical | Source IDs | Title | Status |
|-----------|------------|-------|--------|
| RR-M01 | R-12 / JR-08 / IR-04 | Multiple reflection systems without map | Open |
| RR-M02 | JR-09 | Welcome CTA lands on Home under sole runtime | Deferred |
| RR-M03 | JR-10 | Onboarding skip under-orients | Deferred |
| RR-M04 | JR-11 / R-10 | Calibration / Twin soft-fail → Tutor soft-fail | Contained |
| RR-M05 | JR-14 | History ≠ legacy analytics charts | Deferred |
| RR-M06 | JR-15 / R-15 / **XR-11** | Dual-chrome a11y weaker than EOS | **Resolved** (RR-001.2) | Labels, focus-visible, wizard progress label; no WCAG claim |
| RR-M07 | JR-19 / R-19 | Sparse Journal / Timeline / History early | Deferred |
| RR-M08 | JR-22 / R-23 | Session durable-store / orphaning | Contained |
| RR-M09 | JR-23 / IR-01 partial | Sensei voice inconsistent on chrome | Open |
| RR-M10 | JR-24 / R-11 | Orphan `/assessment` vs QC story | Deferred |
| RR-M11 | JR-25 / R-08 | Export omits Decision Journal | Deferred |
| RR-M12 | IR-05 | “Why the system chose this” | **Resolved** (RR-001.3A rename) | Runtime C summary → “Why this Mission?”; flag still Contained OFF |
| RR-M13 | IR-06 | Onboarding never names Study Sensei | **Resolved** (RR-001.3A) | Meet Study Sensei step + Board handoff |
| RR-M14 | IR-07 | Help FAQ lags ILE memory surfaces | Open | EGC-R03 |
| RR-M15 | IR-08 | Explanation “tip” understates guidance | **Resolved** (RR-001.3A) | “Why this guidance?” |
| RR-M16 | IR-11 | Exam/test-adjacent Help phrasing | Open |
| RR-M17 | R-13 | Accidental UJ / Experience Feedback enable | Contained |
| RR-M18 | R-17 | EI internal alpha misread as full EI widgets | Contained |
| RR-M19 | R-24 | Forbidden engineering terms leak | Contained (tests) |
| RR-M20 | CAP-02/16/19/25 conditions / **XR-05** | Dual chrome capability / mobile nav wrap | **Resolved** (nav) / Contained (caps) | Compact mobile nav (RR-001.2); remaining CAP conditions disclosed |
| RR-M21 | CAP-06/13/14/15/18/21/23 | Conditional capabilities from inventory | Contained / disclosed |

---

## Low findings

| Canonical | Source IDs | Title | Status |
|-----------|------------|-------|--------|
| RR-L01 | IR-13 | Streak language in legacy/settings export | Contained |
| RR-L02 | IR-14 | Journal empty mentions QC while OFF | Open |
| RR-L03 | IR-17 | Assessment flash brands Kwalitec | Deferred |
| RR-L04 | IR-18 | “Optimising for {axis}” engineering tone | **Resolved** (RR-001.3A) | Home MI chrome → “Focusing on …” |
| RR-L05 | IR-19 | Default benefit “strengthen your exam readiness” | Open |
| RR-L06 | IR-20 | Unified Journey nav lexicon if enabled | Contained (OFF) |
| RR-L07 | R-21 | Deep/Recovery/Confidence check flags | Contained |
| RR-L08 | R-22 | Telemetry without closed student loop | Deferred |

---

## Inventory capability status (RP-001.1)

Capability readiness calls from RP-001.1 are unchanged by RR-001.1 except where Critical journey defects affected CAP-11 (commitment completion) and CAP-22 (welcome / revision ack):

| CAP | Remediation note |
|-----|------------------|
| CAP-11 Mission Commitment | Completion arc **Resolved** on V2 session finish (RR-C01) |
| CAP-22 Welcome / Revision Ack | Revision ack **Resolved** on EOS Home (RR-C03); welcome unchanged |
| CAP-03 Student Home | False reflection preview controls **Resolved** (RR-C02) |
| CAP-10 Feedback Loop | Still requires migration Contained (RR-H07) |
| CAP-27–31 | Remain Not Ready / excluded — Contained |

---

## Identity surface status (RP-001.3)

| Surface | Prior | After RR-001.1 |
|---------|-------|----------------|
| SS-10 Guided reflection preview | **Fail** | Trust Fail remediated (controls removed); identity Conditional residuals remain elsewhere |
| SS-11 Commitment reflection ack | Pass (availability Conditional) | Availability strengthened via RR-C01 |
| SS-29 Welcome / revision ack | Conditional Pass | Revision ack path Restored on EOS |
| Other SS-xx | Unchanged | Tracked via IR Open/Deferred rows above |

---

## Experience findings (RP-001.4 → RR-001.2)

| XR ID | Title | Severity | Status | Package |
|-------|-------|----------|--------|---------|
| XR-01 | Dual design languages | High | **Resolved** | RR-001.2 |
| XR-02 | Home cognitive overload | High | **Resolved** | RR-001.2 |
| XR-04 | Empty / sparse early states | High | **Resolved** (presentation) | RR-001.2 |
| XR-05 | Mobile nav wrap | Medium→High for Alpha polish | **Resolved** | RR-001.2 |
| XR-11 | A11y residual on V1 pages | Medium | **Resolved** (presentation) | RR-001.2 |
| XR-17 | Success / empty state fragmentation | Medium | **Resolved** | RR-001.2 |
| XR-14 | Flag enablement without density redesign | High if enabled | **Contained** | Keep OFF |
| XR-20 | Cohort UX validation not executed | High | **Open** | Internal Alpha pack |

---

## Document control

- Implementation packages: RR-001.1 · RR-001.2 · **RR-001.3A**  
- Companion matrix: `CRITICAL_FINDINGS_MATRIX.md`  
- Completions: `RR001_1_COMPLETION_REPORT.md` · `RR001_2_COMPLETION_REPORT.md` · `RR001_3A_COMPLETION_REPORT.md` · `RR001_3A_IMPLEMENTATION_REPORT.md`  
- Do not treat this register as Version 1 production-ready declaration

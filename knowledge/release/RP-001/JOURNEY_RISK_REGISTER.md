# RP-001.2 — Journey Risk Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.2  
**Date:** 2026-07-28  
**Scope:** Risks specific to end-to-end student journey coherence, transitions, and trust  
**Relation to RP-001.1:** Extends `RISK_REGISTER.md` (R-xx). Journey risks use **JR-xx**. Cross-references retained where inventory risks reappear as journey failures.

---

## Severity scale

| Level | Meaning |
|-------|---------|
| Critical | Breaks “what next?” or creates educational contradiction on the default path |
| High | Likely trust damage or false journey claim if unmanaged |
| Medium | Manageable with disclosure / briefing / later fix |
| Low | Residual; monitor |

---

## Journey risk register

| ID | Risk | Category | Severity | Related stages / transitions | Evidence | Residual mitigation (process only — no code in RP-001.2) |
|----|------|----------|----------|------------------------------|----------|----------------------------------------------------------|
| JR-01 | V2 session finish does not call `RecommendationCommitmentService.mark_completed()` — Home completion reflection / journal completion arc may not appear on canonical path | Educational / Trust / Experience | **High** | ST-07, ST-09; T-47; DP-22, DP-28 | `mark_completed` only in `app/mission/routes.py`; no call in `app/presentation/session/` | Disclose to Alpha cohort; track fix in later package; do not claim full commitment arc on V2 finish until wired |
| JR-02 | Dual chrome (EOS vs V1 wizard/onboarding/settings/help) breaks journey visual continuity | Trust / Experience | High | ST-02, ST-03; R-02 | DEP-002; alpha/study_plan/settings templates | Accept Stage 1 condition; brief testers |
| JR-03 | Claiming Quick Check / framing as Alpha journey while flags OFF | Educational / Trust / Operational | High | ST-08; T-51; R-03 | Adaptive flags unset in `render.yaml` | Inventory + this cert exclude QC; any enablement = delta cert |
| JR-04 | Empty Home without authorised recommendation — weak “what next?” | Educational / Trust | High | ST-05; T-30; R-04 | Home empty states | Provision Alpha accounts through plan+calibration; smoke recommendation path |
| JR-05 | MES L1 + Daily Mission Intelligence feel like duplicate Sensei voices | Trust / Educational | Medium | ST-05, ST-06; R-05 | `home.html` both panels | Watch cohort feedback; accept for Alpha |
| JR-PREVIEW / JR-06 | Non-interactive “Done reflecting” / “Skip for today” spans look like decisions | Trust / Experience / Accessibility | **High** | ST-10; T-59; DP-38 | `home.html` reflection preview spans + “nothing is saved yet” | Brief testers; treat as false affordance; fix in later UX honesty package |
| JR-REV-01 / JR-07 | Syllabus-complete revision acknowledgement UI only on legacy dashboard — unreachable under sole runtime | Educational / Trust | **High** | ST-14; T-64; DP-37 | Ack UI in `dashboard/index.html` only; `/dashboard/` redirects to EOS | Disclose; lifecycle still computes flag but student never acknowledges on EOS |
| JR-08 | Multiple reflection systems (session, commitment, ILE-005, research check-in, preview) without student map | Educational / Trust | Medium | ST-10; R-12 | Distinct routes/programmes | Tester briefing; do not conflate in Alpha scripts |
| JR-09 | Welcome CTA “Start Today's Session” returns to Home under sole runtime | Experience | Medium | ST-05; T-29; DP-18 | `canonical_session_entry_url` → home | One extra click; disclose |
| JR-10 | Onboarding skip leaves students under-oriented for Sensei concepts | Educational | Medium | ST-02; DP-04 | Skip POST allowed | Prefer complete in Alpha scripts |
| JR-11 | Calibration abandon / Twin persist soft-fail → later Tutor soft-fail | Educational / Trust | Medium | ST-04; DP-15–16; R-10 | Calibration routes + Twin dependency | Prefer complete calibration; do not market full Tutor |
| JR-12 | Deferral expected to change tomorrow’s ranking but does not | Educational / Trust | Medium | ST-07; DP-20; R-18 | EP-008.3 design | Disclose preference-only |
| JR-13 | Thin / empty Revision surface with adaptive authority OFF | Educational / Trust | Medium | ST-05 nav; R-06 | Adaptive authority unset | Do not claim adaptive revision quality |
| JR-14 | History via `/analytics/` redirect without charts — expectation mismatch | Trust / Experience | Medium | ST-13; T-36 | Sole-runtime redirect | Brief: History ≠ legacy analytics |
| JR-15 | Dual-chrome pages weaker keyboard/screen-reader coverage than EOS Home | Accessibility | Medium | ST-02, ST-03; R-15 | CAP-25 | No WCAG claim; EOS is stronger path |
| JR-16 | Internal Alpha cohort validation not executed — journey cert is code-audit only | Operational / Trust | High | Cross-journey; R-16 | `INTERNAL_ALPHA_RELEASE_VALIDATION.md` | Execute validation pack before declaring student-proven |
| JR-17 | Sole-runtime misconfiguration reintroduces competing homes mid-journey | Educational / Trust / Operational | Critical | Cross; R-01 | `KWALITEC_V2_SOLE_RUNTIME` | Protect Render env; operational tests |
| JR-18 | Accidental enable of Unified Journey / Experience Feedback / Runtime C mid-Alpha | Trust / Operational / Educational | High | Conditional journeys; R-13, R-14 | Flags default OFF | Keep OFF; treat as scope change |
| JR-19 | Sparse Journal / Timeline / History early looks broken | Trust | Medium | ST-11–13; R-19 | Empty states by design | Empty-state copy + briefing |
| JR-20 | Profile implies notifications; return-next-day has no push | Trust / Operational | Medium | ST-14; R-07, R-31 | No NotificationProvider | Disclose: student-initiated return only |
| JR-21 | ILE-005 migration missing → journal reflection fails in env | Technical / Operational | High | ST-10–11; R-09 | Migration `202607280002` | Migrate before Alpha reflection use |
| JR-22 | Session durable-store / orphaning breaks resume “what next?” | Technical / Experience | Medium | ST-09; R-23 | Durable ON in prod | Ops monitoring; resume smoke |
| JR-23 | Sensei voice inconsistent (strong on Home MI; weak on wizard/auth; invisible internal review) | Educational / Trust | Medium | Cross-journey Sensei review | Templates + ILE-005 internal review | Accept for Alpha; track voice pass later |
| JR-24 | Orphan `/assessment` vs future Quick Check confuses assessment story | Educational / Trust | Medium | ST-08; R-11 | Not in nav | Do not market `/assessment` as Alpha primary |
| JR-25 | Export/backup omits Decision Journal evidence | Operational / Trust | Medium | ST-11; R-08 | ILE-002 limitation | Disclose export incompleteness |

---

## Highest journey risks (board view)

1. **JR-01** — Commitment completion unwired on V2 session finish (breaks post-session educational arc).  
2. **JR-07 / JR-REV-01** — Revision acknowledgement unreachable under sole runtime.  
3. **JR-06** — False reflection affordances on Home.  
4. **JR-04** — Empty Home “what next?” hole.  
5. **JR-17** — Sole-runtime integrity (two homes).  
6. **JR-03 / JR-18** — Flag-scope honesty (QC / UJ / Runtime C).  
7. **JR-16** — Cohort validation not yet run.

---

## Category summary

| Category | Critical | High | Medium | Low |
|----------|---------:|-----:|-------:|----:|
| Educational | 1 | 4 | 5 | 0 |
| Trust | 1 | 6 | 6 | 0 |
| Experience | 0 | 2 | 3 | 0 |
| Technical | 0 | 1 | 1 | 0 |
| Operational | 1 | 3 | 2 | 0 |
| Accessibility | 0 | 1 | 1 | 0 |

(Counts overlap across categories.)

---

## Failed / conditional transition risks mapped

| Transition / DP | Cert | Primary JR |
|-----------------|------|------------|
| T-47 V2 finish without `mark_completed` | Fail (continuity) | JR-01 |
| T-59 Fake reflection controls | Fail (affordance) | JR-06 |
| T-64 Revision ack unreachable | Fail | JR-07 |
| T-30 Empty Home | Conditional | JR-04 |
| T-29 Welcome CTA | Conditional | JR-09 |
| DP-22 Reflection ack often missing | Gap | JR-01 |
| DP-37 Revision ack | Fail | JR-07 |
| DP-38 Preview spans | Fail | JR-06 |

---

## Explicit non-risks for this package

- Implementing commitment wiring or revision-ack on EOS (out of scope — identified only).  
- Activating Quick Check to “complete” the journey diagram.  
- KSI / Twin / Recommendation Engine behaviour changes.  
- Speculating Version 1 production-ready declaration.

---

## Document control

Process mitigations only. No application code changed in RP-001.2.

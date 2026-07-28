# RP-001.1 — Risk Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.1  
**Date:** 2026-07-28  
**Scope:** Student-facing Alpha candidate risks only (inventory evidence; no new mitigations implemented)

---

## Severity scale

| Level | Meaning |
|-------|---------|
| Critical | Blocks honest Alpha or creates educational contradiction |
| High | Likely to damage trust or invalidate Alpha claims if unmanaged |
| Medium | Manageable with disclosure / process |
| Low | Residual; monitor |

---

## Risk register

| ID | Risk | Category | Severity | Related CAP | Evidence | Residual mitigation (process only) |
|----|------|----------|----------|-------------|----------|-------------------------------------|
| R-01 | Sole-runtime misconfiguration re-exposes legacy Dashboard/Missions/Analytics as competing homes | Educational / Trust / Operational | Critical | CAP-30, CAP-03, CAP-26 | DEP-002; `redirect_if_sole_runtime`; Render relies on `KWALITEC_V2_SOLE_RUNTIME=1` | Protect Render env; operational sole-runtime tests; rollback playbook only |
| R-02 | Dual chrome (EOS nav + V1 Study Plan / Settings / Alpha / Research shells) feels like two products | Trust / Educational | High | CAP-02, 16, 19–21, 24 | DEP-002 FEATURE_FLAG_AUDIT | Disclose as accepted Alpha Stage 1 condition |
| R-03 | Claiming Quick Check / Contextual Framing in Alpha while flags OFF | Educational / Trust / Operational | High | CAP-13, 14, 26 | Adaptive flags default OFF; not in Render | Inventory excludes activation; any enablement must update register |
| R-04 | Empty Home when no authorised recommendation | Educational / Trust | High | CAP-03, 04, 11 | ILE-004 empty-state limitation | Tester briefing; ensure plan/calibration/recommendation path works for Alpha accounts |
| R-05 | MES L1 + Daily Mission Intelligence duplication feels verbose / inconsistent | Trust / Educational | Medium | CAP-04 | ILE-004 completion known limitation | Accept for Alpha; watch Internal Alpha feedback |
| R-06 | Revision surface empty/degraded without adaptive authority | Educational | Medium | CAP-06 | Adaptive authority default OFF | Disclose; do not claim adaptive revision quality |
| R-07 | Profile “notifications enabled” implies push that does not exist | Trust | Medium | CAP-18, 31 | Profile read-only defaults; unwired NotificationProvider | Disclose: no notification product in Alpha |
| R-08 | Decision Journal evidence not in JSON backup | Operational / Trust | Medium | CAP-08, 19 | ILE-002 limitation | Disclose export incompleteness for journal evidence |
| R-09 | ILE-005 migration not applied → reflection/reviews fail | Technical / Operational | High | CAP-10 | Migration `202607280002` | Release checklist: migrate before Alpha use of reflection |
| R-10 | Tutor explain unavailable without Twin | Educational / Trust | Medium | CAP-23, 17 | Soft-fail; Twin cutover flags OFF | Soft-fail OK; do not market full Tutor |
| R-11 | Two assessment paths (Quick Check vs `/assessment`) confuse students | Educational / Trust | Medium | CAP-13, 15 | Orphan `/assessment` nav | Alpha narrative: Session activity primary; `/assessment` not marketed |
| R-12 | Research check-in confused with ILE-005 educational reflection | Educational | Low | CAP-21, 10 | Distinct programmes | Tester briefing |
| R-13 | Unified Journey / Experience Feedback accidentally enabled mid-Alpha | Trust / Operational | Medium | CAP-27, 28, 26 | Flags default OFF | Keep OFF; treat enablement as scope change |
| R-14 | Runtime C partially enabled → dual educational context | Educational / Trust | High | CAP-29 | Flags OFF; fail-open design | Keep OFF for general Alpha |
| R-15 | Accessibility gaps on V1 dual-chrome pages; no WCAG claim | Accessibility | Medium | CAP-25 | EOS a11y tests stronger than V1 shells | No WCAG conformance claim; track dual-chrome residual |
| R-16 | Internal Alpha cohort validation not executed | Operational / Trust | High | Cross-cutting | `INTERNAL_ALPHA_RELEASE_VALIDATION.md` §6 template only | RP-001 later packages / execute validation pack |
| R-17 | EI internal alpha misread as full EI student widgets | Trust / Operational | Medium | CAP-26 | Missions/explainability/progress always OFF | Document in flag register |
| R-18 | Commitment defer does not change ranking — expectation mismatch | Educational / Trust | Medium | CAP-11 | EP-008.3 design | Disclose: preference only |
| R-19 | Sparse Journey/History/Timeline early in Alpha looks “broken” | Trust | Medium | CAP-05, 07, 09, 32 | Empty states by design | Empty-state copy + tester briefing |
| R-20 | Curriculum V1/V2 breakage via unrelated change | Educational / Technical | High | CAP-16, 05 | Architecture invariant | Preserve in all later RP work; CI curriculum checks |
| R-21 | Deep/Recovery/Confidence/Readiness check flags imply unfinished products | Trust / Operational | Low | CAP-13 | Flags without routes | Do not enable; do not list as Alpha features |
| R-22 | Telemetry / feedback without closed loop to students | Trust | Low | CAP-20 | Alpha feedback service | Ops triage process |
| R-23 | Session orphaning / durable store failure | Technical / Operational | Medium | CAP-12 | Durable ON in prod | Health/ops monitoring; smoke resume tests |
| R-24 | Forbidden engineering terms leak to learners | Trust / Educational | Medium | CAP-25 | Terminology guards + tests | Keep terminology tests green |
| R-25 | Public registration accidentally exposed | Security / Operational | Critical | CAP-01 | Auth has login/logout only | Do not add public register in Alpha |

---

## Highest risks (Alpha decision board)

1. **R-01** — Sole-runtime integrity (two homes).  
2. **R-03** — Scope honesty for Quick Check / flag-gated ILE-001.  
3. **R-16** — Cohort validation not yet executed.  
4. **R-04** — Empty Home recommendation path.  
5. **R-02** — Dual chrome trust hit.  
6. **R-09** — ILE-005 migration discipline.

---

## Risk categories summary

| Category | Critical | High | Medium | Low |
|----------|---------:|-----:|-------:|----:|
| Educational | 1 | 3 | 5 | 1 |
| Trust | 1 | 4 | 7 | 2 |
| Technical | 0 | 2 | 2 | 0 |
| Operational | 1 | 3 | 2 | 1 |
| Accessibility | 0 | 0 | 1 | 0 |

(Counts overlap — one risk may span categories; table above is illustrative of concentration, not unique IDs.)

---

## Explicit non-risks (out of scope speculation)

- Future ILE-006 Study Intelligence behaviour  
- Multi-profession catalogue expansion  
- LLM recommendation authority (not present in core path)  
- Push notification delivery quality (product absent)

---

## Related

- Inventory: `ALPHA_PRODUCT_INVENTORY.md`  
- Flags: `FEATURE_FLAG_REGISTER.md`  
- Completion: `RP001_1_COMPLETION_REPORT.md`

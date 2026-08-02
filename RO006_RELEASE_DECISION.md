# RO-006 — Release Decision

**Programme:** RO-006 — Wave 6 LIVE Release Operations  
**Volume:** CS1-008 · Campaign Theta · `cs1008-1.0.0`  
**Date:** 2026-08-02  
**Authority:** EP-001 Publication APPROVED (HR-006) · EF-001 · CE-001 coverage law  

---

## Decision

```text
RO-006 Wave 6 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CT-D1…CT-R1): PASS (package path)
Natural Continuity Front chain (continue_topic @ 2 → CB…CG…CE…CZ…CH → CT-D1…CT-R1): PASS (true Theta substance after CH-R1 session finish / continuation)
Progressive confidence (PB-008): PASS (Theta LIVE-certified only)
Ops label desync / Finish-Home tomorrow chrome: RESIDUAL RO6-R1…R3 — tracked
Student LIVE credit for Theta packages: AUTHORISED (package path)
Coverage register: 38 / 72 Learning Objectives (52.8%)
Continuity Front: advanced through Topic 2.5
Wave 7: UNBLOCKED for programme start — NOT STARTED in this decision
```

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `a931f23628ba145b1bebbb190c53f2c555590110` live · deploy `dep-d9nclt2jnfac73aqle0g` |
| LIVE verification confirms approved educational experience | **Met for package path** — Guided Reading, CMP, activities, reflection, revision progression, no fallback on true Theta path (`RO006_LIVE_VERIFICATION_REPORT.md`) |
| Progressive confidence passes for Theta | **Met** — `PB008_PROGRESSIVE_CONFIDENCE_REPORT.md` · 2×3 days · stable HIGH |
| No educational regressions introduced | **Met** for inventory + Eta/Zeta/Epsilon/Gamma/Delta session substance; residuals RO6-R1…R3 tracked (do not fail package-path LIVE-complete) |
| Publication status updated | **Met** — dashboard + coverage map + decision log |

**Campaign Theta is LIVE-complete.** Wave 7 may begin under a separate authorised programme; this decision does **not** start Wave 7.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **2** completes remaining Beta/Gamma/Epsilon/Zeta/Eta days and then receives the **approved CS1-008 Theta packages** for LOs **2.5.1–2.5.2** plus **CT-R1** Revision — jointly activated, not as Isolated Golden Days. Cold entry at syllabus topic **2.5** also resolves to **CT-D1**.

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, PB-008 PASS, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 6 LIVE Verified; Wave 7 gated only by separate start authorisation (LIVE-complete exit met).  
3. `EP001_COVERAGE_MAP.md` / `EP006_COVERAGE_UPDATE.md` — Approver+LIVE credit for 2.5; Continuity Front advanced through 2.5.2 → **38 / 72 (52.8%)**.  
4. Certified Educational Coverage Register + Student Reliance Coverage advanced through Topic **2.5**.

---

## Explicit non-claims

- Wave 7 **not started** by this decision (only unblocked).  
- Until-exam educational trust **not** claimed from Wave 6 alone.  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Chapter 2 / spine complete **not** claimed.  
- Finish/Home tomorrow chrome **not** certified as matching package text on CT-R1.  
- RO6-R1 Home / label desync **not** cleared.

---

## Residual register (ops follow-up — not Wave 7 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks Wave 7 start? |
|----|----------|-------------|------------------------|----------------------|
| RO6-R1 | Ops label desync during Continuity Front multi-day walks | PI / selection presentation | **No** | **No** |
| RO6-R2 | Revision-day checklist Q6 Learning-oriented audit on CT-R1 | Presentation / audit rubric | **No** | **No** |
| RO6-R3 | Tomorrow chrome residual on CT-R1 | PI / chrome | **No** | **No** |

---

## References

- `RO006_DEPLOYMENT_REPORT.md`  
- `RO006_LIVE_VERIFICATION_REPORT.md`  
- `PB008_PROGRESSIVE_CONFIDENCE_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO006/` · `knowledge/evidence/releases/PB008/`  
- Commit: `a931f23628ba145b1bebbb190c53f2c555590110`  
- Deploy: `dep-d9nclt2jnfac73aqle0g`  
- Inventory assert: `job-d9ncn8rncjis739tini0`  

---

## Completion report sections

### Summary

RO-006 jointly activated Campaign Theta on LIVE, verified educational fidelity on the Continuity Front package path (CH-R1 → CT-D1…CT-R1), and obtained progressive confidence PASS for CT-D1…CT-R1. Exit criteria for LIVE-complete are met with tracked residuals. Coverage advances to **38 / 72 (52.8%)**. Continuity Front advances through Topic **2.5**. Wave 7 remains not started.

### Files Created

- `RO006_DEPLOYMENT_REPORT.md`
- `RO006_LIVE_VERIFICATION_REPORT.md`
- `PB008_PROGRESSIVE_CONFIDENCE_REPORT.md`
- `RO006_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO006/**`
- `knowledge/evidence/releases/PB008/**`

### Files Modified

- Live package copies + campaign status + selection day-order (activation commit `a931f236…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP006_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 125 passed
```

LIVE inventory assert · LIVE verification · PB-008 progressive confidence.

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order extension only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic unmodified beyond ops continuity wiring class already used in RO-001…RO-005.

### Technical Debt

RO6-R1 label desync and CT-R1 tomorrow chrome / Q6 residual remain open PI follow-ups outside Wave 7 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive (not until-exam) confidence; two-persona PB-008 cohort; Baseline section picker (not leaf 2.5) for Continuity Front entry.

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 2.4.2 / CH-R1 before Wave 6 LIVE.  
- **Student benefit:** Diligent students can study approved Theta days with CMP partnership on LIVE after Eta.  
- **Learning benefit:** Central limit theorem entry (2.5.1–2.5.2) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · PB-008 PASS · 0 fallback on true Theta path · coverage **38 / 72**.  
- **Risks:** Over-claiming until-exam trust; label desync RO6-R1; chrome residual at CT-R1.  
- **Assumptions:** Continuity Front entry via continue at section 2; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO006/` · `knowledge/evidence/releases/PB008/` · deploy `dep-d9nclt2jnfac73aqle0g` · assert job `job-d9ncn8rncjis739tini0`.

### Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CH-R1 → CT-D1 selection is explicit after Eta session completion. Ops label desync can mislabel expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 7 geography still unpublished. RO6-R1 open (PI).

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-006 · 2026-08-02  
**Wave 6 LIVE status:** LIVE-complete (package path) · Residuals RO6-R1 / RO6-R2 / RO6-R3 open · **Wave 7 unblocked · not started**

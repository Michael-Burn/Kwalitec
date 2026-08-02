# RO-010 — Release Decision

**Programme:** RO-010 — Wave 10 LIVE Release Operations  
**Volume:** CS1-012 · Campaign Mu · `cs1012-1.0.0`  
**Date:** 2026-08-02  
**Authority:** EP-001 Publication APPROVED (HR-010) · EF-001 · CE-001 coverage law  

---

## Decision

```text
RO-010 Wave 10 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CM-D1…CM-R1): PASS (package path)
Natural Continuity Front into Topic 3.3 (continue_topic @ 3 → CK…CL-R1 → CM-D1…CM-R1; CL-R1 → CM-D1 selection): PASS
Progressive confidence (PB-012): AUTHORISED — NOT EXECUTED in this decision
Ops label desync / Finish-Home tomorrow chrome: RESIDUAL RO10-R1…R3 — tracked
Student LIVE credit for Mu packages: AUTHORISED (package path)
Coverage register: 63 / 72 Learning Objectives (87.5%)
Continuity Front: advanced through Topic 3.3
Wave 11: NOT STARTED
PB-012 Progressive Confidence: AUTHORISED
```

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `c409ad29871d7845f8d9d832776168142d40fad7` live · deploy `dep-d9nmclp42hec73fueteg` |
| Fingerprint matches | **Met** — `/health` + `/health/live` commit fields |
| Package inventory correct | **Met** — 83 approved · 6 Mu · no duplicate/missing IDs |
| Package-path fidelity holds | **Met** — Guided Reading, CMP, activities, reflection, revision, no fallback on true Mu path (`RO010_LIVE_VERIFICATION_REPORT.md`) |
| No educational regressions | **Met** — inventory cold entries for prior campaigns unchanged |
| Continuity into Topic 3.3 verified | **Met** — section **3** progression → CL-R1 → CM-D1…CM-R1; CL-R1 → CM-D1 selection assert |
| Publication status updated | **Met** — dashboard + coverage map + decision log |

**Campaign Mu is LIVE-complete (package path).** PB-012 is authorised. Wave 11 is **not** started. PB-012 is **not** executed.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **3** progresses through approved Kappa and Lambda days and then receives the **approved CS1-012 Mu packages** for LOs **3.3.1–3.3.5** plus **CM-R1** Revision — jointly activated, not as Isolated Golden Days. Selection after CL-R1 also resolves to **CM-D1**. Cold entry at syllabus topic **3.3** resolves to **CM-D1**.

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, PB-012 authorised, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 10 LIVE Verified; PB-012 authorised · not executed; Wave 11 gated.  
3. `EP001_COVERAGE_MAP.md` / `EP010_COVERAGE_UPDATE.md` — Approver+LIVE credit for 3.3; Continuity Front advanced through 3.3.5 → **63 / 72 (87.5%)**.  
4. Certified Educational Coverage Register + Student Reliance Coverage advanced through Topic **3.3**.

---

## Explicit non-claims

- PB-012 **not executed** by this decision (only authorised).  
- Wave 11 **not started**.  
- Until-exam educational trust **not** claimed from Wave 10 alone.  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Chapter 3 / spine complete **not** claimed.  
- Finish/Home tomorrow chrome **not** certified as matching package text on every Mu day.  
- RO10-R1 Home / label desync **not** cleared.

---

## Residual register (ops follow-up — not Wave 11 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks PB-012? | Blocks Wave 11 start? |
|----|----------|-------------|------------------------|----------------|----------------------|
| RO10-R1 | Ops label desync during Continuity Front multi-day walks | PI / selection presentation | **No** | **No** | **No** |
| RO10-R2 | Revision-day checklist Q6 Learning-oriented audit on CM-R1 | Presentation / audit rubric | **No** | **No** | **No** |
| RO10-R3 | Tomorrow chrome residual on some Mu days (incl. CM-R1) | PI / chrome | **No** | **No** | **No** |

---

## References

- `RO010_DEPLOYMENT_REPORT.md`  
- `RO010_LIVE_VERIFICATION_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO010/`  
- Commit: `c409ad29871d7845f8d9d832776168142d40fad7`  
- Deploy: `dep-d9nmclp42hec73fueteg`  
- Inventory assert: `job-d9nmerijnfac73bcvrs0`  

---

## Completion report sections

### Summary

RO-010 jointly activated Campaign Mu on LIVE, verified educational fidelity on the Continuity Front package path (section 3 → CK…CL-R1 → CM-D1…CM-R1; CL-R1 → CM-D1 selection), and met exit criteria for LIVE-complete with tracked residuals. Coverage advances to **63 / 72 (87.5%)**. Continuity Front advances through Topic **3.3**. PB-012 Progressive Confidence is **authorised**. Wave 11 remains not started. PB-012 is not executed.

### Files Created

- `RO010_DEPLOYMENT_REPORT.md`
- `RO010_LIVE_VERIFICATION_REPORT.md`
- `RO010_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO010/**`

### Files Modified

- Live package copies + campaign status + selection day-order (activation commit `c409ad2…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP010_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 163 passed
```

LIVE inventory assert · LIVE verification (package-path rescored).

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order extension only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic / Student Twin unmodified beyond ops continuity wiring class already used in RO-001…RO-009.

### Technical Debt

RO10-R1 label desync and CM-R1 tomorrow chrome / Q6 residual remain open PI follow-ups outside Wave 11 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive (not until-exam) confidence deferred to PB-012; Baseline section picker (not leaf 3.3) for Continuity Front entry.

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 3.2 / CL-R1 before Wave 10 LIVE.  
- **Student benefit:** Diligent students can study approved Mu days with CMP partnership on LIVE after Lambda.  
- **Learning benefit:** Hypothesis testing (3.3.1–3.3.5) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · 0 fallback on true Mu path · coverage **63 / 72**.  
- **Risks:** Over-claiming until-exam trust; label desync RO10-R1; chrome residual.  
- **Assumptions:** Continuity Front entry via continue at section 3; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO010/` · deploy `dep-d9nmclp42hec73fueteg` · assert job `job-d9nmerijnfac73bcvrs0`.

### Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CL-R1 → CM-D1 selection is explicit after Lambda. Ops label desync can mislabel expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-012.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 11 geography still unpublished. RO10-R1 open (PI). PB-012 not yet executed.

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-010 · 2026-08-02  
**Wave 10 LIVE status:** LIVE-complete (package path) · Residuals RO10-R1 / RO10-R2 / RO10-R3 open · **PB-012 authorised · not executed** · **Wave 11 not started**

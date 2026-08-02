# RO-005 — Release Decision

**Programme:** RO-005 — Wave 5 LIVE Release Operations  
**Volume:** CS1-007 · Campaign Eta · `cs1007-1.0.0`  
**Date:** 2026-08-02  
**Authority:** EP-001 Publication APPROVED (HR-005) · EF-001 · CE-001 coverage law  

---

## Decision

```text
RO-005 Wave 5 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CH-D1…CH-R1): PASS (package path)
Natural Continuity Front chain (continue_topic @ 2 → CB…CG…CE…CZ → CH-D1…CH-R1): PASS (true Eta substance after CZ-R1 session finish / continuation)
Progressive confidence (PB-007): PASS (Eta LIVE-certified only)
Ops label desync / topic_code 2.4 Home collision class: RESIDUAL RO5-R1 — tracked
Finish/Home tomorrow chrome: RESIDUAL on CH-R1 — tracked
Student LIVE credit for Eta packages: AUTHORISED (package path)
Coverage register: 36 / 72 Learning Objectives (50.0%)
Continuity Front: advanced through Topic 2.4
Wave 6: UNBLOCKED for programme start — NOT STARTED in this decision
```

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `40c487e54c73d98a95e8ebfe4b4fbee5c2c52c8d` live · deploy `dep-d9n5qnflk1mc73dpl100` |
| LIVE verification confirms approved educational experience | **Met for package path** — Guided Reading, CMP, activities, reflection, revision progression, no fallback on true Eta path (`RO005_LIVE_VERIFICATION_REPORT.md`) |
| Progressive confidence passes for Eta | **Met** — `PB007_PROGRESSIVE_CONFIDENCE_REPORT.md` · 2×3 days · stable HIGH |
| No educational regressions introduced | **Met** for inventory + Zeta/Epsilon/Gamma/Delta session substance; residuals RO5-R1…R3 tracked (do not fail package-path LIVE-complete) |
| Publication status updated | **Met** — dashboard + coverage map + decision log |

**Campaign Eta is LIVE-complete.** Wave 6 may begin under a separate authorised programme; this decision does **not** start Wave 6.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **2** completes remaining Beta/Gamma/Epsilon/Zeta days and then receives the **approved CS1-007 Eta packages** for LOs **2.4.1–2.4.2** plus **CH-R1** Revision — jointly activated, not as Isolated Golden Days. Cold entry at syllabus topic **2.4** also resolves to **CH-D1**.

Until RO5-R1 is addressed, Home may briefly show a CH-D1 title while late Zeta session substance is still finishing; session Guided Reading for Zeta and then Eta remains package-correct after CZ-R1 completes.

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, PB-007 PASS, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 5 LIVE Verified; Wave 6 gated only by separate start authorisation (LIVE-complete exit met).  
3. `EP001_COVERAGE_MAP.md` / `EP005_COVERAGE_UPDATE.md` — Approver+LIVE credit for 2.4; Continuity Front advanced through 2.4.2 → **36 / 72 (50.0%)**.

---

## Explicit non-claims

- Wave 6 **not started** by this decision (only unblocked).  
- Until-exam educational trust **not** claimed from Wave 5 alone.  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Chapter 2 / spine complete **not** claimed.  
- Finish/Home tomorrow chrome **not** certified as matching package text on CH-R1.  
- RO5-R1 Home / label desync **not** cleared.

---

## Residual register (ops follow-up — not Wave 6 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks Wave 6 start? |
|----|----------|-------------|------------------------|----------------------|
| RO5-R1 | Ops label desync / Home CH-D1 title during late Zeta (`topic_code` 2.4 overlap class) | PI / selection presentation | **No** | **No** |
| RO5-R2 | Revision-day checklist Q6 Learning-oriented audit on CH-R1 | Presentation / audit rubric | **No** | **No** |
| RO5-R3 | Tomorrow chrome residual on CH-R1 | PI / chrome | **No** | **No** |

---

## References

- `RO005_DEPLOYMENT_REPORT.md`  
- `RO005_LIVE_VERIFICATION_REPORT.md`  
- `PB007_PROGRESSIVE_CONFIDENCE_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO005/` · `knowledge/evidence/releases/PB007/`  
- Commit: `40c487e54c73d98a95e8ebfe4b4fbee5c2c52c8d`  
- Deploy: `dep-d9n5qnflk1mc73dpl100`  
- Inventory assert: `job-d9n5rru417fc73cnsoug`  

---

## Completion report sections

### Summary

RO-005 jointly activated Campaign Eta on LIVE, verified educational fidelity on the Continuity Front package path (CZ-R1 → CH-D1…CH-R1), and obtained progressive confidence PASS for CH-D1…CH-R1. Exit criteria for LIVE-complete are met with tracked residuals. Coverage advances to **36 / 72 (50.0%)**. Continuity Front advances through Topic **2.4**. Wave 6 remains not started.

### Files Created

- `RO005_DEPLOYMENT_REPORT.md`
- `RO005_LIVE_VERIFICATION_REPORT.md`
- `PB007_PROGRESSIVE_CONFIDENCE_REPORT.md`
- `RO005_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO005/**`
- `knowledge/evidence/releases/PB007/**`

### Files Modified

- Live package copies + campaign status + selection day-order (activation commit `40c487e54…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP005_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 119 passed
```

LIVE inventory assert · LIVE verification · PB-007 progressive confidence.

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order extension only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic unmodified beyond ops continuity wiring class already used in RO-001…RO-004.

### Technical Debt

RO5-R1 Home / label desync and CH-R1 tomorrow chrome residual remain open PI follow-ups outside Wave 6 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive (not until-exam) confidence; two-persona PB-007 cohort; Baseline section picker (not leaf 2.4) for Continuity Front entry.

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 2.3.2 / CZ-R1 before Wave 5 LIVE.  
- **Student benefit:** Diligent students can study approved Eta days with CMP partnership on LIVE after Zeta.  
- **Learning benefit:** Generating functions entry (2.4.1–2.4.2) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · PB-007 PASS · 0 fallback on true Eta path · coverage **36 / 72**.  
- **Risks:** Over-claiming until-exam trust; Home title collision RO5-R1; chrome residual at CH-R1.  
- **Assumptions:** Continuity Front entry via continue at section 2; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO005/` · `knowledge/evidence/releases/PB007/` · deploy `dep-d9n5qnflk1mc73dpl100` · assert job `job-d9n5rru417fc73cnsoug`.

### Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CZ-R1 → CH-D1 selection is explicit after Zeta session completion. Topic-code overlap and ops label desync can mislabel Home / expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 6 geography still unpublished. RO5-R1 open (PI).

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-005 · 2026-08-02  
**Wave 5 LIVE status:** LIVE-complete (package path) · Residuals RO5-R1 / RO5-R2 / RO5-R3 open · **Wave 6 unblocked · not started**

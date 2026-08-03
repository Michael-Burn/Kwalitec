# RO-012 — Release Decision

**Programme:** RO-012 — Wave 12 LIVE Release Operations  
**Volume:** CS1-014 · Campaign Xi · `cs1014-1.0.0`  
**Date:** 2026-08-03  
**Authority:** EP-001 Publication APPROVED (HR-012) · EF-001 · CE-001 coverage law · FP-01  

---

## Decision

```text
RO-012 Wave 12 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CX-D1…CX-R1): PASS (package path)
Natural Continuity Front chain (continue_topic @ 3 → CK…CL…CM…CN-R1 → CX-D1…CX-R1): PASS (true Xi substance after CN-R1 session finish / continuation)
Progressive confidence (PB-014): AUTHORISED — NOT EXECUTED
Ops label desync / Finish-Home tomorrow chrome: RESIDUAL RO12-R1…R3 — tracked
Student LIVE credit for Xi packages: AUTHORISED (package path)
Coverage register: 63 / 72 Learning Objectives (87.5%) — HELD (4.2 already Published via CS1-003)
Student Reliance: advanced through Topic 4.2
Wave 13: NOT STARTED
PB-014: AUTHORISED only — not started
```

**Coverage honesty note:** The RO-012 mission brief Phase 4 stated Published Coverage → **72 / 72 (100%)**. That figure conflicts with binding **HR-012** activation conditions and **CE-001** Approver-credit law (Topic 4.2 already counted via CS1-003; Wave 0 Alpha/Beta Approver honesty gap still open at **9 / 72** Awaiting Approval). This decision **holds** Certified Educational Coverage at **63 / 72 (87.5%)** and advances **Student Reliance** through Topic **4.2** only. No commercial readiness, product completion, or until-examination trust claim.

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `a800c85f602b68d1380ae355c0d2839403018995` live · deploy `dep-d9o0dnu7bikc73cnt8o0` |
| LIVE verification confirms approved educational experience | **Met for package path** — Guided Reading, CMP, activities, reflection, revision progression, no fallback on true Xi path (`RO012_LIVE_VERIFICATION_REPORT.md`) |
| Progressive confidence | **Not run** — authorised as PB-014 only |
| No educational regressions introduced | **Met** for inventory + prior Continuity Front / Trust Front cold entries; residuals RO12-R1…R3 tracked (do not fail package-path LIVE-complete) |
| Publication status updated | **Met** — dashboard + coverage map + decision log |
| Published Coverage unchanged | **Met** — remains **63 / 72 (87.5%)** |
| Student Reliance advances through Topic 4.2 | **Met** after LIVE verification PASS |

**Campaign Xi is LIVE-complete (package path).** PB-014 may begin under a separate authorised programme; this decision does **not** execute PB-014 or start Wave 13.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **3** completes remaining Kappa/Lambda/Mu/Nu days and then receives the **approved CS1-014 Xi packages** for LOs **4.2.1–4.2.10** plus **CX-R1** Revision — jointly activated, not as Isolated Golden Days. Trust Front cold entry at syllabus topic **4.2** remains **CD-D6** (independent Delta inventory).

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 12 LIVE Verified; PB-014 gated only by separate start authorisation.  
3. `EP001_COVERAGE_MAP.md` / `EP012_COVERAGE_UPDATE.md` — Approver credit **held** 63/72; Student Reliance advanced through Topic **4.2**.  
4. Student Reliance Coverage advanced through Topic **4.2** (no Approver double-count).

---

## Explicit non-claims

- PB-014 **not executed** by this decision (only authorised).  
- Wave 13 **not started**.  
- Until-exam educational trust **not** claimed from Wave 12 alone.  
- Published Coverage **not** increased (4.2 already counted via CS1-003).  
- **100% CS1 Approver coverage not claimed** (Wave 0 Alpha/Beta honesty gap remains).  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Trust Front 5.1 **not** absorbed into Continuity Front credit.  
- Finish/Home tomorrow chrome **not** certified as matching package text on every Xi day.  
- RO12-R1 Home / label desync **not** cleared.

---

## Residual register (ops follow-up — not Wave 13 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks PB-014 start? |
|----|----------|-------------|------------------------|----------------------|
| RO12-R1 | Ops label desync during Continuity Front multi-day walks | PI / selection presentation | **No** | **No** |
| RO12-R2 | Revision-day checklist Q6 Learning-oriented audit on CX-R1 | Presentation / audit rubric | **No** | **No** |
| RO12-R3 | Tomorrow chrome residual on some Xi days (incl. CX-R1) | PI / chrome | **No** | **No** |

---

## References

- `RO012_DEPLOYMENT_REPORT.md`  
- `RO012_LIVE_VERIFICATION_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO012/`  
- Commit: `a800c85f602b68d1380ae355c0d2839403018995`  
- Deploy: `dep-d9o0dnu7bikc73cnt8o0`  
- Inventory assert: `job-d9o0fnm7bikc73co0fi0`  

---

## Completion report sections

### Summary

RO-012 jointly activated Campaign Xi on LIVE, verified educational fidelity on the Continuity Front package path (CN-R1 → CX-D1…CX-R1), and held Published Coverage at **63 / 72 (87.5%)** while advancing Student Reliance through Topic **4.2**. Exit criteria for LIVE-complete are met with tracked residuals. PB-014 remains not started.

### Files Created

- `RO012_DEPLOYMENT_REPORT.md`
- `RO012_LIVE_VERIFICATION_REPORT.md`
- `RO012_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO012/**`

### Files Modified

- Live package copies + campaign status + selection day-order / CN-R1 handoff (activation commit `a800c85…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP012_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 184 passed
```

LIVE inventory assert · LIVE verification (package path rescored).

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order / Nu–Xi–Delta coexistence preference only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic unmodified beyond ops continuity wiring class already used in RO-001…RO-011.

### Technical Debt

RO12-R1 label desync and CX-R1 tomorrow chrome / Q6 residual remain open PI follow-ups outside Wave 13 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive confidence deferred to PB-014; Baseline section picker (not leaf 4.2) for Continuity Front entry; Trust Front cold entry at 4.2 remains Delta; Approver coverage remains 63/72 (not 100%).

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 4.1 / CN-R1 before Wave 12 LIVE.  
- **Student benefit:** Diligent students can study approved Xi days with CMP partnership on LIVE after Nu.  
- **Learning benefit:** GLM CF-join (4.2.1–4.2.10) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · 0 fallback on true Xi path · coverage **63 / 72 held** · reliance through Topic **4.2**.  
- **Risks:** Over-claiming until-exam trust or 100% Approver coverage; label desync RO12-R1; chrome residual; Approver double-count temptation.  
- **Assumptions:** Continuity Front entry via continue at section 3; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO012/` · deploy `dep-d9o0dnu7bikc73cnt8o0` · assert job `job-d9o0fnm7bikc73co0fi0`.

### Lessons learned for student value

Joint activation of a Continuity Front join onto already-Published Trust Front geography works when FP-01 is held, CN-R1 → CX-D1 selection is explicit, and Xi/Delta coexistence is resolved without absorbing 5.1. Ops label desync can mislabel expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory under PB-014. Holding Approver coverage at 63/72 after Xi LIVE is itself a student-trust behaviour.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. RO12-R1 open (PI). PB-014 not executed. No 100% Approver-credit claim.

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-012 · 2026-08-03  
**Wave 12 LIVE status:** LIVE-complete (package path) · Residuals RO12-R1 / RO12-R2 / RO12-R3 open · **PB-014 authorised · not started** · **Wave 13 not started**

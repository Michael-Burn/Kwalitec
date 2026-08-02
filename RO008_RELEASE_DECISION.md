# RO-008 — Release Decision

**Programme:** RO-008 — Wave 8 LIVE Release Operations  
**Volume:** CS1-010 · Campaign Kappa · `cs1010-1.0.0`  
**Date:** 2026-08-02  
**Authority:** EP-001 Publication APPROVED (HR-008) · EF-001 · CE-001 coverage law  

---

## Decision

```text
RO-008 Wave 8 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CK-D1…CK-R1): PASS (package path)
Natural Continuity Front into Topic 3.1 (continue_topic @ 3 → CK-D1…CK-R1; CI-R1 → CK-D1 selection): PASS
Progressive confidence (PB-010): AUTHORISED — NOT EXECUTED in this decision
Ops label desync / Finish-Home tomorrow chrome: RESIDUAL RO8-R1…R3 — tracked
Student LIVE credit for Kappa packages: AUTHORISED (package path)
Coverage register: 50 / 72 Learning Objectives (69.4%)
Continuity Front: advanced through Topic 3.1
Wave 9: UNBLOCKED for programme start only after PB-010 PASS — NOT STARTED in this decision
PB-010 Progressive Confidence: AUTHORISED
```

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `28a06b176cd1ca1249cc74de0726e5d8c46f5982` live · deploy `dep-d9nhl65aeets73bvaabg` |
| Package-path fidelity holds | **Met** — Guided Reading, CMP, activities, reflection, revision, no fallback on true Kappa path (`RO008_LIVE_VERIFICATION_REPORT.md`) |
| No educational regressions | **Met** — inventory cold entries for prior campaigns unchanged |
| Continuity into Topic 3.1 verified | **Met** — section **3** entry → CK-D1…CK-R1; CI-R1 → CK-D1 selection assert |
| Publication status updated | **Met** — dashboard + coverage map + decision log |

**Campaign Kappa is LIVE-complete (package path).** PB-010 is authorised. Wave 9 is **not** started.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **3** receives the **approved CS1-010 Kappa packages** for LOs **3.1.1–3.1.6** plus **CK-R1** Revision — jointly activated, not as Isolated Golden Days. Selection after CI-R1 also resolves to **CK-D1**. Cold entry at syllabus topic **3.1** resolves to **CK-D1**.

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, PB-010 authorised, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 8 LIVE Verified; PB-010 authorised · not executed; Wave 9 gated on PB-010.  
3. `EP001_COVERAGE_MAP.md` / `EP008_COVERAGE_UPDATE.md` — Approver+LIVE credit for 3.1; Continuity Front advanced through 3.1.6 → **50 / 72 (69.4%)**.  
4. Certified Educational Coverage Register + Student Reliance Coverage advanced through Topic **3.1**.

---

## Explicit non-claims

- PB-010 **not executed** by this decision (only authorised).  
- Wave 9 **not started**.  
- Until-exam educational trust **not** claimed from Wave 8 alone.  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Chapter 3 / spine complete **not** claimed.  
- Finish/Home tomorrow chrome **not** certified as matching package text on every Kappa day.  
- RO8-R1 Home / label desync **not** cleared.

---

## Residual register (ops follow-up — not Wave 9 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks PB-010? | Blocks Wave 9 start? |
|----|----------|-------------|------------------------|----------------|----------------------|
| RO8-R1 | Ops label desync during Continuity Front multi-day walks | PI / selection presentation | **No** | **No** | **No** |
| RO8-R2 | Revision-day checklist Q6 Learning-oriented audit on CK-R1 | Presentation / audit rubric | **No** | **No** | **No** |
| RO8-R3 | Tomorrow chrome residual on some Kappa days (incl. CK-R1) | PI / chrome | **No** | **No** | **No** |

---

## References

- `RO008_DEPLOYMENT_REPORT.md`  
- `RO008_LIVE_VERIFICATION_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO008/`  
- Commit: `28a06b176cd1ca1249cc74de0726e5d8c46f5982`  
- Deploy: `dep-d9nhl65aeets73bvaabg`  
- Inventory assert: `job-d9nhpfajnfac73b47gv0`  

---

## Completion report sections

### Summary

RO-008 jointly activated Campaign Kappa on LIVE, verified educational fidelity on the Continuity Front package path (section 3 → CK-D1…CK-R1; CI-R1 → CK-D1 selection), and met exit criteria for LIVE-complete with tracked residuals. Coverage advances to **50 / 72 (69.4%)**. Continuity Front advances through Topic **3.1**. PB-010 Progressive Confidence is **authorised**. Wave 9 remains not started.

### Files Created

- `RO008_DEPLOYMENT_REPORT.md`
- `RO008_LIVE_VERIFICATION_REPORT.md`
- `RO008_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO008/**`

### Files Modified

- Live package copies + campaign status + selection day-order (activation commit `28a06b1…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP008_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 144 passed
```

LIVE inventory assert · LIVE verification (package path).

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order extension only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic unmodified beyond ops continuity wiring class already used in RO-001…RO-007.

### Technical Debt

RO8-R1 label desync and CK-R1 tomorrow chrome / Q6 residual remain open PI follow-ups outside Wave 9 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive confidence not yet run (PB-010 authorised only); Baseline section picker (section **3**) for Continuity Front entry into 3.1.

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 2.6.6 / CI-R1 before Wave 8 LIVE.  
- **Student benefit:** Diligent students can study approved Kappa days with CMP partnership on LIVE after Iota.  
- **Learning benefit:** Estimators (3.1.1–3.1.6) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · 0 fallback on true Kappa path · coverage **50 / 72**.  
- **Risks:** Over-claiming until-exam trust; label desync RO8-R1; chrome residual.  
- **Assumptions:** Continuity Front entry via continue at section 3; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO008/` · deploy `dep-d9nhl65aeets73bvaabg` · assert job `job-d9nhpfajnfac73b47gv0`.

### Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CI-R1 → CK-D1 selection is explicit after Iota. Ops label desync can mislabel expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-010.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 9 geography still unpublished. RO8-R1 open (PI). PB-010 not yet executed.

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-008 · 2026-08-02  
**Wave 8 LIVE status:** LIVE-complete (package path) · Residuals RO8-R1 / RO8-R2 / RO8-R3 open · **PB-010 authorised · not executed** · **Wave 9 not started**

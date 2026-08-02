# RO-009 — Release Decision

**Programme:** RO-009 — Wave 9 LIVE Release Operations  
**Volume:** CS1-011 · Campaign Lambda · `cs1011-1.0.0`  
**Date:** 2026-08-02  
**Authority:** EP-001 Publication APPROVED (HR-009) · EF-001 · CE-001 coverage law  

---

## Decision

```text
RO-009 Wave 9 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CL-D1…CL-R1): PASS (package path)
Natural Continuity Front into Topic 3.2 (continue_topic @ 3 → CK… → CL-D1…CL-R1; CK-R1 → CL-D1 selection): PASS
Progressive confidence (PB-011): AUTHORISED — NOT EXECUTED in this decision
Ops label desync / Finish-Home tomorrow chrome: RESIDUAL RO9-R1…R3 — tracked
Student LIVE credit for Lambda packages: AUTHORISED (package path)
Coverage register: 58 / 72 Learning Objectives (80.6%)
Continuity Front: advanced through Topic 3.2
Wave 10: UNBLOCKED for programme start only after PB-011 PASS — NOT STARTED in this decision
PB-011 Progressive Confidence: AUTHORISED
```

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `518467508e27b609c60e4eb5fe0410ea5c868314` live · deploy `dep-d9njjqm7bikc73c2i86g` |
| Fingerprint matches | **Met** |
| Package inventory correct | **Met** — 77 approved · 9 Lambda · no duplicate/missing IDs |
| Package-path fidelity holds | **Met** — Guided Reading, CMP, activities, reflection, revision, no fallback on true Lambda path (`RO009_LIVE_VERIFICATION_REPORT.md`) |
| No educational regressions | **Met** — inventory cold entries for prior campaigns unchanged |
| Continuity into Topic 3.2 verified | **Met** — section **3** progression → CL-D1…CL-R1; CK-R1 → CL-D1 selection assert |
| Publication status updated | **Met** — dashboard + coverage map + decision log |

**Campaign Lambda is LIVE-complete (package path).** PB-011 is authorised. Wave 10 is **not** started. PB-011 is **not** executed.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **3** progresses through approved Kappa days and then receives the **approved CS1-011 Lambda packages** for LOs **3.2.1–3.2.8** plus **CL-R1** Revision — jointly activated, not as Isolated Golden Days. Selection after CK-R1 also resolves to **CL-D1**. Cold entry at syllabus topic **3.2** resolves to **CL-D1**.

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, PB-011 authorised, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 9 LIVE Verified; PB-011 authorised · not executed; Wave 10 gated on PB-011.  
3. `EP001_COVERAGE_MAP.md` / `EP009_COVERAGE_UPDATE.md` — Approver+LIVE credit for 3.2; Continuity Front advanced through 3.2.8 → **58 / 72 (80.6%)**.  
4. Certified Educational Coverage Register + Student Reliance Coverage advanced through Topic **3.2**.

---

## Explicit non-claims

- PB-011 **not executed** by this decision (only authorised).  
- Wave 10 **not started**.  
- Until-exam educational trust **not** claimed from Wave 9 alone.  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Chapter 3 / spine complete **not** claimed.  
- Finish/Home tomorrow chrome **not** certified as matching package text on every Lambda day.  
- RO9-R1 Home / label desync **not** cleared.

---

## Residual register (ops follow-up — not Wave 10 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks PB-011? | Blocks Wave 10 start? |
|----|----------|-------------|------------------------|----------------|----------------------|
| RO9-R1 | Ops label desync during Continuity Front multi-day walks | PI / selection presentation | **No** | **No** | **No** |
| RO9-R2 | Revision-day checklist Q6 Learning-oriented audit on CL-R1 | Presentation / audit rubric | **No** | **No** | **No** |
| RO9-R3 | Tomorrow chrome residual on some Lambda days (incl. CL-R1) | PI / chrome | **No** | **No** | **No** |

---

## References

- `RO009_DEPLOYMENT_REPORT.md`  
- `RO009_LIVE_VERIFICATION_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO009/`  
- Commit: `518467508e27b609c60e4eb5fe0410ea5c868314`  
- Deploy: `dep-d9njjqm7bikc73c2i86g`  
- Inventory assert: `job-d9njlr5aeets73c3bihg`  

---

## Completion report sections

### Summary

RO-009 jointly activated Campaign Lambda on LIVE, verified educational fidelity on the Continuity Front package path (section 3 → CK… → CL-D1…CL-R1; CK-R1 → CL-D1 selection), and met exit criteria for LIVE-complete with tracked residuals. Coverage advances to **58 / 72 (80.6%)**. Continuity Front advances through Topic **3.2**. PB-011 Progressive Confidence is **authorised**. Wave 10 remains not started. PB-011 is not executed.

### Files Created

- `RO009_DEPLOYMENT_REPORT.md`
- `RO009_LIVE_VERIFICATION_REPORT.md`
- `RO009_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO009/**`

### Files Modified

- Live package copies + campaign status + selection day-order (activation commit `5184675…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP009_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 155 passed
```

LIVE inventory assert · LIVE verification (package path).

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order extension only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic unmodified beyond ops continuity wiring class already used in RO-001…RO-008.

### Technical Debt

RO9-R1 label desync and CL-R1 tomorrow chrome / Q6 residual remain open PI follow-ups outside Wave 10 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive confidence not yet run (PB-011 authorised only); Baseline section picker (section **3**) for Continuity Front entry into 3.2 via natural progression through 3.1.

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 3.1.6 / CK-R1 before Wave 9 LIVE.  
- **Student benefit:** Diligent students can study approved Lambda days with CMP partnership on LIVE after Kappa.  
- **Learning benefit:** Confidence and prediction intervals (3.2.1–3.2.8) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · 0 fallback on true Lambda path · coverage **58 / 72**.  
- **Risks:** Over-claiming until-exam trust; label desync RO9-R1; chrome residual.  
- **Assumptions:** Continuity Front entry via continue at section 3; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO009/` · deploy `dep-d9njjqm7bikc73c2i86g` · assert job `job-d9njlr5aeets73c3bihg`.

### Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CK-R1 → CL-D1 selection is explicit after Kappa. Ops label desync can mislabel expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-011.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 10 geography still unpublished. RO9-R1 open (PI). PB-011 not yet executed.

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-009 · 2026-08-02  
**Wave 9 LIVE status:** LIVE-complete (package path) · Residuals RO9-R1 / RO9-R2 / RO9-R3 open · **PB-011 authorised · not executed** · **Wave 10 not started**

### Exit status

```text
PASS — Wave 9 LIVE-complete (package path) WITH RESIDUAL.
Authorise: PB-011 — Progressive Educational Confidence Certification.
STOP.
Do not execute PB-011.
Do not begin Wave 10.
Certified Educational Coverage: 58 / 72 (80.6%).
Student Reliance Coverage: through Topic 3.2 / 3.2.8.
```

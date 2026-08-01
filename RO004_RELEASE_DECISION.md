# RO-004 — Release Decision

**Programme:** RO-004 — Wave 4 LIVE Release Operations  
**Volume:** CS1-006 · Campaign Zeta · `cs1006-1.0.0`  
**Date:** 2026-08-01  
**Authority:** EP-001 Publication APPROVED (HR-004) · EF-001 · CE-001 coverage law  

---

## Decision

```text
RO-004 Wave 4 LIVE release: LIVE-COMPLETE — ACCEPTED WITH RESIDUAL
Deployment: PASS
Educational package delivery (CZ-D1…CZ-R1): PASS (package path)
Natural Continuity Front chain (continue_topic @ 2 → CB…CG…CE → CZ-D1…CZ-R1): PASS (true Zeta substance after CE-R1 session finish)
Progressive confidence (PB-006): PASS (Zeta LIVE-certified only)
Home title collision during late Epsilon (topic_code 2.3): RESIDUAL RO4-R1 — tracked
Finish/Home tomorrow chrome: RESIDUAL on CZ-R1 — tracked
Student LIVE credit for Zeta packages: AUTHORISED (package path)
Wave 5: UNBLOCKED for programme start — NOT STARTED in this decision
```

---

## Exit criteria scorecard

| Criterion | Result |
|-----------|--------|
| Deployment succeeds | **Met** — tip `58096787f7ea17704dcb60e2475e9a431f2c95e8` live · deploy `dep-d9n4glvlk1mc73dnji4g` |
| LIVE verification confirms approved educational experience | **Met for package path** — Guided Reading, CMP, activities, reflection, revision progression, no fallback on true Zeta path (`RO004_LIVE_VERIFICATION_REPORT.md`) |
| Progressive confidence passes for Zeta | **Met** — `PB006_PROGRESSIVE_CONFIDENCE_REPORT.md` · 2×3 days · stable HIGH |
| No educational regressions introduced | **Met** for inventory + Epsilon/Gamma/Delta session substance; Home title collision RO4-R1 tracked (does not fail package-path LIVE-complete) |
| Publication status updated | **Met** — dashboard + coverage map + decision log |

**Campaign Zeta is LIVE-complete.** Wave 5 may begin under a separate authorised programme; this decision does **not** start Wave 5.

---

## What students receive

A diligent Internal Alpha student entering the Continuity Front via Baseline `continue_topic` at section **2** completes remaining Beta/Gamma/Epsilon days and then receives the **approved CS1-006 Zeta packages** for LOs **2.3.1–2.3.2** plus **CZ-R1** Revision — jointly activated, not as Isolated Golden Days. Cold entry at syllabus topic **2.3** also resolves to **CZ-D1**.

Until RO4-R1 is addressed, Home may briefly show a CZ-D1 title while Epsilon session substance is still finishing; session Guided Reading for Epsilon and then Zeta remains package-correct after CE-R1 completes.

---

## Governance updates required (executed with this decision)

1. `EP001_PUBLICATION_DECISION_LOG.md` — deployment commit, LIVE verify, PB-006 PASS, checklist Done.  
2. `EP001_PUBLICATION_DASHBOARD.md` — Wave 4 LIVE Verified; Wave 5 gated only by separate start authorisation (LIVE-complete exit met).  
3. `EP001_COVERAGE_MAP.md` / `EP004_COVERAGE_UPDATE.md` — Approver+LIVE credit for 2.3; Continuity Front advanced through 2.3.2.

---

## Explicit non-claims

- Wave 5 **not started** by this decision (only unblocked).  
- Until-exam educational trust **not** claimed from Wave 4 alone.  
- Wave 0 Alpha/Beta Publication Approver honesty gap **not waived**.  
- Chapter 2 / spine complete **not** claimed.  
- Finish/Home tomorrow chrome **not** certified as matching package text on CZ-R1.  
- RO4-R1 Home title collision **not** cleared.

---

## Residual register (ops follow-up — not Wave 5 content)

| ID | Residual | Owner class | Blocks LIVE-complete? | Blocks Wave 5 start? |
|----|----------|-------------|------------------------|----------------------|
| RO4-R1 | Home CZ-D1 title during late Epsilon (`topic_code` 2.3 overlap) | PI / selection presentation | **No** | **No** |
| RO4-R2 | Revision-day checklist Q6 Learning-oriented audit on CZ-R1 | Presentation / audit rubric | **No** | **No** |
| RO4-R3 | Tomorrow chrome residual on CZ-R1 | PI / chrome | **No** | **No** |

---

## References

- `RO004_DEPLOYMENT_REPORT.md`  
- `RO004_LIVE_VERIFICATION_REPORT.md`  
- `PB006_PROGRESSIVE_CONFIDENCE_REPORT.md`  
- Evidence: `knowledge/evidence/releases/RO004/` · `knowledge/evidence/releases/PB006/`  
- Commit: `58096787f7ea17704dcb60e2475e9a431f2c95e8`  
- Deploy: `dep-d9n4glvlk1mc73dnji4g`  
- Inventory assert: `job-d9n4j4m1egvs73fcp41g`  

---

## Completion report sections

### Summary

RO-004 jointly activated Campaign Zeta on LIVE, verified educational fidelity on the Continuity Front package path (CE-R1 → CZ-D1…CZ-R1), and obtained progressive confidence PASS for CZ-D1…CZ-R1. Exit criteria for LIVE-complete are met with tracked residuals. Wave 5 remains not started.

### Files Created

- `RO004_DEPLOYMENT_REPORT.md`
- `RO004_LIVE_VERIFICATION_REPORT.md`
- `PB006_PROGRESSIVE_CONFIDENCE_REPORT.md`
- `RO004_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RO004/**`
- `knowledge/evidence/releases/PB006/**`

### Files Modified

- Live package copies + campaign status + selection day-order (activation commit `58096787…`)
- `EP001_PUBLICATION_DECISION_LOG.md`
- `EP001_PUBLICATION_DASHBOARD.md`
- `EP001_COVERAGE_MAP.md`
- `EP004_COVERAGE_UPDATE.md`
- Related educational_packages / PB-002 tests (activation)

### Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 113 passed
```

LIVE inventory assert · LIVE verification · PB-006 progressive confidence.

### Migration Impact

None.

### Architecture Compliance

EA-006 live loader + PB-002 selection day-order extension only. Educational package bodies / Educational Framework / Runtime educational behaviour / recommendation logic unmodified beyond ops continuity wiring class already used in RO-001 / RO-002 / RO-003.

### Technical Debt

RO4-R1 Home title collision and CZ-R1 tomorrow chrome residual remain open PI follow-ups outside Wave 5 content authoring.

### Known Limitations

Ops calendar backdating for multi-day verify; progressive (not until-exam) confidence; two-persona PB-006 cohort; Baseline section picker (not leaf 2.3) for Continuity Front entry.

### Student Impact Assessment

- **Student problem:** Continuity Front stopped at 2.2.4 / CE-R1 before Wave 4 LIVE.  
- **Student benefit:** Diligent students can study approved Zeta days with CMP partnership on LIVE after Epsilon.  
- **Learning benefit:** Conditional expectations entry (2.3.1–2.3.2) + revision sequence is jointly live.  
- **Success metrics:** Deploy PASS · LIVE verify PASS WITH RESIDUAL · PB-006 PASS · 0 fallback on true Zeta path.  
- **Risks:** Over-claiming until-exam trust; Home title collision RO4-R1; chrome residual at CZ-R1.  
- **Assumptions:** Continuity Front entry via continue at section 2; CMP remains external authority.

### Estimated KSI contribution

ΔKSI = 0 (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

### Evidence collected

`knowledge/evidence/releases/RO004/` · `knowledge/evidence/releases/PB006/` · deploy `dep-d9n4glvlk1mc73dnji4g` · assert job `job-d9n4j4m1egvs73fcp41g`.

### Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CE-R1 → CZ-D1 selection is explicit after Epsilon session completion. Topic-code overlap between curriculum nodes and educational packages can mislabel Home without corrupting session substance — keep that residual separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking change.

### Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 5 geography still unpublished. RO4-R1 open (PI).

### CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-004 · 2026-08-01  
**Wave 4 LIVE status:** LIVE-complete (package path) · Residuals RO4-R1 / RO4-R2 / RO4-R3 open · **Wave 5 unblocked · not started**

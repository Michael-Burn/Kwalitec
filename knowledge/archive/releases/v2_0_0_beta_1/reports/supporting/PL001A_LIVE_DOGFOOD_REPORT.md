# PL-001A — Live Dogfood Report

**Programme:** Product Validation · Live Dogfooding  
**Status:** COMPLETE (decision recorded)  
**Date:** 2026-07-30  
**Subject:** CS1 — Actuarial Statistics (IFoA)  
**Sources:** ActEd CS1 CMP 2019 + IFoA CS1 Syllabus 2026 (Studio-bound PDFs)  
**Workspace:** `ws-cs1`  
**Baseline commit:** `6abacdd7d14176a0ada980bf08ea8595295c7b2f`  
**Evidence:** `knowledge/evidence/releases/PL001A/`  
**Harness:** `knowledge/engineering/pl001a_live_dogfood/pl001a_live_dogfood.py`  

---

## Summary

PL-001A validated the existing Curriculum Intelligence Platform end-to-end against
real CS1 documents **without introducing new architecture**. The syllabus-
authoritative Generation Chain (G1–G7) reached **`CERTIFIED_WITH_WARNINGS`**
with a coherent educational hierarchy (5 chapters · 15 topics · 73 learning
objectives), quality score **95.79**, and a full Review Pack. Certified Daily
Missions, Knowledge Graph, Tutor grounding, Progress, Adaptive signals, and
Curriculum Observatory all behaved correctly against the certified snapshot.

Closed beta is nevertheless **BLOCKED**: the **active published package**
students would enrol into remains the FV-002 uncertified noisy extract
(1,931 sections / 5,024 topics / 21 objectives, no `certification` block).
Additional blockers: CMP+syllabus Gen2 fails the production confidence
regression gate, and Founder calibration re-runs do not reliably re-emit a
certification decision.

---

## FINAL DECISION

# BLOCKED

**Justification:** The certified engine path is educationally strong on the
official CS1 syllabus, but the live Student Runtime catalogue still serves the
pre-EQ-001 / pre-EI noisy package. Shipping closed beta now would enrol learners
into an uncertified, front-matter-contaminated curriculum despite a certified
candidate existing offline. Unblock requires: (1) republish certified CS1 as the
active package, (2) Gen2 confidence-epsilon / CMP inclusion fix, (3) calibration
re-certification reliability.

---

## Workflow executed

```
Upload (existing Studio PDFs)
  → Extract + normalise (PyPDF)
  → Curriculum Intelligence Engine G1…G7
  → Certification (Gen 7)
  → Founder Calibration (style dimensions)
  → Founder Preview / certified package projection
  → Review Pack + Observatory
  → Student surfaces: Missions · KG · Tutor · Progress · Adaptive
  → Publication readiness check (active catalogue)
```

| Stage | Result | Notes |
|---|---|---|
| Baseline active package | Fail (quality) | CS1/`2026.1` active, **no certification**, 1931/5024/21 |
| Extract syllabus + CMP | Pass | Syllabus 8p/323 blocks; CMP 912p/37,167 blocks |
| CMP+syllabus probe | Fail @ Gen2 | Confidence `0.8493 < 0.8606` stops production chain |
| Syllabus-authoritative G1–G7 | Pass | `CERTIFIED_WITH_WARNINGS`, 5/15/73 |
| Review Pack | Pass | 8 artefacts; chain matches certification |
| Founder Calibration | Partial | Profile saved; Gen3–7 rerun; **no post-cal certification decision** |
| Founder Preview | Pass | Preview-eligible; quality 95.79 |
| Knowledge Graph | Pass | 93 nodes / 175 edges; certified provenance |
| Daily Missions (×5) | Pass | Official CS1 topic/LO titles; no front-matter |
| Tutor grounding | Pass | Foreign node rejected; certified primary only |
| Progress | Pass | Stable under identical inputs |
| Adaptive learning | Pass | Weak / missed / revision / dependency signals |
| Observatory | Pass | Certification trends, coverage, decision quality |
| Live republish to catalogue | Not done | Candidate package evidence only — active row unchanged |

Primary certification path used **syllabus-authoritative** sources (EQ-001 Founder
publish shape). CMP body inclusion under production `stop_on_regression=True` is
documented as a separate defect probe.

---

## Strengths

1. **Syllabus fidelity** — Certified hierarchy matches official 2026 CS1 weighted
   topics (Data analysis → … → 5 chapters, 15 topic outcomes, 73 LOs).
2. **Mission coherence** — Sample missions start at “1.1 Describe the purpose and
   function of data analysis” with real LO texts (1.1.1…), not “Associateship
   Qualification” / CMP chrome.
3. **Certification quality** — Score 95.79; coverage 1.0; hierarchy 0.8941;
   evidence quality 0.9947; no hard-gate failures.
4. **Tutor grounding** — `CertifiedTutorContextService` rejects foreign ids and
   keeps excerpts on certified nodes with provenance.
5. **Progress stability** — Identical inputs → identical mastery / missed sets.
6. **Adaptive signals** — Meaningful weak/missed/revision/dependency rankings on
   certified node ids.
7. **Review Pack ↔ certification** — Same chain id; Gen comparison + certification
   artefact present.
8. **Observatory** — Reports certification outcomes, coverage metrics, decision
   quality, and policy warnings from Curriculum Memory.

---

## Weaknesses

1. **Active catalogue drift** — Live publish path not yet cut over to certified
   snapshots; Student Discovery still offers noisy CS1/`2026.1`.
2. **CMP inclusion blocked** — Production regression confidence gate rejects Gen2
   noise elimination on real CMP body (~0.01 confidence dip).
3. **Calibration re-cert gap** — Applying Founder style dimensions re-runs Gen3–7
   but did not yield a new `CertificationDecision` in this dogfood.
4. **UI surfaces incomplete** — No Founder Observatory console; no student
   Knowledge Graph page (service-level evidence only); Tutor certified filter
   remains opt-in DI.
5. **Full CMP scale** — 912 pages / ~37k blocks; operational dogfood used pages
   30–180 for the CMP probe (documented).

---

## Critical defects

| # | Defect | Evidence |
|---|---|---|
| C1 | Active published CS1 lacks `package.certification` | `legacy_published_package_summary.json` |
| C2 | Active structure still pre-EQ001 noise (5024 topics) | Same; FV-002 residual |
| C3 | CMP+syllabus Gen2 rejected: `confidence:0.8493<0.8606` | `cmp_probe_regression.json` |
| C4 | Calibration rerun leaves `intelligence_certified=false` / no cert decision | `calibration/calibration_history.json` |

---

## Minor issues

| # | Issue |
|---|---|
| M1 | Certification warning: 1/73 LOs lack syllabus ref / cmp_only_support |
| M2 | Full-CMP Gen1 scale needs windowed / batch ops for live republish |
| M3 | Tutor `certified_tutor=` not bound in production composition (EI-002B) |
| M4 | Observatory Founder Console UI not shipped |
| M5 | Learner KG has no student UI (Mermaid projection used as screenshot substitute) |

---

## Quality gates

| Gate | Result |
|---|---|
| Mission coherence | **Pass** — official CS1 LO titles |
| Curriculum fidelity (certified path) | **Pass** — 5/15/73 |
| Curriculum fidelity (active catalogue) | **Fail** — 1931/5024/21 |
| Objective coverage | **Pass** — 73 LOs; coverage metric 1.0 |
| Tutor accuracy / grounding | **Pass** |
| Progress stability | **Pass** |
| Calibration effectiveness | **Fail** — profile applies; re-cert missing |
| Certification consistency | **Partial** — syllabus path OK; CMP path blocked at Gen2 |
| Student usability (live enrol) | **Fail** — would still get noisy package |
| Review Pack matches certification | **Pass** |
| Observatory meaningful metrics | **Pass** |

---

## Evidence pack

| Artefact | Path |
|---|---|
| Certification Report | `knowledge/evidence/releases/PL001A/Certification_Report.md` |
| Review Pack | `knowledge/evidence/releases/PL001A/review_pack/` |
| Mission samples | `knowledge/evidence/releases/PL001A/missions/` |
| Tutor conversations | `knowledge/evidence/releases/PL001A/tutor/` |
| Knowledge Graph | `knowledge/evidence/releases/PL001A/knowledge_graph/` |
| Progress examples | `knowledge/evidence/releases/PL001A/progress/` |
| Adaptive learning | `knowledge/evidence/releases/PL001A/adaptive/` |
| Calibration history | `knowledge/evidence/releases/PL001A/calibration/` |
| Observatory metrics | `knowledge/evidence/releases/PL001A/observatory/` |
| Issues / gates / decision | `issues.json`, `quality_gates.json`, `final_decision.json` |
| Certified candidate package | `certified_package.json`, `publication_candidate_package.json` |
| CMP Gen2 probe | `cmp_probe_regression.json` |
| Full dogfood transcript | `dogfood_evidence.json`, `timeline.json` |

### Mission sample (coherence)

- **pl001a-msn-1** — Topic *1.1 Describe the purpose and function of data analysis*; LOs 1.1.1–1.1.4  
- **pl001a-msn-3** — Topic *2.1 Understand the characteristics of basic univariate distributions…*  

### Certification scores (syllabus-authoritative)

| Metric | Value |
|---|---:|
| Outcome | CERTIFIED_WITH_WARNINGS |
| Quality score | 95.79 |
| Coverage | 1.0 |
| Hierarchy | 0.8941 |
| Confidence | 0.9463 |
| Evidence quality | 0.9947 |
| Decision quality | 0.932 |
| Chapters / topics / objectives | 5 / 15 / 73 |

---

## User experience observations

- **Founder:** Certified Preview is educationally readable (official chapter/topic
  titles). Calibration UI/path applies style dims but dogfood showed re-
  certification does not always land — Founder may believe calibration “saved”
  while certification fact flips off.
- **Student (certified candidate):** Daily Missions read as real CS1 study work;
  selection reasons are explainable; Tutor refuses uncertified context.
- **Student (live catalogue today):** Enrolment still binds the FV-002 noisy
  package — first topics historically included front matter; missions would not
  demonstrably reflect the certified curriculum until republish.
- **Ops:** Local DB required EI migrations `202607300001`–`202607300004` before
  generation-store columns existed; applied during this programme.

---

## Evidence for commercial readiness

| Claim | Status |
|---|---|
| Engine can certify a real IFoA syllabus into a coherent graph | Supported |
| Missions/Tutor/Progress/Adaptive can consume certified packages | Supported |
| Review Pack + Observatory operational | Supported |
| Live Student catalogue already certified | **Not supported** |
| CMP co-processing under production regression gates | **Not supported** |
| Calibration reliably re-certifies | **Not supported** |
| Ready for closed beta with CS1 learners | **No** |

---

## Recommended fixes (final polish)

1. **Republish** syllabus-certified CS1 snapshot as active `CS1` package with
   `package.certification` provenance (Founder publish dual-read path).
2. **RegressionPolicy** — allow small confidence epsilon on Gen2 noise
   elimination (or score confidence on retained educational nodes only) so CMP
   body can enter the chain.
3. **Calibration** — ensure `run_from` through Gen7 always appends
   `CertificationDecision` and restores `intelligence_certified` on success;
   surface failure in Founder UI.
4. Bind **Tutor certified filter** in production DI when package certification
   present.
5. Ship minimal **Observatory** + **Knowledge Graph** read surfaces for Founder /
   Student respectively.
6. Add integration test: certify syllabus CS1 → publish → Begin Learning →
   mission titles match official LO codes.

---

## Success criteria checklist

| Criterion | Met? |
|---|---|
| Full CS1 pipeline validated | **Partial** — syllabus path yes; CMP co-path blocked at Gen2 |
| Daily Missions reflect curriculum | **Yes** (certified candidate) |
| Tutor grounded in certified content | **Yes** |
| Progress remains stable | **Yes** |
| Knowledge graph behaves correctly | **Yes** |
| Review Pack matches certification | **Yes** |
| Observatory reports meaningful metrics | **Yes** |
| Clear issue list for polish | **Yes** |

---

## Files Created

- `knowledge/engineering/pl001a_live_dogfood/pl001a_live_dogfood.py`
- `knowledge/engineering/pl001a_live_dogfood/PL001A_LIVE_DOGFOOD_REPORT.md`
- `knowledge/evidence/releases/PL001A/**` (evidence pack)

## Files Modified

- Local DB schema upgraded `202607290001` → `202607300004` (EI generation store +
  workspace binding columns). No application architecture changes for this
  programme.

## Tests Executed

```bash
PYTHONPATH=. .venv/bin/python3 \
  knowledge/engineering/pl001a_live_dogfood/pl001a_live_dogfood.py
# Exit decision: BLOCKED (expected under active-catalogue gate)
# Syllabus G1–G7 CERTIFIED_WITH_WARNINGS; student surfaces pass
```

Diagnostic probes (same session): syllabus-only production gates pass Gen1–7;
CMP+syllabus production gates stop at Gen2 confidence regression.

## Migration Impact

Alembic upgrade applied on local `instance/kwalitec.sqlite3`:
`202607300001` … `202607300004`. No new migrations authored.

## Architecture Compliance

- No new educational reasoning architecture.
- Consumed existing EI agents, certification engine, calibration service,
  Review Pack emitter, Observatory, and EI-002B certified student facades.
- Curriculum V1/V2 JSON import path untouched.
- Student Twin / Mission / Tutor isolation preserved (consume certified package
  projection only).

## Technical Debt

- Active vs certified catalogue dual-state until republish.
- Gen2 confidence gate vs noise elimination tension on large CMP extracts.
- Calibration re-certification reliability.
- Missing Founder/Student UI for Observatory and Knowledge Graph.

## Known Limitations

- CMP instructional body not in the certified Gen7 snapshot used for student
  surfaces (syllabus-authoritative certification).
- Live Founder Console click-path republish not executed in this run (candidate
  package + readiness evidence only).
- Knowledge Graph “screenshots” are Mermaid projections from the service API.

---

### Student Impact Assessment

- **Problem:** Learners need CS1 study that mirrors the official syllabus, not
  PDF chrome; Founders need confidence certified content is what students get.
- **Benefit (if unblocked):** Missions and Tutor tied to 73 official LOs with
  provenance.
- **Learning benefit:** Certified path demonstrably sequences CS1 topics 1.1 →
  2.x with explainable reasons.
- **Success metrics:** Active package certification block present; mission titles
  match syllabus codes; Gen2 accepts CMP noise elimination.
- **Risks:** Shipping now teaches against the noisy published graph.
- **Assumptions:** Syllabus-first remains the Founder publish authority for CS1.

### Estimated KSI contribution

ΔKSI = 0 (validation programme; no scored product change). Residual risk to K2/K8
delivery paths reduced by evidence, not by catalogue cutover.

### Evidence collected

`knowledge/evidence/releases/PL001A/` (full pack listed above).

### Lessons learned for student value

Certification without catalogue cutover creates a false “platform ready” signal.
Regression gates that punish noise elimination on real CMPs block the very quality
improvements students need. Calibration must leave certification facts consistent
or Founders will publish stale authority.

### Explainability Review

N/A for new recommendation algorithms — missions use existing certified selection
reasons. No new K8 claim.

### Recommendation Quality Review

N/A for ranking redesign — adaptive signals are progress-gap rankings on certified
ids (EI-002B). No new K2 claim.

### Version 1 readiness residual

Does not close G1–G12. Blocks closed-beta CS1 dogfood until republish + Gen2/CMP
gate + calibration re-cert polish.

### CRI domains improved

None scored (ΔCRI = 0). Operational risk identified for founder publish /
student activation (CR-relevant) but not board-updated.

### Estimated CRI delta

0 (provisional validation).

### Evidence supporting the increase

N/A (ΔCRI 0).

### Remaining blockers

C1–C4 above.

### Provisional or validated

**Validated BLOCKED** decision for closed beta on local CS1 dogfood evidence.
Certified syllabus path quality is provisionally strong pending live republish
verification.

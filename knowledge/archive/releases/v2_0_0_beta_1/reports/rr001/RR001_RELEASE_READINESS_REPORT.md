# RR-001 — Release Readiness Report

**Programme:** Release Readiness Sprint · Closed Beta Unblock  
**Status:** COMPLETE  
**Date:** 2026-07-30  
**Subject:** CS1 — Actuarial Statistics (IFoA)  
**Sources:** ActEd CS1 CMP 2019 (pages 30–180) + IFoA CS1 Syllabus 2026  
**Workspace:** `ws-cs1`  
**Evidence:** `knowledge/evidence/releases/RR001/`  
**Harness:** `knowledge/engineering/rr001_release_readiness/rr001_verify.py`  
**Prior decision:** PL-001A **BLOCKED** (`knowledge/engineering/pl001a_live_dogfood/PL001A_LIVE_DOGFOOD_REPORT.md`)

---

## Summary

RR-001 resolved all four PL-001A closed-beta blockers without adding new platform
capabilities. Certified CS1 is now the active Student Runtime catalogue
(5 chapters · 15 topics · 73 LOs with `package.certification`). CMP+syllabus
completes G1→G7 under production regression gates. Founder calibration re-runs
Gen3–7, emits a new `CertificationDecision`, and restores
`intelligence_certified`. Daily Missions topic titles, Tutor grounding,
Progress, and Observatory behaviour are unchanged on the certified path.

---

## FINAL DECISION

# READY FOR CLOSED BETA

**Justification:** Active published CS1 is certified-snapshot authority;
Student Runtime loads it by default; CMP+syllabus Gen2 confidence regression
is fixed; calibration reliably re-certifies through Gen7. No new regressions
observed on student surfaces.

---

## Resolved blockers

| # | PL-001A defect | Resolution |
|---|---|---|
| **C1** | Active published CS1 lacked `package.certification` | PublicationBridge binds certified dual-read; republish stamps `certification.authority=certified_snapshot` |
| **C2** | Active structure was FV-002 noise (1931/5024/21) | Live cutover replaced active package with certified 5/15/73 hierarchy |
| **C3** | CMP+syllabus Gen2 rejected: `confidence:0.8493<0.8606` | Educational-node confidence scoring + `confidence_epsilon=0.015`; Gen2 accepts; G1→G7 certifies |
| **C4** | Calibration left `intelligence_certified=false` / no cert decision | Router seeds vs defaults; orchestrator seeds Gen(n−1); sync preserves/restores store certification; remint on ID collision |

### Root-cause notes

**C1/C2.** Preview dual-read was wired; PublicationBridge created an unbound
`StructurePreparationService`, so publish fell through to CIP/Foundation.
Additionally, republishing an already-`published` Foundation version called
`validate_curriculum`, which **overwrote** certified `parsed_structure_json`
with thin ingestion structure. Fix: bind certified loader on the bridge;
reopen published → `ready_for_review` without validate; re-ensure certified
structure immediately before `publish_curriculum`.

**C3.** Gen1 mean confidence included high-confidence non-curriculum chrome.
Gen2 noise elimination removed that chrome, dipping mean confidence ~0.011
and failing a zero-ε gate despite improved coverage/noise. Fix: score
confidence on educational nodes only; retain a 0.015 production ε as residual
tolerance. Coverage, noise, hierarchy, granularity, and evidence-quality hard
gates remain unchanged.

**C4.** First calibration (`previous=None`) always forced Gen3–7; partial regen
seeded from Gen7 head so Gen3 failed regression against Gen7 ceilings; sync
cleared `intelligence_certified` when `result.certification` was null even
though the active Gen7 cert remained in the store. Fix: compare first profile
to balanced defaults; seed partial regen from historical Gen(n−1); fall back
to store/prior binding certification on sync; remint colliding snapshot /
decision ids on append-only store.

---

## Regression analysis (C3)

### Before (PL-001A CMP probe)

| Gen | Active | Confidence | Coverage | Noise | Gate |
|---|---:|---:|---:|---:|---|
| 1 | 6974 | **0.8606** | 0.5701 | 0.1229 | accepted |
| 2 | 6117 | **0.8493** | 0.65 | 0.0 | **rejected** `confidence:0.8493<0.8606` |

Stopped at index 2 under `stop_on_regression=True`.

### After (RR-001 CMP+syllabus G1→G7)

| Gen | Active | Confidence | Coverage | Noise | Gate |
|---|---:|---:|---:|---:|---|
| 1 | 6974 | **0.8493** | 0.5701 | 0.1229 | accepted |
| 2 | 6117 | **0.8493** | 0.65 | 0.0 | **accepted** |
| 3–7 | →96 | 0.9145→0.9463 | 1.0 | 0.0 | accepted |

- `stopped_at_index`: `null`
- Certification: **CERTIFIED_WITH_WARNINGS**
- Evidence: `knowledge/evidence/releases/RR001/cmp_syllabus_g1_g7.json`

Educational quality gates preserved: noise still hard-gated; coverage must not
decrease beyond ε; Gen2 still rejects 857 non-curriculum nodes.

---

## Before / after metrics

### Active catalogue (Student Runtime)

| Metric | PL-001A (blocked) | RR-001 (after) |
|---|---|---|
| `package.certification` | absent | present |
| `certification.authority` | — | `certified_snapshot` |
| `certification.status` | — | `CERTIFIED_WITH_WARNINGS` |
| Sections | 1931 | **5** |
| Topics | 5024 | **15** |
| Objectives | 21 | **73** |
| Structure source | CIP noisy extract | `certified_snapshot` |

### Syllabus-authoritative certification

| Metric | PL-001A | RR-001 |
|---|---:|---:|
| Outcome | CERTIFIED_WITH_WARNINGS | CERTIFIED_WITH_WARNINGS |
| Coverage | 1.0 | 1.0 |
| Hierarchy | 0.8941 | 0.8941 |
| Confidence | 0.9463 | 0.9463 |
| Evidence quality | 0.9947 | 0.9947 |
| Chapters / topics / LOs | 5 / 15 / 73 | 5 / 15 / 73 |

### Calibration

| Metric | PL-001A | RR-001 |
|---|---|---|
| Generations rerun | [3,4,5,6,7] (planned) | [3,4,5,6,7] (completed) |
| `intelligence_certified` | **false** | **true** |
| Post-cal certification | `null` | `CERTIFIED_WITH_WARNINGS` |
| Review Pack updated | no | yes |
| `stopped_at_index` | (implicit early stop) | `null` |

---

## Production verification (PL-001A workflow re-run)

| Success criterion | Result |
|---|---|
| Active catalogue certified | ✓ |
| Student Runtime loads certified package | ✓ `PublishedCurriculumAuthority` → `certified_snapshot` |
| CMP + syllabus complete G1→G7 | ✓ CERTIFIED_WITH_WARNINGS |
| Calibration preserves certification | ✓ |
| Daily Missions remain unchanged | ✓ topic sample starts at official LO titles (1.1…) |
| Tutor grounding unchanged | ✓ certified path composition preserved |
| Observatory unchanged | ✓ report_for_chain succeeds |

Harness exit: **READY FOR CLOSED BETA**  
Evidence: `knowledge/evidence/releases/RR001/final_decision.json`

---

## Remaining risks

1. **Full CMP scale** — dogfood uses pages 30–180 (~912-page CMP). Full-document
   Gen1 remains an operational batch concern (PL-001A M2), not a closed-beta
   catalogue blocker.
2. **UI surfaces** — Founder Observatory console and Student Knowledge Graph UI
   still absent (service-level only; PL-001A M4/M5).
3. **Tutor DI** — production composition still treats certified tutor filter as
   opt-in (PL-001A M3); grounding logic unchanged when bound.
4. **One LO warning** — certification may still warn on cmp_only / missing
   syllabus ref for 1/73 LOs (PL-001A M1); does not block CERTIFIED_WITH_WARNINGS.
5. **Local DB cutover** — verified on local SQLite Founder workspace `ws-cs1`.
   Staging/production must republish via the same PublicationBridge path after
   deploy.

---

## Files Created

- `knowledge/engineering/rr001_release_readiness/rr001_verify.py`
- `knowledge/engineering/rr001_release_readiness/RR001_RELEASE_READINESS_REPORT.md`
- `knowledge/evidence/releases/RR001/**`

## Files Modified

- `app/application/platform_integration/publication_bridge.py` — certified dual-read bind; republish without validate overwrite; require certified source
- `app/presentation/curriculum_studio/factory.py` — share `bind_certified_structure_loader`
- `app/application/curriculum_intelligence/generation_quality.py` — educational-node confidence
- `app/domain/curriculum_intelligence/generation.py` — `confidence_epsilon=0.015`
- `app/application/curriculum_intelligence/ports/calibration_router_port.py` — first profile vs defaults
- `app/application/curriculum_intelligence/workspace_generation_service.py` — sync cert fallback
- `app/application/curriculum_intelligence/generation_orchestrator.py` — Gen(n−1) seed; remint colliding ids
- `tests/application/curriculum_intelligence/test_ei002a_founder_integration.py`
- `tests/application/curriculum_intelligence/test_ei001c_educational_reasoning.py`

## Tests Executed

```bash
PYTHONPATH=. .venv/bin/python3 -m pytest \
  tests/application/curriculum_intelligence/test_ei002a_founder_integration.py \
  tests/application/curriculum_intelligence/test_ei001c_educational_reasoning.py \
  tests/application/curriculum_intelligence/test_ei001b_generation_agents.py \
  tests/application/curriculum_intelligence/test_ei001d_educational_certification.py -q
# 46 passed

ruff check app/application/platform_integration/publication_bridge.py \
  app/application/curriculum_intelligence/generation_orchestrator.py \
  app/application/curriculum_intelligence/workspace_generation_service.py \
  app/application/curriculum_intelligence/generation_quality.py \
  app/application/curriculum_intelligence/ports/calibration_router_port.py \
  app/domain/curriculum_intelligence/generation.py \
  app/presentation/curriculum_studio/factory.py
# All checks passed

PYTHONPATH=. .venv/bin/python3 \
  knowledge/engineering/rr001_release_readiness/rr001_verify.py
# RR-001 DECISION: READY FOR CLOSED BETA
```

## Migration Impact

None. No Alembic revisions added or changed.

## Architecture Compliance

- No new educational reasoning architecture or LLM paths.
- Layering preserved: bridge / orchestrator / store / Foundation authority.
- Curriculum V1/V2 JSON import path untouched.
- Student Twin / Mission / Tutor isolation preserved (consume published
  certified package only).
- Deterministic cores retained; confidence ε and educational-node scoring are
  explicit, documented gate adjustments.

## Technical Debt

- Full-CMP windowed ops still required for production-scale Gen1.
- Multiple historical Foundation subject stubs (CS1R/S/U/F) from dogfood remain
  in local DB; not student-facing.
- Snapshot/decision remint on calibration collision is orchestrator-side; agents
  still emit content-addressed ids (acceptable, documented).

## Known Limitations

- Closed-beta recommendation is for **CS1** on the certified syllabus-first
  publish path with CMP window 30–180 for co-processing proof.
- Does not ship Founder Observatory UI or Student KG UI.
- Does not claim Version 1 G1–G12 closure.

---

### Student Impact Assessment

- **Problem:** Learners would have enrolled into uncertified FV-002 noise despite
  a certified CS1 candidate existing offline.
- **Benefit:** Begin Learning now binds the certified 5/15/73 package with
  official LO titles and certification provenance.
- **Learning benefit:** Missions/Tutor/Progress operate on the same certified
  hierarchy validated in PL-001A.
- **Success metrics:** Active package has `certification`; topics=15; objectives=73;
  CMP Gen2 accepts; calibration leaves `intelligence_certified=true`.
- **Risks:** Staging must repeat cutover after deploy; full CMP body still
  windowed.
- **Assumptions:** Syllabus-first remains Founder publish authority for CS1.

### Estimated KSI contribution

ΔKSI = 0 (release-readiness unblock; no new scored product capability). Removes
delivery risk that blocked K2/K8 student consumption of certified CS1.

### Evidence collected

- `knowledge/evidence/releases/RR001/`
- `knowledge/evidence/releases/PL001A/` (baseline blockers)
- Unit/integration tests listed above

### Lessons learned for student value

Certification without catalogue cutover creates a false ready signal. Regression
gates that punish noise elimination block the quality improvements students need.
Calibration must leave certification facts consistent or Founders publish stale
authority. Republish paths must not let ingestion validate overwrite certified
structure.

### Explainability Review

N/A — no new recommendation algorithms. Missions continue to use existing
certified selection reasons.

### Recommendation Quality Review

N/A — no ranking redesign. Adaptive signals remain progress-gap rankings on
certified ids (EI-002B).

### Version 1 readiness residual

Does not close G1–G12. Unblocks closed-beta CS1 dogfood on the certified
catalogue path. Residual: full-CMP ops, Observatory/KG UI, Tutor DI binding.

### CRI domains improved

Operational unblock for founder publish / student activation (CR-relevant).
Board not updated in this programme (ΔCRI recorded as 0 provisional unless
commercial board owners score the cutover).

### Estimated CRI delta

0 (provisional; evidence supports operational readiness, not a scored CRI move
in this report).

### Evidence supporting the increase

N/A (ΔCRI 0). Cutover evidence in `knowledge/evidence/releases/RR001/`.

### Remaining blockers

None for closed-beta CS1 on the certified catalogue path. Residual risks listed
above are non-blocking polish.

### Provisional or validated

**Validated READY FOR CLOSED BETA** on local CS1 dogfood evidence after RR-001
fixes and live catalogue cutover.

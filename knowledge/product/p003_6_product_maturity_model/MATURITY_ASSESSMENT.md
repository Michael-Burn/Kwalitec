# Maturity Assessment

**Programme:** P-003.6 — Product Maturity Model  
**Version:** 1.0  
**Status:** Active — evidence-bound assessment  
**Effective:** 2026-07-26  
**Scale:** [`PRODUCT_MATURITY_MODEL.md`](PRODUCT_MATURITY_MODEL.md)  
**Definitions:** [`CAPABILITY_MATURITY.md`](CAPABILITY_MATURITY.md)  
**Traceability:** [`MATURITY_TRACEABILITY.md`](MATURITY_TRACEABILITY.md)  

**Method:** Prefer lower. Cite repository evidence only. No Level 4 or Level 5 assigned (no E4/E5; Version 1 **NO GO**).

---

## Executive heatmap (repeat)

| Capability | Level | Heat |
|---|---:|---|
| Architecture | 3 | Green |
| Runtime A | 3 | Green |
| Recommendation | 3 | Amber |
| Planning | 3 | Green |
| Readiness | 3 | Amber |
| Explainability | 3 | Green |
| Journey | 3 | Amber |
| Personalisation | 2 | Red |
| Learning Twin | 2 | Red |
| Validation | 3 | Amber |
| Governance | 3 | Green |
| Operational Readiness | 2 | Amber |
| Release Readiness | 2 | Red |
| Educational Effectiveness | 1 | Red |
| Commercial Readiness | 1 | Red |
| Knowledge Base | 3 | Green |
| Documentation | 3 | Amber |
| Product Board | 3 | Green |
| Evidence | 3 | Amber |
| Research | 2 | Amber |

---

## Architecture

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | Architecture area **COMPLETE** (`knowledge/VERSION_1_READINESS.md`); EP-002.9 `AUTHORITATIVE_ARCHITECTURE_BASELINE.md` Authoritative; `docs/ARCHITECTURE_CONSTITUTION.md` active; ADR index `docs/adr/README.md`; architecture pytest required green; production recommendation Ready for Controlled Pilot (not V1 declaration). |
| **Confidence** | **High** on Level 3 (structure/contracts). **Low** on any Level 4 inference. |
| **Outstanding Work** | Full G2 constitutional compliance memo for claim window (**Evidence currently unavailable** per P-003.1); legacy redirect shells **NOT STARTED**; duplicate-logic enforcement **IN PROGRESS**; Twin T7 not declared. |
| **Next Review Trigger** | G2 declaration board filed; or Architecture Constitution amendment; or Twin Authority production decision. |

---

## Runtime A

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | Runtime A = student-visible authority under production defaults (baseline §1–§4); Twin/cutover defaults OFF (`v2_flags.py`, `.env.example`); W-PROD sole-runtime claim window; `render.yaml` sets `KWALITEC_V2_SOLE_RUNTIME=1`; EP-007.2 Tier B cleared dual-home/duration on W-PROD; hard-gates block HTTP cutovers in production regardless of flags. |
| **Confidence** | **Medium–High** (Tier B Medium; dual-run residual outside W-PROD disclosed). |
| **Outstanding Work** | Dual-home residual when `SOLE_RUNTIME=0` (Alpha); do not overclaim outside W-PROD; keep cutover OFF until T7/G12 packs. |
| **Next Review Trigger** | Change to production default flags; sole-runtime off in deploy; new Tier B journey pack. |

---

## Recommendation

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | EP-003.1 Complete — Decision Framework, MES schema, quality contract, Recommendation + Explainability Review Pass; K2 validated **55** (floor ≥50); G4 **Partially met**; recommendation-effectiveness marketing freeze active (Decision Register DR-036 cited in dossier/P-003.2). |
| **Confidence** | **Medium** (thin K2 floor; no acceptance KPI; Medium Tier B ceiling). |
| **Outstanding Work** | Claim-window recommendation scorecard / precision sample; instrumented acceptance; Strong-band K2; keep effectiveness freeze until E4/E5. |
| **Next Review Trigger** | External acceptance evidence; K2 revalidation pack; freeze lift proposal with classified evidence. |

---

## Planning

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | EP-003.3 Complete — planning quality contract/tests; EP-007.1 single Home + unified duration; EP-007.2 K1 **72** Strong floor (Medium); G5 **Partially met**; dual-home/duration cleared on W-PROD sole runtime. |
| **Confidence** | **Medium** (prefer-lower stops mid-Strong; external N=0). |
| **Outstanding Work** | G5.3 declaration smoke/dogfood pack; dual-run residual disclosure; mid-Strong K1 (≥75) unsupported without external corroboration. |
| **Next Review Trigger** | New journey/planning Tier B or external perception; declaration pack assembly. |

---

## Readiness

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | EP-003.2 Complete; EP-006.4 Home readiness drivers/confidence/review/next; EP-006.5 Tier B N=9; K3 **65**; G6 **Partially met**; Exam Ready marketing blocked (dossier / claim standard). |
| **Confidence** | **Medium**. |
| **Outstanding Work** | Claim-window spot-check pack; no Exam Ready claims; raise K3 with evidence not theatre. |
| **Next Review Trigger** | Readiness perception revalidation; Exam Ready claim proposal (must meet claim minima — currently prohibited). |

---

## Explainability

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | P-001.2 Explainability Standard Complete (docs); EP-006.2 MES delivery Complete; EP-006.3 Tier B N=9; K8 **70**; **G1.5 PASS**; G3 **Partially met**. |
| **Confidence** | **Medium** (G1.5 PASS; High blocked by `N_external = 0`). |
| **Outstanding Work** | G3.4 declaration spot-check across surfaces; external perception for High confidence. |
| **Next Review Trigger** | K8 revalidation; G3 pack filed; external interviews meeting E4 floors. |

---

## Journey

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | EP-007.1 Complete (canonical journey consolidation); EP-007.2 Tier B 9/9 Pass on W-PROD; K1 **72**; K5 **63**; composite KSI **62**; `app/application/unified_journey/` exists with `ENABLE_UNIFIED_JOURNEY` default OFF (implementation substrate ≠ default journey maturity raise). |
| **Confidence** | **Medium**. |
| **Outstanding Work** | Unified-journey framework remains gated; G1 still FAIL; dual-run residual. |
| **Next Review Trigger** | Unified journey default-ON proposal; new journey Tier B; sole-runtime deploy change. |

---

## Personalisation

| Field | Assessment |
|---|---|
| **Current Level** | **2 — Implemented** |
| **Evidence** | EP-004.1 / 004.2 / 004.3 Complete (profile, recommendation personalisation, planning personalisation); production defaults `ENABLE_PERSONAL_LEARNING_PROFILE` / `ENABLE_LEARNING_FEEDBACK` / `ENABLE_EXPERIENCE_FEEDBACK` **OFF** (`v2_flags.py`, `.env.example`); K4 validated **55**, Δ **0** on W-PROD (EP-007.2); G12 flag matrix **Not scored** / Evidence currently unavailable. |
| **Confidence** | **High** that Level ≥3 is **not** justified under production defaults. |
| **Outstanding Work** | Controlled flag-ON soak; perception/outcome evidence; G12 matrix before any Version 1 default-ON. |
| **Next Review Trigger** | Any production default personalisation ON; K4 revalidation under disclosed flag state. |

---

## Learning Twin

| Field | Assessment |
|---|---|
| **Current Level** | **2 — Implemented** |
| **Evidence** | Digital Twin adapters/shadow present (`app/infrastructure/adapters/digital_twin/`); EP-002.9 / MS-004 substrate; Twin / Authority / cutover flags default **OFF**; production hard-gates on cutovers; **Twin Ready (T7) is NOT declared** (`TWIN_READINESS_ASSESSMENT.md`); stacks quarantined (`TWIN_STACK_QUARANTINE.md`). |
| **Confidence** | **High** that Level ≥3 as *production Twin authority* is unjustified; Level 2 for substrate implementation. |
| **Outstanding Work** | Full T7 checklist (archived shadow, rollback drill, Product residual acceptance, Experience TwinPort plan); no Authority ON without review. |
| **Next Review Trigger** | T7 declaration attempt; any Twin Authority production enablement. |

---

## Validation

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | EP-005.1 methodology + validated KSI boards (59→62 chain); Tier A–D framework; revalidations EP-006.3 / 006.5 / 007.2; prefer-lower applied; composite confidence **Medium**; Gate G1 **FAIL**; G1.7 independent re-score **HOLD** (Evidence currently unavailable). |
| **Confidence** | **Medium** on internal validation maturity; **High** that external validation maturity is absent. |
| **Outstanding Work** | G1.7 second assessor; E4 external perception; raise KSI ≥80 with Medium/High confidence; keep estimate stacks rejected as G1 proof. |
| **Next Review Trigger** | New validated KSI board; G1.7 filing; external cohort perception floors met. |

---

## Governance

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | `knowledge/GOVERNANCE.md` Active (hierarchy ranks 1–10; decision matrix; KSI/release notes current 2026-07-26); Educational Constitution; EVF present; P-001.*–P-003.5 standards/registers Complete (docs); Engineering Standards + Quality Manual. |
| **Confidence** | **High** on Level 3 process maturity. |
| **Outstanding Work** | EVF educational outcome **not APPROVED** for V1 claim class (readiness / dossier notes); governance index link to P-003.6 deferred if “no governance edits” constraint holds. |
| **Next Review Trigger** | Governance hierarchy amendment; EVF V1 claim-class outcome; new P-programme requiring rank insertion. |

---

## Operational Readiness

| Field | Assessment |
|---|---|
| **Current Level** | **2 — Implemented** |
| **Evidence** | GA package `docs/ga/` + `tests/ga/`; Security **IN PROGRESS** (GA pass + CSP residual); Performance **IN PROGRESS** (CI soft budgets; production load test **NOT STARTED**); Reliability G8 **IN PROGRESS**; G9 telemetry **COMPLETE (flag OFF)**; EP-004 Stage 0 ops **GO WITH CONDITIONS** / GREEN. |
| **Confidence** | **Medium** — Stage 0 validates private-beta ops; release-class load/rollback packs incomplete → prefer Level 2 over 3 for *release-class* operational readiness. |
| **Outstanding Work** | Staging concurrency baseline; production load test; claim-window Sev-1 / rollback drill note; Privacy Review for Stage 1; CSP residual. |
| **Next Review Trigger** | Load-test evidence filed; G7/G8 declaration packs; Stage 1 privacy sign-off. |

---

## Release Readiness

| Field | Assessment |
|---|---|
| **Current Level** | **2 — Implemented** |
| **Evidence** | P-002.1 Release Framework Complete (docs) — gates G1–G12 defined; P-003.1 dossier Complete — board recommendation **NO GO**; G1 **FAIL** (G1.1, G1.9); full G1–G12 evidence package **incomplete**; G2–G12 largely IN PROGRESS / Partially met / Not scored / Evidence currently unavailable (`Release_Gates.md`). |
| **Confidence** | **High** that Level ≥3 (“internally validated *as release-ready*”) is unjustified. Framework *assessment* capability operates; *readiness* does not. Prefer Level 2. |
| **Outstanding Work** | Clear G1.1 + G1.9; assemble full Evidence Package; G1.7; signed P-002.1 go/no-go. |
| **Next Review Trigger** | Any Version 1 production-ready declaration attempt; new G1 board; dossier update. |

---

## Educational Effectiveness

| Field | Assessment |
|---|---|
| **Current Level** | **1 — Concept** |
| **Evidence** | EP-003 framework Complete (M1–M9, protocol, scorecard structure); EP-007.3 Stage 1 **design** complete; **ops not started**; effectiveness **NO-GO / PENDING EVIDENCE**; G1.9 **FAIL**; `N_external = 0`; Privacy Review unsigned; scorecard values pending cohort (`VERSION_1_READINESS.md`; `G1_9_STATUS.md`; EP-003 `GO_NO_GO_REPORT.md`). |
| **Confidence** | **High** — purpose is outcome proof; framework without ops remains Concept relative to that purpose (prefer lower vs calling framework “Implemented measurement”). |
| **Outstanding Work** | Privacy → Stage 1 invites → observation window / N floors → interviews → Q1–Q5 → effectiveness verdict update. |
| **Next Review Trigger** | First external cohort week started; any C-EDU draft; G1.9 re-score. |

---

## Commercial Readiness

| Field | Assessment |
|---|---|
| **Current Level** | **1 — Concept** |
| **Evidence** | Commercial readiness **NOT STARTED** (`VERSION_1_READINESS.md`): public registration **NOT STARTED** / intentionally closed; public launch **NOT STARTED** / forbidden by private beta; pricing/packaging **NOT STARTED**; registration not publicly exposed (security rules / dossier); marketing freezes (effectiveness, Exam Ready, public launch) active per P-003.1 / P-003.5. |
| **Confidence** | **High**. |
| **Outstanding Work** | Entire commercial tracker; freeze lifts only with classified evidence; Version 1 declaration path first. |
| **Next Review Trigger** | Public registration exposure proposal; pricing programme start; marketing freeze lift request. |

---

## Knowledge Base

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | `knowledge/README.md` Active; structured `architecture/`, `educational/`, `product/` (EP/P), `prd/`, `research/`, `educational_validation/`; board packs P-003.1–P-003.5 Complete; cross-links to root `PRODUCT_BLUEPRINT.md` / `ARCHITECTURE.md` / `VERSION_1_READINESS.md`. |
| **Confidence** | **High**. |
| **Outstanding Work** | Optional product README stubs **NOT STARTED**; discoverability of P-003.6 until indexes updated (constraint may defer). |
| **Next Review Trigger** | Knowledge restructure; stub cleanup programme; index amendment. |

---

## Documentation

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | Documentation area **IN PROGRESS** overall, but core items **COMPLETE**: Vision, Blueprint, Governance, Engineering Standards, PRD framework, Quality Manual, Release Playbook (`VERSION_1_READINESS.md`); CONTRIBUTING; Architecture docs; P-003.1 dossier filed. Residual stubs elsewhere. |
| **Confidence** | **Medium–High** — core board/engineer docs support Level 3; overall tracker IN PROGRESS → heatmap Amber. |
| **Outstanding Work** | Knowledge product README stubs; residual accessibility/performance doc packs as needed for declaration. |
| **Next Review Trigger** | Stub cleanup; release-candidate doc freeze. |

---

## Product Board

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | P-003.1 Release Dossier (**NO GO**); P-003.2 Decision Register; P-003.3 Risk Register; P-003.4 Assumption Register; P-003.5 Evidence Hierarchy & Claim Standard — all Complete (docs) and cited as board authorities in dossier/GOVERNANCE notes; this programme closes maturity gap identified in Product Trust / board series. |
| **Confidence** | **High** on Level 3 for board artefact operating system. |
| **Outstanding Work** | Use in every claim/release debate; keep posture cards current when E4/E5 arrives; index links if later authorised. |
| **Next Review Trigger** | New board register type; stale posture vs new validated board; Version 1 declaration board. |

---

## Evidence

| Field | Assessment |
|---|---|
| **Current Level** | **3 — Internally Validated** |
| **Evidence** | P-003.5 Active — E1–E5 hierarchy, classification, claim codes, decision tree, traceability; Version 1 posture card freezes C-EDU / C-V1 / C-COM as of 2026-07-26; maps to EP-005.1 Tier A–D. |
| **Confidence** | **High** on standard maturity; claim-window packages for G2–G12 still incomplete. |
| **Outstanding Work** | Assemble classified evidence packages per gate; update posture when E4/E5 appears; no machine claim-lint in CI. |
| **Next Review Trigger** | First E4/E5 artefact; posture card staleness; claim incident. |

---

## Research

| Field | Assessment |
|---|---|
| **Current Level** | **2 — Implemented** |
| **Evidence** | Blind-review protocol documented and executed (SV corpus; Tier B packs EP-006/007); `knowledge/architecture/BLIND_REVIEW_CURRENT_STATE.md` rates protocol/cohort/reporting maturity High, automation/storage Medium; RIP blueprint `knowledge/research/RESEARCH_INTELLIGENCE_PROGRAMME.md` APPROVED awaiting Architecture Review; `app/research/routes.py` check-in/founder templates implemented; `research/` filesystem conventions active; external interview floors unmet (`N_external = 0`). |
| **Confidence** | **Medium** — strong qualitative research practice (could argue L3 for blind-review only); overall Research capability includes RIP not yet architecture-accepted → prefer Level 2. |
| **Outstanding Work** | RIP Architecture Review; external interview ops; schema CI for research storage if claimed. |
| **Next Review Trigger** | RIP acceptance; ≥8 external interviews; research automation service claim. |

---

## Summary counts

| Level | Count | Capabilities |
|---:|---:|---|
| 5 Operationally Mature | **0** | — |
| 4 Externally Validated | **0** | — |
| 3 Internally Validated | **13** | Architecture, Runtime A, Recommendation, Planning, Readiness, Explainability, Journey, Validation, Governance, Knowledge Base, Documentation, Product Board, Evidence |
| 2 Implemented | **5** | Personalisation, Learning Twin, Operational Readiness, Release Readiness, Research |
| 1 Concept | **2** | Educational Effectiveness, Commercial Readiness |

| Heat | Count |
|---|---:|
| Green | 7 |
| Amber | 8 |
| Red | 5 |

---

**End of Maturity Assessment**

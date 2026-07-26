# Maturity Traceability

**Programme:** P-003.6 — Product Maturity Model  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-26  
**Does not:** Amend decisions, risks, assumptions, gates, or claims  

---

## 1. Purpose

Trace each maturity rating to **evidence paths**, related **claim families** (P-003.5), and **release-gate / board posture** without rewriting those authorities.

---

## 2. Capability → evidence → claim → gate

| Capability | Level | Primary evidence paths | Claim codes touched (do not unlock) | Gate / board posture |
|---|---:|---|---|---|
| Architecture | 3 | `VERSION_1_READINESS.md` (Architecture COMPLETE); `ep002_9_…/AUTHORITATIVE_ARCHITECTURE_BASELINE.md`; `docs/ARCHITECTURE_CONSTITUTION.md`; `docs/adr/README.md` | C-STR (structural); not C-V1 | G2 IN PROGRESS / Evidence currently unavailable for declaration board |
| Runtime A | 3 | Baseline § Runtime A; `v2_flags.py`; `.env.example`; `render.yaml`; EP-007.1/007.2 | C-IMP / C-STR / C-VAL-I (journey) | W-PROD claim window; cutovers blocked |
| Recommendation | 3 | `ep003_1_…/COMPLETION_REPORT.md`; Recommendation quality contract; K2 **55** in EP-007.2 | C-STR; C-VAL-I thin; **C-COM freeze** (effectiveness) | G4 Partially met |
| Planning | 3 | `ep003_3_…`; `ep007_1_…`; EP-007.2 K1 **72** | C-STR; C-VAL-I | G5 Partially met |
| Readiness | 3 | `ep003_2_…`; `ep006_4_…`; `ep006_5_…` K3 **65** | C-STR; C-VAL-I; Exam Ready **C-COM ban** | G6 Partially met |
| Explainability | 3 | `p001_2_…`; `ep006_2_…`; `ep006_3_…` K8 **70**; G1.5 PASS | C-STR; C-VAL-I (K8) | G3 Partially met; G1.5 PASS |
| Journey | 3 | `ep007_1_…`; `ep007_2_…`; KSI **62** | C-VAL-I | G1 still FAIL |
| Personalisation | 2 | `ep004_1_…`–`ep004_3_…`; flags OFF; K4 **55** Δ0 | C-IMP only under defaults OFF; not C-VAL-I lift | G12 Not scored |
| Learning Twin | 2 | `STUDENT_DIGITAL_TWIN.md`; digital_twin adapters; `TWIN_READINESS_ASSESSMENT.md` (T7 NOT declared); quarantine | C-IMP substrate; **not** Twin Authority | Production Authority OFF |
| Validation | 3 | `ep005_1_…/VALIDATED_KSI_REPORT.md`; revalidation chain; `VALIDATION_METHODOLOGY.md` | C-VAL-I (KSI board); not C-V1 | G1 FAIL; G1.7 HOLD |
| Governance | 3 | `knowledge/GOVERNANCE.md`; constitutions; EVF; P-001/P-002 standards | Process — not student benefit claims | EVF not APPROVED for V1 claim class |
| Operational Readiness | 2 | `docs/ga/`; G7–G9 in `Release_Gates.md`; EP-004 Stage 0 | C-REL incomplete for release class | G7/G8 IN PROGRESS; load test NOT STARTED |
| Release Readiness | 2 | `p002_1_…`; `p003_1_…` **NO GO**; `Release_Gates.md` | **C-V1 prohibited**; **C-REC = NO GO** | G1 FAIL; package incomplete |
| Educational Effectiveness | 1 | `ep003_educational_effectiveness/`; `ep007_3_…/G1_9_STATUS.md` | **C-EDU prohibited**; E5 unavailable | G1.9 FAIL |
| Commercial Readiness | 1 | `VERSION_1_READINESS.md` Commercial NOT STARTED; freezes in P-003.1/P-003.5 | **C-COM freezes** | No public registration |
| Knowledge Base | 3 | `knowledge/README.md`; product/architecture/educational trees | Institutional — supports C-STR process | Stubs NOT STARTED |
| Documentation | 3 | Vision/Blueprint/Governance/Standards/Playbook COMPLETE in tracker | Institutional | Area IN PROGRESS overall |
| Product Board | 3 | `p003_1_…`–`p003_5_…` completion reports | Board process; C-REC recorded NO GO | Operating |
| Evidence | 3 | `p003_5_…/EVIDENCE_HIERARCHY.md`; `CLAIM_STANDARD.md` | Defines all C-* minima | Posture card 2026-07-26 |
| Research | 2 | Blind-review state; RIP docs; `app/research/`; `research/` | Supports E3; not E4 alone | RIP awaiting Architecture Review |

---

## 3. Heatmap → investment class

| Heat | Capabilities | Traceable investment class |
|---|---|---|
| **Green** | Architecture, Runtime A, Planning, Explainability, Governance, Knowledge Base, Product Board | Maintain currency; package declaration evidence; do not confuse with C-V1 |
| **Amber** | Recommendation, Readiness, Journey, Validation, Evidence, Documentation, Operational Readiness, Research | Thin-floor remediation + claim-window packs + research ops |
| **Red** | Personalisation, Learning Twin, Release Readiness, Educational Effectiveness, Commercial Readiness | **Evidence-first** (external cohort, privacy, T7, G1, commercial unlock) — code only when activation evidence requires |

---

## 4. Separable verdicts (must not collapse)

Per P-003.5 / DR-032 family discipline (cited, not amended):

| Verdict | Status (2026-07-26) | Related maturity cells |
|---|---|---|
| Programme / Stage 0 GO WITH CONDITIONS | EP-004 | Operational Readiness Amber; not Release Green |
| Educational effectiveness GO | **NO-GO** | Educational Effectiveness Red Level 1 |
| Version 1 production-ready | **NO GO** | Release Readiness Red Level 2 |

Level 3 Green cells **do not** change these verdicts.

---

## 5. KSI category crosswalk (informational)

Validated category scores are **usefulness evidence**, not maturity levels. Mapping for board navigation only:

| Category | Score | Closest capabilities |
|---|---:|---|
| K1 | 72 | Planning, Journey |
| K2 | 55 | Recommendation |
| K3 | 65 | Readiness |
| K4 | 55 | Personalisation (flags OFF) |
| K5 | 63 | Journey (micro) |
| K6 | 50 | Validation / analytics ops (flag OFF) |
| K7 | 58 | (revision — not a separate maturity cell; residual) |
| K8 | 70 | Explainability |

Source: EP-007.2 `K1_REVALIDATION.md`.

---

## 6. Freshness

| Item | Rule |
|---|---|
| Assessment date | 2026-07-26 |
| Stale if | New validated KSI board, E4/E5 artefact, T7 declaration, commercial tracker change, or Version 1 go/no-go update without re-assessment |
| Prefer lower | If new evidence conflicts with a raised level, keep prior lower level until re-scored |

---

**End of Maturity Traceability**

# Governance Hierarchy

**Audit date:** 2026-07-28  
**Source of truth for ranks:** `knowledge/GOVERNANCE.md` §1  
**This document:** Describes the hierarchy as it exists in the repository (observed + official ranks). Does not invent new ranks.

---

## 1. Official ranked hierarchy (GOVERNANCE.md)

Authority flows **downward**. Lower documents must not contradict higher ones. On conflict: **STOP**, document, amend the higher authority first.

```
Rank 0 — Meta-governance
    knowledge/GOVERNANCE.md
    (+ GP-001 Founder Governance Model — capacity / approval procedure)

Rank 1 — Product philosophy (apex)
    knowledge/product/vision/PRODUCT_VISION_2030.md
         Why · north star · philosophies · never-build · Final Test

Rank 2 — Product strategy
    PRODUCT_BLUEPRINT.md
         Audiences · model · Twin role · roadmap · promise

Rank 2a — Educational usefulness measurement
    knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md
         KSI · Version 1 usefulness ≥ 80 · prioritisation by student value

Rank 2b — Product explainability gate
    knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md

Rank 2c — Product recommendation quality gate
    knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md
         (+ Recommendation Decision Framework / Scorecard)

Rank 2d — Version 1 production-ready law
    knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md
         Gates G1–G12 · evidence · go / no-go

Rank 2e — Board evidence synthesis (does not amend gates)
    knowledge/product/p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md

Rank 3 — Educational meaning & integrity (apex educational)
    knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md
         ↓
    EGI-002 Educational Logic Registry
    EGI-003 Educational Governance Review Standard
    EIP specialised standards (evidence, explainability speech, state authority, …)
    Programme VI educational domain models

Rank 4 — Educational quality sufficient to release
    knowledge/educational_validation/  (EVF Programme V)
         Validation Constitution → Dimensions / Capability / Blind → Release Standard → Release Gate

Rank 5 — Structural / runtime law
    docs/ARCHITECTURE_CONSTITUTION.md
    docs/architecture/SYSTEM_ARCHITECTURE.md
    ARCHITECTURE.md
    (+ Digital Twin Constitution; Design Principles; Dependency Rules; EI Architecture)

Rank 6 — Accepted architectural decisions
    docs/adr/  (primary EOS index)
    (+ secondary historical / V2 journey ADR trees)

Rank 7 — How we build and verify
    knowledge/ENGINEERING_STANDARDS.md
    knowledge/QUALITY_MANUAL.md
    (+ docs/ENGINEERING_CHARTER.md — engineering philosophy)

Rank 8 — Feature proposals
    knowledge/prd/

Rank 9 — How we ship
    knowledge/RELEASE_PLAYBOOK.md
    docs/process/RELEASE_PROTOCOL.md
    (+ knowledge/engineering/RELEASE_PROTOCOL.md — engineering gate contract)

Rank 10 — Readiness tracking (not declaration authority)
    knowledge/VERSION_1_READINESS.md
```

---

## 2. Parallel product-philosophy band (ILE — under Rank 1–3)

These documents are **permanent strategic / framework filters**. They sit under Vision 2030 and Educational Constitution; they do **not** create a second apex. GOVERNANCE.md does not assign them numeric ranks, but repository usage treats them as decision filters for experience programmes.

```
Vision 2030 (Rank 1)
    ↓
Educational Constitution (Rank 3)  ←── educational meaning
    ↓
PRODUCT_PRINCIPLES.md (ILE-000)
EDUCATIONAL_PHILOSOPHY.md / USER_EXPERIENCE_PHILOSOPHY.md
STUDY_SENSEI_PHILOSOPHY.md (ILE-010)
    ↓
STUDENT_DECISION_FRAMEWORK.md (ILE-011)
    + Decision Catalogue, Guidance Responsibility Matrix,
      Decision Confidence Model, Silence Principle, Decision Lifecycle
    ↓
NON_GOALS.md  (expands Vision never-build for roadmap rejection)
GUIDANCE_OVER_CONTENT.md / STUDENT_RELATIONSHIP_MODEL.md
    ↓
Implementation programmes (EP / P / ILE delivery)
```

**Relationship to Rank 2a–2c:** Student Decision Framework defines *agency and silence*; P-001.2/1.3 define *product quality gates* for speech and recommendation selection. Orchestration Programme VII defines *constitutional recommendation structure*. All three layers are complementary, not peers of Vision.

---

## 3. Board & operating governance (under Rank 0 / Rank 2d)

```
knowledge/GOVERNANCE.md
    ↓
GP-001 Founder Governance Model
    Role Mapping · Approval Matrix
    ↓
P-003.7 Product Board Charter
    Decision / Release Decision / Evidence Review / Change Control / Cadence
    ↓
Registers (standing memory)
    P-003.2 Decision Register
    P-003.3 Risk Register
    P-003.4 Assumption Register
    P-003.5 Evidence Hierarchy (claim lens)
    P-003.6 Maturity Model
    P-003.8 Version 1 Exit Criteria (synthesis)
```

Product Board **recommends** Version 1 GO / NO GO under P-002.1; Founder acts as Chair (GP-001). Evidence Hierarchy and gate evidence are not weakened by capacity concentration.

---

## 4. Educational dual-track (meaning vs release quality)

Official split (GOVERNANCE.md):

```
Educational Constitution / EGI / EIP
    → Is this educationally *lawful* and *meaningful*?

EVF (Programme V)
    → Is educational *quality / trust* sufficient to *release* to students?

Blind Review (research)
    → Independent perception input consumed by EVF — does not replace EVF
```

Gate order in practice:

```
Law (EGI) → Integrity review (EGI-003) → Quality (EVF Gate) → Ship (Release Playbook / Protocol)
```

For **Version 1 production-ready declaration**, P-002.1 additionally requires validated KSI, constitutional compliance (including EVF outcome), explainability / recommendation / planning / readiness quality, and operational gates G7–G12.

---

## 5. Release stack (observed)

```
Philosophy / Final Test ………… Vision 2030
Strategy ………………………………… Blueprint
Usefulness bar ……………………… P-001.1 KSI
Speech / tip quality …………… P-001.2 / P-001.3
Educational release quality … EVF Gate
Production-ready declaration … P-002.1 G1–G12
Board synthesis ………………… P-003.1 Dossier (+ P-003.8 exit criteria)
Operator procedure …………… RELEASE_PLAYBOOK → docs/process/RELEASE_PROTOCOL
Engineering gate contract … knowledge/engineering/RELEASE_PROTOCOL
Status board …………………… VERSION_1_READINESS (tracker only)
```

Historical trail (not current declaration law): `knowledge/release/KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` (V1R-001 SUBMITTED 2026-07-15).

---

## 6. Architecture stack (observed)

```
Architecture Constitution
    ↓
Design Principles · Dependency Rules · Digital Twin Constitution
    ↓
SYSTEM_ARCHITECTURE · ARCHITECTURE.md · Educational Intelligence Architecture
    ↓
ADRs (docs/adr primary)
    ↓
Engineering Standards · agent rules (.cursor/rules)
```

V2 specialisations (`knowledge/version2/*`, V2 Design Manifesto, Instructional Principles) specialise Learning Journey architecture under the same constitutional apex — they do not replace Rank 1–5.

---

## 7. Orchestration & meta-constitutional corpora

```
EGI-001 Educational Constitution
    ↓
Programme VI domain models (knowledge/educational/*)
    ↓
Programme VII orchestration (workflows · authority · recommendations · state)
    ↓
Programmes VIII–X integration / conformance / verification /
    compliance / certification / evolution / execution / runtime
```

These corpora are **large and specialised**. They sit *below* Educational Constitution and Architecture Constitution. They must not be mistaken for product Vision or Version 1 release law.

---

## 8. Agent / contributor enforcement layer

```
Ranked governance docs
    ↓
CONTRIBUTING.md · ENGINEERING_STANDARDS · QUALITY_MANUAL
    ↓
.cursor/rules/*  (always-applied digests)
```

Agent rules are **procedural enforcement**, not independent constitutions.

---

## 9. Hierarchy health assessment

| Check | Result |
|---|---|
| Single ranked table exists | **Yes** — GOVERNANCE.md |
| Apex product document exists | **Yes** — Vision 2030 |
| Apex educational document exists | **Yes** — Educational Constitution |
| Apex architecture document exists | **Yes** — Architecture Constitution |
| Version 1 release law exists | **Yes** — P-002.1 |
| Founder operating model exists | **Yes** — GP-001 |
| Product Board procedure exists | **Yes** — P-003.7 |
| Risk of duplicate apex | **Low** for Vision/Ed/Arch; **Medium** for naming collisions (EVF vs EP-001) and release checklist proliferation |
| Risk of fragmentation | **High** in constitutional meta-corpora and ILE companion pack — authority is clear if GOVERNANCE.md is followed; discovery is hard |

---

## 10. Practical navigation rule

When choosing which document governs a decision:

1. Start at **GOVERNANCE.md** ranks.  
2. If educational *meaning* → Educational Constitution / EGI.  
3. If educational *release trust* → EVF.  
4. If Version 1 *production-ready* → P-002.1 (not estimated ΔKSI alone).  
5. If student-facing *speech* → EIP-003 then P-001.2.  
6. If student-facing *recommendation selection* → Programme VII then P-001.3.  
7. If *who decides / silence / agency* → Student Decision Framework (ILE-011).  
8. If *who approves* → GP-001 + Product Board Charter.  
9. If *structure / Twin / runtime* → Architecture Constitution + ADRs.  
10. If unsure → STOP and document (GOVERNANCE §3.3).

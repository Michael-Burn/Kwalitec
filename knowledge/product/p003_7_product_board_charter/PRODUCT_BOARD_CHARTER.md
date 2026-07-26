# Product Board Charter

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — documentation charter  
**Effective:** 2026-07-26  
**Audience:** Product Board members and deputies  
**Does not:** Amend Vision, PSF, P-001.2/1.3, P-002.1 gates, Educational Constitution, EVF, architecture baselines, Decision / Risk / Assumption registers, Evidence Hierarchy, Maturity Model, or runtime  

---

## How to read this Charter

After this folder alone, a Board member should be able to answer:

> How does the Product Board govern Kwalitec?

Companion procedures in this folder deepen roles, decisions, evidence, release, change control, and meetings. Canonical *law* and *registers* remain in their own programmes (cited below). This Charter defines **who decides what, and by which procedure**.

---

## 1. Purpose

### 1.1 Mission

The Product Board exists to govern Kwalitec as an **evidence-bound educational product**: to protect students from unsupported claims, to keep Version 1 release decisions honest, and to ensure that architecture, educational quality, and product strategy remain aligned with Vision 2030’s Final Test:

> Does this help students become better professionals?

The Board is the standing authority that **recommends** Version 1 production-ready GO or NO GO, **approves** material product and claim decisions, **reviews** evidence against the Evidence Hierarchy, and **steers** Version planning without micromanaging delivery.

### 1.2 Scope of authority

| The Board **governs** | The Board **does not govern** |
|---|---|
| Architecture *direction and invariants* (one runtime; curriculum V1/V2; Twin boundaries) | Day-to-day implementation details, PR-level design, or ticket prioritisation |
| Educational quality *claim posture* and honesty freezes | Educational algorithm math inside services (owned by Educational Constitution + engineering) |
| Evidence classification for product / release / marketing claims | Runtime telemetry plumbing as an engineering concern |
| Release readiness *declaration* under P-002.1 | Operational deploy / rollback execution (Release Playbook / operator) |
| Material risks, assumptions, and decision register posture | Bug triage, CI greenness, or sprint ceremonies |
| Public and cohort educational claims | Support ticket handling |
| Documentation *governance* (which artefacts are authoritative; supersession) | Copy-editing every programme folder |
| Version planning and post–Version 1 investment *guidance* | Binding engineering roadmaps without Product owner / Blueprint process |

### 1.3 Guiding principles

1. **Evidence before opinion** — Board positions cite classified evidence paths; debate without paths yields HOLD or DEFER, not GO.  
2. **No unsupported educational claims** — Absence of evidence is **unknown**, not success.  
3. **Evidence Hierarchy governs claims** — E1–E5 and claim codes (C-*) from P-003.5 bind what may be said and to whom.  
4. **Registers remain authoritative** — Decisions (DR), Risks (PR), Assumptions (PA) are the standing memory of Version 1; this Charter does not replace them.  
5. **Version 1 decisions remain active until formally superseded** — IDs do not silently change meaning.  
6. **Prefer lower** — When evidence conflicts, credit the lower claim set (PSF honesty; DR-027).  
7. **Separable verdicts** — Programme GO, educational effectiveness GO, and Version 1 production-ready are three different claim families (DR-032).  
8. **Curriculum first; deterministic cores** — Planning, readiness, and recommendations must remain reproducible from the same inputs.  
9. **Hierarchy STOP rule** — If a proposal contradicts a higher-authority document, **STOP**, document, and amend the higher authority first (`GOVERNANCE.md` §1).

---

## 2. Responsibilities

### 2.1 Govern

| Domain | Board duty | Primary artefacts |
|---|---|---|
| **Architecture** | Uphold one-runtime / Runtime A production defaults; Twin and consumer-chain as gated; curriculum V1/V2 loadable | Architecture Constitution; EP-002.9 baseline; ADRs; DR architecture cards |
| **Educational quality** | Enforce claim freezes; consume EVF educational outcome; refuse perception-as-effectiveness | Educational Constitution; EVF; P-001.2 / P-001.3; DR-021 / DR-033 / DR-036 |
| **Evidence** | Admit, classify, freshness-check, and retire evidence for claims | P-003.5 Evidence Hierarchy; validation packages (EP-005.*–EP-007.*) |
| **Release readiness** | Score G1–G12 honesty via dossier; recommend GO / CONDITIONAL GO / NO GO / DEFER | P-002.1; P-003.1 dossier; `VERSION_1_READINESS.md` |
| **Risks** | Accept, retarget, or close Version 1 release risks | P-003.3 Risk Register |
| **Claims** | Approve Board / cohort / public statements per claim tree | P-003.5 Claim Standard + Decision Tree |
| **Documentation** | Keep charter, registers, and dossier current under change control | This folder; P-003.* series |
| **Version planning** | Guide investment toward evidence gaps (not feature vanity) | P-003.6 Maturity Model; Blueprint; PSF |

### 2.2 Do not govern

- Implementation details (function signatures, template markup, adapter wiring).  
- Day-to-day engineering (sprint boards, code review assignment, CI flake triage).  
- Operational delivery (deploy timing, host config, incident runbooks) — except when ops risk becomes a **Version 1 release risk** (then: register + recommend; do not operate).

Engineering and Release authorities execute; the Board **decides posture and claims**.

---

## 3. Membership

The Board is defined by **roles** (capacities), not named individuals. One person may hold multiple roles when the organisation is small; **independent re-score** (G1.7) and similar duties still require a second assessor where gate law demands it.

### 3.1 Founder-operated reality (GP-001)

Kwalitec is currently **founder-operated**. The Founder holds Product Board Chair and the Product / Engineering / Operations / Privacy Owner capacities (and related Board lenses until staffed). See `../gp001_founder_governance_model/FOUNDER_GOVERNANCE_MODEL.md`. This does **not** dissolve the Board or waive evidence requirements. Independent separation of duties is deferred until scale (DR-054; PR-027).

Material Board approvals use **Founder Review** records (Reviewer · Date · Decision · Notes with capacity), per `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`.

| Role | Core duty |
|---|---|
| **Chair** | Convene meetings; ensure quorum for release decisions; publish recommendations |
| **Product Governance Lead** | Own Decision Register currency; claim language; Final Test / KSI bar honesty |
| **Evidence Lead** | Classify evidence (E1–E5); maintain freshness; refuse unavailable→invented fills |
| **Architecture Representative** | One-runtime / Twin / curriculum invariants; ADR currency for G2 |
| **Research Representative** | Blind-review / validation method integrity; external vs internal cohort honesty |
| **Engineering Representative** | Quality contracts, flags, tests, perf/reliability evidence for G5–G12 technical packs |
| **Educational Representative** *(when educational claims or EVF in scope)* | Educational Constitution compliance; EVF outcome interpretation |
| **Security Representative** *(when G10 or public launch in scope)* | Security review posture for declaration packages |

Full RACI: [`BOARD_ROLES_AND_RESPONSIBILITIES.md`](BOARD_ROLES_AND_RESPONSIBILITIES.md). Role → capacity map: `../gp001_founder_governance_model/ROLE_MAPPING.md`.

---

## 4. Decision principles

| Principle | Operational meaning |
|---|---|
| Evidence before opinion | No ACTIVE DR / public claim without linked paths |
| No unsupported educational claims | Marketing freezes stand until E4/E5 (or permitted C-* minimum) clears |
| Evidence hierarchy governs claims | Walk Claim Decision Tree before publish |
| Registers remain authoritative | DR / PR / PA IDs cited in Board minutes and recommendations |
| Version 1 decisions active until superseded | Confirm / Amend / Supersede only via Decision Lifecycle |
| Hard-gate FAIL → overall NO-GO | P-002.1 §5; no optimism override |
| HOLD → GO WITH CONDITIONS at best | Conditions must be named claim restrictions |
| Docs-only ΔKSI = 0 | Governance packaging never invents student-value movement |

Decision procedure: [`DECISION_PROCESS.md`](DECISION_PROCESS.md).  
Lifecycle detail (unchanged law): `../p003_2_product_decision_register/DECISION_LIFECYCLE.md`.

---

## 5. Review process

How governance state moves:

| Flow | Board action | Detail |
|---|---|---|
| **New evidence enters** | Evidence Lead classifies; Board accepts into claim package or rejects as insufficient | [`EVIDENCE_REVIEW_PROCESS.md`](EVIDENCE_REVIEW_PROCESS.md) |
| **Assumptions validated / rejected** | Promote / Demote / Reject via Assumption Review Process | `../p003_4_product_assumption_register/ASSUMPTION_REVIEW_PROCESS.md` |
| **Decisions reviewed** | Confirm / Amend / Supersede | Decision Lifecycle + [`DECISION_PROCESS.md`](DECISION_PROCESS.md) |
| **Risks closed / accepted** | Close with proof; Accept only with named residual under operating mode | Risk Review Process |
| **Maturity changes** | Re-assess only with cited paths; prefer lower; no Level 4/5 without E4/E5 | P-003.6 Maturity Model |

**Default Version 1 posture (as of 2026-07-26, unchanged by this Charter):** Board recommendation **NO GO** on Version 1 production-ready (DR-041); validated KSI **62**; effectiveness **NO-GO**; `N_external = 0`.

---

## 6. Change control

| Artefact class | Board approval required? |
|---|---|
| This Charter (material change) | **Yes** — version bump + Chair ack |
| Decision / Risk / Assumption register content | **Yes** for new ACTIVE law/posture, acceptance, closure that changes release story |
| Evidence Hierarchy / Claim Standard | **Yes** (treat as claim law) |
| Maturity re-assessment numbers | Board note on material heat/level change |
| Programme completion reports (EP/P) | No Board meeting required; Product Governance Lead may spot-check SIA / ΔKSI honesty |
| Higher law (Vision, Constitution, P-002.1 gates) | **Higher-authority amendment first** — Board may recommend, not silently rewrite |

Superseded documents keep readable history; IDs are never reused.  
Full rules: [`CHANGE_CONTROL.md`](CHANGE_CONTROL.md).

---

## 7. Release governance

### 7.1 Interaction map

```
Vision / PSF / Educational Constitution / Architecture
                    │
                    ▼
         P-002.1 Release Framework (G1–G12 law)
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Evidence     Decision     Risk /
   Hierarchy    Register     Assumption
   (P-003.5)    (P-003.2)    (P-003.3/4)
        │           │           │
        └───────────┼───────────┘
                    ▼
         P-003.1 Release Dossier (synthesis)
                    │
                    ▼
         Product Board recommendation
              GO | CONDITIONAL GO | NO GO | DEFER
                    │
                    ▼
         Signed Go / No-Go record (P-002.1)
         + VERSION_1_READINESS alignment
```

### 7.2 Binding rule

> **Only the Product Board may recommend GO or NO GO** on Version 1 production-ready declaration.

- Engineering may report gate packs PASS/FAIL.  
- Release operators may deploy under GA / invite-only rules.  
- Educational Gate Owner confirms EVF outcome (feeds G2.4).  
- **None of the above alone constitutes a Version 1 production-ready recommendation.**

Exit criteria and scoring: [`RELEASE_DECISION_PROCESS.md`](RELEASE_DECISION_PROCESS.md) and P-002.1 Go / No-Go Guide.

### 7.3 Current recommendation (frozen snapshot)

| Field | Value |
|---|---|
| Recommendation | **NO GO** |
| Blocking | G1 FAIL (G1.1, G1.9); incomplete G1–G12 package; G1.7 HOLD |
| Decision ID | DR-041 |
| Dossier | `../p003_1_version1_release_dossier/` |

This Charter does **not** flip that posture.

---

## 8. Meetings

| Meeting | Typical cadence | Purpose |
|---|---|---|
| Monthly governance review | Monthly | Registers, claims, maturity heat, open blockers |
| Milestone review | End of material EP/P | SIA / evidence / decision impact |
| Release review | Before any C-V1 / C-REC change | Full G1–G12 + dossier + recommendation |
| Emergency review | As needed | Honesty incident, flag-default flip, critical risk |
| Evidence review | When new validation packs arrive | Classify E1–E5; refresh claim freezes |

Cadence detail: [`MEETING_CADENCE.md`](MEETING_CADENCE.md).

---

## 9. Outputs

Expected Board outputs (recorded with date, attendees/roles, evidence paths):

| Output | Form |
|---|---|
| **Release recommendation** | GO / CONDITIONAL GO / NO GO / DEFER + blockers |
| **Risk acceptance** | Named PR + residual + operating mode |
| **Decision approval** | New/updated DR or Confirm note |
| **Evidence review** | Classification result + permitted C-* codes |
| **Governance updates** | Charter / process version notes; register maintenance |
| **Roadmap guidance** | Non-binding investment lens (evidence-first; maturity Red cells) |

Minutes need not be verbose; they must be **auditable**.

---

## 10. Success measures

This Charter succeeds when the Board can demonstrate:

| Measure | Signal |
|---|---|
| **Consistent governance** | Same question → same procedure → same class of outcome |
| **Repeatable release decisions** | Two Board sessions with the same package reach the same recommendation class |
| **Transparent evidence handling** | Every claim walks E-level → C-* → approval → (optional) publish |
| **Auditable decision making** | DR/PR/PA IDs and paths cited; supersessions leave history |

Failure modes this Charter exists to prevent: tribal “we’re ready”; optimism overriding hard-gate FAIL; treating E2/E3 as E5; Green maturity cells as C-V1; GA deploy as production-ready Version 1.

---

## 11. Authority stack (quick reference)

| Rank (summary) | Document |
|---:|---|
| 1 | Product Vision 2030 |
| 2 | Product Blueprint |
| 2a–2d | PSF (KSI); Explainability Standard; Recommendation Quality Standard; Version 1 Release Framework |
| 2e | Version 1 Release Dossier (synthesis; does not amend gates) |
| 3–4 | Educational Constitution; EVF |
| 5–6 | Architecture Constitution / System Architecture; ADRs |
| 7+ | Engineering Standards; PRDs; Release Playbook |

Full table: `knowledge/GOVERNANCE.md` §1.

**This Charter** sits as Product Board *procedure* under that hierarchy. It does not insert a new rank that overrides Vision, PSF, P-002.1, or Educational Constitution.

---

## 12. Companion documents in this programme

| Document | Role |
|---|---|
| [`BOARD_ROLES_AND_RESPONSIBILITIES.md`](BOARD_ROLES_AND_RESPONSIBILITIES.md) | Role definitions and RACI |
| [`DECISION_PROCESS.md`](DECISION_PROCESS.md) | How the Board reaches and records decisions |
| [`EVIDENCE_REVIEW_PROCESS.md`](EVIDENCE_REVIEW_PROCESS.md) | How evidence is admitted and classified for Board use |
| [`RELEASE_DECISION_PROCESS.md`](RELEASE_DECISION_PROCESS.md) | How GO / NO GO is formed |
| [`CHANGE_CONTROL.md`](CHANGE_CONTROL.md) | How governance artefacts evolve |
| [`MEETING_CADENCE.md`](MEETING_CADENCE.md) | Meeting types and agendas |
| [`README.md`](README.md) | Folder index and quick start |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student impact (docs-only; ΔKSI = 0) |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion |

---

## 13. Control statement

> The Product Board governs Kwalitec through evidence, registers, and release gates — not through opinion or operational convenience. Only the Product Board may recommend Version 1 production-ready GO or NO GO. As of 2026-07-26 that recommendation remains **NO GO**. This Charter defines procedure; it does not rewrite law, invent external evidence, or activate runtime features.

---

**End of Product Board Charter**

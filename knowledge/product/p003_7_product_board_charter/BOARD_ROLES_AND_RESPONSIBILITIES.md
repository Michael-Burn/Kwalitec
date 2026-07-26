# Board Roles and Responsibilities

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — role charter  
**Effective:** 2026-07-26  
**Companion:** [`PRODUCT_BOARD_CHARTER.md`](PRODUCT_BOARD_CHARTER.md)  
**Does not:** Invent multi-person staffing; waive P-002.1 evidence; change runtime  

**Founder model:** `../gp001_founder_governance_model/FOUNDER_GOVERNANCE_MODEL.md` · [`ROLE_MAPPING.md`](../gp001_founder_governance_model/ROLE_MAPPING.md)

---

## 1. Purpose

Define **roles** (capacities) for the Product Board so governance remains operable when people change. Roles map to P-002.1 sign-off responsibilities without replacing gate ownership tables.

Under GP-001, Kwalitec is founder-operated: the Founder currently holds all Board capacities below. Capacity concentration does **not** waive evidence or independent second-assessor law (G1.7).

---

## 1a. Founder-operated quorum

| Meeting type | Minimum under founder operation |
|---|---|
| Monthly / milestone / evidence | Founder as Chair + recorded Product Owner and Evidence Lead capacity checks |
| Release review | Founder as Chair + Founder Reviews for every capacity required by the Approval Matrix for that claim class |
| Emergency | Founder as Chair + owning capacity for the domain |

If required capacity Founder Reviews are missing → **DEFER**; do not invent GO.

---

## 2. Role catalogue

### 2.1 Chair

| Field | Content |
|---|---|
| **Mission** | Make Board procedure happen on time and on record |
| **Owns** | Agenda; quorum for release recommendations; publication of Board outputs |
| **Must** | Ensure release reviews cite dossier + gates + registers; refuse undocumented GO |
| **Must not** | Unilaterally flip C-V1 without full Board procedure; operate deploys |
| **Quorum role** | Required for Release review and Emergency honesty reviews |

### 2.2 Product Governance Lead

| Field | Content |
|---|---|
| **Mission** | Keep product law, claims, and Decision Register honest |
| **Owns** | DR currency; claim language; Final Test alignment; KSI bar honesty (estimated ≠ validated) |
| **Must** | Block unsupported educational claims; cite DR-021 / DR-033 / DR-036 freezes when relevant |
| **Must not** | Treat estimated ΔKSI as Gate G1 satisfaction |
| **Maps to P-002.1** | Product owner scope (G1, claim language, overall GO / NO-GO recommendation drafting) |

### 2.3 Evidence Lead

| Field | Content |
|---|---|
| **Mission** | Classify and freshness-check evidence used for Board claims |
| **Owns** | E1–E5 assignment for claim packets; “Evidence currently unavailable” labelling |
| **Must** | Prefer lower; split E3 (internal) from E4 (external); refuse anecdote-as-E5 |
| **Must not** | Invent missing packs; stack estimates into validated boards |
| **Maps to** | P-003.5 Evidence Hierarchy & Claim Decision Tree |

### 2.4 Architecture Representative

| Field | Content |
|---|---|
| **Mission** | Protect structural invariants at Board level |
| **Owns** | One-runtime / Runtime A defaults; Twin / consumer-chain gate honesty; curriculum V1/V2; ADR currency inputs to G2 |
| **Must** | Flag proposals that create a second educational brain under production defaults |
| **Must not** | Approve architecture by slide alone without ADR / baseline citation |
| **Maps to P-002.1** | Architecture sign-off (G2.5–G2.6, G2.8) |

### 2.5 Research Representative

| Field | Content |
|---|---|
| **Mission** | Protect validation method integrity |
| **Owns** | Blind-review / Tier A–D method honesty; external vs persona cohort disclosure; falsifier handling |
| **Must** | Keep perception ≠ effectiveness (DR-033); surface `N_external = 0` when relevant |
| **Must not** | Relabel Stage 0 / persona packs as external outcome evidence |
| **Maps to** | EP-005.1 methodology; EP-004 blind-review framework; EP-007.3 effectiveness posture |

### 2.6 Engineering Representative

| Field | Content |
|---|---|
| **Mission** | Represent engineering verification evidence honestly at Board |
| **Owns** | Quality-contract / test / flag-matrix / perf / reliability packs for G5–G12 technical scopes |
| **Must** | Distinguish E2 (engineering verification) from educational outcome claims |
| **Must not** | Equate green CI or operational GA with Version 1 production-ready |
| **Maps to P-002.1** | Engineering lead scope (G5–G9, G11–G12 technical) |

### 2.7 Educational Representative

| Field | Content |
|---|---|
| **Mission** | Represent educational law and EVF trust outcome at Board |
| **Owns** | Interpretation of Educational Constitution constraints; EVF outcome for claim class (feeds G2.4) |
| **Must** | Block mastery theatre / dual educational truths / opaque AI-as-fact |
| **Must not** | Substitute Educational Gate APPROVED for full G1–G12 (separable verdicts) |
| **Required when** | Educational claims, EVF, or C-EDU / effectiveness reviews are on the agenda |
| **Maps to P-002.1** | Educational Gate Owner scope (G2.3–G2.4, G3–G4 educational honesty) |

### 2.8 Security Representative

| Field | Content |
|---|---|
| **Mission** | Represent security posture for declaration and public-facing risk |
| **Owns** | G10 evidence interpretation; secrets / dependency critical honesty |
| **Required when** | Release review aiming at GO; public launch discussion; G10 status change |
| **Maps to P-002.1** | Security sign-off (G10) |

### 2.9 Release Operator (advisor, not Board governor)

| Field | Content |
|---|---|
| **Mission** | Advise on deploy fingerprint, smoke, rollback readiness |
| **Owns** | Execution under Release Playbook — **not** Version 1 declaration |
| **May attend** | Release reviews as advisor |
| **Must not** | Issue Board GO / NO GO |

---

## 3. RACI (Board-level)

R = Responsible · A = Accountable · C = Consulted · I = Informed

| Board output | Chair | Product Governance | Evidence | Architecture | Research | Engineering | Educational | Security |
|---|---|---|---|---|---|---|---|---|
| Monthly governance agenda | A/R | C | C | I | I | I | C* | I |
| Decision approval (new DR / supersede) | A | R | C | C† | C‡ | C† | C* | I |
| Evidence classification for claim | A | C | R | I | C | C | C* | I |
| Risk accept / close (material) | A | R | C | C | C | C | C* | C§ |
| Maturity re-assessment note | A | R | C | C | C | C | I | I |
| Release recommendation (GO/NO GO) | A | R | C | R¶ | C | R¶ | R¶ | R¶ |
| Public / C-COM claim ack | A | R | R | C | C | I | R | C§ |
| Roadmap guidance (non-binding) | A | R | C | C | C | C | C | I |

\* When educational claims or EVF in scope.  
† When architecture / runtime / flags affected.  
‡ When validation method or cohort type affected.  
§ When G10 or public launch affected.  
¶ Sign per P-002.1 scope for their gates; Chair accounts for overall recommendation record.

---

## 4. Quorum

| Meeting type | Minimum (staffed / multi-person future) | Minimum (founder-operated — current) |
|---|---|---|
| Monthly governance | Chair + Product Governance Lead + one of Evidence / Architecture / Engineering | §1a |
| Milestone review | Chair or Product Governance Lead + Evidence Lead (or deputy) | §1a |
| Evidence review | Evidence Lead + Product Governance Lead | §1a |
| Release review | Chair + Product Governance + Evidence + Architecture + Engineering + Educational; Security if GO sought or G10 open | §1a + Approval Matrix capacity reviews |
| Emergency (honesty / flag) | Chair + Product Governance + owning Representative for the domain | §1a |

If quorum fails → **DEFER** recommendation; do not invent GO.

---

## 5. Deputies and conflicts

- Deputies may act if named in meeting minutes for that session.  
- A person holding multiple roles still counts once for quorum **except** where gate law requires an **independent** second assessor (e.g. G1.7) — then a distinct person is required.  
- Conflicts of interest (e.g. author of a validation pack scoring their own pack alone for G1.7) must be disclosed; Chair assigns alternate.

---

## 6. Authority boundaries (summary)

| Role may | Role may not |
|---|---|
| Recommend HOLD / DEFER / NO GO on incomplete evidence | Override hard-gate FAIL with optimism |
| Require evidence paths before claim approval | Rewrite Vision / Constitution / P-002.1 without higher-authority process |
| Accept residual risk under invite-only / NO GO | Accept residual risk that implies public educational effectiveness without E5 |
| Guide post–V1 evidence investment | Commit engineering delivery dates as Board “law” |

---

**End of Board Roles and Responsibilities**

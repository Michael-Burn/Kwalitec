# RP-002 — Non-Compliance Register

**Programme:** RP-002 — Independent Educational Recertification  
**Date:** 2026-07-28  
**Status:** Active — independent findings from live product  
**Authority:** `RP002_EDUCATIONAL_AUDIT_REPORT.md` · DG-001.1–4  
**Constraint:** Record findings only. Remediation → **RR-002**. Do not treat RR-001 closures as proof.

Severity: **Critical / High / Medium / Low**  
Priority: **P0 / P1 / P2 / P3**  
Status: **Open** · **Contained** · **Watch** · **Accepted Residual (AR)** · **Closed** *(none from this audit — remediation is RR-002)*

---

## Purpose

Catalogue every **Non-Compliant** finding and every material **Partially Compliant** residual that affects independent educational governance certification under DG-001.

Fully Compliant pockets live in the Scorecard. Accepted operational residuals that are not educational-copy defects are listed with AR IDs.

---

## Summary

| ID | Title | Class | Severity | Priority | Package | Follow-up |
|----|-------|-------|----------|----------|---------|-----------|
| RP002-NCR-001 | Product Check-in entry labelled “Share Feedback” | **PC / Open** | Medium | P2 | Lexicon / orientation | RR-002 |
| RP002-NCR-002 | Commitment reflection “What we updated” unnamed authority | **PC / Open** | Low–Med | P2 | Authority / reflection close | RR-002 |
| RP002-NCR-003 | Onboarding header “five ideas” vs six steps | **PC / Open** | Low | P3 | Honesty / orientation | RR-002 |
| RP002-NCR-004 | Learning Check entry attributes support to Kwalitec | **PC / Open** (orphan path) | Medium | P2 | Authority D05/D02 | RR-002 |
| RP002-NCR-005 | Latent `recommendation_card` “Today's Recommendation” eyebrow | **Contained** | Medium if surfaced | P1* | Lexicon CI-01 | RR-002 / keep Contained |
| RP002-NCR-006 | Dual-run session feedback “What did Kwalitec observe/conclude?” | **Contained** | High if sole OFF | P0* | Authority CP-10 | Keep sole-runtime; RR-002 if dual-run retained |
| RP002-NCR-007 | Dual-run dashboard “Today's Recommendation” / pre-lexicon chrome | **Contained** | High if sole OFF | P0* | Lexicon / authority | Sole-runtime smoke |
| RP002-AR-001 | Feature-flag educational enablement Contained OFF | **AR** | High if ON | Ops | D07 | Keep OFF until recert |
| RP002-AR-002 | Notifications educational mentor risk (capability absent) | **AR** | Medium if built | P3 | D08 / EGC-R11 | Future notification programme |
| RP002-AR-003 | Parallel reflection stacks (DG-001.3-D08) | **AR** | Medium | Arch | D08 | Consolidation programme |
| RP002-AR-004 | Sole-runtime misconfiguration reintroduces dual home | **AR** | Critical if mishandled | Ops | Journey integrity | Release checklist |
| RP002-AR-005 | Session notes → Journal mirror not implemented | **AR** | Low | Arch | OQ-R01 | Do not invent second memory |
| RP002-AR-006 | Cohort UX / perception validation not executed | **AR / Watch** | Medium for claims | Research | Trust | Required for validated KSI claims |
| RP002-AR-007 | Internal/CSS `study-tip-*` / “Study tip” fallback strings | **AR / Watch** | Low | Eng | DEP-01 hygiene | Prefer rename in polish |

\*Priority escalates to P0 before any dual-run Alpha claim or Contained-flag enablement.

**Open educational NC (Critical/High) on sole-runtime:** **0**  
**Open educational PC (material):** **4** (NCR-001–004)  
**Contained latent:** **3** (NCR-005–007)  
**Accepted Residuals:** **7** (AR-001–007)

---

## Records

### RP002-NCR-001 — “Share Feedback” vs Product Check-in

| Field | Detail |
|-------|--------|
| **Capability** | Product Check-in / Help / nav |
| **Observed** | Check-in page H1 and disclosure correctly say **Product Check-in** and deny educational reflection. Sidebar and Settings entry still say **Share Feedback**. |
| **Clause** | DG-001.1 Product Check-in canonical term; CP-03; CI-03 orientation consistency |
| **Compliance** | **PC** |
| **Risk** | Medium — students may not connect nav entry to Help glossary “Product Check-in” / non-reflection teaching |
| **Student impact** | Mild vocabulary fracture between Help map and chrome |
| **Required remediation** | Align nav/settings labels to **Product Check-in** (or explicit synonym approved by Board) |
| **Priority** | P2 |
| **Evidence** | `app/templates/research/checkin.html` L5–11; `app/templates/partials/sidebar.html` L53; `app/templates/settings/index.html` |
| **RR-002 package** | RR-002.A orientation consistency |

---

### RP002-NCR-002 — Commitment reflection “What we updated”

| Field | Detail |
|-------|--------|
| **Capability** | Home / Commitment reflection |
| **Observed** | Commitment close fields include label **What we updated** without naming Study Sensei or System. |
| **Clause** | DG-001.2-D05 (one primary authority); DG-001.3 commitment reflection; CP-04 |
| **Compliance** | **PC** |
| **Risk** | Low–Medium — unnamed plural can feel like product+mentor mash |
| **Student impact** | Slight authority blur at Mission complete close |
| **Required remediation** | Attribute update field to Sensei framing or neutral System fact label |
| **Priority** | P2 |
| **Evidence** | `app/templates/student/home.html` L163 |
| **RR-002 package** | RR-002.B commitment authority polish |

---

### RP002-NCR-003 — Onboarding step-count honesty

| Field | Detail |
|-------|--------|
| **Capability** | Onboarding |
| **Observed** | Header chrome refers to **five ideas** while `ONBOARDING_STEPS` contains **six** steps (incl. memory). |
| **Clause** | CP-07 educational honesty |
| **Compliance** | **PC** |
| **Risk** | Low |
| **Student impact** | Minor orientation mistrust |
| **Required remediation** | Align count language with step list |
| **Priority** | P3 |
| **Evidence** | `app/services/alpha_onboarding_service.py` ONBOARDING_STEPS; `app/templates/alpha/onboarding.html` header |
| **RR-002 package** | RR-002.C onboarding honesty |

---

### RP002-NCR-004 — Learning Check entry Kwalitec framing

| Field | Detail |
|-------|--------|
| **Capability** | Assessment / Learning Check entry |
| **Observed** | “Your answers help **Kwalitec** understand how to support you.” Educational support speech attributed to product brand. |
| **Clause** | DG-001.2-D01/D02/D05; CP-04; CP-10 |
| **Compliance** | **PC** (path is Deferred/orphan relative to default Mission journey — still student-reachable) |
| **Risk** | Medium if Assessment becomes default; Low on current default Mission path |
| **Student impact** | Confuses product brand with mentor support role |
| **Required remediation** | Reattribute to Study Sensei or System facts; or quarantine route from student journey |
| **Priority** | P2 |
| **Evidence** | `app/templates/student/assessment/entry.html` L7–9 |
| **RR-002 package** | RR-002.D Learning Check authority |

---

### RP002-NCR-005 — Latent recommendation card eyebrow

| Field | Detail |
|-------|--------|
| **Capability** | Educational copy / Recommendation presentation |
| **Observed** | Student macro `recommendation_card.html` eyebrows **Today's Recommendation**. Not included on sole-runtime Home (Home uses Mission hero). Still a live student component. |
| **Clause** | DG-001.1-D02 (Mission-led focus; Recommendation ≠ Mission hero); CI-01 |
| **Compliance** | **Contained** |
| **Risk** | Medium if rewired onto Home without lexicon pass |
| **Student impact** | None on current sole-runtime Home; high confusion if surfaced alongside Today's Mission |
| **Required remediation** | Rename eyebrow to Guidance/Mission-consistent label before any Home include; or retire macro |
| **Priority** | P1 before reuse |
| **Evidence** | `app/templates/student/components/recommendation_card.html` L4; no include on `home.html` |
| **RR-002 package** | RR-002.E latent component lexicon |

---

### RP002-NCR-006 — Dual-run Kwalitec session feedback narrator

| Field | Detail |
|-------|--------|
| **Capability** | Study Session Feedback (legacy mission path) |
| **Observed** | `mission/session_recorded.html`: “What did **Kwalitec** observe?” / “What can **Kwalitec** honestly conclude?” Route redirects under sole runtime. |
| **Clause** | DG-001.2-D01/D02/D03; CP-10; LXP-004 system feedback ≠ Sensei |
| **Compliance** | **Contained** (redirect) |
| **Risk** | High if sole runtime OFF or redirect regresses |
| **Student impact** | Product brand performs educational observation |
| **Required remediation** | Reattribute to System factual layer or Sensei-framed explainability; keep sole-runtime redirect until fixed |
| **Priority** | P0 if dual-run claimed |
| **Evidence** | `app/templates/mission/session_recorded.html` L29, L38; `app/mission/routes.py` sole-runtime redirect |
| **RR-002 package** | RR-002.F dual-run narrator quarantine |

---

### RP002-NCR-007 — Dual-run dashboard lexicon

| Field | Detail |
|-------|--------|
| **Capability** | Legacy dashboard Home |
| **Observed** | `dashboard/index.html` still presents **Today's Recommendation** section header and pre-Mission-led chrome. Redirected under sole runtime. |
| **Clause** | DG-001.1-D02; CP-03 |
| **Compliance** | **Contained** |
| **Risk** | High if sole runtime OFF |
| **Student impact** | Competing daily-focus nouns |
| **Required remediation** | Do not claim dual-run Alpha educational compliance; align or retire dashboard educational chrome |
| **Priority** | P0 if dual-run claimed |
| **Evidence** | `app/templates/dashboard/index.html` L294; `dashboard/routes.py` redirect_if_sole_runtime |
| **RR-002 package** | RR-002.F |

---

## Accepted Residuals (not open educational-copy NC)

### RP002-AR-001 — Feature-flag enablement Contained

| Field | Detail |
|-------|--------|
| **Residual** | QC / Unified Journey / Runtime C / related flags Contained OFF |
| **Justification** | DG-001.2-D07 — flags never Sensei; enablement is a new certification event |
| **Owner** | Product + Educational Governance + Release Engineering |
| **Discipline** | Keep OFF until surface-specific educational recertification |

### RP002-AR-002 — Notifications preventive

| Field | Detail |
|-------|--------|
| **Residual** | No educational notification surface; D08 envelope/body split not yet applicable |
| **Justification** | Capability not built; preventive residual correct |
| **Owner** | Product (notification programme) |
| **Discipline** | No educational notification without D08 tagging |

### RP002-AR-003 — Parallel reflection stacks

| Field | Detail |
|-------|--------|
| **Residual** | DG-001.3-D08 architecture residuals (UJ Guided Reflection, EOS, V2 JourneyReflection, etc.) |
| **Justification** | Law names residual; student map Closed on Alpha path |
| **Owner** | Architecture |
| **Discipline** | Do not teach as additional student reflection categories |

### RP002-AR-004 — Sole-runtime configuration integrity

| Field | Detail |
|-------|--------|
| **Residual** | Misconfiguration reintroduces competing homes / dual-run NC surfaces |
| **Justification** | Not a sole-runtime copy defect; operational Critical |
| **Owner** | Release Engineering |
| **Discipline** | Sole-runtime smoke before any Alpha educational claim |

### RP002-AR-005 — Session notes → Journal mirror

| Field | Detail |
|-------|--------|
| **Residual** | Session reflection notes not mirrored to Decision Journal |
| **Justification** | Architecture residual; Journal remains sole durable host (CI-02) |
| **Owner** | Architecture + Educational Governance |
| **Discipline** | Do not invent second durable memory |

### RP002-AR-006 — Cohort perception validation

| Field | Detail |
|-------|--------|
| **Residual** | Implementation evidence exists; cohort UX validation not executed |
| **Justification** | Blocks **validated** KSI / perception claims — not sole-runtime FC measurement of strings |
| **Owner** | Product Research |
| **Discipline** | Required before validated KSI declaration |

### RP002-AR-007 — study-tip infrastructure hygiene

| Field | Detail |
|-------|--------|
| **Residual** | CSS/DOM `study-tip-*`; internal fallback “Study tip” in services |
| **Justification** | Student-visible labels use Before you begin / Guidance; residual is hygiene |
| **Owner** | Engineering |
| **Discipline** | Prefer rename in polish; do not reintroduce tip as primary noun |

---

## Board reading

| Question | Answer |
|----------|--------|
| Are there open Critical educational NC on sole-runtime? | **No** |
| May unqualified Fully Compliant / “educationally governed Alpha” be claimed? | **No** — Contained + AR + open PC |
| What blocks Full Pass? | NCR-001–004 remediation (RR-002) + Contained discipline + optional cohort validation for perception claims |
| Next programme | **RR-002** — address Open PC + Contained latent chrome |

---

**End of RP002_NON_COMPLIANCE_REGISTER**

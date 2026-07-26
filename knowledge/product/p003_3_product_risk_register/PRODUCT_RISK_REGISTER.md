# Product Risk Register

**Programme:** P-003.3 — Product Risk Register  
**Document:** Canonical Product Risk Register (full cards)  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Does not:** Amend runtime, services, UI, governance law, architecture, release gates, or decisions  

**Purpose:** Permanent Product Board reference for every material risk that could prevent Version 1 from being released successfully.

**Companions:** [`ACTIVE_RISKS.md`](ACTIVE_RISKS.md) · [`CLOSED_RISKS.md`](CLOSED_RISKS.md) · [`RISK_TRACEABILITY.md`](RISK_TRACEABILITY.md) · [`RISK_REVIEW_PROCESS.md`](RISK_REVIEW_PROCESS.md)

**Evidence standard:** Every risk cites existing artefacts. Unsupported risks are not invented. Posture and ratings freeze at 2026-07-26 evidence (aligned with P-003.1 dossier and P-003.2 Decision Register).

**Prior synthesis:** P-003.1 [`Risk_Summary.md`](../p003_1_version1_release_dossier/Risk_Summary.md) (R1–R14) is the upstream board risk table. This register expands those risks into full cards, adds evidence-backed companions, and assigns stable `PR-NNN` IDs.

**How to use:** A Product Board member should answer *what could prevent Version 1 from being released successfully?* from [`ACTIVE_RISKS.md`](ACTIVE_RISKS.md) plus this register.

---

## Register conventions

| Field | Meaning |
|---|---|
| **Risk ID** | Stable `PR-NNN` identifier (never reuse) |
| **Category** | Educational · Operational · Release · Governance · Evidence · Privacy · Technical · Product · Adoption · Deployment |
| **Status** | `ACTIVE` (open material exposure) · `ACTIVE (controlled)` (open but current controls hold residual to Amber/Green) · `WATCH` (mitigated; re-open if controls erode) · `ACCEPTED` (conscious residual under invite-only / NO GO) · `CLOSED` (see [`CLOSED_RISKS.md`](CLOSED_RISKS.md)) |
| **Prior ID** | P-003.1 `Risk_Summary` ID (`R1`…`R14`) where applicable |
| **Owner** | Accountable role for review / closure work (not necessarily the mitigator of every control) |

Indexes: [`ACTIVE_RISKS.md`](ACTIVE_RISKS.md) · Closed: [`CLOSED_RISKS.md`](CLOSED_RISKS.md) · Traceability: [`RISK_TRACEABILITY.md`](RISK_TRACEABILITY.md)

---

## Board-level rating matrix

### Likelihood

| Level | Meaning |
|---|---|
| **Very Low** | Unlikely under current controls and operating mode |
| **Low** | Possible but uncommon; controls usually prevent |
| **Medium** | Plausible within the Version 1 claim window without further action |
| **High** | Expected or already true under current evidence |
| **Very High** | Certain / already materialised as current board state |

### Impact

| Level | Meaning |
|---|---|
| **Very Low** | Negligible effect on Version 1 declaration or student trust |
| **Low** | Local inconvenience; does not block declaration alone |
| **Medium** | Material friction for ops, confidence, or partial gates |
| **High** | Blocks honest expansion, evidence, or claim classes |
| **Critical** | Blocks Version 1 production-ready declaration or causes student/governance harm if ignored |

### Overall Rating

Default band from Likelihood × Impact:

| Likelihood ↓ \\ Impact → | Very Low | Low | Medium | High | Critical |
|---|---|---|---|---|---|
| **Very Low** | Green | Green | Green | Amber | Amber |
| **Low** | Green | Green | Amber | Amber | Amber |
| **Medium** | Green | Amber | Amber | Red | Red |
| **High** | Amber | Amber | Red | Red | Red |
| **Very High** | Amber | Red | Red | Red | Red |

**Control adjustment:** Strong, enforced controls may reduce Overall by **one band** (documented as `ACTIVE (controlled)`). Controls never erase Critical impact if Likelihood remains High/Very High without closing evidence (e.g. effectiveness NO-GO stays Red).

---

## Board control statement

> Release risk is currently dominated by **unproven educational effectiveness** and **sub-bar validated KSI (62 &lt; 80)**, compounded by **privacy-blocked external evidence** (external N = 0). Under P-002.1 and P-003.1, these force **NO GO** on Version 1 production-ready declaration. Continuing Stage 0 private beta under EP-004 conditions does not close these risks.

---

# Part A — Critical release blockers

---

## PR-001 — Educational effectiveness unproven while product may be described as “ready”

| Field | Content |
|---|---|
| **Category** | Educational · Evidence |
| **Status** | ACTIVE |
| **Prior ID** | R1 |
| **Description** | Version 1 educational-effectiveness Go/No-Go remains **NO-GO / PENDING EVIDENCE**. Perception packs and structural quality do not prove learning outcomes. Claiming the product is “ready” (or that recommendations/planning improve exam outcomes) without cohort evidence creates student harm and governance breach. |
| **Evidence** | `knowledge/product/p003_1_version1_release_dossier/Risk_Summary.md` R1; `knowledge/product/ep007_3_educational_effectiveness_validation_stage1/G1_9_STATUS.md` (G1.9 FAIL); `COHORT_EVIDENCE_REGISTER.md` (ABSENT floors); EP-003 educational effectiveness PENDING EVIDENCE; P-003.1 `Version_1_RELEASE_DOSSIER.md` §8 |
| **Likelihood** | High (claim language can slip; effectiveness already unproven) |
| **Impact** | Critical |
| **Overall Rating** | **Red** — High × Critical; no control closes G1.9 without external evidence |
| **Current Controls** | Effectiveness marketing freeze (DR-036); educational claims require educational evidence (DR-021); perception ≠ effectiveness (DR-033); board NO GO (DR-041); prefer-lower scoring |
| **Remaining Exposure** | G1.9 FAIL until Stage 1 ops + scorecards/interviews (or approved waiver with claim restrictions) |
| **Owner** | Product Board |
| **Review Trigger** | Stage 1 privacy clearance; first external cohort week complete; EP-003/007.3 effectiveness re-verdict |
| **Closure Criteria** | Educational effectiveness Go/No-Go is not NO-GO for the claim window; G1.9 PASS (or HOLD with written claim restrictions under P-002.1) |
| **Related Decisions** | DR-021, DR-022, DR-033, DR-036, DR-041 |
| **Related Programmes** | EP-003, EP-004, EP-007.3, P-002.1, P-003.1 |

---

## PR-002 — Validated KSI below Version 1 bar (62 &lt; 80)

| Field | Content |
|---|---|
| **Category** | Release · Evidence |
| **Status** | ACTIVE |
| **Prior ID** | R2 |
| **Description** | Published W-PROD validated KSI is **62**; Version 1 product-success bar is **KSI ≥ 80** (gap **18**). Declaring Version 1 product success or production-ready usefulness without closing the gap is a false success claim. |
| **Evidence** | `Risk_Summary.md` R2; P-003.1 `KSI_Evolution.md`; EP-007.2 board; EP-005.1 `VALIDATED_KSI_REPORT.md` (historical 59→ later 62); DR-051; G1.1 FAIL in `Release_Gates.md` |
| **Likelihood** | Very High (current board state) |
| **Impact** | Critical |
| **Overall Rating** | **Red** — Very High × Critical |
| **Current Controls** | Prefer-lower discipline (DR-027); estimated ≠ validated (DR-026); no estimate stacking; remediation portfolio via EP-005.2 / EP-007; NO GO until G1 |
| **Remaining Exposure** | Gap of 18 points; G1.1 FAIL blocks declaration |
| **Owner** | Product |
| **Review Trigger** | New validated KSI board published; category-level remediation programmes complete |
| **Closure Criteria** | Validated KSI ≥ 80 under production defaults for the claim window (G1.1 PASS), with confidence rules met |
| **Related Decisions** | DR-025, DR-026, DR-027, DR-051, DR-041 |
| **Related Programmes** | EP-005.1, EP-005.2, EP-006.*, EP-007.2, P-001.1, P-003.1 |

---

## PR-003 — Privacy Review unsigned blocks Stage 1 expansion

| Field | Content |
|---|---|
| **Category** | Privacy · Release |
| **Status** | ACTIVE |
| **Prior ID** | R3 |
| **Description** | `private_beta/PRIVACY_REVIEW.md` remains an **unsigned** checklist (Founder Reviews for Product Owner + Privacy Owner capacities still OPEN under GP-001). Expanded external cohort (Stage 1) cannot start without those reviews. This is both a compliance control and an evidence bottleneck: without Stage 1, effectiveness cannot be measured. |
| **Evidence** | `knowledge/product/private_beta/PRIVACY_REVIEW.md`; EP-004 `GO_NO_GO_DECISION.md` condition C1; EP-004 `LESSONS_LEARNED.md` (“Privacy sign-off is the real critical path”); EP-007.3 EFF-02 / Stage 1 HOLD; `Risk_Summary.md` R3; GP-001 Approval Matrix |
| **Likelihood** | High (currently blocking) |
| **Impact** | High |
| **Overall Rating** | **Red** — High × High; blocks evidence chain |
| **Current Controls** | Invite-only / no public registration (DR-034); Stage 0 dogfood may continue under internal alpha rules; GO WITH CONDITIONS requires C1 before expansion (DR-040); Founder Review form (GP-001) |
| **Remaining Exposure** | Illegal/unethical expansion if ignored; permanent evidence stall if unsigned indefinitely |
| **Owner** | Founder — Product Owner + Privacy Owner capacities |
| **Review Trigger** | Both Founder Reviews Approve; Stage 1 invite plan scheduled |
| **Closure Criteria** | Privacy Founder Reviews Approve for the Stage 1 claim window; C1 cleared in private-beta Go/No-Go |
| **Related Decisions** | DR-034, DR-040, DR-054 |
| **Related Programmes** | EP-004 private beta, EP-007.3, P-003.1 |

---

## PR-004 — Premature Version 1 production-ready declaration

| Field | Content |
|---|---|
| **Category** | Release · Governance |
| **Status** | ACTIVE (controlled) |
| **Prior ID** | R4 |
| **Description** | Pressure to declare Version 1 production-ready while G1 FAIL and G1–G12 package incomplete. Shipping a build or completing ops GA must not be reinterpreted as Version 1 ready. |
| **Evidence** | `Risk_Summary.md` R4; P-003.1 dossier board recommendation **NO GO**; `Release_Gates.md`; DR-030, DR-031, DR-041; P-002.1 Release Framework |
| **Likelihood** | Medium without board discipline; Low while NO GO held |
| **Impact** | Critical |
| **Overall Rating** | **Amber** — Medium × Critical with control adjustment (NO GO enforced today) |
| **Current Controls** | Hard-gate FAIL → overall NO-GO (DR-031); three separable verdicts (DR-032); dossier NO GO (DR-041); this Risk Register |
| **Remaining Exposure** | Regulatory/reputational harm and wrong go-to-market if discipline breaks |
| **Owner** | Product Board |
| **Review Trigger** | Any proposal to declare V1 ready; G1 status change; commercial launch request |
| **Closure Criteria** | G1 PASS (or approved HOLD path that does not overclaim) and remaining hard gates PASS/HOLD under P-002.1; board GO recorded |
| **Related Decisions** | DR-030, DR-031, DR-032, DR-041 |
| **Related Programmes** | P-002.1, P-003.1, P-003.2 |

---

# Part B — Evidence and cohort chain

---

## PR-005 — Cold-start / sparse-evidence overconfidence

| Field | Content |
|---|---|
| **Category** | Educational · Product |
| **Status** | ACTIVE |
| **Prior ID** | R5 |
| **Description** | Students (especially cold-start / sparse session evidence) may receive readiness, plan, or confidence signals that feel more certain than evidence warrants. Overconfidence risk for resitters is repeatedly cited in Tier B / journey reviews. |
| **Evidence** | `Risk_Summary.md` R5; readiness honesty / refusal path (EP-003.2, EP-006.4/006.5); prefer-lower notes; EP-005.2 student journey review overconfidence themes; DR-004 / DR-018 risks |
| **Likelihood** | Medium |
| **Impact** | Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | Unknown remains unknown; honest refusal; Exam Ready marketing ban (DR-035); Readiness ≠ Next Action (DR-018); no Exam Ready theatre |
| **Remaining Exposure** | Residual sparse-session content and composite unpacking gaps; presentation must keep honesty adjacent |
| **Owner** | Product (Educational experience) |
| **Review Trigger** | Readiness cutover ON; Exam Ready marketing request; new Tier B overconfidence codes |
| **Closure Criteria** | Validated honesty path retained under production defaults; no Exam Ready / soothing-composite regressions in declaration spot-checks |
| **Related Decisions** | DR-004, DR-018, DR-035 |
| **Related Programmes** | EP-003.2, EP-005.2, EP-006.4, EP-006.5 |

---

## PR-006 — External cohort unavailable; evidence floors unmet

| Field | Content |
|---|---|
| **Category** | Evidence · Adoption |
| **Status** | ACTIVE |
| **Prior ID** | R6 |
| **Description** | External cohort N = **0**. Conditions C4–C6 (≥20 path, ≥4 weeks measurement, interview floors) remain unmet. Educational GO is impossible under EP-003/004 rules until floors are met or a written waiver with claim restrictions is approved. |
| **Evidence** | `knowledge/product/ep004_private_beta/BETA_COHORT.md` (External N=0; Stage 1 HOLD); `ep007_3_.../COHORT_EVIDENCE_REGISTER.md` (CE absences); `GO_NO_GO_DECISION.md` C4–C6; `Risk_Summary.md` R6; DR-022 |
| **Likelihood** | High (while privacy blocks ops) |
| **Impact** | High |
| **Overall Rating** | **Red** |
| **Current Controls** | Explicit HOLD on Stage 1; staff/dogfood N must not inflate exit bar; claim freezes |
| **Remaining Exposure** | G1.9 remains FAIL indefinitely if privacy/recruitment chain stalls |
| **Owner** | Product (Private beta ops) |
| **Review Trigger** | PR-003 closed; first external invite accepted; weekly scorecard N updates |
| **Closure Criteria** | Documented external N/duration/interview floors met (or approved waiver); COHORT_EVIDENCE_REGISTER updated from ABSENT |
| **Related Decisions** | DR-022, DR-040 |
| **Related Programmes** | EP-004, EP-007.3, EP-003 educational effectiveness |

---

## PR-007 — Stage 1 / Stage 2 recruitment blocked on privacy (not a recruitment failure)

| Field | Content |
|---|---|
| **Category** | Adoption · Privacy |
| **Status** | ACTIVE |
| **Prior ID** | — (companion to R3/R6; brief “beta recruitment” theme) |
| **Description** | Stage 1/2 external recruitment is on **HOLD** pending privacy sign-off. There is **no** evidenced failed recruitment campaign; the risk is a blocked precondition that can starve Version 1 evidence if prolonged. |
| **Evidence** | `BETA_COHORT.md` Stage 1 HOLD; `GO_NO_GO_DECISION.md` C1/C4; `PRIVATE_BETA_PROTOCOL.md` (expansion pending privacy); EP-004 `LESSONS_LEARNED.md` |
| **Likelihood** | High |
| **Impact** | High |
| **Overall Rating** | **Red** — same chain as PR-003/PR-006 |
| **Current Controls** | Protocol approved for ops design; dogfood/founder accounts under internal rules; invite-only |
| **Remaining Exposure** | Calendar slip of effectiveness evidence; pressure to count staff as external N |
| **Owner** | Product (Private beta ops) |
| **Review Trigger** | Privacy signatures; invite list approved; first acceptance |
| **Closure Criteria** | Stage 1 invites issued under signed privacy; external N path documented toward C4 |
| **Related Decisions** | DR-034, DR-040 |
| **Related Programmes** | EP-004, EP-007.3 |

**Note:** Do not retitle this as “beta recruitment failure” — repository evidence shows HOLD, not a failed campaign.

---

## PR-008 — Confidence Medium ceiling without external corroboration

| Field | Content |
|---|---|
| **Category** | Evidence |
| **Status** | ACTIVE |
| **Prior ID** | R10 |
| **Description** | Tier B / validated KSI confidence remains **Medium**. G1.2 may PASS at Medium, but High-confidence declaration narratives and aggressive marketing require external corroboration. |
| **Evidence** | `Risk_Summary.md` R10; EP-006/007.2 confidence notes; `ep007_3_.../CONFIDENCE_UPDATE.md`; G1.2 PASS but not High |
| **Likelihood** | High |
| **Impact** | Medium |
| **Overall Rating** | **Red** — High × Medium per matrix |
| **Current Controls** | Prefer-lower; Medium accepted for G1.2 PASS; marketing claim limits |
| **Remaining Exposure** | Cannot reach High-confidence G1 without external N + re-score |
| **Owner** | Product (Validation) |
| **Review Trigger** | External cohort evidence lands; independent re-score (PR-013) |
| **Closure Criteria** | Confidence band raised under published rules with external corroboration, or claim language permanently capped at Medium |
| **Related Decisions** | DR-027, DR-051 |
| **Related Programmes** | EP-006.*, EP-007.2, EP-007.3 |

---

## PR-009 — Independent KSI re-score (G1.7) unfinished

| Field | Content |
|---|---|
| **Category** | Evidence · Governance |
| **Status** | ACTIVE |
| **Prior ID** | R13 |
| **Description** | Gate G1.7 independent / second-assessor KSI re-score remains **HOLD**. Even if KSI later reaches ≥80, declaration can remain blocked until G1.7 clears. |
| **Evidence** | `Risk_Summary.md` R13; `Release_Gates.md` G1.7 HOLD; P-002.1 evidence requirements |
| **Likelihood** | Very High (until staffed) |
| **Impact** | Medium |
| **Overall Rating** | **Red** — Very High × Medium |
| **Current Controls** | Explicit HOLD status; no silent claim of dual-assessor confidence |
| **Remaining Exposure** | Declaration blocked even after KSI≥80 if G1.7 unfinished |
| **Owner** | Product Board (second assessor staffing) |
| **Review Trigger** | Second assessor assigned; dual score published |
| **Closure Criteria** | G1.7 PASS (or approved HOLD with claim restrictions) |
| **Related Decisions** | DR-051, DR-030 |
| **Related Programmes** | EP-005.1, P-002.1, P-003.1 |

---

# Part C — Operational, deployment, and flag risks

---

## PR-010 — Production load / performance claims unverified

| Field | Content |
|---|---|
| **Category** | Operational · Technical |
| **Status** | ACTIVE |
| **Prior ID** | R7 |
| **Description** | Gate G7 production load test is **NOT STARTED**. CI soft budgets and Stage 0 stability are positive but insufficient for high-traffic performance claims. |
| **Evidence** | `Risk_Summary.md` R7; `Release_Gates.md` G7 IN PROGRESS; `knowledge/VERSION_1_READINESS.md` Performance |
| **Likelihood** | Medium (if traffic grows or claims escalate) |
| **Impact** | Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | Invite-only traffic limits; claim language must not assert load-tested production capacity; CI budgets green |
| **Remaining Exposure** | Outage / degraded study sessions under unexpected load |
| **Owner** | Engineering (ops) |
| **Review Trigger** | Public/high-traffic proposal; production sampling plan |
| **Closure Criteria** | Production load sample completed and packaged for G7, or HOLD with explicit traffic claim limits |
| **Related Decisions** | DR-030, DR-034 |
| **Related Programmes** | P-002.1, P-003.1 |

---

## PR-011 — Telemetry / Journey-emit overclaim while gated OFF

| Field | Content |
|---|---|
| **Category** | Operational · Governance |
| **Status** | ACTIVE (controlled) |
| **Prior ID** | R8 |
| **Description** | Analytics / Journey emit remains deferred (flag OFF). Treating gated metrics as “live KPIs” would drive false product decisions. |
| **Evidence** | `Risk_Summary.md` R8; `Release_Gates.md` G9 COMPLETE (flag OFF); DR-047 |
| **Likelihood** | Medium without claim discipline |
| **Impact** | Medium |
| **Overall Rating** | **Amber** — controlled toward Green if honesty held |
| **Current Controls** | DR-047 claim language must match flag state; G9 honesty |
| **Remaining Exposure** | Dashboarding deferred metrics as live |
| **Owner** | Product + Analytics |
| **Review Trigger** | Journey emit flag ON; KPI dashboard proposals |
| **Closure Criteria** | Either flag ON with verified emit + documented KPIs, or permanent claim exclusion of deferred metrics |
| **Related Decisions** | DR-047 |
| **Related Programmes** | Analytics activation / EP-002 telemetry lineage |

---

## PR-012 — Feature-flag matrix / rollback unreadiness for ON defaults (G12)

| Field | Content |
|---|---|
| **Category** | Deployment · Release |
| **Status** | ACTIVE |
| **Prior ID** | R9 |
| **Description** | Architecture defines fail-open rollback for Twin/cutover. Gate **G12 is not scored** as a declaration board: Version 1 flag matrix and kill-switch documentation for high-risk educational flags are incomplete for ON-default claims. Casual flag flips risk dual truths. |
| **Evidence** | `Risk_Summary.md` R9; `Release_Gates.md` G12 Not scored; DR-009, DR-043; P-002.1 `VERSION_1_EVIDENCE_REQUIREMENTS.md` flag matrix requirement |
| **Likelihood** | Medium (if flags flipped casually) |
| **Impact** | Medium (High if educational flags ON without matrix) |
| **Overall Rating** | **Amber** (escalates to **Red** if ON defaults proposed without matrix) |
| **Current Controls** | Production defaults Twin/cutover/personalisation OFF; fail-open legacy; production hard-gate (DR-010); soak/rollback drills exist for Twin paths in architecture programmes |
| **Remaining Exposure** | Dual educational truths; unsafe student-visible behaviour if ON without G12 |
| **Owner** | Engineering + Product |
| **Review Trigger** | Any proposal to flip educational flags ON as production default |
| **Closure Criteria** | Published Version 1 flag matrix with owners, defaults, student-visible?, rollback switch, soak prerequisites; G12 PASS/HOLD |
| **Related Decisions** | DR-009, DR-010, DR-039, DR-043 |
| **Related Programmes** | EP-002.*, P-002.1, P-003.1 |

---

## PR-013 — Rollback drill / reliability packaging incomplete (G8)

| Field | Content |
|---|---|
| **Category** | Deployment · Operational |
| **Status** | ACTIVE |
| **Prior ID** | — (G8 residual companion to R9) |
| **Description** | G8 Reliability is IN PROGRESS: health/smoke pass, but production load residual and rollback-drill / Sev-1 packaging notes remain outstanding for declaration. |
| **Evidence** | `Release_Gates.md` G8; `VERSION_1_READINESS.md` Reliability; architecture soak rollback artefacts (exist for Twin, not fully packaged as V1 declaration evidence) |
| **Likelihood** | Medium |
| **Impact** | Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | Fail-open flag-OFF rollback model; invite-only blast radius |
| **Remaining Exposure** | Incomplete reliability evidence package for high-traffic or ON-default claims |
| **Owner** | Engineering (ops) |
| **Review Trigger** | Declaration package assembly; Sev-1 incident; flag ON proposal |
| **Closure Criteria** | G8 PASS or HOLD with documented rollback drill note in evidence package |
| **Related Decisions** | DR-009, DR-030 |
| **Related Programmes** | P-002.1, EP-002 soak programmes, P-003.1 |

---

## PR-014 — Deployment / release execution vs declaration confusion

| Field | Content |
|---|---|
| **Category** | Release · Governance |
| **Status** | ACTIVE (controlled) |
| **Prior ID** | R11 |
| **Description** | Shipping a release tag, completing CI, or running a playbook must not be interpreted as Version 1 production-ready declaration. |
| **Evidence** | `Risk_Summary.md` R11; DR-032 three separable verdicts; Release Playbook vs P-002.1 split noted in Risk_Summary |
| **Likelihood** | Medium without process discipline |
| **Impact** | Medium |
| **Overall Rating** | **Amber** — controlled if process held |
| **Current Controls** | Separate “ship build” from “declare V1”; DR-032; dossier/register/risk register trinity |
| **Remaining Exposure** | External stakeholders treat a ship as V1 ready |
| **Owner** | Product Board |
| **Review Trigger** | Release communications; tag naming; press/commercial copy |
| **Closure Criteria** | Standing communications checklist separating ship vs declare; no observed conflation in board minutes |
| **Related Decisions** | DR-032, DR-041 |
| **Related Programmes** | P-002.1, P-003.1 |

---

## PR-015 — Support / commercial unreadiness for public launch

| Field | Content |
|---|---|
| **Category** | Operational · Adoption |
| **Status** | ACCEPTED |
| **Prior ID** | R12 |
| **Description** | Commercial readiness NOT STARTED; support is founder-operated. Public launch would risk student abandonment and support failure. |
| **Evidence** | `Risk_Summary.md` R12; `VERSION_1_READINESS.md` Support / Commercial NOT STARTED |
| **Likelihood** | High **if** public launch attempted; Low under invite-only |
| **Impact** | Medium |
| **Overall Rating** | **Amber** residual; **Green** operating posture under invite-only NO GO |
| **Current Controls** | Invite-only; no public registration (DR-034); NO GO declaration |
| **Remaining Exposure** | Acceptable under current mode; becomes Red if public launch attempted |
| **Owner** | Product + Founder ops |
| **Review Trigger** | Public registration proposal; paid launch; support volume growth |
| **Closure Criteria** | Staged support rota + commercial readiness artefacts for the intended launch class — or permanent invite-only claim |
| **Related Decisions** | DR-034, DR-041 |
| **Related Programmes** | P-003.1, VERSION_1_READINESS |

---

# Part D — Claim-language and product honesty

---

## PR-016 — Personalisation / Twin capabilities marketed while flags OFF

| Field | Content |
|---|---|
| **Category** | Governance · Product |
| **Status** | ACTIVE (controlled) |
| **Prior ID** | R14 |
| **Description** | Personalisation and Twin paths exist but production defaults keep flags OFF. Marketing or UI copy implying live personalisation / Twin intelligence is a dishonest product promise and unsupported ΔKSI. |
| **Evidence** | `Risk_Summary.md` R14; EP-005.1 unsupported personalisation Δ while OFF; DR-006, DR-009, DR-039 |
| **Likelihood** | Medium without G12/copy discipline |
| **Impact** | High |
| **Overall Rating** | **Amber** — control adjustment from Red while claim exclusions enforced |
| **Current Controls** | Flags OFF (DR-039/DR-009); claim language excludes OFF capabilities; G12 matrix discipline required before ON |
| **Remaining Exposure** | UI/marketing drift; K4 claims without ON defaults + cohort evidence |
| **Owner** | Product |
| **Review Trigger** | Marketing review; flag ON proposal; K4 claim in roadmap |
| **Closure Criteria** | Either flags ON with G12 + effectiveness evidence, or audited claim surface with zero OFF-capability promises |
| **Related Decisions** | DR-006, DR-009, DR-039, DR-043 |
| **Related Programmes** | EP-004.*, EP-005.1, P-003.1 |

---

## PR-017 — Sparse onboarding / orientation content

| Field | Content |
|---|---|
| **Category** | Adoption · Educational |
| **Status** | ACTIVE |
| **Prior ID** | — (brief “sparse onboarding”; FB-008) |
| **Description** | Private-beta feedback records orientation confusion (Journey vs History vs Revision). Sparse onboarding/orientation content increases early abandonment and decision burden the product claims to remove. |
| **Evidence** | `knowledge/product/ep004_private_beta/FEEDBACK_REGISTER.md` FB-008 (Open); EP-005.2 journey review decision-burden themes; cold-start adjacency to PR-005 |
| **Likelihood** | Medium |
| **Impact** | Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | Protocol First Session guidance; canonical Home (DR-007); journey consolidation (EP-007.1) reduces dual-home confusion |
| **Remaining Exposure** | Orientation still needed for secondary surfaces; FB-008 open |
| **Owner** | Product (Experience) |
| **Review Trigger** | New FB orientation codes; Stage 1 onboarding scorecards |
| **Closure Criteria** | FB-008 closed with verified orientation path; Stage 1 onboarding success ops metric met (≥1 productive Session within 7 days per protocol) for sampled cohort |
| **Related Decisions** | DR-007, DR-020 |
| **Related Programmes** | EP-004, EP-005.2, EP-007.1 |

---

## PR-018 — Coach / Session naming and Twin trust perception

| Field | Content |
|---|---|
| **Category** | Educational · Adoption |
| **Status** | WATCH |
| **Prior ID** | — (FB-001, FB-003) |
| **Description** | Feedback flags Coach/Session naming trust risk and Twin “made up” readiness perception risk. Not a declaration hard-blocker alone, but can erode K2/K3/K8 if unaddressed when Twin/personalisation surfaces expand. |
| **Evidence** | `FEEDBACK_REGISTER.md` FB-001 (Open), FB-003 (Watch); DR-035 Exam Ready ban; readiness honesty path |
| **Likelihood** | Medium |
| **Impact** | Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | Honesty copy; Twin OFF in production defaults; Exam Ready ban |
| **Remaining Exposure** | Naming/trust residuals in open feedback |
| **Owner** | Product (Experience) |
| **Review Trigger** | Twin ON in any student-visible cohort; naming IA change |
| **Closure Criteria** | FB-001/FB-003 closed or accepted with claim limits; no unsupported Twin trust claims |
| **Related Decisions** | DR-001, DR-004, DR-035 |
| **Related Programmes** | EP-004 private beta, EP-006.* |

---

# Part E — Gate incompleteness and governance hygiene

---

## PR-019 — Release gate package incompleteness (G2–G12 residuals)

| Field | Content |
|---|---|
| **Category** | Release · Governance |
| **Status** | ACTIVE |
| **Prior ID** | — (umbrella for brief “release gate incompleteness”; dossier gates) |
| **Description** | Beyond G1 FAIL, multiple gates remain Partially met / IN PROGRESS / Not scored: G2 EVF claim-class approval, G3 explainability spot-check pack, G4 recommendation scorecard instrumentation, G7/G8/G10 residuals, G12 unscored. Incomplete package blocks honest declaration even if single narratives improve. |
| **Evidence** | P-003.1 `Release_Gates.md`; `Version_1_RELEASE_DOSSIER.md` §7; DR-030 |
| **Likelihood** | High (current state) |
| **Impact** | High |
| **Overall Rating** | **Red** |
| **Current Controls** | P-002.1 hard-gate rules; NO GO; per-gate HOLD allowed only without overclaim |
| **Remaining Exposure** | Partial narrative wins mistaken for full package |
| **Owner** | Product Board |
| **Review Trigger** | Any gate status change; declaration proposal |
| **Closure Criteria** | G1–G12 all PASS or approved HOLD under P-002.1 with packaged evidence |
| **Related Decisions** | DR-030, DR-031, DR-041 |
| **Related Programmes** | P-002.1, P-003.1 |

---

## PR-020 — Constitutional / EVF compliance not APPROVED for V1 claim class (G2)

| Field | Content |
|---|---|
| **Category** | Governance · Release |
| **Status** | ACTIVE |
| **Prior ID** | — (G2 detail under PR-019) |
| **Description** | Gate G2 remains IN PROGRESS: EVF / constitutional compliance outcome not APPROVED for the Version 1 claim class. |
| **Evidence** | `Release_Gates.md` G2; DR-024, DR-045 |
| **Likelihood** | Medium |
| **Impact** | High |
| **Overall Rating** | **Red** |
| **Current Controls** | Educational Constitution highest educational law; EVF outside decision path (DR-045) |
| **Remaining Exposure** | Claim-class approval gap |
| **Owner** | Product Board + Educational governance |
| **Review Trigger** | EVF outcome published for V1 claim class |
| **Closure Criteria** | G2 PASS/HOLD with APPROVED (or equivalent) artefact cited |
| **Related Decisions** | DR-024, DR-045, DR-030 |
| **Related Programmes** | P-002.1, EGI/EVF lineage, P-003.1 |

---

## PR-021 — Documentation drift between companion release artefacts

| Field | Content |
|---|---|
| **Category** | Governance · Evidence |
| **Status** | ACTIVE |
| **Prior ID** | — (brief “documentation drift”) |
| **Description** | Companion docs can diverge. Concrete example: P-003.1 `Version_1_RELEASE_DOSSIER.md` §8 embeds an older R1–R10 table that does not match canonical `Risk_Summary.md` R1–R14 numbering/wording. Historical TD-ARCH-06 and RC2 residuals also cite documentation drift. Drift creates board confusion and false closure. |
| **Evidence** | `Version_1_RELEASE_DOSSIER.md` §8 vs `Risk_Summary.md`; `knowledge/architecture/ep001_5_architectural_integration_review/COMPLETION_REPORT.md` TD-ARCH-06; RC2 operational readiness residual notes |
| **Likelihood** | Medium |
| **Impact** | Low–Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | This register designates `Risk_Summary` + `PR-NNN` as risk ID authority for Version 1; Decision Register for DR IDs; authority hierarchy (DR-023) |
| **Remaining Exposure** | Stale embedded tables in dossiers until next docs sync programme |
| **Owner** | Product (documentation) |
| **Review Trigger** | New dossier/register revision; conflicting ID citations in board papers |
| **Closure Criteria** | Dossier §8 reconciled to Risk_Summary/PR IDs; no conflicting active risk ID schemes in board packs |
| **Related Decisions** | DR-023 |
| **Related Programmes** | P-003.1, P-003.2, P-003.3 |

---

## PR-022 — Shadow constitution / constitutional bypass pressure (“governance drift”)

| Field | Content |
|---|---|
| **Category** | Governance |
| **Status** | WATCH |
| **Prior ID** | — (brief “governance drift”; DR-023/024 forward risks) |
| **Description** | No evidenced open *incident* of governance drift. Residual exposure: programme folders inventing shadow constitutions, or feature programmes bypassing constitutional verification — named as risks on DR-023/DR-024. |
| **Evidence** | DR-023 Risks field; DR-024 Risks field; `GOVERNANCE.md` hierarchy (read-only reference) |
| **Likelihood** | Low–Medium |
| **Impact** | High |
| **Overall Rating** | **Amber** |
| **Current Controls** | Document authority hierarchy; Educational Constitution as highest educational law; SIA / explainability / recommendation review mandates |
| **Remaining Exposure** | Future programmes could bypass unless reviews enforce hierarchy |
| **Owner** | Product Board |
| **Review Trigger** | New programme proposing educational law without constitution/EVF path; conflicting local “constitutions” |
| **Closure Criteria** | No active shadow-law artefacts; constitutional verification recorded on educational programmes |
| **Related Decisions** | DR-023, DR-024, DR-037 |
| **Related Programmes** | P-001.*, P-002.1, governance index |

**Note:** Registered as WATCH residual exposure — not as an observed drift incident.

---

## PR-023 — Security CSP / dependency residuals (G10)

| Field | Content |
|---|---|
| **Category** | Technical · Privacy |
| **Status** | ACTIVE |
| **Prior ID** | — (G10 residual) |
| **Description** | G10 Security IN PROGRESS: GA review pass exists, but CSP hardening beyond `'unsafe-inline'` and related residuals remain; Stage 1 privacy signatures also sit on the security/privacy path (see PR-003). |
| **Evidence** | `Release_Gates.md` G10; `VERSION_1_READINESS.md` Security NOT STARTED items (CSP hardening); historical RC2 CSP fix (closed separately) |
| **Likelihood** | Low–Medium |
| **Impact** | Medium |
| **Overall Rating** | **Amber** |
| **Current Controls** | Prior CSP critical fix closed; invite-only; Flask security headers baseline |
| **Remaining Exposure** | Residual CSP/dependency policy for declaration package |
| **Owner** | Engineering (security) |
| **Review Trigger** | Declaration package; dependency CVE; CSP change |
| **Closure Criteria** | G10 PASS/HOLD with residuals explicitly accepted or remediated |
| **Related Decisions** | DR-030 |
| **Related Programmes** | GA / VERSION_1_READINESS, P-003.1 |

---

## PR-024 — Pass-rate (Vision north-star) measurement methodology undefined

| Field | Content |
|---|---|
| **Category** | Evidence · Educational |
| **Status** | ACTIVE |
| **Prior ID** | — (`VERSION_1_READINESS` Analytics; DR-046) |
| **Description** | Pass-rate measurement methodology remains NOT STARTED. Distinct from KSI gap (DR-046): even with KSI≥80, Vision 2030 north-star measurement would remain undefined. |
| **Evidence** | `knowledge/VERSION_1_READINESS.md` Analytics / pass-rate methodology; DR-046; Framework O9 open notes in readiness |
| **Likelihood** | High for north-star claims; Low for near-term KSI-only board work |
| **Impact** | High (for Vision claims); Medium (for V1 KSI declaration alone) |
| **Overall Rating** | **Amber** for Version 1 declaration scope; escalates if pass-rate claims made |
| **Current Controls** | KSI does not replace Vision north star (DR-046); no pass-rate marketing |
| **Remaining Exposure** | Long-term measurement gap |
| **Owner** | Product (Validation) |
| **Review Trigger** | Any pass-rate / exam-outcome marketing; O9 programme start |
| **Closure Criteria** | Published methodology + measurement plan for intended claim class — or explicit non-claim |
| **Related Decisions** | DR-046, DR-021 |
| **Related Programmes** | Vision, VERSION_1_READINESS, EP-001 O9 lineage |

---

# Part F — Architecture integrity (watch / accepted)

---

## PR-025 — Second / opaque educational brain creep

| Field | Content |
|---|---|
| **Category** | Educational · Technical |
| **Status** | WATCH |
| **Prior ID** | — (EP-003.4 / EP-004 RISK_ASSESSMENT themes) |
| **Description** | Profile, feedback loop, MissionOptimizer, or presentation must not become a second educational authority. Programme exits rated residual acceptable while flags OFF and ownership contracts hold. |
| **Evidence** | EP-004.1–004.3 `RISK_ASSESSMENT.md`; EP-003.4 `RISK_ASSESSMENT.md`; DR-006, DR-015, DR-016, DR-038, DR-049 |
| **Likelihood** | Low–Medium while OFF; Medium if ON without re-certification |
| **Impact** | Critical (if realised) |
| **Overall Rating** | **Amber** (WATCH; control-dependent) |
| **Current Controls** | Runtime A sole authority; Twin quarantine; personalisation tertiary; feedback record-only OFF; MissionOptimizer quarantined; constitutional verification |
| **Remaining Exposure** | Flag ON without ownership re-certification |
| **Owner** | Architecture + Product |
| **Review Trigger** | Any educational flag ON as production default; new “brain” service proposal |
| **Closure Criteria** | Re-certified ownership under EP-002.9 rules for any new student-visible authority path |
| **Related Decisions** | DR-001, DR-006, DR-015, DR-016, DR-038, DR-049 |
| **Related Programmes** | EP-002.9, EP-003.4, EP-004.* |

---

## PR-026 — Process-local state loss on restart (profile / metrics)

| Field | Content |
|---|---|
| **Category** | Technical · Operational |
| **Status** | ACCEPTED |
| **Prior ID** | — (EP-004.1 R9; EP-002.9 RX-02 class) |
| **Description** | Personal learning profile / some observational state is process-local and can be lost on restart. Accepted near-term residual for gated observational infrastructure; Low impact on Version 1 declaration while personalisation OFF. |
| **Evidence** | EP-004.1 `RISK_ASSESSMENT.md` R9; EP-002.9 risk register RX-02 class references |
| **Likelihood** | High |
| **Impact** | Low |
| **Overall Rating** | **Amber** → accepted residual (**Green** for declaration impact under OFF flags) |
| **Current Controls** | Personalisation OFF in W-PROD; no educational authority in profile APIs |
| **Remaining Exposure** | Durability required before personalisation ON defaults |
| **Owner** | Engineering |
| **Review Trigger** | Personalisation ON proposal; durable store design |
| **Closure Criteria** | Durable store + migration for profile state before ON defaults — or permanent acceptance documented in G12 matrix |
| **Related Decisions** | DR-039, DR-006 |
| **Related Programmes** | EP-004.1, EP-002.9 |

---

## PR-027 — Concentration of duties under founder operation

| Field | Content |
|---|---|
| **Category** | Governance · Operational |
| **Status** | ACCEPTED |
| **Prior ID** | — (GP-001) |
| **Description** | A single Founder holds Product Owner, Engineering Owner, Operations Owner, Privacy Owner, and Product Board Chair capacities. This concentrates approval power and reduces independent challenge relative to a staffed multi-role organisation. Accepted as current operating reality provided capacity-labelled Founder Reviews are filed and evidence requirements are not weakened. Does **not** satisfy gate law requiring an independent second natural person (e.g. G1.7). |
| **Evidence** | `knowledge/product/gp001_founder_governance_model/FOUNDER_GOVERNANCE_MODEL.md`; DR-054; PR-009 (G1.7) |
| **Likelihood** | Very High (current state) |
| **Impact** | Medium (governance quality) / High if reviews are skipped or evidence fabricated |
| **Overall Rating** | **Amber** — accepted residual under invite-only / founder-operated Stage 1 claim class |
| **Current Controls** | Capacity-labelled Founder Reviews; Approval Matrix; blank-until-real signatures; Evidence Hierarchy; hard-gate FAIL → NO-GO; Product Board authority preserved |
| **Remaining Exposure** | Founder self-dealing optimism; missed G1.7 independence; privacy competence gaps without counsel |
| **Owner** | Founder — Product Board Chair capacity |
| **Review Trigger** | Second operator/engineer hired; external Board member; public launch; multi-jurisdiction processing |
| **Closure Criteria** | Separation of at least one material capacity to a distinct natural person **or** permanent Board expansion documented — without relaxing evidence |
| **Related Decisions** | DR-054, DR-023, DR-030 |
| **Related Programmes** | GP-001 |

---

## End of full cards

**Active material set:** see [`ACTIVE_RISKS.md`](ACTIVE_RISKS.md).  
**Closed / fixed:** see [`CLOSED_RISKS.md`](CLOSED_RISKS.md).  
**ID maps:** see [`RISK_TRACEABILITY.md`](RISK_TRACEABILITY.md).

**Counts (this register):** 27 product risks (PR-001…PR-027).

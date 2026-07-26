# EP-007.3 — Stage 1 Cohort Design

**Programme:** EP-007.3 — Educational Effectiveness Validation (Stage 1 Cohort)  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Design COMPLETE — enrollment cleared; early-access wave **N=3 external** selected 2026-07-26 (exploratory under-size vs 5–10)  
**Governing protocol:** [`../ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md`](../ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md)  
**Cohort registry:** [`../ep004_private_beta/BETA_COHORT.md`](../ep004_private_beta/BETA_COHORT.md)  
**Does not:** Put PII in git; change runtime / UI; redefine M1–M9; claim educational effectiveness or full Stage 1 N floors  

---

## 1. Purpose of Stage 1

Stage 1 is a **small external pilot** that tests whether post–Runtime A improvements produce measurable study behaviour and educational-usefulness signals — distinct from Stage 0 dogfood and from Tier B perception packs.

| Question | Stage 0 | Perception (Tier B) | Stage 1 (this design) |
|---|---|---|---|
| Can staff use the product? | Yes | — | Assumed |
| Do students understand / trust surfaces? | Partial | Primary | Supporting interview codes |
| Do students study consistently / complete sessions / find it useful over weeks? | Exploratory only | No | **Primary** |

---

## 2. Participant selection

### 2.1 Inclusion

| Rule | Spec |
|---|---|
| Audience | IFoA (or designated) students preparing for in-scope subject |
| Priority subjects | CM2 and/or CS2 (curricula loadable V1/V2) |
| Size | **5–10** external invite-only (EP-004 Stage 1 target) |
| Account model | Invite-only; **no** public registration |
| Platform | W-PROD sole-runtime defaults (post–EP-007.1 path) |
| Exam window | Prefer dated exam proximity when available (aids M8/M9 interpretation) |
| Region | Prefer single primary privacy regime for first pilot |

### 2.2 Exclusion

| Rule | Spec |
|---|---|
| Cannot consent to privacy / measurement terms | Ineligible |
| Staff dogfood only | Does **not** count toward Stage 1 N unless marked participant **and** treated as internal (Stage 0) |
| Recommendation A/B experiment subjects | Out of scope — recommendations remain no-claim until separate PRD |

### 2.3 ID scheme

`BETA-PIL-001` … `BETA-PIL-010` (reserved in `BETA_COHORT.md`). Pseudonymous IDs only in evidence artefacts.

### 2.4 Current selection state (2026-07-26)

| Population | N | Status |
|---|---|---|
| Stage 0 internal participants | 3 | Active (not Stage 1 N) |
| Stage 1 invited / accepted | **0** | **HOLD** — Privacy Review unsigned (EP-004 C1) |
| Stage 2 | 0 | HOLD until Stage 1 exit |

---

## 3. Observation period

| Parameter | Spec |
|---|---|
| Personal start | Date of invite acceptance |
| Minimum window for **directional** claims | ≥2 weeks, ≥10 active (Metrics §4) — Stage 1 aspirational; often unmet |
| Minimum window for **product-decision / effectiveness GO** | ≥4 weeks, ≥20 active (Stage 2 / EP-003 G7) — **not** Stage 1 alone |
| Stage 1 success for *advancing ops* | ≥4 weeks measurement for ≥5 accepted pilots with ≥1 productive Session each; scorecards filed weekly |
| Check-ins | Week 1 activation; Week 2–3 consistency / reflection; Week 4+ structured interview |
| Scorecard cadence | Weekly M1–M4, M6–M7; bi-weekly M5; M8–M9 at window end |

**Assessment window for this programme (design review):** 2026-07-24 (EP-004 Week 0) → 2026-07-26 (post–EP-007.2). No external productive Sessions in window.

---

## 4. Success metrics

Mapped to EP-003 Educational Metrics and Stage 1–relevant proxies. Targets are **provisional** until a live baseline week exists.

### 4.1 Primary behavioural metrics

| ID | Metric | Stage 1 target (directional) | Notes |
|---|---|---|---|
| M6 | Study consistency (rolling) | Mean ≥0.50 over available weeks (relax vs 0.60 until N≥20) | Primary “sustained behaviour” signal |
| M4 | Session completion (completed/started) | ≥70% (relax vs 75% until week 4 + N≥20) | Mission completion |
| M2 | Sessions per WAL | Median ≥1.5 / week early; track toward ≥2 | Intensity |
| M1 | WAL among accepted | ≥60% of accepted remain WAL by week 3 of personal start | Retention of productive use |
| M3 | Reflection completion | ≥70% when reflection required | Learning loop |
| M7 | Continuity (WoW) | ≥60% post week 1 among pilots | Dropout watch |

### 4.2 Educational usefulness / preparedness (qualitative + proxy)

| Signal | Definition | Stage 1 target |
|---|---|---|
| Perceived preparedness | Interview: readiness / progress understood without false certainty | ≥70% Yes or Partial-with-Why among interviewed |
| Educational usefulness over time | Interview Final Test: “helped you study like a professional?” | ≥70% Yes among interviewed (N≥5 Stage 1; ≥8 for GO path) |
| Recommendation uptake | Follow-through on primary next action from Home / Session | **Observational only** — excluded from effectiveness marketing (EP-001 O8 freeze) |
| Recovery adherence | Return to Session after miss / fail night | Theme code + optional count; no vanity streak |

### 4.3 Explicitly out of Stage 1 claims

| Claim | Status |
|---|---|
| Exam pass-rate improvement | Forbidden (north star; separate methodology) |
| Recommendation-effectiveness marketing | Frozen |
| “Exam Ready” marketing | Forbidden without readiness gates |
| KSI ≥ 80 from Stage 1 alone | Impossible — Stage 1 clears claimability path for G1.9, not G1.1 |

---

## 5. Ethical and data considerations

| Topic | Rule |
|---|---|
| Privacy Review | **Must be signed** before any external invite (`../private_beta/PRIVACY_REVIEW.md`) — currently **unsigned** |
| Privacy notice | Honest scope: storage, analytics metadata/hashes (not reflection body), retention, support access |
| Measurement consent | Required for KPI inclusion; withdrawal → exclude from numerators |
| Interview / quote consent | Optional; decline does not remove study access |
| Analytics flag | Pilot ON only after EP-002 go-live Pilot checklist (EP-004 C2); prod default remains OFF until authorised |
| PII in reports | Pseudonymous IDs only; no emails/names in knowledge artefacts |
| Never-Build | No vanity engagement metrics as success; no opaque AI educational truth; no public registration |
| Support | P0/P1 same-day / immediate; no unresolved “cannot study” backlog before Stage 1 exit |
| Experiment control | No silent educational behaviour change (`EXPERIMENT_FRAMEWORK.md`) |

---

## 6. Confidence criteria

### 6.1 Evidence confidence bands (for effectiveness assessment)

| Band | Requirements |
|---|---|
| **High** | External N≥10 active ≥2 weeks **or** N≥20 ≥4 weeks; interviews ≥8 (or 25% active); M1–M4/M6–M7 filled; no honesty incident; Q1–Q5 all Yes |
| **Medium** | Stage 1 N 5–9 with ≥2 weeks scorecards **or** Strong Tier B + Stage 0 with explicit exploratory label; interviews partial; Q1–Q5 not all Yes |
| **Low** | External N=0; KPIs empty / exploratory; perception-only substitutes |

### 6.2 Gate G1.9 / educational GO confidence rule

| Outcome | Requires |
|---|---|
| Educational **GO** | EP-003 Q1–Q5 all Yes + C5–C6 (N≥20, ≥4 weeks, interview sample) + Privacy signed |
| **CONDITIONAL GO** | Named holds only; never waive external N floors by substituting Tier B |
| **NO-GO / PENDING EVIDENCE** | Any Insufficient on Q1–Q3, or N below floors, or privacy unsigned for claimed population |

### 6.3 What Tier B may and may not do

| Allowed | Forbidden |
|---|---|
| Support Q2 understandability / Q3 trust themes as *context* | Substitute for M1–M9 behavioural evidence |
| Raise KSI category confidence when paired with Tier A | Clear G1.9 alone |
| Inform remediation priority | Count as Stage 1 cohort N |

---

## 7. Ops gates before first invite

| # | Gate | Owner | Status 2026-07-26 |
|---|---|---|---|
| C1 | Privacy Review signatures | Product + Security / ops | **OPEN** |
| C2 | Analytics Pilot checklist before external flag ON | Ops | **OPEN** |
| C3 | Stage 0 monitoring GREEN; no open P0 | Ops / Product | **GREEN** (EP-004) |
| Design freeze | This document + metrics freeze | Product | **COMPLETE** |

---

## 8. Exit criteria for Stage 1 *ops* (future)

Stage 1 ops exit (advance toward Stage 2 / educational GO path) when:

1. Privacy Review signed; invites sent under protocol.  
2. ≥5 accepted pilots with ≥1 productive Session.  
3. ≥4 weekly scorecards filed with honest N labels.  
4. ≥3 structured interviews coded to M / Q IDs (full ≥8 deferred to GO path).  
5. No open P0/P1 study blockers.  
6. Effectiveness verdict updated (still may remain PENDING if floors unmet).  
7. No public registration.

**This programme does not claim Stage 1 ops exit.** It claims Stage 1 **design + assessment** exit with honest blocked-ops status.

---

## References

- [`../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md`](../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md)  
- [`../ep003_educational_effectiveness/GO_NO_GO_REPORT.md`](../ep003_educational_effectiveness/GO_NO_GO_REPORT.md)  
- [`../ep004_private_beta/GO_NO_GO_DECISION.md`](../ep004_private_beta/GO_NO_GO_DECISION.md)  
- [`../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md`](../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md) (REM-07)  

---

**End of COHORT_DESIGN**

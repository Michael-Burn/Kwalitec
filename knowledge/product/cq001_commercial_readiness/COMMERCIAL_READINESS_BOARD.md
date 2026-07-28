# Commercial Readiness Board

**Status:** Active — living board  
**Owner capacity:** Founder — Product Owner  
**Framework:** [`COMMERCIAL_READINESS_FRAMEWORK.md`](COMMERCIAL_READINESS_FRAMEWORK.md)  
**Baseline:** [`BASELINE_CRI_ASSESSMENT.md`](BASELINE_CRI_ASSESSMENT.md)  
**Update rule:** Refresh at every CRI-affecting programme start/completion and before any `cri-*` tag proposal.  
**Constraint:** Status index only — does not amend KSI, P-002.1 gates, or release artefacts.

---

## 1. Snapshot

| Field | Value |
|---|---|
| **Current CRI** | **53%** |
| **Validation** | **Provisional** |
| **As of** | 2026-07-28 |
| **Trend** | Flat (0) after CQ-007 confirmation |
| **Prior CRI** | 53% (CQ-006) |
| **Nearest tag** | `cri-50` — composite at provisional band; **tag not created** (validation required) |
| **Founder Adoption** | **🟡 GO WITH CONSTRAINTS** ([CQ-007](../cq007_founder_adoption_readiness/FOUNDER_ADOPTION_DECISION.md)) |
| **Founder Validated CRI** | **Not Started** — opens after Board acceptance of CQ-007 |
| **Current highest-priority programme** | **CQ-007** — completing |
| **Next recommended programme** | **Founder Validation** (Founder Validated CRI under GO WITH CONSTRAINTS) |

---

## 2. Domain scores

| ID | Domain | Weight | Score | Band | Blockers (active) |
|---|---|---:|---:|---|---|
| CR1 | Core Study Loop | 18 | 63 | Emerging | Strong-band needs founder dogfood; density residual Minor |
| CR2 | Daily Habit Fit | 14 | 57 | Emerging | Strong-band needs founder dogfood; prefs/density Minor |
| CR4 | Session Substance | 14 | 56 | Emerging | Scaffolded practice constraint (C-01); authored banks V2 |
| CR3 | Guidance Trust | 12 | 62 | Emerging | Strong-band observational follow-through / founder validation open |
| CR5 | Experience Cohesion | 10 | 57 | Emerging | Maintain sole-runtime; residual dual-run Contained |
| CR6 | Premium Craft | 8 | 56 | Emerging | Strong-band needs founder “proud to operate” dogfood |
| CR8 | Evidence Confidence | 10 | 25 | Weak | G1 FAIL; effectiveness NO-GO; N_external = 0 |
| CR7 | Operational Reliability | 8 | 68 | Strong | Maintain; G7 HOLD + ER2 residuals constrain claim class |
| CR9 | Commercial Envelope | 6 | 12 | Broken | Freezes; public registration/launch/pricing NOT STARTED |

**Composite:** 53.44 → **53%** (provisional). Confirmed by CQ-007 — no inflation.

---

## 3. Trend log

| Date | CRI | Δ | Validation | Programme | Note |
|---|---:|---:|---|---|---|
| 2026-07-28 | 43% | — | Provisional | CQ-001 | Baseline board opened |
| 2026-07-28 | 45% | +2 | Provisional | CQ-002 | Core loop polish; no `cri-45` tag |
| 2026-07-28 | 47% | +2 | Provisional | CQ-003 | Habit resume / Continue; no `cri-*` tag |
| 2026-07-28 | 49% | +2 | Provisional | CQ-004 | Session substance refinements; no `cri-*` tag |
| 2026-07-28 | 51% | +2 | Provisional | CQ-005 | Guidance trust continuity / wording; no `cri-*` tag |
| 2026-07-28 | 53% | +2 | Provisional | CQ-006 | Premium craft CSS/template polish; no `cri-*` tag |
| 2026-07-28 | 53% | 0 | Provisional | CQ-007 | Founder adoption **GO WITH CONSTRAINTS**; CRI confirmed; no `cri-*` tag |

---

## 4. Active blockers (cross-domain)

| ID | Blocker | Caps | Clearance path |
|---|---|---|---|
| C-01 | Scaffolded practice ≠ authored CS1 item banks | Exclusive content claim; CR4 Strong | Accept for V1 OS adoption; V2 banks later |
| B-CR1-01 | CR1 still Emerging (density / scarce-time continuity) | CR1 Strong | Founder Validation observations |
| B-CR2-02 | Habit fit Emerging — fresh-start density / prefs echo | CR2 Strong | Founder Validation; optional Minor polish |
| B-CR4-02 | Session substance Emerging — Strong needs dogfood / authored banks V2 | CR4 Strong | Founder Validation; V2 item banks later |
| B-CR3-02 | Guidance trust Emerging — Strong needs validated follow-through | CR3 Strong | Founder Validation |
| B-CR6-02 | Premium craft Emerging — Strong needs founder dogfood | CR6 Strong | Founder “proud to operate” validation |
| B-CR8-01 | Validated KSI 64; Gate G1 FAIL | CR8 | Educational evidence / Stage 1 path (not CR9 work) |
| B-CR8-02 | Effectiveness NO-GO; external N = 0 | CR8 | Privacy + Stage 1 enrollment when HOLD clears |
| B-CR7-01 | G7 performance HOLD | CR7 claims | Load evidence programme when justified |
| B-CR9-01 | Commercial freezes / NOT STARTED | CR9 | Only after higher domains + claim freezes permit |

---

## 5. Programme focus

| Role | Programme | Domains | Expected ΔCRI | Status |
|---|---|---|---|---|
| Completing | CQ-007 Founder Adoption Readiness | CR1–CR6 adoption lens | **0** (confirm 53%) | Completing |
| Next recommended | **Founder Validation** | CR1–CR6 → Founder Validated CRI | TBD (validation, not provisional inflate) | Proposed — starts after Board acceptance |
| Closed phase | Commercial Quality engineering (CQ-001–CQ-007) | — | +10 provisional (43→53) | Complete pending Board accept |
| Deferred | Non-CRI / V2 ideas | — | — | [`VERSION_2_BACKLOG.md`](VERSION_2_BACKLOG.md) |

---

## 6. Tag readiness

| Tag | Threshold | Ready? | Notes |
|---|---:|---|---|
| `cri-45` | 45% validated | **No** | Composite ≥45% **provisional only** |
| `cri-50` | 50% validated | **No** | Composite 53% provisional — not validated |
| `cri-60` | 60% validated | No | |
| `cri-70` | 70% validated | No | |
| `cri-80` | 80% validated | No | |
| `cri-90` | 90% validated | No | |
| `v1.0.0` | CRI maturity + P-002.1 GO | No | CRI alone insufficient |

---

## 7. How to update this Board

1. Complete programme CRI sections (domains, ΔCRI, evidence, blockers, provisional/validated).  
2. Recompute composite with framework weights.  
3. Append trend log row.  
4. Refresh next recommended programme using priority order.  
5. Propose tags only when validated threshold is met — never prematurely.

If this Board conflicts with a cited authoritative artefact, **the cited source wins** — then fix this Board.

---

**End of Commercial Readiness Board**

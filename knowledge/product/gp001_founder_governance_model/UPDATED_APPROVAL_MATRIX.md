# Updated Approval Matrix

**Programme:** GP-001 — Founder Governance Model  
**Version:** 1.0  
**Effective:** 2026-07-26  
**Companion:** [`FOUNDER_GOVERNANCE_MODEL.md`](FOUNDER_GOVERNANCE_MODEL.md) · [`ROLE_MAPPING.md`](ROLE_MAPPING.md)  
**Does not:** Change evidence artefacts, dry-run requirements, or gate PASS criteria  

---

## 1. How to read this matrix

| Column | Meaning |
|---|---|
| **Decision / gate** | What is being approved |
| **Evidence still required** | Unchanged proof — **do not skip** |
| **Prior approval theatre** | Multi-person labels previously written |
| **Founder-operated approval** | Who signs and in which capacity |
| **Record form** | Founder Review fields |

**Rule:** Approval ownership changes. Evidence requirements do not.

---

## 2. Stage 1 / privacy / ops

| Decision / gate | Evidence still required | Prior approval theatre | Founder-operated approval | Record form |
|---|---|---|---|---|
| **OR-01 / CE-01** Privacy Review | Completed Privacy Sign-off Package; honest notice; inventory; consent wording | Product signature + Security/ops signature | **Two** Founder Reviews: (1) Product Owner (2) Privacy Owner | Reviewer · Date · Decision · Notes (capacity) |
| **OR-02 / CE-03** Export dry-run | `GO_LIVE_CHECKLIST.md` §E1 Pass log | Ops / Export SLA owner | Founder Review — Operations Owner | Reviewer · Date · Decision · Notes |
| **OR-02 / CE-04** Deletion dry-run | §E2 Pass + audit Yes | Ops / Deletion SLA owner | Founder Review — Operations Owner | Reviewer · Date · Decision · Notes |
| **OR-02 / CE-05** Kill-switch rehearsal | §E3 + Rollback §3.3 Pass | Ops / on-call | Founder Review — Operations Owner | Reviewer · Date · Decision · Notes |
| **CE-02** Named operational owners | §E4 names + dates | Product + Ops confirmation | Founder Review — Operations Owner (may name self) | Reviewer · Date · Decision · Notes |
| **Stage 1 enrollment clearance** | G-S1-1…G-S1-7 evidenced; Critical CE-01…CE-05 EVIDENCED | Product + Security/ops clearance table | Founder Review — Product Board Chair (after capacity reviews) | Reviewer · Date · Decision · Notes |
| **Pilot C1 / C2 decision** | Activation log + measurement label honesty | Product decision | Founder Review — Product Owner | Reviewer · Date · Decision · Notes |

---

## 3. Version 1 production-ready declaration

| Decision / gate | Evidence still required | Prior approval theatre | Founder-operated approval | Record form |
|---|---|---|---|---|
| **G1** Validated KSI | Validated KSI package ≤90 days; criteria G1.1–G1.10 | Product owner | Founder Review — Product Owner | Reviewer · Date · Decision · Notes |
| **G1.7** Independent re-score | Second assessor within ±3 **or** HOLD / dispute path per P-002.1 | Independent assessor | **Not** satisfied by Founder dual-capacity alone | Second person **or** HOLD |
| **G2** Constitutional / EVF | Compliance memo + EVF outcome | Product + Educational + Architecture | Founder Reviews: Product Owner; Educational Gate Owner; Engineering Owner (architecture lens) | One row per capacity |
| **G3–G4** Explainability / Recommendation | Checklists / scorecards | Product + Educational | Founder Reviews: Product Owner + Educational Gate Owner | Per capacity |
| **G5–G6** Planning / Readiness quality | Quality packs | Product + Engineering | Founder Reviews: Product Owner + Engineering Owner | Per capacity |
| **G7–G9, G11–G12** Perf / reliability / telemetry / tests / flags | Technical packs + HOLD rules | Engineering (+ Product/Release as scoped) | Founder Reviews: Engineering Owner; Product Owner; Operations Owner (release) as scoped | Per capacity |
| **G10** Security / data integrity | Security review + residuals | Security / Engineering | Founder Reviews: Privacy Owner (security lens) + Engineering Owner | Per capacity |
| **Overall GO / NO GO recommendation** | Complete evidence package + scored gates | Product Board + multi-role sign-off board | Founder as Product Board Chair **after** capacity Founder Reviews | Reviewer · Date · Decision · Notes |
| **Release operator ack** | Deploy fingerprint / smoke / rollback | Release operator | Founder Review — Operations Owner (release lens) | Reviewer · Date · Decision · Notes |

---

## 4. Product Board / registers

| Decision / gate | Evidence still required | Prior approval theatre | Founder-operated approval | Record form |
|---|---|---|---|---|
| New ACTIVE DR / material supersede | Paths + lifecycle | Chair + Product Governance (+ consults) | Founder Reviews: Chair + Product Owner (may be same person, two Notes capacities if meeting record requires) | Minutes + DR card |
| Risk accept / close (material) | Closure proof / residual named | Chair + Product Governance | Founder as Chair + Product Owner capacity | Minutes + PR card |
| Evidence classification for claims | E-level + paths | Evidence Lead | Founder Review — Evidence Lead capacity | Classification note |
| Charter material change | Version bump | Chair ack | Founder Review — Product Board Chair | Reviewer · Date · Decision · Notes |
| Public / C-COM claim | Claim Decision Tree walk | Multi-role | Founder Reviews per Claim Standard consult set | Per capacity |

---

## 5. Standard Founder Review block (copy template)

```markdown
### Founder Review — <gate / title>

| Field | Value |
|---|---|
| Reviewer | |
| Date | |
| Capacity | Product Owner / Engineering Owner / Operations Owner / Privacy Owner / Product Board Chair / <other> |
| Decision | Approve / Reject / Confirm / HOLD / DEFER |
| Notes | |
```

Leave blank until a real review occurs. **Do not fabricate.**

---

## 6. Explicit non-changes

| Item | Status under GP-001 |
|---|---|
| Dry-runs mandatory | **Unchanged** |
| Privacy Review mandatory | **Unchanged** |
| Kill-switch rehearsal mandatory | **Unchanged** |
| Evidence Hierarchy | **Unchanged** |
| Claim Standard / Decision Tree | **Unchanged** |
| Hard-gate FAIL → NO-GO | **Unchanged** |
| Product Board sole V1 recommendation authority | **Unchanged** |

---

**End of UPDATED_APPROVAL_MATRIX**

# MS-006 — Governance Model

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Companions:** `POLICY_EVALUATION.md`, `EXPERIMENT_FRAMEWORK.md`, `OUTCOME_ANALYTICS.md`, `RISK_ANALYSIS_MS006.md`  
**Related:** EP-004 strategic principles SP1–SP8; Architecture Constitution dependency law

---

## 1. Purpose

Define the **human and process governance** that turns observational evaluation into allowed policy evolution — without letting measurement seize educational authority.

Evidence Platform **recommends**; governance **decides**; upstream owners **apply** flag/config changes; Runtime A **remains** fact authority.

---

## 2. Roles

| Role | Responsibility | Must not |
|---|---|---|
| **Policy Owner** | Owns `EducationalPolicy` for a layer (Adaptive / Strategy / Experience routing / ops gates) | Bypass evaluation for learner-visible flips without logged exception |
| **Evidence Steward** | Owns Evidence Model quality, claim boundaries, intake integrity | Write educational facts; “fix” Runtime A via analytics |
| **Experiment Designer** | Authors ExperimentProtocol / pre-registration | Invent arms that write missions / Twin |
| **Evaluation Reviewer** | Checks ExplanationBundle completeness & SP8 honesty | Rubber-stamp overclaim |
| **Architecture Guardian** | Enforces dependency law / ADR-MS006-001 | Approve reverse dependencies |
| **Programme Decision Maker** | Final keep / revise / roll back / expand for material changes | Treat shadow agreement as Ready alone |
| **Engineering Operator** | Executes flag rollback_map / soak monitors | Silent Authority promotion |

One person may hold multiple roles in early Alpha; **separation of duties** is required before broad learner-visible experiments.

---

## 3. Governance process

```
PROPOSE
  Policy change or experiment protocol drafted
  (intent, claim boundary, principles, rollback_map)
        │
REVIEW
  Architecture boundary check
  Evidence / statistical / educational rationale check
  SP1–SP8 mapping check
        │
REGISTER
  Freeze pre-registration fingerprint
  Status → registered
        │
EXECUTE (observational first)
  Shadow measurement preferred
  Serve-arms only with explicit approval
        │
EVALUATE
  EvaluationRecord + ExplanationBundle + gate
        │
DECIDE
  keep | revise | roll_back | expand_soak | inconclusive
        │
APPLY
  Upstream owners change flags/config per decision
  Evidence Platform does not auto-apply
        │
VERIFY
  Post-change soak / guardrails
  Abort path ready
```

### 3.1 Decision meanings

| Decision | Meaning |
|---|---|
| `keep` | Retain treatment / new policy version under stated scope |
| `revise` | Amend policy/protocol; new version required |
| `roll_back` | Execute rollback_map immediately |
| `expand_soak` | Continue observation; no Authority expansion |
| `inconclusive` | No behavioural change; document limitations |

---

## 4. Change classes & required bars

| Change class | Examples | Minimum bar |
|---|---|---|
| **Docs / registry only** | New outcome definition draft | Reviewer ACK |
| **Shadow measurement** | ENABLE_EVIDENCE_SHADOW | Steward + ops |
| **Cross-layer experiment (shadow)** | Assignment + measure | Designer + Steward + Reviewer |
| **Flag-mediated serve (limited)** | Small cohort Authority difference | Full review + Decision Maker + guardrails + rollback drill |
| **Default Authority / policy flip** | Broad Adaptive/Strategy Authority ON | Prior soak PASS + Evaluation gate PASS + Architecture Guardian + Decision Maker + migration checklist |
| **Learning-depth primary claims** | Depth outcome as experiment primary | Explicit programme approval; SP8 audit |
| **Transfer / exam claims** | Marks-linked metrics | Separate evidence programme — out of MS-006 default |

**Hard rule:** Evidence Platform evaluation `passed` is **necessary but not sufficient** for default Authority flips. Upstream migration checklists (MS-003/004/005) remain binding.

---

## 5. Proposal artefact

### 5.1 `GovernanceProposal`

| Field | Meaning |
|---|---|
| `proposal_id` | |
| `kind` | `policy_change` \| `experiment` \| `authority_expansion` \| `rollback` \| `registry` |
| `summary` | |
| `educational_intent` | |
| `claim_boundary` | |
| `sp_mapping[]` | |
| `risk_refs[]` | Links to `RISK_ANALYSIS_MS006` themes |
| `rollback_map` | Required for serve-affecting |
| `evaluation_plan_ref` | |
| `owner_layer` | |
| `requester` / `reviewers[]` | |
| `status` | `draft` → … → `decided` / `withdrawn` |

---

## 6. Review checklist (binding questions)

Reviewers must answer:

1. Does this preserve Runtime A fact authority?  
2. Does Twin remain interpretive only?  
3. Does Adaptive remain recommendation-only?  
4. Does Strategy remain orchestration-only?  
5. Does Evidence Platform remain observational (no writes)?  
6. Are claim boundaries honest (SP8)?  
7. Is explainability complete for the planned evaluation?  
8. Is rollback immediate and tested?  
9. Are multiple Authority flags being flipped together? (If yes → **reject** or split.)  
10. What does success **not** prove?

Any “no” / unmet → do not register serve-affecting work.

---

## 7. Exceptions

| Exception type | Requirements |
|---|---|
| **Emergency rollback** | Operator may execute rollback_map without full review; must file post-incident EvaluationRecord (`post_hoc_incident`) within defined SLA |
| **Docs-only hotfix** | No educational behaviour change; Steward ACK |
| **Security / privacy incident** | Disable Evidence Platform flags; Architecture Guardian notified |

**Forbidden exception:** “Ship Authority because demo looked good.”

---

## 8. Audit & transparency

| Artefact | Retention intent |
|---|---|
| GovernanceProposal + decision log | Programme audit |
| EvaluationRecord + ExplanationBundle | Reconstructibility |
| Assignment / exposure violations | Ops audit |
| Flag change events | Correlate with evaluations |

Student-facing transparency of experiments is a **product** decision outside this architecture directive; governance must still remain reconstructable internally.

---

## 9. Relationship to ADRs

| ADR (design) | Topic |
|---|---|
| ADR-MS006-001 | Evidence Platform Authority Boundaries |
| ADR-MS006-002 | Observational retention |
| ADR-MS006-003 | Serve-arm experiment ethics / consent (if product requires) |
| ADR-MS006-004 | Learning-depth metric programme gate |

Ratify ADR-MS006-001 before E0. Others may draft at E0+.

---

## 10. Stop / Ready governance

| Declaration | Allowed when |
|---|---|
| Architecture Design complete | This doc set delivered; awaiting review |
| Evidence Platform Ready | Migration E0–E7 checklist PASS (`MIGRATION_PLAN_MS006.md`) — **not** this directive |
| Policy “proven” | Never absolute; only `keep` under stated limitations |

---

## 11. Non-goals

- Automated governance bots that flip flags  
- Replacing engineering code review  
- Making Evidence Steward the Adaptive/Strategy owner  
- Using governance theatre to justify overclaim  

---

## 12. Acceptance hooks

Architecture PASS requires a governance path where:

- Measurement recommends; humans decide; upstream applies  
- Educational authority layers remain unseized  
- Rollback and claim-boundary honesty are mandatory

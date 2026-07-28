# CP-002 — Governance Safeguards

**Programme:** CP-002 — Capability Programme  
**Version:** 1.0  
**Status:** Active — governance, review, and rollback architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP002_LEARNING_FEEDBACK_ARCHITECTURE.md`  
**Constraint:** Process and constitutional design only — no application behaviour changed by this programme.

---

## 1. Purpose

Define the **constitutional safeguards**, **human review checkpoints**, and **rollback strategy** that prevent the Learning Feedback Loop from becoming uncontrolled self-modification.

**Acceptance criterion:** No feedback directly changes recommendation behaviour without governed review.

---

## 2. Constitutional safeguards (normative)

| ID | Safeguard | Authority | Binding effect on the loop |
|----|-----------|-----------|----------------------------|
| **CS-01** | Trust > optimisation | PC-01, Vision 2030 | Engagement maximisers forbidden |
| **CS-02** | Claims ≤ evidence | PC-03, PC-04, OM-001 | No “we learned X” without pack / CalibrationRecord |
| **CS-03** | Independent boards | PC-02 | Educational GO ≠ Engineering GO for loop promotes |
| **CS-04** | ADR before structural apply | PC-06 | New write paths, weight tables, Twin writers need ADR |
| **CS-05** | Deterministic cores | PC-09 | Approved policies versioned and reproducible |
| **CS-06** | Curriculum truth first | PC-10 | Feedback cannot invent syllabus order |
| **CS-07** | Agency preserved | PC-11 | Reject/defer never scored as moral failure |
| **CS-08** | STOP on thin evidence | PC-12 | Default when C0–C1 would drive LU-POL |
| **CS-09** | Understanding ≠ certainty | Twin Constitution | No mastery from accepts |
| **CS-10** | No second educational brain | EP-002.9, SI-001 | Loop proposes; Runtime A owners decide under gate |
| **CS-11** | Observe ≠ adapt | EP-003.4, ILE-005, CP-002 | Recording alone never re-ranks |
| **CS-12** | Explainability freeze | P-001.2, CP-001 | History immutable; future speech gated |
| **CS-13** | Recommendation quality law | P-001.3 | Behaviour changes need checklist Pass (or waiver) |
| **CS-14** | Flag honesty | ER-002 / OA-001 | OFF flags ≠ live adaptation narrative |
| **CS-15** | Fail open on student path | EP-003.4 posture | Loop failures must not break study |

Violation of CS-* in a future implementation programme is a constitutional defect — not a tuning choice.

---

## 3. LearningProposal (conceptual)

| Field | Meaning |
|-------|---------|
| `proposal_id` | Stable id |
| `update_class` | LU-OBS \| LU-CAL \| LU-TWN \| LU-POL \| LU-EXP |
| `title` / `rationale` | Human-readable educational purpose |
| `evidence_refs[]` | QualifiedEvidence / pack / CalibrationRecord ids |
| `ef_codes[]` | Educational meanings relied upon |
| `om_metric_ids[]` | Catalogue links |
| `affects_recommendation_behaviour` | Boolean — **true ⇒ mandatory gate** |
| `proposed_diff` | Versioned before→after description |
| `risk_notes[]` | Agency, privacy, certainty risks |
| `rollback_plan` | Required for apply |
| `status` | `draft` \| `in_review` \| `approved` \| `rejected` \| `applied` \| `rolled_back` |

---

## 4. Human review checkpoints

### 4.1 Checkpoint matrix

| Update class | Affects recommendation behaviour? | Minimum checkpoint |
|--------------|-----------------------------------|--------------------|
| LU-OBS | No | Automated validation only |
| LU-CAL (disclose-down, internal tables) | No | Product ops review + versioning |
| LU-CAL (student-facing speech) | Indirect | P-001.2 checklist + product review |
| LU-TWN (behaviour/preference understanding) | No | Twin Constitution attestation + ADR if new write path |
| LU-POL | **Yes** | **Full gate (§4.2)** |
| LU-EXP promote | **Yes** | SI-C10 path: pre-registration + Independent Review + OA-001 lifecycle |

### 4.2 Full gate for recommendation-behaviour changes (LU-POL / LU-EXP promote)

All of the following are required before `applied`:

1. **QualifiedEvidence** at C3+ (LU-POL) or C4 (LU-EXP)  
2. **LearningProposal** with rollback_plan  
3. **ADR** accepted if structural / weight / authority boundary changes (PC-06)  
4. **P-001.3 Recommendation Review** Pass or documented waiver  
5. **P-001.2 Explainability Review** Pass or waiver if student-facing speech/ranking presentation changes  
6. **Founder / Educational governance review** when claim class expands (per OA-001 / OM evidence requirements)  
7. **Flag / cohort plan** — how the change is gated; default OFF until authorised  
8. **Audit record** written (§5)

**Hard rule:** Automated pipelines may *draft* LU-POL proposals; they may not *apply* them.

### 4.3 Reviewer capacities (design)

| Capacity | Reviews |
|----------|---------|
| Product educational owner | Educational meaning, agency, claim honesty |
| Engineering owner | Determinism, flags, rollback technical feasibility |
| Independent reviewer | Required for LU-EXP promote and claim-class expansion |
| Privacy owner | When Class D reflection or free-text rationale enters training-like aggregates |

---

## 5. Audit trail requirements

Every transition of a LearningProposal to `approved`, `applied`, or `rolled_back` MUST record:

| Audit field | Content |
|-------------|---------|
| `audit_id` | Stable id |
| `proposal_id` | Link |
| `actor` | Human capacity (not anonymous automation for apply) |
| `decision` | Approved / Rejected / Applied / Rolled back |
| `timestamp` | UTC |
| `evidence_refs[]` | Snapshot of cited refs at decision time |
| `checklist_paths[]` | P-001.2 / P-001.3 / ADR paths |
| `policy_version_before` / `after` | For applied / rolled_back |
| `limitations[]` | Copied forward |
| `notes` | Non-secret rationale |

**Immutability:** Audit entries are append-only. Corrections are new entries referencing the prior `audit_id`.

Sensei self-review (ILE-005) may feed evidence_refs but is not itself a substitute for this audit when behaviour changes.

---

## 6. Rollback strategy

### 6.1 Principles

| Principle | Meaning |
|-----------|---------|
| **Rollback-first design** | No apply without `rollback_to` version pointer |
| **Student-safe** | Rollback must not corrupt Decision Journal history or ExplanationSnapshot freeze |
| **Deterministic restore** | Prior policy / calibration / Twin-input version restored bit-for-bit where feasible |
| **Claim honesty** | After rollback, marketing/claims must not continue as if change were live (PC-03) |
| **Time-bounded** | Emergency rollback may be engineering-led; educational claim retraction follows within review SLA |

### 6.2 Rollback triggers

- Adverse educational signal (EF-LEARN negative with warrant)  
- Explainability / agency incident  
- Determinism break or non-reproducible weights  
- Flag matrix honesty failure  
- Independent Review revoke  
- PC-12 STOP invoked by Founder Review  

### 6.3 Rollback procedure (design)

```
Detect trigger
    → Freeze further LU-POL applies
    → Restore policy_version / Twin-input version via rollback handle
    → Append audit (rolled_back)
    → Notify educational + engineering owners
    → File claim retraction / Contained disclosure if student-facing claims were made
    → Root-cause LearningProposal (new) — do not silent re-apply
```

### 6.4 What rollback does not do

- Erase Decision Journal or observational history  
- Rewrite past student-visible explanations  
- Invent compensatory ranking “to make up for” the rollback  
- Quietly leave feature flags ON while behaviour is restored  

---

## 7. Anti-patterns (forbidden)

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Online RL on tip weights from accepts | Opaque; PC-09; CS-11 |
| “Auto-improve” marketing while flag OFF | PC-03 / CS-14 |
| Training Twin mastery from dismissals | Twin Constitution |
| Using reflection skip as negative score | PC-11 |
| Applying LU-POL because A/B click lift looked good | Learning ≠ engagement |
| Deleting audit on rollback | CS-02 / audit immutability |
| Dual scoring brain in analytics | SI-C8 / OM integrity |

---

## 8. Integration with OA-001 lifecycle

| OA-001 artefact | Loop use |
|-----------------|----------|
| Feature lifecycle | LU-POL treated as significant feature when student-facing |
| ADR standard | Required for structural apply |
| Risk review | Agency / certainty / privacy risks on proposal |
| Change management | Versioned policy changes |
| Release governance | Flag default OFF; Contained disclosures |
| Programme dashboard | Optional future row — not required by this package |

---

## 9. Non-goals

- No workflow tool implementation  
- No change to existing EP-003.4 fail-open emitters  
- No production rollback runbooks beyond this architecture  
- No amendment of Product Constitution text  

---

**End of CP-002 Governance Safeguards**

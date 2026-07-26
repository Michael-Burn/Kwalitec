# MS-004 — Digital Twin Explainability

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design — **T3 Explainability Implemented** (explanation contracts + service; gate remains later Authority path)  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Contracts:** `DIGITAL_TWIN_INTERFACE_SPECIFICATION.md`  
**Principles:** DP-005 Explainability, DP-008 Trust, DP-009 Evidence Before Opinion, DP-010 Human-Centred Intelligence  
**Related:** MS-003 `ADAPTIVE_EXPLAINABILITY.md` (decision-facing six questions)

---

## 1. Purpose

Every **student-visible Twin claim** (readiness summary statement, learning insight, learner-summary assertion about knowledge/behaviour) must answer the Twin explainability questions. If it cannot, it is **not ready** to display under Twin Authority.

Twin explainability is complementary to Adaptive explainability:

| Layer | Question focus |
|---|---|
| Twin | *Who is the learner now, based on what evidence?* |
| Adaptive | *What should they do next, based on what evidence and rules?* |

---

## 2. Twin six-question model

| # | Question | Contract field |
|---|---|---|
| 1 | What is claimed? | `claim` |
| 2 | Why this claim? | `why` |
| 3 | Which evidence? | `evidence_refs` |
| 4 | Which Twin facet / rule? | `facet_or_rule` |
| 5 | Confidence? | `confidence` |
| 6 | What are the limits? | `limitations` |

Optional seventh for Adaptive-facing packaging (not required for Experience TwinPort):

| # | Question | Contract field |
|---|---|---|
| 7 | Alternatives / competing signals? | `competing_signals` |

---

## 3. `TwinExplanationBundle` contract

```
TwinExplanationBundle {
  claim: {
    kind,                    # readiness | knowledge | behaviour | performance | goals | insight
    summary,                 # plain language, student-safe
    facet                    # knowledge | memory | behaviour | performance | predictions | confidence | identity | goals
  },
  why: {
    summary,
    reason_codes[]           # stable machine codes
  },
  evidence_refs: [
    { kind, id, observed_at?, note? }
  ],
  facet_or_rule: {
    facet,
    rule_or_model_id,        # registered synthesis rule id
    version,
    description
  },
  confidence: {
    score?,                  # optional 0..1
    band,                    # low | medium | high | unavailable
    rationale
  },
  limitations: {
    codes[],
    summary
  },
  competing_signals: {
    items: [
      { signal, direction, note }
    ]
  } | null,
  runtime_a_note: {
    alignment,               # pass_through | derived | conflict_runtime_a_wins
    summary
  }
}
```

### Completeness rule

For Twin Authority UX claims, questions 1–6 must be present (`claim.summary` and `why.summary` non-empty; `evidence_refs` may be empty **only** with `sparse_evidence` / `no_active_plan` limitations and non-high confidence).

`TWIN_EXPLAINABILITY_INCOMPLETE` if required groups missing.

---

## 4. Evidence refs

| `kind` | `id` | Notes |
|---|---|---|
| `attempt` | AttemptId | Preferred for practice-grounded claims |
| `mission` | MissionId | Session / behaviour lineage |
| `topic_progress` | topic_code (+ user scope) | Knowledge factual claims |
| `readiness` | aggregate label / as_of | Not a substitute for attempts |
| `study_plan` | plan id | Goals / identity |
| `lifecycle` | stage + as_of | Stage claims |

**Forbidden:** Citing evidence the student does not own; inventing ids; treating absence of evidence as mastery (DP-009); citing Adaptive `decision_id` as if it were learning evidence.

---

## 5. Rule / model registry (design)

Every Twin claim cites a registered `rule_or_model_id`.

| Example id (illustrative) | Intent |
|---|---|
| `twin.pass_through.topic_progress` | Surface Runtime A progress fact |
| `twin.pass_through.readiness` | Package ReadinessService snapshot |
| `twin.structure.behaviour_session_counts` | Count completed/missed missions |
| `twin.structure.knowledge_evidence_refs` | Attach attempt refs to topics |
| `twin.insight.sparse_evidence` | Honest empty / sparse narrative |
| `twin.estimate.*` | **Forbidden under Authority until ADR-MS004-004** |

---

## 6. Claim kinds and required honesty

| Claim kind | Must include | Must not |
|---|---|---|
| Readiness summary | Readiness pass-through + confidence + limitations | Invented readiness formula |
| Knowledge insight | TopicProgress and/or attempt refs | “Mastered” without Runtime A status |
| Behaviour insight | Mission refs; Behaviour≠learning disclaimer when needed | Equating completion with exam readiness |
| Performance insight | Attempt/mission outcome refs | Raw scores that leak answer keys |
| Goals / identity | StudyPlan refs | Fabricated exam dates |

---

## 7. Gate behaviour

| Outcome | Meaning |
|---|---|
| **PASS** | Claim eligible for Twin Authority Experience surfaces |
| **FAIL** | Shadow-only / fallback; emit `TWIN_GATE_FAILED`; no mutation |

Gate executes when Twin Shadow (and later Authority) paths produce student-visible claims. Incomplete bundles never “auto-fix” copy.

---

## 8. Human-centred language rules (DP-010)

| Do | Don't |
|---|---|
| “Based on your last N completed sessions…” | “Our AI knows you will pass” |
| “Coverage on Topic X is incomplete in your plan progress” | “You have mastered X” without TopicProgress |
| “Limited practice evidence — confidence is low” | Hide sparse_evidence |
| Separate behaviour cadence from readiness | “You skipped Friday so you are not ready” as sole causal claim |

---

## 9. Relationship to Adaptive ExplanationBundle

| Concern | Rule |
|---|---|
| Shared evidence refs | Prefer identical Attempt/Mission ids |
| Distinct bundles | Twin explains profile; Adaptive explains next action |
| Twin attached to Adaptive | Adaptive ExplanationBundle may list `inputs_used` including `twin_snapshot_ref`; Twin bundle remains separate |
| Gate independence | Adaptive Gate PASS ≠ Twin Gate PASS |

---

## 10. Acceptance (architecture)

| ID | Criterion |
|---|---|
| TE-1 | Six-question Twin bundle defined |
| TE-2 | Incomplete → not Authority |
| TE-3 | Runtime A alignment note required |
| TE-4 | Estimate rules gated behind ADR |
| TE-5 | No Adaptive decision cited as learning evidence |

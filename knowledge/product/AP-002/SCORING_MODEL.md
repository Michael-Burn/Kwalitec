# AP-002 — Scoring Model (Educational Evidence)

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Principle

Do **not** think in marks.

The Assessment Engine does not award grades, percentages-as-identity, or league tables. It extracts **educational evidence dimensions** from responses so Educational Reasoning can update Twin belief.

> Correctness is evidence. A score is not a person.

---

## 2. Evidence dimensions

| Dimension | Definition | Typical use in Reasoning |
|---|---|---|
| **Correctness** | Match to accepted response / rubric category | Strong factual signal when combined with context |
| **Partial correctness** | Which facets were right/wrong | Diagnoses incomplete understanding |
| **Confidence** | Self-reported certainty at response time | Calibration vs performance (soft alone) |
| **Response time** | Elapsed time to commit | Fluency / struggle proxy; never sole mastery driver |
| **Hint usage** | Hints revealed before commit | Independence vs scaffolded success |
| **Retries** | Attempts before accepted commit | Persistence / instability indicator |
| **Misconception category** | Tagged error pattern | Gap specificity for recovery missions |
| **Knowledge stability** | Consistency across spaced checks | Supports durable mastery inferences |
| **Consistency** | Agreement across related items in a session | Reduces noise from single lucky hits |
| **Mastery confidence (input)** | Not a Twin write — a *candidate signal* about evidence strength for later Reasoning | Feeds evidence-strength aggregation |
| **Evidence strength** | Quality/density of this observation bundle | Gates high-mastery language (EIP-002) |

These dimensions are stored as structured metadata on Observations / Assessment Results — not as a single “mark”.

---

## 3. Deterministic evaluation

For each item type, evaluation is rule-based:

| Type | Evaluation |
|---|---|
| Multiple choice / response | Exact set match; record selected distractor tags |
| Numeric | Tolerance window; record magnitude of error if useful |
| Formula | Deterministic normalisation + equivalence rules |
| Free text | Closed rubric categories only (V1); unknown → `uncoded` |
| Worked solution | Step checklist; error locus codes |
| Confidence / reflection | Pass-through coded values; no “correctness” |

No LLM judges mastery in the Engine path.

---

## 4. Composite session summaries (evidence-only)

A session may emit a **PerformanceSummary**-compatible rollup (AP-001 already has evidence-only summaries):

- counts by correctness / partial / incorrect
- misconception frequency
- median response time
- hint/retry rates
- confidence–correctness agreement rate
- declared evidence strength band (thin · moderate · strong)

Summaries **must not** duplicate Twin mastery rows or invent readiness percentages as authority.

---

## 5. What “scoring” must never do

| Forbidden | Why |
|---|---|
| Write Estimated Mastery directly | Twin authority + EIP-002 |
| Convert one lucky correct into “Mastered” theatre | Evidence density required |
| Punish slow response with lower identity score | Anxiety + unfair fluency bias |
| Hide marks that still drive ranking UX | Philosophy violation |
| Let Tutor invent a grade from prose | Tutor explains; does not grade |

---

## 6. Mapping to Twin observations

Evidence dimensions travel inside Observation `metadata` (and Assessment Result linkage), for example:

```text
correctness: correct | partial | incorrect
misconception_tags: [tag…]
confidence: 1..5 | null
response_time_ms: int
hints_used: int
retries: int
evidence_strength: thin | moderate | strong
assessment_session_id / item_id / item_version
intent: diagnostic | checkpoint | …
```

Reasoning rules consume these facts. Assessment does not interpret them into recommendations.

---

## 7. Confidence calibration

When confidence and correctness diverge:

| Pattern | Educational meaning (for Reasoning, not UI shame) |
|---|---|
| High confidence + incorrect | Possible misconception / overconfidence |
| Low confidence + correct | Fragile knowledge / underconfidence |
| Aligned high | Candidate stability signal (needs repetition) |
| Aligned low | Clear learning need |

UI language stays supportive; see `UX_PRINCIPLES.md`.

---

## 8. Evidence strength heuristic (design contract)

A minimal deterministic band (implementation detail deferred):

| Band | Illustrative conditions |
|---|---|
| Thin | Single item, heavy hints, or first exposure |
| Moderate | Multiple consistent items, limited scaffolding |
| Strong | Spaced consistency, low hint dependence, misconception cleared |

Exact thresholds belong to Reasoning policy / future AP-002C–D — not presentation.

---

## 9. Relationship to legacy practice outcomes

LXP-003 Observed Practice Outcomes remain lawful soft/structured practice inputs. The Assessment Engine deepens intentional instruments; it does not invalidate practice capture. Cutover to Engine-as-canonical ingress is a later programme decision.

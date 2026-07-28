# AP-002D — Explainability Requirements

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`ENGINEERING_STANDARD.md`](../../engineering/ENGINEERING_STANDARD.md), P-001.2 Explainability Standard, [`TRACEABILITY_MODEL.md`](TRACEABILITY_MODEL.md)

---

## 1. Principle

Every Twin update from assessment evidence must remain explainable.  
Every educational decision must reference evidence.  
Every explanation must remain deterministic.

Incomplete explainability must not ship as Twin Authority insight.

---

## 2. Twin update explainability

For each assessment-triggered Twin inference change, the system must be able to answer:

| Question | Required source |
|---|---|
| What facts were considered? | Observation ids + evidence references |
| Which assessment session/items? | Session id, instrument id, question ids |
| What evidence quality applied? | Evidence strength band + scaffolding metadata |
| Which rules fired? | `RuleExecution` / reasoning steps |
| What changed on the Twin? | Before/after inference fields via ReasoningResult |
| What was *not* concluded? | Honesty limits (thin evidence, soft signals alone) |

`ReasoningRecord` on the Twin (`triggered_by`, `observation_ids`, steps, summary, `reasoning_version`) is the primary student-intelligence audit unit.

---

## 3. Decision → evidence linkage

Every educational decision / recommendation produced after assessment ingress must carry or resolve:

1. **Evidence refs** — observation ids and/or `evidence_reference` / bundle ids  
2. **Rule identity** — which declared rule(s) produced the decision  
3. **Curriculum refs** — opaque entity ids + Retrieval citations used  
4. **Limitations** — what the decision does not claim (e.g. soft confidence alone)

Decisions without reconstructable evidence linkage are non-compliant for student-facing intelligence.

---

## 4. Deterministic explanations

| Requirement | Meaning |
|---|---|
| Same inputs → same explanation artefacts | No hidden randomness in explanation codes / rule narratives |
| LLM prose (if any) | Behind Tutor generation port only — must not invent new educational conclusions |
| Student-facing copy | Narrates reasoned outcomes; does not re-score |
| Founder diagnostics | May show denser evidence; still must not become Twin SoT |

Explanation codes and structured `Explanation` objects from the Reasoning Engine are preferred over free-form only strings for audit.

---

## 5. Surface-specific rules

### Twin / Reasoning surfaces

- Show estimates as estimates; advice as advice.
- Do not present Evidence Strength as “your mastery score”.
- Prefer under-claiming when evidence is thin.

### Mission surfaces

- Mission reasons cite Twin decisions / gaps — not raw Engine marks.
- Assessment activities (when present) use anxiety-safe framing (AP-002 UX principles).

### Tutor surfaces

- Tutor explains decisions already produced.
- May summarise Learning Feedback / Assessment Result evidence.
- Must never grade or invent alternate mastery.

### Assessment surfaces

- Show progress of the check / evidence collected — not league tables.
- Do not imply Twin conclusions before Reasoning has run.

---

## 6. Forbidden explainability failures

1. “Mastery updated” with no observation linkage  
2. Soft signal alone presented as high Estimated Knowledge  
3. Tutor inventing a second score  
4. Mission claiming “because you scored 40%” as identity  
5. Non-reproducible explanation text that changes educational meaning between runs  

---

## 7. Implementation milestone note

When AP-002D implementation changes student-facing intelligence surfaces, complete:

- `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md`
- Recommendation checklist if recommendation ranking/selection changes

This design milestone itself is documentation-only; checklist execution belongs to the implementation programme.

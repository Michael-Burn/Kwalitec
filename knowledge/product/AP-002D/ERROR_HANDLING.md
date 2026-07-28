# AP-002D — Error Handling

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`REASONING_CONTRACT.md`](REASONING_CONTRACT.md), [`EVIDENCE_BOUNDARY.md`](EVIDENCE_BOUNDARY.md)

---

## 1. Purpose

Define how invalid, duplicate, partial, or incomplete assessment evidence is handled at the Evidence Boundary and beyond — without fabricating educational conclusions.

---

## 2. Invalid evidence

| Example | Detection | Response |
|---|---|---|
| Bundle fails structural validation | Packaging validation | Do not export; do not append Twin observations for that package |
| Malformed metadata / unknown required fields | DTO / pipeline validation | Reject event; return actionable error to caller |
| Mixed session observations in one package | Aggregator invariant | Reject package |
| Evidence claiming mastery / recommendation payloads | Boundary policy | Strip/reject — Assessment must not export inferences |

**Rule:** Invalid evidence never becomes Twin belief.

---

## 3. Duplicate evidence

| Example | Response |
|---|---|
| Same observation id packaged twice | Reject at aggregation (AP-002C behaviour) |
| Same evidence_reference / event replayed into pipeline | Idempotent skip — do not create a second Twin observation |
| Reasoning re-run with identical observation set | Deterministic same inferences; history policy per existing Twin rules (prefer explicit re-trigger provenance) |

Duplicates must not inflate mastery through double-counting.

---

## 4. Partial evidence

| Situation | Preferred strategy |
|---|---|
| Some items fail evaluation / coding | Record coded outcomes (`uncoded` where needed); do not invent correctness |
| Session abandoned mid-way | Package only committed observations; strength likely `thin` |
| Packaging with a subset of invalid items | **Default: fail-closed** for the whole package. Optional later contract: validated subset + `partial=true` flag — must be explicit and tested |
| Pipeline receives partial export | If partial allowed, Reasoning treats missing items as absent facts (honesty), not as failures |

Never synthesise “completed session” evidence for unanswered items.

---

## 5. Unknown concepts

| Situation | Response |
|---|---|
| Concept id not in Graph / Retrieval | Append observation with opaque ref if present; Reasoning does not invent concept meaning |
| Concept tag on distractor unknown to catalogue | Keep tag as metadata string; gap specificity may remain coarse |
| Soft concept hints in free text | V1: `uncoded` — no LLM mastery claim |

Unknown ≠ mastered. Unknown ≠ failed. Unknown = incomplete educational mapping.

---

## 6. Missing learning objectives

| Situation | Response |
|---|---|
| Instrument item lacks LO ref | Packaging may proceed with empty LO set; strength/completeness factors reflect incompleteness |
| Observation curriculum_entity_id empty | Allowed as fact; Reasoning must not fabricate an LO; recommendations remain general / deferred |
| Retrieval cannot resolve entity | Record empty curriculum evidence for that ref; do not scrape syllabus ad hoc |

Founder diagnostics should flag LO-less instruments as quality debt — not silently “fix” via Twin guesses.

---

## 7. Recovery strategy

```
Detect → Isolate → Do not infer → Preserve prior Twin belief → Signal operator/caller → Retry lawfully
```

| Layer | Recovery action |
|---|---|
| Packaging | Fix instrument/session data; re-package; new export |
| Pipeline validation | Correct event payload; replay idempotently |
| Observation append | Only after validation passes |
| Reasoning failure | Keep prior inferences; log/audit failed run; alert Founder path |
| Persistence failure | Roll back; no half Graph + half Twin apply |
| Mission refresh failure | Twin belief already updated remains SoT; retry refresh later |

**Never recover by inventing mastery to “keep the UX moving”.**

---

## 8. Student-visible honesty

When evidence cannot update belief:

- Do not show false “progress saved as mastery”.
- Prefer “we could not use this check yet” / retry framing over silent success.
- Tutor must not invent conclusions the Twin does not hold.

---

## 9. Test expectations (implementation)

Independently testable cases:

1. Invalid bundle → no Twin observation  
2. Duplicate export → single observation  
3. Thin / abandoned session → no high-mastery promotion  
4. Missing LO → no fabricated curriculum claim  
5. Reasoning error → prior Twin inferences unchanged  

# CP-001 — Decision Journal Explainability Integration

**Programme:** CP-001 — Capability Programme  
**Version:** 1.0  
**Status:** Active — explainability integration architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP001_DECISION_JOURNAL_ARCHITECTURE.md`, `CP001_DOMAIN_MODEL.md`  
**Constraint:** No student-facing speech, Coach/Insights copy, or APIs modified by this programme.

---

## 1. Purpose

Define how the Decision Journal **integrates with the Explainability Standard (P-001.2)** and EIP-003 educational speech law so that every recorded decision preserves a durable, honest explanation of guidance — and so later outcome claims remain inspectable.

**Explainability improves understanding of decisions already authorised.  
The journal freezes that understanding; it never invents post-hoc educational certainty.**

---

## 2. Authority

| Authority | Binding effect |
|-----------|----------------|
| P-001.2 Explainability Standard | Levels, Mandatory Explanation Schema, review gate (K8) |
| EIP-003 | Facts ≠ estimates ≠ advice; four-question educational speech |
| SI-001 SI-C7 | Explainability continuous from H1 |
| OM-001 OM-EXP-* | Effectiveness and compliance sampling metrics |
| ILE-002 Philosophy | Permanent educational explainability arc on entries |
| Twin Constitution | Estimates labelled; unknown remains unknown |
| OA-001 PC-01, PC-03, PC-11 | Trust, claim honesty, agency |

---

## 3. Integration principle

```
Recommendation authorised (P-001.3)
        ↓
Explanation assembled (P-001.2 at declared level)
        ↓
Decision Journal freezes ExplanationSnapshot
        ↓
Student choice / reflection / outcome append
        ↓
Historical explanation remains readable and immutable
        ↓
OM-EXP sampling / audits read frozen snapshots
```

| Rule | Meaning |
|------|---------|
| **Freeze at show** | ExplanationSnapshot written when guidance becomes journal-eligible |
| **No rewrite** | Later evidence appends; original why/evidence/confidence unchanged |
| **No AI backfill** | Generative wording must not invent new reasons into past entries (P-001.2 P9) |
| **Level honesty** | Stored level matches what the student was shown by default |
| **Agency speech** | Journal narrative must allow follow / defer / reject without shame |

---

## 4. Mandatory schema → journal field map

P-001.2 Mandatory Explanation Schema (product law) maps to Domain Model `ExplanationSnapshot` + `GuidanceSnapshot`:

| Schema concern | Journal field | Student question |
|----------------|---------------|------------------|
| Recommendation / action | `GuidanceSnapshot.action_summary` | What was suggested? |
| Why | `ExplanationSnapshot.why` | Why this? |
| Evidence | `ExplanationSnapshot.evidence_summary` | What evidence? |
| Confidence | `ExplanationSnapshot.confidence_band` | How sure? |
| Next action | `ExplanationSnapshot.next_action` | What should I do now? |
| Uncertainty / missing data | `ExplanationSnapshot.uncertainty` | What is unknown? |
| Observation / meaning / benefit | `GuidanceSnapshot.*` | Continuity arc (ILE-002) |
| Review point (when material) | EvidenceEvent or OutcomeLink note | When reassess? |

**Joint rule (P-001.3 §4):** Guidance that cannot satisfy the schema at the declared level is **not ready to show** — and therefore **not ready to journal as eligible primary guidance**.

---

## 5. Explanation levels in the journal

| Level | Journal behaviour |
|-------|-------------------|
| **Level 1 — Simple** | Store short why + next; confidence may be humble/implicit; still freeze uncertainty if material |
| **Level 2 — Detailed** | Full schema fields required for eligible primary recommendations |
| **Level 3 — Diagnostic** | Optional progressive disclosure; may store richer lineage behind opt-in / operator views — never default daily chrome |

Journal chronology UI should default to Level 1/2 student-safe narrative. Level 3 internals (warrants, Twin enums, pipeline ids) remain forbidden on student surfaces (P-001.2 P5; ILE-002 hard rules).

---

## 6. Facts ≠ estimates ≠ advice in frozen memory

| Speech type | Journal treatment |
|-------------|-------------------|
| **Fact** | Observed Mission outcome, attempt result, syllabus position — labelled as observed |
| **Estimate** | Readiness band, mastery estimate, Twin facet — labelled as estimate; never “you know X” |
| **Advice** | Recommendation action — labelled as advice; refuse coercion |

`ExplanationSnapshot.fact_estimate_advice_separation` is the design compliance flag for OM-EXP-02 sampling.

Sparse evidence → humble bands or lawful refusal (`EV-REFUSE`). Empty evidence + strong language is an **incident** (OM-EXP-04), not a successful journal entry.

---

## 7. Student choice and explainability

Explainability supports **decision quality**, not compliance theatre.

| Student act | Explainability obligation |
|-------------|---------------------------|
| Accept | Preserve why they were asked to accept |
| Defer | Preserve uncertainty and expected benefit without guilt copy |
| Reject / dismiss | Preserve rationale tags when offered; never rewrite guidance as “wrong student” |
| Ask for more detail | Progressive disclosure of frozen Level 2/3 — not new invented reasons |

Optional StudentRationale is **part of agency**, not a substitute for the system’s explanation freeze.

---

## 8. Reflection and explainability

Reflection closes the Sensei–learner loop (ILE-011). Explainability rules:

1. Reflection must not coerce (PC-11; OM-REF invariant).  
2. Reflection text must not silently rewrite GuidanceSnapshot / ExplanationSnapshot.  
3. If reflection changes *future* guidance, the **new** recommendation gets a **new** ExplanationSnapshot.  
4. Linking reflection to past decisions is narrative continuity — not proof of mastery.

---

## 9. OM-001 measurement hooks

| Metric | Journal explainability role |
|--------|----------------------------|
| **OM-EXP-01** | Schema compliance rate over ExplanationSnapshots |
| **OM-EXP-02** | Fact≠estimate≠advice separation rate |
| **OM-EXP-03** | Perception sampling: student can state why (uses frozen why) |
| **OM-EXP-04** | Empty-evidence strong-language incidents |
| **OM-EXP-05** | Lawful refusal rate (`EV-REFUSE` / sparse-evidence) |
| **OM-REC-02** | Understood rate — explanation complete at impression |
| **OM-REC-10** | Completeness — disposition recorded for eligible decisions |

K8 claims still require Explainability Review Checklist Pass (or waiver). Journal architecture alone does not move K8.

---

## 10. Review gate for future programmes

Any future programme that changes how journaled guidance explains itself must:

1. Complete `EXPLAINABILITY_REVIEW_CHECKLIST.md` (P-001.2).  
2. If recommendations change, also complete Recommendation Review Checklist (P-001.3).  
3. Declare default explanation level for affected surfaces.  
4. Preserve freeze / append-only invariants (ADR if changing).  
5. Cite CP-001 + OM-EXP / OM-REC metric ids in evidence packs.

CP-001 itself: **N/A** for checklist Pass — no student-facing intelligence speech changed.

---

## 11. Anti-patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| Post-hoc “why” invented after reject | Rewrites history; destroys trust |
| Journal stores Twin jargon | Violates educational language rule |
| Accept-rate used as explainability score | Conflates agency with understanding |
| Level 3 dump in daily chronology | Overloads; violates level fitness |
| Silent steering without ExplanationSnapshot | Unexplainable guidance is incomplete |

---

## 12. Explicit non-goals

- Changing Coach/Insights/Plan copy in this programme  
- Implementing compliance samplers  
- Amending P-001.2 schema  
- Declaring K8 movement  

---

**End of CP001_EXPLAINABILITY_INTEGRATION**

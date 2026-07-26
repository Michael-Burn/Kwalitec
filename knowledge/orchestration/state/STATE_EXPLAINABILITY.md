# State Explainability

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS001 — Educational State Model  
**Classification:** Explainability contract for constitutional educational state  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **educational state** (constitutional educational context) to students and developers.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
4. [`EDUCATIONAL_STATE_MODEL.md`](EDUCATIONAL_STATE_MODEL.md)
5. [`STATE_OBJECTIVES.md`](STATE_OBJECTIVES.md) (especially ESO-05)
6. [`STATE_TYPES.md`](STATE_TYPES.md)
7. [`STATE_BOUNDARIES.md`](STATE_BOUNDARIES.md)
8. Programme VI explainability corpora for any meaning authority whose question is constitutive in the live EST type
9. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) — orchestration speech when workflows reference context
10. [`../authority_explainability/`](../authority_explainability/) — permission / refusal speech when ownership narration is material
11. [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md) and assembly / set explainability — when guidance references context
12. [`../state_explainability/`](../state_explainability/) — WS4 / MS003 unified context-and-progression explanation contract (principles, components, boundaries, patterns); this document remains the MS001 static-context speech contract (ESQ-01…ESQ-04)

> **Explainability improves understanding of constitutional context already represented.  
> It never invents educational certainty, mastery, success, tips, or ownership.**

---

## 1. Purpose

Students should never have to guess whether Kwalitec is focusing on today, recovery, revision, exam preparation, plan change, or simply holding continuity — or mistake that focus for “you have mastered this” or “you are done.”

Developers should never have to reverse-engineer which EST type was live, why it entered, what warranted it, or which workflows and recommendations referenced it.

State explainability exists so every material educational state answers — in the right language for the audience — **what the current constitutional state is**, **why it exists**, **what constitutional evidence / warrants support it**, and **what workflows and recommendations reference it**.

Without state explainability:

- focus changes feel arbitrary;
- context is confused with mastery or completion;
- audits cannot prove EST catalogue discipline;
- orchestration and tips appear detached from educational situation.

With state explainability:

- the student trusts which educational focus is live;
- developers can verify WS4 did not invent modes or evaluative overclaims;
- claim types stay honest;
- holding, awaiting, and absence remain dignified and clear.

---

## 2. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Current focus (“today / recovery / revision / exam / plan / waiting / holding”); why that focus; honest limits; what to expect next | EST/ESO/SB IDs, Twin facets, optimiser jargon, internal document paths, mastery rhetoric from context alone |
| **Developer / auditor** | Precise constitutional references | EST-xx, entry/exit satisfaction, warrant sources, observing consumers (WS1/WS2/WS3), SB-xx pass, Article IV non-identity | Student motivational fluff as a substitute for audit fields |

Student copy narrates educational focus. Developer traces cite EST IDs and warrant checks.

---

## 3. Traceability Obligation (Architectural)

Every material constitutional educational state must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Current state** | “Right now we’re focusing on…” / “We’re holding steady until…” | EST-xx primary (+ parallel-read siblings if any) |
| **Why it exists** | “Because … is the live educational question / situation…” | Entry conditions satisfied; prior exit if required |
| **Supporting constitutional warrants** | “Given your Study Plan / recent disruption / exam preparation need / …” | Warrant class: plan class, Programme VI warrant, WS1 event, WS2 disposition, continuity hold |
| **Workflows that reference it** | Optional: “We’re coordinating your coaches around this focus…” | WS1 workflow instance / stage references observing EST-xx |
| **Recommendations that reference it** | Optional: “This guidance fits your current focus…” | WS3 artefact / set context references to EST-xx |
| **Non-claim honesty** | Implicit: no mastery/success/completion from focus alone | Explicit SB-06…SB-08 / prohibited-interpretation checks |

A context with no current-state → why → warrant → consumer honesty chain is invalid — even if the explanation sounds motivating.

---

## 4. Four State Questions (Binding)

Every material educational state must answer these four questions.

### ESQ-01 — What is the current constitutional state?

**Student examples:**

- “Right now the focus is what to study today under your Study Plan.”
- “Right now the focus is recovering your study rhythm after a disruption.”
- “Right now we’re waiting until your Study Plan can be adjusted — we’re not inventing a tip.”
- “You’re on track with an active Study Plan, and there’s no special focus interrupting ordinary study yet.”

**Developer requirements:**

- Record primary EST-xx (and any parallel-read siblings).
- Record that Article IV meaning-bearing states were not aliased as EST-xx.
- Record SB-06…SB-08 non-claim checks for the narration.

---

### ESQ-02 — Why does this state exist?

**Student examples:**

- “You’ve opened study for the day, so today’s priority coaching leads.”
- “There’s been a meaningful break, so recovery leads before ordinary daily tips.”
- “Several valid next steps competed, so we’re settling which one to act on first.”
- “Nothing new is interrupting your Study Plan, so we’re holding continuity.”

**Developer requirements:**

- Cite entry conditions from `STATE_TYPES.md` for the EST type.
- Cite initiating educational event / warrant / disposition / continuity basis.
- Cite prior primary EST exit when succession required it.

---

### ESQ-03 — What constitutional evidence supports it?

**Student examples:**

- “Your active Study Plan and today’s coaching warrant this focus.”
- “The disruption signal and recovery coaching rules support this focus.”
- “We’re not claiming you’ve mastered anything — this is about focus, not mastery.”

**Developer requirements:**

- Distinguish **context warrants** (plan class, Programme VI warrant IDs, WS1 event class, WS2 RO disposition, continuity hold) from **EIP-002 Educational Evidence of understanding**.
- Forbid treating time-on-task, confidence alone, or UI mode as understanding evidence.
- Record that EST support does not write Article IV states (SB-09).

---

### ESQ-04 — What workflows and recommendations reference it?

**Student examples:**

- “Your study coordination is following this focus.”
- “The guidance you’re seeing is tied to this recovery focus.”
- “No tip yet — we’re waiting on a Study Plan update.”

**Developer requirements:**

- List WS1 workflow instances / stages that observed the EST type (or explicit none).
- List WS3 recommendations / sets that cited the EST type as context (or explicit none).
- List WS2 permission / conflict narrations that consumed the EST type when material.
- Ensure consumers did not treat EST as ownership transfer or tip creation (SB-01 / SB-03).

---

## 5. Audience Patterns

### 5.1 Student pattern (focus, not score)

> “Right now we’re focusing on **[plain EST meaning]**.  
> That’s because **[why]**.  
> This is about **where we are**, not a judgement that you’ve mastered the topic or finished everything.”

### 5.2 Developer pattern (audit)

```text
primary_est: EST-xx
parallel_read: [EST-yy?]
entry: <conditions + warrant refs>
exit_of_prior: <EST-zz | none>
context_warrants: [plan | programme_vi | ws1_event | ws2_disposition | continuity]
article_iv_identity: false
workflows_referencing: [...]
recommendations_referencing: [...]
boundary_pass: [SB-01…SB-10]
prohibited_interpretation_pass: true
```

---

## 6. Special Cases

| Situation | Explainability rule |
|-----------|---------------------|
| **EST-01 Absent Plan** | Say plainly that day coaching waits on a Study Plan; do not invent tips |
| **EST-10 Conflict Disposition** | Explain waiting / settling among valid options; do not narrate a fake single coach merge |
| **EST-11 Escalation Await** | Explain waiting for plan / ownership resolution; prefer no-recommendation |
| **EST-12 Continuity Holding** | Explain holding as lawful care, not product emptiness or student failure |
| **Succession EST-07 → EST-03** | Name the return to ordinary daily focus when material (continuity) |
| **Article IV mentioned in speech** | Keep “Study Progress / evidence / estimates” clearly distinct from EST focus |

---

## 7. Relationship to Other Explainability Corpora

| Corpus | Explains | State explainability adds |
|--------|----------|---------------------------|
| Programme VI coach / planner explainability | Why the educational answer means what it means | Frames *which focus context* made that question live |
| WS1 workflow explainability | Why flow started / who participated / outcome | Names EST context observed along the path |
| WS2 authority / conflict explainability | Why owner permitted / how concurrency dispositioned | May cite EST-10 / owner-aligned EST types as situation |
| WS3 recommendation / assembly / set explainability | Why tip / set exists | May cite EST-xx as context reference — never as tip source |

State explainability **does not replace** Programme VI educational explainability. It **frames** constitutional context.

---

## 8. Non-Responsibility of Explanation

Explanation must **not**:

- invent EST types absent from `STATE_TYPES.md`;
- claim success, mastery, or workflow completion from context (SB-06…SB-08);
- create recommendations in speech that lack Programme VI / WS3 warrant (SB-01);
- transfer ownership in narration (SB-03);
- redefine Educational Evidence (SB-02);
- treat Version 2 operational state machines as this Model’s constitutional vocabulary.

---

## 9. Binding Summary

| ID | Question |
|----|----------|
| **ESQ-01** | What is the current constitutional state? |
| **ESQ-02** | Why does this state exist? |
| **ESQ-03** | What constitutional evidence / warrants support it? |
| **ESQ-04** | What workflows and recommendations reference it? |

Every material educational-state narration must answer ESQ-01…ESQ-04 for the appropriate audience — and must refuse evaluative overclaim.

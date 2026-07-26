# Resolution Explainability

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS002 — Conflict Resolution Framework  
**Classification:** Explainability contract for educational conflict resolution  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **educational conflict resolution** — why a conflict existed, which constitutional rules applied, why the outcome was lawful, and how authority ownership was preserved.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`CONFLICT_RESOLUTION_FRAMEWORK.md`](CONFLICT_RESOLUTION_FRAMEWORK.md)
4. [`CONFLICT_TYPES.md`](CONFLICT_TYPES.md)
5. [`RESOLUTION_PRINCIPLES.md`](RESOLUTION_PRINCIPLES.md)
6. [`RESOLUTION_OUTCOMES.md`](RESOLUTION_OUTCOMES.md)
7. [`../authority/AUTHORITY_EXPLAINABILITY.md`](../authority/AUTHORITY_EXPLAINABILITY.md) — ownership-layer narration (complementary)
8. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) — orchestration-layer narration (complementary)
9. Programme VI explainability corpora for each contributing owner

> **Explainability improves understanding of resolution already authorised.  
> It never invents educational certainty, a second owner, or a discretionary winner story.**

---

## 1. Purpose

Students should never have to guess why recovery guidance led while today’s plan topic waited, or why two good pieces of advice did not both demand equal action.

Developers should never have to reverse-engineer whether a “winner tip” transferred ownership, rewrote meaning, or merely dispositioned action.

Resolution explainability exists so every material conflict resolution answers — in the right language for the audience:

1. **Why a conflict existed**
2. **Which constitutional rules applied**
3. **Why the outcome was lawful**
4. **How authority ownership was preserved**

Without resolution explainability:

- deferred guidance feels like the system “changed its mind” arbitrarily;
- supersession feels like coaches arguing;
- merges feel like anonymous mega-advice;
- audits cannot prove ownership survived concurrency.

With resolution explainability:

- the student trusts which tutor voice leads *now* and what still stands;
- developers can verify CT / RP / RO chains against this corpus;
- preservation is speakable (RP-01 / RP-02);
- discretion is visible when absent — and refuseable when present.

---

## 2. Relationship to Sibling Explainability

| Layer | Document | Student question |
|-------|----------|------------------|
| **Programme VI meaning** | Coach / planner explainability corpora | Why is this educational guidance warranted? |
| **Authority ownership** | [`../authority/AUTHORITY_EXPLAINABILITY.md`](../authority/AUTHORITY_EXPLAINABILITY.md) | Why this component decided? Why not another? How was ownership preserved by design? |
| **Workflow orchestration** | [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) | Why did this workflow start / hand off / conclude? |
| **Conflict resolution** | **This document** | Why did several valid guidances compete? Which rules chose what leads? Why was that lawful? Did ownership survive? |

Resolution speech must remain consistent with ownership and orchestration speech. It adds **concurrency disposition clarity**; it does not invent a second educational story or a new owner.

Authority explainability emphasises **conflict prevention by design** (AP-01).  
Resolution explainability emphasises **conflict disposition when valid artefacts still compete for action** (MS002).  
Both may appear in one student journey; they must not contradict.

---

## 3. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Which guidance leads now; what waits and why; honest limits; that the plan/coach roles were not secretly rewritten | CT/RP/RO IDs, score vectors, optimiser jargon, Twin facets |
| **Developer / auditor** | Precise constitutional references | CT-xx, RP-xx, RO-xx set, owners preserved, higher obligations applied, no ownership transfer, no meaning rewrite | Student motivational fluff as a substitute for audit fields |

Student copy narrates tutor posture under concurrency. Developer traces cite document IDs and outcome sets.

---

## 4. Traceability Obligation

Every material conflict resolution must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Conflict kind** | “You had more than one good kind of guidance at once…” / “Recovery needed to lead for now…” | CT-xx (+ secondary if any) |
| **Competing artefacts** | Plain names of the guidances that competed | Owner domain + artefact class for each peer |
| **Validity gate** | Implicit: only real coach/plan guidance counted | RP-05; RO-05 list if any unlawful excluded |
| **Rules applied** | “Because recovery needed to come first…” / “Because we’re not rewriting your Study Plan…” | RP-xx list; higher obligations (RP-03) cited |
| **Outcome set** | What leads; what waits / follows / was set aside as not allowed | RO-06 (or RO-03) + RO-01/02/04/05 as applicable |
| **Ownership preserved** | “Your day coach still owns today’s plan priorities; recovery led the action for now…” | RP-01 pass; owners unchanged |
| **Meaning preserved** | “We’re not saying yesterday’s topic tip was wrong — it waits…” | RP-02 pass; no reinterpretation |
| **Programme VI reasoning** | Leading owner’s educational explainability | Link to coach / planner explainability artefact |
| **Orchestration (if CT-05)** | Optional: “Timing brought both into the same moment…” | Workflow explainability + this resolution layer |

A conflict resolution with no conflict → rules → outcome → preservation chain is invalid — even if the UI shows a single tip smoothly.

---

## 5. Four Resolution Questions (Binding)

Every material conflict resolution must answer these four questions.

### RQ1 — Why did a conflict exist?

**Student pattern:**

> “You had **[plain description of competing guidances]** at the same time, and we can’t treat all of them as the main next step together.”

**Developer pattern:**

> `conflict=CT-xx; peers=[owner:artefact, …]; competition=primary_action; ownership_dispute=false`

### RQ2 — Which constitutional rules applied?

**Student pattern:**

> “We’re letting **[leading educational obligation in plain speech]** lead because **[honest educational reason — e.g. recovery after disruption / not rewriting your Study Plan / …]**.”

**Developer pattern:**

> `principles=[RP-…]; higher_obligations=[AB-xx|EIP-…|…]; application_order=RP-08→…→RP-10`

### RQ3 — Why was the outcome lawful?

**Student pattern:**

> “So for now: **[leading guidance]**. **[Deferred / waiting guidance]** still stands — we’re not throwing it away or changing what it means.”

**Developer pattern:**

> `outcomes={acted_upon: RO-06|RO-03, dispositions:[{artefact, RO-xx}, …]}; single_primary=true; merge_pathway=null|cited`

### RQ4 — How was authority ownership preserved?

**Student pattern:**

> “We’re **not** giving one coach the other coach’s job. **[Owner A]** still owns **[domain in plain speech]**; **[Owner B]** still owns **[domain]** — we only chose what to do first.”

**Developer pattern:**

> `ownership_preserved=true; owners_unchanged=[AD-…]; meaning_unchanged=true; transfer=false; authority_model_amended=false`

All four RQs are mandatory for material resolutions. Omitting RQ4 is an architectural defect.

---

## 6. Mandatory Explanation Themes by Outcome

### 6.1 Acted upon (RO-06)

Student: which guidance leads and why it is the main step *now*.  
Developer: `RO-06; owner=…; RP list`.

### 6.2 Deferred (RO-01)

Student: what waits and that it is not discarded.  
Developer: `RO-01; owner unchanged; reason=yielded_to_primary|higher_obligation`.

### 6.3 Superseded (RO-02)

Student: what replaced earlier *action*; earlier guidance’s meaning still recognised.  
Developer: `RO-02; earlier=…; later=…; action_replaced=true; ownership_replaced=false`.

### 6.4 Merged (RO-03)

Student: both roles named; composite not anonymous.  
Developer: `RO-03; merge_pathway=cited; contributors=[…]`.

### 6.5 Queued (RO-04)

Student: what comes after the leading step when the later window is lawful.  
Developer: `RO-04; owner unchanged; later_window=constitutional`.

### 6.6 Rejected as unlawful (RO-05)

Student: honest refusal without shaming; name what would be rightful if known.  
Developer: `RO-05; boundary|domain failure; rightful_owner=…|none`.

### 6.7 Ownership dispute refusal (RP-08)

Student: system will not invent dual ownership or a merged mega-coach.  
Developer: `refused=ownership_dispute; AP-01; no_RO-06_among_disputants`.

---

## 7. What Resolution Explainability Must Never Do

| Unlawful narration | Why |
|--------------------|-----|
| “The algorithm picked the higher score” | RP-04 — discretion / scoring is not educational law |
| “Recovery now owns your daily plan” | RP-01 — ownership transfer fiction |
| “That earlier tip was wrong because we switched” | RP-02 / RO-01–RO-02 — disposition ≠ invalidation of meaning |
| “We merged everything into one tip” (without pathway) | RO-03 exceptional; AB-08 |
| “The workflow decided what you should study” | RP-09 — orchestration non-education |
| Inventing certainty of pass/mastery from resolution | EIP-006 / AB-06 |
| Hiding an ownership dispute as a friendly merge | RP-08 |

---

## 8. Completeness Checklist

Before shipping student- or developer-facing conflict narration, confirm:

- [ ] RQ1–RQ4 answered for the audience
- [ ] CT-xx classified; P1–P4 held (or unlawful / ownership-dispute path taken instead)
- [ ] RP application recorded (including RP-03 higher obligations if any)
- [ ] Outcome set uses only RO-xx from this corpus
- [ ] Single primary (or cited RO-03 pathway)
- [ ] Ownership and meaning preservation explicit
- [ ] Programme VI explainability for the acted-upon owner linked
- [ ] No scoring / optimiser / job-queue jargon presented as educational law

---

## 9. Closing

Conflict resolution is trustworthy only when it can say — plainly and constitutionally — **why concurrency existed, which rules chose the leading action, why that was lawful, and that ownership survived.**

> **Why the conflict. Which rules. Why lawful. How ownership stayed intact.**

# Known-Unknowns Register

**Artefact:** Standing product record of what Kwalitec can genuinely show today, and what it genuinely cannot yet prove  
**Origin:** Quality Gate item 11 (locked Quality Gate, 2026-09-11 / 2026-09-12)  
**Status:** Active living register  
**Audience:** Internal product, engineering, and board readers (not student-facing copy)  
**Does not:** Change runtime, amend EF-001, alter P-002.1 gates, or authorize public educational-effectiveness claims  

**Companions (do not replace this register):**

| Companion | Role |
|---|---|
| [`p003_4_product_assumption_register/`](p003_4_product_assumption_register/) | What Version 1 assumes (known / believed / rejected) |
| [`p003_5_evidence_hierarchy/`](p003_5_evidence_hierarchy/) | What claim language evidence levels permit |
| [`p003_3_product_risk_register/`](p003_3_product_risk_register/) | What could block successful release |
| [`EF001_OPERATIONAL_REVIEW_INTERLEAVED_PRACTICE.md`](../../EF001_OPERATIONAL_REVIEW_INTERLEAVED_PRACTICE.md) | Formal boundary on classic within-session interleaving |

---

## Claim levels used by this register

Tonight's Quality Gate work treats product claims in four levels. Levels 1-3 can be verified directly from code, content, and learner-facing surfaces. Level 4 cannot.

| Level | Name | What it asks | Provable without a real student's exam outcome? |
|---|---|---|---|
| **1** | Mechanical correctness | Did the system do what the code and records say it did? | Yes |
| **2** | Educational correctness | Is the authored educational substance true and coherent? | Yes, by audit and SME judgment |
| **3** | Learner-facing quality | Do the product's own words match the mechanisms that actually run? | Yes, by claim-to-capability audit |
| **4** | Effectiveness | Did this help someone learn or pass? | No. Not without a real student, and this project has permanently ruled out using a real student's actual exam outcome as an experiment to prove it |

This register exists so that distinction is a durable part of the product's own record, not a conversation-only memory.

---

## SECTION 1 - What Kwalitec can genuinely show today (with real evidence)

Each item below is a claim that is true today because Quality Gate work verified it, fixed it, or both. These are Level 1-3 claims.

### 1.1 What content was presented in a sitting

**Claim:** For an executed Session, the product can show which authored package and items were presented.

**Why this is true today:** Runtime C session records and package activity persistence hold the presented package and response surface. Quality Gate item 2's evidence-integrity work closed silent empty-store divergence on the session document path (composition-based durable store wiring; bare in-memory constructors hardened so callers cannot quietly receive a separate empty store when durability is on).

### 1.2 What the learner submitted

**Claim:** For scored practice, the product can show the submitted response (MCQ choice or numeric entry).

**Why this is true today:** Submissions are written onto the session response document. After Quality Gate item 2's durability fixes (shared durable-store pattern for session documents and Objective Evidence), scored submissions are not process-RAM-only on the production durable-store path.

### 1.3 Whether a submission was scored correct

**Claim:** The product can show the mechanical score outcome for a submitted practice item.

**Why this is true today:** Scoring runs on the package activity path and is recorded with the response. This is Level 1 mechanical correctness: match against the authored accepted answer / correct choice, not a claim that the learner has mastered the topic.

### 1.4 What educational evidence was durably recorded

**Claim:** After tonight's evidence-integrity fixes, scored practice evidence that the live pipeline intends to keep is durably recorded on the production durable-store path, and campaign-revision sittings no longer attribute practice to the tip-topic surrogate.

**Why this is true today:**

- Quality Gate item 2 fixed fabricated Twin contamination in local founder data, made Objective Evidence genuinely durable (ending the false "durable" RAM claim), and hardened remaining bare store constructors against silent divergence.
- Earlier same-night identity work closed Twin/Policy V1 wrong-key resolution, Twin durability (writer vs reader store), and VP-001 practiced-node attribution.
- Quality Gate item 3 Finding A (campaign revision packages remapped to tip topic `5.1` for mission generation, then treated as practiced identity for Twin / LEE / SQL) was fixed by resolving practiced identity from `return_targets` rather than the tip surrogate.

This claim is about durable recording and correct attribution on the closed paths. It is not a claim that every historical flag-gated or deferred companion path is complete (see Section 2 for residual identity risk).

### 1.5 What policy selected a sitting, and why

**Claim:** When Adaptive / Policy V1 selection is in play, the product can show which sitting won and the selection reason chain (for example overdue, due, adaptive, sequential).

**Why this is true today:** Arbitration and selection-reason surfaces are deterministic and inspectable. Quality Gate claim-honesty work (item 7) also forced learner-facing Help copy to describe the live mechanism rather than a readiness-signal fiction. When Policy V1 is dark / default OFF, the honest claim is the plan-and-precedence path that actually runs, not an adaptive narrative.

### 1.6 Why a calendar review was due

**Claim:** The product can show that a spaced review is due or overdue from the spacing scheduler's calendar ladder and recorded exposures.

**Why this is true today:** Spacing is an implemented calendar mechanism keyed by package exposure and ladder step (including the narrow metacognition ladder-step nudge). "Due because the calendar ladder says so" is a Level 1 fact. "Due because this interval is educationally optimal" is not (Section 2).

### 1.7 What state transitions occurred

**Claim:** The product can show mission/session lifecycle transitions that the runtime recorded (started, completed, reflection captured when written, educational events emitted on the completion path).

**Why this is true today:** Runtime educational events and session completion bridges record those transitions. Quality Gate item 2 made the durability story honest for the stores that hold them on the production path.

### 1.8 Catalogue numeric content correctness (checkable subset)

**Claim:** Across the full CS1 `publication_approved` catalogue audited in Quality Gate item 1 (**393** items: 130 worked examples + 263 knowledge checks), every mechanically checkable numeric chain recomputes to the authored answer.

**Why this is true today:** Item 1 classified all 393 items, independently recomputed all **139** mechanically checkable items (**264** numeric claims + **2** algebraic identities), and found **zero** content-correctness discrepancies. The remaining **254** conceptual items were inventoried for SME review and worked through item 1's SME queues (including real defect fixes found in that pass). Numeric chain truth for the checkable subset is proven by recomputation. Conceptual truth rests on that SME pass, not on arithmetic re-derivation.

### 1.9 Learner-facing claim honesty for the closed overclaim set

**Claim:** The eight confirmed claim-to-capability overclaims closed in Quality Gate item 7 now match live mechanisms in Help, brand descriptor, Study Sensei framing, Learning Check / Quick Check copy, session briefing epistemology, and login pairing.

**Why this is true today:** Item 7's audit found live mismatches; the approved rewrites were wired exactly; regressions lock the honest text in `tests/test_claim_capability_honesty_qg7.py`. This is Level 3 honesty for those surfaces. It does not prove educational effectiveness.

---

## SECTION 2 - What Kwalitec genuinely cannot yet prove

Each item below is an open question. None of these is secretly resolved. Where a related mechanism exists, that mechanism is named plainly so the gap is not confused with "feature missing entirely."

### 2.1 Effectiveness and outcome (single most important open question)

**Open question:** Does using Kwalitec actually help someone learn, or pass their professional exam?

**Status:** Permanently unresolved at Level 4 by design for this project's current evidence rules.

**Why it stays open:** Levels 1-3 can be verified without treating a real student as an experimental subject whose exam outcome proves the product. This project has explicitly and permanently ruled out using a real student's actual exam outcome as an experiment to prove effectiveness. External educational-outcome evidence therefore remains absent. Perception, activity, and engineering verification do not substitute for it.

**Related board posture:** Educational effectiveness and Version 1 production-ready declaration remain outside what this register upgrades. Companion law: P-003.5 Claim Standard (C-EDU / C-BEN / C-V1), EP-007.3 effectiveness Stage 1, P-002.1 Gate G1.9.

### 2.2 Whether the calendar-only spacing schedule is genuinely optimal

**Open question:** Are the current spacing intervals the right intervals for learning, or merely consistent calendar delays?

**Status:** Unproven.

**What exists today:** A real spacing scheduler with calendar ladder steps, due/overdue states, and exposure recording. Metacognition can nudge the ladder by a bounded calendar step.

**What does not exist:** Evidence-based interval optimization from forgetting curves, retrieval strength, or outcome trials. "Review is due on this date" is showable. "This date is educationally optimal" is not.

### 2.3 Whether mastery can be reliably claimed with sparse evidence

**Open question:** When evidence is thin, can the product reliably claim mastery (or equivalent strong understanding language)?

**Status:** Unproven, and currently ungated.

**What exists today:** Practice evidence, Estimated Knowledge / Twin facts on authorized paths, and honest copy that practice is not a grade.

**What does not exist:** A mastery gate that refuses strong mastery claims until evidence density and consistency clear a defined bar. Sparse evidence can still produce a number. A reliable mastery claim from sparse evidence cannot yet be proven, and the product must not talk as if that gate exists.

### 2.4 Whether the narrow metacognition effect meaningfully helps

**Open question:** Does the live metacognition path (confidence captured at reflection, applied as a bounded spacing ladder-step nudge) meaningfully help learning?

**Status:** Unproven.

**What exists today:** A real, narrow mechanism: stated confidence can move the calendar ladder by a bounded step. That is Level 1 true.

**What is not proven:** That this narrow effect improves retention, study decisions, or exam outcomes. The mechanism is deliberately small. Small and real is not the same as educationally meaningful.

### 2.5 Whether interleaving would improve outcomes if built

**Open question:** If classic within-session interleaved practice were built for this curriculum, would outcomes improve?

**Status:** Unproven, and deliberately not built.

**What was done instead:** A completed EF-001 Operational Review for interleaved practice (`EF001_OPERATIONAL_REVIEW_INTERLEAVED_PRACTICE.md`). Live arbitration forbids session-split mixing; Educational Atomicity and the Study Progress vs understanding split make classic within-session multi-topic mix a framework-boundary question, not a missing toggle. Day-level spaced or adaptive revisits are not substitutes for within-session interleaving.

**Honest residual:** The review documents the boundary and the deferral. It does not prove that building interleaving would help, and it does not prove that leaving it unbuilt is educationally optimal. Both sides remain Level 4-open.

### 2.6 Latent identity-mismatch risks banked from the canonical identity audit

**Open question:** Will the four latent identity-mismatch findings from Quality Gate item 3 fire in live use?

**Status:** Real structural risks. Not yet proven to have fired. Not ruled out.

Finding A (campaign revision tip-surrogate attribution) was a live instance of the class and was fixed. The audit banked four further findings of the same class that remain latent:

| Banked finding | Risk |
|---|---|
| **B** | Title-only ORM ↔ published/engine joins. Duplicate titles across syllabus years or multiple active curricula can attach Twin / TopicProgress to the wrong ORM id while looking fine. |
| **C** | Runtime version → engine version soft fallback. On version mismatch, mapping falls back to latest engine version (logged, not raised). Downstream code→ORM joins can bind the wrong year's topic. |
| **D** | Legacy mission title substring → ORM topic (`mission/routes`). Substring match or fallback-to-next-incomplete can mark progress on the wrong topic if that path runs. |
| **E** | Assessment ingress takes first learning-objective only. Multi-LO bundles attribute every item to LO`[0]`. |

These are not theoretical neatness complaints. They are the same identity-mismatch class that already produced multiple live bugs tonight. Absence of a proven production incident for B-E is not evidence that the joins are safe.

---

## SECTION 3 - How this register should be maintained

This document is a living permanent artefact, not a one-time snapshot of Quality Gate night.

Update it whenever either of the following happens:

1. **A known unknown becomes a proven capability.** When a Quality Gate item, audit, fix, or evidence programme resolves an open question into something that can genuinely be shown, move it from Section 2 to Section 1 with a short note of what verified or fixed it, and the date.
2. **A new unresolved question is found.** When investigation surfaces a real open question that the product cannot yet prove, add it to Section 2 without hedging and without implying it is already handled.

Maintenance rules:

- Prefer precise past-tense evidence ("verified by…", "fixed in…") over aspirational future tense.
- Do not promote Level 4 effectiveness claims into Section 1 without the governing evidence standard in P-003.5 (and related gates). Engineering pride and internal perception do not close Section 2.1.
- Do not remove a Section 2 item because the related mechanism exists. Existence of a calendar, a confidence nudge, or a Twin number is often exactly why the open question must stay visible.
- Keep student-facing copy out of this file. Learner honesty belongs in product surfaces and claim-honesty tests; this register is the internal ledger of epistemic status.

**Last substantive update:** 2026-09-12 (Quality Gate item 11 initial register)

# Explanation Examples

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS003 — Educational State Explainability  
**Classification:** Illustrative constitutional explanation patterns  
**Status:** APPROVED — governing as pattern law; examples are illustrative, not a closed product-copy catalogue  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document provides **illustrative constitutional explanation patterns** for educational state (constitutional context) and contextual progression.

Subordinate to:

1. [`EDUCATIONAL_STATE_EXPLAINABILITY.md`](EDUCATIONAL_STATE_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md)
4. [`EXPLANATION_BOUNDARIES.md`](EXPLANATION_BOUNDARIES.md)
5. [`../state/`](../state/)
6. [`../state_transitions/`](../state_transitions/)

> **Examples illustrate lawful shape.  
> They are not Runtime A copy, UI templates, or a scoring rubric.**

---

## 1. How to Read These Patterns

Each pattern includes:

| Section | Role |
|---------|------|
| **Situation** | Educational / constitutional setup |
| **Student speech** | Plain-language context / progression narrative (ESEP-10) |
| **Developer trace** | Constitutional audit shape (ESEC-01…ESEC-10) |
| **ESEQ coverage** | How ESEQ-01…ESEQ-05 are answered |
| **Unlawful contrast** | Narration that would cross ESEB boundaries |

Patterns deliberately avoid binding product microcopy. Wording may vary; constitutional facts must not.

---

## 2. Pattern Catalogue

| ID | Pattern | Situation family |
|----|---------|------------------|
| **SXP-E01** | Initial contextual state | First speakable EST posture; no prior succession in window |
| **SXP-E02** | Single state transition | One CST step; from/to EST; continuity preserved |
| **SXP-E03** | Multiple contextual transitions | Ordered CST chain across intermediate EST postures |
| **SXP-E04** | Workflow-referenced contextual progression | C-FLOW facts situate succession; State Engine did not execute the workflow |

---

## 3. SXP-E01 — Initial Contextual State

### Situation

An Active-class Canonical Study Plan is present. The student opens study for the day. Day Priority Context (EST-03) is the first speakable primary posture in the explanation window. No CST succession has occurred yet. Daily Coach guidance may later reference this focus; no tip is invented by the State Engine.

### Student speech (illustrative)

> “Right now we’re focusing on **what is most useful today** under your Study Plan. That’s because you’ve opened study for the day, and today’s priority coaching is the live question. This is about **where we are**, not a judgement that you’ve mastered anything or finished everything.”

### Developer trace (illustrative)

```
primary_est: EST-03
parallel_read: none
preceding_est: initial
cst_path: none
context_evidence:
  warrants: [active_canonical_study_plan, programme_vi_daily_today_priority]
  understanding_evidence_alias: false
rules_applied: [EST-03_entry, SB-01..SB-10_checked]
continuity:
  prior_est_recorded: baseline_initial
  eip005_pass: true
  article_iv_mutated: false
workflows_referencing: none
authority_refs: none
recommendations_referencing: none
non_claim:
  boundary_pass: [SB-06, SB-07, SB-08]
  prohibited_interpretation_pass: true
```

### ESEQ coverage

| ESEQ | Answer |
|------|--------|
| ESEQ-01 | EST-03 Day Priority Context |
| ESEQ-02 | Day opened under Active plan; today-priority warrant |
| ESEQ-03 | Initial — no succession in window |
| ESEQ-04 | Plan class + Programme VI daily warrant; SB non-claims |
| ESEQ-05 | No workflow / authority / tip consumers yet (explicit none) |

### Unlawful contrast

> “You’re in day mode — so today’s mission is complete.” / “The app picked this mode.” / “Because `rank=0.88`…”

Violates ESEP-06 / ESEB-06 / ESEB-10.

---

## 4. SXP-E02 — Single State Transition

### Situation

Primary context was Day Priority (EST-03). A meaningful study-rhythm disruption is warranted. CST-07 (coach-focus succession) moves primary context to Recovery (EST-07). Ownership of day-priority decisions remains with Daily Coach when that question returns; Recovery owns recovery decisions. Continuity of the prior day focus is preserved in speech. No tip is minted by succession.

### Student speech (illustrative)

> “We’re changing focus from **today’s priorities** to **recovering your study rhythm**. That’s because there’s been a meaningful break, so restorative focus leads before ordinary daily tips. We’re **not** rewriting your Study Plan, and we’re **not** saying you’ve failed or mastered anything — this is about where we are now, and we’re not forgetting that today’s priorities were the focus before.”

### Developer trace (illustrative)

```
primary_est: EST-07
parallel_read: none
preceding_est: [EST-03]
cst_path: [CST-07]
context_evidence:
  warrants: [disruption_signal, programme_vi_recovery_warrant, active_canonical_study_plan]
  understanding_evidence_alias: false
rules_applied:
  - EST-03_exit
  - EST-07_entry
  - CST-07
  - condition_families: [G_coach_focus, C-CONTEXT]
  - STB-01..STB-10_checked
continuity:
  prior_est_recorded: true
  eip005_pass: true
  article_iv_mutated: false
workflows_referencing: none
authority_refs: [authority_explainability_ref=recovery_leads_action]
recommendations_referencing: none
non_claim:
  boundary_pass: [SB-03, SB-06, SB-07, STB-02, STB-04]
  prohibited_interpretation_pass: true
```

### ESEQ coverage

| ESEQ | Answer |
|------|--------|
| ESEQ-01 | EST-07 Recovery Context |
| ESEQ-02 | Disruption warrant makes recovery the live question |
| ESEQ-03 | EST-03 → CST-07 → EST-07; prior day focus recorded |
| ESEQ-04 | Recovery warrant + EST exit/entry + CST-07 + STB checks |
| ESEQ-05 | Optional authority ref; no tip invented by State Engine |

### Unlawful contrast

> “Recovery now owns your daily plan.” / “You succeeded at getting into recovery.” / “The State Engine decided Topic X.”

Violates ESEB-06 / ESEB-07 / ESEB-09.

---

## 5. SXP-E03 — Multiple Contextual Transitions

### Situation

An ordered progression across one study sitting window:

1. Continuity Holding (EST-12) → Day Priority (EST-03) via CST-12 exit / day warrant  
2. Day Priority (EST-03) → Session (EST-04) via CST-02 nested open  
3. Session (EST-04) → Reflection (EST-05) via CST-02/CST-03 family close-and-open under published nest rules  
4. Reflection (EST-05) → Day Priority (EST-03) via CST-03 nested return  

Intermediate postures remain speakable. No intermediate is erased. No mastery claim from completing the sitting. Session/reflection close does not complete a workflow by EST label alone.

### Student speech (illustrative)

> “You moved from a steady hold into **today’s priorities**, then into a **study sitting**, then into **reflection** after the sitting, and now back to **today’s priorities**. Each step followed your Study Plan and sitting rules — we’re not forgetting the sitting or pretending reflection means you’ve mastered the topic. This is the story of **where focus was**, not a score.”

### Developer trace (illustrative)

```
primary_est: EST-03
parallel_read: none
preceding_est: [EST-12, EST-03, EST-04, EST-05]
cst_path: [CST-12, CST-02, CST-02_or_CST-03_nest_advance, CST-03]
context_evidence:
  warrants:
    - continuity_hold_then_day_warrant
    - programme_vi_session_authorised
    - programme_vi_reflection_loop_closure
  understanding_evidence_alias: false
rules_applied:
  - EST-12_exit / EST-03_entry
  - EST-03_exit / EST-04_entry (CST-02)
  - EST-04_exit / EST-05_entry
  - EST-05_exit / EST-03_entry (CST-03)
  - STB continuity + nest rules
continuity:
  prior_est_recorded: true
  intermediates_preserved: true
  eip005_pass: true
  article_iv_mutated: false
workflows_referencing: none
authority_refs: none
recommendations_referencing: none
non_claim:
  boundary_pass: [SB-06, SB-07, SB-08, STB-02, STB-03, STB-07]
  prohibited_interpretation_pass: true
```

### ESEQ coverage

| ESEQ | Answer |
|------|--------|
| ESEQ-01 | EST-03 Day Priority (post-return) |
| ESEQ-02 | Nested return after reflection under day warrant |
| ESEQ-03 | Ordered EST-12 → EST-03 → EST-04 → EST-05 → EST-03 via CST path |
| ESEQ-04 | Nest open/return rules + continuity; no understanding Evidence alias |
| ESEQ-05 | Explicit none unless a tip/workflow later references post-return focus |

### Unlawful contrast

> “You finished the session — you’ve completed learning.” / “Skip straight to today; the sitting didn’t matter.” / Invent undocumented EST types for “warmup mode.”

Violates ESEP-03 / ESEB-06 / SEXI-01.

---

## 6. SXP-E04 — Workflow-Referenced Contextual Progression

### Situation

WS1 records a lawful handoff: coordination that had been sequencing ordinary day study now invites Recovery as primary authority for the stage (workflow progression fact). Concurrently, MS002 CST-07 updates primary context EST-03 → EST-07 because recovery warrants hold. The Educational State Engine **references** the published WS1 progression/completion fact as C-FLOW supporting evidence; it does **not** execute the workflow, invent stages, or author tips. Authority explainability may separately narrate why Recovery was permitted to lead action.

### Student speech (illustrative)

> “We’re shifting focus to **recovery** because restoring continuity after a disruption is the live question — and your study coordination has handed focus to recovery coaching for this stretch. The coordination didn’t invent what you should study; it followed the educational question. This is about **focus and coordination**, not mastery or a finished workflow certificate.”

### Developer trace (illustrative)

```
primary_est: EST-07
parallel_read: none
preceding_est: [EST-03]
cst_path: [CST-07]
context_evidence:
  warrants:
    - disruption_signal
    - programme_vi_recovery_warrant
    - C-FLOW: ws1_handoff_to_recovery_stage  # referenced, not executed
  understanding_evidence_alias: false
rules_applied:
  - EST-03_exit
  - EST-07_entry
  - CST-07
  - C-RULE cites: WS1_transition_explainability_ref
  - STB-06_state_engine_did_not_execute_workflow
continuity:
  prior_est_recorded: true
  eip005_pass: true
  article_iv_mutated: false
workflows_referencing: [ws1_instance_…_recovery_stage]
authority_refs: [authority_explainability_ref=AD-04_leads_action]
recommendations_referencing: none
non_claim:
  boundary_pass: [SB-03, SB-08, STB-04, STB-06, STB-07]
  prohibited_interpretation_pass: true
  executed_by_state_engine: false
```

### ESEQ coverage

| ESEQ | Answer |
|------|--------|
| ESEQ-01 | EST-07 Recovery Context |
| ESEQ-02 | Recovery warrant + coordination handoff situating the focus |
| ESEQ-03 | EST-03 → CST-07 → EST-07 |
| ESEQ-04 | Context warrants + CST rules + C-FLOW *reference* only |
| ESEQ-05 | Workflow instance referenced; authority ref optional; no tip authorship |

### Unlawful contrast

> “The workflow decided you should study Topic X.” / “The State Engine completed your recovery workflow.” / “Flag `FORCE_RECOVERY` is why you’re here” as sole justification.

Violates ESEB-04 / ESEB-09 / ESEB-10 / SEXI-09.

---

## 7. Pattern Notes (Cross-Cutting)

| Note | Rule |
|------|------|
| **Refuse / remain** | A fifth lawful family exists (CST-13) — narrate why focus did *not* change; treat as first-class honesty (see MS002 `TRANSITION_EXPLAINABILITY.md`) |
| **Holding / await** | EST-10…EST-12 speech must remain dignified care, never emptiness or student blame |
| **Tips under focus** | When recommendations appear, link WS3 / Programme VI explainability; EST remains context reference only |
| **Article IV** | Keep Study Progress / Evidence / estimates distinct from EST focus language |

---

## 8. Closing

These patterns show lawful shape for educational-state speech:

> **Initial focus named. Single and multi-step succession traced. Workflow facts referenced without execution fiction. Continuity preserved. Mastery never implied.**

Use them as constitutional templates — not as locked product copy.

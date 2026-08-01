# EA-004 — Reading Guidance Architecture

**Programme:** Educational Excellence Programme EA-004 — Study Session Architecture & Educational Flow  
**Status:** Binding — Guided Reading philosophy and architecture for Version 1 onward  
**Effective:** 2026-08-01  
**Parent:** `EA004_SESSION_BLUEPRINT.md` · `EA004_STUDY_SESSION_FLOW.md`  
**Related:** EP-04 Guided Reading · EP-01 Educational Leverage · Guidance Over Content · `EA001_SESSION_PHILOSOPHY.md` §5–6 · Mission `cmp_reading_scope`  
**Nature:** Reading architecture law — not educational content, not application code  

---

## 1. Purpose

Define how Kwalitec conducts **Guided Reading** so that:

- the CMP remains the **authoritative learning material**;
- Kwalitec remains the **educational guide**;
- reading is **deliberate, selective, and accountable**;
- the student experiences an excellent tutor — not continuous software interruption.

> Expert tutors rarely say “read the chapter.”  
> They say what to look for, which example to work, what to ignore today, and when to come back.

This document is the permanent Reading Guidance architecture. It does not author reading passages or rewrite CS1.

---

## 2. Purpose of guided reading

| Dimension | Statement |
|-----------|-----------|
| **Educational** | Structure CMP engagement so scarce hours produce extractable understanding, not page-turning. |
| **Tutor** | Multiply the value of the candidate’s Core Reading / CMP by directing attention and demanding return. |
| **Product** | Prove Guidance Over Content: Kwalitec owns decisions and checks; CMP owns exposition. |
| **Trust** | Never force the student to abandon Kwalitec mid-Session because reading was an empty shell (EV-001 TB-007). |

### What guided reading is not

- Not a second textbook inside Kwalitec  
- Not an open-ended “read everything” timer  
- Not a chatbot narrating the chapter  
- Not a free-text box with no locus or prompts  
- Not mastery evidence by itself  

---

## 3. Architecture overview

```text
READING PREPARATION          (Kwalitec: dense)
        ↓
READING OBJECTIVES           (Kwalitec: present)
        ↓
MISCONCEPTION HIGHLIGHTS     (Kwalitec: brief watch-list)
        ↓
ATTENTION DIRECTIVES         (Kwalitec: what to hunt / ignore)
        ↓
EXIT INTO READING            (Kwalitec yields)
        ↓
UNINTERRUPTED CMP STUDY      (Student + CMP)
        ↕
SPARSE PAUSE POINTS          (optional; designed)
        ↓
STOP CONDITION MET
        ↓
RE-ENTRY AFTER READING       (Kwalitec returns)
        ↓
KNOWLEDGE CHECKS             (retrieval / practice)
```

---

## 4. How reading objectives are presented

### 4.1 Requirements

Reading objectives must be:

1. **Bound to today’s Mission** learning objective and concept focus.  
2. **Actionable** — verbs the student can execute in the CMP (find, extract, write in own words, attempt before reveal).  
3. **Bounded** — scoped to `cmp_reading_scope` open / stop / out-of-scope.  
4. **Few** — typically **2–4** focus objectives/questions; more dilutes selective attention.  
5. **Visible before exit** — student sees them before deep CMP work begins.

### 4.2 Presentation standard

| Element | Standard |
|---------|----------|
| Lead line | One sentence: what this reading block is for |
| Focus questions | 2–4 numbered questions the CMP should answer |
| Success link | Explicit tie to Mission/Session success criteria (“You will later explain…”) |
| Out of scope | One line naming what **not** to deep-read today |

### 4.3 Fail if

- “Read the material for Today’s topic”  
- Objectives identical to syllabus heading only  
- Objectives that require Kwalitec-pasted CMP prose to answer  
- More than one screen of pre-reading lecture replacing CMP  

### 4.4 Illustrative pattern only

> **Reading objective:** Extract how a GLM joins exponential family, linear predictor, and link.  
> **Q1:** Where is the linear predictor defined? Write it in your own words.  
> **Q2:** Which example shows a non-identity link? Attempt the middle step before reading the solution.  
> **Stop after:** Example 2.  
> **Not today:** Full deviance diagnostics chapter.

---

## 5. How misconceptions are highlighted

### 5.1 Source

Mission field `common_misconceptions` (EA-003) is the primary input. Session Reading Guidance **uses** those misconceptions; it does not invent a textbook error catalogue.

### 5.2 Presentation

| Rule | Requirement |
|------|-------------|
| Timing | Present in Reading Preparation / Guidance — **before** uninterrupted reading |
| Form | Short “watch for” list (1–3 items); each implies what to notice in CMP |
| Tone | Tutor caution — calm, specific — not fear or shame |
| Use later | Feed Knowledge Checks and Reflection prompts |

### 5.3 Fail if

- Empty watch-list on known-risk topics without Board HOLD  
- Long dump of error lists without study use  
- False misconceptions  
- Using misconceptions as continuous interrupt banners during reading  

---

## 6. How attention is directed

Attention direction is the core Guided Reading move (EP-04).

### 6.1 Directives authors must specify

| Directive type | Purpose |
|----------------|---------|
| **Open point** | Exact CMP locus (chapter / section / example / LO) |
| **Hunt targets** | What to look for (definition, identity, step, diagram) |
| **Ignore today** | What to skip so the chapter does not swallow the hour |
| **Annotation task** | One concrete note action (own-words definition; least-clear sentence) |
| **Attempt-before-reveal** | Where to pause *inside* CMP work before reading a solution |
| **Stop condition** | When reading ends and Kwalitec re-enters |

### 6.2 Attention principles

1. **Selective > exhaustive.** Depth on the concept focus beats coverage theatre.  
2. **One centre.** Concept focus remains the gravitational centre of attention.  
3. **Exam-aware when accurate.** Direct attention to examiner-weighted moves without panic.  
4. **Leverage.** Every directive should multiply CMP value (EP-01).

### 6.3 Fail if

- No open point  
- No stop condition  
- Attention directives that paste CMP paragraphs  
- Attention that thrash-switches topics mid-Session  

---

## 7. How Kwalitec exits during uninterrupted reading

### 7.1 Exit is a designed educational event

Exit into reading is not “the app goes idle.” It is the tutor **yielding the floor**.

### 7.2 Exit packet (mandatory)

Before yielding, Kwalitec must leave the student with:

| Packet item | Required |
|-------------|----------|
| Open locus | Yes |
| Focus questions / reading objectives | Yes |
| Stop condition | Yes |
| Return cue (“Come back to Kwalitec when…”) | Yes |
| Annotation / attempt instruction | Yes (at least one) |
| Misconception watch-list | Yes (or Board HOLD) |

### 7.3 During uninterrupted reading

| Kwalitec may | Kwalitec must not |
|--------------|-------------------|
| Remain available via explicit student-initiated return | Push continuous prompts |
| Honour pre-authored sparse Pause Points only | Restate Mission / why-now |
| Show a quiet “return when ready” affordance | Narrate CMP page-by-page |
| Keep timer/duration honest if shown | Claim the student has learned because the timer ran |

### 7.4 Philosophical rule

> **Silence is part of teaching.**  
> An excellent tutor does not talk over the candidate’s reading.

---

## 8. How Kwalitec re-enters after reading

### 8.1 Re-entry triggers

| Trigger | Meaning |
|---------|---------|
| **Stop condition met** | Primary designed path |
| **Student-initiated return** | Always lawful; may prompt “Have you hit the stop point?” |
| **Pause Point completion** | Temporary re-entry → re-exit (not full Knowledge Checks) |

### 8.2 Re-entry behaviour

On full re-entry after reading:

1. **Acknowledge the return** without congratulatory fluff.  
2. **Do not re-brief the Mission** — progressive disclosure (Flow RF-07).  
3. **Move to Knowledge Checks** — closed-book or reduced-cue demand tied to focus questions / success criteria.  
4. **Feedback + advance** — never “answer recorded” dead-ends (TB-008).  
5. **Carry residuals** into Reflection.

### 8.3 Re-entry fail if

- Returns to another wall of Orientation copy  
- Skips Knowledge Checks and treats reading completion as success  
- Pastes CMP “summary” that replaces retrieval  
- Cannot advance stages  

---

## 9. Reading Pause Points (architecture)

Pause Points are **authored sparse checkpoints**, not a conversation layer.

| Property | Rule |
|----------|------|
| Count | Prefer 0–2; soft max 3 for typical Sessions |
| Length | One cue + brief student action |
| Placement | At natural CMP boundaries (after definition; before solution reveal; after example) |
| After pause | **Re-exit** to CMP until stop |
| Certification | Each pause must justify learning value; unjustified pauses fail interruption reject class |

**Pause ≠ Knowledge Check.** Full retrieval belongs after the stop condition.

---

## 10. What must never happen

| ID | Forbidden behaviour | Why |
|----|---------------------|-----|
| RG-X01 | Empty reading stage (prompt + free-text only; no locus/guidance) | TB-007; EP-04 |
| RG-X02 | Placeholder topic strings in reading copy | TB-001 |
| RG-X03 | Pasting CMP / syllabus dump as episode body | V1 E1; Guidance Over Content |
| RG-X04 | Continuous interruption during CMP study | RF-03; tutor feel destroyed |
| RG-X05 | Chatbot-style chapter narration | Product is guide, not textbook |
| RG-X06 | No stop condition / no return path | Student abandoned mid-Session |
| RG-X07 | Reading completion declared as mastery or sole success | EP-06; Constitution VIII |
| RG-X08 | Restacking full Mission brief inside reading UI | SB-09; educational filler |
| RG-X09 | Opening Guided Reading when locus/topic unresolved | Honest refuse required |
| RG-X10 | Mechanical template fragments as “guidance” | Episode audit; EP-09 |
| RG-X11 | Using Reflection textarea as the only reading activity | EP-05; SS-03 |
| RG-X12 | Platform/engineering jargon on reading surfaces | EP-09; TB-012 |

---

## 11. Quality criteria for Reading Guidance (reviewer quick test)

Reading Guidance PASSes only if a reviewer can answer **yes** to all:

1. Would an IFoA tutor send a candidate into the CMP with *these* instructions?  
2. Is the open / stop / out-of-scope unmistakable?  
3. Are focus questions specific to today’s concept focus?  
4. Does Kwalitec clearly exit and clearly re-enter?  
5. Are pauses sparse and justified?  
6. Is CMP still the content authority?  
7. Does post-reading work demand retrieval or performance?  

Any **no** → Gate LE Guided Reading special rule FAIL and/or EA-004 reject class “Lack deliberate reading guidance.”

---

## 12. Relationship to Mission and Episodes

| Artefact | Reading Guidance role |
|----------|----------------------|
| Mission `cmp_reading_scope` | Authoritative locus bounds — Session must implement |
| Mission `common_misconceptions` | Watch-list source |
| Mission `study_strategy` | Must match Guided Reading + subsequent Episode design |
| Learning Episode (Guided Reading) | Primary carrier of Reading Guidance in the Session arc |
| Gate LE special rule | Material locus + focus prompts mandatory; lone free-text box = automatic FAIL |

---

## 13. Explicit non-goals

This architecture does **not**:

- License or reproduce CMP text  
- Generate subject-specific reading passages  
- Redesign UI chrome  
- Amend EP-04 text  
- Claim live Guided Reading defects are remediated  

Successor content programmes author Reading Guidance **instances** under this architecture and certify them under Gate LE + EA-004 Session Certification.

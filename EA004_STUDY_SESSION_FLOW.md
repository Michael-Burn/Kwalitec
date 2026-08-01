# EA-004 — Study Session Flow

**Programme:** Educational Excellence Programme EA-004 — Study Session Architecture & Educational Flow  
**Status:** Binding — educational rhythm and stage handoffs for premium Study Sessions  
**Effective:** 2026-08-01  
**Parent:** `EA004_SESSION_BLUEPRINT.md`  
**Related:** `EA001_SESSION_PHILOSOPHY.md` · `EA004_READING_GUIDANCE_ARCHITECTURE.md` · EP-01–EP-10  
**Nature:** Flow engineering law — not educational content, not application code  

---

## 1. Purpose

Engineer the educational rhythm of a premium Kwalitec Study Session so the student feels guided by an excellent tutor — not interrupted by software prompts.

This document specifies **when** Kwalitec speaks, **when** the student studies the CMP, **when** Kwalitec returns, **when** the student reflects, and **when** tomorrow is introduced.

> **Avoid continuous interruption.**  
> Guidance is dense at the edges of reading and sparse in the middle.

---

## 2. Master rhythm (non-negotiable)

```text
Kwalitec guides
        ↓
Student studies the CMP   ← uninterrupted by default
        ↓
Kwalitec returns
        ↓
Student reflects
        ↓
Tomorrow is introduced
        ↓
Session completes
```

### Rhythm laws

| ID | Law |
|----|-----|
| RF-01 | **Guide before open.** Orientation + Reading Preparation happen *before* CMP deep work. |
| RF-02 | **Exit into reading.** After Reading Guidance is set, Kwalitec yields the floor. |
| RF-03 | **Sparse pauses only.** Reading Pause Points are pre-authored, few, and purposeful — never a continuous chat. |
| RF-04 | **Return for cognition.** After stop condition, Knowledge Checks demand retrieval/performance. |
| RF-05 | **Reflect after evidence.** Reflection follows Knowledge Checks — not instead of them. |
| RF-06 | **Tomorrow after close.** Tomorrow Preparation follows Wrap-up / Confidence — no heavy new teaching. |
| RF-07 | **One orientation.** Mission facts are not restacked verbatim at every stage. |
| RF-08 | **Honest refuse.** If topic or CMP locus cannot bind, do not open a fake Session. |

---

## 3. Full stage flow

```text
Home / Mission
    → Session Entry
        → Mission Orientation
            → Reading Preparation
                → CMP Reading Guidance ──exit──→ Uninterrupted CMP study
                        ↑                         │
                        └── Reading Pause Points ←┘  (0–N sparse)
                                    │
                                    ↓ stop condition
                         Kwalitec re-entry
                                    ↓
                         Knowledge Checks
                                    ↓
                         Reflection
                                    ↓
                         Confidence Assessment
                                    ↓
                         Session Wrap-up
                                    ↓
                         Tomorrow Preparation
                                    ↓
                         Session Completion
```

---

## 4. Stage-by-stage flow specification

### 4.1 Session Entry

| Aspect | Specification |
|--------|---------------|
| **Trigger** | Student opens Session from Mission / Home Begin path |
| **Kwalitec does** | Resolve topic identity, parent Mission binding, duration authority, stage plan integrity |
| **Student does** | Arrives ready to begin — or receives honest recovery |
| **CMP** | Not yet open as the study block |
| **Exit when** | Lawful bind succeeds → Orientation. Fail → unavailable / recovery (never placeholders) |
| **Must never** | Open with “Today’s topic”; Begin enabled on failed resolution (TB-001) |

**Feel:** Door opens only when the room is real.

---

### 4.2 Mission Orientation

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Answer: *Am I ready to begin?* + *What is today’s block?* |
| **Kwalitec does** | Present topic, objective, concept focus, why-now (short), structure of stages, duration, Begin CTA |
| **Tutor move** | Orient once — progressive disclosure from Home, not a duplicate wall |
| **Student does** | Confirm understanding; Begin |
| **CMP** | Locus may be named; deep reading not yet required |
| **Exit when** | Student begins → Reading Preparation (may be combined UI with Overview) |
| **Must never** | Full CMP dump; platform essays; multiple competing CTAs; restack entire Mission narrative (SB-09) |

**Feel:** A calm tutor briefing before the books open.

**Relationship to Session Philosophy §10:** Orientation implements Overview educational job. UI may merge Entry + Orientation + Preparation; educational sequence remains.

---

### 4.3 Reading Preparation

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Create selective attention before the CMP opens |
| **Kwalitec does** | Focus questions (2–4); material locus; stop condition; misconception watch-list (from Mission); duration honesty; annotation task preview |
| **Tutor move** | “Here is what you are hunting for.” |
| **Student does** | Internalise questions; note stop condition |
| **CMP** | Still closed or skim-open only — deep study waits for exit cue |
| **Exit when** | Guidance complete → CMP Reading Guidance / Exit into reading |
| **Must never** | Begin deep reading without focus; dump chapter; enable empty reading shell (TB-007) |

**Feel:** “I know what I’m hunting for before I open the notes.” (`EA001_SESSION_PHILOSOPHY.md` §5)

---

### 4.4 CMP Reading Guidance → Exit into reading

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Direct engagement; then **yield** |
| **Kwalitec does** | Present reading objectives; highlight misconceptions to watch; attention directives; explicit **exit** (“Open CMP at …; return after …”) |
| **Tutor move** | Set the hunt; leave the candidate with the book |
| **Student does** | Opens CMP; studies under the stop condition |
| **CMP** | Authoritative content owns the middle of the Session |
| **Exit when** | Student begins uninterrupted study (RF-02) |
| **Must never** | Continuous prompts during reading; paste CMP; abandon without return path |

**Detail:** `EA004_READING_GUIDANCE_ARCHITECTURE.md`.

**Feel:** The tutor steps back so real study can happen.

---

### 4.5 Reading Pause Points (optional sparse)

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Accountability without continuous interruption |
| **Budget** | Prefer **0–2** pauses for a typical 45–60 minute Session; absolute soft max **3** unless Board HOLD for lab-style Sessions |
| **Kwalitec does** | At each pause: one short check or note cue tied to a focus question; then **re-exit** to CMP |
| **Student does** | Brief response / annotation; resumes reading |
| **CMP** | Remains primary; pause is a glance back at the tutor |
| **Exit when** | Pause complete → resume uninterrupted reading until next pause or stop |
| **Must never** | Pause after every paragraph; chatty reminders; re-state Mission; duplicate CMP text |

**Interruption test:** If removing a pause would not harm learning, remove it.

**Feel:** Occasional “check you’re still hunting” — not a nagging app.

---

### 4.6 Knowledge Checks (Kwalitec returns)

| Aspect | Specification |
|--------|---------------|
| **Trigger** | Stop condition met (or student returns on cue) |
| **Educational job** | Convert exposure into retrieval and performance (EP-05, EP-03) |
| **Kwalitec does** | Re-enter with Active Recall / Worked Example (guided) / Practice / Checkpoint; immediate feedback where objective; lawful stage advance |
| **Tutor move** | “Close the book. Show me.” |
| **Student does** | Explain / solve / identify / justify without full notes |
| **CMP** | Closed or set aside for recall; optional reference *after* attempt |
| **Exit when** | Required cognitive demands complete with feedback → Reflection |
| **Must never** | “Answer recorded” with no feedback and no Continue (TB-008); declare mastery; skip checks and jump to Reflection as sole activity |

**Feel:** “I know whether today’s idea survived contact with my memory.”

**Composition:** May be one or more Learning Episodes (Gate LE). At least one active cognitive demand is mandatory (SS-03).

---

### 4.7 Reflection

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Metacognitive close; residual-uncertainty harvest (EP-07) |
| **Kwalitec does** | Topic-specific prompts implementing Mission Reflection Goal: clearer · uncertain · carry forward |
| **Tutor move** | “Name the gap while it’s fresh.” |
| **Student does** | Student-authored text or structured student decisions |
| **CMP** | Not required |
| **Exit when** | Reflection captured → Confidence Assessment (or combined surface) |
| **Must never** | Generic placeholders; system-written reflection as student voice; skip while marking complete; platform jargon |

**Feel:** Continuity fuel, not a survey.

---

### 4.8 Confidence Assessment

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Soft metacognitive signal tied to today’s success criteria |
| **Kwalitec does** | Ask confidence relative to what was checked — with honest framing that confidence ≠ mastery |
| **Tutor move** | Calibrate without inflating |
| **Student does** | Self-rate; optionally note mismatch with check performance |
| **Exit when** | Captured → Wrap-up |
| **Must never** | Raise Estimated Mastery from confidence alone; “High confidence” theatre contradicting empty History (TB-011 pattern); replace Knowledge Checks |

**Feel:** Honest self-check — warrant-aware.

---

### 4.9 Session Wrap-up

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Close what was studied and evidenced — Study Progress language |
| **Kwalitec does** | Summarise topic + objective outcomes; what evidence was created; what remains open (from Reflection) |
| **Tutor move** | Truthful close |
| **Student does** | Sees a coherent end to today’s block |
| **Exit when** | Summary acknowledged → Tomorrow Preparation |
| **Must never** | Invent completion beyond warrant; mastery claims; unlock theatre; heavy new teaching |

**Feel:** “This sitting had a shape.”

---

### 4.10 Tomorrow Preparation

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Educational Continuity (EP-02) + Exam Focus (EP-08) |
| **Kwalitec does** | Tomorrow Preview: next topic + continuity line from today; optional light prep cue with named CMP locus |
| **Tutor move** | “Here’s how the story continues — you can stop.” |
| **Student does** | Receives handoff aligned with next Home Mission |
| **When unknown** | Honest empty state: heading · one sentence · one action — no fabricated topic |
| **Exit when** | Preview shown → Session Completion |
| **Must never** | Contaminant nodes; contradict Twin/plan; heavy teaching for tomorrow tonight |

**Feel:** Anxiety drops; continuity holds.

---

### 4.11 Session Completion

| Aspect | Specification |
|--------|---------------|
| **Educational job** | Lawful close; One Educational Truth |
| **Kwalitec does** | Mark Session complete per constitutional rules; update session history / journey inputs; feed Mission completion rules; emit revision signals as designed |
| **Student does** | Leaves; surfaces agree on what happened |
| **Must never** | Home still assigns identical Mission as “not done” while claiming complete (TB-005); mastery conflation; erase rightful history |

**Feel:** Done means done — without claiming “mastered forever.”

---

## 5. Who speaks when (interruption budget)

| Phase | Kwalitec speech density | Student cognitive centre |
|-------|-------------------------|--------------------------|
| Entry → Orientation → Preparation | **High** — briefing | Absorb plan |
| Exit into reading | **Closing instruction** — then silence | — |
| Uninterrupted CMP study | **None** (default) | CMP |
| Reading Pause Points | **Minimal** — one cue each | Brief response → CMP again |
| Knowledge Checks | **High** — demand + feedback | Retrieval / practice |
| Reflection → Confidence | **Moderate** — prompts only | Metacognition |
| Wrap-up → Tomorrow → Completion | **Moderate** — close + handoff | Receive continuity |

### Interruption budget rule

```text
Designed pauses during CMP reading ≤ interruption_budget (Blueprint)
If a stage would require continuous Kwalitec presence during reading → redesign or FAIL certification
```

**Reject class:** Excessive interruption — see `EA004_SESSION_CERTIFICATION.md`.

---

## 6. Progressive disclosure (anti-duplication)

| Surface | May include | Must not |
|---------|-------------|----------|
| Home / Mission | Full tutor brief | Session stage chat |
| Mission Orientation | Short orient + structure + Begin | Full CMP; restacked Home essay |
| Reading Preparation | Focus questions + locus + stop | Repeat entire why-now paragraph unless one clause bridge |
| During reading | Sparse pause cues only | Mission restatement; CMP paste |
| Knowledge Checks | Success-criteria-linked items | Re-teach the Orientation |
| Reflection | Residual harvest | Generic “Today’s topic” prompts |
| Wrap-up / Tomorrow | Outcome + next bridge | New Mission authoring |

**Duplicate Mission information test:** If Orientation, Preparation, and Wrap-up each contain the same multi-sentence why-now verbatim, fail RF-07 / reject class “Repeats Mission information.”

---

## 7. Timing model (honesty)

| Segment | Typical share of Session budget | Notes |
|---------|--------------------------------:|-------|
| Entry + Orientation + Preparation | 10–15% | Dense guidance |
| CMP reading (+ sparse pauses) | 45–60% | Student owns the middle |
| Knowledge Checks | 15–25% | Mandatory cognitive demand |
| Reflection + Confidence | 5–10% | Required close |
| Wrap-up + Tomorrow + Completion | 5–10% | Continuity; no new teaching |

Claims must match Episode depth (SS-06). Home duration and Session duration must share one authority (TB-009).

---

## 8. Failure modes mapped to EV-001

| Flow defect | Trust break / principle |
|-------------|-------------------------|
| Placeholder topic at Entry/Orientation | TB-001 |
| Empty reading / no locus | TB-007 · EP-04 |
| Stuck after answer | TB-008 |
| Duration contradiction | TB-009 |
| Tomorrow contaminant / fabricated | TB-003 · TB-010 |
| Completion truth split | TB-005 · EP-10 |
| Continuous interruption / chatbot reading | EP-04 · RF-03 |
| Reflection-only “activity” with no recall | EP-05 · SS-03 |
| Platform meta hero | EP-09 · TB-012 |

---

## 9. Composer note for authors

Design the Session as a **tutor hour**, not a screen tour:

1. Brief like a professional.  
2. Send the candidate into the CMP with a hunt.  
3. Stay quiet while they work.  
4. Call them back for proof.  
5. Harvest the gap.  
6. Point to tomorrow.  
7. Let them stop.

If the flow feels like software constantly checking in, it is not yet a Kwalitec Session.

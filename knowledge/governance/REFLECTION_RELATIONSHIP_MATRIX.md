# Reflection Relationship Matrix

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.3 — Reflection Architecture  
**Status:** Active — Board educational law  
**Effective:** 2026-07-28  
**Companions:** `REFLECTION_ARCHITECTURE.md`, `REFLECTION_LIFECYCLE.md`  
**Constraint:** Governance only.

---

## 1. Purpose

Document **dependencies**, **information flow**, **educational flow**, and **storage flow** among:

- Mission  
- Session  
- Reflection (family)  
- Decision Journal  
- Educational Timeline  
- Educational Feedback Loop  
- Calibration  
- Recommendations  

Clarify how reflection sits inside the wider educational system without becoming a second product OS.

---

## 2. Entity roles (one line each)

| Entity | Role relative to reflection |
|--------|----------------------------|
| **Mission** | Today’s authorised educational focus that creates the experience worth reflecting on |
| **Session** | Practice workflow that produces experience; hosts Session reflection |
| **Reflection (family)** | Converts experience into judgement practice across roles (Session / Commitment / Sensei / Timeline / Preview) |
| **Decision Journal** | Sole durable educational memory for memory-grade reflection and decision continuity |
| **Educational Timeline** | Narrative interpretation of Journal; hosts Timeline reflection prompts |
| **Educational Feedback Loop** | Capability that uses outcomes + Sensei reflection to review guidance usefulness (no re-rank) |
| **Calibration** | Declared coverage cold start — **not** reflection; seeds Twin honesty |
| **Recommendations** | Authorised next-action objects; may be *judged* by Sensei reflection; never *scored* by reflection into new ranks |

---

## 3. Dependency matrix

Legend: **R** = requires · **F** = feeds · **P** = projects/reads · **X** = must not depend · **—** = no direct dependency

| From ↓ / To → | Mission | Session | Reflection | Journal | Timeline | Feedback Loop | Calibration | Recommendations |
|---------------|---------|---------|------------|---------|----------|---------------|-------------|-----------------|
| **Mission** | — | R (practice) | F (experience) | F (present/accept/…) | — | — | — | R (composes from) |
| **Session** | R (often via commitment) | — | F (Session reflection) | —* | — | — | X | May show next |
| **Reflection** | Educational object of judgement | Practice close | — | Sensei → R store | Timeline prompts P Journal | Sensei → R | X as reflection | Judges usefulness; X re-rank |
| **Journal** | Stores Mission arcs | Indirect via commitment | Hosts Sensei reflection | — | F (source) | F (inputs) | X | Stores snapshots; X re-rank |
| **Timeline** | Narrates Mission milestones | — | Hosts Timeline reflection | R (read) | — | May highlight reflected | X | X |
| **Feedback Loop** | Reviews Mission guidance | — | Consumes Sensei reflection | R | P (indirect) | — | X | Reviews; X re-rank |
| **Calibration** | — | — | X (not reflection) | X | X | X | — | Soft cold-start only when Twin lawful |
| **Recommendations** | Become Mission briefs | Drive Session focus | Subject of Sensei reflection | F (recorded) | Narrated | Reviewed | May use declared priors | — |

\*Session notes do not auto-write Journal (architecture residual). Commitment completion mirrors Journal separately.

---

## 4. Information flow

```
Recommendations ──compose──► Mission (Daily Mission Intelligence)
        │                         │
        │                         ▼
        │                   Commitment (accept / defer)
        │                         │
        │                         ▼
        │                      Session practice ──► practice evidence
        │                         │
        │                         ├──► Session reflection ──► session document store
        │                         │
        │                         └──► mark_completed ──► Commitment reflection
        │                                        │
        └──────── snapshots / mirrors ───────────┴──► Decision Journal
                                                         │
                         Sensei reflection (optional) ◄──┤
                                                         │
                                                         ├──► Educational Feedback Loop (internal reviews)
                                                         │
                                                         └──► Educational Timeline (projection + questions)

Calibration ──► Twin birth priors          (isolated from reflection family)
Product Check-in ──► Research DB           (isolated — not on this diagram’s educational edges)
```

**Hard cuts (must remain):**

- Product Check-in ↛ Journal / Timeline / Twin / Recommendations  
- Sensei reflection ↛ Recommendation ranker  
- Calibration ↛ labelled as reflection  
- Timeline ↛ new educational writes  

---

## 5. Educational flow

Student-facing meaning of the same edges:

| Step | Educational meaning |
|------|---------------------|
| Recommendation → Mission | “Here is today’s focus, explained.” |
| Mission → Commitment | “I choose (or defer) deliberately.” |
| Commitment → Session | “I practise what I chose.” |
| Session → Session reflection | “I notice what practice taught.” |
| Session → Commitment reflection | “I close the commitment honestly.” |
| Arcs → Decision Journal | “The Sensei remembers our decisions.” |
| Journal → Sensei reflection | “I judge whether that guidance helped.” |
| Journal → Timeline | “I see how my learning story evolved.” |
| Timeline questions | “I practise long-term professional judgement.” |
| Memory → Future Mission | “Tomorrow’s focus respects evidence and continuity — not guilt or streaks.” |

This is the **single coherent professional learning narrative**. Parallel stacks that do not join these edges must not be taught as separate reflection products.

---

## 6. Storage flow

| Source event | Primary store | Secondary / derived | Forbidden sinks |
|--------------|---------------|---------------------|-----------------|
| Mission present/accept/defer/complete | Decision Journal | Timeline projection | Twin mastery claims from mere present |
| Commitment reflection ack | `recommendation_commitments` | Journal mirror | Ranking tables |
| Session optional note | Session `NS_REFLECTION` | (none default) | Journal unless Board-authorised mirror; Twin |
| Sensei reflection | Journal `reflection_note` + evidence | `educational_feedback_reviews` | Learner-visible “you scored X”; ranker |
| Timeline view | — | — | New Journal rows from questions alone |
| Product Check-in | Research tables | Founder analytics | Educational Evidence / Twin / Journal |
| Calibration submit | Twin birth pipeline | — | Reflection history surfaces |

---

## 7. Relationship cards (pairwise)

### 7.1 Mission ↔ Reflection

- Mission creates the experience.  
- Commitment reflection closes Mission commitment.  
- Sensei reflection judges Mission guidance usefulness after outcomes.  
- Mission must explain educational purpose; reflection must not replace Mission as daily focus noun.

### 7.2 Session ↔ Reflection

- Session hosts Session reflection as practice close.  
- Session finish enables Commitment reflection on Home.  
- Session notes ≠ Sensei reflection (different store and purpose).

### 7.3 Reflection ↔ Decision Journal

- Only **Sensei reflection** is Journal-native capture.  
- Commitment arcs mirror into Journal as decision memory (not free-text reflection essays).  
- Session notes are not Journal by default.  
- Journal is the gate to Timeline and Feedback Loop.

### 7.4 Decision Journal ↔ Educational Timeline

- Timeline is a **read-only projection** of Journal.  
- Timeline reflection questions do not mutate Journal.  
- History (PX) must not compete as a second mentor memory (ED-05).

### 7.5 Reflection ↔ Educational Feedback Loop

- Feedback Loop is the **capability**; Sensei reflection is the **student interaction**.  
- Internal reviews are Sensei-side learning about guidance quality.  
- Students should not need the phrase “Feedback Loop” to participate.

### 7.6 Reflection ↔ Calibration

- Calibration is upstream cold-start declaration.  
- It is not post-practice reflection and must not share the student reflection map.  
- Declared coverage ≠ mastery; Sensei reflection ≠ Calibration.

### 7.7 Reflection ↔ Recommendations

- Recommendations are objects of reflection (usefulness, timing, understanding why).  
- Reflection evidence may inform **internal** Sensei review honesty.  
- Reflection must **never** become a hidden ranking feature or engagement score.

---

## 8. Contribution matrix (quick reference)

| Capability | → Journal | → Timeline | → Sensei memory | → Recommendations | → Twin |
|------------|-----------|------------|-----------------|-------------------|--------|
| Session reflection | No (default) | No (default) | Session-local only | No | No |
| Commitment reflection | Via mirror | Indirect | Continuity | No re-rank | No |
| Sensei reflection | Yes | Yes (projection) | Yes (+ internal review) | No re-rank | No |
| Timeline reflection | No | Self (prompts) | Narrative only | No | No |
| Guided preview | No | No | No | No | No |
| Product Check-in | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |
| Calibration | No | No | Declared history only | Soft priors only when lawful | Birth priors |

---

## 9. Conflict / confusion edges (governance)

| Edge | Risk | Board stance |
|------|------|--------------|
| Session note vs Sensei reflection | Students think both “save to Sensei” | Teach map; different stores |
| Commitment reflection vs Guided preview | Fake agency on Home | Preview honesty (RR-001.1); distinct names |
| Sensei reflection vs Product Check-in | False cousin (ED-18) | DEP-15; research labelling |
| Feedback Loop vs Learning Feedback emitters | Internal telemetry confusion | ILE-005 ≠ EP behavioural buffers |
| Timeline vs History | Dual memory stories (ED-05) | Timeline = Sensei narrative; History = archive context |
| Calibration vs reflection | Metacognition vs declaration | Separate map entirely |

---

## 10. Certification

An implementer can reconstruct from this matrix:

- what depends on what  
- how information, education, and storage flow  
- which edges are forbidden  
- how Mission, Session, Journal, Timeline, Feedback Loop, Calibration, and Recommendations relate to the reflection family  

Without inventing a second reflection system.

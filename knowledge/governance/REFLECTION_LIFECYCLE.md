# Reflection Lifecycle

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.3 — Reflection Architecture  
**Status:** Active — Board educational law  
**Effective:** 2026-07-28  
**Companion:** `REFLECTION_ARCHITECTURE.md`  
**Constraint:** Governance only.

---

## 1. Purpose

Map the **complete reflection lifecycle** for Kwalitec so that no reflection is orphaned: every prompt, capture, store, narrative use, and future recommendation link is defined.

**Invariant (DG-001.3-D04):** No orphan reflections are permitted. Every interaction is either:

1. a named stage in this lifecycle, or  
2. explicitly classified as non-recording / non-reflection / architecture residual.

---

## 2. Master lifecycle (canonical educational path)

```
Study Experience (Mission → Commitment → Session practice)
        ↓
Reflection Prompt (Session / Commitment / Sensei / Timeline — by role)
        ↓
Student Reflection (optional note, ack, optional Journal judgement, or silent prompt consideration)
        ↓
Decision Journal (durable educational memory — when the reflection is memory-grade)
        ↓
Educational Timeline (narrative interpretation + Timeline reflection questions)
        ↓
Study Sensei Learning Memory (continuity of guidance conversations; internal Feedback Loop reviews)
        ↓
Future Recommendation / Mission (evidence- and memory-informed — never reflection-scored)
```

**Educational chain (must remain visible in product design intent):**

```
Experience → Evidence → Reflection → Learning → Professional judgement → Long-term mastery
```

---

## 3. Stage definitions

| Stage | What happens | Who speaks | What may be stored |
|-------|--------------|------------|--------------------|
| **S0 — Study Experience** | Mission offered; student commits or defers; Session practice produces outcomes | Study Sensei (guidance); System (timestamps) | Commitment state; session runtime; practice evidence (lawful paths) |
| **S1 — Reflection Prompt** | Product invites notice, acknowledgement, usefulness judgement, or interpretive thought | Study Sensei | Prompt catalogue only (no student answer yet) |
| **S2 — Student Reflection** | Student responds, skips, or merely considers | Student agency; Sensei frames | Category-dependent (see §5) |
| **S3 — Decision Journal** | Significant guidance, choice, outcome, and Sensei reflection become memory | Study Sensei | Journal entries + evidence events |
| **S4 — Educational Timeline** | Journal projected into learning story; Timeline reflection questions posed | Study Sensei | None new — read-only projection |
| **S5 — Sensei Learning Memory** | Continuity for mentor relationship; optional internal Feedback Loop review | Study Sensei (internal review not learner-visible) | `educational_feedback_reviews` (internal) |
| **S6 — Future Recommendation** | Next Mission / authorised recommendation composed from educational authorities | Study Sensei narrates; deterministic cores decide | Recommendation / Mission artefacts — **not** reflection scores |

---

## 4. Lifecycle by reflection category

### 4.1 Session reflection

```
Session activities complete
    → S1 Session reflection prompt / surface
    → S2 Optional note + continue
    → Session document store (NS_REFLECTION)
    → Session summary / complete
    → (parallel) Commitment mark_completed → Commitment reflection path
```

| Attribute | Law |
|-----------|-----|
| Enters Decision Journal? | **Not by default** (architecture residual: optional future mirror under Board rules) |
| Enters Timeline? | Only if later mirrored to Journal |
| Affects ranking? | Never |
| Skip / empty note? | Lawful |

### 4.2 Commitment reflection

```
Commitment state = completed (after Session finish wiring)
    → Home S1 five-beat composed reflection
    → S2 Acknowledge (“Got it”)
    → state = reflected; reflected_at set
    → Journal mirror (via commitment adapter, fail-open)
    → S4/S5 via Journal when mirrored
```

| Attribute | Law |
|-----------|-----|
| Student free-text required? | No — composed beats |
| Scores learner? | Never |
| Next day guidance? | Continuity narrative only — not a reflection score input |

### 4.3 Sensei reflection (ILE-005)

```
Journal entry has outcome / can_reflect
    → S1 Optional reflection prompts on Decision Journal
    → S2 Answer some/all or skip
    → S3 reflection_note + evidence append on entry; lifecycle → reflected
    → Internal Feedback Loop review (S5, learner-invisible)
    → S4 Timeline may highlight reflection
    → S6 Future recommendations unchanged by ranking (no re-rank)
```

| Attribute | Law |
|-----------|-----|
| Optional? | Always |
| Prefer not to say? | Lawful |
| Re-ranks Mission? | Forbidden |

### 4.4 Timeline reflection

```
Student opens Educational Timeline
    → S4 narrative built from Journal
    → S1/S2 Timeline reflection questions (consideration prompts)
    → No POST store
    → Professional judgement practised in situ
```

| Attribute | Law |
|-----------|-----|
| Creates Journal rows? | Never |
| Orphan risk? | None if questions always cite narrative evidence |

### 4.5 Guided Reflection preview

```
Home render (preview-only)
    → S1 illustrative prompts
    → No S2 capture
    → Honesty: nothing saved
    → Does not enter S3–S6
```

| Attribute | Law |
|-----------|-----|
| Lifecycle status | Orientation spur — must not look like a decision |
| Orphan? | Avoided by explicit non-recording classification |

### 4.6 Quick Check reflection phase

```
Quick Check questions complete
    → Presentation reflection phase
    → Optional framing / text in presentation state
    → Return / complete
    → Not durable Journal memory (writer for QUICK_CHECK_RECOMMENDATION incomplete)
```

| Attribute | Law |
|-----------|-----|
| Lifecycle status | Assessment-close spur |
| Future | Journal mirror of Quick Check recommendations may join S3 under existing entry kinds |

---

## 5. Storage lifecycle matrix

| Capture | Durable store | Expiry / archive | Retrieval surface |
|---------|---------------|------------------|-------------------|
| Sensei reflection answers | Decision Journal entry + evidence | Append-only educational memory; archive states per Journal lifecycle | Journal; Timeline projection |
| Internal Feedback Loop review | `educational_feedback_reviews` | Internal Sensei calibration store | Not student-visible |
| Commitment reflection ack | `recommendation_commitments` | Commitment history | Home / recent commitment chrome; Journal via mirror |
| Session optional note | Session document `NS_REFLECTION` | Session lifetime / durable store policy | Session summary; **not** primary History reflection archive |
| Timeline questions | None | N/A | Timeline page |
| Guided preview | None | N/A | Home only |
| Product Check-in | Research DB | Research retention | Research / founder — not educational Timeline |
| Calibration | Twin birth pipeline | Twin lifecycle | Calibration / Twin — not reflection history |

**Journal entry lifecycle (memory host):**  
`recommended → accepted/deferred → evidence_evolving → reflected → outcome_recorded → archived`  
(Sensei reflection participates at `reflected`; outcomes may precede or follow per capability rules.)

---

## 6. Information flow vs educational flow

| Flow type | Path |
|-----------|------|
| **Educational flow** | Experience → notice/judgement → learning → better future choices |
| **Information flow** | Practice evidence + commitment state → (optional) Journal → Timeline projection → Sensei continuity |
| **Storage flow** | Category store (§5) → never Product Check-in → Journal; never reflection score → recommendation ranker |
| **Surveillance anti-flow** | No silent harvesting of free-text reflection into Twin mastery or marketing |

---

## 7. Orphan prevention checklist

A reflection interaction is **lawful** only if all are true:

1. **Named** in `REFLECTION_ARCHITECTURE.md` taxonomy (or explicit non-reflection / residual).  
2. **Owned** by an approved owner (Sensei / Session / Commitment / ILE / Research / Calibration).  
3. **Staged** in this lifecycle (including orientation-only or non-reflection branches).  
4. **Stored** in a declared location — or declared non-storing.  
5. **Contributes** to the coherent narrative (master path §2) — or explicitly excluded as non-educational.  
6. **Does not** re-rank recommendations or score the learner.

### Current residuals (not orphans if classified; must not be taught as map members)

| Residual | Classification | Required future action |
|----------|----------------|------------------------|
| Session note without Journal mirror | Practice-close store; narrative gap | Decide Board-authorised mirror or honest Help: “stays with session” |
| Dual Session vs JourneyReflection stacks | Architecture residual | Consolidate under Session reflection law |
| Unified Journey non-persisting reflection | Flag-gated residual | Honesty + map update before Alpha claims |
| EOS / EpisodeReflection | Non-Alpha path residual | Keep out of student map or converge |
| Unwired Journal kinds (revision / recovery / Quick Check) | Catalogue kinds | Wire writers or retire from student narrative claims |
| RIP-001 “Daily Reflection” title | Naming collision | Copy remediation — Product Check-in only |

---

## 8. End-to-end scenarios

### Scenario A — Happy path (Alpha intent)

1. Sensei presents Mission (Journal: recommended).  
2. Student commits → Session practice.  
3. Session reflection: optional note in session store.  
4. Finish → Commitment reflection ack on Home.  
5. Journal: acceptance / completion mirrored.  
6. Optional Sensei reflection on Journal entry.  
7. Timeline narrates turning points; poses Timeline reflection questions.  
8. Tomorrow’s Mission uses authorised recommendation evidence — not reflection scores.

### Scenario B — Skip all optional reflection

1–2 as above.  
3. Skip Session note.  
4. Ack Commitment reflection (minimal close) or, if shown, still no free-text.  
5. Skip Sensei reflection.  
6. Timeline still available from Journal decision memory.  
**Lawful.** Student must not be punished or guilted.

### Scenario C — Product Check-in only

1. After study, student opens Product Check-in.  
2. Research store updates.  
3. **No** Journal / Timeline / Twin / ranking effect.  
**Lawful as research; unlawful if taught as educational reflection.**

### Scenario D — Timeline-only reflection

1. Student reviews Timeline weeks later.  
2. Considers reflection questions; no form submit.  
3. Professional judgement practised; no new store.  
**Lawful.**

---

## 9. Lifecycle ownership

| Stage | Primary owner |
|-------|---------------|
| S0 Study Experience | Mission Intelligence + Commitment + Session |
| S1–S2 Session | Session Experience |
| S1–S2 Commitment | Mission Commitment |
| S1–S3 Sensei reflection | ILE-005 + ILE-002 |
| S4 Timeline | ILE-003 |
| S5 Internal review | ILE-005 |
| S6 Future recommendation | Authorised recommendation cores + Study Sensei narration |

---

## 10. Certification

From this document alone, an implementer can reconstruct:

- the master educational path  
- per-category stage graphs  
- storage and retrieval rules  
- orphan-prevention gates  
- skip-optional and non-reflection branches  

**No orphan reflections** under Board classification — residuals are named for consolidation, not left undefined.

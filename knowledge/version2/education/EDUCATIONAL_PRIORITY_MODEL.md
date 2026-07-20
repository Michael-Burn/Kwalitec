# Educational Priority Model

**Document ID:** V2-ERM-005  
**Classification:** Educational Architecture — Reasoning Foundation  
**Status:** Authoritative prioritisation framework  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md)  
**Companions:** [`TEACHING_INTENTION_MODEL.md`](TEACHING_INTENTION_MODEL.md) · [`EDUCATIONAL_REASONING_LOOP.md`](EDUCATIONAL_REASONING_LOOP.md) · [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md) · [`LEARNING_EPISODE_SEQUENCE.md`](LEARNING_EPISODE_SEQUENCE.md)

---

## 1. Purpose

Students rarely present a single educational problem. Actuarial and related professional preparation typically reveals **clusters** of deficiencies: a misconception here, a prerequisite gap there, weak retention on last term’s topic, false confidence near an exam window.

This document defines how a tutor should **prioritise** when multiple educational problems exist.

It answers:

1. Which principles govern educational priority?  
2. What explicit framework orders competing diagnoses?  
3. How do exam pressure and long-term learning interact without collapsing into mark theatre?  
4. What may never outrank educational truth?

This is educational architecture. It is not a scoring formula, ranking algorithm, or recommendation engine specification.

---

## 2. Definition

**Educational Priority:** the reasoned selection of which diagnosed educational problem — and therefore which Teaching Intention — should govern the next Learning Episode when more than one lawful need is present.

Priority is a reasoning act between Diagnosis and Intention. It does not invent needs; it orders them.

---

## 3. Governing Principles

These principles are binding for Version 2 educational governance.

### P1 — Repair prerequisites before extension

When a prerequisite gap blocks honest progress on a dependent objective, strengthen the prerequisite before extending into the dependent material.

**Rationale:** Advanced struggle that is really upstream absence produces theatre, demoralisation, and false diagnosis of the advanced topic.

### P2 — Repair misconceptions before practice

When evidence supports a stable wrong model, address the misconception explicitly before assigning undifferentiated practice on the same objective.

**Rationale:** Practice on a wrong model strengthens the wrong model.

### P3 — Address dangerous false confidence

When self-appraisal materially exceeds warrant — especially near examinations — prioritise calibration and discriminating challenge over comfort or further coverage celebration.

**Rationale:** False confidence is an integrity and outcomes hazard; it misallocates scarce late-calendar time.

### P4 — Prefer foundational understanding over speed

When conceptual misunderstanding or incomplete understanding competes with fluency/speed aims on the same objective, prefer understanding first.

**Rationale:** Speed without foundation is brittle under exam rewording and professional variation.

### P5 — Protect long-term learning over short-term progress theatre

When a move would improve immediate completion, streaks, or same-day scores while worsening durable understanding, retention, or transfer, prefer the durable good.

**Rationale:** Kwalitec’s promise is learning, not activity optics.

### P6 — Support exam readiness without sacrificing conceptual understanding

Exam-technique and timed practice are lawful and sometimes urgent, but they must not erase needed misconception repair, prerequisite work, or conceptual consolidation.

**Rationale:** Marks gained by technique on empty understanding are fragile and educationally dishonest as a sole strategy.

### P7 — Prefer discriminating teaching when hypotheses compete

When competing hypotheses underdetermine the next move, prefer an intention that tests the fork before committing long sequences to one reading.

**Rationale:** Wrong long commitments waste calendar and entrench error.

### P8 — Do not let engagement metrics set educational order

Streaks, points, and novelty must not reorder diagnoses against P1–P6.

**Rationale:** Engagement may support habit; it is not an educational dimension.

---

## 4. Explicit Prioritisation Framework

When multiple material diagnoses are present, apply the following **ordered gates**. Stop at the first gate that yields a clear primary problem for the next episode. If a gate yields several still-competing items, use the tie-breakers in §5.

```text
Gate 0  Safety of educational honesty
Gate 1  Blocking prerequisites
Gate 2  Active misconceptions (same objective family)
Gate 3  Dangerous false confidence
Gate 4  Foundational understanding deficits
Gate 5  Application / procedural deficits (concept adequate)
Gate 6  Retention threats (especially with delay or exam horizon)
Gate 7  Transfer and fragmentation (local competence present)
Gate 8  Exam technique and timed deployment
Gate 9  Confidence recovery (evidence-supported under-appraisal)
Gate 10 Extension, enrichment, and challenge
```

### Gate 0 — Safety of educational honesty

Prefer any move required to stop an actively harmful false claim path (for example product language about to imply mastery from completion) over cosmetic progress. This gate is rarely the content diagnosis itself; it protects integrity of the loop.

### Gate 1 — Blocking prerequisites

If a prerequisite gap prevents lawful work on the student’s current dependent aim, that gap is primary.

### Gate 2 — Active misconceptions

If a misconception is evidenced on the objective (or tightly coupled neighbour) the student is currently accountable for, repair it before fluency, volume practice, or extension.

### Gate 3 — Dangerous false confidence

If false confidence is likely to cause harmful study allocation or exam disaster, calibrate before adding coverage or celebrating readiness.

### Gate 4 — Foundational understanding deficits

Conceptual misunderstanding and incomplete understanding on the active objective outrank speed, exam tricks, and optional enrichment.

### Gate 5 — Application / procedural deficits

When concept is adequate, strengthen application and procedural fluency before transfer theatre or exam simulation that assumes fluent deployment.

### Gate 6 — Retention threats

Weak retention on high-value, previously acquired objectives rises in priority as delay grows or exam horizon approaches — still after Gates 1–3 when those block honesty.

### Gate 7 — Transfer and fragmentation

When local competence exists, improve transfer and reconnect fragmented knowledge before further identical drills.

### Gate 8 — Exam technique

When capacity is largely present, prioritise exam-condition deployment. Never use this gate to skip Gates 1–4.

### Gate 9 — Confidence recovery

Low confidence that contradicts adequate evidence may be primary when it blocks engagement — but not when used to avoid harder needed repairs.

### Gate 10 — Extension and challenge

Advance to new objectives, deeper challenge, or enrichment only when higher gates do not demand repair.

---

## 5. Tie-Breakers

When a single gate still leaves multiple candidates:

1. **Curriculum criticality** — prefer objectives that unlock more of the syllabus graph or appear with high exam weight *without inventing a private syllabus*.  
2. **Evidence strength** — prefer the better-warranted diagnosis over a speculative one.  
3. **Remediability in one atomic episode** — prefer a need that can be honestly advanced now over a vague multi-week fog.  
4. **Hypothesis discriminability** — prefer the intention that most reduces uncertainty among competing readings.  
5. **Student reflection of stuckness** — soft signal; use to break ties, not to override Gates 1–3.  
6. **Recency of failure on an active aim** — prefer unresolved active struggle over distant mild weakness *unless* retention Gate 6 is clearly dominant for exam survival.  
7. **Stability of harm** — prefer problems that worsen with continued wrong practice (misconceptions) over static mild gaps.

Tie-breakers never authorise scoring formulae as educational law. They are qualitative governance aids.

---

## 6. Worked Prioritisation Examples

### Example A — GLM cluster

Diagnoses present:

- Prerequisite gap (exponential families)  
- Application weakness on GLM fitting  
- Low confidence  

**Primary:** Strengthen prerequisite (Gate 1).  
**Deferred:** Application and confidence work after upstream capacity exists.

### Example B — Reserves near exam

Diagnoses present:

- Misconception (prospective vs retrospective)  
- Exam technique weakness  
- Weak retention on life table look-ups  

**Primary:** Repair misconception (Gate 2).  
**Next:** Retention on look-ups (Gate 6) and/or exam technique (Gate 8) once the wrong model is addressed.  
**Forbidden:** Timed papers that practise the misconception into permanence.

### Example C — False confidence after chapter completion

Diagnoses present:

- False confidence  
- Transfer weakness  
- Desire to “move on” to next chapter  

**Primary:** Calibrate false confidence / improve transfer with discriminating variants (Gates 3 and 7).  
**Deferred:** Extension (Gate 10).

### Example D — Fragmentation with solid locals

Diagnoses present:

- Knowledge fragmentation across annuity chapters  
- Mild procedural slowness  
- Strong conceptual explanations locally  

**Primary:** Connect fragmented knowledge / improve transfer (Gate 7).  
**Secondary:** Procedural fluency (Gate 5) if still needed after connection work.

---

## 7. Exam Horizon Policy

As examinations approach, Gates 6–8 rise in practical urgency **relative to Gate 10**, but they do **not** abolish Gates 1–4.

Lawful near-exam posture:

- Prefer retention and transfer on high-weight objectives already substantially learned.  
- Prefer exam technique when capacity is present.  
- Still repair blocking misconceptions and prerequisites that would make exam practice fraudulent.  
- Refuse coverage theatre that creates new false confidence.

Unlawful near-exam posture:

- “No time for concepts — only mocks,” while patterned misconceptions remain.  
- Dropping Twin honesty to preserve calm.  
- Reordering everything around engagement streaks.

---

## 8. Outputs of Prioritisation

A complete prioritisation act yields:

1. **Primary diagnosis** for the next episode.  
2. **Primary Teaching Intention**.  
3. **Deferred diagnoses** list (acknowledged, not erased).  
4. **Justification** in educational language (for governance and, when appropriate, student explanation).  
5. **Revisit condition** — what evidence would promote a deferred item.

Priority does not delete secondary problems from educational memory.

---

## 9. Summary Propositions

1. Priority orders diagnosed problems; it does not invent them.  
2. Prerequisites and misconceptions outrank undifferentiated practice and extension.  
3. Dangerous false confidence is a high gate, especially near exams.  
4. Foundational understanding outranks speed.  
5. Long-term learning outranks short-term progress theatre.  
6. Exam readiness is supported without sacrificing conceptual honesty.  
7. The gated framework plus qualitative tie-breakers is the Version 2 prioritisation architecture.

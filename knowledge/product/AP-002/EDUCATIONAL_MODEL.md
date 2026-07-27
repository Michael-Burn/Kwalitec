# AP-002 — Educational Model

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Why assessments exist

In Kwalitec, assessment exists to **improve learning** by reducing uncertainty about what the learner understands.

Professional exam candidates already live under enough evaluative pressure. The platform must not recreate exam theatre inside daily study. Instead, assessment answers:

- What does the Twin still not know about this learner?
- Where is mastery unstable?
- Which misconception is active?
- What evidence would make the next mission better?

Every assessment must increase the platform’s understanding of the learner. If an interaction does not produce educational evidence usable by Reasoning, it is not an Assessment Engine concern.

---

## 2. Concept distinctions

| Concept | Purpose | Primary output | Emotional frame |
|---|---|---|---|
| **Assessment** | Collect evidence to reduce Twin uncertainty | Structured observations + learning feedback | Supportive inquiry |
| **Quiz** | Short structured set of questions on a bounded objective | Observations (often correctness + confidence) | Check understanding |
| **Practice** | Rehearse skill with low stakes; may or may not be assessed | Attempt outcomes; optional observations | Skill building |
| **Mission** | Today’s actionable learning plan | Scheduled activities (may include assessment steps) | Directed progress |
| **Revision** | Revisit previously studied material for durability | Revision observations; spaced-evidence | Consolidation |
| **Exam** | High-stakes credential evaluation (external or simulated) | Marks / pass-fail (outside Engine philosophy) | Evaluation — **out of core Engine intent** |

### Assessment vs Quiz

A **quiz** is a delivery form (a bundle of questions). An **assessment** is an educational intent (why we are collecting evidence). A quiz may implement an assessment; not every quiz is educationally justified as assessment.

### Assessment vs Practice

**Practice** prioritises skill rehearsal. Practice outcomes may feed the Assessment Pipeline (as AP-001 / LXP-003 already allow). The Assessment Engine owns intentional evidence designs — diagnostic, checkpoint, mastery verification — not every practice click.

### Assessment vs Mission

A **mission** answers *what to do today*. Assessment is one activity type a mission may schedule. Missions consume Twin decisions; they do not invent assessment grades.

### Assessment vs Revision

**Revision** targets durability and recovery of known material. Assessment during revision verifies stability; it does not redefine revision as testing.

### Assessment vs Exam

**Exams** judge readiness for a credential. The Assessment Engine explicitly rejects exam anxiety patterns as the default student experience. Future exam-simulation products (if any) are a separate programme and must not collapse into Twin mastery theatre.

---

## 3. How assessment supports mastery

Mastery in Kwalitec is a **Twin inference**, produced only by Educational Reasoning from lawful evidence — never by Assessment alone.

Assessment supports mastery by:

1. **Producing denser evidence** than completion or elapsed time alone (EIP-002 Evidence Integrity).
2. **Surfacing misconceptions** that soft signals cannot reveal.
3. **Measuring knowledge stability** across time (retries, consistency, spaced re-checks).
4. **Calibrating confidence** when self-report and performance diverge.
5. **Informing mission priorities** after Reasoning updates gaps and recommendations.

### Lawful succession

```
Assessment response
        ↓
Observation (fact)
        ↓
Educational Reasoning (inference)
        ↓
Estimated Knowledge / Mastery / Gaps (Twin)
        ↓
Mission / Tutor (action & explanation)
```

Unlawful succession (forbidden):

```
Correct answer / high confidence / finished quiz
        ↓
Direct mastery upgrade (bypass Reasoning)
```

Completion, confidence, and elapsed time remain soft or incomplete signals. High Estimated Mastery language still requires lawful Educational Evidence of sufficient quality and accumulation.

---

## 4. Assessment intents

| Intent | Educational question | Typical trigger |
|---|---|---|
| Diagnostic | What does the learner not yet understand? | Cold start, new topic, thin Twin |
| Formative checkpoint | Is learning progressing on the current objective? | Mid-mission / after study block |
| Adaptive probe | Which of several uncertain nodes should we clarify? | Reasoning flags unstable mastery |
| Recovery check | Did recovery work close the gap? | After recovery mission steps |
| Mastery verification | Is evidence strong enough to support higher mastery confidence? | Twin requests verification |
| Revision stability | Does knowledge hold after spacing? | Spaced revision missions |
| Reflection | How does the learner interpret their own understanding? | Soft signal / metacognition |

All intents produce observations. None produce “marks”.

---

## 5. Educational guarantees

1. Assessment never replaces Learning Mode syllabus sequencing as mission authority.
2. Assessment never becomes a second Twin.
3. Assessment never grades the student in language of pass/fail for daily learning.
4. Assessment always prefers explainable next action over score theatre.
5. Assessment always leaves an auditable observation trail.

---

## 6. Alignment with product philosophy

| Principle | Assessment Engine stance |
|---|---|
| Reduce decisions. Increase learning. | Assessment clarifies what to study next via Twin, not via another dashboard score. |
| Curriculum first | Questions map to learning objectives and curriculum entities via Retrieval. |
| Deterministic cores | Observation schemas and feedback templates are reproducible. |
| Explainability | Outcomes cite evidence; Tutor may narrate, not invent. |
| Evidence before inference | No fabricated mastery to fill cold start. |

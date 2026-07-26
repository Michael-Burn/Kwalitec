# Blind Review Scoring Guide

**Authority:** Permanent definitions for every scoring dimension used in the SV-001–SV-020 programme  
**Scale:** Integer **1–10** unless a persona YAML explicitly states otherwise  
**Rule:** Score only the dimensions listed in the active persona’s `scoring` list. Do not add dimensions from other reviewers.

---

## How to score

| Score band | Meaning |
|---|---|
| 1–2 | Fails the dimension for this persona; would actively avoid relying on it |
| 3–4 | Weak; occasional signal, mostly noise or friction |
| 5–6 | Mixed / conditional; useful only under constraints the student must invent |
| 7–8 | Solid for this persona’s hypothesis; clear positive with bounded caveats |
| 9–10 | Strongly earns trust or behaviour change on this dimension |

Notes in the scoring table must cite **observed** product behaviour, not aspirations.

**Overall** is not an average. It is the persona’s single judgement against their `central_question`.

---

## Core / shared dimensions

### Overall
Holistic answer to the persona’s central question after the session(s). Not a mean of other rows.

### First Impression
Immediate sense of whether the product understands the student’s problem (often at sign-in / first dashboard). Not visual taste.

### Clarity
Whether the student understands what the product wants them to do next without decoding competing surfaces.

### Ease of Starting / Ease of Learning
How quickly a student can begin productive study (or learn the loop) without product problem-solving.

### Navigation
Whether moving between Dashboard, Home, Session, Journey, Coach, Settings, etc. supports study rather than creating a second map to memorise.

### Return Likelihood / Daily Use Potential / Daily Utility / Daily Usefulness / Daily Value / Daily Practical Value
Likelihood the student would open the product again on a normal study day. Emphasise weekday reality, not ideal Sunday conditions.

### Recommendation Likelihood
Whether the student would tell a peer in a similar situation to try / install / adopt Kwalitec.

### Commitment / Long-Term Adoption / Long-term Value / Long-term Usefulness / Long-term Educational Value / Long-Term Educational Value / Long-Term Learning Value / Long-Term Decision Quality / Long-Term Dependence
Willingness to keep the product in the preparation system over weeks/months. Distinguish organisation dependence from learning dependence when the persona asks.

### Educational Value / Educational Effectiveness / Educational Depth / Educational Insight / Educational Clarity / Educational Confidence
Whether the product improves learning-related outcomes for this persona (understanding, preparation quality, exam-relevant capability) — not mere activity completion.

### Educational Trust / Trust / Trustworthiness / Trust in Recommendations / Trust Through Understanding / Long-term Trust
Whether claims, recommendations, and progress language feel earned by evidence the student can inspect. Contradictions (dual durations, evidence language with empty history) lower this sharply.

### Confidence / Confidence Building / Confidence Accuracy
Effect on the student’s belief about their preparation. High scores require justified confidence; false reassurance should lower **Confidence Accuracy** and **Educational Safety** even if mood improves.

### Motivation / Encouragement / Willingness to Restart / Ease of Restarting / Would Help Me Stay Consistent / Routine Sustainability / Habit Formation
Support for starting, returning after gaps, and forming a durable loop — without shame mechanics or empty pep talk.

---

## Time, urgency, and cognitive load

### Time Efficiency / Time Value / Mental Effort Saved / Cognitive Load Reduction
Whether the product increases minutes spent studying versus minutes spent deciding, reconciling screens, or administering the tool.

### Urgency Support
Whether late-sitting / final-weeks students get triage and exam-proximate priorities rather than comfortable multi-month pacing theatre.

### Session Clarity / Organisational Support
Whether tonight’s session is obvious (topic, structure, finish path) and whether the product reduces syllabus/admin burden.

---

## Workflow and substitution

### Integration with Existing Workflow / Workflow Integration
Fit beside CMP, past papers, Anki, notes, trackers, calendar — without forcing a rip-and-replace.

### Replacement Value / Replaceability / Practical Benefit / Practical Usefulness / Practical Preparation
What (if anything) becomes obsolete; whether remaining value is worth the switching cost. High **Replaceability** means the student could lose the product with little pain (often a negative for dependence hypotheses).

---

## Trust, transparency, and explainability

### Transparency / Consistency / Predictability
Whether selection rules are inspectable, screens tell one story, and the student can forecast tomorrow’s recommendation.

### Credibility of Recommendations / Intelligence of Recommendations / Recommendation Quality
Whether “next study” feels intelligent and evidence-based rather than generic syllabus pointer dressed as optimisation.

### Coach Usefulness / Coach Value
Whether Coach adds information beyond restating the mission. Restatement without working scores low.

### Evidence
Whether readiness / progress / coaching claims show inputs the student can verify.

### Psychological Safety / Emotional Safety / Educational Safety
Non-shaming tone after gaps or failure; protection from false confidence where relevant. Safety without usefulness still scores middling on Overall if the hypothesis demands more.

---

## Feedback, adaptation, calibration

### Quality of Feedback / Progress Clarity
Whether the student can tell what improved, what remains weak, and whether today’s work was a good study day in learning terms.

### Adaptation / Personalisation / Educational Intelligence
Whether poor performance or changing evidence visibly changes subsequent missions / coaching (not only a private ledger).

### Calibration
Whether confidence signals match likely ability — especially for resitters sensitive to overconfidence.

---

## Decision support and deliberate practice

### Decision Support / Prioritisation / Behaviour Change
Whether the product changes what the student studies (topic choice, sequencing) versus leaving all strategy to the student. Prefer evidence of actual behaviour change over claimed intelligence.

### Deliberate Practice / Reflection Support / Learning Quality
Whether sessions push intelligent practice (purpose, success criteria tied to understanding, mistake reflection) rather than organised busywork / completion theatre.

---

## Exam transfer and companion role

### Exam Relevance / Knowledge Transfer / Confidence in Exam Impact
Whether tonight’s work convincingly connects to answering exam questions / marks — not only to finishing a checklist.

### Recoverability / Clarity After Errors / Navigation Recovery
Whether ordinary mistakes (wrong nav, pause, close tab, thin overview path) are forgiving and return the student to the correct study state.

---

## Dimension → primary programme use

| Dimension family | Typical reviewers |
|---|---|
| Adoption / first use | SV-001, SV-020 |
| Workflow / time / cognitive load | SV-002, SV-016, SV-018 |
| Trust / explainability | SV-003, SV-005, SV-014 |
| Motivation / recovery | SV-004, SV-008 |
| Urgency | SV-006 |
| Habit | SV-007, SV-018 |
| Substitution | SV-009 |
| Error recovery | SV-010 |
| Educational feedback | SV-011 |
| Adaptation | SV-012 |
| Calibration | SV-013 |
| Decision support | SV-015 |
| Deliberate practice | SV-017 |
| Exam transfer | SV-019 |

Exact lists always come from the active persona YAML.

---

## Anti-patterns

- Scoring visual polish
- Scoring engineering elegance
- Averaging other reviewers’ scores
- Inflating Overall because one screen was nice while the central question failed
- Introducing dimensions not listed in the persona YAML

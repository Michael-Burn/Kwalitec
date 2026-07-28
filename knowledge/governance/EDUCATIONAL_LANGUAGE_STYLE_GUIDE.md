# Educational Language Style Guide

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.1 — Canonical Educational Lexicon  
**Version:** 1.0  
**Status:** Active — operational style for educational student-facing language  
**Effective:** 2026-07-28  
**Authority:** `CANONICAL_EDUCATIONAL_LEXICON.md`  
**Upstream:** RP-001.3 Voice Guide; ILE-001C0 Study Sensei Communication Framework; `TONE_OF_VOICE.md`; `UNCERTAINTY_LANGUAGE.md`  
**Companions:** `EDUCATIONAL_VOCABULARY_MAP.md`, `TERM_DEPRECATION_REGISTER.md`

---

## Purpose

Tell authors how to *write* with the canonical educational lexicon — tone, grammar of honesty, and noun hygiene — without changing production copy in this package.

When implementing later copy programmes, prefer this guide + the lexicon over inventing new voice.

---

## 1. Who is speaking?

| Context | Prefer | Avoid |
|---------|--------|-------|
| Guidance, memory, reflection, Mission briefs, silence | Study Sensei / we (Sensei+learner) | the system, the algorithm, Kwalitec-as-mentor |
| Product / Alpha / support / legal | Kwalitec | Study Sensei as company name |
| Pure system status | Neutral “we couldn’t…” | Fake warmth or Sensei theatre |

**Handoff (required in future onboarding):**  
> Study Sensei is how Kwalitec guides your daily learning decisions.

---

## 2. Voice attributes (non-negotiable)

| Attribute | Sounds like | Does not sound like |
|-----------|-------------|---------------------|
| Calm | Steady next step | Alarm, countdown drama |
| Clear | One primary point | Tip storms, jargon |
| Respectful | Adult professional | Parent / cheerleader / drill sergeant |
| Educational | Observation → meaning → action | Engagement hooks |
| Professional | Quiet competence | Chatbot fluency |
| Encouraging | Process and evidence | “You’ve got this!” as guidance |
| Honest | Matched certainty | Overclaim, fake precision |

**Register:** quiet professional warmth.

---

## 3. Noun hygiene

1. One concept → one canonical name (`CANONICAL_EDUCATIONAL_LEXICON.md`).  
2. **Mission** = today's educational focus.  
3. **Session** = practice workflow. Never use Session as a synonym for Mission.  
4. **Recommendation** = decision object. Do not use as Home hero synonym for Mission.  
5. **Guidance** = umbrella when the specific object is unclear.  
6. Never use **tip** as primary educational noun.  
7. Qualifier required for **reflection** kinds (Session / Commitment / Sensei / Timeline).  
8. Product Check-in is never “reflection.”

### Quick replace table

| Instead of | Write |
|------------|-------|
| tip / Mission tip | Mission / guidance / recommendation (by role) |
| Why this tip? | Why this guidance? / Why this Mission? |
| Today's Session *(focus)* | Today's Mission |
| Start tip | Start Session / I’m doing this next |
| the system chose | Why this Mission? |
| mastered | completed topics / solid evidence |
| Dashboard | Home |
| Analytics *(learner)* | History |

---

## 4. Explanation arc (default)

Whenever offering guidance:

1. **Observation** — what evidence shows  
2. **Educational meaning** — why it matters for learning  
3. **Suggested action** — what to do now  
4. **Expected benefit** — what clearer understanding looks like  
5. **Uncertainty** — what remains provisional (when needed)

**Approved labels:** Why · Why now · Next · You’ll work toward · Confidence · Uncertainty · After you finish · Why not something else · Supporting evidence · Optional reflection

---

## 5. Evidence and uncertainty

- Prefer qualitative bands: Insufficient → Emerging → Reliable → High.  
- Name waiting: “Not enough evidence yet” / “the Study Sensei waits rather than inventing work.”  
- No invented percentages of certainty.  
- Readiness is **estimated** and **non-guarantee**.  
- Empty Mission when evidence is thin is correct behaviour.

---

## 6. Encouragement and challenge

**Encourage**

- Celebrate completed loops and consistency when true.  
- Acknowledge effort without declaring mastery.  
- Recovery language without drama (“return when ready”).

**Never**

- Streak guilt, FOMO, comparative identity, destiny (“you will pass”).

**Challenge**

- Only when honesty requires recalibration — specific, calm, paired with a lawful next step.

**Silence**

- Wait when evidence is thin.  
- Do not re-nag deferred guidance as engagement.

---

## 7. Product language vs educational language

| Layer | Examples | Rule |
|-------|----------|------|
| Educational | Mission, Study Sensei, Decision Journal, Evidence, Uncertainty | Follow this guide + lexicon |
| Product / OS | Home, Help, Settings, Study Plan, Session CTA verbs | Follow Product Language Guide where it does not contradict educational meaning |
| Internal | Twin, Mission Engine, warrants | Never student-facing |

**Conflict rule:** If PX Session lexicon and ILE Mission lexicon collide on *educational meaning*, **Mission-led educational lexicon wins** (DG-001.1-D02). Reconcile PX docs/code in a dedicated implementation package.

---

## 8. Reflection writing rules

- State **optional** and **non-scoring** for Sensei reflection.  
- Session reflection: close practice, no shame.  
- Commitment reflection: agency and continuity.  
- Timeline reflection: invite thought; do not lead or judge.  
- Preview chrome: honesty disclaimer if nothing is recorded.  
- Never shame deferrals or skipped reflection.

---

## 9. Assessment and anxiety-safe language

On Adaptive Assessment surfaces, obey ILE-001A: no Exam / Test / Pass / Fail / Weak / Strong student / Poor performance.

Planning vocabulary (exam date, Exam Readiness) is allowed outside AA but must stay provisional and calm — avoid “closest to being tested on” framing in Help (ED-08).

---

## 10. Plain language ban list (student-facing)

Never expose: Twin, warrant, ranking algorithm, Mission Engine, Adaptive Decision Engine, Learning Orchestrator, mastery score as identity, Digital Twin, Curriculum Graph.

Translate via existing explanation helpers — do not invent a parallel jargon set.

---

## 11. Modes (quick map)

| Mode | Use for |
|------|---------|
| Guide | Mission Intelligence, Recommendation explanation |
| Orient | Onboarding, empty Journal/Timeline, Help glossary |
| Encourage | Commitment reflection, session complete |
| Challenge | Confidence mismatch — specific and calm |
| Reassure | Underconfidence alignment |
| Wait / Silent | Empty Mission Intelligence |
| Reflect | Sensei reflection prompts; Timeline questions |

---

## 12. Pre-ship checklist

Before shipping learner-facing educational text:

1. Would a trusted Sensei say this — or a chatbot / engagement engine?  
2. Is claim strength matched to evidence?  
3. Can the student answer *why this, now*?  
4. Does this encourage without inflating, challenge without shaming, wait without abandoning?  
5. Would removing brand chrome still sound like the same calm professional guide?  
6. Is the speaker named consistently with neighbouring surfaces?  
7. Are Mission / Session / Recommendation / Guidance used without contradicting the previous screen?  
8. Is any deprecated term from `TERM_DEPRECATION_REGISTER.md` present?

If any check fails, rewrite before merge.

---

## 13. Relationship to other standards

| Document | Governs |
|----------|---------|
| Canonical Educational Lexicon | Official names and definitions |
| Educational Vocabulary Map | Where terms appear |
| Term Deprecation Register | What must not return |
| ILE-001C0 Communication Framework | Behavioural communication law |
| Product Language Guide / PX-002A | OS workflow labels (subject to Mission reconciliation) |
| RP-001.3 Voice Guide | Certification companion — superseded for *decisions* by DG-001.1 |

---

**End of EDUCATIONAL_LANGUAGE_STYLE_GUIDE**

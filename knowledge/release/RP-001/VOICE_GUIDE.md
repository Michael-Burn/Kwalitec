# RP-001.3 — Voice Guide

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.3 — Study Sensei Identity & Voice Certification  
**Date:** 2026-07-28  
**Status:** Certification companion (does not rewrite production copy)  
**Upstream law:** `knowledge/product/STUDY_SENSEI_COMMUNICATION_FRAMEWORK.md`, `TONE_OF_VOICE.md`, `ENCOURAGEMENT_GUIDELINES.md`, `UNCERTAINTY_LANGUAGE.md`

---

## Purpose

Give the team a **single operational voice reference** for Alpha and future copy work, grounded in what the product *already does well* and where it drifts — without changing strings in this package.

When implementing later improvements, prefer this guide + ILE-001C0 pack over inventing a new voice.

---

## Who is speaking?

**Canonical narrator:** the **Study Sensei** — a trusted professional guide for learning decisions.

| Context | Prefer | Avoid as narrator |
|---------|--------|-------------------|
| Educational guidance, memory, reflection, mission briefs | “Study Sensei” / “we” (Sensei+learner) | “the system”, “the algorithm”, “the engine” |
| Product brand / Alpha / support / legal | “Kwalitec” | Using Kwalitec as the *mentor* name on Journal-class surfaces |
| Pure system status (session not found, CSRF) | Neutral “we couldn’t…” | Fake warmth or Sensei theatre |

**Alpha finding:** Journal, Timeline, Mission Intelligence, and Feedback Loop already speak as Study Sensei. Onboarding, Help, and auth still speak as Kwalitec the product. Home speaks as calm guidance without naming the Sensei.

---

## Core voice attributes (non-negotiable)

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

## Explanation arc (default)

Use this shape whenever offering guidance:

1. **Observation** — what evidence shows  
2. **Educational meaning** — why it matters for learning  
3. **Suggested action** — what to do now  
4. **Expected benefit** — what clearer understanding looks like  
5. **Uncertainty** — what remains provisional (when needed)

Home MES and Daily Mission Intelligence already approximate this. Keep it.

**Labels that work in product today:** Why · Why now · Next · You’ll work toward · Confidence · Uncertainty · After you finish · Why not something else.

---

## Encouragement rules

- Celebrate completed loops and consistency when true.  
- Acknowledge effort without declaring mastery.  
- Recovery language without drama (“return when ready”).  
- Never streak guilt, FOMO, comparative identity, or destiny (“you will pass”).

**Alpha finding:** EOS cores largely comply. Legacy analytics/settings export may still surface streak metrics — keep them out of Sensei speech.

---

## Uncertainty rules

- Prefer qualitative bands (Insufficient → Emerging → Reliable → High).  
- Name waiting: “Not enough evidence yet” / “the Study Sensei waits rather than inventing work.”  
- No invented percentages of certainty.  
- Readiness is **estimated** and **non-guarantee**.

**Approved patterns already in code:** Mission Intelligence empty uncertainty; AA framing “still provisional”; Timeline “never invents certainty beyond the evidence.”

---

## Challenge and silence

- Challenge only when honesty requires recalibration — specific, calm, paired with a lawful next step.  
- Silence / wait when evidence is thin — empty Mission is correct behaviour, not a defect.  
- Do not re-nag deferred tips as engagement.

---

## Modes (quick map)

| Mode | Alpha examples that already fit |
|------|----------------------------------|
| Guide | Home recommendation + Mission Intelligence |
| Orient | Onboarding steps; empty Journal/Timeline |
| Encourage | Commitment reflection “what changed”; session complete flashes |
| Challenge | Confidence mismatch copy (AA / MES when authored) |
| Reassure | Underconfidence alignment patterns in microcopy library |
| Wait / Silent | Empty Mission Intelligence; honest refusal |
| Reflect | ILE-005 journal prompts; commitment five-beat |

---

## Plain language

**Never expose to students:** Twin, warrant, ranking algorithm, Mission Engine, Adaptive Decision Engine, Learning Orchestrator, mastery score as identity.

**Translation already exists** in `recommendation_explanation.py` — keep using it for authored MES strings.

**Avoid robotic chrome:** “Why the system chose this” (Runtime C panel) fails Sensei voice if that surface is ever enabled.

---

## Speaker & noun hygiene (operational)

Until a future copy programme converges terms:

1. Pick **one daily-focus noun** per surface family and stick to it in new copy.  
2. Prefer **Mission** on Sensei educational surfaces (Journal / Timeline / Mission Intelligence) *or* **Session** on PX OS chrome — do not invent a third (“tip”) for primary guidance.  
3. Name the Sensei on first educational orientation (onboarding should eventually introduce Study Sensei once, then use it consistently on memory surfaces).  
4. Reflection invites must state **optional** and **non-scoring** (ILE-005 already does).

See `TERMINOLOGY_REGISTER.md` for observed conflicts.

---

## Evaluation checklist (before shipping learner-facing text)

1. Would a trusted Sensei say this — or a chatbot / engagement engine?  
2. Is claim strength matched to evidence?  
3. Can the student answer *why this, now*?  
4. Does this encourage without inflating, challenge without shaming, wait without abandoning?  
5. Would removing brand chrome still sound like the same calm professional guide?  
6. Is the speaker named consistently with neighbouring surfaces?  
7. Are Mission / Session / tip / recommendation used without contradicting the previous screen?

If any answer fails, rewrite in a later package — not in RP-001.3.

---

## Relationship to other standards

| Document | Governs |
|----------|---------|
| ILE-001C0 Communication Framework | Behavioural communication law |
| PTP-003 Product Communication Standard | Claim taxonomy (Observed / Estimated / Unavailable) |
| ILE-001A Terminology Standard | Anxiety-safe AA wording (exam/test/pass/fail bans) |
| PX-002A / PRODUCT_LANGUAGE_GUIDE | OS surface nouns (Home, History, Session…) |
| This Voice Guide | Operational Sensei voice for Alpha certification |

Conflicts between PX Session nouns and ILE Mission nouns are **documented**, not resolved, in RP-001.3.

---

**End of VOICE_GUIDE**

# Student Journeys — Adaptive Assessment

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design  
**Effective:** 2026-07-28  

---

## Purpose

Describe how Adaptive Assessment appears inside real study life. Journeys are product narratives for design and implementation sequencing — not engine algorithms.

Each journey states: trigger, student feeling to protect, session type(s), feedback expectation, and Twin / Mission / Tutor effects (conceptually).

---

## Shared journey grammar

Every Adaptive Assessment journey follows:

1. **Frame** — why this check exists now (Context Card when ILE-001C framing is enabled)  
2. **Consent to continue** — start is voluntary within the Mission path; exit/pause allowed  
3. **Check** — questions selected for educational intent and time budget  
4. **Immediate feedback** — Educational Summary + next action; no identity score  
5. **State update** — observations → Reasoning → Twin (platform path; not changed by ILE-001C)  
6. **Bridge** — Mission / Tutor reflect the new honest state  

Student experience diagram (Quick Check with framing):

```
Mission → Context Card → Quick Check → Reflection → Educational Summary → Mission
```

If any step cannot be explained in plain language, the journey must not ship as authoritative.

---

## 1. Daily learning check

**Intent:** Keep today’s mission accurate with a short formative probe.

| Aspect | Design |
|---|---|
| **When** | Mid-mission or end of a study block on today’s topic |
| **Session type** | Quick Check (default); Deep Check only if time budget allows and uncertainty is high |
| **Student need** | “Am I getting this idea enough to move on?” |
| **Feeling to protect** | Calm continuity with the session — not a pop quiz |
| **Framing copy (illustrative)** | “Short check so today’s plan stays accurate.” |
| **After** | Brief evidence summary; continue or gently redirect within the same Mission |
| **Avoid** | Surprise timing; long batteries; percentage banners |

---

## 2. Knowledge confirmation

**Intent:** Strengthen evidence before the product speaks more confidently about understanding.

| Aspect | Design |
|---|---|
| **When** | Twin / Reasoning requests stronger evidence before firmer mastery language; after a solid study stretch |
| **Session type** | Deep Check or Readiness Check (topic-scoped) |
| **Student need** | “Is this actually solid, or only familiar?” |
| **Feeling to protect** | Respect — confirmation is not a pass/fail gate |
| **Framing** | “Confirm this understanding with a careful check — no grades.” |
| **After** | Either “evidence looks stronger” (provisional) or “still uncertain — here’s what to reinforce” |
| **Avoid** | Locking progress until “pass”; declaring mastery from one run |

---

## 3. Confidence calibration

**Intent:** Align how confident the student *feels* with what evidence supports.

| Aspect | Design |
|---|---|
| **When** | Persistent mismatch signals (optional self-confidence vs outcomes); student requests a Confidence Check; pre-revision honesty moments |
| **Session type** | Confidence Check |
| **Student need** | “Am I over- or under-confident on this?” |
| **Feeling to protect** | Non-judgemental curiosity; optional confidence prompts never forced into anxiety |
| **During** | Invite brief confidence before or after items when pedagogically useful |
| **After** | Calibration narrative: aligned / overconfident / underconfident — with what would reduce uncertainty |
| **Avoid** | Shaming language; treating calibration as a personality flaw |

Detailed UX: `CONFIDENCE_AND_UNCERTAINTY_UX.md`.

---

## 4. Revision verification

**Intent:** Test durability of understanding on spaced revisit — not re-teach by default.

| Aspect | Design |
|---|---|
| **When** | Revision due; stability uncertain; Learning Graph / Twin flags revisit |
| **Session type** | Revision Check |
| **Student need** | “Does this still hold after time away?” |
| **Feeling to protect** | Normalise forgetting; frame as expected professional learning |
| **Framing** | “See what still feels solid from earlier work.” |
| **After** | Hold / reinforce / recover — Mission adjusts tomorrow accordingly |
| **Avoid** | Treating forgotten items as failure of character |

---

## 5. Weak-topic reinforcement

**Intent:** Target known weak or gapped topics with checks that feed recovery — not endless drill for engagement.

| Aspect | Design |
|---|---|
| **When** | Persistent gap / misconception tags; recovery path mid-flight; student accepts a weak-topic recommendation |
| **Session type** | Quick Check or Deep Check scoped to the weak objective; Recovery Check when verifying foundation repair |
| **Student need** | “Help me shore this up without drowning me.” |
| **Feeling to protect** | Encouragement; specific misconception language when known |
| **After** | Clear link to recovery or practice Mission steps; Tutor available to explain the mix-up |
| **Avoid** | Repeating identical items immediately; piling multiple weak topics into one anxious battery |

---

## 6. Recovery after long inactivity

**Intent:** Re-enter study gently; re-establish Educational State without pretending the gap didn’t happen.

| Aspect | Design |
|---|---|
| **When** | Significant study gap; Twin evidence stale; plan resumes |
| **Session type** | Recovery Check (primary); short Quick Check only if cognitive load must stay minimal |
| **Student need** | “Where am I, safely?” |
| **Feeling to protect** | Welcome back — never delinquency or streak punishment |
| **Framing** | “Welcome back. A gentle check helps us restart accurately.” |
| **Selection intent** | Prefer breadth-light confirmation of last stable areas + one soft probe of likely decay — respect time and fatigue |
| **After** | Honest “we’re less sure after the break”; Mission prioritises re-orientation over aggressive new content |
| **Avoid** | Full syllabus stress tests; guilt copy; inventing mastery to “motivate” return |

---

## 7. Pre-exam confidence check

**Intent:** Calibrate readiness belief before sitting — honest and bounded.

| Aspect | Design |
|---|---|
| **When** | Near exam date; student or Mission requests a Readiness / Confidence Check; syllabus-weighted sample within time budget |
| **Session type** | Readiness Check (primary); Confidence Check as companion reflection |
| **Student need** | “Where should I focus in the time left?” |
| **Feeling to protect** | Honesty without terror or false reassurance |
| **Framing** | “A readiness check — it guides last study, it does not predict your result.” |
| **After** | Prioritised focus list grounded in evidence + uncertainty; explicit non-guarantee language |
| **Avoid** | Pass prediction; “Exam Ready” marketing; competitive percentiles |

---

## Cross-journey rules

| Rule | Rationale |
|---|---|
| Always explain why the check exists | Product Principles — explain every decision |
| Respect available study time | Sustainable progress; Mission duration realism |
| Prefer one journey intent per session | Cognitive load doctrine |
| Incomplete journeys leave uncertainty visible | Evidence before inference |
| Home still shows one primary Next | One educational truth |

---

## Journey → session type map (summary)

| Journey | Primary session type | Secondary |
|---|---|---|
| Daily learning check | Quick Check | Deep Check |
| Knowledge confirmation | Deep Check | Readiness Check (topic) |
| Confidence calibration | Confidence Check | Quick Check |
| Revision verification | Revision Check | Quick Check |
| Weak-topic reinforcement | Quick / Deep Check | Recovery Check |
| Recovery after inactivity | Recovery Check | Quick Check |
| Pre-exam confidence | Readiness Check | Confidence Check |

Session definitions: `SESSION_TYPES.md`.

---

**End of STUDENT_JOURNEYS**

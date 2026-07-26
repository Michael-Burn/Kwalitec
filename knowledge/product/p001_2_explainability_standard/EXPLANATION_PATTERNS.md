# Explanation Patterns

**Programme:** P-001.2 — Explainability Standard  
**Version:** 1.0  
**Status:** Active — standard templates for student-facing guidance  
**Effective:** 2026-07-26  
**Companion:** [`EXPLAINABILITY_STANDARD.md`](EXPLAINABILITY_STANDARD.md)  

---

## How to use

1. Choose the pattern that matches the guidance type.
2. Fill every schema field required for the target [explanation level](EXPLAINABILITY_STANDARD.md#6-explanation-levels).
3. Keep wording educational and student-safe (EIP-003 language rules).
4. Substitute bracketed placeholders; do not ship placeholder text.
5. If a field is not yet knowable, say so honestly — do not invent evidence.

Templates below show **Level 2** as the complete schema. **Level 1** compressions and **Level 3** expansions follow each pattern.

---

## Pattern catalogue

| ID | Pattern | Default level |
|---|---|---|
| XP-01 | Daily Study Plan | L1 summary + L2 detail |
| XP-02 | Readiness Assessment | L2 |
| XP-03 | Revision Recommendation | L2 |
| XP-04 | Topic Prioritisation | L2 |
| XP-05 | Study Warning | L1 / L2 |
| XP-06 | Positive Reinforcement | L1 |
| XP-07 | Missed Session Recovery | L1 / L2 |

---

## XP-01 — Daily Study Plan

### Level 2 template

| Field | Template |
|---|---|
| **Recommendation** | Today’s study plan: **[Topic A]** (primary), then **[Topic B]** if time remains. |
| **Why it is recommended** | This order advances your syllabus from your **Current Learning Topic** and repairs **[weak-topic signal]** before adding new material. |
| **Supporting evidence** | Syllabus position: **[topic / unit]**. Recent practice: **[result summary]**. Available study time: **[duration]**. |
| **Confidence level** | **[High / Moderate / Low — Suggested]**. |
| **Expected benefit** | Steady coverage progress today without overloading the session. |
| **Suggested next action** | Start **Today’s Mission** for **[Topic A]**. |
| **Review point** | Revisit after this session completes or if you change available time. |

### Level 1 compression

> **Today:** study **[Topic A]**.  
> **Why:** it’s your next syllabus focus.  
> **Next:** start Today’s Mission.

### Level 3 expansion add

- Decision class: daily plan assembly  
- Inputs cited: plan duration, Learning Mode focus, optional advisory overlays (labelled as advice if divergent)  
- Explicit note if advisory tips differ from Today’s Mission authority  

### Non-compliant examples

- “Highest-value learning path selected.” (no evidence)
- Two conflicting “today” headlines across Dashboard and Coach

---

## XP-02 — Readiness Assessment

### Level 2 template

| Field | Template |
|---|---|
| **Recommendation** | Estimated readiness for **[exam / sitting focus]**: **[building / on track / needs attention / cannot yet be estimated]**. |
| **Why it is recommended** | This judgement reflects **[coverage + practice consistency + recent results]** — not a pass prediction. |
| **Supporting evidence** | Study Progress: **[coverage cue]**. Practice results: **[summary]**. Consistency: **[recent sessions / gaps]**. |
| **Confidence level** | **[High / Moderate / Low / Cannot yet be estimated]**. |
| **Expected benefit** | Honest picture of preparation so you can prioritise the next study block. |
| **Suggested next action** | **[Continue Today’s Mission / focus revision on Topic X / complete a practice check]**. |
| **Review point** | Re-estimate after **[N sessions / next timed practice / weekly plan refresh]**. |

### Level 1 compression

> **Estimated readiness:** **[label]**.  
> **Why:** based on your recent study and practice.  
> **Next:** **[one action]**.

### Level 3 expansion add

- Which components entered the composite (student-safe names only)
- What is missing (e.g. no timed practice yet)
- Explicit non-claim: does not forecast exam pass/fail  

### Non-compliant examples

- Bare percentage with no unpacking
- “You are ready to pass” / mastery theatre from coverage alone
- Empty-state readiness invented as a mid-range score

---

## XP-03 — Revision Recommendation

### Level 2 template

| Field | Template |
|---|---|
| **Recommendation** | Suggested revision: revisit **[Topic X]** for **[duration / session type]**. |
| **Why it is recommended** | Recent practice shows **[error pattern / score drop / long gap since last review]** on this topic. |
| **Supporting evidence** | Last studied: **[date or session count]**. Practice checks: **[summary]**. Time to exam: **[cue if used]**. |
| **Confidence level** | **[Moderate / Low — Suggested]** (prefer humble labels when history is thin). |
| **Expected benefit** | Strengthen recall before moving further or sitting timed practice. |
| **Suggested next action** | Schedule or start a revision block for **[Topic X]** (optional if Learning Mode focus differs — say so). |
| **Review point** | After the revision session or next practice check on **[Topic X]**. |

### Level 1 compression

> **Suggested:** revise **[Topic X]**.  
> **Why:** recent practice was weak / overdue.  
> **Next:** open a short revision session.

### Level 3 expansion add

- Gap length, practice trend direction, whether advice diverges from Today’s Mission  
- Maintenance vs intensive revision posture in plain language  

### Non-compliant examples

- “The engine selected Topic X.”  
- Silent replacement of Today’s Mission with revision advice

---

## XP-04 — Topic Prioritisation

### Level 2 template

| Field | Template |
|---|---|
| **Recommendation** | Prioritise **[Topic X]** over **[Topic Y]** for this study block. |
| **Why it is recommended** | **[Topic X]** is **[next on syllabus / blocking later topics / showing weaker practice]** relative to **[Topic Y]**. |
| **Supporting evidence** | Syllabus order: **[cue]**. Practice comparison: **[X vs Y]**. Constraints: **[time / exam proximity]**. |
| **Confidence level** | **[High / Moderate / Low — Suggested]**. |
| **Expected benefit** | Better use of limited study time on the higher-leverage topic. |
| **Suggested next action** | Study **[Topic X]** now; keep **[Topic Y]** for later. |
| **Review point** | After this block or when practice results change the comparison. |

### Level 1 compression

> **Focus first:** **[Topic X]**.  
> **Why:** **[one syllabus or practice reason]**.  
> **Next:** start that topic.

### Level 3 expansion add

- Ranked factors (max three) with which factor dominated  
- Explicit uncertainty if topics are near-tied  

### Non-compliant examples

- Multi-factor jargon dump without a winner
- Prioritisation that contradicts the same-day plan without disclosure

---

## XP-05 — Study Warning

### Level 2 template

| Field | Template |
|---|---|
| **Recommendation** | Attention: **[risk statement in plain language]**. |
| **Why it is recommended** | Continuing as-is may **[slow coverage / deepen a weak topic / reduce readiness honesty]**. |
| **Supporting evidence** | **[Missed sessions / declining practice / plan–duration mismatch / overdue revision]**. |
| **Confidence level** | **[Moderate / High]** for observed facts; keep estimates labelled. |
| **Expected benefit** | Early course-correction before the gap widens. |
| **Suggested next action** | **[Concrete recovery step]**. |
| **Review point** | Check again after **[next session / end of week]**. |

### Level 1 compression

> **Heads-up:** **[short risk]**.  
> **Why:** **[one evidence cue]**.  
> **Next:** **[one action]**.

### Level 3 expansion add

- Severity basis (observed fact vs estimate)
- What is *not* claimed (no panic pass/fail prophecy)

### Non-compliant examples

- Fear-only copy with no next action
- Colour/icon warning with no text reason
- Threatening language that invents exam failure certainty

---

## XP-06 — Positive Reinforcement

### Level 1 template (default)

| Field | Template |
|---|---|
| **Recommendation** | Well done — you completed **[session / mission / practice check]** on **[Topic X]**. |
| **Why it is recommended** | Consistent study on the syllabus builds exam preparation. |
| **Supporting evidence** | Completed: **[what happened]**. |
| **Confidence level** | N/A for pure observed completion; do not inflate into mastery. |
| **Expected benefit** | Reinforces the habit of finishing planned study. |
| **Suggested next action** | **[Rest / reflect / continue to next checklist step / review tomorrow’s plan]**. |
| **Review point** | Usually N/A; optional “see progress on Journey” without new claims. |

### Level 2 (when celebrating a streak of learning evidence)

Add one evidence-backed estimate only if lawful — still labelled **Estimated** — and never equate coverage with mastery.

### Level 3

Rarely needed; if used, separate celebration (Experience) from educational judgement (authority surfaces).

### Non-compliant examples

- “You’ve mastered Topic X” from session completion alone
- Achievement theatre that rewrites readiness or mission priority

---

## XP-07 — Missed Session Recovery

### Level 2 template

| Field | Template |
|---|---|
| **Recommendation** | Recovery plan: resume with **[Topic X / Today’s Mission]** for **[adjusted duration]**. |
| **Why it is recommended** | You missed **[session / day]**; a shorter restart protects consistency better than skipping again. |
| **Supporting evidence** | Missed: **[when]**. Open focus: **[Current Learning Topic]**. Available time today: **[cue]**. |
| **Confidence level** | **[Moderate / Suggested]**. |
| **Expected benefit** | Return to a sustainable study rhythm without pretending the miss did not happen. |
| **Suggested next action** | Start the recovery session for **[Topic X]** now (or schedule today’s shorter block). |
| **Review point** | After this recovery session; restore normal plan duration when back on track. |

### Level 1 compression

> **Resume today:** **[Topic X]** (short session).  
> **Why:** get back on your syllabus after the missed study.  
> **Next:** start the recovery session.

### Level 3 expansion add

- Whether plan duration was adjusted and why
- Explicit note that recovery does not invent catch-up mastery

### Non-compliant examples

- Silent plan rewrite with no miss acknowledgement
- Guilt-heavy copy without a feasible next action
- “Double session” pressure that ignores available time honesty

---

## Cross-pattern rules

1. **One authorised today** — XP-01, XP-04, XP-05, and XP-07 must not fight Learning Mode / Today’s Mission without labelling advice as optional.
2. **Honesty over comfort** — XP-02 and XP-05 must under-claim rather than soothe with false precision.
3. **Celebration ≠ diagnosis** — XP-06 must not become a readiness or mastery engine.
4. **Same inputs → same story** — If Coach and Dashboard cite the same decision, Why + Evidence must agree (Runtime A consistency).

---

## Related

- Schema & levels: [`EXPLAINABILITY_STANDARD.md`](EXPLAINABILITY_STANDARD.md)
- Review gate: [`EXPLAINABILITY_REVIEW_CHECKLIST.md`](EXPLAINABILITY_REVIEW_CHECKLIST.md)
- Educational speech law: `knowledge/educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`

---

**End of EXPLANATION_PATTERNS**

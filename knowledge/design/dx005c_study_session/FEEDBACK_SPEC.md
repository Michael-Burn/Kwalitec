# Feedback Spec

**Programme:** DX-005C  
**Status:** Binding for Study Session feedback  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 Success & Error Copy; `PRACTICE_MODEL.md`  

---

## 1. Purpose

Feedback closes the Decision → Action → Feedback loop for practice. It must teach. It must not soothe, celebrate, or entertain.

---

## 2. Philosophy

Feedback should be:

| Attribute | Meaning |
|---|---|
| **Immediate** | Shown in-session as soon as the attempt is evaluated |
| **Specific** | Names the outcome and the learning target |
| **Educational** | Points to what to review or how to correct |
| **Never emotional** | No cheer, comfort, shame, or humour |

---

## 3. Pattern

```
Outcome
    ↓
Educational directive (one short sentence)
    ↓
Optional detail (expandable / L2)
```

### Correct

```
Correct.
[Optional one-line reinforcement of the method — not praise]
```

Example:

> Correct.  
> Posterior updates with the likelihood under each hypothesis.

### Incorrect

```
Incorrect.
[What to review or how to proceed]
```

Example:

> Incorrect.  
> Review Bayes' theorem before continuing.

### Partial / needs work (if product supports)

```
Incomplete.
[What remains]
```

Example:

> Incomplete.  
> State the prior before applying the update.

---

## 4. Forbidden feedback

| Forbidden | Why |
|---|---|
| Don’t worry! | Emotional padding |
| You’re doing great! | Encouragement theatre |
| Oops! / Whoops! | Unprofessional (DX-003) |
| Keep it up! / You’ve got this! | Motivation — not Session’s job |
| Confetti / badges / +XP | Gamification |
| Long essays before next Primary | Blocks practice |
| Blame (“You failed because…”) | Unprofessional; prefer content directive |
| Platform tutorial (“Here’s how Kwalitec scores…”) | Wrong owner |

---

## 5. Tone rewrite examples

| Instead of | Use |
|---|---|
| “Don’t worry — everyone struggles with Bayes!” | **Incorrect. Review Bayes' theorem before continuing.** |
| “Amazing work!!! 🎉” | **Correct.** |
| “Oops, something’s not quite right with your answer.” | **Incorrect.** + one educational line |
| “You’re on a 5-day streak — keep going!” | *(omit entirely)* |
| “The system thinks you might want to revisit…” | **Review [topic] before continuing.** |

---

## 6. Placement

| Element | Layer |
|---|---|
| Outcome + one educational sentence | L1 (immediate, visible) |
| Worked approach / full solution | L2 disclosure after outcome |
| Why this question / explainability | L2 |
| Scoring diagnostics / item ids | L3 |

Do not open L2 by default after every answer. After incorrect, optional **Show worked approach** disclosure is allowed without becoming a second Primary — Primary remains **Continue** (or **Retry** when that is the required next action).

---

## 7. Primary after feedback

| State | Primary |
|---|---|
| More steps remain; attempt closed | **Continue** |
| Retry required before advance | **Retry** / **Try again** |
| Finding must be acknowledged | **Review Finding** |
| Last step done | **Complete Session** |

Exactly one Primary. “View explanation” is L2, not a peer filled CTA.

---

## 8. Blocking vs feedback

| Signal | Role |
|---|---|
| **Blocking issue** | Prevents Primary success (e.g. empty answer) — validation, not educational outcome |
| **Feedback** | Result after a valid attempt |

Blocking copy (DX-003): problem → reason → action. Example: **Answer required.** Focus the input.

---

## 9. Timing

| Event | Latency |
|---|---|
| Client-side validation (empty) | Immediate |
| Server-evaluated attempt | Prefer <1s perceived; show quiet pending only if needed |
| Never | Delay feedback for celebration animation |

---

## 10. Accessibility

- Feedback region uses an assertive live region for outcome text.  
- Focus moves to feedback heading after submit.  
- Colour is not the sole incorrect/correct signal (text outcome required).  
- Semantic colour only (DX-001).

---

## 11. Acceptance tests

1. Incorrect answer shows “Incorrect.” plus educational directive — no encouragement.  
2. Correct answer does not award badges or streaks.  
3. Feedback appears before navigation to the next activity.  
4. L2 explanation is collapsed by default.  
5. Empty submit shows blocking validation, not “Incorrect.”

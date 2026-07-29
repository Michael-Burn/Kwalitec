# Success & Error Copy Guide

**Programme:** DX-003  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`

---

## Success messages

Replace verbose confirmations with outcome labels.

### Pattern

```
[Object] [Outcome]
```

or simply:

```
[Outcome]
```

### Examples

| Instead of | Use |
|---|---|
| “The curriculum has successfully been published and is now available to students in the catalogue.” | **Published** or **CS1 published.** |
| “Your study plan was created successfully! You can now start learning.” | **Plan saved.** |
| “Welcome back — continuing where you left off.” | **Continued.** (or omit if Session already shows progress) |
| “Validation completed with no blocking findings.” | **Validation passed.** |
| “Preview built successfully for founder review.” | **Preview ready.** |
| “Curriculum approved. You may now publish.” | **Approved.** |

### Rules

- Prefer **1–4 words**; maximum one short sentence.  
- Name the object when ambiguity exists across subjects.  
- Do not narrate student-facing consequences already implied by Ready.  
- Do not stack success flash + permanent success banner + KPI “Published” chip.

---

## Error messages

Professional. Specific. Actionable.

Never: “Oops.”  
Never: “Something went wrong.”  
Never: humour or blame.

### Pattern

```
Problem
    ↓
Reason
    ↓
Action
```

| Beat | Content |
|---|---|
| **Problem** | What failed (outcome verb) |
| **Reason** | Why (gate, missing input, conflict) |
| **Action** | What to do next |

### Compact form (flashes)

One sentence may encode all three beats when space is limited:

> Couldn’t publish — approval incomplete. Approve, then publish.

Prefer three short clauses over one essay.

### Rewrite examples (operator)

| Current tendency | Target |
|---|---|
| “We couldn't create this subject because the code already exists. Duplicate codes confuse enrolment and version history. Choose a different subject code or open the existing workspace, then try again.” | Subject code exists. Open existing workspace or choose another code. |
| “We couldn't advance the workflow because readiness gates are incomplete. Skipping gates risks publishing an unfinished curriculum. Complete the current stage checklist, then try again.” | Can’t advance — stage incomplete. Finish the current stage, then advance. |
| “We couldn't complete validation because blocking findings remain. Students must not receive incomplete curriculum. Review the Validation findings below, fix CMP/syllabus issues, then try again.” | Validation blocked — 3 findings. Fix findings, then validate. |
| “We couldn't approve this curriculum because validation has not passed…” | Can’t approve — validation not passed. Validate, then approve. |
| “We couldn't complete this step because a Studio service is temporarily unavailable…” | Studio service unavailable. Refresh and retry. |

### Student examples

| Situation | Target |
|---|---|
| Subject not Ready | Subject not Ready. Choose another subject. |
| Session submit failed | Answer not saved. Check connection, then submit again. |
| Permission | Access denied. Sign in with an authorised account. |
| Not found | Page not found. Return Home. |
| Server | Request failed. Retry. If it persists, contact support. |

---

## Mapping to existing `recover_flash`

`operator_guidance.recover_flash` today uses long “We couldn't… because… then try again” essays. DX-004+ should shorten to Problem → Reason → Action without losing specificity. Keep exception-type branching; cut pedagogical justification sentences (“Students must not…”, “Duplicate codes confuse…”).

---

## Flash severity

| Level | Use |
|---|---|
| success | Outcome label only |
| warning | Gate / incomplete — actionable |
| danger / error | Failed Action with recovery |
| info | Rare; prefer silence or inline state |

---

## Checklist

- [ ] Success ≤ one short sentence  
- [ ] Error has Problem, Reason, Action  
- [ ] No “Oops” / “Something went wrong”  
- [ ] No marketing or congratulations  
- [ ] Canonical verbs from `TERMINOLOGY_DICTIONARY.md`

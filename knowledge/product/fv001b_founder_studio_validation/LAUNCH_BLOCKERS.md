# FV-001B — Launch Blockers

**Date:** 2026-07-28  
**Definition:** Critical usability or workflow issues that prevent reliable curriculum publication through the visible Founder Studio.

---

## Blocker list

### LB-1 — Publication path cannot reach Ready

**Severity:** Critical  
**Evidence:** Approve and Publish refused; Studio counters **Published 0 / Drafts 1 / Pending validation 1**; Subjects show CS1B at Validation, not Ready.  
**Why it blocks:** Acceptance requires publish verified curriculum and confirm Ready.

---

### LB-2 — No trustworthy extracted curriculum to review

**Severity:** Critical  
**Evidence:** Preview `not_ready · 0 nodes`; Review Queue has no structure/correction UI; Founder cannot verify IFoA topics/objectives.  
**Why it blocks:** Acceptance requires review extracted curriculum and correct issues.

---

### LB-3 — Validation / progress messaging is not actionable

**Severity:** Critical  
**Evidence:** Simultaneous signals: validation failed (blocking), NEXT STEP “validation looks ready”, “0 validation errors”, checklist 3/8.  
**Why it blocks:** Founder cannot understand extraction/validation progress or what to fix next.

---

### LB-4 — Official document slots can show the wrong file

**Severity:** Critical  
**Evidence:** After sequential PDF selection, syllabus file labelled under Official CMP and CMP under Official Syllabus.  
**Why it blocks:** Undermines confidence that the authorised sources are correctly bound before publish.

---

### LB-5 — Unnecessary EI/engineering terminology on authoring surface

**Severity:** Critical (acceptance criterion)  
**Evidence:** Knowledge Graph, Pipeline, Entity Details, embeddings, nodes on workspace.  
**Why it blocks:** Explicit acceptance criterion: never encounter unnecessary Educational Intelligence terminology.

---

## Non-blockers (constrained)

| Item | Notes |
|---|---|
| Invite-only accounts | Assumed for Internal Alpha; not scored as Studio publication blocker |
| Student experience gaps | Out of FV-001B scope |
| Correct refuse of incomplete publish | Safety behaviour; blocker is inability to ever succeed, not the refuse itself |

---

## Launch decision implication

Any one of LB-1…LB-4 is sufficient for **NO-GO**. LB-5 independently fails a stated acceptance criterion.

**Combined:** **NO-GO** for internal production use of Founder Studio as a complete curriculum-authoring experience.

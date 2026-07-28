# CQ-005 — Guidance Journey Audit

**Programme:** CQ-005 — Guidance Trust  
**Date:** 2026-07-28  
**Path audited:** Production sole-runtime — Home guidance → Session Overview → Activity → completion → Home  
**Method:** Code + template inspection; EP-008 / CQ-002–004 residual inventory; CR3 lens  
**Constraint:** No recommendation / Twin / readiness algorithm changes

---

## 1. Journey map (guidance lens)

```
Home (pre-session)
  MES L1: Why · Why now · You'll work toward · Next · readiness bridge
  L2 disclosure + Mission Intelligence <details>
  Guidance panel → often pointer (“covered in the Mission card above”)
  Friction: label drift (Why / Why it matters); rich why buried;
            Guidance empty of trust extras; “Evidence” jargon in Readiness

Session entry
  Overview intro echoes topic (CQ-004)
  why_studying often default “High value for exam readiness” or empty of Home why
  Friction: personalised Home why disappears — trust discontinuity

Active study
  Topic-threaded prompts (CQ-004); no mission-why echo
  Friction: practice feels connected to topic, not to “why today”

Resume (mid-session Home)
  Continue CTA; Why / commitment suppressed (CQ-003 / CR2)
  Friction: no one-line reconnection to original rationale

Completion → Home
  Summary next step; commitment reflection (compacted CQ-004)
  Friction: residual density; History defers full “why” to Journal/Timeline
```

---

## 2. Friction inventory (trust lens)

| ID | Moment | Friction | Severity | V1 fix? |
|---|---|---|---|---|
| G01 | Overview | Home why not threaded into `why_studying` | **Critical** | Yes |
| G02 | Home hero | Competing why labels / sources | **Major** | Yes |
| G03 | Resume | Full why suppressed; no reconnection line | **Major** | Yes (one line) |
| G04 | Guidance panel | Pointer instead of evidence/alternatives teaser | **Med** | Yes |
| G05 | Readiness / QC / MI | “Evidence” / over-confident synthesis | **Med** | Yes (copy) |
| G06 | Activity | No mission-why echo in context | **Med** | Yes |
| G07 | Cold-start fallbacks | Sound authoritative without authored MES | **Med** | Yes (soften) |
| G08 | History | Why deferred to Journal/Timeline | **Low–Med** | Defer |
| G09 | Reflection family | Meta disclaimers (residual CQ-004) | **Low** | Defer |

---

## 3. What already works (trust enablers)

- Schema-complete MES with `why_recommended`, `timeliness_line`, `suggested_next_action`, alternatives, refusal
- EP-008.1 L2 explanation card and commitment lifecycle
- CQ-002 single primary CTA; CQ-003 honest Continue resume
- CQ-004 topic continuity Home → Activity
- Honest readiness non-guarantee language on Session meta

---

## 4. Audit verdict

**CR3 remains Emerging (50)** because guidance is **computed and often correct on Home**, but **feels fragmented** across surfaces: why is buried, Overview drops it, resume erases it, and secondary panels use system jargon or empty pointers. Highest-leverage V1 work: **surface and echo existing authored why** — continuity and wording, not new intelligence.

---

**End of Guidance Journey Audit**

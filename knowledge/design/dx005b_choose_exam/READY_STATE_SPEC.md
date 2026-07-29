# Ready State Specification

**Programme:** DX-005B  
**Status:** Binding for Ready availability on Choose Exam  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 Status System; DX-005B Discovery Architecture  
**Companion:** `COMING_SOON_SPEC.md`

---

## 1. Law

Only **Ready** curricula may expose **Begin Learning**.

No false affordances. If the student cannot start studying, the UI must not look like they can.

---

## 2. Definition (student-facing)

| Term | Meaning |
|---|---|
| **Ready** | Verified curriculum is available for the student to begin learning |
| Operator **Published** | Operator outcome — never used as the student catalogue badge |

Per DX-003: Operators Publish; students see Ready.

---

## 3. Technical readiness (implementation mapping)

A catalogue card is **Ready + selectable** only when all hold:

1. Support / catalogue projection marks availability `ready`  
2. Plan creation / enrolment is allowed (`allows_plan_creation` / Runtime enrolment flags)  
3. Active package or on-disk curriculum exists as required by the enrolment path  

| Projection state | Badge | Selectable | Begin Learning |
|---|---|---|---|
| Ready + enrolable | Ready (optional quiet) | Yes | Enabled after select + confirm |
| Ready package, enrolment disabled | Ready or quiet none | **No** | **Disabled** — prep line only |
| Coming Soon | Coming Soon | No | Never |
| Not supported | — | Omitted | — |

Fail closed at confirm / POST even if UI is bypassed (preserve existing gate behaviour).

---

## 4. Presentation

### L0 Ready band

| Element | Rule |
|---|---|
| Band heading | **Ready to begin** |
| Selection | Single-select only |
| Badge | Optional quiet **Ready** — omit if band heading already conveys it |
| L2 fields | Brief description; estimated study scope; last updated |
| Primary | Page-level **Begin Learning** (not per-row filled Primaries) |

### L2 field rules

| Field | Purpose | Forbidden |
|---|---|---|
| Brief description | Recognise the exam | Marketing; feature lists |
| Estimated study scope | Commitment honesty (e.g. topic count / structured scope) | Progress %; mastery rings |
| Last updated | Freshness of published material | Pipeline timestamps as theatre |

Edition / version may appear quietly in L2 if needed for identity — never as hero chrome.

---

## 5. Prioritisation within Ready

Default order:

1. **Recommended** (if deterministic signal exists)  
2. **Recently updated**  
3. **Alphabetical**  

Recommended is sort priority or a single quiet marker — never an essay.

---

## 6. Empty Ready

| Beat | Copy |
|---|---|
| **Reason** | No Ready subjects yet. |
| **Next Action** | Return later |

Aligns DX-003 empty standards; DX-005B brief: Reason → Return later. Nothing else.

Contact support is **not** a default empty Primary for general Alpha emptiness. If Alpha policy requires unblock, place Contact under Help — not as a competing Choose Exam Primary.

---

## 7. Blocked selection (support gate)

If POST attempts a non-Ready subject:

| Beat | Copy |
|---|---|
| Reason | Subject not Ready. Choose another subject. |
| Next | Return to Ready list (no Begin) |

Gate may list Ready alternatives as **informational names** — not a second catalogue redesign. Prefer auto-focus back to Ready band.

---

## 8. Success test

A reviewer can Begin Learning only on a Ready, enrolable row. Enrolment-gated “Ready” rows never enable the Primary. Empty Ready shows two beats only.

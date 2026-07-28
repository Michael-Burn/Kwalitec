# Authority Transition Map

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.2 — Educational Authority Model  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** `EDUCATIONAL_AUTHORITY_MODEL.md`  
**Companions:** `AUTHORITY_DECISION_MATRIX.md`, `AUTHORITY_CONFLICT_REGISTER.md`

---

## Purpose

Map **intentional authority transitions** throughout the student journey so learners always know who is speaking — and so implementers never hide a speaker change.

Authority transitions must always be intentional. Hidden handoffs are governance defects (see Conflict Register AC-05).

This map does not change product behaviour.

---

## Canonical journey (authorised)

```
Authentication
      │
      ▼
   Kwalitec
      │
      ▼
  Onboarding
      │
      ▼
Kwalitec introduces Study Sensei
  (required handoff sentence)
      │
      ▼
     Home
      │
      ▼
Study Sensei becomes educational authority
      │
      ├──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
   Mission       Session      Study Plan      Revision
      │              │         (structure)     (Sensei)
      ▼              ▼
Mission Intelligence / Commitment / explanations
      │              │
      ▼              ▼
 Decision Journal ←── Session / Commitment reflection close
      │
      ▼
 Educational Timeline
      │
      ▼
 Educational Feedback Loop
      │
      ▼
 History / Journey (context; not Sensei narrative primary)
      │
      ▼
 Settings / Profile / Help / Auth recovery
      │
      ▼
   Kwalitec
```

**Required handoff sentence (DG-001.1-D01 / DG-001.2-D04):**  
> Study Sensei is how Kwalitec guides your daily learning decisions.

---

## Transition catalogue

Each row is an authorised edge. “Signal” is how the student should perceive the change (future copy programmes).

| ID | From | To | Trigger | Primary after | Signal (governance intent) | Hidden? |
|----|------|----|---------|---------------|----------------------------|---------|
| T01 | — | Kwalitec | Arrive at login / welcome | Kwalitec | Product brand visible | No |
| T02 | Kwalitec | Kwalitec | Successful authentication | Kwalitec | Account acknowledged by product | No |
| T03 | Kwalitec | Kwalitec | Enter onboarding / wizard | Kwalitec | Product orients “what this is” | No |
| T04 | Kwalitec | Study Sensei | Onboarding handoff sentence | Study Sensei | Explicit introduction of mentor | **Must not be silent** |
| T05 | Study Sensei | Study Sensei | Land on Home educational hero | Study Sensei | Mentor owns “what today” | Prefer Sensei named once nearby |
| T06 | Study Sensei | Study Sensei | Open Mission Intelligence | Study Sensei | Same mentor; deeper brief | No |
| T07 | Study Sensei | Study Sensei | Mission Commitment (accept/defer) | Study Sensei | Agency with mentor continuity | No |
| T08 | Study Sensei | Study Sensei | Mission explanation disclosure | Study Sensei | Why this Mission / guidance | No |
| T09 | Study Sensei | Study Sensei | Start Session | Study Sensei (+ System status) | Mentor frames practice; System clocks | No |
| T10 | Study Sensei | Study Sensei | Session / Commitment reflection | Study Sensei | Close practice; not new tutor | No |
| T11 | Study Sensei | Study Sensei | Open Decision Journal | Study Sensei | Educational memory | No |
| T12 | Study Sensei | Study Sensei | Open Educational Timeline | Study Sensei | Long-term story | No |
| T13 | Study Sensei | Study Sensei | Feedback Loop reflection | Study Sensei | Calibrate guidance usefulness | No |
| T14 | Study Sensei | Kwalitec | Open Help / support | Kwalitec | Product teaches Sensei vocabulary | Explicit product chrome |
| T15 | Study Sensei | Kwalitec | Open Settings / Profile | Kwalitec | Account / preferences | Explicit product chrome |
| T16 | Study Sensei | Kwalitec (+ System) | History archive view | System facts + Kwalitec framing | Stats are context, not mentor | Prefer bridge, not alternate tutor |
| T17 | Study Sensei | Kwalitec | Calibration intake (first) | Kwalitec | Declarative product intake | Sensei meaning after T04 |
| T18 | Any | System | Loading / saving / error mechanical | System | Neutral status | No mentor warmth |
| T19 | Any | Kwalitec | Feature-flag / gated capability notice | Kwalitec | Product honesty | Never Sensei |
| T20 | Study Sensei | Kwalitec | Logout / session expiry product path | Kwalitec | Product account speech | No |
| T21 | Kwalitec | Study Sensei | Return Home after Settings | Study Sensei | Re-enter educational domain | Intentional; chrome change sufficient |
| T22 | Study Sensei | Study Sensei | Revision surface | Study Sensei | Review work as guidance | Avoid competing Mission theatre |
| T23 | Study Sensei | Mixed | Notifications | By payload | Delivery = Kwalitec; educational body = Sensei | Payload must declare owner |
| T24 | Any | System → Kwalitec | Error recovery CTA | Kwalitec after System fact | “Try again” / support = product | No Sensei apology theatre |

---

## Phase map

### Phase A — Product gate

| Stage | Primary | Student expectation |
|-------|---------|---------------------|
| Authentication | Kwalitec | I am entering a product |
| Account recovery / errors | Kwalitec + System | Product helps me in; System states facts |

**Boundary:** No educational recommendations before authenticated product entry (except marketing pages outside this Alpha student path).

### Phase B — Orientation and handoff

| Stage | Primary | Student expectation |
|-------|---------|---------------------|
| Onboarding start | Kwalitec | Product explains what Kwalitec is |
| Calibration / plan setup | Kwalitec | I declare coverage and exam context to the product |
| Sensei introduction | **Transition T04** | I meet the mentor; relationship begins |
| First Home | Study Sensei | Mentor answers what deserves attention today |

**Boundary:** Onboarding may describe Missions as product capability, but must complete T04 before claiming mentor memory or guidance ownership.

### Phase C — Educational core

| Stage | Primary | Student expectation |
|-------|---------|---------------------|
| Home | Study Sensei | One educational authority |
| Mission Intelligence | Study Sensei | Same authority, deeper brief |
| Commitment | Study Sensei | I choose with the mentor |
| Explanations | Study Sensei | Mentor explains evidence and uncertainty |
| Session | Study Sensei + System | Mentor frames; System reports workflow facts |
| Journal / Timeline / Feedback Loop | Study Sensei | Mentor remembers and interprets |

**Boundary:** No Kwalitec-as-mentor speech inside Phase C educational surfaces.

### Phase D — Context and structure

| Stage | Primary | Student expectation |
|-------|---------|---------------------|
| Study Plan | Kwalitec structure; Sensei if advising | Plan is syllabus spine, not daily mentor voice by default |
| Journey | Kwalitec / System position facts | Where I am on syllabus |
| History | System + Kwalitec | Archive and stats; bridges to Sensei memory |
| Revision | Study Sensei | Review guidance remains mentor-owned |
| Calibration (return) | Kwalitec intake; Sensei meaning of honesty | Declared coverage ≠ mastery |

**Boundary:** History must not become a second educational narrator (ED-05).

### Phase E — Product control plane

| Stage | Primary | Student expectation |
|-------|---------|---------------------|
| Help | Kwalitec | Product orients; glossary defines Sensei terms |
| Profile / Settings | Kwalitec | Account and preferences |
| Notifications prefs | Kwalitec | Product delivery control |
| Feature-flag messaging | Kwalitec | Product honesty about gated capabilities |
| Success (account/settings) | Kwalitec | Product confirmation |
| Empty / error (product) | Kwalitec / System | Recovery without mentor theatre |

**Boundary:** Help explains Sensei; Help does not *become* Sensei.

---

## Loop transitions (returning students)

| Loop | Path | Rule |
|------|------|------|
| Daily study | Auth (if needed) → Home → Mission → Session → Journal optional → Home | Stay Sensei once past T04 |
| Memory deepen | Home → Journal / Timeline → Home | Sensei throughout |
| Product admin | Home → Settings → Home | Explicit Kwalitec then return Sensei (T21) |
| Support | Home → Help → Home | Kwalitec glossary; return Sensei |
| Re-auth | Session expiry → Kwalitec → Home Sensei | Do not re-teach Sensei every login; handoff once per cohort orientation unless reset |

---

## Intentional vs defective transitions

| Pattern | Classification | Action |
|---------|----------------|--------|
| Onboarding names Sensei once (T04) | Intentional | Required |
| Home educational speech unnamed but Sensei-owned | Acceptable interim | Prefer naming density decision (OQ from DG-001.1) |
| Orientation says “Kwalitec prepares missions”; memory says “Study Sensei remembers” with no handoff | **Defective** (ED-01) | Future copy must insert T04 |
| Runtime C “Why the system chose this” | **Defective if ON** (ED-11) | Rename to Sensei explanation before enable |
| Settings microcopy that recommends what to study | **Defective** | Reassign to Sensei or remove judgement |
| Error page apologising as Study Sensei for outage | **Defective** | System fact + Kwalitec recovery |
| Help FAQ that interprets evidence as tutor | **Defective** | Keep product orientation; point to Sensei surfaces |

---

## Student journey checklist (Board)

A student walking the default Alpha path should experience:

1. **Kwalitec** at the door.  
2. **One clear introduction** of Study Sensei.  
3. **Study Sensei** for every learning decision, explanation, and educational memory.  
4. **Kwalitec** whenever they manage account, legal, or product honesty.  
5. **System** only for facts and mechanical status.  
6. **No surprise** second tutor.

---

## How to use this map

1. Design or review flows against transition IDs T01–T24.  
2. Any new capability must declare entry/exit authority edges.  
3. Copy programmes closing ED-01 must implement T04 and verify Phase C has no Kwalitec-as-mentor.  
4. Cite transition IDs in completion reports when remediating authority drift.

---

**End of AUTHORITY_TRANSITION_MAP**

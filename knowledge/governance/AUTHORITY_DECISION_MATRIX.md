# Authority Decision Matrix

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.2 — Educational Authority Model  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** `EDUCATIONAL_AUTHORITY_MODEL.md`  
**Companions:** `AUTHORITY_TRANSITION_MAP.md`, `AUTHORITY_CONFLICT_REGISTER.md`

---

## Purpose

For every audited student-facing capability, determine:

- **Primary authority**
- **Secondary authority** (if any)
- **Reason**
- **Authority boundary**

Then record **Board governance decisions** with rationale, student expectation, and implementation / future-governance implications.

Governance only — no implementation in this package.

---

## Matrix legend

| Code | Authority |
|------|-----------|
| SS | Study Sensei |
| KW | Kwalitec |
| SY | System |
| → | Intentional transition (see Transition Map) |

---

## Capability matrix

| Capability | Primary | Secondary | Reason | Authority boundary |
|------------|---------|-----------|--------|-------------------|
| Authentication | KW | SY | Product gate; account access | No educational judgement; no Sensei |
| Onboarding | KW → SS | SY | Product orients then hands off mentor | Must complete T04 before Sensei memory claims |
| Home (educational hero / Mission) | SS | SY; KW chrome | Daily educational focus is mentor speech | KW nav/brand chrome only; no KW-as-tutor |
| Mission Intelligence | SS | SY | Composes authorised Mission brief | Never “the system chose”; no billing |
| Mission Commitment | SS | SY | Accept/defer is educational agency with mentor | Product prefs stay in Settings |
| Mission explanations | SS | SY | Why / evidence / uncertainty | No infrastructure narration |
| Study Session | SS | SY | Mentor frames practice; System reports workflow | Session executes; does not re-rank Mission |
| Decision Journal | SS | SY | Educational memory | KW never authors journal narrative |
| Educational Timeline | SS | SY | Interprets Journal as learning story | Not from vanity score theatre |
| Educational Feedback Loop | SS | SY | Calibrates guidance usefulness | Not a second recommendation engine |
| Study Plan | KW | SY; SS when advising | Syllabus spine is product structure | SS may advise pacing; KW owns plan chrome |
| Revision | SS | SY | Evidence-timed review is guidance | Must not compete as second daily Mission (ED-13) |
| History | SY + KW | SS bridges | Archive + stats context | Stats ≠ educational narrative authority |
| Calibration | KW | SY; SS meaning | Declared coverage intake | Honesty: not mastery; Sensei uses after handoff |
| Help | KW | SS glossary | Product teaches product + Sensei vocabulary | Help explains Sensei; does not replace Sensei |
| Profile | KW | SY | Account identity | No learning recommendations |
| Settings | KW | SY | Preferences and controls | No educational judgement copy |
| Notifications (delivery) | KW | SY | Product delivery channel | Educational payload body → SS |
| Notifications (educational body) | SS | KW envelope | Mentor content in product envelope | Envelope must not override mentor meaning |
| Success — educational action | SS | SY | Mentor acknowledges learning step | No subscription upsell as Sensei |
| Success — account / settings | KW | SY | Product confirmation | No fake educational praise |
| Empty — Journal / Timeline / MI | SS | SY | Mentor silence / waiting | Name Sensei; no “system empty” |
| Empty — Help / Settings / Auth | KW | SY | Product empty | No mentor theatre |
| Error — mechanical / HTTP | SY | KW recovery | Facts first | Never Sensei outage apology |
| Error — auth / account | KW | SY | Product recovery | No educational reinterpretation |
| Feature-flag messaging | KW | SY | Product honesty about gated capabilities | Sensei must not explain flags |

---

## Governance decisions

### DG-001.2-D01 — Sole educational judgement authority

| Field | Decision |
|-------|----------|
| **Authority owner** | Study Sensei |
| **Educational rationale** | One mentor relationship for judgement, recommendations, evidence interpretation, memory, and reflection |
| **Student expectation** | The same guide who suggests also explains and remembers |
| **Implementation implications** | Future copy must attribute Mission / Journal / Timeline / MI / Feedback / explanations to Sensei; retire Kwalitec-as-mentor and “the system” narrator |
| **Future governance implications** | Amendments require Board; identity (DG-001.1) and voice guides remain subordinate speakers, not competing owners |

### DG-001.2-D02 — Product / operational authority

| Field | Decision |
|-------|----------|
| **Authority owner** | Kwalitec |
| **Educational rationale** | Product, legal, account, and ops speech must not impersonate teaching |
| **Student expectation** | Company and software speak clearly as product — never as a second tutor |
| **Implementation implications** | Auth, Settings, Profile, Help product FAQ, billing, Alpha notices, flag honesty stay KW-owned |
| **Future governance implications** | New commercial or support surfaces default to KW unless Board creates a fourth authority (forbidden without amendment) |

### DG-001.2-D03 — Factual layer authority

| Field | Decision |
|-------|----------|
| **Authority owner** | System |
| **Educational rationale** | Facts without encouragement protect honesty |
| **Student expectation** | Loading, timestamps, and mechanical errors are not mentoring moments |
| **Implementation implications** | Neutral chrome; no Sensei warmth on CSRF / 404 / sync |
| **Future governance implications** | Telemetry and status UX must remain SY-primary |

### DG-001.2-D04 — Mandatory Sensei handoff

| Field | Decision |
|-------|----------|
| **Authority owner** | Transition T04 (KW → SS) |
| **Educational rationale** | Closes ED-01 dual narrator without deleting product orientation |
| **Student expectation** | I meet Study Sensei once, then educational surfaces belong to that mentor |
| **Implementation implications** | Onboarding (and Help glossary) must include DG-001.1 handoff sentence in a future copy programme |
| **Future governance implications** | Naming density on Home (DG-001.1 OQ-02) is separate; handoff itself is not optional |

### DG-001.2-D05 — One primary per interaction

| Field | Decision |
|-------|----------|
| **Authority owner** | Board rule (all capabilities) |
| **Educational rationale** | Competing primaries recreate narrator drift |
| **Student expectation** | At any moment, one clear speaker owns the message |
| **Implementation implications** | Secondary only for chrome, facts, or glossary; never dual educational judgement |
| **Future governance implications** | New features must declare primary in PRD / educational review |

### DG-001.2-D06 — History is context, not mentor

| Field | Decision |
|-------|----------|
| **Authority owner** | System + Kwalitec primary; Study Sensei secondary bridges only |
| **Educational rationale** | Protects ED-05 — stats must not become alternate epistemology |
| **Student expectation** | Numbers orient; meaning lives in Journal / Timeline |
| **Implementation implications** | History copy must not claim mentor narrative; bridges to Sensei memory allowed |
| **Future governance implications** | Learning Insights soft Twin speech remains Sensei-adjacent; not History-as-tutor |

### DG-001.2-D07 — Feature flags and ops never Sensei

| Field | Decision |
|-------|----------|
| **Authority owner** | Kwalitec (+ System) |
| **Educational rationale** | Engineering and commercial state are not teaching |
| **Student expectation** | Gated capability honesty comes from the product |
| **Implementation implications** | Flag messaging, maintenance, outages → KW/SY; Sensei forbidden |
| **Future governance implications** | Before enabling Runtime C, replace “system chose” with Sensei explanation (ED-11) |

### DG-001.2-D08 — Notifications split envelope / body

| Field | Decision |
|-------|----------|
| **Authority owner** | KW envelope; SS educational body (when content is guidance) |
| **Educational rationale** | Delivery is product; guidance content remains mentor |
| **Student expectation** | A Mission reminder still feels like Sensei guidance, not marketing |
| **Implementation implications** | Future notification programmes must tag payload authority |
| **Future governance implications** | Marketing notifications stay KW-only; never SS |

### DG-001.2-D09 — Session practice vs Mission focus

| Field | Decision |
|-------|----------|
| **Authority owner** | Study Sensei for framing; System for workflow status |
| **Educational rationale** | Aligns DG-001.1 Mission ≠ Session; Session does not become second daily focus authority |
| **Student expectation** | Practice is what I do; Mission is what deserves attention |
| **Implementation implications** | Session CTAs remain practice language; Mission labels remain focus language |
| **Future governance implications** | Lexicon DEP-02 remains binding |

### DG-001.2-D10 — Help teaches vocabulary; Sensei owns meaning in use

| Field | Decision |
|-------|----------|
| **Authority owner** | Kwalitec primary on Help; Sensei terms defined, not performed |
| **Educational rationale** | Orientation lag (ED-04) closes by glossary + handoff, not by making Help a tutor |
| **Student expectation** | Help explains what Journal / Timeline / MI are; using them feels like Sensei |
| **Implementation implications** | Future Help programme: Sensei glossary + first-introduction map (DG-001.1-D04) |
| **Future governance implications** | Reflection student map lives in Help as KW teaching SS vocabulary |

---

## Decision index (quick)

| ID | Title |
|----|-------|
| DG-001.2-D01 | Sole educational judgement → Study Sensei |
| DG-001.2-D02 | Product / ops → Kwalitec |
| DG-001.2-D03 | Facts → System |
| DG-001.2-D04 | Mandatory KW → SS handoff |
| DG-001.2-D05 | Exactly one primary per interaction |
| DG-001.2-D06 | History = context, not mentor |
| DG-001.2-D07 | Flags / ops never Sensei |
| DG-001.2-D08 | Notifications envelope/body split |
| DG-001.2-D09 | Session practice under Sensei framing |
| DG-001.2-D10 | Help teaches; Sensei performs |

---

## How to use this matrix

1. Look up the capability before writing or reviewing copy.  
2. Obey primary / secondary / boundary columns literally.  
3. Cite decision IDs (D01–D10) in remediation programmes.  
4. If a capability is missing, propose a Board amendment — do not invent a speaker.

---

**End of AUTHORITY_DECISION_MATRIX**

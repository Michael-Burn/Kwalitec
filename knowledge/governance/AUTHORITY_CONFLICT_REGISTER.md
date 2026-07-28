# Authority Conflict Register

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.2 — Educational Authority Model  
**Version:** 1.0  
**Status:** Active — governance register (observations + Board resolutions)  
**Effective:** 2026-07-28  
**Authority:** `EDUCATIONAL_AUTHORITY_MODEL.md`  
**Upstream:** RP-001.5 Educational Drift Register; RP-001 Educational Consistency Audit; DG-001.1  
**Companions:** `AUTHORITY_TRANSITION_MAP.md`, `AUTHORITY_DECISION_MATRIX.md`

---

## Purpose

Identify and classify educational **authority** defects:

- competing authorities
- duplicated authority
- authority overlap
- authority gaps
- hidden authority transitions
- inappropriate authority ownership

This register converts RP-001 observations into DG-001.2 governance status. It does **not** implement copy or product changes.

Severity: **Critical / High / Medium / Low**  
Likelihood: **Likely / Possible / Unlikely** (Alpha cohort misunderstanding)  
Status: **Resolved (governance)** / **Open (implementation)** / **Contained**

---

## Summary table

| ID | Conflict | Type | Severity | Likelihood | Governance | Implementation |
|----|----------|------|----------|------------|------------|----------------|
| AC-01 | Dual narrator KW vs SS without handoff | Competing / gap | High | Likely | **Resolved** D01/D02/D04 | **Closed** RR-001.3A (T04); Help closed RR-001.3B (AC-04) |
| AC-02 | “The system / algorithm” as mentor substitute | Inappropriate ownership | High | Possible (High if Runtime C ON) | **Resolved** D01/D03/D07 | **Closed** Runtime C rename RR-001.3A; flag Contained OFF |
| AC-03 | History stats vs Timeline narrative | Competing epistemology | Medium | Possible | **Resolved** D06 | **Closed** RR-001.3C (ED-05 copy) |
| AC-04 | Help / Onboarding teach KW; memory teaches SS | Hidden transition / gap | High | Likely | **Resolved** D04/D10 | **Closed** — onboarding RR-001.3A; Help RR-001.3B |
| AC-05 | Home educational speech often unnamed | Hidden attribution | Medium | Likely | **Resolved** D01/D05; density OQ | **Closed** RR-001.3D OQ-02 policy |
| AC-06 | Mission / Session / tip noun storm as false multi-authority | Duplicated concept → felt authority | High | Likely | Lexicon DG-001.1; authority D09 | **Closed** tip empties RR-001.3C; density RR-001.3D |
| AC-07 | Reflection family without map | Fragmented judgement practice | High | Likely | DG-001.3 map | **Closed** RR-001.3B |
| AC-08 | Revision vs Mission competing focus | Overlap | Medium | Possible | D09 + Mission primacy | **Closed** RR-001.3D (ED-13) |
| AC-09 | MI + MES hero duplication | Authority noise | Medium | Possible | D05 | Mitigated disclosure (RR-001.2); watch |
| AC-10 | Feature-flag / gated copy in mentor voice | Inappropriate ownership | Medium | Possible | **Resolved** D07 | Open if any Sensei-flag copy remains |
| AC-11 | Error / outage as Sensei theatre | Inappropriate ownership | Medium | Possible | **Resolved** D03/D07 | Audit residual |
| AC-12 | Settings / Profile learning recommendations | Inappropriate ownership | Medium | Unlikely | **Resolved** D02 | Prevent in future features |
| AC-13 | Notifications marketing as Sensei | Overlap / inappropriate | Medium | Possible | **Resolved** D08 | Open until notification programme |
| AC-14 | Study Plan pacing advice unsigned | Gap / overlap | Low | Possible | Matrix: KW structure; SS if advising | Clarify in copy programmes |
| AC-15 | Success states mixing account praise with educational judgement | Overlap | Low | Possible | Matrix success rows | **Closed** RR-001.3D |
| AC-16 | Journal empty mentions gated QC while OFF | Flag honesty / KW duty | Low | Possible | D07 | **Closed** RR-001.3C |
| AC-17 | Latent MissionOptimizer as mission-shaped authority | Competing decision narration risk | High if surfaced | Unlikely (unrendered) | D01; cores remain singular | Contained (EGI quarantine residual) |

---

## Conflict types (definitions)

| Type | Meaning |
|------|---------|
| Competing authorities | Two speakers claim the same educational role |
| Duplicated authority | Same role expressed under multiple names/surfaces |
| Authority overlap | Domains bleed without clear primary |
| Authority gap | No intentional speaker / missing handoff |
| Hidden authority transition | Speaker changes without student-visible signal |
| Inappropriate authority ownership | Wrong speaker for the domain |

---

## Conflict detail

### AC-01 — Dual narrator without handoff

| Field | Detail |
|-------|--------|
| **Type** | Competing narrative authority; handoff gap |
| **Surfaces** | Onboarding, Help, Auth (KW) vs Journal, Timeline, MI, Feedback Loop (SS); Home often unnamed |
| **Educational risk** | No single mentor relationship; guidance feels modular |
| **RP link** | ED-01 / IR-01 |
| **Board resolution** | D01 + D02 + D04 — KW orients; SS owns educational speech; mandatory T04 |
| **Implementation residual** | Insert handoff sentence; remove KW-as-mentor on Sensei surfaces (DEP-16) |
| **Status** | Governance resolved; copy open |

### AC-02 — System-as-mentor

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership |
| **Surfaces** | Runtime C “Why the system chose this”; any “algorithm decided” copy |
| **Educational risk** | Robotic authority replaces Sensei; trust fracture |
| **RP link** | ED-11 / DEP-04 |
| **Board resolution** | D01 + D03 — System never recommends; Sensei explains authorised decisions |
| **Implementation residual** | Rename before any Runtime C enable |
| **Status** | Contained while OFF; governance forbids enable-as-is |

### AC-03 — History vs Timeline epistemology

| Field | Detail |
|-------|--------|
| **Type** | Competing authority (felt) |
| **Surfaces** | History stats panels vs Timeline “not from scores” |
| **Educational risk** | Students treat numbers as the learning story |
| **RP link** | ED-05 |
| **Board resolution** | D06 — History = SY+KW context; SS bridges only; meaning in Journal/Timeline |
| **Implementation residual** | Copy programme: bridge language; no mentor claims on stats |
| **Status** | **Closed** — History bridge + Help FAQ RR-001.3C |

### AC-04 — Orientation lag / hidden handoff

| Field | Detail |
|-------|--------|
| **Type** | Hidden transition; authority gap |
| **Surfaces** | Help / Onboarding omit Sensei memory surfaces and never introduce SS |
| **Educational risk** | Student meets Sensei mid-journey without introduction |
| **RP link** | ED-01, ED-04 |
| **Board resolution** | D04 + D10 + DG-001.1-D04 first-introduction ownership |
| **Implementation residual** | Onboarding T04 + Help glossary |
| **Status** | **Closed** — onboarding RR-001.3A; Help journey/glossary/handoff RR-001.3B |

### AC-05 — Unnamed Home authority

| Field | Detail |
|-------|--------|
| **Type** | Hidden attribution |
| **Surfaces** | Home hero calm guidance without naming Sensei |
| **Educational risk** | Authority is correct in law but invisible to student |
| **RP link** | ED-01 partial; Voice Guide Alpha finding |
| **Board resolution** | D01 owns speech; naming density remains DG-001.1 OQ-02 |
| **Implementation residual** | Prefer Sensei named once nearby Home educational hero |
| **Status** | Ownership clear; naming density open |

### AC-06 — Daily-focus noun storm

| Field | Detail |
|-------|--------|
| **Type** | Duplicated concept felt as multi-authority |
| **Surfaces** | Mission / Session / tip / Recommendation labels |
| **Educational risk** | “Who is telling me what to do?” becomes “which widget?” |
| **RP link** | ED-02 |
| **Board resolution** | DG-001.1 lexicon + D09 (Session under Sensei framing, not second focus authority) |
| **Implementation residual** | Tip retirement; Mission-led Home |
| **Status** | Vocabulary + authority law set; copy open |

### AC-07 — Reflection multiplicity

| Field | Detail |
|-------|--------|
| **Type** | Overlap / student map gap |
| **Surfaces** | Session, Commitment, Sensei, Timeline, Guided preview, Check-in |
| **Educational risk** | Reflection loses meaning; unclear who owns calibration |
| **RP link** | ED-03 |
| **Board resolution** | DG-001.1 reflection family; Sensei reflection → SS; Help map → KW teaching (D10) |
| **Implementation residual** | Student-visible map in Help |
| **Status** | **Closed** — Help + onboarding map; Check-in rename (RR-001.3B) |

### AC-08 — Revision vs Mission

| Field | Detail |
|-------|--------|
| **Type** | Authority overlap (focus) |
| **Surfaces** | Revision vs Home Mission |
| **Educational risk** | Two “what today?” feelings |
| **RP link** | ED-13 |
| **Board resolution** | Mission remains authorised daily focus; Revision is SS-owned review work, not second Mission |
| **Implementation residual** | Disclosure copy when both visible |
| **Status** | **Closed** — Revision Mission primacy disclosure (RR-001.3D) |

### AC-09 — MI + MES hero duplication

| Field | Detail |
|-------|--------|
| **Type** | Authority noise |
| **Surfaces** | Home Mission Intelligence + MES hero |
| **Educational risk** | Two briefs feel like two speakers |
| **RP link** | ED-10 |
| **Board resolution** | D05 one primary; compose as one Sensei educational moment |
| **Implementation residual** | Watch post RR-001.2 disclosure |
| **Status** | Mitigated; monitor |

### AC-10 — Feature flags in mentor voice

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership |
| **Surfaces** | Any gated-capability explanation attributed to Sensei |
| **Educational risk** | Mentor discusses engineering |
| **Board resolution** | D07 — KW (+ SY) only |
| **Implementation residual** | Audit remaining strings |
| **Status** | Law set |

### AC-11 — Sensei error theatre

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership |
| **Surfaces** | Outage / 500 / CSRF dressed as mentor apology |
| **Educational risk** | Mentor becomes ops; trust confusion |
| **Board resolution** | D03 + recovery KW |
| **Implementation residual** | Keep mechanical errors neutral |
| **Status** | Law set |

### AC-12 — Control-plane educational judgement

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership |
| **Surfaces** | Settings / Profile recommending what to study |
| **Educational risk** | Second tutor in preferences |
| **Board resolution** | D02 — KW only for controls; judgement → SS surfaces |
| **Implementation residual** | Prevent in future features |
| **Status** | Law set |

### AC-13 — Notification envelope confusion

| Field | Detail |
|-------|--------|
| **Type** | Overlap |
| **Surfaces** | Push / email / in-app notifications |
| **Educational risk** | Marketing feels like mentor; or mentor feels like spam |
| **Board resolution** | D08 — KW envelope; SS educational body; marketing KW-only |
| **Implementation residual** | Tag authority in notification programmes |
| **Status** | Law set; programme open |

### AC-14 — Study Plan unsigned advice

| Field | Detail |
|-------|--------|
| **Type** | Gap / overlap |
| **Surfaces** | Study Plan pacing hints |
| **Educational risk** | Unclear whether product structure or mentor advice |
| **Board resolution** | Matrix — KW owns structure; SS if educationally advising |
| **Implementation residual** | Attribute advice explicitly when present |
| **Status** | Law set |

### AC-15 — Mixed success states

| Field | Detail |
|-------|--------|
| **Type** | Overlap |
| **Surfaces** | Account save success vs Mission complete success |
| **Educational risk** | Product confirmation read as educational praise (or reverse) |
| **Board resolution** | Success rows in matrix — domain of completed action |
| **Implementation residual** | Keep domains separate |
| **Status** | **Closed** — Session/assessment success honesty (RR-001.3D) |

| Field | Detail |
|-------|--------|
| **Type** | Flag honesty (KW duty leaking into SS empty) |
| **Surfaces** | Journal empty mentioning Quick Check while OFF |
| **Educational risk** | Mentor promises unavailable product state |
| **RP link** | ED-14 |
| **Board resolution** | D07 — gated honesty is KW; Sensei empties must not advertise OFF capabilities |
| **Implementation residual** | Remove or gate-honest copy |
| **Status** | Law set; copy open |

### AC-17 — Latent dual mission generator

| Field | Detail |
|-------|--------|
| **Type** | Competing decision narration risk |
| **Surfaces** | MissionOptimizer (unrendered) vs Learning Mode / MI |
| **Educational risk** | Future template rewire could revive dual Mission authority |
| **Upstream** | EGI Educational Governance Recertification GAP residual |
| **Board resolution** | D01 — Sensei narrates sole authorised Mission path; quarantine latent generators |
| **Implementation residual** | EIP-V1-QUARANTINE direction remains |
| **Status** | Contained |

---

## Gaps closed by this package (governance)

| Gap | Closure |
|-----|---------|
| No explicit three-authority model | `EDUCATIONAL_AUTHORITY_MODEL.md` |
| No transition law | `AUTHORITY_TRANSITION_MAP.md` |
| No per-capability primary | `AUTHORITY_DECISION_MATRIX.md` |
| ED-01 ownership ambiguity | D01/D02/D04 |
| System vs Sensei vs KW domain bleed | D01–D03, D07 |

## Gaps remaining (implementation / later governance)

| Gap | Owner |
|-----|-------|
| Live dual-narrator copy | Future copy programme citing DG-001.2 |
| Home naming density | DG-001.1 OQ-02 — **Closed** RR-001.3D |
| Help Sensei glossary + reflection map | Copy + D10 |
| Runtime C rename before enable | Engineering + educational review |
| Notification authority tagging | Future notification programme |
| History epistemology copy | ED-05 remediation |

---

## Board reading rule

When a new conflict appears:

1. Classify type.  
2. Assign primary from the Authority Model — do not create a fourth speaker.  
3. Log here with ID `AC-XX`.  
4. Link to decision ID or raise Outstanding Governance Question.  
5. Do not “fix in prose” by letting KW and SS both judge the same learning action.

---

**End of AUTHORITY_CONFLICT_REGISTER**

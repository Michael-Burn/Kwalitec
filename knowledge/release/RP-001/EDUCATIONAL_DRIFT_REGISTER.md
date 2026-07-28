# RP-001.5 — Educational Drift Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.5 — Educational Consistency Certification  
**Date:** 2026-07-28  
**Status:** Active for Alpha educational-consistency residual tracking  
**Companions:** `EDUCATIONAL_CONSISTENCY_AUDIT.md`, `LEARNING_MODEL_MAP.md`  
**Related prior registers:** `IDENTITY_RISK_REGISTER.md` (RP-001.3), `JOURNEY_RISK_REGISTER.md`, `ALPHA_REMEDIATION_REGISTER.md` (RR-001)

---

## Purpose

Catalogue every observed **educational inconsistency, authority conflict, and philosophy drift** across Alpha educational capabilities. No mitigations implemented in this package.

Severity: **Critical / High / Medium / Low**.  
Likelihood: **Likely / Possible / Unlikely** for Alpha cohort misunderstanding.

---

## Drift summary

| ID | Title | Type | Severity | Likelihood | Status |
|----|-------|------|----------|------------|--------|
| ED-01 | Dual narrator (Kwalitec vs Study Sensei) | Authority / identity | High | Likely | Open (maps IR-01 / RR-H11) |
| ED-02 | Mission / Session / tip / recommendation noun storm | Terminology | High | Likely | Open (IR-02) |
| ED-03 | Multiple reflection systems without student map | Duplicate concept | High | Likely | Partially mitigated (RR-001.1 honesty; map open) |
| ED-04 | Help / onboarding omit Sensei memory surfaces | Orientation drift | High | Likely | Open (IR-06 / IR-07) |
| ED-05 | History stats vs Timeline “not from scores” | Competing epistemology | Medium | Possible | Open |
| ED-06 | Commitment continuity says “tip” | Terminology | Medium | Likely | Open |
| ED-07 | Explanation eyebrow “Why this tip?” | Terminology / tone | Medium | Possible | Open (IR-08) |
| ED-08 | Help “closest to being tested on” | Anxiety / tone drift | Medium | Possible | Open (IR-11) |
| ED-09 | Home Guided Reflection looks interactive | Trust residual | Medium | Possible | Mitigated — disclaimer (RR-001.1) |
| ED-10 | MI + MES hero duplication | Cognitive / authority noise | Medium | Possible | Mitigated by disclosure (RR-001.2) |
| ED-11 | Runtime C “Why the system chose this” | Competing authority | High if ON | Unlikely (OFF) | Contained |
| ED-12 | Empty-state phrasing fragmentation | Consistency | Medium | Possible | Improved (RR-001.2) |
| ED-13 | Revision vs one primary mission | Competing focus | Medium | Possible | Open (thin Alpha) |
| ED-14 | Journal empty mentions Quick Check while QC OFF | Flag honesty | Low | Possible | Open (IR-14) |
| ED-15 | “Optimising for {axis}” on Home | Engineering tone | Low | Possible | Open (IR-18) |
| ED-16 | Session completion “Exam readiness” label | Confidence framing | Medium | Possible | Open |
| ED-17 | Tutor explain as alternate narrator | Authority (soft path) | Low | Unlikely | Soft-fail / COND |
| ED-18 | Product Check-in mistaken for educational reflection | Duplicate concept | Low | Possible | Open (disclose) |
| ED-19 | No cohort educational-philosophy validation | Process | High | Certain | Open (audit-only) |
| ED-20 | Onboarding “reasons Kwalitec used” vs Sensei guidance | Authority handoff | Medium | Likely | Open |

---

## Cross-system categories

### Contradictory advice

| ID | Tension | Surfaces | Educational effect |
|----|---------|----------|--------------------|
| ED-05 | Timeline: learning story “not from scores” vs Help History: “accuracy over time” | Timeline · Help · History | Students may think scores *are* the Sensei’s truth |
| ED-08 | Calm Sensei vs test-anxiety adjacency in Help | Help FAQ vs MI/Journal | Undermines anxiety-safe professional tone |
| ED-13 | One primary mission vs “Today's best revision” as parallel focus | Home · Revision | Competing “what matters today” |

### Duplicate educational concepts

| ID | Concept cluster | Instances |
|----|-----------------|-----------|
| ED-02 | Daily focus | Mission · Session · Recommendation · Mission tip · tip |
| ED-03 | Reflection | Home preview · Commitment ack · Session reflection · ILE-005 · Help FAQ · (Check-in false cousin) |
| — | Progress story | Journey · Educational Timeline · History · Home learning journey |
| — | Readiness | Exam Readiness card · session metric · Help FAQ · MI confidence |

### Conflicting terminology

Documented in detail in RP-001.3 `TERMINOLOGY_REGISTER.md`. Educational-consistency impact: **same philosophy, fractured labels** → student cannot transfer learning across surfaces.

### Competing educational authority

| Authority claim | Surfaces | Status |
|-----------------|----------|--------|
| Study Sensei | Journal · Timeline · MI silence · Feedback Loop | Canonical for guidance memory |
| Kwalitec product | Onboarding · Help · Auth · Welcome | Product brand — not second tutor, but second *teacher voice* |
| Unnamed calm guidance | Home hero · Commitment · Session | Missing Sensei attribution |
| History statistics | History page | Soft alternate epistemology |
| “the system” | Runtime C panel | Contained OFF |
| Tutor explain | Conditional Home POST | Explains authorised decisions — lawful if soft-fail |

### Competing learning models

| Model | Present on default Alpha? | Notes |
|-------|---------------------------|-------|
| Evidence → Sensei guidance → practice → reflection | **Yes** — primary | Coherent |
| Content library / question bank as identity | No | Pass |
| Engagement / streak optimisation | No on EOS cores | Legacy residual Low (IR-13) |
| Chatbot as educational brain | No | Pass |
| Dual recommendation engines presenting as two “missions” | Contained | MES + MI are composition layers, not dual selectors; Tutor does not re-rank |

### Educational drift (philosophy vs orientation)

| Drift | Description |
|-------|-------------|
| Narrator drift | First sessions teach “Kwalitec prepares”; later memory teaches “Study Sensei remembers” without handoff |
| Noun drift | PX Session lexicon vs ILE Mission lexicon vs tip slang |
| Reflection drift | Reflection taught as session close in onboarding; Sensei calibration appears later without map |
| Epistemology drift | Narrative evidence culture (Timeline) coexists with accuracy/stats culture (Help/History) without reconciliation copy |

---

## Risk records (detail)

### ED-01 — Dual narrator (Kwalitec vs Study Sensei)

| Field | Detail |
|-------|--------|
| **Description** | Orientation and support speak as Kwalitec; memory and silence speak as Study Sensei; Home often unnamed. |
| **Educational risk** | No single mentor relationship; guidance feels modular. |
| **Authority risk** | Competing narrative authority without competing decision engine. |
| **Evidence** | `alpha_onboarding_service.py`; Journal/Timeline DTOs; Help; MI compose empty. |
| **Mitigation direction** | One onboarding sentence: Study Sensei is how Kwalitec guides daily decisions; Help glossary. |
| **Status** | Open |

### ED-02 — Mission / Session / tip / recommendation noun storm

| Field | Detail |
|-------|--------|
| **Description** | Same daily focus named five ways across Home, Session, Help, explanation card, commitment, Journal empty. |
| **Educational risk** | Breaks “one focus today” mental model across commitment → practice → memory. |
| **Evidence** | TERMINOLOGY_REGISTER §2; PX-002A vs ILE-004 conflict. |
| **Mitigation direction** | Board noun decision; alias in Help/onboarding; retire “tip” as primary. |
| **Status** | Open |

### ED-03 — Multiple reflection systems without map

| Field | Detail |
|-------|--------|
| **Description** | Five+ reflection concepts; different persistence and voice. |
| **Educational risk** | Reflection becomes “another form,” not professional judgement practice. |
| **Mitigation progress** | RR-001.1 removed false Home submit affordances; preview honesty present. |
| **Remaining** | Student-facing map (purpose · optional · recorded?). |
| **Status** | Partially mitigated |

### ED-04 — Help / onboarding omit Sensei memory surfaces

| Field | Detail |
|-------|--------|
| **Description** | FAQ/orientation cover Session, Readiness, session reflection — not Journal, Timeline, Mission Intelligence, Feedback Loop. |
| **Educational risk** | Students never learn where long-term mastery story lives. |
| **Status** | Open |

### ED-05 — History stats vs Timeline not-from-scores

| Field | Detail |
|-------|--------|
| **Description** | Epistemological tension between accuracy/progress stats and qualitative Sensei narrative. |
| **Educational risk** | Students privilege numbers over educational meaning. |
| **Mitigation direction** | History intro: stats are context; Journal/Timeline are Sensei meaning. |
| **Status** | Open |

### ED-09 — Guided Reflection preview residual

| Field | Detail |
|-------|--------|
| **Description** | Choice chips / note placeholder remain after RR-001.1; honesty disclaimer states nothing recorded. |
| **Educational risk** | Residual confusion with real reflection paths (not Critical trust fail). |
| **Status** | Mitigated (honesty); map still needed (ED-03) |

### ED-11 — Runtime C “the system”

| Field | Detail |
|-------|--------|
| **Description** | Flag-gated panel attributes choice to “the system.” |
| **Educational risk** | Replaces Sensei with robotic agent if enabled. |
| **Status** | Contained — must rename before enablement |

---

## Resolved / contained (baseline for this certification)

| Prior ID | Resolution | Effect on RP-001.5 |
|----------|------------|--------------------|
| IR-03 / JR-06 / RR-C02 | False reflection controls removed | No Critical trust Fail in reflection |
| JR-01 / RR-C01 | Commitment completion wired on V2 finish | Learning chain practice → reflection restored |
| XR-04 / XR-17 (RR-001.2) | Empty/success presentation patterns | Empty/success philosophy clearer |

---

## Highest educational risks (priority order)

1. **ED-01** Dual narrator  
2. **ED-02** Daily-focus noun storm  
3. **ED-03** Reflection map  
4. **ED-04** Orientation lag vs ILE memory  
5. **ED-05** Stats vs narrative epistemology  

---

## End of EDUCATIONAL_DRIFT_REGISTER

# DG-001.1 — Completion Report

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.1 — Canonical Educational Lexicon  
**Date:** 2026-07-28  
**Commit message (mandated):** `docs(dg-001.1): establish canonical educational lexicon`  
**Constraint compliance:** Governance only — no templates, UI, architecture, educational behaviour, recommendations, Mission Intelligence, feature flags, or curriculum modified.

---

## Executive Summary

DG-001.1 establishes the **single authoritative educational vocabulary** for Kwalitec. It converts RP-001.3 / RP-001.5 terminology observations (ED-01–ED-04) into Board decisions: one Study Sensei narrator vs Kwalitec product brand; **Mission-led** daily educational focus with Session as distinct practice workflow; a reflection family map; and explicit deprecation of tip and other synonym collisions.

**Overall governance decision:** Educational language is Mission-led and Sensei-narrated; product OS language remains distinct; deprecated synonyms are registered for future remediation. No student-facing behaviour changed in this package.

---

## Educational Terms Audited

| Metric | Count |
|--------|------:|
| Canonical lexicon entries | 27 |
| Reflection subtypes mapped | 6 (incl. Check-in as non-reflection) |
| Deprecation register items | 16 |
| Approximate named terms / labels reviewed | 42 |

**Categories covered**

- Narrator / brand (Study Sensei, Kwalitec)  
- Daily focus (Mission, Session, Recommendation, Guidance, tip)  
- Reflection family  
- Memory / archive (Decision Journal, Educational Timeline, History)  
- Planning / position (Study Plan, Journey, Home, Calibration)  
- Honesty grammar (Evidence, Confidence, Uncertainty, Readiness, Progress, Mastery)  
- Practice / review (Session, Revision, Mission Commitment)  
- Assessment (Quick Check / AA)  
- Intelligence surfaces (Daily Mission Intelligence, Learning Insights, Feedback Loop)

**Coverage sources**

Product documentation · Educational Philosophy · ILE-001–005 / ILE-010 · PX-002A / Product Language Guide · Ubiquitous Language · MICROCOPY / Voice Guide · RP-001.3 Terminology Register · RP-001.5 Drift Register · Home / Session / Journal / Timeline / Mission Intelligence / Recommendation explanation surfaces (as documented in RP-001 audits)

---

## Canonical Decisions

| Term | Definition (short) | Owner | Educational purpose |
|------|--------------------|-------|---------------------|
| Study Sensei | Trusted educational mentor narrator | ILE-010 / ILE-001C0 | One mentor relationship |
| Kwalitec | Product / company brand | Vision / brand | Distinct from mentor |
| Mission | Authorised primary educational focus | ILE-004 | One focus today |
| Session | Focused practice workflow | PX / Session | Deliberate practice container |
| Recommendation | Authorised explainable next-action suggestion | P-001.3 / cores | Inspectable decision object |
| Guidance | Umbrella educational speech | ILE-001C0 | Generic Sensei direction |
| Decision Journal | Persistent educational memory | ILE-002 | Continuity and trust |
| Educational Timeline | Narrative interpretation of Journal | ILE-003 | Long-term learning story |
| Educational Feedback Loop | Sensei guidance calibration capability | ILE-005 | Improve usefulness honesty |
| Study Plan | Exam-date syllabus plan | Study Plan | Pacing spine |
| Calibration | Declared coverage (≠ mastery) | Calibration | Honest cold start |
| Confidence | Certainty of a claim / estimate (disambiguated) | UL / MI / ILE-001 | Match strength to evidence |
| Readiness | Estimated exam preparedness | Readiness / PX | On-track signal |
| Progress | Movement through plan/practice | Journey / History | Orient without false mastery |
| Mastery | Twin probabilistic estimate | UL / Constitution | Evidence-based understanding |
| Revision | Evidence-timed review work | Philosophy / PX | Protect fragile knowledge |
| History | Study archive + stats context | PX | Context, not Sensei narrative |
| Evidence | Observable signals justifying guidance | Evidence model | Ground every claim |
| Uncertainty | Provisional honesty when evidence thin | ILE-001C0 | Protect trust |
| Daily Mission Intelligence | Compose one Mission brief | ILE-004 | Answer what today |
| Mission Commitment | Accept / defer with agency | Commitment lineage | Deliberate choice |
| Journey | Syllabus progress surface | PX | Curriculum position |
| Home | Student landing | PX | What now |
| Quick Check | Anxiety-safe AA session type | ILE-001 | Evidence without exam chrome |
| Learning Insights | Explainable readiness/progress summaries | Product Language | Soft Twin speech |

**Board decisions logged**

- **DG-001.1-D01** — Study Sensei is how Kwalitec guides daily learning decisions (ED-01).  
- **DG-001.1-D02** — Mission-led educational focus; Session is practice, not a Mission synonym (ED-02).  
- **DG-001.1-D03** — Reflection is a qualified family with an explicit student map (ED-03).  
- **DG-001.1-D04** — First-introduction and Help ownership for Journal / Timeline / Mission Intelligence vocabulary (ED-04 direction).

Full definitions: `knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md`.

---

## Deprecated Terms

| ID | Terms | Reason | Migration |
|----|-------|--------|-----------|
| DEP-01 | tip / Mission tip / Why this tip? | Noun storm | Mission / Guidance / Recommendation by role |
| DEP-02 | Today's Session as Mission synonym | Concept collision | Today's Mission (focus); Session (practice CTA) |
| DEP-03 | Today's Recommendation as hero focus | Third synonym | Mission hero; recommendation for decision object |
| DEP-04 | the system / algorithm / engine | Robotic narrator | Study Sensei / Why this Mission? |
| DEP-05–11 | Dashboard, Analytics (learner), Archive primary, Learning Session required label, Roadmap family, Twin/Mastery Score labels, Remediation/Intervention | PX / engine / deficit language | Home, History, Journey, Session, Learning Insights, Revision |
| DEP-12 | AA Exam/Test/Pass/Fail/Weak… | Anxiety-safe law | Check framing |
| DEP-13 | Streak guilt / FOMO / destiny pass | Engagement theatre | Consistency / estimated readiness |
| DEP-14 | mastered (History identity) | False mastery badge | Completed topics |
| DEP-15 | Check-in as reflection | False cousin | Product Check-in |
| DEP-16 | Kwalitec-as-mentor on Sensei surfaces | Dual narrator | Study Sensei on memory/guidance |

Full register: `knowledge/governance/TERM_DEPRECATION_REGISTER.md`.

---

## Outstanding Governance Questions

| ID | Question | Notes |
|----|----------|-------|
| OQ-01 | Exact PX / `product_language.py` reconciliation sequence | Lexicon supersedes educational meaning; implementation programme must update PX docs/tests without breaking Session CTAs |
| OQ-02 | Whether Home must *always* name Study Sensei in-chrome | D01 requires onboarding handoff; continuous naming density open |
| OQ-03 | Student-visible name for Educational Feedback Loop | Prefer invisible + Journal optional reflection; Help glossary depth TBD |
| OQ-04 | Mastery student-facing exposure policy | Soft wording preferred; full ban vs limited use still open for Journey/Insights |
| OQ-05 | Revision vs Mission competition disclosure copy | ED-13 educational risk — copy programme, not lexicon blocker |
| OQ-06 | Exam Readiness vs AA “no Exam” tension in Help | Soften anxiety phrasing; planning term retained |

None of these block DG-001.1 lexicon completeness; they block later *implementation* claims of full ED-01–ED-04 closure.

---

## Certification Decision

**Conditional Pass**

**Rationale:** The Board can recreate a consistent educational vocabulary from the four governance documents. Core conflicts ED-01–ED-04 have governance resolutions (D01–D04). Unqualified Pass for *student-facing consistency* remains blocked until a future copy/implementation programme applies the lexicon (PX reconciliation, tip retirement, Help/onboarding map). This package correctly does not implement those changes.

---

## Decision Log

| When | Decision | Outcome |
|------|----------|---------|
| 2026-07-28 | Open DG-001.1 from RP-001.3 / RP-001.5 residuals | Governance package authorised |
| 2026-07-28 | Audit terms across product, ILE, PX, UL, RP registers | 42 terms/labels reviewed |
| 2026-07-28 | **DG-001.1-D01** Narrator split | Study Sensei educational; Kwalitec product |
| 2026-07-28 | **DG-001.1-D02** Mission-led focus | Mission ≠ Session ≠ Recommendation; tip deprecated |
| 2026-07-28 | **DG-001.1-D03** Reflection family | Qualified map; Check-in excluded |
| 2026-07-28 | **DG-001.1-D04** Orientation ownership | First-introduction points for Journal / Timeline / MI |
| 2026-07-28 | Publish lexicon + map + deprecation + style guide | Active vocabulary law |
| 2026-07-28 | Certification | Conditional Pass — governance complete; implementation pending |

---

## Summary

**What was achieved**

Four permanent educational vocabulary authorities plus this completion report. Board decisions resolve the largest educational-lexicon risks identified in Alpha certification without touching application code.

**Why it matters**

Professional learners should never wonder whether two educational words mean the same thing. Future remediation can converge copy against one law instead of re-debating Mission vs Session vs tip on every surface.

**How future implementation should use these documents**

1. Treat `CANONICAL_EDUCATIONAL_LEXICON.md` as naming law.  
2. Place terms using `EDUCATIONAL_VOCABULARY_MAP.md`.  
3. Refuse deprecated strings via `TERM_DEPRECATION_REGISTER.md`.  
4. Write tone with `EDUCATIONAL_LANGUAGE_STYLE_GUIDE.md`.  
5. Cite DG-001.1 in any programme remediating ED-01–ED-04.

---

## Files Created

- `knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md`
- `knowledge/governance/EDUCATIONAL_VOCABULARY_MAP.md`
- `knowledge/governance/TERM_DEPRECATION_REGISTER.md`
- `knowledge/governance/EDUCATIONAL_LANGUAGE_STYLE_GUIDE.md`
- `knowledge/governance/DG001_1_COMPLETION_REPORT.md`

---

## Files Modified

None.

---

## Tests Executed

None.

Governance package.

---

## Migration Impact

None.

---

## Architecture Compliance

- No architecture changes.  
- No educational behaviour changes.  
- No recommendation changes.  
- No curriculum changes.  
- No feature-flag changes.  
- Curriculum V1/V2 traversal/import compatibility: **N/A** (unchanged).  
- Layering preserved: documentation under `knowledge/governance/` only.

---

## Technical Debt

- PX-002A / Product Language Guide still reject “Today's Mission” while ILE-004 and this lexicon require it for educational focus — **documented conflict pending implementation reconciliation (OQ-01)**.  
- Live templates still contain tip / dual-narrator / reflection multiplicity — governance resolved, product not yet updated.  
- ED-05 epistemology (History stats vs Timeline) guided but not copy-closed.  
- Outstanding questions OQ-02–OQ-06 remain for later Board/copy programmes.

---

## Known Limitations

- Assumes RP-001.3 / RP-001.5 audits remain accurate observations of Alpha surfaces as of 2026-07-28.  
- Does not validate cohort understanding of the new vocabulary (no student testing).  
- Does not amend `UBIQUITOUS_LANGUAGE.md` or PX files in this package (additive governance authority).  
- Success criterion is *governance recreatability*, not *production string convergence*.

---

## Student Impact Assessment

Governance only.

No student-facing changes.

| Field | Value |
|---|---|
| **Programme / Milestone ID** | DG-001.1 |
| **Title** | Canonical Educational Lexicon |
| **Date** | 2026-07-28 |
| **Student-visible change?** | No |
| **Production activation?** | None |
| **Related KSI categories** | None directly (enables future K1/K8 copy coherence) |

### 1. Student problem

Students encounter Mission / Session / tip / Recommendation and Kwalitec vs Study Sensei without a single vocabulary law (ED-01–ED-04). This package does not yet change what students see.

**Evidence:** RP-001.3 Terminology Register; RP-001.5 Educational Drift Register.

### 2. Student benefit

Indirect: future copy programmes can converge language so learners stop guessing whether words mean the same thing.

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A (governance) | Future Mission-led copy |
| How am I progressing? | N/A | Future Journal/Timeline orientation |
| What is stopping me? | N/A | — |
| What happens next? | N/A | — |

**Final Test:** Does this help students become better professionals? **Indirectly** — only after implementation uses this lexicon.

### 3. Learning benefit

No immediate learning-behaviour change. Enables consistent teaching of professional learning vocabulary later.

### 4. Success metrics

Board recreatability criterion (below). No KSI movement claimed.

### 5. Risks

Over-claiming student-facing consistency before ED-01–ED-04 copy remediation.

### 6. Assumptions

Implementation programmes will cite and obey DG-001.1; PX reconciliation will not reintroduce tip as primary noun.

Template reference: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`.

---

## Estimated KSI Contribution

**ΔKSI = 0**

Governance only. No student-visible educational usefulness change in this package.

| Category | Δ | Rationale |
|---|---|---|
| K1–K8 | 0 | Docs/governance only |

---

## Evidence collected

- `knowledge/release/RP-001/TERMINOLOGY_REGISTER.md`  
- `knowledge/release/RP-001/EDUCATIONAL_DRIFT_REGISTER.md`  
- `knowledge/release/RP-001/VOICE_GUIDE.md`  
- `knowledge/release/RP-001/LEARNING_MODEL_MAP.md`  
- `knowledge/release/RP-001/RP001_3_COMPLETION_REPORT.md`  
- `knowledge/release/RP-001/RP001_5_COMPLETION_REPORT.md`  
- `knowledge/product/ILE-001/TERMINOLOGY_STANDARD.md`  
- `knowledge/product/px002a/TERMINOLOGY_STANDARD.md`  
- `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md`  
- `knowledge/product/ILE-004/MISSION_PHILOSOPHY.md`  
- `knowledge/product/STUDY_SENSEI_PHILOSOPHY.md`  
- `knowledge/product/EDUCATIONAL_PHILOSOPHY.md`  
- `UBIQUITOUS_LANGUAGE.md` (Mission / Recommendation / Mastery / Readiness / Confidence)

---

## Lessons learned for student value

Alpha certification proved educational *behaviour* can be coherent while educational *labels* still fracture the mentor relationship. Vocabulary must be Board law before copy sprints — otherwise Mission vs Session debates recur per surface.

---

## Explainability Review

N/A — governance documentation only; no student-facing intelligence behaviour, speech, or schema changed. Future copy that renames explanation eyebrows (e.g. tip → guidance) should cite P-001.2 when those strings ship.

---

## Recommendation Quality Review

N/A — no recommendation ranking, selection, or Mission Intelligence composition changed. Lexicon clarifies Recommendation vs Mission naming only.

---

## Version 1 readiness residual

N/A for production-ready declaration. DG-001.1 does not claim Version 1 progress beyond clarifying educational vocabulary law that later release programmes may consume. Residual open gates G1–G12 unchanged.

---

## Success Criteria

> If every student-facing educational word disappeared tomorrow, could we recreate the entire educational vocabulary consistently from these governance documents?

**Yes** — from `CANONICAL_EDUCATIONAL_LEXICON.md` + `EDUCATIONAL_VOCABULARY_MAP.md` + `TERM_DEPRECATION_REGISTER.md` + `EDUCATIONAL_LANGUAGE_STYLE_GUIDE.md`.

**DG-001.1 is complete** (governance). Student-facing remediation remains future work.

---

**End of DG001_1_COMPLETION_REPORT**

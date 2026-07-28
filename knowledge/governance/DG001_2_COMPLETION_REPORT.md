# DG-001.2 — Completion Report

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.2 — Educational Authority Model  
**Date:** 2026-07-28  
**Commit message (mandated):** `docs(dg-001.2): establish educational authority model`  
**Constraint compliance:** Governance only — no templates, UI, architecture, educational behaviour, recommendations, Mission Intelligence, feature flags, or curriculum modified.

---

## Executive Summary

DG-001.2 establishes the **single authoritative educational authority model** for Kwalitec. Building on DG-001.1’s vocabulary (who the speakers are), this package defines what each speaker may and may not communicate: **Study Sensei** (educational mentor), **Kwalitec** (product), and **System** (pure factual layer).

It publishes a per-capability authority matrix, an intentional transition map for the student journey (including the mandatory Kwalitec → Study Sensei handoff), a conflict register converting RP-001 ED-01 / ED-05 / ED-11 observations into Board law, and ten governance decisions (D01–D10).

**Overall governance decision:** Every educational interaction has exactly one primary authority. Identity, Authority, and Voice remain separate concepts. No student-facing behaviour changed in this package.

---

## Authorities Defined

| Authority | Role | May | Must never |
|-----------|------|-----|------------|
| **Study Sensei** | Educational mentor | Judgement, recommendations, evidence interpretation, uncertainty, encouragement, educational memory, reflection, long-term learning, professional development | Infrastructure, subscriptions, authentication, outages, deployment, feature flags, operational notices |
| **Kwalitec** | Product / company | Auth, accounts, settings, billing, privacy, legal, maintenance, operational notices, support, release information | Educational judgements, evidence interpretation, replacing Sensei, recommending learning actions as mentor |
| **System** | Pure factual layer | Timestamps, calculations, sync, loading, processing, storage, status | Encourage, motivate, recommend, interpret, teach |

**Separations affirmed**

| Concept | Question | Law |
|---------|----------|-----|
| Identity | Who am I interacting with? | DG-001.1 |
| Authority | What may they communicate? | **DG-001.2** |
| Voice | How should they communicate? | Style Guide / ILE-001C0 / Voice Guide |

---

## Authority Matrix Summary

| Metric | Count |
|--------|------:|
| Capabilities audited | 25+ (auth through flag messaging, incl. success/empty/error) |
| Primary-authority assignments | 25 (exactly one primary each) |
| Board decisions (D01–D10) | 10 |
| Transition edges catalogued | 24 (T01–T24) |
| Conflict register items | 17 (AC-01–AC-17) |

**Primary distribution (educational core)**

- Study Sensei: Home, Mission Intelligence, Commitment, explanations, Session framing, Journal, Timeline, Feedback Loop, Revision  
- Kwalitec: Authentication, Onboarding (until handoff), Help, Profile, Settings, flag messaging, product success/empty  
- System: Mechanical errors, loading, timestamps; co-primary with Kwalitec on History archive facts  

Full matrix: `knowledge/governance/AUTHORITY_DECISION_MATRIX.md`.

---

## Capability Mapping

| Capability | Primary | Secondary | Boundary (short) |
|------------|---------|-----------|------------------|
| Authentication | Kwalitec | System | No educational judgement |
| Onboarding | Kwalitec → Study Sensei | System | Mandatory handoff T04 |
| Home | Study Sensei | System; Kwalitec chrome | No KW-as-tutor |
| Mission Intelligence | Study Sensei | System | No “system chose” |
| Mission Commitment | Study Sensei | System | Agency with mentor |
| Mission explanations | Study Sensei | System | Evidence / uncertainty only |
| Study Session | Study Sensei | System | Framing vs workflow status |
| Decision Journal | Study Sensei | System | KW never authors narrative |
| Educational Timeline | Study Sensei | System | Not vanity-score theatre |
| Educational Feedback Loop | Study Sensei | System | Calibration ≠ new ranking |
| Study Plan | Kwalitec | System; Sensei if advising | Structure vs advice |
| Revision | Study Sensei | System | Not second Mission |
| History | System + Kwalitec | Sensei bridges | Context ≠ mentor |
| Calibration | Kwalitec | System; Sensei meaning | Coverage ≠ mastery |
| Help | Kwalitec | Sensei glossary | Teaches; does not perform |
| Profile / Settings | Kwalitec | System | No learning recommendations |
| Notifications | Kwalitec envelope / Sensei body | System | Split per D08 |
| Success / Empty / Error | By domain | System | No mentor ops theatre |
| Feature-flag messaging | Kwalitec | System | Never Sensei |

---

## Authority Transition Findings

1. **Canonical flow is intentional:** Auth (KW) → Onboarding (KW) → **handoff** → Home/Mission/Session/Journal/Timeline (SS) → Settings/Help (KW).  
2. **Defect pattern (Alpha):** Orientation and support speak as Kwalitec; memory speaks as Study Sensei; Home often unnamed — **handoff missing** (ED-01 / AC-01 / AC-04).  
3. **Required fix (future copy, not this package):** Transition **T04** with sentence *“Study Sensei is how Kwalitec guides your daily learning decisions.”*  
4. **Return loops** (Settings → Home) are authorised (T21) without re-teaching Sensei every time.  
5. **System inserts** (loading/errors) must never be dressed as mentor warmth (T18 / T24).  
6. **Notifications** require envelope/body authority split (T23 / D08) before any notification programme claims Sensei consistency.

Full map: `knowledge/governance/AUTHORITY_TRANSITION_MAP.md`.

---

## Authority Conflicts

Governance converts RP-001 conflicts into Board resolutions; copy/implementation residuals remain open where noted.

| Priority | ID | Issue | Governance | Residual |
|----------|-----|-------|------------|----------|
| 1 | AC-01 / AC-04 | Dual narrator + missing handoff | D01/D02/D04/D10 | Copy |
| 2 | AC-02 | System-as-mentor | D01/D03/D07 | Contained OFF; rename before enable |
| 3 | AC-06 / AC-07 | Noun storm / reflection map (felt multi-authority) | Lexicon + D09/D10 | Copy |
| 4 | AC-03 | History vs Timeline | D06 | Copy |
| 5 | AC-08–AC-17 | Revision overlap, flag honesty, latent MissionOptimizer, etc. | Matrix + D05–D08 | Mixed open/contained |

Full register: `knowledge/governance/AUTHORITY_CONFLICT_REGISTER.md`.

---

## Board Decisions

| ID | Decision |
|----|----------|
| **DG-001.2-D01** | Study Sensei is sole primary authority for educational judgement, recommendations, evidence interpretation, memory, and guidance reflection |
| **DG-001.2-D02** | Kwalitec is primary for product, account, legal, and operational speech — never a second tutor |
| **DG-001.2-D03** | System is sole primary for pure factual / mechanical status — zero educational judgement |
| **DG-001.2-D04** | Mandatory onboarding handoff KW → SS (T04) |
| **DG-001.2-D05** | Exactly one primary authority per student-facing interaction |
| **DG-001.2-D06** | History is context (System + Kwalitec); Sensei bridges only |
| **DG-001.2-D07** | Feature flags and operational notices never Study Sensei |
| **DG-001.2-D08** | Notifications: Kwalitec envelope; Study Sensei educational body |
| **DG-001.2-D09** | Session practice under Sensei framing; not second daily-focus authority |
| **DG-001.2-D10** | Help teaches Sensei vocabulary; Sensei owns meaning in use |

---

## Outstanding Governance Questions

| ID | Question | Notes |
|----|----------|-------|
| OQ-A01 | Home Sensei naming density | Inherits DG-001.1 OQ-02 — ownership clear; continuous naming open |
| OQ-A02 | Study Plan educational advice attribution threshold | When does pacing hint require Sensei attribution vs pure KW structure? |
| OQ-A03 | Learning Insights speaker | Soft Twin speech — Sensei-adjacent vs named Sensei (coordinate with lexicon) |
| OQ-A04 | Notification programme authority schema | Concrete payload tags for D08 |
| OQ-A05 | Whether re-auth must restate handoff | Transition map prefers once-per-orientation; Board may tighten for reset cohorts |

None block DG-001.2 authority-model completeness; they block later *implementation* claims of full ED-01 closure and notification Sensei consistency.

---

## Certification Decision

**Conditional Pass**

**Rationale:** The Board can answer without ambiguity who speaks, why, what they may say, and what they are forbidden from saying — from the four authority governance documents. Every audited capability has exactly one primary authority under law. Unqualified Pass for *student-facing authority consistency* remains blocked until a future copy/implementation programme applies the handoff (T04), retires KW-as-mentor / system-as-mentor strings, and aligns Help/History/empty states. This package correctly does not implement those changes.

---

## Decision Log

| When | Decision | Outcome |
|------|----------|---------|
| 2026-07-28 | Open DG-001.2 from DG-001.1 + RP-001 authority residuals | Governance package authorised |
| 2026-07-28 | Audit authority across student-facing capabilities | 25+ capabilities mapped |
| 2026-07-28 | Define three authorities only | Study Sensei / Kwalitec / System |
| 2026-07-28 | Separate Identity / Authority / Voice | Authority scoped to DG-001.2 |
| 2026-07-28 | **DG-001.2-D01–D10** Board decisions | Published in decision matrix |
| 2026-07-28 | Catalogue transitions T01–T24 | Mandatory handoff T04 |
| 2026-07-28 | Conflict register AC-01–AC-17 | Governance resolutions + residuals |
| 2026-07-28 | Certification | Conditional Pass — governance complete; implementation pending |

---

## Summary

**What was achieved**

Four permanent educational authority authorities plus this completion report. Board decisions resolve ownership of educational speech domains identified in Alpha certification (especially ED-01 narrator drift) without touching application code.

**Why it matters**

Professional learners should never wonder whether the product, the mentor, or “the system” is teaching them. Future remediation can assign every string to one primary authority instead of re-debating narrator ownership per surface.

**How future implementation should use these documents**

1. Treat `EDUCATIONAL_AUTHORITY_MODEL.md` as speech-domain law.  
2. Place journey handoffs using `AUTHORITY_TRANSITION_MAP.md`.  
3. Assign capability speakers via `AUTHORITY_DECISION_MATRIX.md`.  
4. Track defects via `AUTHORITY_CONFLICT_REGISTER.md`.  
5. Cite DG-001.2 in any programme remediating ED-01 / ED-05 / ED-11 authority drift.  
6. Keep DG-001.1 lexicon for *names*; DG-001.2 for *permission to speak*.

---

## Files Created

- `knowledge/governance/EDUCATIONAL_AUTHORITY_MODEL.md`
- `knowledge/governance/AUTHORITY_TRANSITION_MAP.md`
- `knowledge/governance/AUTHORITY_DECISION_MATRIX.md`
- `knowledge/governance/AUTHORITY_CONFLICT_REGISTER.md`
- `knowledge/governance/DG001_2_COMPLETION_REPORT.md`

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
- Decision-engine singularity (deterministic cores) affirmed as distinct from student-facing narration authority.

---

## Technical Debt

- Live templates still contain dual-narrator / system-as-mentor / missing handoff — governance resolved, product not yet updated (AC-01, AC-02, AC-04).  
- History epistemology copy (ED-05 / AC-03) guided but not closed.  
- Outstanding questions OQ-A01–OQ-A05 remain for later Board/copy programmes.  
- Latent MissionOptimizer quarantine residual (AC-17) unchanged — contained, not deleted.

---

## Known Limitations

- Assumes RP-001.3 / RP-001.5 / Educational Consistency Audit observations remain accurate as of 2026-07-28.  
- Does not validate cohort understanding of authority handoff (no student testing).  
- Does not amend templates, PX files, or ILE product copy in this package.  
- Success criterion is *governance recreatability of authority law*, not *production string convergence*.

---

## Student Impact Assessment

Governance only.

No student-facing changes.

| Field | Value |
|---|---|
| **Programme / Milestone ID** | DG-001.2 |
| **Title** | Educational Authority Model |
| **Date** | 2026-07-28 |
| **Student-visible change?** | No |
| **Production activation?** | None |
| **Related KSI categories** | None directly (enables future K1/K8 narrator coherence) |

### 1. Student problem

Students encounter Kwalitec product voice and Study Sensei mentor voice without a clear handoff, and sometimes “the system” as a third implied teacher (ED-01 / ED-11). History stats can feel like a competing learning story (ED-05). This package does not yet change what students see.

**Evidence:** RP-001 Educational Consistency Audit (authority review); RP-001.5 Educational Drift Register; DG-001.1 DEP-04 / DEP-16.

### 2. Student benefit

Indirect: future copy programmes can converge speakers so learners always know who is teaching, who is explaining recommendations, who remembers learning, who presents product information, and when the UI is only reporting facts.

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A (governance) | Future Sensei-primary Mission speech |
| How am I progressing? | N/A | Future Journal/Timeline vs History boundary |
| What is stopping me? | N/A | — |
| What happens next? | N/A | — |

**Final Test:** Does this help students become better professionals? **Indirectly** — only after implementation uses this authority model.

### 3. Learning benefit

No immediate learning-behaviour change. Enables a singular, intentional mentor relationship later — reducing narrator drift that undermines trust in guidance.

### 4. Success metrics

Board recreatability criterion (below). No KSI movement claimed.

### 5. Risks

Over-claiming student-facing authority consistency before ED-01 / handoff copy remediation.

### 6. Assumptions

Implementation programmes will cite and obey DG-001.2; Runtime C will not enable with “system chose” narration; Help will teach Sensei vocabulary without becoming a second tutor.

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

- `knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md`  
- `knowledge/governance/EDUCATIONAL_VOCABULARY_MAP.md`  
- `knowledge/governance/EDUCATIONAL_LANGUAGE_STYLE_GUIDE.md`  
- `knowledge/governance/TERM_DEPRECATION_REGISTER.md`  
- `knowledge/governance/DG001_1_COMPLETION_REPORT.md`  
- `knowledge/release/RP-001/EDUCATIONAL_CONSISTENCY_AUDIT.md`  
- `knowledge/release/RP-001/EDUCATIONAL_DRIFT_REGISTER.md`  
- `knowledge/release/RP-001/VOICE_GUIDE.md`  
- `knowledge/product/STUDY_SENSEI_PHILOSOPHY.md`  
- `knowledge/educational/EDUCATIONAL_GOVERNANCE_RECERTIFICATION.md` (latent dual-authority residual)

---

## Lessons learned for student value

Alpha certification showed educational *decision* authority can be singular while educational *narrative* authority stays dual. Vocabulary law (DG-001.1) names speakers; without authority law (DG-001.2), product orientation and mentor memory still compete. Authority transitions must be designed — especially the first introduction of Study Sensei — or professional learners never form one mentor relationship.

---

## Explainability Review

N/A — governance documentation only; no student-facing intelligence behaviour, speech schema, or explanation UI changed. Future copy that reattributes “Why the system chose this” → Sensei explanation should cite P-001.2 when those strings ship.

---

## Recommendation Quality Review

N/A — no recommendation ranking, selection, or Mission Intelligence composition changed. Authority model clarifies who may *narrate* authorised recommendations (Study Sensei only).

---

## Version 1 readiness residual

N/A for production-ready declaration. DG-001.2 does not claim Version 1 progress beyond clarifying educational authority law that later release programmes may consume. Residual open gates G1–G12 unchanged.

---

## Success Criteria

> Who is speaking? Why? What authority do they possess? What are they forbidden from exercising? Does every educational interaction have exactly one primary authority?

**Yes** — from `EDUCATIONAL_AUTHORITY_MODEL.md` + `AUTHORITY_TRANSITION_MAP.md` + `AUTHORITY_DECISION_MATRIX.md` + `AUTHORITY_CONFLICT_REGISTER.md`.

**DG-001.2 is complete** (governance). Student-facing remediation remains future work.

---

**End of DG001_2_COMPLETION_REPORT**

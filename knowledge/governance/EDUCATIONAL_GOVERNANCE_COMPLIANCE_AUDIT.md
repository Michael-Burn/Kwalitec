# Educational Governance Compliance Audit

**Programme:** EGC-001 — Educational Governance Compliance  
**Version:** 1.0  
**Status:** Active — Board compliance baseline (audit only)  
**Audit date:** 2026-07-28  
**Authority:** Educational Governance Constitution (DG-001.4); subordinate instruments DG-001.1–3  
**Constraint:** Audit only — no templates, copy, architecture, recommendations, feature flags, curriculum, or educational behaviour modified.

**Companions:**  
`GOVERNANCE_TRACEABILITY_MATRIX.md` · `GOVERNANCE_NON_COMPLIANCE_REGISTER.md` · `GOVERNANCE_COMPLIANCE_SCORECARD.md` · `EGC001_COMPLETION_REPORT.md`

**Upstream evidence:** RP-001.5 Educational Drift Register (ED-01–ED-20); DG-001 Authority Conflict Register (AC-*); DG-001 Term Deprecation Register (DEP-*); Alpha templates and DTO copy under `app/templates/` and `app/application/`.

---

## 1. Purpose

Certify whether the **existing Alpha product** complies with DG-001 educational governance law.

This audit does **not** redesign the product. It establishes a complete compliance baseline so every future remediation can cite an exact constitutional clause.

**Educational principle:** Governance cannot improve a product until governance can measure the product.

---

## 2. Method

1. Load DG-001.1 lexicon, DG-001.2 authority model, DG-001.3 reflection architecture, DG-001.4 Constitution (CP-01–CP-10, CI-01–CI-06, hard prohibitions).  
2. Inventory student-facing educational surfaces listed in the EGC-001 brief.  
3. Observe live template / DTO / onboarding service copy (not aspirational docs alone).  
4. Cross-map to RP-001 ED-* and DG-001 AC-* / DEP-* residuals.  
5. Classify each finding as exactly one of: **Fully Compliant · Partially Compliant · Non-Compliant · Not Applicable**.  
6. Record required evidence fields and propose a future remediation package ID for every Non-Compliant / Partially Compliant item.

**Evidence quality rule:** Prefer exact student-facing strings. Governance-only “resolved in law” does **not** equal product compliance.

---

## 3. Compliance dimensions (applied to every capability)

| Dimension | Law primary |
|-----------|-------------|
| Lexicon Compliance | DG-001.1; CP-03; CI-01 |
| Authority Compliance | DG-001.2; CP-04; CP-10; CI-05–CI-06 |
| Reflection Compliance | DG-001.3; RG-01–RG-20; CP-05; CI-02–CI-04 |
| Constitutional Compliance | DG-001.4 CP-01–CP-10; §11 prohibitions |
| Explainability Compliance | CP-07–CP-08; P-001.2 (presentation honesty) |
| Educational Honesty | CP-07; CP-08 |
| Professional Judgement | CP-09 |
| Student Trust | CP-06 |
| Narrator Consistency | CP-04; CP-10; DG-001.2-D04–D05 |
| Evidence Quality | Audit standard — quote / path / residual ID |

---

## 4. Executive verdict

| Question | Answer |
|----------|--------|
| Does the product comply with its own educational governance? | **No — not as a whole.** Pockets of Full / Partial compliance exist; critical narrator, lexicon, orientation, and reflection-map clauses fail in the live Alpha surface. |
| Which clauses are already satisfied? | See Scorecard § Fully Compliant pockets (Journal Sensei chrome, Timeline Sensei chrome, Guided Reflection honesty disclaimer, Calibration non-reflection honesty, Session optional note, Decision Journal as durable memory host). |
| Which require remediation? | See Non-Compliance Register (NCR-*). |
| Can every remediation package be traced to constitutional law? | **Yes** — every NCR cites clause + proposed EGC-R* package. |

**Product compliance certification:** **NON-COMPLIANT** (baseline certified).  
**Programme EGC-001:** complete when Board can answer the four questions above — **Yes**.

---

## 5. Capability audits

For each capability: observed behaviour · applicable clauses · status · risk · student impact · remediation · priority · dependency.

Status abbreviations: **FC** Fully Compliant · **PC** Partially Compliant · **NC** Non-Compliant · **NA** Not Applicable.

---

### 5.1 Authentication

| Field | Detail |
|-------|--------|
| **Capability** | Authentication (login / logout / invite-only Alpha) |
| **Observed** | Login presents Kwalitec brand (`auth/login.html`: “Kwalitec is invite-only…”). No Study Sensei mentoring. No educational judgement. |
| **Clauses** | DG-001.2-D02 (Kwalitec owns auth); CP-10 (Sensei not on auth); CP-04 |
| **Status** | **FC** (authority domain correct) |
| **Risk** | Low |
| **Student impact** | Product identity clear at gate. |
| **Remediation** | None for authority. |
| **Priority** | — |
| **Dependency** | — |
| **Dimensions** | Lexicon FC · Authority FC · Reflection NA · Constitution FC · Explainability NA · Honesty FC · Judgement NA · Trust FC · Narrator FC · Evidence High |

---

### 5.2 Onboarding

| Field | Detail |
|-------|--------|
| **Capability** | Alpha product onboarding |
| **Observed** | `alpha_onboarding_service.py` ONBOARDING_STEPS: “What Kwalitec is”; “Each day **Kwalitec** prepares a focused study mission”; “reasons **Kwalitec** used”; reflection “helps **Kwalitec** understand…”. **No** mandatory handoff sentence “Study Sensei is how Kwalitec guides your daily learning decisions.” Mission/session mixed in one breath. |
| **Clauses** | DG-001.1-D01; DG-001.2-D04 (mandatory KW→SS handoff); CI-05; CP-04; CP-10; ED-01; ED-20 |
| **Status** | **NC** |
| **Risk** | High — establishes dual / wrong mentor at first educational orientation |
| **Student impact** | Students learn Kwalitec-as-tutor before meeting Sensei memory surfaces. |
| **Remediation** | Insert Board handoff; reattribute guidance/explanation to Study Sensei; separate Mission vs Session wording. |
| **Priority** | P0 |
| **Dependency** | EGC-R01 (narrator handoff); EGC-R02 (lexicon) |
| **Finding** | NCR-001 |

---

### 5.3 Home

| Field | Detail |
|-------|--------|
| **Capability** | Home / student landing |
| **Observed** | Hero eyebrow often “Today's Mission” (`student/home.html`) — lexicon-aligned when Mission path. CTA / forms still “Start Today's Session” (practice shell — allowed for Session concept, but PX synonym collision with Mission remains). Guided Reflection preview has honesty: “nothing here is recorded…”. “Optimising for {axis}” engineering tone (ED-15). Home educational speech often **unnamed** (no Study Sensei). Welcome modal: “Each day Kwalitec recommends…” + “Start Today's Session”. |
| **Clauses** | DG-001.1-D02; DEP-01/02; DG-001.2-D01/D05; OQ-02; CP-03; CP-04; CP-10; ED-01/02/09/15 |
| **Status** | **PC** |
| **Risk** | High (narrator gap + noun storm) |
| **Student impact** | Daily focus partly Mission-named but authority invisible; tip/Session synonyms elsewhere fracture the chain. |
| **Remediation** | Sensei naming density; retire tip adjacent copy; soften optimisation chrome; keep Guided Reflection honesty. |
| **Priority** | P0 |
| **Dependency** | EGC-R01; EGC-R02; EGC-R08 |
| **Finding** | NCR-002 |

---

### 5.4 Mission Intelligence

| Field | Detail |
|-------|--------|
| **Capability** | Daily Mission Intelligence composition / presentation |
| **Observed** | Domain compose uses Study Sensei silence / wait copy (`daily_mission_intelligence/compose.py`). Student Home may show MI axis label “Optimising for…”. MES + MI dual-hero noise mitigated by RR-001.2 disclosure (ED-10 watch). |
| **Clauses** | DG-001.2-D01; DG-001.1 Mission entry; CP-07–CP-08; ED-10; ED-15 |
| **Status** | **PC** |
| **Risk** | Medium |
| **Student impact** | Intelligence can feel engineering-led when axis chrome shows; Sensei silence path is stronger when empty. |
| **Remediation** | Student-safe axis wording; keep singular Mission brief; no second tutor. |
| **Priority** | P1 |
| **Dependency** | EGC-R02; EGC-R08 |
| **Finding** | NCR-003 |

---

### 5.5 Mission Commitment

| Field | Detail |
|-------|--------|
| **Capability** | Mission commitment accept → practice → complete → ack |
| **Observed** | Commitment completion wired (RR-001). Continuity copy historically uses “tip” (ED-06). Commitment reflection is acknowledgement (lawful under DG-001.3-D07). |
| **Clauses** | DG-001.3-D07; DEP-01; CP-05; CP-09; ED-06 |
| **Status** | **PC** |
| **Risk** | Medium (terminology) |
| **Student impact** | Agency close works; tip wording breaks Mission vocabulary transfer. |
| **Remediation** | Replace tip with Mission / Recommendation / guidance by context. |
| **Priority** | P1 |
| **Dependency** | EGC-R02 |
| **Finding** | NCR-004 |

---

### 5.6 Study Session

| Field | Detail |
|-------|--------|
| **Capability** | Study Session practice workflow + session reflection |
| **Observed** | Session reflection note is **optional** (`session/reflection.html`). Completion card labels “Exam readiness” (ED-16). Brand chrome “Kwalitec” on session shell (product — OK). Framing of Session as Mission synonym still present in PX CTAs. Session notes do **not** auto-mirror to Decision Journal (OQ-R01 open — lawful residual, not auto-fail if not claimed as Journal). |
| **Clauses** | DG-001.1 Session; DG-001.3-D07; RG-02; CP-07; ED-02; ED-16 |
| **Status** | **PC** |
| **Risk** | Medium |
| **Student impact** | Practice loop works; readiness label may overclaim certainty; Mission≠Session still confused via CTAs/Help. |
| **Remediation** | Soften readiness framing; align Help/CTA lexicon; Board decide Journal mirror separately. |
| **Priority** | P1 |
| **Dependency** | EGC-R02; EGC-R10; OQ-R01 |
| **Finding** | NCR-005 |

---

### 5.7 Decision Journal

| Field | Detail |
|-------|--------|
| **Capability** | Decision Journal (educational memory) |
| **Observed** | Page eyebrow **“Study Sensei”**; intro honesty about not rewriting history; “Why this guidance” provenance; optional reflection label. Empty description still says “**Mission tip**, Quick Check, or revision suggestion” — tip + gated QC mention (ED-14 / DEP-01). Sole durable Sensei memory store present (CI-02). |
| **Clauses** | DG-001.1 Journal; DG-001.2-D01; DG-001.3-D02; CI-02; DEP-01; ED-14; CP-07–CP-10 |
| **Status** | **PC** |
| **Risk** | Medium (empty-state tip/QC honesty) · Low for memory host itself |
| **Student impact** | Strong Sensei memory when entries exist; empty state reintroduces tip noun and may mention OFF capabilities. |
| **Remediation** | Empty-state lexicon + flag honesty. |
| **Priority** | P1 |
| **Dependency** | EGC-R02; EGC-R12 |
| **Finding** | NCR-006 |

---

### 5.8 Educational Timeline

| Field | Detail |
|-------|--------|
| **Capability** | Educational Timeline |
| **Observed** | Sensei eyebrow/intro DTO; drawn from journal entries; narrative not-from-scores culture. Narrative strings may still say “Mission tip” (DEP-01). Epistemology tension with History/Help stats (ED-05). |
| **Clauses** | DG-001.1 Timeline; DG-001.2-D06; DG-001.3 Timeline reflection; CP-07–CP-08; ED-05 |
| **Status** | **PC** |
| **Risk** | Medium |
| **Student impact** | Long-term story present; tip wording + stats competition dilute Meaning vs numbers. |
| **Remediation** | Tip retirement in narrative; History bridge copy. |
| **Priority** | P1 |
| **Dependency** | EGC-R02; EGC-R06 |
| **Finding** | NCR-007 |

---

### 5.9 Feedback Loop / Sensei reflection

| Field | Detail |
|-------|--------|
| **Capability** | Educational Feedback Loop (student-facing = optional Journal reflection) |
| **Observed** | Optional reflection on Journal; DTO: helps Study Sensei understand usefulness; does not re-rank (architecture). Student-visible “Feedback Loop” jargon density low (OQ-03 preferred). |
| **Clauses** | DG-001.3-D06; RG-02; CP-05; CI-04; OQ-03 |
| **Status** | **PC** (core behaviour FC; orientation/Help map missing) |
| **Risk** | Medium (discoverability / map) |
| **Student impact** | Calibration of guidance exists for those who find Journal; Help does not teach it. |
| **Remediation** | Help map; keep optional; no re-rank claims. |
| **Priority** | P1 |
| **Dependency** | EGC-R03; EGC-R04 |
| **Finding** | NCR-008 |

---

### 5.10 Revision

| Field | Detail |
|-------|--------|
| **Capability** | Revision surface |
| **Observed** | Thin Alpha revision surface; risk of competing “today's best revision” vs primary Mission (ED-13). Acknowledgement ≠ Revision Reflection capture (DG-001.3 non-reflection). |
| **Clauses** | DG-001.2 Mission primacy; CP-04; ED-13; OQ-05 |
| **Status** | **PC** |
| **Risk** | Medium |
| **Student impact** | Possible second “what matters today” if revision presented as peer focus. |
| **Remediation** | Disclose Mission primacy; do not invent Revision Reflection until architecture update. |
| **Priority** | P2 |
| **Dependency** | EGC-R09 |
| **Finding** | NCR-009 |

---

### 5.11 History

| Field | Detail |
|-------|--------|
| **Capability** | History (past sessions / accuracy) |
| **Observed** | Help: “History shows… accuracy over time…”. Timeline culture: learning story not from scores. No Sensei bridge language on History as System+Kwalitec context (DG-001.2-D06). |
| **Clauses** | DG-001.2-D06; CP-07–CP-08; ED-05 |
| **Status** | **NC** (epistemology ownership / bridge missing) |
| **Risk** | Medium |
| **Student impact** | Students may treat accuracy stats as the Sensei’s truth. |
| **Remediation** | Intro: stats are context; Journal/Timeline hold educational meaning. |
| **Priority** | P1 |
| **Dependency** | EGC-R06 |
| **Finding** | NCR-010 |

---

### 5.12 Calibration

| Field | Detail |
|-------|--------|
| **Capability** | Calibration (declared coverage) |
| **Observed** | `calibration/alpha.html`: “declarations, not Estimated Knowledge”; “Declared coverage only — not Estimated Knowledge.” Not labelled reflection. |
| **Clauses** | DG-001.3-D05; DEP non-reflection; CP-07 |
| **Status** | **FC** |
| **Risk** | Low |
| **Student impact** | Structural honesty preserved. |
| **Remediation** | None — do not relabel as reflection. |
| **Priority** | — |
| **Dependency** | — |

---

### 5.13 Help

| Field | Detail |
|-------|--------|
| **Capability** | Help & Support |
| **Observed** | Speaks as Kwalitec product support (lawful for product FAQ). Topics: “How is my **Session** chosen?”; “closest to being tested on” (ED-08 anxiety); Reflection FAQ collapses to Session record only — **omits** Decision Journal, Educational Timeline, Mission Intelligence, Feedback Loop / Sensei reflection (ED-04). No Study Sensei handoff glossary. |
| **Clauses** | DG-001.1-D04; DG-001.2-D04/D10; CI-05; CP-03; CP-06; ED-04; ED-08 |
| **Status** | **NC** |
| **Risk** | High |
| **Student impact** | Orientation never teaches Sensei memory surfaces; anxiety-adjacent phrasing. |
| **Remediation** | Educational map + Sensei glossary; soften ED-08; Session≠Mission clarity. |
| **Priority** | P0 |
| **Dependency** | EGC-R03; EGC-R01; EGC-R04 |
| **Finding** | NCR-011 |

---

### 5.14 Notifications

| Field | Detail |
|-------|--------|
| **Capability** | Notifications |
| **Observed** | No mature student notification educational mentor surface found in Alpha templates (settings prefs may exist for product prefs). AC-13: governance forbids Sensei-as-marketing. |
| **Clauses** | DG-001.2-D08; CP-06; CP-10 |
| **Status** | **NA** (capability thin / not educationally speaking) — **FC** for “does not currently violate” with watch |
| **Risk** | Medium if future marketing-as-Sensei ships |
| **Student impact** | None today from mentor-as-spam. |
| **Remediation** | Future notification programme must follow D08 (EGC-R11). |
| **Priority** | P3 (preventive) |
| **Dependency** | EGC-R11 when notifications educationalise |

---

### 5.15 Settings

| Field | Detail |
|-------|--------|
| **Capability** | Settings / About / data |
| **Observed** | “About Kwalitec”; product/account controls; research link to Product Check-in. No Study Sensei educational judgement on Settings. |
| **Clauses** | DG-001.2-D02; AC-12 prevent |
| **Status** | **FC** |
| **Risk** | Low |
| **Student impact** | Product ownership clear. |
| **Remediation** | Prevent future learning recommendations in mentor voice here. |
| **Priority** | — |
| **Dependency** | — |

---

### 5.16 Success states

| Field | Detail |
|-------|--------|
| **Capability** | Success / completion states |
| **Observed** | Session completion / QC completion mix product and educational labels (“Today's Mission” on some AA paths; “Exam readiness” on session complete). Research thank-you is product. AC-15 residual. |
| **Clauses** | CP-04; CP-07; ED-16 |
| **Status** | **PC** |
| **Risk** | Low–Medium |
| **Student impact** | Occasional overclaim or brand/mentor mix on close. |
| **Remediation** | Separate product praise from educational judgement; honesty on readiness. |
| **Priority** | P2 |
| **Dependency** | EGC-R10 |
| **Finding** | NCR-012 |

---

### 5.17 Empty states

| Field | Detail |
|-------|--------|
| **Capability** | Empty states (Home, Journal, Timeline, etc.) |
| **Observed** | RR-001.2 improved empty/success philosophy. Journal empty still tip/QC (ED-14). MI empty Sensei wait path stronger. |
| **Clauses** | CP-07–CP-08; DEP-01; ED-12; ED-14 |
| **Status** | **PC** |
| **Risk** | Medium |
| **Student impact** | Emptiness can reintroduce deprecated nouns or gated features. |
| **Remediation** | Lexicon + flag honesty pass on empties. |
| **Priority** | P1 |
| **Dependency** | EGC-R02; EGC-R12 |
| **Finding** | NCR-013 |

---

### 5.18 Error states

| Field | Detail |
|-------|--------|
| **Capability** | Error / unavailable / CSRF / session-not-found |
| **Observed** | System/product chrome for mechanical failures (e.g. “Today's Session is temporarily unavailable”). No Sensei theatre found as primary error narrator (AC-11 watch). |
| **Clauses** | DG-001.2-D03; CP-04 |
| **Status** | **FC** (with residual watch) |
| **Risk** | Low |
| **Student impact** | Facts remain facts. |
| **Remediation** | Keep System/Kwalitec; never Sensei-as-outage. |
| **Priority** | — |
| **Dependency** | — |

---

### 5.19 Feature flag messaging

| Field | Detail |
|-------|--------|
| **Capability** | Feature-flag / gated capability speech |
| **Observed** | Runtime C “Why the system chose this” **contained OFF** (ED-11 / DEP-04). Journal empty may mention Quick Check while QC OFF (ED-14). Unified Journey / Guided Reflection stacks residual (DG-001.3-D08). |
| **Clauses** | DG-001.2-D07; Constitution §11; DEP-04; ED-11; ED-14; D08 |
| **Status** | **PC** (contained) → treat enable-as-is as **NC** |
| **Risk** | High **if enabled**; Low while OFF for Runtime C |
| **Student impact** | Trust fracture if System-as-mentor enabled; confusion if OFF features advertised. |
| **Remediation** | Rename before enable; empty-state flag honesty. |
| **Priority** | P0 before any Runtime C ON; P1 for empty honesty |
| **Dependency** | EGC-R07; EGC-R12 |
| **Finding** | NCR-014 |

---

### 5.20 Educational copy (cross-cutting)

| Field | Detail |
|-------|--------|
| **Capability** | Educational copy corpus |
| **Observed** | Tip primary noun survives (`explanation_card.html`: “Why this tip?”; Journal empty “Mission tip”; study tip cards on dashboard/mission). Mission and Session compete as focus labels (PX `product_language.py` “Today's Session”). |
| **Clauses** | CP-03; CI-01; DEP-01; DEP-02; ED-02; ED-07 |
| **Status** | **NC** |
| **Risk** | High |
| **Student impact** | Cannot track one daily decision across surfaces. |
| **Remediation** | Tip retirement; Mission-led focus; Session = practice. |
| **Priority** | P0 |
| **Dependency** | EGC-R02 (OQ-01 PX reconciliation) |
| **Finding** | NCR-015 |

---

### 5.21 Educational explanations

| Field | Detail |
|-------|--------|
| **Capability** | Why-this / explanation disclosures |
| **Observed** | Journal provenance “Why this guidance” (**compliant eyebrow**). Home explanation card “Why this tip?” (**non-compliant**). Onboarding attributes reasons to Kwalitec. |
| **Clauses** | DEP-01; CP-07–CP-08; DG-001.2-D01; ED-07; ED-20 |
| **Status** | **PC** |
| **Risk** | Medium–High |
| **Student impact** | Explainability present but inconsistently named and owned. |
| **Remediation** | Standardise “Why this guidance / Mission / recommendation”; Sensei ownership. |
| **Priority** | P0 |
| **Dependency** | EGC-R02; EGC-R01 |
| **Finding** | NCR-016 |

---

### 5.22 Reflection flows

| Field | Detail |
|-------|--------|
| **Capability** | Reflection family (all variants) |
| **Observed** | Multiple lawful types exist in product; Guided preview honesty **present**. Student-facing **map absent** (ED-03). Product Check-in titled “Daily Reflection & Product Check-in” (**forbidden naming**, DG-001.3-D05 / ED-18). Parallel stacks residual (D08). Sensei reflection optional. Session note optional. |
| **Clauses** | CP-05; CI-03; DG-001.3-D01–D08; RG-01–RG-07; ED-03; ED-09; ED-18 |
| **Status** | **NC** (as coherent student system) |
| **Risk** | High |
| **Student impact** | Reflection feels like forms, not professional judgement practice. |
| **Remediation** | Publish Help map; rename Check-in; keep honesty; consolidate residuals later. |
| **Priority** | P0 |
| **Dependency** | EGC-R04; EGC-R05; OQ-R02 |
| **Finding** | NCR-017 |

---

### 5.23 Narrator transitions

| Field | Detail |
|-------|--------|
| **Capability** | KW ↔ SS narrator transitions |
| **Observed** | Hidden transition: onboarding/Help = Kwalitec; Journal/Timeline/MI silence = Study Sensei; Home often unnamed (AC-01, AC-04, AC-05). Mandatory T04 handoff **missing**. |
| **Clauses** | DG-001.2-D04; CI-05; CP-04; CP-10; ED-01 |
| **Status** | **NC** |
| **Risk** | High |
| **Student impact** | No single mentor relationship. |
| **Remediation** | Explicit handoff + continuous naming policy (OQ-02). |
| **Priority** | P0 |
| **Dependency** | EGC-R01; EGC-R08 |
| **Finding** | NCR-018 |

---

### 5.24 Authority ownership

| Field | Detail |
|-------|--------|
| **Capability** | Authority ownership across surfaces |
| **Observed** | Three authorities exist in law; product still assigns educational judgement speech to Kwalitec on onboarding/explanations; tip/Session labels create felt multi-authority (AC-06). History soft alternate epistemology (AC-03). |
| **Clauses** | DG-001.2-D01–D10; CP-04; CP-10; Constitution §11 |
| **Status** | **NC** |
| **Risk** | High |
| **Student impact** | Unclear who teaches them. |
| **Remediation** | Implement authority matrix in copy programmes. |
| **Priority** | P0 |
| **Dependency** | EGC-R01; EGC-R03; EGC-R06 |
| **Finding** | NCR-019 |

---

### 5.25 Educational terminology

| Field | Detail |
|-------|--------|
| **Capability** | Educational terminology consistency |
| **Observed** | Lexicon is Board law; live product still uses tip, Today's Session-as-focus, Mission tip, Study Tip cards. |
| **Clauses** | CP-03; CI-01; DG-001.1 entire; DEP-01–DEP-03 |
| **Status** | **NC** |
| **Risk** | High |
| **Student impact** | Noun storm — ED-02. |
| **Remediation** | EGC-R02 + OQ-01. |
| **Priority** | P0 |
| **Dependency** | EGC-R02 |
| **Finding** | NCR-020 |

---

### 5.26 Educational memory

| Field | Detail |
|-------|--------|
| **Capability** | Educational memory (Decision Journal singularity) |
| **Observed** | Decision Journal is the durable Sensei memory store (architecture + student surface). No second durable Sensei memory product found. Session notes / Guided preview correctly non-Journal by default. Orientation **fails to introduce** Journal (ED-04). Empty tip wording weakens lexicon. |
| **Clauses** | CI-02; DG-001.3-D02; Constitution §11.4; ED-04 |
| **Status** | **PC** (host FC; introduction NC) |
| **Risk** | High for discoverability |
| **Student impact** | Memory exists but many students never learn it exists. |
| **Remediation** | Help/onboarding first-introduction (DG-001.1-D04). |
| **Priority** | P0 |
| **Dependency** | EGC-R03; EGC-R01 |
| **Finding** | NCR-021 |

---

### 5.27 Product Check-in (research)

| Field | Detail |
|-------|--------|
| **Capability** | Product Check-in |
| **Observed** | Title: “Daily Reflection & Product Check-in” (`research/checkin.html`). Description says optional product feedback — **title still calls it Reflection**. Session recorded path discloses “not about your learning” in one place — title still violates D05. |
| **Clauses** | DG-001.3-D05; CI-03; Constitution §11.5; DEP Check-in; ED-18; OQ-R03 |
| **Status** | **NC** |
| **Risk** | Medium (Low likelihood, High conceptual damage) |
| **Student impact** | Product survey mistaken for educational reflection. |
| **Remediation** | Rename title; remove “Reflection” from Check-in. |
| **Priority** | P1 |
| **Dependency** | EGC-R05 |
| **Finding** | NCR-022 |

---

## 6. Constitutional principles roll-up

| Principle | Product status | Notes |
|-----------|----------------|-------|
| CP-01 Philosophy precedes implementation | **PC** | Philosophy docs exist; live copy drifts |
| CP-02 Governance precedes remediation | **FC** *(this programme)* | EGC-001 audits before remediation — satisfied for process |
| CP-03 One concept → one definition | **NC** | tip / Session / Mission storm |
| CP-04 One primary authority | **NC** | Dual narrator / unnamed Home |
| CP-05 Reflection one system | **NC** | Map missing; Check-in misnamed |
| CP-06 Trust over engagement | **PC** | No streak theatre found; anxiety Help residual |
| CP-07 Educational honesty | **PC** | Strong on Journal/Calibration/preview; weak on tip/QC/readiness |
| CP-08 Evidence over certainty | **PC** | Uncertainty fields exist; some overclaim labels |
| CP-09 Professional judgement | **PC** | Sensei reflection supports; orientation lag |
| CP-10 Sole Study Sensei mentor | **NC** | Kwalitec-as-mentor on onboarding/explanations |

---

## 7. Supporting invariants roll-up

| Invariant | Status |
|-----------|--------|
| CI-01 Mission ≠ Session ≠ Recommendation; tip deprecated | **NC** in product |
| CI-02 Journal sole durable Sensei memory | **FC** (host) |
| CI-03 Check-in / Calibration / system feedback ≠ educational reflection | **PC** (Calibration FC; Check-in title NC) |
| CI-04 Reflection optional; never scores / re-ranks | **FC** on audited Sensei/Session paths |
| CI-05 Mandatory Sensei handoff | **NC** |
| CI-06 Identity / Authority / Voice separate | **PC** (law clear; product conflates identity speech) |

---

## 8. Proposed remediation packages (traceable)

| ID | Package intent | Primary clauses | Closes (examples) |
|----|----------------|-----------------|-------------------|
| **EGC-R01** | Narrator handoff & Sensei attribution | D01; D04; CI-05; CP-10 | NCR-001, 018, 019, 021 |
| **EGC-R02** | Lexicon application (tip / Mission / Session) | D02; DEP-01/02; CP-03; CI-01; OQ-01 | NCR-002, 004, 015, 016, 020 |
| **EGC-R03** | Help educational orientation map | D04; D10; ED-04 | NCR-011, 008, 021 |
| **EGC-R04** | Reflection family student map | D01–D08; CP-05; ED-03 | NCR-017, 008 |
| **EGC-R05** | Product Check-in rename | D05; §11.5; ED-18 | NCR-022 |
| **EGC-R06** | History–Timeline epistemology bridge | D06; ED-05 | NCR-010, 007 |
| **EGC-R07** | Flag speech / Runtime C rename-before-enable | D07; DEP-04; ED-11 | NCR-014 |
| **EGC-R08** | Home Sensei naming density | OQ-02; D05 | NCR-002, 003, 018 |
| **EGC-R09** | Revision vs Mission disclosure | ED-13; OQ-05 | NCR-009 |
| **EGC-R10** | Session success / readiness honesty | ED-16; CP-07–08 | NCR-005, 012 |
| **EGC-R11** | Notifications authority (when built) | D08 | Preventive |
| **EGC-R12** | Empty-state tip / gated-feature honesty | ED-14; DEP-01 | NCR-006, 013, 014 |

**Rule:** No remediation programme may begin without citing one of these packages **and** the exact clause IDs above.

---

## 9. Outstanding governance questions (inherited — not closed by EGC-001)

| ID | Question | Blocks |
|----|----------|--------|
| OQ-01 | PX / `product_language.py` reconciliation sequence | EGC-R02 complete closure |
| OQ-02 | Home continuous Sensei naming density | EGC-R08 |
| OQ-03 | Feedback Loop student-visible name | EGC-R03/R04 |
| OQ-04 | Mastery student-facing exposure | Future copy |
| OQ-05 | Revision vs Mission disclosure copy | EGC-R09 |
| OQ-R01 | Session notes → Journal mirror? | Board before engineering |
| OQ-R02 | When to publish Help reflection map | EGC-R04 |
| OQ-R03 | RIP-001 Daily Reflection rename | EGC-R05 |

EGC-001 does **not** answer these — it records them as open inputs to remediation.

---

## 10. Certification statement

**EGC-001 certifies the Alpha product against DG-001 as NON-COMPLIANT overall**, with enumerated Fully Compliant and Partially Compliant pockets.

Governance law is sufficient to measure the product.  
Remediation may now proceed under EGC-R* packages with clause-level traceability.

**This audit does not close ED-01–ED-20.** Implementation evidence remains required (Constitution §11.6).

---

**End of EDUCATIONAL_GOVERNANCE_COMPLIANCE_AUDIT**

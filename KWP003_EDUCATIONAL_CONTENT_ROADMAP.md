# KWP-003 — Educational Content & Evidence Expansion

**Programme:** KWP-003 · Educational Content & Evidence Expansion  
**Phase:** Commercialisation Phase 3  
**Date:** 2026-07-30  
**Nature:** Content & evidence-density audit — **no runtime redesign**  
**Authority:** KWP-002 · SR-001A · SR-003 · `PRODUCT_BLUEPRINT.md` · EV-001A · EV-001B · SDT-004 · LXP-004A  

---

## Executive Summary

KWP-002 activated the commercial study companion. LearningSessionRuntime, EducationalEvidenceAuthority, StudentTwinEngine, and ProgressEngine are stable and wired. The commercial loop can lawfully accept sittings, advance coverage, and (when Educational+ exists) update the Twin.

**The limiting factor is no longer architecture. It is the density and richness of Educational+ learning opportunities flowing through that architecture.**

Today’s Session substance path (Read → Worked example → Practice → Reflection) mostly produces **Behavioural** evidence: participation, stage completion, unscored free-text practice. The Evidence Package builder can emit **Educational+** types (`EV-RT-07` / `EV-RT-08` / `EV-RT-40`), and the Twin will consume them — but production activity content almost never supplies attributable scored outcomes. `scored_correct` is never set on the live response path, so practice collapses to `EV-RT-06` (attempted) or `EV-RT-09` (partial / unscored).

| Layer | Status |
|---|---|
| Session / Evidence / Twin / Progress authorities | Complete (SR-001A) |
| Commercial Loop packaging | Complete (KWP-002) |
| Educational flow shell | Complete (LXP-004A) |
| **Scored, assessable educational content** | **Thin — Phase 3 priority** |

**Verdict:** Enrich package-derived reading, worked examples, practice items, feedback, model answers, and assessment pathways so every commercial sitting can lawfully produce Accepted Educational+ evidence — without changing Evidence Authority rules, Progress math, Twin math, or Session FSM.

**Phase 3 mandate:** Content in → Educational+ out. Architecture unchanged.

---

## Current Evidence Density

### Pipeline (already lawful)

```
Mission → Study Session
  → Learning Objectives → Reading → Worked Example → Practice → Reflection
  → Finish Review
  → Evidence Package (Generated)
  → EducationalEvidenceAuthority (Accept / Reject)
  → Progress (when authorised) · Twin (Educational+ only)
```

### What each stage actually emits today

| Stage / activity | Typical observation | Ceiling grade | Live density | Notes |
|---|---|---|---|---|
| Learning objectives presented | `EV-RT-01` | Informational | Medium | Overview presentation; not understanding |
| Reading started / completed | `EV-RT-02` / `EV-RT-03` | Informational → Behavioural | Medium | Body is LO list + rationale template — not syllabus chapter depth |
| Worked example started / completed | `EV-RT-04` / `EV-RT-05` | Informational → Behavioural | Low–Medium | Generic “method steps” scaffold; rarely a real worked solution |
| Practice attempted | `EV-RT-06` | Behavioural | **High (default path)** | Free-text response; no authorised scoring |
| Practice correct / incorrect | `EV-RT-07` / `EV-RT-08` | **Educational** | **Near zero** | Builder supports it; activity engine never sets `scored_correct` |
| Practice partial / unscored | `EV-RT-09` | Behavioural | Occasional | Empty or unscoreable responses |
| Reflection submitted / skipped | `EV-RT-10` / `EV-RT-11` | Behavioural / Informational | Medium | Soft signal; never Twin alone (by design) |
| Confidence reported | `EV-RT-12` | Informational | Low | Soft calibration only |
| Finish Review Yes / Partially / No | `EV-RT-23`–`25` | Behavioural | High when product ON | Honesty ritual — not mastery |
| Structured question results | `EV-RT-40` | Educational | **Reserved / silence** | EIP-002 pathway exists; not wired into daily Session practice |
| Quiz / mission assessment / mock / official | `EV-RT-41`–`44` | Educational → Constitutional | **Reserved / silence** | Catalogue ready; no commercial daily-loop content |

### Authority outcome under commercial defaults

| Package shape | Disposition | Progress | Twin | Student experience |
|---|---|---|---|---|
| Scored practice (`EV-RT-07`/`08`) or structured (`EV-RT-40`) | **Accepted** (Educational+) | Advances | Updates | Learning Insights can thicken |
| Unscored practice (`EV-RT-06`) | **Accepted with Restrictions** | Advances | **Silent** | Journey moves; Insights stay “building” |
| Reading / reflection / duration only | **Rejected** | No | No | Gate outcome language (KWP-002) |
| Finish Review Partially / No | Accepted with Restrictions | No | No | Honest close |

**Density verdict:** Commercial sittings are Behaviourally dense and Educationally sparse. Progress can move on participation. Twin quality, Progress weak-topic quality, and Exam Readiness speech remain starved of Educational+ observations.

### Content source audit

`EducationalSubstancePlanner` builds activities from published package artefacts / mission facts:

| Input available today | How it is used | Educational richness |
|---|---|---|
| Topic title / code | Titles, syllabus refs | Structural only |
| Learning objectives | Reading bullets, practice prompts (“Apply {LO}…”) | Medium — prompts, not assessable items |
| Mission `task_descriptions` | Reading / example walkthrough bullets | Low–Medium — often procedural task lists |
| `educational_rationale` | Reading + example body | Medium — why, not how-to-solve |
| Authorable reading passages | **Not consumed as first-class body** | Gap |
| Worked solutions / mark schemes | **Not present as artefacts** | Gap |
| Answer keys / scoring criteria | **Not present** | Gap — blocks Educational+ |
| Model answers / explanations | Generic stage explanation text only | Gap |
| Structured / MCQ / numeric items | **Not in substance planner** | Gap |

Substance is an honest educational *arc*. It is not yet an assessable educational *corpus*.

---

## Educational+ Opportunity Analysis

### Activities that produce only Behavioural (or weaker) evidence

| Activity | Why Behavioural only | Pathway to Educational+ |
|---|---|---|
| **Reading** | Exposure / engagement by contract | Keep Behavioural; enrich quality for learning — do not inflate grade |
| **Worked example** | Method exposure without demonstrated application | Keep Behavioural for completion; add *follow-on scored check* after example |
| **Unscored free-text practice** | No authorised criteria → `EV-RT-06`/`09` | Add scoreable item types + answer keys → `EV-RT-07`/`08` |
| **Reflection** | Soft metacognition by EV-001A law | Keep soft; improve prompt quality using prior incorrect practice |
| **Finish Review** | Honesty, not understanding | Unchanged |
| **Checklist / duration / clicks** | Telemetry | Never Educational+ |

### Activities that can produce Educational+ without new authorities

| Pathway | Evidence type | Twin? | Progress? | Content dependency |
|---|---|---|---|---|
| Scored practice (correct/incorrect) | `EV-RT-07` / `EV-RT-08` | Yes | Yes (already) | Answer key + scoring adapter in content/activity layer |
| Structured question results | `EV-RT-40` | Yes | Yes | Item bank / package structured items |
| Mission assessment results | `EV-RT-42` | Yes | Yes | Assessment pack content (later) |
| Quiz results | `EV-RT-41` | Yes | Yes | Quiz pack (later) |
| Mock examination results | `EV-RT-43` | Yes (Mastery) | Conditional | Exam-condition content (premium later) |

### Twin / Progress / Readiness impact of denser Educational+

| Consumer | Today (Behavioural-heavy) | With Educational+ density |
|---|---|---|
| **StudentTwinEngine** | Often Initialised / silent Active | Active estimates per topic from scored outcomes |
| **ProgressEngine** | Coverage advances; weak annotations thin | Weak-topic annotations gain Twin estimate inputs |
| **Exam Readiness** | Coverage + soft signals | Evidence-backed drivers students can trust |
| **Learning Insights (KWP-002)** | “Building” empty states dominate | Plain-language strength/weakness after sittings |
| **Mission composition** | Syllabus order + limited estimates | Better “why this Session” from estimate-informed composition inputs |

**Constraint:** Do not change Twin, Progress, or Evidence Authority. Change *what content enters* the existing emission → validation → consumption path.

---

## High-Impact Content Improvements

Prioritised for Twin quality, Progress quality, and Exam Readiness — **content & activity enrichment only**.

### H1 — Scoreable practice items (highest leverage)

**Problem:** Practice is free-text with generic explanations; `record_response_opaque` never passes `scored_correct`.

**Content improvement:**

- Author (or generate-and-certify) per-topic practice items with:
  - prompt bound to learning objective / syllabus code
  - response type: MCQ · numeric · short structured · multi-part
  - authorised answer key / acceptable variants / mark scheme
  - explanation + model answer for post-attempt feedback
- Activity engine scores against key → emit `EV-RT-07` / `EV-RT-08` via existing builder.

**Impact:** Unlocks Educational+ on the daily loop; Twin becomes Active; Insights leave “building.”

**Non-goal:** Do not redefine grade ceilings or Authority columns.

### H2 — Real worked examples (not method scaffolds)

**Problem:** Worked examples are templated restatements (“Restate the objective… Apply to one concrete case”).

**Content improvement:**

- Package artefact: worked example body with given data, step-by-step solution, common pitfall, and syllabus reference.
- Optional **example check** (1–2 scored micro-questions) after walkthrough → Educational+ without pretending example completion is understanding.

**Impact:** Students rehearse exam method; practice becomes comparable; feedback can cite “compare to step 3.”

### H3 — Syllabus-faithful reading density

**Problem:** Reading body ≈ LO bullets + rationale.

**Content improvement:**

- Attach certified reading excerpts / concept notes / formula boxes from published curriculum artefacts.
- Keep completion Behavioural; raise *learning value* so practice and Twin inputs improve downstream.

**Impact:** Session feels like a coach with materials, not a checklist of objectives.

### H4 — Feedback quality (correct / incorrect / model answer)

**Problem:** Stage explanations echo the student’s note; no correctness, no mark scheme, no model answer.

**Content improvement (KWP-001 M4, now content-backed):**

- After scored attempt: outcome label, short explanation, reveal model answer / mark points.
- After unscored attempt (transition period): honest “not yet scored” + model answer for self-check (still Behavioural until scoring exists).

**Impact:** Immediate educational value; higher willingness to finish sittings; clearer Exam Readiness drivers later.

### H5 — Reflection quality (coach prompts from practice outcomes)

**Problem:** Reflection is generic; skip allowed (correct); soft grade by law.

**Content improvement:**

- Structure prompts from sitting facts: incorrect items, skipped stages, low-confidence LOs.
- Capture confidence against named objectives (still Informational/Behavioural).
- Never Twin-score from reflection alone.

**Impact:** Metacognition that prepares tomorrow’s Session; soft readiness calibration.

### H6 — Multiple practice opportunities per sitting

**Problem:** Planner emits ~1–2 LO-derived free-text practices.

**Content improvement:**

- Target 3–5 scoreable items (or 2 scored + 1 extended) per Session for CS1 commercial topics.
- Mix difficulty; keep time-bounded for sustainable progress (Blueprint principle 4).

**Impact:** Evidence density per sitting rises; Twin estimates stabilize faster; Progress weak-topic signal improves.

### H7 — Explanation & model-answer library

**Problem:** No reusable explanation artefacts tied to items.

**Content improvement:**

- Per item: learner explanation, common error note, syllabus “see also.”
- Align with Product Language Guide (no Twin/evidence jargon).

**Impact:** Premium feel vs question banks that only show “correct.”

---

## Assessment Roadmap

Assessment-class types already exist in EV-001A. Phase 3 sequences **content availability** before product chrome.

### Stage A — Daily Session structured practice (now)

| Deliverable | Evidence | Student promise |
|---|---|---|
| Scoreable items inside Session Practice stage | `EV-RT-07`/`08` and/or `EV-RT-40` | “I practised and knew if I was right” |
| Model answer + explanation reveal | Educational+ payload | “I learned from mistakes today” |
| Per-objective attribution | Package metadata | Twin/Progress can attribute topic/LO |

**Authority stance:** Emit through existing Session → Evidence Package path. Prefer `EV-RT-07`/`08` for simple scored practice; use `EV-RT-40` when item shape matches EIP-002 structured question results.

### Stage B — Topic Quick Check packs (near-term)

| Deliverable | Evidence | Student promise |
|---|---|---|
| Short scored sets (5–8 items) on weak topics | `EV-RT-40` / `EV-RT-41` | “Strengthen {topic}” with honest results |
| Report in student language | Same package validation | Sitting Report (KWP-001 premium) |

Compose via existing Mission / Session path — no new Mission AUTHORITY.

### Stage C — Mission assessment & mock (premium later)

| Deliverable | Evidence | Notes |
|---|---|---|
| Mission assessment results | `EV-RT-42` | When assessment packs certified |
| Mock examination results | `EV-RT-43` | Exam-like conditions; Mastery-grade |
| Official examination results | `EV-RT-44` | Constitutional; rare; import path |

**Do not** ship mock/official UI before scoreable daily practice exists — otherwise assessment theatre without daily Educational+.

### Assessment content quality bar

Every assessable item must have:

1. Syllabus / LO binding  
2. Authorised scoring criteria  
3. Learner-facing explanation  
4. Model answer or mark scheme  
5. Deterministic or bounded scoring (no opaque LLM grading in the core path)  

Matches Blueprint: evidence before opinion; deterministic cores; professional quality.

---

## Evidence Quality Roadmap

### Quality ladder (content programmes, not Authority redesign)

| Level | Sitting produces | Twin | Progress | Commercial readiness |
|---|---|---|---|---|
| **L0 — Shell** | Stages without practice | Silent | Blocked / rejected | Lab only |
| **L1 — Behavioural (today)** | Unscored practice + Finish Review | Silent | May advance | Honest coverage; thin Insights |
| **L2 — Educational+ daily** | ≥1 scored correct/incorrect or structured result | Updates | Advances | **Phase 3 target** |
| **L3 — Dense Educational+** | Multi-item scored set + explanations | Stable estimates | Weak topics meaningful | Premium companion |
| **L4 — Assessment density** | Topic checks + occasional mock | Mastery trajectory | Exam pacing credible | Exam Briefing viable |

### Evidence quality workstreams

| ID | Workstream | Outcome |
|---|---|---|
| **EQ-C1** | Item schema in published package / mission artefacts | Authorable scoreable content without engine redesign |
| **EQ-C2** | Scoring adapter in activity/content layer | Sets `scored_correct` / structured payload for existing builder |
| **EQ-C3** | Feedback artefacts (explanation, model answer) | Student-visible quality after attempt |
| **EQ-C4** | Worked-example corpus | Real methods, not scaffolds |
| **EQ-C5** | Reading corpus binding | Syllabus-faithful study material |
| **EQ-C6** | Coverage of CS1 commercial topics | Enough topics at L2+ for a paid cohort dogfood |
| **EQ-C7** | Founder observability of Educational+ rate | % sittings Accepted Educational+ vs Restrictions |

### Non-negotiables (EV-001A)

- Do not inflate Reading / Reflection / Finish Review to Educational+.  
- Do not update Twin from Behavioural-only packages.  
- Prefer silence to fake scoring.  
- Activity remains ≠ understanding until scored observations are Accepted.

---

## Commercial Value Assessment

### Why this phase monetises KWP-002

KWP-002 made the product *speak* like a premium companion. Without Educational+ density, the companion still:

- advances Journey on participation (Integrity Progress softens),  
- leaves Learning Insights empty,  
- cannot defend Exam Readiness with practice outcomes,  
- loses the word-of-mouth claim: “After two weeks I could see where I was weak.”

| Differentiator | Requires Educational+ content |
|---|---|
| Integrity Progress that *feels* earned | Scored practice, not only participation |
| Learning Insights | Twin Active on Educational+ |
| Exam Readiness drivers | Scored outcomes + coverage |
| Sitting Report / weekly Exam Briefing | Dense Educational+ history |
| Weak-topic Strengthen CTA | Estimate-backed annotations |

### Willingness-to-pay signals unlocked by Phase 3

1. **Correctness feedback** — students pay for knowing if they are right.  
2. **Model answers** — exam prep standard; currently missing.  
3. **Visible Journey + Insights movement after real practice** — KWP-002 chrome finally has fuel.  
4. **Syllabus-bound worked examples** — differentiates vs generic banks (Blueprint: not a question bank identity — curriculum-first assessable practice).

### Competitive position

| Competitor pattern | Kwalitec with L2+ content |
|---|---|
| Question bank + streaks | Syllabus Session + scored practice + honest Progress |
| Opaque AI tutor | Deterministic scoring + explainable feedback |
| XP for opening pages | Evidence Gate already blocks theatre — content must match |

### Risk if Phase 3 is skipped

- Commercial Loop ON + Evidence Gate ON + empty Insights → “premium packaging, thin learning.”  
- Twin silence misread as broken personalisation (KWP-001/002 residual risk).  
- Coverage advances without understanding → trust erosion when Exam Readiness stays flat.

**Estimated commercial effect (provisional):** Phase 3 is the highest Δ perceived student value remaining without new authorities. CRI domains CR3 (study loop reliability) and CR4 (explainability) move when scored feedback + Insights activate; pass-probability marketing remains constrained by Vision/Blueprint.

---

## Implementation Priority

Impact × effort for content enrichment. **No runtime authority redesign.**

| Priority | Item | Impact | Effort | Depends on |
|---|---|---|---|---|
| **P0** | Scoreable practice item schema + CS1 seed set (high-traffic topics) | Critical | M–L | Package / curriculum artefacts |
| **P0** | Wire activity scoring → existing `scored_correct` / `EV-RT-07`/`08` emission | Critical | M | Item schema; **no Authority change** |
| **P0** | Model answer + explanation reveal on activity feedback | Critical | M | Item artefacts |
| **P1** | Real worked examples for seeded topics | High | M–L | Content authoring / certification |
| **P1** | Multi-item practice density (3–5) per Session | High | M | Item bank depth |
| **P1** | Founder metric: Educational+ accept rate per sitting | High | S | Observability / Feedback Hub |
| **P2** | Syllabus reading binding (certified excerpts) | Medium–High | L | Curriculum content pipeline |
| **P2** | Reflection prompts from incorrect practice | Medium | S–M | Scored outcomes available |
| **P2** | `EV-RT-40` structured question packaging for richer items | Medium–High | M | EIP-002 alignment; content |
| **P3** | Topic Quick Check packs + weak-topic Session composition | Medium–High | L | P0–P1 density |
| **P3** | Mission assessment / mock content packs | Medium | L | Assessment roadmap Stage C |
| **P4** | Full CS1 L2+ coverage + Exam Briefing fuel | Premium | L | Sustained content programme |

### Suggested sequencing

```
Week 1–2:   P0 schema + scoring wire + feedback reveal (pilot topics)
Week 3–6:   P0/P1 seed CS1 topics to L2; worked examples; density 3–5
Month 2:    P2 reading + reflection quality; Educational+ rate dashboard
Month 3:    P3 Quick Checks on weak topics; expand coverage
Later:      P4 / KWP-004 Assessment Mode + Exam Briefing content fuel
```

### Explicit non-goals

- Redesign LearningSessionRuntime  
- Redesign EducationalEvidenceAuthority  
- Redesign ProgressEngine  
- Redesign StudentTwinEngine  
- Inflate Behavioural stages to Educational+ by policy change  
- Opaque LLM grading in the core Educational+ path  

---

## Recommendation for KWP-004

### Name

**KWP-004 — Assessable Practice Activation** (working title)

### Mandate

Implement the P0/P1 content path so commercial Sessions routinely emit Accepted Educational+ evidence: scoreable package items, activity-layer scoring into the existing evidence builder, model-answer feedback, and a CS1 seed corpus — still without changing Evidence / Progress / Twin / Session authorities.

### Definition of done (draft)

1. ≥N commercial CS1 topics (Board-set) ship with scoreable practice + model answers.  
2. Typical Finish Review Yes sitting with practice yields **Accepted** (Educational+), not only Accepted with Restrictions.  
3. Twin becomes **Active** after first scored sitting under Commercial Loop.  
4. Student sees correct/incorrect + explanation + model answer without engine jargon.  
5. Founder dashboard shows Educational+ vs Behavioural sitting rates.  
6. Completion report includes Student Impact Assessment and evidence of Twin/Progress quality improvement from content alone.

### What KWP-004 is not

Not another singularity. Not Assessment Mode chrome alone. Not Exam Briefing marketing. Those consume the Educational+ fuel KWP-004 creates.

### Optional immediate follow-on after KWP-004

- **KWP-005** — Assessment Mode & Sitting Reports (Stage B/C surfaces)  
- **KWP-006** — Exam Briefing (presentation aggregation over dense Educational+ history)

---

## Audit Area Scorecard

| Audit area | Current | Educational+ capable? | Phase 3 action |
|---|---|---|---|
| Practice activities | Free-text, unscored | Yes — with keys | **P0 score + seed** |
| Worked examples | Template scaffolds | Indirect (example checks) | **P1 real examples** |
| Structured questions | Catalogue reserved | Yes (`EV-RT-40`) | **P2 wire with content** |
| Reflection quality | Generic / skip OK | No (by law) | Improve prompts only |
| Assessment activities | Reserved silence | Yes (later types) | After daily L2 |
| Feedback quality | Generic stage copy | Yes | **P0 model answers** |
| Model answers | Absent | Yes | **P0 artefact** |
| Explanation quality | Thin | Yes | Bundle with items |
| Scoring opportunities | Builder ready; content empty | Yes | **P0 scoring wire** |

---

## Architecture Compliance

| Invariant | Stance |
|---|---|
| LearningSessionRuntime sole Session AUTHORITY | Unchanged |
| EducationalEvidenceAuthority sole Evidence AUTHORITY | Unchanged — richer candidates only |
| StudentTwinEngine estimate AUTHORITY | Unchanged — more Educational+ to observe |
| ProgressEngine sole Progress AUTHORITY | Unchanged — same authorisation columns |
| Curriculum V1/V2 | Content must remain syllabus-faithful for both where published |
| Blueprint | Outcomes before engagement; evidence before opinion; not a question bank identity |

**This roadmap does not modify application code.** It defines Phase 3 content strategy for programmes that enrich educational material flowing through the completed architecture.

---

## Closing

SR-001A built the Educational Operating System.  
KWP-001 audited student value.  
KWP-002 activated the commercial experience.  

**KWP-003’s finding:** the commercial product is now content-constrained. Enrich assessable educational content so Educational+ evidence becomes the daily default — and Twin, Progress, and Exam Readiness finally receive the observations the architecture was built to honour.

> Architecture complete. Evidence hungry. Feed the loop.

---

**Document status:** Complete — KWP-003 audit / roadmap deliverable  
**Next programme:** KWP-004 Assessable Practice Activation (recommended)  
**Architecture stance:** SR-001A authorities unchanged; content & evidence-density expansion only  

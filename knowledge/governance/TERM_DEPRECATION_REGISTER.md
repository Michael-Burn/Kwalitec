# Term Deprecation Register

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.1 — Canonical Educational Lexicon  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** `CANONICAL_EDUCATIONAL_LEXICON.md`  
**Companions:** `EDUCATIONAL_VOCABULARY_MAP.md`, `EDUCATIONAL_LANGUAGE_STYLE_GUIDE.md`

---

## Purpose

Record every educational term **approved for retirement** from student-facing primary vocabulary, with reason and migration guidance.

Deprecation here is **governance**. No templates or product strings are changed in DG-001.1.

**Status values:** Approved for retirement · Contained (flag OFF) · Soft-deprecate (prefer alternatives) · Keep internal-only

---

## Register

### DEP-01 — tip / Mission tip (primary daily-focus noun)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | tip; Mission tip; “Why this tip?” |
| **Reason** | Same authorised focus named tip alongside Mission / Session / Recommendation — ED-02 / ED-06 / ED-07 / IR-08. Informal productivity slang, not educational vocabulary. |
| **Replacement** | **Mission** (today's focus); **Recommendation** (decision object); **Guidance** (umbrella / explanation eyebrow) |
| **Migration guidance** | Home / Journal / Timeline / commitment continuity: replace tip with Mission or guidance by context. Explanation disclosure: “Why this guidance?” or “Why this Mission?” |
| **Surfaces known** | Explanation card; Journal empty; Timeline narrative; commitment continuity |
| **Status** | Approved for retirement |
| **Blocks** | Unqualified “one Study Sensei noun” claim |

---

### DEP-02 — Today's Session as synonym for Mission

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Today's Session *when used to mean today's educational focus* (synonym collision with Today's Mission) |
| **Reason** | PX-002A treated Session and Mission as competing labels for one concept. DG-001.1-D02 separates them: Mission = focus; Session = practice. |
| **Replacement** | **Today's Mission** for focus; **Session** / “Start today's Session” for practice CTA |
| **Migration guidance** | Product Language Guide / `product_language.py` reconciliation is a future implementation programme. Until then: new educational copy follows Mission-led lexicon; do not add new “Today's Session” hero labels. |
| **Surfaces known** | PX CTAs; product_language REJECTED_SYNONYMS; Help Session OS framing |
| **Status** | Approved for retirement *(as synonym)* — Session itself remains canonical for practice |
| **Blocks** | ED-02 closure |

---

### DEP-03 — Today's Recommendation as Home hero focus label

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Today's Recommendation *(as primary Home educational eyebrow for the daily focus)* |
| **Reason** | Third synonym for Mission — noun storm. Recommendation remains valid for the decision object. |
| **Replacement** | Today's Mission (focus); keep “recommendation” in explanations / commitment / Feedback Loop where the decision object is meant |
| **Migration guidance** | `recommendation_card.html` and related macros: hero → Mission; body may still say recommendation |
| **Surfaces known** | Recommendation card macro |
| **Status** | Soft-deprecate (prefer Mission for hero) |
| **Blocks** | Partial — medium educational confusion |

---

### DEP-04 — the system / the algorithm / the engine (narrator)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | the system chose; the algorithm; the engine (as student-facing agents) |
| **Reason** | Replaces Study Sensei with robotic authority — IR / ED-11 |
| **Replacement** | Study Sensei; Why this Mission?; Why this guidance? |
| **Migration guidance** | Rename Runtime C panel before any enablement |
| **Surfaces known** | Runtime C summary (flag OFF) |
| **Status** | Contained (flag OFF) — must retire before enable |
| **Blocks** | Runtime C enablement |

---

### DEP-05 — Dashboard (learner landing)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Dashboard (learner UI for landing) |
| **Reason** | PX-002A trust friction; Home is canonical |
| **Replacement** | Home |
| **Migration guidance** | Already largely enforced; legacy Learning Workspace may retain label while phased out |
| **Surfaces known** | Legacy dashboard templates |
| **Status** | Approved for retirement (learner canonical path) |
| **Blocks** | None for Alpha sole-runtime |

---

### DEP-06 — Analytics (learner history)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Analytics (learner nav / history surface) |
| **Reason** | Founder term; learner surface is History |
| **Replacement** | History |
| **Migration guidance** | Keep Analytics for Founder Command Centre only |
| **Surfaces known** | Historical nav; PX-002A fixed canonical |
| **Status** | Approved for retirement (learner) |
| **Blocks** | None for Alpha sole-runtime |

---

### DEP-07 — Archive (primary History name)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Archive as primary student name for History-class surface |
| **Reason** | Unified Journey alternate; History is PX-canonical |
| **Replacement** | History |
| **Migration guidance** | Do not reintroduce Archive nav while Unified Journey remains OFF |
| **Surfaces known** | Unified Journey nav (flag OFF) |
| **Status** | Contained |
| **Blocks** | Unified Journey enablement without rename review |

---

### DEP-08 — Study Session / Learning Session (as required UI label)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Learning Session; Study Session *as mandatory distinct UI product name* |
| **Reason** | PX one-name rule — Session is enough |
| **Replacement** | Session |
| **Migration guidance** | “Study Session” allowed in Help prose as plain language; not as competing product noun |
| **Surfaces known** | Product Language Guide rejected synonyms |
| **Status** | Soft-deprecate |
| **Blocks** | None |

---

### DEP-09 — Roadmap / Progress Path / Learning Path / Curriculum Graph (learner)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Roadmap; Progress Path; Learning Path; Curriculum Graph (student UI) |
| **Reason** | Journey is canonical syllabus progress surface |
| **Replacement** | Journey |
| **Migration guidance** | Keep graph language internal/engineering only |
| **Surfaces known** | Product Language Guide |
| **Status** | Approved for retirement (learner) |
| **Blocks** | None |

---

### DEP-10 — Twin Insights / Digital Twin / Mastery Score / Student Analysis (learner labels)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Twin Insights; Digital Twin; Mastery Score; Student Analysis (as learner UI) |
| **Reason** | Engine / identity language |
| **Replacement** | Learning Insights; Exam Readiness; understanding / evidence language |
| **Migration guidance** | Enforce via presentation reviews |
| **Surfaces known** | Product Language Guide internal ban list |
| **Status** | Approved for retirement (learner) |
| **Blocks** | Sensei voice claims if reintroduced |

---

### DEP-11 — Remediation / Intervention (learner Revision)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Remediation; Intervention (learner UI) |
| **Reason** | Clinical / deficit tone; Revision is educational |
| **Replacement** | Revision |
| **Migration guidance** | Keep clinical terms out of student copy |
| **Surfaces known** | Product Language Guide |
| **Status** | Approved for retirement (learner) |
| **Blocks** | None |

---

### DEP-12 — AA forbidden anxiety / identity terms

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Exam; Test; Pass; Fail; Weak; Strong student; Poor performance *(on Adaptive Assessment student resources)* |
| **Reason** | ILE-001A anxiety-safe law |
| **Replacement** | Quick Check / Deep Check / learning check; complete; needs reinforcement; thin evidence |
| **Migration guidance** | Enforced in AA terminology validator; out-of-AA Exam Readiness / exam date remain planning vocabulary with care |
| **Surfaces known** | AA copy registry |
| **Status** | Approved for retirement (AA scope) |
| **Blocks** | AA CI if reintroduced |

---

### DEP-13 — Engagement theatre in Sensei speech

| Field | Detail |
|-------|--------|
| **Deprecated terms** | streak guilt; broke your streak; FOMO; destiny “you will pass” as guidance |
| **Reason** | Constitution / Sensei philosophy — not educational honesty |
| **Replacement** | Consistency / sustainable rhythm; estimated readiness |
| **Migration guidance** | Keep streak metrics out of Sensei surfaces (legacy analytics may still export) |
| **Surfaces known** | Commitment / feedback guards; legacy analytics |
| **Status** | Approved for retirement (Sensei speech) |
| **Blocks** | Trust / educational consistency claims |

---

### DEP-14 — mastered (History identity)

| Field | Detail |
|-------|--------|
| **Deprecated terms** | mastered *(as student History identity label)* |
| **Reason** | Implies Mastery badge; prefer completed topics |
| **Replacement** | Completed topics; solid evidence; well-supported understanding |
| **Migration guidance** | Prefer “completed” in new History copy |
| **Surfaces known** | History |
| **Status** | Soft-deprecate |
| **Blocks** | None |

---

### DEP-15 — Product Check-in called “reflection”

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Calling Product Check-in educational reflection |
| **Reason** | ED-18 — false cousin of Sensei / Session reflection |
| **Replacement** | Product Check-in / research feedback |
| **Migration guidance** | Disclose research purpose in UI/Help |
| **Surfaces known** | Alpha research |
| **Status** | Approved for retirement (as reflection synonym) |
| **Blocks** | ED-03 map clarity |

---

### DEP-16 — Kwalitec as educational mentor name on Sensei surfaces

| Field | Detail |
|-------|--------|
| **Deprecated terms** | Kwalitec speaking *as* the mentor on Journal / Timeline / Mission Intelligence |
| **Reason** | ED-01 dual narrator |
| **Replacement** | Study Sensei on those surfaces; Kwalitec on product/support |
| **Migration guidance** | Onboarding handoff sentence; Help glossary |
| **Surfaces known** | Onboarding vs Journal split |
| **Status** | Approved for retirement *(role misuse)* — brand name itself remains |
| **Blocks** | One Study Sensei identity claim |

---

## Migration priority (for future programmes)

1. DEP-01 tip → Mission / Guidance  
2. DEP-02 Session≠Mission synonym fix + PX reconciliation  
3. DEP-16 / ED-01 narrator handoff  
4. DEP-03 Recommendation hero → Mission  
5. DEP-04 before Runtime C ON  
6. Remaining soft-deprecations opportunistically  

---

## What is *not* deprecated

| Term | Note |
|------|------|
| Mission | Canonical educational focus |
| Session | Canonical practice workflow |
| Recommendation | Canonical decision object |
| Guidance | Canonical umbrella |
| Study Sensei / Kwalitec | Both canonical in distinct roles |
| Decision Journal / Educational Timeline / History | Distinct archive layers |
| Exam Readiness | Canonical readiness label (estimated) |
| Calibration | Canonical declarations (≠ mastery) |

---

**End of TERM_DEPRECATION_REGISTER**

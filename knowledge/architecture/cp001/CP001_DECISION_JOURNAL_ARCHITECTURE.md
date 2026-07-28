# CP-001 — Decision Journal Capability Architecture

**Programme:** CP-001 — Capability Programme  
**Version:** 1.0  
**Status:** Active — Decision Journal capability architecture (design only)  
**Effective:** 2026-07-28  
**Change class:** Architecture & Product Capability  
**Constraint:** No application behaviour, schema, recommendation algorithms, or UI modified by this programme.

---

## 1. Purpose

Define the **Decision Journal** as a durable Student Intelligence capability: the primary evidence source that records, explains, and evaluates meaningful student decisions throughout the learning journey.

The Decision Journal connects four product facts that must remain joinable without inventing a second educational brain:

1. **What guidance was offered** (recommendation + explanation)  
2. **What the student chose** (accept / defer / reject / dismiss + optional rationale)  
3. **What learning behaviour followed** (start / complete / revise / recover)  
4. **What outcomes can be measured later** (OM-001 L1…L5)

This package is **capability architecture only**. It does not implement collectors, change ranking, or amend Twin authority.

---

## 2. Authority and non-contradiction

| Authority | Binding effect |
|-----------|----------------|
| **Vision 2030** | Agency, reflection, recommendation acceptance as success substrate; never-build opaque AI / coercive habits |
| **OA-001 Product Constitution** | PC-01 trust; PC-03–PC-04 claims ≤ evidence; PC-09 determinism; PC-11 agency; PC-12 STOP |
| **SI-001** | Student Intelligence capability map; Decision Journal as measurement / agency substrate for SI-C2, SI-C5, SI-C7, SI-C8, SI-C9 |
| **OM-001** | Outcome layers; guidance causal chain; OM-REC-* / OM-EXP-* / OM-REF-* catalogue IDs |
| **P-001.2 Explainability Standard** | Mandatory explanation schema frozen into journal memory |
| **P-001.3 Recommendation Quality Standard** | Acceptance / effectiveness measurement law for recommendations |
| **Student Digital Twin Constitution** | Understanding ≠ certainty; journal must not mint mastery or destiny |
| **ILE-002 Decision Journal** | Product philosophy, entry lifecycle, retention baseline for the current educational memory store |
| **ILE-011 Student Decision Framework** | Decision ownership; Sensei proposes; student acts |

**Conflict rule:** Vision 2030 and Educational Constitution win on philosophy and educational meaning. Twin Constitution wins on understanding vs certainty. OA-001 wins on claim discipline. OM-001 wins on outcome semantics. ILE-002 remains the product educational-memory baseline. CP-001 specialises *capability architecture* for SI/OM integration; it does not soft-amend those authorities.

---

## 3. Capability definition

### 3.1 What the Decision Journal is

The Decision Journal is the **authoritative educational memory of meaningful student decisions** under Student Intelligence.

| Property | Meaning |
|----------|---------|
| **Educational memory** | Persists significant guidance interactions as a student-safe narrative arc |
| **Agency record** | Captures accept / defer / reject / dismiss without shame or coercion scoring |
| **Explainability freeze** | Stores what / why / evidence / confidence / next / uncertainty at decision time |
| **Outcome substrate** | Supplies OM-001 guidance-chain and completeness metrics (e.g. OM-REC-03…10) |
| **Twin input (provisional)** | May emit *behaviour / preference* signals for Twin understanding — never Estimated Knowledge |

### 3.2 What the Decision Journal is not

| Not | Why |
|-----|-----|
| Telemetry / clickstream | Activity vanity is Product Analytics territory |
| Recommendation engine | Ranking / selection remain SI-C2 / Decision Engine owners |
| Twin / Educational State | Understanding model remains Twin; journal does not invent mastery |
| Second educational truth | Runtime A facts remain write authority for educational evidence |
| Product Decision Register | Board/product decisions are organisational, not learner memory |
| Coercive scorecard | Refusal and deferral are lawful agency, not failure identity |

### 3.3 Relationship to ILE-002 (baseline substrate)

ILE-002 implements the current learner Decision Journal (domain, persistence, service, student chronology).

| Layer | Owner |
|-------|-------|
| Product educational memory (current) | ILE-002 philosophy + runtime store |
| Capability architecture (SI/OM integration) | **This programme (CP-001)** |
| Outcome metric semantics | OM-001 |
| Twin consumption of decision signals | Twin Constitution + future ADR-gated programmes |

CP-001 **does not** reopen ILE-002 implementation, schema, or UI. Future enhancement programmes must cite CP-001 architecture + ADR (PC-06) before structural change.

---

## 4. Placement in Student Intelligence

### 4.1 Capability map placement

Decision Journal is a **cross-cutting capability substrate**, not a eleventh SI capability ID. It serves:

| SI capability | Journal role |
|---------------|--------------|
| **SI-C2** Recommendation Engine | Accept / defer / reject capture; Shown→…→Completed chain |
| **SI-C5** Reflection Intelligence | Optional reflection attachment; non-coercive loop close |
| **SI-C7** Explainability | Permanent freeze of explanation schema at guidance time |
| **SI-C8** Learning analytics | Source of truth for decision completeness (OM-REC-10) |
| **SI-C9** Outcome measurement | Primary L1 guidance evidence pack substrate |
| **SI-C1** Digital Twin | Optional behaviour/preference inputs only (provisional) |
| **SI-C4** Mission Intelligence | Mission present / commit / complete moments when mirrored |

### 4.2 Layering (normative)

```
Templates/JS → Blueprints → Services → Models + Curriculum Engine → DB/JSON
                     ↑
         Decision Journal Capability (educational memory service)
                     ↑
         Recommendation / Insight presentation (communication)
                     ↑
         Twin Foundation (understanding — may read journal signals)
                     ↑
         Runtime A evidence / educational writes
```

| Layer | May | Must not |
|-------|-----|----------|
| Presentation | Show chronology; capture choice / optional rationale | Rank recommendations; invent mastery |
| Blueprints | Authz, forms, ownership scope | Planning / recommendation math |
| Decision Journal service | Persist arcs; append evidence; enforce student-safe text | Depend on `flask.request` globals; mutate Twin mastery |
| Twin | Interpret lawful journal signals as behaviour evidence | Treat accept rates as certainty of understanding |
| Curriculum Engine | Topic ids via CurriculumService | Own student decision state |

Preserves ARCHITECTURE.md layering and curriculum V1/V2 traversability.

---

## 5. Target information flow

```
Eligible guidance shown (+ P-001.2 explanation)
        ↓
Decision Journal entry created (recommended)
        ↓
Student choice recorded (accept / defer / reject / dismiss)
   + optional student rationale
        ↓
Append-only evidence / behaviour events
        ↓
Optional reflection (SI-C5; consented; non-coercive)
        ↓
Outcome linkage (Mission complete, practice evidence, readiness delta — when known)
        ↓
OM-001 metric packs (OM-REC-*, OM-EXP-*, OM-REF-*)
        ↓ (lawful, provisional)
Twin behaviour / preference understanding inputs
```

**OM causal chain alignment** (`OM001_OUTCOME_MODEL` §8): Journal records the early and mid stages of Shown → Understood → Accepted → Started → Completed → Learning movement. Later stages remain owned by Evidence / Twin / research — journal links, it does not invent learning depth.

---

## 6. Decision lifecycle (capability)

Normative stages for every **eligible** recorded decision. Detail entities: `CP001_DOMAIN_MODEL.md`. Product vocabulary alignment: ILE-002 `ENTRY_LIFECYCLE.md`.

```
Eligible / Recommended
        ↓
Choice captured (Accepted | Deferred | Rejected | Dismissed)
        ↓
Evidence evolving (append-only)
        ↓
Reflection (optional | not_applicable)
        ↓
Outcome recorded (when knowable)
        ↓
Evaluated for measurement (OM packs)
        ↓
Archived (soft; readable)
```

| Invariant | Rule |
|-----------|------|
| **Immutable guidance snapshot** | Original observation / meaning / recommendation text never rewritten |
| **Append-only evidence** | New facts append; history is not edited |
| **Agency preserved** | Defer / reject / dismiss are first-class lawful outcomes |
| **No shame semantics** | Lifecycle and UI language never treat refusal as character failure |
| **Educational purpose required** | Every entry declares a purpose code (see §8) |
| **Soft archive** | Archive never deletes educational memory |

---

## 7. Recommendation acceptance / rejection capture

### 7.1 Disposition vocabulary (capability)

| Disposition | Meaning | OM mapping |
|-------------|---------|------------|
| **Accept** | Student agrees to pursue the recommended action | OM-REC-03 numerator |
| **Defer** | Student postpones; may revisit | OM-REC-04 |
| **Reject** | Student explicitly declines this guidance | OM-REC-05 |
| **Dismiss** | Student sets aside without detailed reject (UI may collapse to deferred posture for continuity) | OM-REC-05 / product policy |
| **None yet** | Guidance shown; choice not recorded | Completeness gap (OM-REC-10) |

### 7.2 Capture requirements (design)

1. Every **eligible** student-facing primary recommendation that ships under P-001.3 must be journal-eligible.  
2. Capture must distinguish **shown** from **acted** (impressions ≠ acceptance).  
3. Time-to-start and accept→complete remain **linked** via outcome events or Mission/Session ids — not inferred from clicks alone.  
4. Chronic dismiss-without-alternative remains a **quality failure signal** (OM-REC-09), not a student blame signal.  
5. Capture must not coerce choice (PC-11). Silent auto-accept is forbidden.

Detail rationale model: `CP001_DOMAIN_MODEL.md` § Student Rationale.

---

## 8. Educational value model

Every recorded decision must have a **traceable educational purpose**. Purpose is not marketing copy; it is the educational reason the interaction was worth remembering.

### 8.1 Purpose codes (closed catalogue)

| Code | Educational purpose | Typical SI link |
|------|---------------------|-----------------|
| **EV-NEXT** | Highest-value next study action under scarce time | SI-C2 |
| **EV-REVISE** | Weak-topic / revision timing repair | SI-C2, SI-C6 |
| **EV-MISSION** | Authoritative Mission / Session commitment | SI-C4 |
| **EV-RECOVER** | Resume / recovery after abandon or missed study | SI-C4 |
| **EV-READY** | Readiness honesty / pacing honesty (advisory) | SI-C3 |
| **EV-REFLECT** | Optional reflection closing the learning loop | SI-C5 |
| **EV-MILESTONE** | Learning milestone worth continuity memory | SI-C8 |
| **EV-REFUSE** | Lawful silence or refusal of fabricated certainty (system or student) | SI-C7 |

### 8.2 Value test (Final Test aligned)

A journal entry is educationally valuable when **all** hold:

1. It reduces future decision noise or strengthens continuity of guidance.  
2. It preserves explainability for a past recommendation (trust).  
3. It enables honest measurement of guidance usefulness without activity vanity.  
4. It never shames the student or invents mastery from the choice alone.

Entries that fail the value test must not be written (prefer silence over journal spam).

### 8.3 Non-value (forbidden journal content)

- Raw item answers / micro-telemetry  
- Engagement theatre (streaks-as-success identity)  
- Internal ranking dumps, warrant ids, Twin enums on student surfaces  
- Preference writes that mutate Estimated Knowledge  
- Coercive “you failed to accept” scoring artefacts

---

## 9. Reflection integration

Aligned with SI-001 §6.5 Reflection Intelligence and OM-REF-*.

```
Session / Mission outcome
        ↓
Optional ReflectionExperience (presentation)
        ↓ (consented, optional)
Reflection attached to Decision Journal entry
        ↓
Typed reflection evidence (when ADR allows Twin write)
        ↓
Explainable effect on *next* guidance (never coercive ranking)
```

| Rule | Meaning |
|------|---------|
| Optional | Reflection participation must not gate Mission completion |
| Sensitive | Reflection free text is privacy-elevated (`CP001_PRIVACY_MODEL.md`) |
| Non-mastery | Feelings alone never mint Estimated Knowledge |
| Linkage | Reflection references journal entry id; does not rewrite guidance snapshot |
| Measurement | OM-REF-* forbid coercion-as-success |

Horizon note: Twin write expansion from reflection remains **ADR-gated** (SI-H3 primary).

---

## 10. Digital Twin inputs

Per Twin Constitution: journal contributes to **Behaviour** (and optionally preference constraints), not Knowledge certainty.

| Allowed Twin input (design) | Forbidden |
|-----------------------------|-----------|
| Acceptance / deferral / rejection patterns as study behaviour | Treating accept rate as mastery |
| Stated rationale tags (structured) when consented | Opaque psych profiling from free text |
| Mission commit / complete continuity signals | Destiny / exam-pass claims from journal alone |
| Sparse-evidence honesty when student rejected overclaim | Inventing confidence from silence |

Journal → Twin is **read of signals**, never journal-owned Twin mutation of educational truth. Preference ≠ mastery (ILE-002 / Twin Constitution Art. V posture).

Detail: `CP001_TRACEABILITY_MODEL.md` § Twin.

---

## 11. Outcome Measurement linkage

| OM artefact | Journal contribution |
|-------------|----------------------|
| Outcome Model L1 | Primary substrate for guidance outcomes |
| Causal chain §8 | Records Shown / Understood(frozen) / Accepted / Started / Completed links |
| OM-REC-01…10 | Impression, disposition, completeness, effectiveness chain |
| OM-EXP-* | Frozen schema compliance sampling source |
| OM-REF-* | Reflection attachment participation / usefulness |
| Evidence Requirements | Decision Journal packs for “recommendations are useful” claims |
| OM-H1 instrumentation | Completeness (OM-REC-10) is first-class design target |

**Claim honesty:** Journal completeness supports L1 claims. It never alone proves L4 north-star exam outcomes.

---

## 12. Privacy and retention (summary)

| Topic | Architecture posture |
|-------|----------------------|
| Ownership | Student-scoped educational data |
| Minimisation | Significant decisions only; no clickstream in journal |
| Reflection | Elevated sensitivity; default care on free text |
| Retention | Account-lifetime educational memory by default (ILE-002); erasure via future privacy programme |
| Research extracts | Opaque keys; no PII on trial DTOs (OM Measurement Standard §10) |
| Soft archive | Never silent purge for storage hygiene |

Detail: `CP001_PRIVACY_MODEL.md`.

---

## 13. Explainability linkage (summary)

Every journal entry freezes a P-001.2-compatible educational arc at guidance time. Student UI may show Level 1/2; Level 3 remains opt-in / operator. AI must not invent post-hoc reasons into historical entries.

Detail: `CP001_EXPLAINABILITY_INTEGRATION.md`.

---

## 14. Multi-horizon capability roadmap (design)

| Horizon | Intent | Dominant work | Gate |
|---------|--------|---------------|------|
| **DJ-H0** | Freeze capability architecture (this programme) | Domain, privacy, explainability, OM/SI traceability | Docs-only |
| **DJ-H1** | Measurement readiness under invite-only Alpha | Completeness vs eligible guidance; OM-REC-* adoption; rationale capture design | ER-002 claim class; no Twin-live marketing |
| **DJ-H2** | Closed-loop evaluation | Outcome linkage quality; accept→learning movement windows | OM-H2/H3 evidence packs; ADR for schema |
| **DJ-H3** | Reflection → Evidence maturity | Lawful reflection evidence into Twin under SI-C5 | ADR + privacy review |
| **DJ-H4** | Longitudinal decision trajectories | Multi-exam / retention research with consent | L4 ethics / privacy |

Ordering: completeness and explainability freeze (H1) before Twin write expansion (H3) and longitudinal research (H4).

---

## 15. Cross-cutting invariants

1. **Student agency** — guidance proposes; student decides (PC-11; ILE-011).  
2. **Deterministic cores untouched** — journal records decisions; it does not re-rank (PC-09).  
3. **One Educational State** — journal is memory, not a parallel mastery brain.  
4. **Claims ≤ evidence** — acceptance ≠ learning; completion ≠ mastery (OM-001).  
5. **Curriculum V1/V2** — topic references remain CurriculumService-faithful.  
6. **ADR before structural change** (PC-06).  
7. **No opaque LLM authority** over journal meaning or post-hoc explanation invention.  
8. **Never rewrite history** — append-only evidence.

---

## 16. Explicit non-goals (CP-001)

- Implementation of new collectors, schema migrations, or UI  
- Modification of recommendation algorithms or Twin authority flags  
- Amendment of Vision 2030, Twin Constitution, SI-001, or OM-001 in place  
- Declaring OM-REC completeness achieved in production  
- Enabling educational trials or expanding advisory fields  
- Replacing ILE-002 product philosophy documents  

---

## 17. Related artefacts

| Artefact | Path |
|----------|------|
| Domain Model | `CP001_DOMAIN_MODEL.md` |
| Explainability Integration | `CP001_EXPLAINABILITY_INTEGRATION.md` |
| Privacy Model | `CP001_PRIVACY_MODEL.md` |
| Traceability Model | `CP001_TRACEABILITY_MODEL.md` |
| Completion Report | `CP001_COMPLETION_REPORT.md` |
| ILE-002 Philosophy | `knowledge/product/ILE-002/DECISION_JOURNAL_PHILOSOPHY.md` |
| SI-001 Architecture | `knowledge/architecture/si001/SI001_STUDENT_INTELLIGENCE_ARCHITECTURE.md` |
| OM-001 Outcome Model | `knowledge/architecture/om001/OM001_OUTCOME_MODEL.md` |
| OM Metric Catalogue | `knowledge/architecture/om001/OM001_METRIC_CATALOGUE.md` |

---

**End of CP001_DECISION_JOURNAL_ARCHITECTURE**

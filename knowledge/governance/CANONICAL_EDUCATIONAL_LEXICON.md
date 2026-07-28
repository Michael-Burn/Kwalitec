# Canonical Educational Lexicon

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.1 — Canonical Educational Lexicon  
**Version:** 1.0  
**Status:** Active — Board-approved educational vocabulary  
**Effective:** 2026-07-28  
**Authority:** Educational Governance (DG-001); subordinate to Vision 2030, Educational Constitution, Study Sensei Philosophy (ILE-010)  
**Companions:** `EDUCATIONAL_VOCABULARY_MAP.md`, `TERM_DEPRECATION_REGISTER.md`, `EDUCATIONAL_LANGUAGE_STYLE_GUIDE.md`  
**Upstream evidence:** RP-001.3 Terminology Register; RP-001.5 Educational Drift Register (ED-01–ED-04)

---

## Purpose

Establish the **single authoritative educational vocabulary** for Kwalitec.

Every student-facing educational surface must eventually use these terms. This document is governance law for educational naming — it does **not** change application behaviour, templates, or copy in this package.

**Success criterion:** If every student-facing educational word disappeared tomorrow, the Board could recreate the entire educational vocabulary consistently from this lexicon and its companions.

---

## Educational vocabulary principles

1. **One concept → one canonical name.**  
2. **Different concepts must not share the same wording.**  
3. **Educational language preferred over productivity language.**  
4. **Evidence-based wording preferred over certainty.**  
5. **Product language and educational language remain distinct.**  
6. **Student-facing terminology supports long-term mastery.**  
7. **Deprecated synonyms must be explicit** — never silent.

---

## Authority split (resolved ED-01)

| Layer | Canonical term | Role |
|-------|----------------|------|
| Product brand | **Kwalitec** | Company, product, Alpha, auth, support, legal |
| Educational mentor | **Study Sensei** | Guidance, memory, reflection, mission briefs, silence |
| Neutral chrome | *(unnamed)* | System status, CSRF, session-not-found — calm, not mentor theatre |

**Board decision DG-001.1-D01:** Study Sensei is how Kwalitec guides daily learning decisions. Kwalitec is never a second tutor. Study Sensei is never the product brand on legal/support surfaces.

**Required handoff sentence (future copy programmes):**  
> “Study Sensei is how Kwalitec guides your daily learning decisions.”

---

## Lexicon entries

For each concept: canonical term · definition · educational purpose · student-facing meaning · first introduction · owner · approved synonyms · deprecated terms · future implementation notes.

---

### 1. Study Sensei

| Field | Decision |
|-------|----------|
| **Canonical term** | Study Sensei |
| **Definition** | The trusted educational mentor narrator that observes evidence, guides the next highest-value learning action, explains why, and remembers guidance over time. |
| **Educational purpose** | Give the learner one calm professional relationship for educational decisions. |
| **Student-facing meaning** | “The guide that helps me decide what to study and remembers what we decided.” |
| **First point of introduction** | Onboarding (one explicit sentence); then Journal, Timeline, Mission Intelligence, Feedback Loop. |
| **Approved owner** | ILE-010 Study Sensei Philosophy; ILE-001C0 Communication Framework |
| **Approved synonyms** | the Sensei (after first introduction); we (Sensei + learner), sparingly |
| **Deprecated terms** | the system; the algorithm; the engine; AI tutor (as product identity); chatbot |
| **Future implementation notes** | Name Sensei on first educational orientation; keep Kwalitec for product chrome. Remediates ED-01 / IR-01. |

---

### 2. Kwalitec

| Field | Decision |
|-------|----------|
| **Canonical term** | Kwalitec |
| **Definition** | The product and company brand — the software platform and organisation, not the educational mentor. |
| **Educational purpose** | Separate product identity from educational guidance authority. |
| **Student-facing meaning** | “The product I use to prepare for my exam.” |
| **First point of introduction** | Auth welcome / first account experience |
| **Approved owner** | Product brand / Vision 2030 |
| **Approved synonyms** | none for educational narrator role |
| **Deprecated terms** | Using Kwalitec as mentor name on Journal / Timeline / Mission Intelligence |
| **Future implementation notes** | Help and onboarding may say Kwalitec, then hand off to Study Sensei for guidance memory. |

---

### 3. Mission

| Field | Decision |
|-------|----------|
| **Canonical term** | Mission |
| **Definition** | The authorised primary educational focus for a day (or study period): what deserves attention now, with one educational reason and one expected benefit. |
| **Educational purpose** | Reduce daily decision load to one meaningful focus. |
| **Student-facing meaning** | “What I should focus on today.” |
| **First point of introduction** | Home / Daily Mission Intelligence (after onboarding) |
| **Approved owner** | ILE-004 Daily Mission Intelligence; Educational Philosophy (mission philosophy) |
| **Approved synonyms** | Today's Mission; primary mission; daily mission (lowercase descriptive) |
| **Deprecated terms as synonyms for Mission** | tip; Mission tip (as primary noun); Today's Recommendation (as Home hero label); Today's Session (as *synonym* for Mission — see Session) |
| **Future implementation notes** | **Board decision DG-001.1-D02 (Mission-led):** Educational surfaces use Mission. Session is a different concept (practice workflow). Remediates ED-02. PX-002A “Today's Session” rejects “Today's Mission” as UI synonym — superseded for *educational meaning* by this lexicon; product-language reconciliation is a future implementation programme. |

---

### 4. Session

| Field | Decision |
|-------|----------|
| **Canonical term** | Session |
| **Definition** | The focused study practice workflow in which the learner executes deliberate practice — often carrying out today's Mission. |
| **Educational purpose** | Provide a calm, single-purpose container for practice without competing priorities. |
| **Student-facing meaning** | “The study work I am doing right now.” |
| **First point of introduction** | When starting practice from Home (“Start Session” / begin Mission practice) |
| **Approved owner** | Student Experience / PX product language (workflow); Educational Philosophy (practice) |
| **Approved synonyms** | Study Session (allowed in Help/orientation prose); today's session (descriptive of the open workflow) |
| **Deprecated terms** | Using Session as a synonym for Mission; Learning Session; Mission (as UI label *for the practice shell* when Mission means the focus) |
| **Future implementation notes** | CTAs may say “Start today's Session” when the action begins practice of today's Mission. Do not label the Home educational focus “Today's Session.” Remediates ED-02 by separating concepts. |

---

### 5. Recommendation

| Field | Decision |
|-------|----------|
| **Canonical term** | Recommendation |
| **Definition** | An authorised, deterministic, explainable suggestion for what the learner should do next — the decision object before or beneath Mission composition. |
| **Educational purpose** | Make “what next” inspectable and reproducible from evidence. |
| **Student-facing meaning** | “What the Sensei suggests I do, and why.” |
| **First point of introduction** | Home explanation / commitment (“I’m doing this next”) |
| **Approved owner** | Recommendation Quality Standard (P-001.3); Ubiquitous Language; MES / recommendation cores |
| **Approved synonyms** | suggested focus; authorised guidance (prose) |
| **Deprecated terms** | tip (as primary label for a Recommendation); using Recommendation and Mission interchangeably in hero labels |
| **Future implementation notes** | Recommendation ≠ Mission. Mission Intelligence *composes* a Mission brief from authorised Recommendation evidence. Keep “recommendation” in Commitment / Feedback Loop prompts where the decision object is meant. |

---

### 6. Guidance

| Field | Decision |
|-------|----------|
| **Canonical term** | Guidance |
| **Definition** | Umbrella educational speech: Sensei direction grounded in evidence — may include a Recommendation, Mission brief, explanation, or silence. |
| **Educational purpose** | Name educational help without forcing Mission/Session/Recommendation when the specific object is not yet clear. |
| **Student-facing meaning** | “Helpful direction for my learning.” |
| **First point of introduction** | Empty states; Help glossary; Feedback Loop |
| **Approved owner** | ILE-001C0; Study Sensei Philosophy |
| **Approved synonyms** | educational guidance |
| **Deprecated terms** | tip (as default umbrella); advice (engagement tone) |
| **Future implementation notes** | Prefer “Why this guidance?” over “Why this tip?” (ED-07 / IR-08). |

---

### 7. Tip

| Field | Decision |
|-------|----------|
| **Canonical term** | *(none — deprecated as educational primary noun)* |
| **Definition** | Informal synonym historically used for Mission / Recommendation / guidance. |
| **Educational purpose** | None as primary vocabulary — causes noun storm (ED-02). |
| **Student-facing meaning** | Ambiguous; students cannot track one decision across surfaces. |
| **First point of introduction** | Do not introduce |
| **Approved owner** | N/A — deprecation owned by DG-001.1 |
| **Approved synonyms** | N/A |
| **Deprecated terms** | tip; Mission tip; Why this tip? (as primary labels) |
| **Future implementation notes** | See `TERM_DEPRECATION_REGISTER.md` DEP-01. Replace with Mission, Recommendation, or Guidance by context. |

---

### 8. Reflection (family)

Board decision **DG-001.1-D03:** Reflection is a **family** of distinct concepts. One word may appear in UI only with a qualifier, or via the student map below.

#### 8a. Session reflection

| Field | Decision |
|-------|----------|
| **Canonical term** | Session reflection |
| **Definition** | Optional or workflow-bound reflection step that closes a Session after practice. |
| **Educational purpose** | Close the practice loop with calm acknowledgement of effort and learning. |
| **Student-facing meaning** | “A short pause after studying to notice what I learned.” |
| **First point of introduction** | End of Session / Help FAQ about closing the loop |
| **Approved owner** | Session experience / PX workflows |
| **Approved synonyms** | reflection (only inside Session chrome) |
| **Deprecated terms** | Treating Session reflection as Sensei calibration or Journal persistence without saying so |
| **Future implementation notes** | Map in Help: Session reflection ≠ Decision Journal reflection. |

#### 8b. Commitment reflection

| Field | Decision |
|-------|----------|
| **Canonical term** | Commitment reflection |
| **Definition** | Post-complete acknowledgement beats after Mission commitment (accept → practice → close). |
| **Educational purpose** | Reinforce agency and continuity without scoring the learner. |
| **Student-facing meaning** | “A short confirmation that I finished what I committed to.” |
| **First point of introduction** | Home commitment complete path |
| **Approved owner** | Mission Commitment (EP-008.3 lineage) |
| **Approved synonyms** | none |
| **Deprecated terms** | Guided Reflection (as if it were this system) |
| **Future implementation notes** | Keep five-beat calm close; name as commitment close in Help map. |

#### 8c. Sensei reflection

| Field | Decision |
|-------|----------|
| **Canonical term** | Sensei reflection |
| **Definition** | Optional usefulness judgement on a Decision Journal recommendation (ILE-005 student reflection). |
| **Educational purpose** | Calibrate Sensei guidance quality; practise professional judgement. |
| **Student-facing meaning** | “Optional questions about whether that guidance helped.” |
| **First point of introduction** | Decision Journal — “Optional reflection” |
| **Approved owner** | ILE-005 Educational Feedback Loop |
| **Approved synonyms** | Optional reflection (approved UI label); student reflection (docs) |
| **Deprecated terms** | Product Check-in as “reflection” |
| **Future implementation notes** | Always state optional and non-scoring. Remediates ED-03. |

#### 8d. Timeline reflection

| Field | Decision |
|-------|----------|
| **Canonical term** | Timeline reflection |
| **Definition** | Interpretive questions on the Educational Timeline inviting thought about growth, recovery, and turning points. |
| **Educational purpose** | Support long-term professional judgement from narrative evidence. |
| **Student-facing meaning** | “Questions that help me understand how my learning has changed.” |
| **First point of introduction** | Educational Timeline |
| **Approved owner** | ILE-003 |
| **Approved synonyms** | reflection questions (Timeline context) |
| **Deprecated terms** | none beyond family collision without qualifier |
| **Future implementation notes** | Cite journal evidence; never lead or judge. |

#### 8e. Guided Reflection preview

| Field | Decision |
|-------|----------|
| **Canonical term** | Guided Reflection preview |
| **Definition** | Home orientation chrome that illustrates reflection; does not record educational reflection. |
| **Educational purpose** | Orient only — not a persistence path. |
| **Student-facing meaning** | “A preview — not saved.” |
| **First point of introduction** | Home (if shown) — with honesty disclaimer |
| **Approved owner** | Home presentation |
| **Approved synonyms** | none preferred for primary teaching |
| **Deprecated terms** | Presenting as interactive educational reflection without honesty |
| **Future implementation notes** | RR-001.1 honesty retained; student map must distinguish (ED-03 / ED-09). |

#### 8f. Product Check-in (not reflection)

| Field | Decision |
|-------|----------|
| **Canonical term** | Product Check-in |
| **Definition** | Research / product survey intake — not educational reflection. |
| **Educational purpose** | None educational |
| **Student-facing meaning** | “Feedback for the product team.” |
| **First point of introduction** | Alpha / research surfaces |
| **Approved owner** | Research / Alpha |
| **Approved synonyms** | none as reflection |
| **Deprecated terms** | Calling Check-in “reflection” |
| **Future implementation notes** | Disclose as product research (ED-18). |

---

### 9. Decision Journal

| Field | Decision |
|-------|----------|
| **Canonical term** | Decision Journal |
| **Definition** | Persistent educational memory: significant guidance, evidence at the time, learner choices, and later outcomes. |
| **Educational purpose** | Continuity and trust — recommendations become conversations over time. |
| **Student-facing meaning** | “Where the Sensei remembers what we decided.” |
| **First point of introduction** | Help + first Journal empty state (ED-04 remediation) |
| **Approved owner** | ILE-002 |
| **Approved synonyms** | Journal (after first introduction) |
| **Deprecated terms** | telemetry; analytics (as labels for this surface); Archive (as primary name) |
| **Future implementation notes** | Append-only; never rewrite history; never shame deferrals. |

---

### 10. Educational Timeline

| Field | Decision |
|-------|----------|
| **Canonical term** | Educational Timeline |
| **Definition** | Narrative interpretation of Decision Journal memories into a coherent learning story. |
| **Educational purpose** | Help learners understand how learning has evolved — growth, recovery, consistency — without analytics theatre. |
| **Student-facing meaning** | “The story of how my learning has changed.” |
| **First point of introduction** | Help + Timeline empty state (ED-04) |
| **Approved owner** | ILE-003 |
| **Approved synonyms** | Timeline (after first introduction) |
| **Deprecated terms** | Analytics; Learning Path (as synonym); score dashboard framing |
| **Future implementation notes** | Distinct from History stats (ED-05 epistemology). |

---

### 11. Educational Feedback Loop

| Field | Decision |
|-------|----------|
| **Canonical term** | Educational Feedback Loop |
| **Definition** | Capability that evaluates educational usefulness of Sensei guidance over time for calibration — not engagement optimisation. |
| **Educational purpose** | Improve guidance honesty via outcome + reflection evidence. |
| **Student-facing meaning** | Mostly invisible; student sees Optional reflection on Journal, not “Feedback Loop” jargon. |
| **First point of introduction** | Help advanced glossary / Sensei surfaces — not as a nav destination |
| **Approved owner** | ILE-005 |
| **Approved synonyms** | Feedback Loop (internal / Help); Sensei calibration (prose) |
| **Deprecated terms** | engagement loop; streak feedback |
| **Future implementation notes** | Does not change recommendation selection. |

---

### 12. Study Plan

| Field | Decision |
|-------|----------|
| **Canonical term** | Study Plan |
| **Definition** | Exam-date-driven plan across available study days bound to official curriculum structure. |
| **Educational purpose** | Give syllabus spine and pacing — not a daily Mission substitute. |
| **Student-facing meaning** | “My plan for covering the syllabus before the exam date.” |
| **First point of introduction** | Study Plan wizard / onboarding |
| **Approved owner** | Study Plan / Curriculum Intelligence |
| **Approved synonyms** | plan (after context) |
| **Deprecated terms** | Roadmap; Learning Path (as Study Plan synonym) |
| **Future implementation notes** | Plan ≠ Mission ≠ Journey. |

---

### 13. Calibration

| Field | Decision |
|-------|----------|
| **Canonical term** | Calibration |
| **Definition** | Learner declaration of coverage / starting position used as provisional input — not Estimated Knowledge and not mastery. |
| **Educational purpose** | Honest cold-start positioning without false certainty. |
| **Student-facing meaning** | “I tell Kwalitec what I’ve already covered so guidance can start fairly.” |
| **First point of introduction** | Onboarding / Calibration workflow |
| **Approved owner** | Calibration surfaces; Educational Constitution (preference ≠ mastery) |
| **Approved synonyms** | declare coverage (verb phrase) |
| **Deprecated terms** | Treating calibration as mastery; self-certified Mastery |
| **Future implementation notes** | Keep honesty: declarations ≠ Estimated Knowledge (RP-001.5 Pass behaviour). |

---

### 14. Confidence

| Field | Decision |
|-------|----------|
| **Canonical term** | Confidence |
| **Definition** | Certainty attached to a belief or output. Always disambiguate kind: Mission confidence / Recommendation Confidence / Twin estimate confidence / learner self-report. |
| **Educational purpose** | Prevent over-trust; match claim strength to evidence. |
| **Student-facing meaning** | “How sure this guidance is — based on evidence, not vibes.” |
| **First point of introduction** | Mission Intelligence / explanations (Mission confidence) |
| **Approved owner** | Ubiquitous Language; ILE-001 confidence/uncertainty UX; Mission Intelligence |
| **Approved synonyms** | Mission confidence (when Mission-scoped); qualitative bands (Insufficient → Emerging → Reliable → High) |
| **Deprecated terms** | Unlabelled high % certainty; guarantee language |
| **Future implementation notes** | Prefer qualitative bands; never invent percentages of certainty in Sensei speech. |

---

### 15. Readiness

| Field | Decision |
|-------|----------|
| **Canonical term** | Readiness |
| **Definition** | Explainable estimate of exam preparedness for the active goal/sitting — provisional, non-guarantee. |
| **Educational purpose** | Answer “Am I on track?” with inspectable factors. |
| **Student-facing meaning** | “How prepared I appear to be — estimated, not a promise.” |
| **First point of introduction** | Exam Readiness card / Journey-adjacent summaries |
| **Approved owner** | Readiness Engine; PX Exam Readiness label |
| **Approved synonyms** | Exam Readiness (approved UI label); Estimated readiness (provisional) |
| **Deprecated terms** | Mastery score (as readiness); Twin score; pass guarantee |
| **Future implementation notes** | Soften Help “closest to being tested on” (ED-08). AA surfaces prefer check framing over exam anxiety. |

---

### 16. Progress

| Field | Decision |
|-------|----------|
| **Canonical term** | Progress |
| **Definition** | Movement through syllabus work and study continuity over time — descriptive, not a mastery identity. |
| **Educational purpose** | Orient learners without equating activity with understanding. |
| **Student-facing meaning** | “How far I’ve come in the plan and practice.” |
| **First point of introduction** | Journey / History |
| **Approved owner** | Journey / History presentation |
| **Approved synonyms** | Journey (surface for syllabus progress) |
| **Deprecated terms** | Progress Path; Learning Path; Roadmap (as Progress synonyms) |
| **Future implementation notes** | Progress ≠ Mastery ≠ Readiness. |

---

### 17. Mastery

| Field | Decision |
|-------|----------|
| **Canonical term** | Mastery |
| **Definition** | Probabilistic belief about how well the learner can perform a curriculum entity *now*, updated from Learning Evidence — Twin estimate, not a badge. |
| **Educational purpose** | Drive gaps, recommendations, and honest coverage — never self-certified theatre. |
| **Student-facing meaning** | Prefer not to foreground raw “Mastery” as identity; speak of understanding / evidence / completed topics when possible. |
| **First point of introduction** | Prefer delayed; use completed / needs reinforcement language first |
| **Approved owner** | Ubiquitous Language; Educational Constitution |
| **Approved synonyms** | Estimated Knowledge (technical); understanding (student prose) |
| **Deprecated terms** | Mastery score as student identity; mastered (prefer completed topics in History); self-certified mastery from Calibration |
| **Future implementation notes** | Never expose mastery score as brand; Mission Completion ≠ Mastery. |

---

### 18. Revision

| Field | Decision |
|-------|----------|
| **Canonical term** | Revision |
| **Definition** | Highest-value review work scheduled from forgetting risk, syllabus weight, and evidence. |
| **Educational purpose** | Protect fragile knowledge without engagement theatre. |
| **Student-facing meaning** | “Review work that evidence says I should revisit.” |
| **First point of introduction** | Revision nav / when warranted by evidence |
| **Approved owner** | Educational Philosophy (revision); PX Revision |
| **Approved synonyms** | review (prose); Revision Check (AA session type) |
| **Deprecated terms** | Remediation; Intervention (learner UI) |
| **Future implementation notes** | Revision must not compete as a second “primary mission” without disclosure (ED-13). |

---

### 19. History

| Field | Decision |
|-------|----------|
| **Canonical term** | History |
| **Definition** | Student study-history / progress-over-time surface: accomplished sessions, stats context, bridges to Journal/Timeline. |
| **Educational purpose** | Archive of practice and choices — context, not Sensei narrative authority. |
| **Student-facing meaning** | “What I’ve done and chosen over time.” |
| **First point of introduction** | Nav History |
| **Approved owner** | PX-002A / Product Language Guide |
| **Approved synonyms** | study history |
| **Deprecated terms** | Analytics (learner UI); Archive (as primary nav — Unified Journey OFF) |
| **Future implementation notes** | Intro copy should state: stats are context; Journal/Timeline carry Sensei meaning (ED-05). |

---

### 20. Evidence

| Field | Decision |
|-------|----------|
| **Canonical term** | Evidence |
| **Definition** | Observable learning signals that justify guidance — attempts, outcomes, choices, reflections — never engagement theatre. |
| **Educational purpose** | Ground every educational claim. |
| **Student-facing meaning** | “What we’ve seen that supports this guidance.” |
| **First point of introduction** | Explanation cards — Supporting evidence |
| **Approved owner** | Learning Evidence Model; Explainability Standard |
| **Approved synonyms** | Supporting evidence (UI label); educational evidence |
| **Deprecated terms** | Proof; guarantee; certainty from thin data |
| **Future implementation notes** | Empty Mission when evidence insufficient is correct. |

---

### 21. Uncertainty

| Field | Decision |
|-------|----------|
| **Canonical term** | Uncertainty |
| **Definition** | Explicit acknowledgement that guidance remains provisional given thin or mixed evidence. |
| **Educational purpose** | Honesty; protect trust when the Sensei waits rather than invents. |
| **Student-facing meaning** | “We’re not sure yet — and that’s OK.” |
| **First point of introduction** | Mission Intelligence empty / explanation Uncertainty |
| **Approved owner** | ILE-001C0; Uncertainty language standards |
| **Approved synonyms** | provisional; not enough evidence yet |
| **Deprecated terms** | Fake precision; invented certainty percentages |
| **Future implementation notes** | Keep silence lawful. |

---

### 22. Daily Mission Intelligence

| Field | Decision |
|-------|----------|
| **Canonical term** | Daily Mission Intelligence |
| **Definition** | Learner-facing composition of one primary Mission brief from authorised Recommendation / MES evidence — not a second ranking brain. |
| **Educational purpose** | Answer “What should I focus on today?” immediately. |
| **Student-facing meaning** | “Today’s Mission, explained.” |
| **First point of introduction** | Home Mission Intelligence; Help (ED-04) |
| **Approved owner** | ILE-004 |
| **Approved synonyms** | Mission Intelligence (short) |
| **Deprecated terms** | tip of the day; dual-mission presentation without disclosure |
| **Future implementation notes** | Does not re-run Decision Engine selection. |

---

### 23. Mission Commitment

| Field | Decision |
|-------|----------|
| **Canonical term** | Mission Commitment |
| **Definition** | Learner accept or defer of authorised Mission / Recommendation with non-shaming defer reasons. |
| **Educational purpose** | Agency: one deliberate choice, then practice. |
| **Student-facing meaning** | “I’m doing this next” / “Not today.” |
| **First point of introduction** | Home commitment controls |
| **Approved owner** | Recommendation Commitment lineage |
| **Approved synonyms** | commitment; accept / defer |
| **Deprecated terms** | Forced accept; streak guilt on defer |
| **Future implementation notes** | Continuity copy must not say “tip” (ED-06). |

---

### 24. Journey

| Field | Decision |
|-------|----------|
| **Canonical term** | Journey |
| **Definition** | Syllabus progress surface — movement through topics toward exam readiness. |
| **Educational purpose** | Show curriculum position without inventing a parallel syllabus. |
| **Student-facing meaning** | “Where I am in the syllabus.” |
| **First point of introduction** | Nav Journey |
| **Approved owner** | PX Product Language |
| **Approved synonyms** | none preferred |
| **Deprecated terms** | Roadmap; Progress Path; Learning Path; Curriculum Graph (student UI) |
| **Future implementation notes** | Journey ≠ Educational Timeline (structure vs narrative story). |

---

### 25. Home

| Field | Decision |
|-------|----------|
| **Canonical term** | Home |
| **Definition** | Student landing surface for today’s educational focus and next action. |
| **Educational purpose** | One answer to “what now?” |
| **Student-facing meaning** | “Where I start today.” |
| **First point of introduction** | First login after auth |
| **Approved owner** | PX-002A |
| **Approved synonyms** | none |
| **Deprecated terms** | Dashboard (learner UI) |
| **Future implementation notes** | Prefer Mission Intelligence empty waiting narrative when no Mission (IR-10). |

---

### 26. Quick Check (and AA checks)

| Field | Decision |
|-------|----------|
| **Canonical term** | Quick Check |
| **Definition** | Anxiety-safe Adaptive Assessment session type (and family: Deep / Recovery / Confidence / Revision / Readiness Check). |
| **Educational purpose** | Gather evidence without exam/test identity language. |
| **Student-facing meaning** | “A short learning check — not an exam.” |
| **First point of introduction** | Only when feature enabled; otherwise do not advertise as default Alpha path |
| **Approved owner** | ILE-001 Terminology Standard |
| **Approved synonyms** | learning check (secondary path `/assessment`) |
| **Deprecated terms** | Exam; Test; Pass; Fail; Weak; Strong student (on AA surfaces) |
| **Future implementation notes** | Flag-gated; Journal empty must not imply QC is always on (ED-14). |

---

### 27. Learning Insights

| Field | Decision |
|-------|----------|
| **Canonical term** | Learning Insights |
| **Definition** | Explainable readiness / progress summaries for learners. |
| **Educational purpose** | Make Twin-backed insight speak educationally without engine jargon. |
| **Student-facing meaning** | “Clear summaries of how I’m doing.” |
| **First point of introduction** | When insights surfaces are shown |
| **Approved owner** | Product Language Guide |
| **Approved synonyms** | insights (after context) |
| **Deprecated terms** | Twin Insights; Digital Twin; Mastery Score; Student Analysis (learner UI) |
| **Future implementation notes** | Internal Twin names never student-facing. |

---

## Concept relationships (must remain distinct)

```
Kwalitec (product)
    └── Study Sensei (educational mentor)
            ├── Recommendation (decision object)
            ├── Mission (today's authorised educational focus)
            │       └── Session (practice workflow executing focus)
            ├── Decision Journal (memory)
            │       ├── Sensei reflection (optional calibration)
            │       └── Educational Timeline (narrative interpretation)
            ├── Educational Feedback Loop (Sensei self-calibration)
            └── Evidence + Uncertainty + Confidence (honesty grammar)
```

**Hard rule:** Mission ≠ Session ≠ Recommendation ≠ Tip ≠ Guidance (umbrella only).

---

## Explainability grammar (convergent — keep)

Approved labels for Sensei explanations:

- Why  
- Why now  
- Why this Mission / Why this recommendation? / Why this guidance?  
- Why not something else  
- Supporting evidence  
- Expected benefit / You’ll work toward  
- Confidence / Mission confidence  
- Uncertainty  
- After you finish / What happens next  
- Optional reflection  

**Retire:** Why this tip? · Why the system chose this

---

## Forbidden in Sensei speech

| Class | Examples |
|-------|----------|
| Engagement theatre | streak guilt, FOMO, comparative identity |
| Engine names | Twin, Mission Engine, Adaptive Decision Engine, warrant, ranking algorithm |
| Shame / identity | weak, fail (AA); broke your streak |
| Certainty theatre | guarantee pass; unlabelled high % |
| Robotic agent | the system chose |

---

## Relationship to prior standards

| Document | Relationship after DG-001.1 |
|----------|----------------------------|
| `UBIQUITOUS_LANGUAGE.md` | Domain definitions remain; student-facing educational naming follows this lexicon |
| `PRODUCT_LANGUAGE_GUIDE.md` / PX-002A | Workflow labels (Home, History, Journey, Session CTA) remain; **Mission** is restored as educational focus noun — reconciliation required in a future copy/implementation package |
| ILE-001 / ILE-002–005 philosophies | Affirmed; lexicon makes student-facing names explicit |
| RP-001.3 Terminology Register | Observation → this document is the Board decision |
| RP-001.5 ED-01–ED-04 | Governance resolution recorded; implementation still pending |

---

## Amendment

Amend this lexicon only via Educational Governance (DG-001) Board decision. Do not invent student-facing synonyms in features without updating `TERM_DEPRECATION_REGISTER.md` and this file.

---

**End of CANONICAL_EDUCATIONAL_LEXICON**

# Reflection Architecture

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.3 — Reflection Architecture  
**Status:** Active — Board educational law for reflection  
**Effective:** 2026-07-28  
**Authority:** Educational governance (subordinate to Educational Constitution; extends DG-001.1 lexicon and DG-001.2 authority)  
**Constraint:** Governance only — does not change product behaviour, templates, recommendations, Mission Intelligence, curriculum, or feature flags.

---

## 1. Purpose

This document is the **single authoritative Reflection Architecture** for Kwalitec.

It defines:

- what reflection is (and is not)
- why every reflection interaction exists
- how reflection variants relate as one family
- where each reflection is stored
- who owns each reflection
- how reflection contributes to Study Sensei, Decision Journal, Educational Timeline, and professional judgement
- how every reflection contributes to one coherent professional learning narrative

**Success criterion:** If every reflection interaction disappeared tomorrow, the complete reflection system could be recreated from this document together with `REFLECTION_LIFECYCLE.md`, `REFLECTION_RELATIONSHIP_MATRIX.md`, and `REFLECTION_GOVERNANCE_RULES.md`.

---

## 2. Educational principle

**Reflection is not data collection.**

Reflection is a deliberate educational practice through which professional learners convert experience into better future judgement.

Every lawful reflection interaction must reinforce:

```
Experience
    ↓
Evidence
    ↓
Reflection
    ↓
Learning
    ↓
Professional judgement
    ↓
Long-term mastery
```

Reflection that does not advance this chain is engagement theatre and is forbidden (see `REFLECTION_GOVERNANCE_RULES.md`).

**Governing philosophy:** Educational Philosophy belief #4 — feedback and reflection close the loop: attempt → outcome → interpretation → next guidance must be visible to the student.

---

## 3. Board decision (DG-001.3)

| ID | Decision |
|----|----------|
| **DG-001.3-D01** | Reflection is one coherent educational system — a **family** of roles in a single learning narrative — not a bag of unrelated forms. |
| **DG-001.3-D02** | The Decision Journal is the **sole durable educational memory** for Sensei-visible reflection that shapes the long-term learning story. |
| **DG-001.3-D03** | Study Sensei is the sole primary authority for educational reflection meaning (per DG-001.2-D01 / D09). |
| **DG-001.3-D04** | No orphan reflections: every recording reflection must have a defined owner, store, lifecycle stage, and contribution to the narrative — or be explicitly classified as non-recording / non-reflection. |
| **DG-001.3-D05** | Product Check-in, Calibration declarations, and system-authored session feedback are **not** educational reflection (affirm DEP-15 / ED-18). |
| **DG-001.3-D06** | Reflection must remain optional unless educationally justified; it must never score the learner, imply surveillance, or re-rank recommendations. |
| **DG-001.3-D07** | Session-local notes and commitment acknowledgement are lawful practice-close reflections; they must not be presented as Decision Journal persistence unless mirrored. |
| **DG-001.3-D08** | Parallel / flag-gated / EOS reflection stacks are **architecture residuals**, not second student mental models — consolidation is future implementation work governed by this law. |

---

## 4. Canonical taxonomy

Board decision **DG-001.1-D03** established the reflection family. DG-001.3 assigns each category **architecture roles**.

### 4.1 Educational reflection categories

| Category | Definition | Educational purpose | Authority (primary) | Lifecycle role | Student visibility | Records? |
|----------|------------|---------------------|---------------------|----------------|--------------------|----------|
| **Session reflection** | Workflow-bound pause that closes a Session after practice | Convert practice experience into noticed learning; close the practice loop | Study Sensei (framing); Session/PX owns workflow | Practice close | Yes — Session surface | Optional note → session document store (not Journal by default) |
| **Commitment reflection** | Post-complete acknowledgement beats after Mission commitment | Reinforce agency and continuity without scoring | Study Sensei | Commitment close | Yes — Home | Ack / composed beats only; state on `recommendation_commitments` |
| **Sensei reflection** | Optional usefulness judgement on a Decision Journal recommendation (ILE-005) | Practise professional judgement; calibrate Sensei guidance honesty | Study Sensei; ILE-005 owns capability | Memory calibration | Yes — Decision Journal “Optional reflection” | Yes → Journal + internal reviews |
| **Timeline reflection** | Interpretive questions on the Educational Timeline | Support long-term professional judgement from narrative evidence | Study Sensei; ILE-003 owns capability | Narrative interpretation | Yes — Timeline | Prompts only (no POST store) |
| **Guided Reflection preview** | Home orientation chrome illustrating reflection | Orient only — honesty required | Study Sensei framing; Home presentation owns chrome | Orientation (non-recording) | Yes — with “not saved” honesty | **No** |
| **Quick Check reflection phase** | Presentation close after Quick Check questions | Calm close of check experience | Study Sensei when framing on; AA owns workflow | Assessment close | Yes when Quick Check path used | Presentation state only (not durable educational memory) |

### 4.2 Memory and narrative hosts (not reflection subtypes)

| Host | Role in reflection architecture | Authority |
|------|----------------------------------|-----------|
| **Decision Journal** | Sole durable educational memory for significant guidance, choices, outcomes, and Sensei reflection | Study Sensei (ILE-002) |
| **Educational Timeline** | Narrative interpretation of Journal; surfaces Timeline reflection questions | Study Sensei (ILE-003) |
| **Educational Feedback Loop** | Capability that consumes outcomes + Sensei reflection to review guidance usefulness **without re-ranking** | Study Sensei (ILE-005); student sees optional Journal reflection, not “Feedback Loop” jargon by default |

### 4.3 Explicit non-reflections

| Item | Why not reflection | May never |
|------|--------------------|-----------|
| **Product Check-in** (RIP-001; historically titled “Daily Reflection & Product Check-in”) | Product / research survey | Be taught as educational reflection; write Twin / Evidence / Journal / Mission ranking |
| **Calibration declarations** | Declared coverage for Twin birth — structural honesty, not metacognition after practice | Be labelled reflection; claim mastery |
| **LXP-004 Study Session Feedback** | System-authored explainability narrative | Be presented as student reflection |
| **Revision acknowledgement** | Lifecycle milestone ack on syllabus complete | Be conflated with Revision Reflection (which does not yet exist as a capture surface) |
| **Vision Journal / Alpha product feedback / behavioural Learning Feedback emitters** | Founder, product, or observational telemetry | Enter the student educational reflection map |

### 4.4 Architecture residuals (parallel stacks — not Alpha student map members)

These exist in code or docs but are **not** additional student mental-model categories. Future programmes must consolidate or retire them under this architecture:

| Residual | Status | Governance stance |
|----------|--------|-------------------|
| V2 `JourneyReflection` / `ReflectionManager` | Domain + tests; not Alpha `/session/` path | Do not teach as a third session reflection; converge to Session reflection law |
| Unified Journey Guided Reflection (`ENABLE_UNIFIED_JOURNEY`) | Implemented; default OFF; responses never persisted | If enabled, honesty: non-recording orientation or explicit map update required before claiming educational reflection |
| EOS `/eos/reflection` + `EpisodeReflection` | Separate `src/` stack | Outside sole-runtime Alpha student journey; must not invent a second reflection brand |
| Coach `ReflectionPrompts` (`src/`) | Deterministic prompt models | Subordinate to this architecture when surfaced |
| Decision Journal kinds without writers (`revision_recommendation`, `recovery_recommendation`, `quick_check_recommendation`) | Catalogue placeholders | Lawful kinds; wiring is future work — not new reflection types |
| Educational Reflection Model (VI/MS003 docs) | Governing documentation for tutor-grade interpretation | Informs Session / Sensei speech quality; not a separate student reflection product |

### 4.5 Student map sentence (canonical — future Help)

> Reflection after a Session closes practice. Commitment reflection on Home confirms you finished what you chose. Optional reflection in the Decision Journal helps the Study Sensei learn whether guidance was useful. The Educational Timeline asks deeper questions about your learning story. Product Check-in is feedback for the product team — not educational reflection.

---

## 5. Reflection type audit (architecture register)

For each audited capability: educational purpose, trigger, timing, required/optional, visibility, storage, Study Sensei / Timeline / Journal contribution, recommendations, professional judgement.

### 5.1 Decision Journal

| Field | Law |
|-------|-----|
| **Educational purpose** | Persistent memory of significant guidance — observation → meaning → recommendation → choice → outcome → reflection |
| **Trigger** | Mission present / accept / defer / complete; milestones; Sensei reflection writes |
| **Timing** | Continuous chronology at decision and outcome moments |
| **Required / optional** | Passive accumulation; Sensei reflection on entries is optional |
| **Student visibility** | Full chronology at Decision Journal |
| **Storage** | `decision_journal_entries`, `decision_journal_evidence_events` |
| **Study Sensei** | Primary educational memory surface |
| **Timeline** | Upstream source of truth |
| **Decision Journal** | Self |
| **Recommendations** | Records snapshots; **never re-ranks** |
| **Professional judgement** | Enables review of past choices under uncertainty |

### 5.2 Session reflection (Alpha Session Experience)

| Field | Law |
|-------|-----|
| **Educational purpose** | Close practice with calm acknowledgement; optional note of what was learned |
| **Trigger** | After last session activity → reflection step |
| **Timing** | After practice, before summary/complete |
| **Required / optional** | Workflow step to continue; **note optional** |
| **Student visibility** | Session reflection surface |
| **Storage** | Session document store (`NS_REFLECTION`); durable when durable store enabled |
| **Study Sensei** | Framing / guidance projection; does not mutate Twin |
| **Timeline** | No direct write |
| **Decision Journal** | **No automatic mirror** (governance residual — see D07 / orphans) |
| **Recommendations** | Does not alter ranking |
| **Professional judgement** | Immediate metacognition after practice |

### 5.3 Commitment reflection

| Field | Law |
|-------|-----|
| **Educational purpose** | Close accept → practice → complete arc; reinforce agency |
| **Trigger** | Commitment `completed` → Home shows reflection ack |
| **Timing** | After session finish, on Home |
| **Required / optional** | Shown at completion; single ack advances state — not scored |
| **Student visibility** | Home commitment reflection block |
| **Storage** | `recommendation_commitments` (`reflected_at`, composed beats — not free-text student essay) |
| **Study Sensei** | Mentors the close |
| **Timeline** | Indirect via Journal commitment mirror |
| **Decision Journal** | Mirror via commitment adapter (fail-open) |
| **Recommendations** | Preference/intent only — no ranking change |
| **Professional judgement** | Deliberate practice closure |

### 5.4 Sensei reflection (Educational Feedback Loop — student facing)

| Field | Law |
|-------|-----|
| **Educational purpose** | Practise judgement on guidance usefulness; improve Sensei honesty |
| **Trigger** | Journal entries eligible for reflection (`can_reflect`) |
| **Timing** | After outcome on entry; anytime from Journal |
| **Required / optional** | **Always optional**; skip lawful |
| **Student visibility** | Optional form on Journal (“Optional reflection”) |
| **Storage** | Student answers → Journal reflection note + evidence; internal → `educational_feedback_reviews` (**not learner-visible**) |
| **Study Sensei** | Calibrates guidance quality reviews |
| **Timeline** | Reflected entries feed narrative / reflection highlights |
| **Decision Journal** | Host and durable store |
| **Recommendations** | **Never re-ranks** |
| **Professional judgement** | Explicit: did this guidance help? would I choose again? |

### 5.5 Timeline reflection

| Field | Law |
|-------|-----|
| **Educational purpose** | Invite thought about growth, recovery, turning points from evidence |
| **Trigger** | Student opens Educational Timeline |
| **Timing** | On-demand retrospective |
| **Required / optional** | Optional viewing; questions are prompts |
| **Student visibility** | Timeline narrative sections |
| **Storage** | None — projection from Journal |
| **Study Sensei** | Narrative voice |
| **Timeline** | Self |
| **Decision Journal** | Read-only upstream |
| **Recommendations** | None |
| **Professional judgement** | Long-horizon interpretation |

### 5.6 Guided Reflection preview

| Field | Law |
|-------|-----|
| **Educational purpose** | Orient to the habit of reflection |
| **Trigger** | Home when not in active unified/guided session reflection |
| **Timing** | Between sessions on Home |
| **Required / optional** | N/A — non-functional when preview-only |
| **Student visibility** | Yes — must disclose not saved |
| **Storage** | None |
| **Study Sensei / Timeline / Journal** | None |
| **Recommendations** | None |
| **Professional judgement** | Orientation only — must not fake agency |

### 5.7 Product Check-in (non-reflection)

| Field | Law |
|-------|-----|
| **Educational purpose** | **None** — product research |
| **Trigger** | Post-study invitation or Settings |
| **Timing** | After study or anytime |
| **Required / optional** | Optional; dismiss without penalty |
| **Student visibility** | Research surfaces; must be labelled product research |
| **Storage** | Research tables — isolated |
| **Study Sensei / Timeline / Journal / recommendations** | **Forbidden** |
| **Professional judgement** | Not educational metacognition |

### 5.8 Calibration declarations (non-reflection)

| Field | Law |
|-------|-----|
| **Educational purpose** | Honest declared educational history for Twin birth |
| **Trigger** | After Study Plan creation |
| **Timing** | Onboarding / cold start |
| **Required / optional** | Skip/abandon lawful with empty-history honesty |
| **Student visibility** | Calibration workflow |
| **Storage** | Twin birth pipeline — not Journal |
| **Study Sensei** | Seeds declared coverage when Twin enabled |
| **Timeline / Journal** | No |
| **Recommendations** | No direct re-rank from self-certification as mastery |
| **Professional judgement** | Positioning honesty ≠ reflection after practice |

### 5.9 Mission Commitment outcomes (supporting, not a separate reflection type)

| Field | Law |
|-------|-----|
| **Role** | State machine that **creates the conditions** for Commitment reflection and Journal mirrors |
| **States** | offered → committed → in_session → completed → reflected (or deferred / refusal) |
| **Contribution** | Links Mission choice → Session practice → Commitment reflection → Journal memory |

### 5.10 Revision Reflection (status)

| Field | Law |
|-------|-----|
| **Status** | **No dedicated student capture surface** in Alpha |
| **Closest** | Journal `revision_recommendation` kind (writer incomplete); Revision ack (non-reflection) |
| **Governance** | When Revision recommendations are mirrored to Journal, Sensei reflection applies — do not invent a seventh student-facing reflection brand without Board update |

### 5.11 Quick Check reflection phase

| Field | Law |
|-------|-----|
| **Educational purpose** | Calm close of Quick Check; optional framing |
| **Storage** | Not durable educational memory |
| **Governance** | Assessment-close presentation; Journal kind exists without writer — wiring is future |

### 5.12 Reflection prompts, retrieval, explanations, history

| Concern | Architecture law |
|---------|------------------|
| **Prompts** | Each category owns its prompt catalogue; Sensei reflection prompts are the only prompts that write educational memory by default |
| **Retrieval** | Student educational reflection history is Decision Journal (+ Timeline interpretation). Session notes are session-local. Research is research-only |
| **Explanations** | Journal arc and Timeline narrative explain *why guidance existed*; Sensei reflection explains *whether it helped*; Session cards may project calm insight without claiming mastery |
| **History (PX archive)** | Practice/stats context — not primary reflection history (ED-05); must link to Journal/Timeline without competing as mentor memory |

---

## 6. Contribution to Study Sensei

Study Sensei uses reflection as **learning memory and judgement practice**, not as engagement metrics.

| Input | Sensei use |
|-------|------------|
| Decision Journal entries | Continuity of guidance conversations |
| Sensei reflection answers | Internal Feedback Loop reviews (learner-invisible); narrative honesty |
| Commitment outcomes | Continuity of accept/defer/complete arcs |
| Timeline projection | Long-term story the Sensei can narrate |
| Session notes | Practice-close only unless future Board-authorised Journal mirror |
| Product Check-in | **Never** |

Sensei **must never** claim that skipping optional reflection harms the student, changes ranking, or is being “watched.”

---

## 7. One coherent professional learning narrative

Canonical narrative (student-visible story):

1. **Mission** — Study Sensei proposes today’s educational focus.  
2. **Commitment** — Student accepts or defers with agency.  
3. **Session** — Deliberate practice.  
4. **Session reflection** — Notice what practice taught.  
5. **Commitment reflection** — Acknowledge completion of the chosen focus.  
6. **Decision Journal** — Sensei remembers guidance, choice, and outcome.  
7. **Sensei reflection (optional)** — Student judges whether guidance helped.  
8. **Educational Timeline** — Narrative of how judgement and learning evolved.  
9. **Future Mission / Recommendation** — Next focus grounded in evidence and memory — **not** in reflection scores.

Anything outside this narrative must either join it (mirror, write, or prompt), be labelled non-reflection, or be treated as residual pending consolidation.

---

## 8. Ownership summary

| Concern | Owner |
|---------|-------|
| Vocabulary of reflection family | DG-001.1 / this architecture |
| Educational meaning of reflection | Study Sensei (DG-001.2) |
| Durable educational memory | Decision Journal (ILE-002) |
| Narrative interpretation | Educational Timeline (ILE-003) |
| Guidance calibration capability | Educational Feedback Loop (ILE-005) |
| Session practice-close workflow | Session Experience / PX |
| Commitment close workflow | Mission Commitment |
| Product research intake | Research (RIP) — non-reflection |
| Declared coverage cold start | Calibration — non-reflection |

---

## 9. Related documents

| Document | Role |
|----------|------|
| `REFLECTION_LIFECYCLE.md` | End-to-end lifecycle; no orphans |
| `REFLECTION_RELATIONSHIP_MATRIX.md` | Dependencies and flows |
| `REFLECTION_GOVERNANCE_RULES.md` | Permanent rules |
| `CANONICAL_EDUCATIONAL_LEXICON.md` §8 | Term definitions |
| `EDUCATIONAL_VOCABULARY_MAP.md` §4 | Student map |
| `EDUCATIONAL_AUTHORITY_MODEL.md` | Who may speak reflection |
| ILE-002 / ILE-003 / ILE-005 product docs | Capability detail |
| RP-001.5 `EDUCATIONAL_DRIFT_REGISTER.md` ED-03 / ED-18 | Origin defects |

---

## 10. Certification statement

The Board can answer from this architecture:

| Question | Answer location |
|----------|-----------------|
| Why does every reflection exist? | §5 audit + §4 taxonomy |
| Where is it stored? | §5 Storage fields + §4 |
| Who owns it? | §8 + Authority column |
| How does it improve future learning? | §2 chain + §6 Sensei + §7 narrative |
| How does every reflection contribute to one coherent narrative? | §7 + lifecycle companion |

**DG-001.3 Reflection Architecture is established as Board law.** Implementation and Help publication remain future work.
`)
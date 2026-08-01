# EA-007 — Trust Break Register

**Programme:** Educational Excellence Programme EA-007 — Longitudinal Educational Continuity  
**Campaign:** CS1 2026 first-pass spine · Days 1–14 (topics 1.1 → 5.1)  
**Audit date:** 2026-08-01  
**Method:** Longitudinal Academic Board review of consecutive study days; live EV-001 evidence retained where campaign experience still depends on published runtime behaviour  
**Nature:** Observational register — remedies suggested only; **not implemented** (EA-007 creates no content and changes no code)

---

## Purpose

Record every moment across the campaign where a diligent daily student might think:

- “This mission is too generic.”
- “This doesn’t follow naturally from yesterday.”
- “I don’t understand why I’m studying this now.”
- “This feels copied from a template.”
- “Yesterday’s quality was a fluke.”
- “I should probably go back to the textbook instead.”

Do not minimise. Recurring patterns are worse than single incidents.

---

## Register

### LTB-001 — Template Mission stamp across Days 1–12 and Day 14

| Field | Evidence |
|-------|----------|
| **Day / mission** | Campaign Days 1–12 (1.1–4.1) and Day 14 (5.1) |
| **What caused the loss of trust** | Mission titles follow `Study {code} — {title}`; rationale follows *“Today focuses on {code} — {title} because it is the next incomplete topic in syllabus order.”* Objectives and success lines are interchangeable frames with topic nouns swapped (`writing.py`, `derivation.py`). |
| **Educational impact** | Missions feel administrative. After a few days the student stops reading the brief. EA-003 Mission law (bridge, unique why-now, assessable verb) is unmet at campaign scale. |
| **Pattern class** | Generic missions · Educational repetition · Motivation fatigue |
| **Suggested remedy** | Certify and publish Educational Packages for each Learning Mode day before student exposure; block Home Mission display when only derivation templates exist (HOLD), or show honest “Mission not yet authored” rather than syllabus-paste theatre. |

---

### LTB-002 — Session monotony (identical pedagogy shell)

| Field | Evidence |
|-------|----------|
| **Day / mission** | All non-pack days; Session substance via `substance_planner.py` / authoring `episode.py` |
| **What caused the loss of trust** | Every day: Read (*“Read the material for {T}. Note one idea…”*) → generic worked-example method → practice → generic reflection. Only Day 13 (4.2 pack) breaks the pattern with CMP Reading Guidance and Knowledge Checks. |
| **Educational impact** | Session stage chrome becomes educational theatre. Cognitive demand does not rise with topic difficulty (CLT vs estimators vs Bayes). |
| **Pattern class** | Session monotony · Educational theatre · Cognitive load failure |
| **Suggested remedy** | Require Gate SS/LE PASS packages per topic-day; vary study moves deliberately across a week (structure day, retrieval day, comparison day) under EA-004. |

---

### LTB-003 — Tutor voice cliff at Day 13 then collapse at Day 14

| Field | Evidence |
|-------|----------|
| **Day / mission** | Day 13 = EA-006 Golden pack voice; Day 14 = templated 5.1 |
| **What caused the loss of trust** | Student finally hears Study Sensei (prior bridge, misconception watch, closed-book chain). Next morning Bayesian Mission reverts to syllabus paste and generic Session. Continuity_line from 4.2 preview promised a bridge; 5.1 Mission does not reciprocate with prior_bridge. |
| **Educational impact** | Proves premium quality is possible — then withholds it. Trust declines faster after a good day than after uniformly mediocre days. |
| **Pattern class** | Tutor voice drift · Artificial continuity · Motivation fatigue |
| **Suggested remedy** | Do not publish isolated Golden packs into a template sea without a continuity publication plan for predecessor and successor days (at minimum 4.1 and 5.1 flanking 4.2). |

---

### LTB-004 — Reading Guidance absent on 13 of 14 days

| Field | Evidence |
|-------|----------|
| **Day / mission** | Days 1–12, 14; contrast Day 13 `reading_guidance` in pack JSON |
| **What caused the loss of trust** | Non-pack days lack open_point / stop_condition / out_of_scope / focus questions / pause points. Student is told to “read the material” without a selective CMP map (EA-004 / EP-04 unmet). |
| **Educational impact** | Forces dual-tracking with textbook from early week. Primary-study reliance fails before GLM. |
| **Pattern class** | Reading overload (unscoped) · Educational theatre |
| **Suggested remedy** | No Learning Mode day without certified Reading Guidance instance; HOLD publication otherwise. |

---

### LTB-005 — Reflection fatigue from identical harvest prompts

| Field | Evidence |
|-------|----------|
| **Day / mission** | Days 1–12, 14 reflection stamp in `writing.py` |
| **What caused the loss of trust** | Prompt always: *“Reflect briefly: what in {T} is now clearer, and what still needs careful attention?”* Day 13 shows topic-specific residual harvest is possible. |
| **Educational impact** | Reflections become compliance typing. Residuals do not feed revision. EP-07 reflection quality collapses over time. |
| **Pattern class** | Reflection fatigue · Educational repetition |
| **Suggested remedy** | Author one misconception-tied reflection goal per package; accumulate residuals into spaced revision Missions. |

---

### LTB-006 — Tomorrow Preview boilerplate

| Field | Evidence |
|-------|----------|
| **Day / mission** | Default `build_tomorrow_preview()` for all non-pack handoffs |
| **What caused the loss of trust** | Continuity line always *“Building directly on today's {today} work.”* Start Early detail always *“You may begin the introduction today. Tomorrow's Mission will adjust automatically.”* — platform semantics on a study surface. |
| **Educational impact** | Gate TP fails by repetition. Student cannot anticipate the *skill* bridge (e.g. CLT → sampling distributions; estimators → intervals). |
| **Pattern class** | Artificial continuity · Motivation fatigue |
| **Suggested remedy** | Require authored continuity_line naming the cognitive handoff; ban identical tomorrow strings across consecutive Missions. |

---

### LTB-007 — One-way continuity (4.2 → 5.1 preview without 5.1 reception)

| Field | Evidence |
|-------|----------|
| **Day / mission** | End of Day 13 pack Tomorrow Preview → start of Day 14 Mission |
| **What caused the loss of trust** | Pack promises Bayesian foundations with distribution/likelihood continuity. Day 14 Mission has no prior_bridge acknowledging yesterday’s GLM chain work. |
| **Educational impact** | Continuity is a wrap-up courtesy, not a campaign narrative. Feels like marketing copy for tomorrow that tomorrow does not honour. |
| **Pattern class** | Artificial continuity · Abrupt topic transitions (narrative) |
| **Suggested remedy** | Successor package must open with reciprocal prior_bridge; certify pairs/triples, not orphan nodes. |

---

### LTB-008 — Abrupt conceptual leaps without authored bridges (pre-4.2)

| Field | Evidence |
|-------|----------|
| **Day / mission** | Especially Day 8→9 (sampling → estimators), Day 11→12 (testing → regression), Day 12→13 (linear → GLM — remediated only on Day 13 side) |
| **What caused the loss of trust** | Syllabus order is correct, but Missions do not explain the conceptual hinge. Official JSON lacks prerequisite edges; templated rationale cites “next incomplete topic” only. |
| **Educational impact** | Student experiences topic teleportation. Dependency correctness is structural, not taught. |
| **Pattern class** | Knowledge dependency failures · Abrupt topic transitions |
| **Suggested remedy** | Author prerequisite skill statements and prior_bridge on every non-cold-start Mission (EA-003 MG-03). |

---

### LTB-009 — Practice content mismatch / empty retrieval

| Field | Evidence |
|-------|----------|
| **Day / mission** | Non-pack Sessions using `CS1_SCOREABLE_SEED` |
| **What caused the loss of trust** | Seed corpus centres on cash flow, equity method, discounting — not CS1 statistics. Keyword miss → generic fallback one-liner. Only Day 13 Knowledge Checks are syllabus-faithful. |
| **Educational impact** | Active recall is fake or off-subject. Exam preparation trust collapses if a wrong item ever surfaces; if fallback always wins, practice is hollow. |
| **Pattern class** | Educational theatre · Knowledge dependency failures |
| **Suggested remedy** | Replace seed with CS1-statistics items per topic, or suppress Practice stage until package Knowledge Checks exist. |

---

### LTB-010 — Revision programme invisible across the campaign

| Field | Evidence |
|-------|----------|
| **Day / mission** | Full Days 1–14 Learning Mode spine; EV-001 `/student/revision` empty-state at high first-pass claim |
| **What caused the loss of trust** | No student-visible spaced revisit of early chapters while advancing. Reflection residuals unused. “Nothing to revise yet” after alleged coverage. |
| **Educational impact** | Long-term retention strategy absent. After Day 20 / exam approach, student cannot trust Kwalitec for memory. |
| **Pattern class** | Poor revision timing |
| **Suggested remedy** | Schedule Learning Mode revision days inside campaigns (e.g. after Ch 2, after Ch 3); seed revision from completed sittings and residual harvest. |

---

### LTB-011 — Cognitive load does not track syllabus weight

| Field | Evidence |
|-------|----------|
| **Day / mission** | Same Session shell for 2.5 (CLT) and 3.2 (intervals) vs 50–70 min structured Day 13 |
| **What caused the loss of trust** | Harder topics do not receive harder or longer authored pedagogy (except 4.2). Curriculum minute estimates imply multi-hour depth; daily experience is uniform thinness. |
| **Educational impact** | Student under-prepares heavy chapters or abandons the product for CMP pacing. |
| **Pattern class** | Educational pacing failure · Reading overload when student self-scopes CMP |
| **Suggested remedy** | Multi-day certified packages for heavy topics with escalating demands; honest multi-sitting claims on Mission briefs. |

---

### LTB-012 — Confidence / progress theatre (campaign residual from EV-001)

| Field | Evidence |
|-------|----------|
| **Day / mission** | Cross-cutting Home / Syllabus / History / Journey / Decision Journal (EV-001 TB-005, TB-012) |
| **What caused the loss of trust** | High progress % and “High confidence” without sitting memory; Decision Journal boilerplate “highest-value next step”. EA-006 improved 4.2 chrome only. |
| **Educational impact** | Even a perfect Mission day cannot repair scoreboard distrust. Longitudinal reliance fails. |
| **Pattern class** | Student confidence mismanagement · Educational theatre |
| **Suggested remedy** | Outside EA-007 scope (Runtime/progress truth) — but Board records it as a campaign blocker until remediated by a successor programme. |

---

### LTB-013 — Curriculum contaminant on published path (EV-001 residual)

| Field | Evidence |
|-------|----------|
| **Day / mission** | Any Remaining / Map / Up Next encounter with `1 Jln Kilang Timor #06-01 · Singapore 159303` |
| **What caused the loss of trust** | Non-syllabus address node in pathway. Canonical 14-topic JSON is clean; published runtime may not be. |
| **Educational impact** | Catastrophic single-event abandonment risk mid-campaign (EV-001 TB-003). |
| **Pattern class** | Abrupt topic transitions · Educational theatre |
| **Suggested remedy** | Curriculum republish / quarantine (separate programme); do not claim campaign continuity PASS while contaminant remains live. |

---

### LTB-014 — Coverage mirage (7% certified days presented as Educational Excellence pipeline)

| Field | Evidence |
|-------|----------|
| **Day / mission** | Programme narrative EA-005/EA-006 success vs campaign ratio 1/14 |
| **What caused the loss of trust** | Founder/student may infer that publication pipeline implies subject readiness. Longitudinal audit shows one node. |
| **Educational impact** | Institutional over-confidence; shipping pressure before semester continuity exists. |
| **Pattern class** | Artificial continuity · Educational theatre |
| **Suggested remedy** | Gate large-scale publication on campaign continuity PASS (this programme’s bar); publish packages in contiguous arcs, not orphans. |

---

### LTB-015 — Motivation stamp fatigue by mid-week one

| Field | Evidence |
|-------|----------|
| **Day / mission** | Approximately Day 4–5 onward (2.2 / 2.3) |
| **What caused the loss of trust** | Identical educational_context / success_criteria / reflection / tomorrow frames. No new motivational or intellectual variety. |
| **Educational impact** | Engagement becomes mechanical. Textbook feels more “alive” than Kwalitec. |
| **Pattern class** | Motivation fatigue · Educational repetition |
| **Suggested remedy** | Voice variety within EA-002 dial (struggle days, exam-near days, retrieval days) — still one Sensei, not one paragraph template. |

---

### LTB-016 — Day 12→13 handoff asymmetry

| Field | Evidence |
|-------|----------|
| **Day / mission** | End of 4.1 (templated) → start of 4.2 (premium prior_bridge assumes “Yesterday you finished classical linear models”) |
| **What caused the loss of trust** | Pack *assumes* a quality 4.1 day the student may not have received. If Day 12 was empty shell, Day 13’s “yesterday you finished…” feels unearned or false. |
| **Educational impact** | Premium Mission gaslights the prior day. Continuity claim exceeds prior evidence. |
| **Pattern class** | Artificial continuity · Knowledge dependency failures |
| **Suggested remedy** | Certify 4.1 package before or with 4.2; or soften bridge when prior sitting evidence is weak. |

---

## Summary counts

| Severity | Count | IDs |
|----------|------:|-----|
| Catastrophic (would abandon Kwalitec mid-campaign) | 5 | LTB-002, LTB-004, LTB-009, LTB-012, LTB-013 |
| Severe (would dual-track with textbook / lose primary reliance) | 7 | LTB-001, LTB-003, LTB-005, LTB-007, LTB-008, LTB-010, LTB-014 |
| Material (erodes quiet confidence week by week) | 4 | LTB-006, LTB-011, LTB-015, LTB-016 |

**Recurring pattern families (campaign-defining):**

1. Generic Mission / Session / Reflection / Tomorrow stamps  
2. Single-day quality spike (orphan Golden pack)  
3. Absent Reading Guidance and revision spacing  
4. Assessment / progress theatre residuals  

**Register status:** Open — sufficient alone to withhold longitudinal continuity PASS and to delay large-scale educational package publication until contiguous arcs are certified.

---

## Relationship to EV-001

| EV-001 | EA-007 relationship |
|--------|---------------------|
| TB-001 / TB-007 | Partially remediated on Day 13 only (EA-006); remain as LTB-002 / LTB-004 campaign-wide |
| TB-002 | Remains as LTB-001 on non-pack days |
| TB-003 / TB-010 | Retained as LTB-013 |
| TB-004 / TB-005 / TB-012 | Retained as LTB-012 |
| TB-014 | Retained as LTB-010 |
| New | LTB-003, LTB-007, LTB-014, LTB-016 — longitudinal / publication-shape failures invisible in a single-day EV audit |

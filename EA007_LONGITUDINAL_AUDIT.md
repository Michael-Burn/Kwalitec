# EA-007 — Longitudinal Educational Continuity Audit

**Programme:** Educational Excellence Programme EA-007 — Longitudinal Educational Continuity  
**Phase:** Longitudinal Educational Continuity  
**Nature:** Educational continuity audit only — no new educational content; no application code; no Runtime A/C, SCI, Twin, or recommendation redesign  
**Authority:** EA-001 PASS · EA-002 PASS · EA-003 PASS · EA-004 PASS · EA-005 PASS · EA-006 PASS · EV-001  
**Audit date:** 2026-08-01  
**Auditor stance:** Academic Board reviewing an entire semester campaign, not a single lesson  

---

## 1. Purpose

Determine whether a diligent student who follows Kwalitec every day for weeks could sustain trust in a premium educational experience — or whether quality collapses into template monotony, dependency gaps, and educational theatre.

Governing question (asked at every horizon):

> Would this student still trust Kwalitec after Day 20?

---

## 2. Campaign under audit

### 2.1 Selection

| Field | Value |
|-------|-------|
| **Subject** | CS1 — Actuarial Statistics (IFoA 2026) |
| **Canonical source** | `app/curriculum/data/ifoa/cs1/2026.json` |
| **Campaign** | Full CS1 first-pass spine, one planned Learning Mode day per leaf topic |
| **Planned study days** | **14 consecutive topic-days** (within 10–20 requirement) |
| **Realistic stretch note** | Heavy topics (3.2, 4.1, 4.2, 5.1) would expand toward ~18–20 sittings; that stretch **worsens** template fatigue rather than curing it |

### 2.2 Day sequence (student journey)

| Day | Topic | Title (short) | Package coverage |
|----:|-------|---------------|------------------|
| 1 | 1.1 | Purpose and function of data analysis | **None** — templated |
| 2 | 1.2 | Exploratory data analysis | **None** — templated |
| 3 | 2.1 | Basic univariate distributions | **None** — templated |
| 4 | 2.2 | Jointly distributed random variables | **None** — templated |
| 5 | 2.3 | Expectations and conditional expectations | **None** — templated |
| 6 | 2.4 | Generating functions | **None** — templated |
| 7 | 2.5 | Central limit theorem | **None** — templated |
| 8 | 2.6 | Random sampling and sampling distributions | **None** — templated |
| 9 | 3.1 | Estimators and their properties | **None** — templated |
| 10 | 3.2 | Confidence and prediction intervals | **None** — templated |
| 11 | 3.3 | Hypothesis testing and goodness of fit | **None** — templated |
| 12 | 4.1 | Linear regression models | **None** — templated |
| 13 | 4.2 | Generalised linear models | **Certified** — EA-006 published Golden pack |
| 14 | 5.1 | Bayesian statistics fundamentals | **None** — templated |

**Coverage ratio:** 1 of 14 days (≈ **7%**) carries a certified Educational Package. All other days fall through to auto-derived mission templates and generic session substance.

### 2.3 Evidence bases

- Official CS1 2026 syllabus JSON (14 clean leaf topics)  
- Sole published package: `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json`  
- Default authoring: `writing.py`, `tomorrow.py`, `composition.py`, `substance_planner.py`, `derivation.py`  
- Practice seed: `scoreable_seed.py` (CB/accounting-biased corpus)  
- Prior live validation: EV-001 suite (including longitudinal trust 1/10)  
- EA-001–EA-006 educational law and Golden pack quality on Day 13 only  

---

## 3. Method

1. Walk the 14-day campaign as one continuous journey.  
2. Score each audit dimension against EA-001 principles, EA-002 Tutor Voice, EA-003 Mission law, EA-004 Session law, and Gate TP (Tomorrow Preview).  
3. Contrast Day 13 (certified) with Days 1–12 and Day 14 (templated).  
4. Actively hunt trust breaks; do not minimise.  
5. Simulate a student who uses Kwalitec as primary study system daily.

This programme authors **no** new packages and changes **no** application code.

---

## 4. Dimension scores

Scale: **0–10** (Academic Board judgement). **7+** required for campaign-level continuity confidence on that dimension.

| # | Dimension | Score | Verdict |
|---|-----------|------:|---------|
| D1 | Mission continuity | 2 | FAIL |
| D2 | Session continuity | 2 | FAIL |
| D3 | Tutor voice consistency | 2 | FAIL |
| D4 | Reading guidance consistency | 1 | FAIL |
| D5 | Reflection quality over time | 2 | FAIL |
| D6 | Tomorrow Preview quality | 3 | FAIL |
| D7 | Cognitive load progression | 3 | FAIL |
| D8 | Concept dependency correctness | 4 | WEAK |
| D9 | Revision spacing | 1 | FAIL |
| D10 | Motivation without repetition | 2 | FAIL |
| D11 | Educational pacing | 3 | FAIL |
| D12 | Student confidence management | 2 | FAIL |
| D13 | Alignment with CMP progression | 3 | FAIL |
| D14 | Alignment with IFoA syllabus progression | 7 | PASS (structure only) |

**Campaign mean (unweighted):** ≈ **2.7 / 10**

---

## 5. Dimension narratives

### D1 — Mission continuity — **2/10**

**What works:** Syllabus order advances deterministically (1.1 → … → 5.1). Day 13 Mission is a tutor brief with prior bridge from 4.1, unique why-now, and assessable success criteria (EA-006 pack).

**What fails across the campaign:** Days 1–12 and 14 use the derivation pattern `Study {code} — {title}` with rationale of the form *“Today focuses on {code} — {title} because it is the next incomplete topic in syllabus order.”* That is administrative sequencing, not Mission continuity. There is no authored yesterday→today bridge on those days. Day 14 (5.1) does **not** receive a reciprocal prior_bridge from the 4.2 pack — continuity is one-directional and single-day.

**Board judgement:** A semester of Missions that are syllabus pastes with one sudden premium Mission on Day 13 is not continuity; it is a discontinuity spike.

---

### D2 — Session continuity — **2/10**

**What works:** Stage skeleton (Read → Worked Example → Practice → Reflection) is stable. Day 13 Session executes Guided Reading → structure walkthrough → Knowledge Checks → topic-specific Reflection with CMP locus.

**What fails:** Non-pack Sessions reuse interchangeable prompts (*“Read the material for {title}. Note one idea you want to remember.”*; generic four-step worked-example method; generic practice fallback). A student finishing Day 8 cannot distinguish Session pedagogy from Day 3 except by topic noun substitution. Day 14 reverts to that shell immediately after the Golden day — a quality cliff.

**Board judgement:** Session continuity requires *pedagogical* sameness of standard, not sameness of empty scaffold. The campaign delivers the latter.

---

### D3 — Tutor voice consistency — **2/10**

**EA-002 north star:** *“Today we do this, because of that, so you can demonstrate this skill — then we continue here.”*

**Campaign reality:**

| Days | Voice character |
|------|-----------------|
| 1–12, 14 | Template professionalese — calm but interchangeable; topic title inserted into fixed frames |
| 13 | Study Sensei — specific, decisive, misconception-aware, CMP-guiding |

Voice **drifts upward** once then **collapses**. Consistency fails both ways: the student never hears one continuous tutor across weeks, and the premium day teaches them what they were missing — which accelerates distrust of surrounding days.

Forbidden EA-002 patterns present on non-pack days: vague success language (*“Develop a clear, exam-ready understanding of {T}.”*), non-specific tomorrow lines, platform-leaning Start Early copy on Tomorrow Preview.

---

### D4 — Reading guidance consistency — **1/10**

Only Day 13 carries EA-004 Reading Guidance (open / stop / out-of-scope / focus questions / pause points / exit line). All other days instruct *“Read the material for {title}”* without selective CMP map. EV-001 already showed empty reading shells destroy primary-study trust; EA-006 remediated **one** node. Across 14 days the student receives selective guidance **once**.

**Board judgement:** Reading Guidance is not a campaign capability; it is a single-day exception.

---

### D5 — Reflection quality over time — **2/10**

| Days | Reflection character |
|------|----------------------|
| 1–12, 14 | *“Reflect briefly: what in {T} is now clearer, and what still needs careful attention?”* |
| 13 | Harvest stickiest GLM-chain part (family / η / link) + concrete CMP residual for Bayesian bridge |

Identical generic reflection across ~13 days produces **reflection fatigue**. Residuals do not accumulate into a revision programme. Day 13 shows what topic-specific harvest looks like — then Day 14 returns to the stamp.

---

### D6 — Tomorrow Preview quality — **3/10**

| Source | Continuity line pattern |
|--------|-------------------------|
| Default (`tomorrow.py`) | *“Building directly on today's {today} work.”* + Start Early boilerplate |
| Day 13 pack | Authored skill bridge: distribution/likelihood thinking → Bayesian priors/posteriors (5.1) |

Structural successor selection is usually correct on the canonical 14-topic spine. Narrative quality is not. Gate TP requires a continuity sentence that an IFoA tutor would send; the default line fails that test by Day 3 through sheer repetition.

**Additional hazard (published runtime, EV-001):** Tomorrow / Remaining / Map can surface the Singapore address contaminant — destroying continuity messaging even when canonical JSON is clean.

---

### D7 — Cognitive load progression — **3/10**

Syllabus weight rises sensibly (Ch 1 → Ch 4/5). Curriculum minute estimates escalate (e.g. 1.1 ~686 min full coverage vs 4.2 ~2400 min). **Daily Session budgets**, however, do not progressive-load with concept difficulty for templated days — same Read / Example / Practice shell regardless of whether the topic is CLT or GLM. Day 13 alone budgets 50–70 minutes with deliberate stop conditions. The campaign therefore under-loads early days pedagogically (empty depth) and under-structures late days (except 4.2).

---

### D8 — Concept dependency correctness — **4/10**

**Structural:** Official display order is educationally sensible (data → distributions → inference → regression → Bayes). Day 13 pack correctly requires 4.1 fluency and refuses Bayesian teaching on the GLM structure day.

**Lived:** Official JSON has **no prerequisite edges**; order is display_order only. Templated Missions do not state concrete prerequisite skills (beyond generic graph enrichment when available). Practice seed items for CS1 are largely **cash-flow / equity / discounting** — wrong subject family — so retrieval practice on non-pack days can violate concept dependency catastrophically if keywords ever match, or else fall through to a generic one-liner that exercises nothing.

---

### D9 — Revision spacing — **1/10**

Planner infrastructure exists (revision ratio defaults, long-gap rules, Twin-based candidates). Student-visible campaign experience (EV-001 + empty Twin evidence path): **“Nothing to revise yet”** even after substantial first-pass claims. No authored spaced revisit of 1.x–3.x appears inside the 14-day Learning Mode spine. Reflection residuals from templated days are not harvested into Day-N revision Missions.

**Board judgement:** Revision spacing is not operating as an educational campaign feature.

---

### D10 — Motivation without repetition — **2/10**

Motivation on non-pack days is the same sentence shapes with new nouns. After approximately **Day 4–5**, a diligent student recognises the stamp. Day 13’s genuine brief creates a **motivation spike** followed by Day 14 relapse — classic motivation fatigue amplified by contrast. No campaign-level variety of study moves (e.g. deliberate retrieval days, comparison days, exam-style sitting days) appears outside the single Golden pack.

---

### D11 — Educational pacing — **3/10**

IFoA CS1 recommends ~200h; 14 first-pass days cannot cover it — acceptable if the product is honest about multi-sitting topics. The failure is not that 4.2 needs more than one day; it is that **only one authored day exists for 4.2**, and expanding Days 15–20 for remaining LOs would currently regenerate **templated** substance (or repeat the same structure pack identity). Pacing is therefore either too thin (one day per heavy topic) or monotonously padded (extra template days). Neither is deliberate Academic Board pacing.

---

### D12 — Student confidence management — **2/10**

EA-001 / Educational Constitution demand honesty: Study Progress ≠ mastery. Day 13 wrap-up models this well. Campaign-level surfaces (EV-001): High confidence / high progress % with empty sitting history and empty revision — **confidence theatre**. Templated success criteria (*explain core ideas / solve a standard problem*) invite false closure without assessable, topic-faithful checks. Across weeks, the student cannot calibrate confidence from Kwalitec evidence.

---

### D13 — Alignment with CMP progression — **3/10**

Day 13: selective CMP guidance pinned to Syllabus 4.2 setup. Other days: no open/stop/out-of-scope map; student must invent CMP pacing. Guidance Over Content is policy; without Reading Guidance instances, the product fails to *guide*. CMP progression alignment is therefore aspirational for 13/14 days.

---

### D14 — Alignment with IFoA syllabus progression — **7/10**

**Pass on structure:** The audited sequence matches official CS1 2026 leaf order. Topic codes and titles are lawful on the canonical JSON path. Concept leap 4.1 → 4.2 → 5.1 is syllabus-faithful.

**Residual:** Published runtime contaminant nodes (EV-001 TB-003) can break lived syllabus alignment even though this audit’s canonical sequence is clean. Score remains 7 because the **planned campaign under review** uses the official 14-topic spine.

---

## 6. Day-by-day continuity sketch

| Day | Continuity quality | Student likely thought |
|----:|--------------------|------------------------|
| 1 | Cold-start OK as entry; generic Mission | “Admin checklist, but I’ll try.” |
| 2–3 | Bridge is noun-swap only | “Same tutor sentence as yesterday.” |
| 4–6 | Monotony established | “I should open the CMP myself.” |
| 7–9 | Inference weight rises; pedagogy does not | “Kwalitec isn’t teaching harder ideas harder.” |
| 10–11 | Heavy CI / testing days still templated | “Primary study means textbook.” |
| 12 | 4.1 linear models — no authored handoff into GLM | “Why is tomorrow’s leap unexplained?” |
| 13 | **Premium day** — Sensei appears | “Finally — this is what I needed all along.” |
| 14 | Template relapse on Bayesian | “Yesterday’s quality was a one-off. I can’t rely on this.” |

**Trust inflection:** Decline begins by **Day 4**. Partial recovery on **Day 13** is insufficient; **Day 14** confirms the premium day was exceptional, not campaign standard. After Day 20 (if heavy topics are stretched with more template days), trust does not recover.

---

## 7. Artificial continuity and educational theatre

| Pattern | Where observed |
|---------|----------------|
| **Artificial continuity** | Default Tomorrow line claims “Building directly on today’s work” without naming the skill bridge |
| **Educational theatre** | Stable Session stage chrome with interchangeable empty pedagogy |
| **Quality mirage** | One published Golden pack implies programme maturity the campaign does not have |
| **Progress theatre** | (EV-001 residual) Completion / confidence language without sitting memory |
| **Assessment theatre** | Practice seed mismatched to CS1 statistics on non-pack days |

---

## 8. Audit conclusion

| Question | Answer |
|----------|--------|
| Is educational continuity maintained across the audited campaign? | **No** |
| Does tutor voice remain consistent? | **No** — one Sensei day amid template voice |
| Does pacing remain deliberate? | **No** |
| Does revision timing remain appropriate? | **No** — not student-visible |
| Are recurring trust-breaking patterns absent? | **No** — see Trust Break Register |
| Application / Runtime / SCI changed? | **No** (compliant with programme constraints) |

**Longitudinal continuity result: FAIL**

Students could not confidently rely on Kwalitec every day for months on this campaign shape. The Academic Board withholds semester-level educational continuity certification.

---

## 9. Related artefacts

| Artefact | Role |
|----------|------|
| `EA007_TRUST_BREAK_REGISTER.md` | Enumerated trust breaks |
| `EA007_CONTINUITY_REPORT.md` | Continuity synthesis + Day-20 verdict |
| `EA007_EDUCATIONAL_CAMPAIGN_REVIEW.md` | Semester Board review |
| `EA007_IMPLEMENTATION_REPORT.md` | Programme completion report |

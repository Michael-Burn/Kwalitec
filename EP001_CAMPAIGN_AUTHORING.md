# EP-001 — Campaign Authoring (Campaign Alpha)

**Programme:** Educational Production Programme EP-001 — Campaign Alpha Educational Production  
**Campaign ID:** `CS1-EP001-CAMPAIGN-ALPHA`  
**Version:** `ep001-1.0.0`  
**Display title:** Campaign Alpha — From Purpose to Exploratory Judgement  
**Subject:** CS1 · IFoA 2026  
**Scope class:** Pilot Arc (chapter-family: CS1-A Data analysis)  
**CMP edition pin:** IFoA CS1 Core Reading / CMP · 2026 syllabus alignment  
**Status:** Authored · package-certified · Gate CG PASS (see `EP001_CAMPAIGN_CERTIFICATION.md`)  
**Nature:** Production educational content — not Runtime work, not application feature work, not a CS1 subject rewrite  
**Authority:** EA-001…EA-006 PASS · EA-007 FAIL (standing continuity problem) · EA-008 PASS (Campaign law)  

---

## 1. Campaign selection

### 1.1 Why this Campaign begins the student’s journey

Campaign Alpha is the **opening educational campaign** for CS1. It is not defined by “Week 1.” It is defined by the first coherent professional transformation a CS1 candidate must make:

> From *syllabus opener / chart instinct* → to *purposeful actuarial data analysis with disciplined exploratory judgement*.

| Selection test | Decision |
|----------------|----------|
| Begins the official first-pass spine | Yes — lawful cold-start at **1.1** |
| One educational transformation | Yes — purpose → exploratory craft → honest association |
| Contiguous Pilot Arc (≥ 3 Learning + Revision) | Yes — three Learning packages + one Revision |
| Contaminant-free | Yes — only lawful CS1-A nodes |
| Distinct from EA-006 orphan 4.2 | Yes — opening chapter, not mid-spine absorption |

**Why not absorb 4.1→4.2→5.1 first?**  
EA-008 recommends that arc to remediate orphan excellence. EP-001’s brief is the **opening** Campaign — the journey students enter first. Mid-spine absorption remains a successor programme. Campaign Alpha establishes the Study Sensei standard at the door.

**Why not the full CS1-A including PCA (1.2.3)?**  
PCA is a distinct cognitive leap (dimensionality reduction). Forcing it into Day 3 would either overload association day or create a thin fourth Learning day without enough Pilot Arc revision spacing. **1.2.3 is explicitly out of scope** for Campaign Alpha Learning days and is named as a deferred LO for a successor placement — honest completion language, not silent coverage theatre.

### 1.2 Campaign Purpose

This Campaign exists so the candidate can move from an undirected “start CS1 with data” instinct to a professional stance: name the aim of an analysis, choose exploratory summaries and visualisations that serve that aim, and interpret bivariate association without overclaiming — arriving at that chain under one consistent Study Sensei, with one Revision return before the distributional spine opens.

### 1.3 Campaign Educational Objective

**Assessable journey outcome:**  
By Campaign completion, the candidate can **retrieve and connect** (1) the aims/stages/sources/reproducibility purpose map, (2) an aim-linked summary-and-visualisation choice, and (3) a justified Pearson/Spearman/Kendall choice with one explicit non-claim — a competence no single day alone guarantees.

**Does not claim:** Topic Complete for all of 1.2 (PCA deferred); Estimated Mastery of CS1-A; readiness for exam sitting.

### 1.4 Purpose / objective tests (Architecture CP / objective rules)

| ID | Result |
|----|--------|
| CP-01 Educational purpose | PASS |
| CP-02 Distinct from any single Mission Purpose | PASS |
| CP-03 Implies continuity | PASS |
| CP-04 Guidance Over Content | PASS — CMP remains materials authority |

---

## 2. Campaign scope map

| Day | Mode | Topic / LO | Package ID | Display title |
|-----|------|------------|------------|---------------|
| **CA-D1** | Learning | **1.1** | `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | Name why actuarial data analysis exists |
| **CA-D2** | Learning | **1.2** · LO **1.2.1** | `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | Choose summaries and plots for a stated aim |
| **CA-D3** | Learning | **1.2** · LO **1.2.2** | `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | Interpret association without overclaiming |
| **CA-R1** | Revision | Return **1.1 · 1.2.1 · 1.2.2** | `CS1-EP001-PKG-REV-PURPOSE-EDA` | Retrieve the purpose-to-EDA chain |

**Subject + package version:** CS1 · IFoA 2026  
**Day count:** 3 Learning + 1 Revision = 4 Campaign days  
**Out of scope:** 1.2.3 PCA; Chapter 2+ first-pass; CS1B coding marathons; regression/Bayesian chapters  

**Catalogue paths (production content artefacts; not live EA-006 auto-load):**

```text
app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/
  campaign.json
  packages/
    1.1-purpose-function-ep001.json
    1.2-eda-summaries-ep001.json
    1.2-eda-association-ep001.json
    revision-purpose-eda-ep001.json
```

Status on packages: `campaign_member_certified` — **not** in the EA-006 live `publication_approved` loader set. Commercial exposure requires Campaign Publication Approval (`EP001_PUBLICATION_READINESS.md`).

---

## 3. Entry and completion criteria

### 3.1 Entry (CE)

| ID | Applied |
|----|---------|
| CE-01 | Dossier complete (this document + package inventory) |
| CE-02 | First-day package certified |
| CE-03 | Cold-start lawful at 1.1 |
| CE-04 | Contaminant-free |
| CE-05 | CMP edition pin known |
| CE-06 | Day 1 mode = Learning |
| CE-07 | Gate CG PASS before commercial exposure |

### 3.2 Completion (CC) — design-time

| ID | Design satisfaction |
|----|---------------------|
| CC-01 | All Learning packages Session-complete under certified substance |
| CC-02 | All Knowledge Check families authored closed-book |
| CC-03 | Topic-specific Reflections (unique per day) |
| CC-04 | Reciprocal bridges at D1→D2, D2→D3, D3→R1; terminal handoff to 2.1 / deferred 1.2.3 |
| CC-05 | CA-R1 Revision placement required |
| CC-06 | Campaign Objective assessable via R1 triple retrieval |
| CC-07 | Confidence language evidence-linked; no mastery theatre |

---

## 4. Dependency graph (concept hinges)

```text
[Cold start]
    ↓
1.1  Aims / stages / sources / reproducibility
    ↓ hinge: "exploratory stage under a named aim"
1.2.1  Summary + visualisation judgement
    ↓ hinge: "described variables become a bivariate pair"
1.2.2  Pearson / Spearman / Kendall + non-claims
    ↓ hinge: "retrieve the chain before Chapter 2"
CA-R1  Revision return (1.1 + 1.2.1 + 1.2.2)
    ↓ terminal: honest handoff → successor opens 2.1; 1.2.3 deferred
```

---

## 5. Continuity plan

### 5.1 Reciprocal bridge map

| Boundary | Day *n* Tomorrow skill hinge | Day *n+1* prior_bridge acknowledgement |
|----------|------------------------------|----------------------------------------|
| D1 → D2 | Aim/stage named → exploratory tools serve that aim | Yesterday’s purpose map; today inside exploratory stage |
| D2 → D3 | Summaries/plots prepare variables → association | Yesterday’s tool judgement; today bivariate association |
| D3 → R1 | Association done → revision of full chain | Yesterday 1.2.2; today Revision mode, no new LO |
| R1 → next | Campaign complete → 2.1 distributions; 1.2.3 deferred | Successor Campaign entry (not inside this inventory) |

Bridge integrity target: **100%** internal boundaries.

### 5.2 Voice plan

One Study Sensei across all four days. Each day has a **unique Tutor Intent**. Sample audit days: D1, D2, R1 (first / middle Learning / Revision).

### 5.3 Pacing plan

| Day | Load | Rationale |
|-----|------|-----------|
| D1 | Moderate | Conceptual map; light calculation |
| D2 | Moderate–heavy | Judgement density on tool choice |
| D3 | Moderate–heavy | Three-measure discrimination + honesty |
| R1 | Moderate | Retrieval; shorter budget 40–55 min |

### 5.4 Confidence plan

- Progress language = Session / Study Progress / revision Study Progress only.  
- Confidence prompts require a **warrant** tied to today’s checks.  
- Forbidden: Topic Complete from one pass; Estimated Mastery; scoreboard theatre (EV-001 classes denied).

---

## 6. Revision Strategy

| Element | Content |
|---------|---------|
| Placement | **CA-R1** after three Learning days |
| Return targets | 1.1 purpose map; 1.2.1 summary/plot judgement; 1.2.2 measure choice + non-claim |
| Spacing rationale | Protect opening-chain memory before Chapter 2 cognitive load; Pilot Arc minimum satisfied |
| Session shape | Revision Session with closed-book checks first; targeted CMP re-open only on failure (Gate RV) |
| Confidence link | Warrant = weakest retrieved link |

**Forbidden revision theatre denied:** empty “review yesterday”; generic return; spaced-repetition claim without named targets.

---

## 7. Package authoring packs (summary)

Full machine-readable substance lives in the JSON catalogue paths above. Human certification fields summarised here.

### 7.1 CA-D1 — 1.1 Purpose and function

| Field | Value |
|-------|-------|
| Mission Purpose | Professional purpose map so later EDA answers a named aim |
| Tutor Intent | Force aims distinction + one reproducibility element before deep CMP |
| Learning Objective | Explain aims; outline stages and reproducibility for a real-world actuarial problem |
| Reading open/stop | 1.1.1–1.1.4 centre / through reproducibility block |
| Checks | AR: three aims + examples · CP: stages, sources, reproducibility |
| Reflection | Stickiest of aims / stages / sources / reproducibility |
| Tomorrow | Aim-linked EDA tools (1.2.1) |

**Gate self-claim:** MG / SS / LE / TP designed PASS (see Certification).

### 7.2 CA-D2 — 1.2.1 Summaries and visualisations

| Field | Value |
|-------|-------|
| Mission Purpose | Turn purpose map into exploratory craft |
| Tutor Intent | Refuse chart-surfing; aim-first summary + plot |
| Learning Objective | Select and justify summaries and visualisations for aim + variable type |
| Reading open/stop | 1.2.1 / stop before 1.2.2–1.2.3 |
| Checks | AR: skewed claims summary · CP: visualisation + misuse refuse |
| Reflection | Stickiest aim→type / type→summary / summary→plot link |
| Tomorrow | Association measures (1.2.2) |

### 7.3 CA-D3 — 1.2.2 Association measures

| Field | Value |
|-------|-------|
| Mission Purpose | Extend craft into bivariate association without overclaiming |
| Tutor Intent | Force measure sensitivity + refuse causation-from-coefficient |
| Learning Objective | Interpret Pearson / Spearman / Kendall and state inferential limits |
| Reading open/stop | 1.2.2 / stop before PCA 1.2.3 |
| Checks | AR: three-measure discrimination · CP: choose + refuse overclaim |
| Reflection | Stickiest distinguish / choose / refuse |
| Tomorrow | Campaign Revision day (not a new LO) |

### 7.4 CA-R1 — Revision

| Field | Value |
|-------|-------|
| Mode | `revision` |
| Mission Purpose | Protect memory of the Campaign chain |
| Tutor Intent | Closed-book retrieval across three hinges — not CMP re-read theatre |
| Checks | Triple return: purpose · tool judgement · association limits |
| Reflection | Weakest link + scheduled rework; confirm PCA/2.1 out of scope |
| Terminal bridge | Successor opens 2.1; 1.2.3 deferred honestly |

---

## 8. Uniqueness audit (anti-stamp)

| Artefact class | Uniqueness evidence |
|----------------|---------------------|
| Tutor Intent | Four distinct intents (map / refuse chart-surfing / refuse causation / retrieval-not-reread) |
| Why-now | Four distinct reasons (spine start / LO next / examiner discrimination / Pilot Arc memory law) |
| Reflection stems | Purpose-map parts · tool-judgement links · association triad · weakest Campaign link |
| Tomorrow bridges | Skill-named reciprocal pairs; R1 terminal is Campaign handoff not fake next LO |
| Knowledge Checks | Topic-faithful; no CS1_SCOREABLE_SEED generics; no future-skill dependency |

---

## 9. Author quality self-check

| Check | Result |
|-------|--------|
| Mission Blueprint MB-01…MB-08 | Held on all days |
| Session Blueprint SB-01…SB-10 | Held on all days |
| Tutor Voice Guide | Executed; no chatbot / mastery cheer / platform jargon |
| Educational Style Guide | Specific verbs; CMP loci; no placeholder lexicon |
| Campaign Architecture §§3–13 | Dossier fields complete |
| Guidance Over Content | No CMP prose reproduced |
| EV-001 / EA-007 pattern families | Denied by design (see Certification Trust table) |
| Application / Runtime code | Untouched |

**Author sign-off:** Educational Author · EP-001 · 2026-08-01 · packs ready for independent review.

---

## 10. Relationship to EA-006 4.2 pilot

| Item | Status |
|------|--------|
| 4.2 grandfather `pre-campaign-pilot` | Unchanged by EP-001 |
| Campaign Alpha | Separate opening Pilot Arc |
| Mid-spine 4.1→4.2→5.1 absorption | Explicit successor work (not this programme) |

---

Signed notionally: Educational Author · EP-001 · Campaign Alpha Authoring · 2026-08-01

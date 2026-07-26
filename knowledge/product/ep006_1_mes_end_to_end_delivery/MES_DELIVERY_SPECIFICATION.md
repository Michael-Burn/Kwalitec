# EP-006.1 — MES Delivery Specification

**Programme:** EP-006.1 — MES End-to-End Delivery  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Binding delivery contract for successor implementation (this programme does not implement)  
**Authority:** Specialises P-001.2 Explainability Standard for **presentation delivery**  
**Does not:** Change RecommendationService / PlanningService / ReadinessService reasoning

---

## 1. Purpose

Define how Mandatory Explanation Schema (MES) fields must travel from Runtime A service boundaries to student-visible surfaces — including which fields are **mandatory**, **optional**, and **progressive-disclosure** — without inventing new educational meaning.

Companion audit: [`MES_TRACEABILITY_REPORT.md`](MES_TRACEABILITY_REPORT.md).

---

## 2. Non-negotiable constraints

| Constraint | Rule |
|---|---|
| Runtime A ownership | Recommendation, Planning, and Readiness services remain the sole authors of educational judgements and MES content |
| No second narrator | Presentation may **translate terminology** and **layout** fields; it must not invent why, evidence, confidence, or next action when schema-complete payload exists |
| Product Constitution | Advice remains advisory; Learning Mode / Today’s Mission authority preserved (P-001.2 P10) |
| Explainability Standard | Levels, length targets, EIP-003 four questions, and MES field definitions unchanged |
| Architecture Art. IV | Unexplainable guidance remains incomplete — delivery gaps are defects |
| Version 1 | Delivery work targets G1.5 (K8 ≥ 70) trajectory; does not claim G1 PASS alone |

**STOP:** If a design requires soft-amending Vision 2030, Educational Constitution, or inventing opaque AI educational truth → halt and escalate.

---

## 3. Delivery contract — field taxonomy

For each decision class, fields are classified as:

| Class | Meaning |
|---|---|
| **M** Mandatory visible at default level for that surface | Must appear without requiring expand (or lexical equivalent that still contains the element) |
| **D** Progressive disclosure | Must be reachable in ≤1 disclosure control (“Why this?” / “Learn more”); Level-1 summary must remain true when opened |
| **O** Optional | Render when present and student-safe; may omit if empty or not applicable |
| **X** Non-student | Meta/operator only (schema version, internal ranks) — must not leak engineering vocabulary |

### 3.1 Recommendation explanations

**Surfaces:** Student Home Coach / primary tip, Dashboard recommendation card, Revision primary tip.  
**Default level:** Level 1 on daily tip; Level 2 available via one disclosure on Home and Dashboard.

| MES field (service) | Level 1 (always visible) | Level 2 (disclosure) | Notes |
|---|---|---|---|
| Recommendation (`title` / topic) | **M** | **M** | Hero / card title |
| Why (`why_recommended`) | **M** | **M** | Pass through authored text; do not re-synthesise from reason codes when schema-complete |
| Suggested next action (`suggested_next_action` / `next_action`) | **M** | **M** | One clear CTA-aligned action |
| Expected benefit | **O** short cue | **M** | May merge into L1 if ≤40-word budget allows |
| Confidence (`confidence_level`) | **O** lexical (Suggested / Estimated) | **M** + basis cue | Match evidence strength |
| Supporting evidence | **O** one cue | **M** (≤3–4 bullets) | Identifiable syllabus/practice facts |
| Review point | When applicable → **D** | **M** when judgement provisional | Required after thin evidence / provisional rank |
| Plan coherence label | — | **O** | Student-safe wording only |
| Decision ladder rank | — | **X** / **O** diagnostic | Not default daily chrome |
| Personalisation factors | — | **D** when flag ON | Must show provenance if personalisation applied |
| Schema version / level | — | **X** | |

**Honest refusal:** When `honest_refusal` is set, Level 1 must show refusal reason + protective next action; do not fabricate evidence.

### 3.2 Planning explanations

**Surfaces:** Mission / Unified Journey day card, Dashboard mission narrative, Home mission summary.  
**Default level:** Level 1 on start/continue; Level 2 on “Why this plan?” disclosure.

| MES field (service) | Level 1 | Level 2 | Notes |
|---|---|---|---|
| Judgement (today’s plan / focus) | **M** | **M** | Aligns with Mission authority |
| Why this plan (`why_this_plan`) | **M** | **M** | Full sentence; avoid first-sentence-only clip that loses meaning |
| Suggested next action | **M** | **M** | Start / continue CTA text may embody this |
| Expected benefit | **O** | **M** | |
| Confidence | **O** | **M** | |
| Supporting evidence | — | **M** | Observed facts list |
| Plan drivers | — | **M** (≤3 named, ordered) | Student labels; no internal ids |
| Review point | — | **D** / **M** when provisional | e.g. “Reassess after tonight’s session” |
| Change reasoning | — | **D** | Especially after miss/fail / recovery day |
| Readiness / recommendation alignment | — | **O** | Label advisory vs authoritative |
| Personalisation factors | — | **D** when flag ON | |
| Schema meta | — | **X** | |

### 3.3 Readiness explanations

**Surfaces:** Analytics readiness panel (Level 2 default), Home readiness card (Level 1 + disclosure), Dashboard readiness.  
**Default level:** Level 2 on Analytics; Level 1 summary + mandatory Level 2 disclosure on Home (P-001.2 §7.3: never show composite without access to Why + Evidence + Confidence).

| MES field (service) | Level 1 (Home card) | Level 2 (disclosure / Analytics) | Notes |
|---|---|---|---|
| Judgement (label / estimate band) | **M** | **M** | Prefer band language over bare % when thin |
| Why this estimate | **M** one sentence | **M** | |
| Confidence | **M** lexical | **M** + basis | |
| Suggested next action | **M** | **M** | |
| Supporting evidence | — | **M** | Structured list preferred over single blob |
| Readiness drivers | — | **M** (≤4, ordered) | coverage, knowledge, discipline, density — student labels |
| Expected benefit of acting | **O** | **M** | |
| Review point | — | **M** | When to reassess |
| Change reasoning | — | **D** | After new practice |
| Cannot yet be estimated | **M** when applicable | **M** | Prefer honest refusal over soothing composite |
| Schema meta | — | **X** | |

---

## 4. Progressive disclosure rules

1. **Default daily path (Home / Mission start):** Level 1 always visible; Level 2 behind exactly **one** control (`Why this?` / `Learn more` / `explanation_card`).
2. **Judgement surfaces (Analytics readiness, plan detail):** Level 2 by default; Level 3 opt-in only.
3. **No bait-and-switch:** Opening Level 2 must not replace Level 1’s primary reason with a different story.
4. **Clipping policy:** Hard sentence caps are allowed **only** when full MES remains available via disclosure. Clipping that **destroys** mandatory fields without disclosure is non-compliant.
5. **Dual-home interim:** Until a single home is consolidated (EP-005.2 REM-02), **both** Dashboard and Home must meet this contract for the same decision class (P7). Prefer raising Home to Dashboard fidelity — never lower Dashboard to match Home opacity.

---

## 5. Implementation design (presentation only)

### 5.1 Design principles

1. **Pass-through first** — When `has_complete_explanation_schema` (or planning/readiness equivalents) is true, adapters map authored fields 1:1 into student DTOs.  
2. **Re-narration is fallback only** — Reason-code synthesis allowed only when schema-incomplete / cold-start / refusal paths.  
3. **Widen before render** — Extend DTOs before template work.  
4. **Reuse existing macros** — Wire `explanation_card`, `learn_more`, `explainability_block`; extend rather than invent parallel Coach-only speech.  
5. **No educational math in presentation** — No re-ranking, no new drivers, no Twin calls from templates.

### 5.2 Layered change map

| Layer | Change | Ownership preserved |
|---|---|---|
| Services | **None** for educational reasoning | Rec / Plan / Readiness unchanged |
| Bridge mapper | Expand explanation dict to include MES keys (`why_recommended`, `supporting_evidence`, `confidence_level`, `suggested_next_action`, `review_point`, …) | Mapper remains non-authoritative |
| `ExplanationService.from_opaque` | Prefer authored MES keys; fall back to reason-code builder only if incomplete | Student Experience presentation |
| `ExplanationSnapshot` | Add `suggested_next_action`, `review_point`, `confidence_basis` (optional), keep evidence tuple | DTO widen |
| `JourneyContext` / daily mission | Carry why, evidence, confidence, next action, review_point, plan_drivers (student-safe) | Unified Journey assembly |
| `RuntimeAPresentationAdapter` | Map `plan_drivers` / `readiness_drivers` / `review_point` / `expected_benefit` into narratives; stop dropping on schema path | Presentation adapter |
| View models | Stop discarding evidence; coach insight L1 + disclosure for L2; remove hard clip when disclosure present | `view_models.py` |
| Templates | Bind `explanation_card` on `home.html`; Level-2 readiness drivers on Home/Analytics; Mission binds drivers + review_point | Templates only |

### 5.3 Suggested work packages (successor programmes)

| WP | Scope | Depends on | Maps to |
|---|---|---|---|
| WP-A | Widen DTOs + pass-through mapper/ExplanationService | — | Prerequisite for REM-01 |
| WP-B | Home template: Level-1 MES + `explanation_card` Level-2 | WP-A | REM-01 |
| WP-C | Readiness drivers + review_point on Home/Analytics schema path | WP-A | REM-05 |
| WP-D | Planning drivers + review_point on Mission / Journey | WP-A | REM-01 planning branch |
| WP-E | Dogfood checklist + Tier B perception pack | WP-B…D | REM-04 / validation |

Ordering rule: **WP-A before any template claim of “MES complete.”**

### 5.4 Explicit non-goals

- Changing Decision Framework ranking, readiness weights, or plan optimisation.  
- Activating personalisation flags (separate REM-08).  
- Opaque LLM Coach personality.  
- New educational scores or dual runtimes.  
- Declaring Gate G1 PASS from this specification alone.

### 5.5 Compatibility

| Concern | Approach |
|---|---|
| Curriculum V1/V2 | Untouched — explanations cite syllabus topics via existing service fields |
| Feature flags | Personalisation disclosure only when factors present |
| Dual home | Contract applies to both until REM-02 consolidates |
| Tests | Successor adds presentation contract tests: field presence at VM + template smoke; services remain green without change |

---

## 6. Validation plan

### 6.1 Success criteria (measurable)

| Dimension | Metric | Baseline (W-PROD) | Target after implementation + Tier B |
|---|---|---|---|
| **Visibility** | % of Home sessions where L1 why + next action visible without expand | Effectively low (coach clip / no card) | **100%** of schema-complete recommendations |
| **Visibility** | L2 evidence list reachable in ≤1 click on Home | 0% (card unused) | **100%** when evidence present |
| **Visibility** | `review_point` shown when service sets provisional/applicable | 0% surfaces | **≥90%** of applicable payloads |
| **Visibility** | Readiness drivers named on Home/Analytics L2 | Unbound | **≥3 drivers** or honest cannot-estimate |
| **Comprehension** | Blind-review / interview code: student can restate why in own words | Coach opacity Near-Universal | Opacity theme **cleared or minority** |
| **Trust** | K8 category (validated) | **65** | **≥70** (G1.5) |
| **Trust** | Conflicting Why across Dashboard vs Home for same day | Occurs (P7 fail) | **0** material conflicts in smoke pack |
| **Actionability** | Student-reported “I know what to do next” (dogfood / interview) | Weak–Partial | **≥80%** affirmative on Home path |
| **Actionability** | Next action on Home matches Mission CTA intent | Often missing | **Aligned** on smoke pack |

### 6.2 Evidence methods

| Method | When | Pass | Fail |
|---|---|---|---|
| Automated presentation contract tests | CI on successor PR | Required MES keys on Home/Mission/Analytics VMs | Missing mandatory keys |
| Dogfood checklist (internal) | After WP-B/C/D | Why + next visible; drivers unpackable | Opacity / missing next |
| Tier B blind re-review (SV pack) | After presentation soak | Coach opacity not Near-Universal; K8 claimable ≥70 | Opacity persists |
| Validated KSI re-score | Successor to EP-005.1 | K8 ≥ 70; no K1/K2/K3 regression | K8 still &lt; 70 |
| Accessibility spot-check | With WP-B | Disclosure keyboard-operable; meaning not colour-only | Hover-only / colour-only |

### 6.3 Mapping to K8 (Product Success Framework)

| K8 sub-signal | How delivery contract moves it |
|---|---|
| Evidence visibility | L2 supporting evidence mandatory |
| Confidence honesty | Confidence + basis on L2; lexical L1 |
| Next-action clarity | Mandatory L1 next action on Home |
| Consistency (P7) | Same MES story on Dashboard and Home |
| Unpackability | Drivers + review_point on judgement surfaces |

**Expected validated movement (forecast for successor, not this programme):** K8 **+5 to +10** category points if WP-A–D land and Tier B clears opacity → weighted ≈ **+0.7 to +1.4** KSI, unlocking **G1.5** when K8 ≥ 70. Secondary lifts possible on K2/K3 via trust/unpackability (see [`K8_REMEDIATION_PLAN.md`](K8_REMEDIATION_PLAN.md)).

**This programme ΔKSI = 0** — design only.

### 6.4 Failure modes to watch

| Failure | Signal | Response |
|---|---|---|
| Template-only “fix” | Evidence still empty in VM | Enforce WP-A gate |
| Length overwhelm | Students skip L1 | Keep L1 ≤40 words; push detail to L2 |
| Dual messaging | Dashboard Why ≠ Home Why | Pass-through same service payload |
| False confidence | High label with empty evidence | Enforce confidence–evidence coupling tests |
| Claiming G1 early | Marketing before Tier B | Forbidden by P-002.1 |

---

## 7. Acceptance for successor “MES delivery complete”

A successor programme may claim MES delivery complete only when:

1. Traceability omissions in §7 of the Traceability Report are closed for **M** and **D** fields on Home, Mission, and Analytics.  
2. Automated contract tests green.  
3. Dogfood checklist Pass.  
4. Explainability Review Checklist Pass for changed surfaces.  
5. Tier B perception pack scheduled or completed before claiming validated K8 ≥ 70.

---

## References

- [`MES_TRACEABILITY_REPORT.md`](MES_TRACEABILITY_REPORT.md)  
- [`K8_REMEDIATION_PLAN.md`](K8_REMEDIATION_PLAN.md)  
- `../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`  
- `../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md`  

---

**End of MES_DELIVERY_SPECIFICATION**

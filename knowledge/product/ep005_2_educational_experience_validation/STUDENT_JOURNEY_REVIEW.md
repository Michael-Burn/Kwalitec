# EP-005.2 — Student Journey Review

**Programme:** EP-005.2 — Educational Experience Validation  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Evidence audit (no runtime / UI / API changes)  
**Claim window:** W-PROD production defaults unless noted  
**Does not:** Redesign UI; does not change educational authority  

---

## 1. Purpose

Audit the complete student educational loop and, for each step, answer:

1. What educational decision is being communicated?  
2. Is that communication obvious?  
3. Does the student know why?  
4. What action is expected?

Evidence sources: EP-004 blind-review corpus (pre-change perception), EP-005.1 validated KSI package, EP-003.1–.3 quality contracts, template/presentation inventory (presentation ≠ authority).

---

## 2. Journey map (production-default posture)

Two presentation stacks coexist until sole-runtime cutover:

| Stack | Entry | Session path |
|---|---|---|
| Legacy Runtime A | `/dashboard`, `/missions` | Mission hub → session → practice outcome → recorded |
| Canonical Experience | `/student`, `/session` | Home → session overview → activity → summary / reflection |

`KWALITEC_V2_SOLE_RUNTIME` defaults **OFF**. Students may encounter dual homes / dual start paths — a Near Universal friction theme (EV-PERC-002).

Authoritative educational decisions remain Runtime A services (Recommendation / Planning / Readiness). Presentation adapters narrate; they must not re-rank.

---

## 3. Step audits

### 3.1 Dashboard / Student Home

| Question | Finding |
|---|---|
| **Decision communicated** | What to study today; whether on track (legacy: “What to study today, and whether you are on track.” Canonical: Today’s Mission / Guided Study Session hero). |
| **Obvious?** | **Partial.** One primary CTA is enforced on canonical Home (`student.js`), but legacy Dashboard and canonical Home compete for “home” authority when both reachable. |
| **Know why?** | **Weak–Partial.** Legacy “Why this session” is behind `learn_more`. Canonical Unified Journey can surface “Why it matters” in hero when enabled; default Coach compresses explanation to 2–3 sentences without evidence list. Reusable `explanation_card.html` exists but is **not** bound on Home. |
| **Expected action** | Start / Resume Study Session; Create Study Plan; Review Session / Journey. |

**Educational risk:** Decision burden the product claims to remove reappears as “which home / which clock?” (SV-002).

---

### 3.2 Readiness

| Question | Finding |
|---|---|
| **Decision communicated** | Provisional exam-preparation estimate (or honest refusal: “cannot yet be estimated”). Separates coverage / Estimated Knowledge / readiness when EIP-003 narrator is used. |
| **Obvious?** | **Partial.** Percentage and stage labels are visually prominent; meaning is not. |
| **Know why?** | **Weak.** Service attaches `readiness_drivers`, `confidence_level`, `review_point`, `change_reasoning`. Templates typically show narrative prose / confidence chip; **drivers and review point have no direct template bindings**. Canonical Home shows metric + trend + confidence without evidence drill-down. |
| **Expected action** | Schema suggests a next mission/action; UI often merges it into prose rather than a readiness-specific CTA. “Review journey” routes to progress, not readiness working. |

**Student quote (SV-013):** “I get composition. I do not get a defensible readiness story.”

**Educational risk:** Honest empty states are trusted more than filled composites students cannot unpack — overconfidence risk for resitters.

---

### 3.3 Recommendations (Coach / Insights / Tips)

| Question | Finding |
|---|---|
| **Decision communicated** | Primary tip for next focus, with plan-coherence labels (“Aligned with Today’s Mission” / “Advisory — does not replace Today’s Mission”) when EP-003.1 contract is on the path. |
| **Obvious?** | **Partial.** Title and next step are discoverable; coherence labels may be present while confidence chip / ladder rank / review point are not rendered as dedicated controls. |
| **Know why?** | **Weak on default daily surfaces.** Mandatory Explanation Schema exists in RecommendationService; legacy expands “Why this recommendation” (Observed / Estimates / Advice); canonical Home Coach collapses to opaque prose. Near-universal pre-change theme: “highest-value / learning evidence” without working (EV-EXP-003). |
| **Expected action** | Start / continue session; lighter session; advisory tips must not commandeer Mission. |

**Student quote (SV-014):** “It sounds like a conclusion without a derivation.”

**Educational risk:** RecommendationService decision quality can be structurally sound while student trust remains low — **presentation-limited K2**, not necessarily ranking-limited.

---

### 3.4 Daily planning / Today’s Session / Mission

| Question | Finding |
|---|---|
| **Decision communicated** | One authorised focus: Today’s Study Session / Mission topic, duration, success criteria, next step. Tips remain advisory. |
| **Obvious?** | **Strong on a single path** (Learning Workspace Dashboard → Session) when duration agrees. **Weak across surfaces** when dual homes or 30-vs-90 minute mismatch appear (Universal theme, 14+ reviewers). |
| **Know why?** | **Partial.** Labels “Why you are studying this” / “Why it matters” exist; detailed drivers (`plan_drivers`, `change_reasoning`, personalisation factors) remain in payload / collapsed guidance. EP-003.3 recovery paths exist structurally; student visibility of “lighter recovery day” depends on presentation. |
| **Expected action** | Start / Resume / Finish Study Session; Open / Create Study Plan. |

**Student quote (SV-002):** “Home had said 30. Session said 90…. That is decision fatigue the product claims to remove.”

**Educational risk:** PlanningService quality contracts can be schema-complete while experiential authority fractures — **caps validated K1 below Strong**.

---

### 3.5 Study session

| Question | Finding |
|---|---|
| **Decision communicated** | Execute tonight’s objective (canonical: Q&A progression; legacy: timer + checklist activities). |
| **Obvious?** | **Strong once started** on Learning Workspace path — named topic, structure, “what do I do tonight?” answered. Thin Home → Session Overview remains Near Universal friction before start. |
| **Know why?** | **Partial.** Objective / why studying shown on overview; per-activity explanation is post-answer (canonical), not the full MES for the plan/recommendation that selected the session. |
| **Expected action** | Begin; answer / check activities; pause/resume; finish. |

**Educational risk:** Two session models coexist. Client-side timers / sessionStorage checklist state can diverge from planned duration and do not themselves create Estimated Knowledge.

---

### 3.6 Completion / session outcome

| Question | Finding |
|---|---|
| **Decision communicated** | What happened today; what was observed; what can honestly be concluded; what happens next. Legacy Practice Outcome + recorded page is the strongest epistemic separation in the journey. |
| **Obvious?** | **Strong on legacy recorded path** (completion ≠ understanding language valued). **Weaker on canonical summary** (outcomes/readiness change without full evidence/confidence). |
| **Know why?** | **Strong (legacy honesty)** / **Weak (canonical next-recommendation rationale)**. |
| **Expected action** | Record practice results; optional helpfulness/clarity feedback; return Home / Dashboard; continue. |

**Educational risk:** Readiness-change language on completion can be misread as exam prediction unless honesty copy remains adjacent and prominent.

---

### 3.7 Feedback / reflection / analytics

| Question | Finding |
|---|---|
| **Decision communicated** | Optional reflection; analytics trends (readiness, Estimated Knowledge, accuracy, hours, topics needing practice). Learning Feedback Loop (EP-003.4) is **record-only and flag OFF** — not a student-visible closed loop in W-PROD. |
| **Obvious?** | Analytics metrics are visible; **decision usefulness is contested**. Unified Home reflection may state “nothing is saved yet” (presentation-only controls). |
| **Know why?** | Methodology often in tooltips; History lacks causal “why trend changed.” Students struggle to treat analytics as decision-grade learning evidence (baseline / EV-PERC). |
| **Expected action** | Reflect / skip; return Home; optionally use analytics to choose practice focus (weakly guided). |

**Educational risk:** Vanity-dashboard risk (Vision / Never-Build adjacent). K6 remains validated **50** with high confidence that W-PROD lift is zero while feedback flag is OFF.

---

## 4. Journey-level verdict

| Property | Verdict |
|---|---|
| Best student value today | Single-path **nightly workflow director**: named topic → session → honest close |
| Largest experience failures | Dual homes; duration mismatch; Coach opacity; readiness unpackability; thin overview |
| MES / quality contracts | Present in services; **incompletely rendered** on default daily surfaces |
| Closed-loop personalisation | Implemented behind flags; **invisible** in W-PROD |
| Net educational journey maturity | Organisational value **under contested educational authority** (EP-004 strategy bridge) |

---

## 5. Implications for remediation (forward reference)

Journey fixes that raise validated KSI without constitutional conflict:

1. One authoritative home/start/continue path.  
2. One duration fact per day across surfaces.  
3. Level-1 “why” always visible; Level-2 evidence one disclosure away (not compressed into opaque Coach prose).  
4. Readiness drivers + review point visible on judgement surfaces.  
5. Tier B perception re-test after presentation fixes — do not re-score from contracts alone.

Detail and ranking: [`PRIORITISED_REMEDIATION_PLAN.md`](PRIORITISED_REMEDIATION_PLAN.md).

---

## References

- `../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`  
- `../ep005_1_ksi_validation_evidence/KSI_EVIDENCE_REGISTER.md`  
- `../ep004_private_beta/BLIND_REVIEW_META_ANALYSIS_V2.md`  
- `../ep004_private_beta/EVIDENCE_TO_STRATEGY.md`  
- `../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`  
- `knowledge/architecture/ep002_8_presentation_consolidation/`  

---

**End of STUDENT_JOURNEY_REVIEW**

# ILE-001C — Explainability Review

**Programme / Milestone ID:** ILE-001C  
**Title:** Contextual Intent & Educational Framing  
**Date:** 2026-07-28  
**Reviewer:** Implementation agent (product framing review)  
**Surfaces / contracts in scope:** Context Card, Educational Summary, RecommendationFrameContract, ReflectionFrameContract, Mission entry why-body  
**Default explanation level(s):** L1–L2 (daily Adaptive Assessment framing)  
**Runtime A surfaces touched:** Adaptive Assessment Quick Check (Mission-embedded)  

**Canonical checklist:** `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md`

---

## Mandatory verification

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | Pass | Supporting evidence copy cites Mission context + Quick Check; presentation intent focus label — not vague theatre (`educational_framing.py`, `framing.recommendation.supporting_evidence`) |
| R2 | Confidence communicated appropriately | Pass | Qualitative bands Insufficient → Strong; uncertainty shown when not High; no percentages (`EvidenceBand`, `framing.confidence.*`) |
| R3 | Student action is clear | Pass | One primary Begin / Continue / Return; recommendation accept optional; suppress_primary when thin evidence |
| R4 | Avoid unnecessary technical detail | Pass | No Twin / algorithm / pipeline / AI terminology in framing copy; architecture purity tests |
| R5 | Consistency across Runtime A | N/A | Only AA Quick Check surfaces changed; no Coach/Insights/Dashboard recommendation speech in this milestone |

## Schema & level checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Schema fields present | Pass | Recommendation, Why, Evidence, Confidence, Expected benefit, Next action (Begin/Return), uncertainty when applicable |
| S2 | Default level matches job | Pass | L1–L2 for Mission-embedded check framing |
| S3 | Length targets | Pass | Short paragraphs / clear headings in templates |
| S4 | EIP-003 questions | Pass | Why seeing / why now / evidence / next covered by Context Card + summary + recommendation |
| S5 | Facts / estimates / advice distinguishable | Pass | Observation vs meaning vs suggestion vs guidance-only note |
| S6 | Advice does not replace Mission | Pass | Continue with Mission focus; Return to Mission CTA |
| S7 | Explanation patterns | Pass | Maps to ILE-001C0 Adaptive Assessment entry + post-check + recommendation arcs |
| S8 | Accessibility | Pass | Region roles, keyboard details/summary, reduced-motion CSS, plain headings |

**Outcome:** **Pass**

**Notes:** Presentation-only framing. Does not claim Twin-backed warrant strength; default evidence band is provisional (`emerging`) until later eligibility wiring.

---

**End of ILE001C_EXPLAINABILITY_REVIEW**

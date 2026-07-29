# Premium Scorecard — Founder Home

**Programme:** DX-004A  
**Status:** Design review (architecture target)  
**Release Candidate:** `RC-2026.07.29-01`  
**Checklist:** DX-001 `PREMIUM_DESIGN_CHECKLIST.md`  
**Screen:** Founder Home (target design)  
**Reviewer:** DX-004A design authority  
**Date:** 2026-07-29  

---

## Mandatory checks

| Check | Result |
|---|---|
| One Primary action | **PASS** |
| KPI policy respected (no vanity metrics) | **PASS** |
| Cards only for justified grouping | **PASS** (lists; optional single L0 group) |
| Empty state = Reason + Next Action | **PASS** |
| Lucide only; Inter only | **PASS** (spec) |
| Semantic colour only; Gold not UI chrome | **PASS** |
| No implementation leakage in primary UI | **PASS** |
| Motion ≤250ms and purposeful | **PASS** (none required) |

**Mandatory checks: PASS**

---

## Scores (target design)

| # | Dimension | Score | Rationale |
|---:|---|---:|---|
| 1 | **Visual Hierarchy** | **10** | Title → L0 Current Work → Primary → L1 → L2; position + space only |
| 2 | **Task Focus** | **10** | Single question; publication-only; no ops mashup |
| 3 | **Information Density** | **9** | Dense lists where useful; zero KPI clutter; L2 capped at 5 |
| 4 | **Typography** | **10** | 24 / 18 / 16 / 14 per DX-001; no Display inflation |
| 5 | **Spacing** | **9** | Canonical 48 section gaps; restrained L0 stack |
| 6 | **Minimalism** | **10** | Every section justified; forbid list enforced |
| 7 | **Professional Tone** | **10** | Labels not tutorials; no pulse essay; no cheerleading |
| 8 | **Consistency** | **9** | Aligns DX-001–003 + Brand; terminology Home rename noted for dictionary update |
| 9 | **Decision Clarity** | **10** | One Decision → one Action; queue cannot outshout Primary |
| 10 | **Overall Premium Feel** | **10** | Operational Elegance; Linear/Stripe restraint |

**All dimensions ≥9/10.**

---

## Verdict

**SHIP (design)** — redesign required before ship only if implementation regresses any score below 9.

---

## Comparison: legacy Overview (reference)

| Dimension | Legacy (DX-002) | Target |
|---|---:|---:|
| Visual Hierarchy | ~3 | 10 |
| Task Focus | ~3 | 10 |
| Information Density | ~3 | 9 |
| Typography | ~5 | 10 |
| Spacing | ~5 | 9 |
| Minimalism | ~2 | 10 |
| Professional Tone | ~4 | 10 |
| Consistency | ~4 | 9 |
| Decision Clarity | ~3 | 10 |
| Premium Feel | **3/10** | **10/10** |

Legacy failed DX-001 gate. Target clears gate.

---

## Anything below 9?

None on the target architecture. Implementation must re-score against this card in DX-004 UI execution; any dimension ≤8 forces redesign before Alpha claim on Home.

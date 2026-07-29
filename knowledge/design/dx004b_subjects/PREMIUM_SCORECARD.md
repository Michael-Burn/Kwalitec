# Premium Scorecard — Subjects Catalogue

**Programme:** DX-004B  
**Status:** Design review (architecture target)  
**Release Candidate:** `RC-2026.07.29-01`  
**Checklist base:** DX-001 `PREMIUM_DESIGN_CHECKLIST.md`  
**Screen:** Subjects (target design)  
**Reviewer:** DX-004B design authority  
**Date:** 2026-07-29  

---

## Mandatory checks

| Check | Result |
|---|---|
| One Primary action (Create Subject) | **PASS** |
| KPI policy respected (no vanity metrics) | **PASS** |
| Cards only for justified grouping | **PASS** (table/list; no card catalogue) |
| Empty state = Reason + Next Action | **PASS** |
| Lucide only; Inter only | **PASS** (spec) |
| Semantic colour only; Gold not UI chrome | **PASS** |
| No implementation leakage in primary UI | **PASS** |
| Motion ≤250ms and purposeful | **PASS** (search debounce / row hover only) |
| Subjects is the only catalogue | **PASS** (architecture) |
| Object permanence documented | **PASS** (`OBJECT_MODEL.md`) |
| Search-first architecture | **PASS** (`SEARCH_FILTER_SPEC.md`) |
| Navigation boundaries defined | **PASS** (`NAVIGATION_BOUNDARIES.md`) |

**Mandatory checks: PASS**

---

## Scores (DX-004B dimensions — target design)

| # | Dimension | Score | Rationale |
|---:|---|---:|---|
| 1 | **Catalogue Clarity** | **10** | One table; one row = one subject; no hub mashup |
| 2 | **Recognition Speed** | **10** | Name-first rows; search primary; 3-second success test |
| 3 | **Search Experience** | **10** | Search-first; <200ms target; clear/no-match states defined |
| 4 | **Information Density** | **9** | Dense professional table; quiet L2 metadata; no KPI strip |
| 5 | **Object Consistency** | **10** | Permanence contract across Catalogue → Workspace → Publish |
| 6 | **Minimalism** | **10** | Explicit removal set; Open + More only; one Primary |
| 7 | **Professional Tone** | **10** | Labels not tutorials; empty Reason factual |
| 8 | **Navigation Clarity** | **10** | Discovery vs Home vs Workspace vs Review vs Publish owned |
| 9 | **Scalability** | **9** | Hundreds without redesign; virtualisation allowed; same L0–L3 |
| 10 | **Overall Premium Feel** | **10** | Quiet, fast, Linear/Stripe catalogue restraint |

**All dimensions ≥9/10.**

---

## Verdict

**SHIP (design)** — redesign required before ship only if implementation regresses any score below 9.

---

## Comparison: legacy multi-hub (reference)

| Dimension | Legacy hubs (DX-002) | Target |
|---|---:|---:|
| Catalogue Clarity | ~3 | 10 |
| Recognition Speed | ~4 | 10 |
| Search Experience | ~3 | 10 |
| Information Density | ~4 | 9 |
| Object Consistency | ~5 | 10 |
| Minimalism | ~2 | 10 |
| Professional Tone | ~3 | 10 |
| Navigation Clarity | ~2 | 10 |
| Scalability | ~4 | 9 |
| Premium Feel | **~3/10** | **10/10** |

Legacy failed DX-001 gate (tutorial + duplicate catalogues). Target clears gate.

---

## Anything below 9?

None on the target architecture. Implementation must re-score against this card in UI execution; any dimension ≤8 forces redesign before Alpha claim on Subjects.

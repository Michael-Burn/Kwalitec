# DX-004A Executive Summary

**Programme:** DX-004A — Founder Home Redesign (Operational Elegance)  
**Status:** Complete (design architecture)  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None in this programme — documentation only  

---

## Verdict

Founder Home is redesigned from an empty canvas as an **operational workspace** that answers one question: **What should I work on next?** Exactly one Primary action. No KPI theatre. Hierarchy L0 Current Work → L1 Publication Queue → L2 Recent Publications → L3 shell navigation. Premium target **≥9/10 on all dimensions** — design scorecard **PASS**.

This is not a CSS refresh of `overview.html`. Zero Legacy Rule: the current Console Home is treated as if it does not exist.

---

## Design target

**Operational Elegance** — calm, precise, deliberate. Continue publishing curricula with almost no thought:

```
Arrive → Recognise current work → Click Resume → Continue publishing
```

---

## Structure

| Layer | Content |
|---|---|
| **L0** | Current Work — subject, stage, one Primary |
| **L1** | Publication Queue — attention-only rows |
| **L2** | Recent Publications — ≤5, quiet |
| **L3** | Shell nav only — no Quick Actions |

---

## Explicit removals

Platform Summary, Attention KPI grids, Quick Actions, operational detail cards, pulse/timezone essays, version eyebrows, health scores, usage metrics, multi-Primary CTAs, welcome/hero/promotion patterns.

Full register: `CONTENT_REMOVAL_REGISTER.md`.

---

## Authorities applied

| Authority | Role |
|---|---|
| **DX-001** | Type 24/18/16/14; spacing; one Primary; no vanity KPIs; premium gate |
| **DX-002** | Home type; one question; Console nav tree; B-001 decision surface |
| **DX-003** | Decision → Action → Feedback; reading flow; terminology; empty states |
| **Brand Guidelines** | Inter; palette; gold not UI chrome; premium minimal tone |

---

## Impact (when implemented)

| Metric | Legacy Overview | Target | Δ |
|---|---|---|---|
| Independent decisions | 4–6 | 1 | ~75% |
| KPI tiles | 8 | 0 | −100% |
| Primary buttons | 2–5 | 1 | ~80% |
| Premium Feel | 3/10 | 10/10 | Gate cleared |

---

## Non-goals

- No UI / CSS / route code in DX-004A  
- No Subjects redesign (DX-004B)  
- No Workspace stage redesign  
- No student surfaces  

---

## Exit

All DX-004A exit criteria met at architecture level. UI execution must follow `IMPLEMENTATION_PLAN.md` and re-validate the scorecard live before claiming Home complete in product.

**Next:** DX-004B — Subjects Experience Redesign (after Home implementation or as sequential design programme per product sequencing).

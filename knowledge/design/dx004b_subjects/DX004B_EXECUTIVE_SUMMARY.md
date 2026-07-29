# DX-004B Executive Summary

**Programme:** DX-004B — Subjects Experience Redesign (Catalogue First)  
**Status:** Complete (design architecture)  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None in this programme — documentation only  

---

## Verdict

Subjects is redesigned from an empty canvas as the **canonical curriculum catalogue**. It answers one question: **Which subject do I want to work on?** Exactly one Primary action: **Create Subject**. Search-first. Recognition over recall. Object permanence across Catalogue → Workspace → Publication → Review → History. Premium target **≥9/10 on all dimensions** — design scorecard **PASS**.

This is not a dashboard refresh of Studio hubs. Zero Legacy Rule: existing Subjects / Review / Publishing / Versions / Quality hubs are treated as if they do not exist.

---

## Design target

**Catalogue First** — quiet, fast, professional, scalable. Find or create a subject with almost no thought:

```
Arrive → Search or scan → Recognise subject → Open workspace
         or Create Subject
```

---

## Structure

| Layer | Content |
|---|---|
| **L0** | Subject Catalogue — professional table/list; one row = one subject |
| **L1** | Search & Filters — minimal; status / activity / publish readiness |
| **L2** | Quick Metadata — stage, updated, publication status (quiet) |
| **L3** | Shell navigation only — no duplicate local nav |

---

## Explicit removals

KPI cards, analytics, charts, progress rings, platform statistics, tutorial essays, feature promotion, recent-activity feeds, operational summaries, duplicate quick actions, decorative icons, competing Studio hub catalogues (Review / Publishing / Versions / Quality as pages).

---

## Pillar relationship (Founder Operating System)

| Surface | Question | Owns |
|---|---|---|
| **Home** (DX-004A) | What should I work on next? | Continuation |
| **Subjects** (DX-004B) | Which subject do I want to work on? | Discovery |
| **Workspace** (DX-004C) | How do I advance this curriculum? | Execution |
| **Review** | Is this ready? | Verification |
| **Publish** | Can this release? | Release |

Responsibilities must never overlap. Subjects is the **only** catalogue.

---

## Authorities applied

| Authority | Role |
|---|---|
| **DX-001** | Type 24/18/16/14; spacing; one Primary; no vanity KPIs; premium gate |
| **DX-002** | Catalogue type; one question; Console nav; hub consolidation |
| **DX-003** | Decision → Action → Feedback; terminology; empty states; status system |
| **DX-004A** | Home vs Subjects boundary; Operational Elegance tone |
| **Brand Guidelines** | Inter; palette; gold not UI chrome; premium minimal tone |

---

## Impact (when implemented)

| Metric | Legacy multi-hub | Target | Δ |
|---|---|---|---|
| Competing catalogues | 5 hubs | 1 | −80% |
| Primary buttons on Subjects | 2–4 | 1 | ~70% |
| Independent decisions on entry | 3–5 | 1 | ~70% |
| Nav hops to open known subject | 2–4 | 1 (search → open) | ~50–75% |
| Premium Feel (Subjects) | ~3–4/10 | ≥9/10 | Gate cleared |

---

## Non-goals

- No UI / CSS / route code in DX-004B  
- No Founder Home implementation (DX-004A plan remains separate)  
- No Publication Workspace redesign (DX-004C)  
- No student Subject Catalogue redesign (student Ready catalogue remains separate surface)  
- No curriculum engine / V1–V2 changes  

---

## Exit

All DX-004B exit criteria met at architecture level. UI execution must follow `IMPLEMENTATION_PLAN.md` and re-validate the scorecard live before claiming Subjects complete in product.

**Next:** DX-004C — Publication Workspace Redesign (design), and/or Subjects UI execution per `IMPLEMENTATION_PLAN.md`.

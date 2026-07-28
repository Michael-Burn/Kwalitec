# RR-002.3 — Runtime Convergence Report

**Programme:** RR-002 — Governance Convergence  
**Work Package:** RR-002.3 — Repository & Runtime Convergence  
**Date:** 2026-07-28  
**Governance authority:** DG-001.1 · DG-001.2 · DG-001.3 · DG-001.4 · RP-002 · RR-002  
**Companions:** `RR002_3_LEGACY_INVENTORY.md` · `RR002_3_RUNTIME_OWNERSHIP.md`

---

## Executive summary

RR-002.1 and RR-002.2 closed assigned educational **navigation** and **chrome lexicon** findings without retiring dual presentation stacks. RR-002.3 converges **repository guidance**: the Education Operating System under sole runtime is documented as the authoritative student presentation runtime; legacy Runtime A shells are inventoried as Contained / READY FOR MIGRATION; developer docs and template annotations discourage accidental reuse. **No educational behaviour, algorithms, schema, architecture, or student-facing copy changes.**

---

## Problem statement

The repository still carries two student presentation stacks:

1. **Certified:** `/student/*` + `/session/*` (EOS)  
2. **Legacy Contained:** `/dashboard/`, `/missions/*`, `/analytics/` (redirect-gated under sole runtime)

Shared pages flip chrome via `layouts/base.html` (DEP-003). Without a definitive inventory and ownership map, engineers risk extending legacy templates or reintroducing Contained macros onto certified Home — recreating governance regressions RR-001 / RR-002 already closed.

---

## Convergence decisions

| Decision | Statement |
|---|---|
| D1 Authoritative runtime | Sole-runtime EOS (`student` + `session`) is the only certification path |
| D2 Legacy disposition | Legacy shells remain registered + redirect; not deleted in this WP |
| D3 Certified presentation path | Prefer `app/presentation/student|session` and `templates/student|session` |
| D4 Latent macros | `recommendation_card.html` and Runtime C panel are reuse-risk; annotated |
| D5 Terminology | No new educational concepts; mappings recorded from DG-001 / RR-002.1–2 |
| D6 Future cleanup | Explicit candidate list only — retirement requires a later WP |

---

## What was converged (in scope)

| Artefact | Action |
|---|---|
| Legacy inventory | Created definitive classification (certified / shared / legacy / latent) |
| Runtime ownership | Documented authoritative runtime, certified vs legacy components |
| Developer documentation | Updated `ARCHITECTURE.md`, `PROJECT_CONTEXT.md`, `CONTRIBUTING.md` |
| Template annotations | HTML comments on deprecated / latent templates (no markup behaviour change) |
| Completion package | This report + completion report |

---

## What was deliberately not converged

| Area | Reason |
|---|---|
| Student-facing copy | Out of scope; chrome already remidiated in RR-002.1/2 |
| Recommendation / MI algorithms | Excluded |
| Reflection / Journal / Timeline / History | Excluded |
| Database schema / API / flags | Excluded |
| Blueprint deletion | Retirement needs parity evidence (Phase 1 / V2-020) |
| Domain `TERMINOLOGY_MAP` synonyms | Domain student-safety strings; Board lexicon pass if retired |

---

## Relationship to prior packages

| Package | Contribution |
|---|---|
| Phase 0 / Phase 1 | Capability inventory + binding canonical selections |
| DEP-003 | Layout router (EOS vs legacy workspace) |
| EP-007.1 | Sole-runtime home consolidation helpers |
| RR-002.1 | Nav / terminology PC findings closed |
| RR-002.2 | Contained chrome NCR-005–007 closed |
| **RR-002.3** | Repository + runtime ownership documentation |

---

## Developer guidance (normative for new work)

1. Build new student educational UI under `app/presentation/student/` or `app/presentation/session/` and matching `app/templates/student|session/`.  
2. Do not add features to `dashboard/`, `mission/` LXP shells, or `analytics/` presentation except dual-run soak / redirect maintenance.  
3. Extend `layouts/base.html` only when the page must participate in DEP-003 chrome routing; prefer EOS layouts for certified-only pages.  
4. Do not include latent `recommendation_card.html` as a Mission-competing hero on Home.  
5. Obey DG-001 lexicon and authority speech (System / Study Sensei / product).  
6. Treat `READY FOR MIGRATION` and RR-002.3 annotations as **do not extend** signals.

Full ownership table: `RR002_3_RUNTIME_OWNERSHIP.md`.  
Full inventory: `RR002_3_LEGACY_INVENTORY.md`.

---

## Governance impact

| Clause | Effect |
|---|---|
| DG-001.1 | Lexicon mappings inventoried; no new terms |
| DG-001.2 | Authority speech ownership restated; no speech change |
| DG-001.3 | Reflection architecture untouched |
| DG-001.4 | Remediation path RP-002 → RR-002 preserved; residuals remain |
| RP-002 | Does not claim Full Pass; AR-001–007 unchanged |

---

## Architectural regression declaration

| Area | Status |
|---|---|
| Educational Behaviour | **Unchanged** |
| Recommendation Logic | **Unchanged** |
| Mission Intelligence | **Unchanged** |
| Educational Authority Model | **Unchanged** |
| Reflection Architecture | **Unchanged** |
| Database Schema | **Unchanged** |
| API Contracts | **Unchanged** |
| Feature Flags | **Unchanged** |
| Runtime Behaviour | **Unchanged** |

---

## Residual risk

Documentation reduces accidental reuse risk but does not remove legacy code. Dual-run misconfiguration can still surface Contained templates (now lexicon-safe post RR-002.2). Physical retirement remains Board / retirement-programme work.

---

**End of RR002_3_RUNTIME_CONVERGENCE_REPORT**

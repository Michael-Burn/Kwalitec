# DX-004C Executive Summary

**Programme:** DX-004C — Publication Workspace Redesign (Execution First)  
**Status:** Complete (architecture)  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None (documentation-only)

---

## Verdict

The Publication Workspace is redesigned as the **sole execution environment** for curriculum production. It answers exactly one question — **What is the next step for this subject?** — with exactly one Primary action per stage. Review and Publish are stages inside the workspace, not destinations. Premium scorecard target **≥9/10** is met for the architecture.

---

## Operating system position

```
Home (DX-004A)        →  Continue work
Subjects (DX-004B)    →  Find work
Workspace (DX-004C)   →  Complete work
```

| Surface | Owns | One question |
|---|---|---|
| Home | Continuation | What should I work on next? |
| Subjects | Discovery | Which subject do I want to work on? |
| **Workspace** | **Execution** | **What is the next step for this subject?** |

Responsibilities must never overlap. Workspace must not become a catalogue, a second Home, a wizard, or a reporting wall.

---

## Design law: Execution First

Every element on the Workspace must contribute directly to completing publication.

| Include | Exclude |
|---|---|
| Persistent Subject context | Platform summaries / analytics |
| Stage header (where / done / next) | Decorative KPI cards / progress wheels |
| One Primary per stage | Welcome messages / tutorial essays |
| Blocking findings at L0 | Feature promotion |
| Stage content required to advance | Duplicate navigation / secondary dashboards |

---

## Stage model (Founder-facing)

```
Upload → Validate → Review → Approve → Publish
```

Each stage is a **focused mode of the same workspace URL**, not a competing page. Domain workflow stages (`content_sources`, `validation`, `preview`, `approval`, `publication`) map into this model — see `STAGE_MODEL.md`.

---

## Primary action (exactly one)

| Stage | Example Primary |
|---|---|
| Upload | Upload documents / Continue processing |
| Validate | Run validation / Resolve findings |
| Review | Continue review / Confirm structure |
| Approve | Approve |
| Publish | Publish |

The Primary changes with the stage. The page still has only one.

---

## Layout (L0–L3)

| Layer | Content |
|---|---|
| **L0** | Current stage · Primary action · Blocking findings |
| **L1** | Stage content (exactly what is needed to complete the stage) |
| **L2** | Supporting information (prior validation, history, versions) — only when useful |
| **L3** | Technical metadata (IDs, timestamps, diagnostics) — collapsed by default |

Persistent Subject identity (code, name, version, current stage) remains visible above stage chrome and never changes role.

---

## Continuity & completion

- Leaving and returning restores the Founder to the **exact stage** left.  
- Errors appear **inline**; recovery is immediate — no redirect for recoverable issues.  
- Successful **Publish** returns to **Home** with the item in **Recent Publications**.  
- Navigation must not interrupt execution; exit only when the Founder chooses.

---

## Exit criteria (met)

| Criterion | Status |
|---|---|
| Workspace owns execution | ✓ Architecture |
| Review exists only as a stage | ✓ Stage model |
| Publish exists only as a stage | ✓ Stage model |
| Exactly one Primary per stage | ✓ Stage model + architecture |
| Persistent context documented | ✓ `PERSISTENT_CONTEXT_SPEC.md` |
| Premium score ≥9/10 | ✓ Scorecard |

**Next:** DX-004D — Review & Publish Flow Refinement (design refinement of Review/Approve/Publish decision quality within this stage model). UI execution may follow `IMPLEMENTATION_PLAN.md` in parallel with Home/Subjects slices, keeping nav labels coherent.

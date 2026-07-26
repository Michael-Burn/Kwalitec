# MIG-001 — Executive Summary

**Date:** 2026-07-27  
**Programme:** MIG-001 Migration Graph Forensic Investigation  
**Mode:** Investigation only (no code or migration changes)

---

## Verdict

**`202607240001` is not an orphan.** It is the intentional PRD-001 analytics tip on the main Alembic line after `202607230002`. Dual heads exist because **`202607260001` (recommendation commitments) was parented onto historical branchpoint `202611120001`**, not because analytics is dead or disconnected.

**Do not delete, merge-away, or rebase the analytics migration.** Keep it. Resolve the dual-head by reparenting or merging the commitments revision, after an environment stamp audit.

---

## What we found

| Item | Finding |
|---|---|
| Heads | `202607240001`, `202607260001` |
| Analytics feature | Shipped (PRD-001 Approved; ADR-025 Accepted; Phases A–E + EP-002); flag OFF |
| Analytics runtime | Models, SQL stores, CLI, emit hooks present; writes gated |
| Local primary DB | Stamped `202607240001`; analytics tables present; commitments table absent |
| Commitments feature | Live EP-008.3A student preference persistence; separate table |
| CI head pin | Still asserts `202607230002` (already stale) |

---

## Correct fix (choose by gate)

1. **Preferred:** set `202607260001.down_revision = "202607240001"` if never applied anywhere.  
2. **Safe default:** empty merge migration of both heads if any apply risk.  
3. **Never:** delete `202607240001`.

---

## One-line answer for release

The analytics migration should **remain**; the commitments migration should be **reparented onto it** (or **merged** with it) — not removed.

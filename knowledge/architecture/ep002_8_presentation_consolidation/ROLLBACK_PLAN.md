# EP-002.8 — Rollback Plan

**Milestone:** EP-002.8  
**Date:** 2026-07-26  
**Nature:** Fully reversible presentation consolidation

---

## 1. Guarantees

- No data migration
- No schema migration
- No persistence changes
- No production flag defaults changed
- Cutover eligibility unchanged

---

## 2. Behavioural rollback (preferred)

| Step | Action | Effect |
|---|---|---|
| 1 | Ensure all cutover flags OFF | `source_authority=legacy` |
| 2 | Optionally Twin OFF | No Twin assemble |
| 3 | Redeploy not required for flag rollback | Facade serves EIP-003 |

**Kill switches (env):**

- `KWALITEC_STUDY_INSIGHTS_CUTOVER=0`
- `KWALITEC_READINESS_INTELLIGENCE_CUTOVER=0`
- `KWALITEC_DAILY_PLAN_CUTOVER=0`
- `KWALITEC_DIGITAL_TWIN=0` (full Twin off)

---

## 3. Code rollback

If facade itself misbehaves:

1. Revert `app/presentation/intelligence_surface/`
2. Restore prior inline route narration (git revert)
3. Existing cutover projectors remain valid

---

## 4. Verification after rollback

| Check | Expected |
|---|---|
| Production defaults | Legacy surfaces |
| Dashboard recommendations | EIP-003 enrich |
| Readiness narrative | EIP-003 composite |
| Mission narrative | EIP-003 mission |
| Feature-flag tests | Pass with OFF matrix |

---

## 5. Rollback coverage

**Coverage:** Flag-level 100% of Twin-served presentation; code-level revert available.  
**Data risk:** None.

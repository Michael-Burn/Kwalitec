# PX-003 — Confidence Review

**Programme:** Product Experience Programme PX-003 — Workflow Transparency & Confidence  
**Date:** 2026-07-31  
**Question used throughout:** *Has the user seen enough to make this decision confidently?*

---

### Verdict

**PASS (presentation).** High-impact decision points now show enough outcome context before commit. Educational behaviour and workflow gates unchanged.

### Decision points reviewed

| Decision | Before | After | Confident? |
|----------|--------|-------|------------|
| Create Subject | Generic success | Flash names upload as next step | Yes |
| Continue processing | Opaque “Validate” / raw tokens | Plain processing copy + Step X of Y | Yes |
| Generate preview | CTA “Confirm structure” mismatch | “Generate preview”; empty state explains absence | Yes |
| Approve structure | No structure visible on Approve | Preview tree + count summary on Approve | Yes |
| Assign version | Buried under Technical details when primary | Primary strip when required; next-step sentence | Yes |
| Publish | Thin copy; generic success | Summary + ready status; flash explains students can enrol | Yes |
| Start Session (Home) | Decision-only (UX-001) | “After this · …” confidence line; why stays on Overview | Yes |
| Begin Session (Overview) | Briefing collapsed | Briefing open — preview actually previews | Yes |
| Submit answer | Silent redirect | “Answer recorded…” flash | Yes |
| Finish Session | Dense completion wall | Primary outcome first; details disclosed | Yes |

### Confidence principles applied

1. **Preview must preview** — Overview briefing open; Approve retains hierarchy tree; curriculum Preview empty state is honest.
2. **Confidence before commitment** — Approve and Publish show what is being committed.
3. **Confirmations reassure** — Studio and Session success flashes state outcome + next step.
4. **User progress, not system state** — Step X of Y; Ready to publish / Processing / Needs upload.

### Remaining confidence debt

- No modal confirm on Publish/Approve (existing pattern; not added as a feature).
- Publication note field still non-functional if filled.
- Founder Settings lifecycle shortcuts remain advanced/secondary.

# Stage Transition Spec

**Programme:** DX-004C  
**Status:** Binding for workspace stage continuity  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** `STAGE_MODEL.md`, domain studio workflow  

---

## 1. Purpose

Stage transitions must feel like **continuing work**, not navigating to another product. Instant where possible; never a hub detour.

---

## 2. Transition types

| Type | Example | UX |
|---|---|---|
| **Advance** | Validate → Review | Same workspace; update stage chrome + L1; Primary changes |
| **Retreat** | Review → Validate (blocker) | Same workspace; Primary becomes recovery |
| **In-stage refresh** | Re-run validation | Stay on Validate; update findings |
| **Exit complete** | Publish succeeds | Leave workspace → Home |
| **Exit abandon** | Founder chooses Subjects/Home | Persist stage; no reset |

---

## 3. Instant transition rules

Prefer in-place update (full page render or turbo/partial) over multi-route wizard hops.

| Allowed | Forbidden |
|---|---|
| POST advance → redirect to same workspace URL | Redirect to Studio dashboard between stages |
| Flash/inline “Validation passed” | Interstitial “Step complete! What’s next?” chooser |
| Update persistent context stage label | New page title identity (“Review App”) |

Target: stage transitions **instant where possible** (perceived continuity <1s on local).

---

## 4. Continuity persistence

On every meaningful action:

1. Persist `current_stage` (and highest reached if used).  
2. Persist blocking finding snapshot or recompute on load.  
3. On next Open/Resume, restore that stage — **no manual stage picker required**.

Deep links may include stage for support, but canonical open ignores stale UI and trusts server stage.

---

## 5. Gate before advance

| Stage exit | Gate |
|---|---|
| Upload → Validate | Required sources present; processing not failed |
| Validate → Review | Validation passed; blocking count = 0 |
| Review → Approve | Structure/preview accepted |
| Approve → Publish | Approval recorded |
| Publish → Home | Publication succeeded |

If gate fails: stay on stage; show inline reason; Primary = recovery.

UI must not offer Publish as Primary while Validate is blocked.

---

## 6. Stage strip interaction

| Click behaviour | Rule |
|---|---|
| Current stage | No-op / focus L1 |
| Completed earlier stage | Allowed retreat to inspect/fix (not a second Primary) |
| Future stage | Disabled or non-activating until lawful |
| Strip items | Never styled as five equal Primaries |

---

## 7. Feedback after transition

Per Decision → Action → Feedback:

| Event | Feedback |
|---|---|
| Advance | Stage header updates; new Primary visible |
| Validation pass | Inline success; Primary becomes Continue / Confirm |
| Approval | Inline success; Primary becomes Publish |
| Publish | Confirmation then Home + Recent Publications |

No unnecessary confirm modals on Advance. Publish confirm — if required for irreversibility — is a single clear confirm, refined in DX-004D.

---

## 8. Failure during transition

If advance request fails:

- Remain on current stage  
- Inline error  
- Primary = Retry / Resolve  
- Do not bounce to error-only page  

See `ERROR_RECOVERY_SPEC.md`.

---

## 9. Estimated navigation reduction

| Legacy | Target |
|---|---|
| Hub pick (Review / Publishing / Studio) then workspace | Direct workspace stage |
| Separate preview “panel destination” competing with workflow | Review stage in-place |
| Post-publish stay on celebration / re-nav to Overview KPIs | Home Recent Publications |

Expected: **~50–70% fewer destination choices** during a single subject’s publication path vs multi-hub Studio.

---

## 10. Success test

Complete Upload → Publish without visiting any page that is not Home, Subjects, or this workspace.

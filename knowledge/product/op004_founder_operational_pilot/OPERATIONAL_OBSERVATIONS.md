# OP-004 — Operational Observations

**Programme:** OP-004 — Founder Operational Pilot  
**As of:** 2026-07-26 (Day-0 structured rehearsal)  
**Scope:** Operational observations only  
**Does not:** Claim educational effectiveness, KSI improvement, external validation, or Stage 1 readiness  

---

## 1. Observation taxonomy

| Code | Class |
|---|---|
| **OBS-WF** | Workflow operability |
| **OBS-UX** | Usability / copy / navigation |
| **OBS-DOC** | Documentation / runbook clarity |
| **OBS-OPS** | Operator / CLI / rights / rollback |
| **OBS-SEC** | Security / privacy posture (operational) |

---

## 2. Day-0 observations

### OBS-WF-001 — Invite-only registration matches Stage 1 design

**Class:** OBS-WF / OBS-SEC  
**Finding:** There is no public registration route. Account creation is operator CLI (`flask create-test-user`) or controlled invite provisioning.  
**Implication:** Founder pilot “registration” must be scripted as provisioning + first login. External Stage 1 must not assume self-serve signup.  
**Severity:** Info (by design — DR-034).

### OBS-WF-002 — Canonical student journey is operable on paper

**Class:** OBS-WF  
**Finding:** Login → Home tip → commitment confirm/defer → start session → reflection → history is mapped in presentation routes and EP-008.3 commitment services.  
**Implication:** Day-1+ live use can follow the Pilot Runbook day-0 participant script without inventing a second journey.  
**Severity:** Info.

### OBS-UX-001 — Dual export surfaces are easy to confuse

**Class:** OBS-UX / OBS-DOC / OBS-OPS  
**Finding:** Students can export a **learning backup** via Settings (`/settings/export/backup`). Analytics **event** export is operator CLI (`flask analytics-export-user`). Privacy Ops guide emphasises the CLI path.  
**Implication:** Solo founder and future beta operator need a one-line “which export?” card in the invite/support pack.  
**Severity:** P2 (docs / orientation).

### OBS-OPS-001 — Full account deletion is not self-serve in Settings

**Class:** OBS-OPS / OBS-DOC  
**Finding:** Settings data management supports backup/restore (restore deletes then re-imports **learning** records for that user). No dedicated “delete my account” student control was found. Analytics deletion is CLI; educational-domain deletion is documented as existing support/ops workflow.  
**Implication:** Deletion rehearsal on **FND-TST-DEL** requires an explicit ops checklist (analytics CLI + account removal steps). Risk of incomplete rights fulfilment if Stage 1 starts without a written account-deletion procedure.  
**Severity:** P2 (blocks clean CE-04 confidence until procedure exercised).

### OBS-OPS-002 — Rollback R1 is clear; live evidence still blank

**Class:** OBS-OPS  
**Finding:** EP-008.2B Rollback Playbook R1 (flag OFF → restart → metrics verify → educational smoke) is actionable for a founder-operator. Rehearsal log tables in §3.3 / Go-Live §E3 remain empty.  
**Implication:** OP-004 live window is the right place to produce CE-05 evidence — but Day-0 tabletop alone must not be filed as Pass.  
**Severity:** Info / process.

### OBS-DOC-001 — Stage 1 HOLD remains the enrollment truth

**Class:** OBS-DOC  
**Finding:** OP-001 Critical items CE-01…CE-05 remain OPEN / DOC READY; OP-002 dashboard HOLD; PB-001 HOLD.  
**Implication:** Completing founder operational rehearsal improves readiness **preparation** only. It does not lift HOLD.  
**Severity:** Info (governance).

### OBS-SEC-001 — Primary study account must not be the deletion subject

**Class:** OBS-SEC / OBS-OPS  
**Finding:** Plan correctly isolates **FND-TST-DEL** for destructive rights tests.  
**Implication:** Preserve FND-PIL-001 continuity for the 7-day study window; never run `--yes` delete against the primary dogfood account during the pilot.  
**Severity:** Info (control).

---

## 3. Observations deferred to live Days 1–7

These require real daily use and must be filled by the founder during the window (do not invent):

| ID | Prompt |
|---|---|
| OBS-UX-L01 | Time-to-first-useful Home tip after cold login |
| OBS-UX-L02 | Commitment confirm vs defer clarity under real fatigue |
| OBS-WF-L01 | Session complete → reflection → history continuity on a real day |
| OBS-OPS-L01 | Settings backup download size / content adequacy |
| OBS-OPS-L02 | Analytics export/delete dry-run results (dated) |
| OBS-OPS-L03 | Kill-switch rehearsal result (dated) |

---

## 4. Explicit non-inferences

| Observation | Does **not** mean |
|---|---|
| Journey paths exist | Educational effectiveness |
| Founder can dogfood | External validation |
| Export/delete/rollback docs exist | CE-03…CE-05 EVIDENCED |
| Pilot window opened | Stage 1 readiness |

---

**End of OPERATIONAL_OBSERVATIONS**

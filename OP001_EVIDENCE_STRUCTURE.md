# OP-001 — Evidence Structure

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · claim honesty (no fabricated evidence)

**Creates empty structure only.** No fake data. No placeholder results. No invented participants, scores, or interviews.

---

## 1. Root

```text
knowledge/evidence/releases/OP001/
```

Machine-readable pointer: `knowledge/evidence/releases/OP001/README.md`  
Optional manifest: `ops_manifest.json` (status only; zeros allowed).

---

## 2. Folder tree

```text
knowledge/evidence/releases/OP001/
├── README.md
├── ops_manifest.json
├── registers/
│   ├── enrollment/          # Pseudonymous enrollment snapshots (future)
│   ├── consent/             # Completeness flags only — never raw PII
│   └── exclusions/          # Exclusion / duplicate log (future)
├── recruitment/
│   ├── channels/            # Channel summaries (no emails)
│   ├── candidates/          # Pseudonymous candidate cards (future)
│   └── invitations/         # Invite send log pointers (future)
├── onboarding/
│   ├── accounts/            # Provisioning completeness (no credentials)
│   ├── first_login/         # First-login chase notes (future)
│   └── orientation/         # Orientation completion flags (future)
├── support/
│   ├── bugs/
│   ├── feature_requests/
│   ├── questions/
│   └── incidents/
├── communications/
│   ├── sent_log/            # Dates + template IDs + pseudonymous IDs only
│   └── templates_used/      # Which template version was used
├── dashboard/
│   └── snapshots/           # Empty until real counts exist
├── interviews/
│   ├── scheduled/
│   ├── completed/           # Coded sheets later — no fabrication
│   └── declined/
├── consent_logs/            # PLACEHOLDER ONLY — real consent stays in ops store
├── withdrawals/
├── incidents/               # P0/P1 cross-cutting
├── weekly_ops/
│   ├── week_01/
│   ├── week_02/
│   ├── week_03/
│   └── week_04/
└── checklists/              # Completed checklist copies (future)
```

Each leaf directory contains a `README.md` stating **EMPTY — await real artefacts**.

---

## 3. What must never be stored in git here

- Raw emails, phone numbers, full names  
- Passwords, session cookies, magic links  
- Fabricated scorecards, interview transcripts, or dashboard non-zero counts without basis  
- Validated KSI recalculations (out of OP-001 scope)  

Consent **content** belongs in the approved ops consent log (see EP-008.2B template). This tree may hold only pseudonymous “consent recorded Y/N” flags when Founder chooses to archive them.

---

## 4. Relationship to KSI evidence

| Package | Role |
|---------|------|
| `knowledge/evidence/releases/OP001/` | Early Access **operations** evidence |
| `knowledge/evidence/releases/KSI003/` | Prior study attempt (N=0) — historical |
| Future KSI study package | Behavioural / interview / SAP artefacts under study authority |

Do not merge fake study results into OP001 to green G1.9.

---

## 5. STOP

Structure is ready. Filling begins only after Founder-authorised real operations.

Signed: OP-001 Evidence Structure · 2026-08-04

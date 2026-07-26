# EP-009 — Version 1 Operational Hardening

**Programme:** Engineering Programme EP-009  
**Date:** 2026-07-26  
**Status:** Complete (triage + plan) — Stage 1 remains **HOLD**  
**Type:** Operational readiness planning from Founder Operational Pilot findings  
**Upstream:** OP-004 · OP-001 / OP-002 · EP-008.2A/2B  

---

## Board answer (current)

> Did EP-009 clear Stage 1 or fix the product?

# **No**

EP-009 tells the Board **which founder-pilot issues must close before Stage 1** and **which may wait**. It does not execute evidence Passes, lift HOLD, or change application / Runtime A / recommendation behaviour.

---

## Must fix before Stage 1 (Critical / High)

| Priority | Item | Issue |
|---|---|---|
| Critical | File export / delete / kill-switch live evidence (§E1–E3) | ISSUE-003 |
| High | Dual-export operator card | ISSUE-002 |
| High | Account Deletion Checklist (ops path for ISSUE-001) | ISSUE-005 / ISSUE-001 |

## May wait (Medium / Low)

| Item | Issue |
|---|---|
| Self-serve “delete my account” UI | ISSUE-001 (application half) |
| “Registration” wording polish | ISSUE-004 (already DOCUMENTED) |

---

## Artefacts

| File | Role |
|---|---|
| [`ISSUE_TRIAGE.md`](ISSUE_TRIAGE.md) | Class + min solution + severity per OP-004 issue |
| [`IMPLEMENTATION_PRIORITY.md`](IMPLEMENTATION_PRIORITY.md) | Critical/High vs deferred; decision record |
| [`HARDENING_PLAN.md`](HARDENING_PLAN.md) | Work packages WP-A…E |
| [`READINESS_IMPACT.md`](READINESS_IMPACT.md) | Stage 1 / CE / Version 1 impact |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion |

---

## Naming note

This **EP-009** is **Version 1 Operational Hardening**. Earlier roadmap text that proposed “EP-009.x” for personalisation dogfood/cutover is a **different**, uncommissioned recommendation set (P-004.1).

---

## Explicit non-claims

No educational effectiveness · No KSI improvement · No Stage 1 GO · No Version 1 production-ready · No Runtime A / recommendation change · No fabricated CE Passes · No commits  

---

**End of README**

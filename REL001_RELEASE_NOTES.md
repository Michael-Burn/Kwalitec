# REL-001 — Release Notes

**Programme:** REL-001 — Early Access Baseline Release  
**Tag:** `rel-001`  
**Commit:** `95a82b04ae50d32003add3a2f5e6789005a4c962`  
**Version:** `2.0.0-beta.1`  
**Date:** 2026-08-04  
**Audience:** Founder / Early Access operators  

---

## What this release is

The first **external Early Access baseline** on production: a tagged, fingerprinted deploy of the already-validated Premium Experience (PX-007 Conditional PASS) and Early Access operational authority (OP-001 / OP-002 / EA-001), on top of the educationally frozen CS1 Approver inventory (PB-017 · 72/72).

This is an **operational release**. It does not declare Version 1 production-ready.

---

## What students get

- Invite-only access to the LIVE Education OS student home and session spine  
- Full published CS1 Approver educational inventory (Content Freeze held)  
- Premium Experience craft certified Conditional PASS (PX-007)  
- Continuity fixes for tip-complete revision / campaign join races already validated in PX backlog  

---

## What did not change

- Educational package bodies  
- Curriculum JSON / engine  
- Recommendation Engine  
- Student Twin  
- Educational Framework (EF-001)  
- Database schema (Alembic remains `202607310002`)  

---

## Deployment

| Item | Value |
|------|--------|
| URL | https://kwalitec.onrender.com |
| Deploy | `dep-d9p4a85bedkc73e3aa9g` |
| Health / Ready | PASS |
| Smoke | PASS (19/19) |

---

## Known limitations (honest)

- Version 1 production-ready: **NO-GO** (P-002.1 — G1 FAIL, G7 HOLD)  
- Premium Experience: **Conditional PASS** (evidence residuals remain)  
- Educational effectiveness (KSI-003): **NO-GO / Pending Evidence** until a real cohort runs  
- No Early Access invitations are sent by this release  

---

## Operator next step

**STOP.** Await Founder approval before sending the first Early Access invitations (EA-001 / OP-001 G-INVITE).

---

## Rollback

Redeploy `272a0950ca1a65df01badf5e180c3c06a41681e7` (RO-015). No migration rollback required.

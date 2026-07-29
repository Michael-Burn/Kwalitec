# FV-001A — Launch Blockers

**Date:** 2026-07-28  
**Definition:** Stops a first-time founder completing the Version 1 zero-setup → completed study session journey using only the visible product.

---

## Blockers

| ID | Blocker | Phase | Why it blocks launch of *this* journey | Linked findings |
|---|---|---|---|---|
| LB-01 | No self-serve account creation | 2 | Founder cannot enter without external provisioning | UX-C01 |
| LB-02 | Document upload does not yield a trusted curriculum | 5–7 | Failed status + 0 nodes → nothing to review or teach from | UX-C02 |
| LB-03 | Cannot publish founder-created subject to student-ready state | 8 | Publish refused; checklist incomplete | UX-C03 |
| LB-04 | Mission/session topic identity insufficient | 10–12 | Founder will not trust or start real CS1 study | UX-C04, UX-M04 |
| LB-05 | Coach journey step unavailable | 15 | Specified Coach Q&A path does not exist on screen | UX-C05 |
| LB-06 | Console Home mis-orients day-one founder | 3 | “What should I click?” fails the ten-second test | UX-C06 |

---

## Non-blockers (important constraints, not journey killers alone)

| ID | Item | Notes |
|---|---|---|
| NB-01 | Invite-only policy | Acceptable *if* Version 1 declares provisioned access only — still fails self-serve success criterion |
| NB-02 | Publish safety refusals | Correct behaviour; becomes blocker only because upstream extraction never reaches approvable state |
| NB-03 | Revision empty on day one | Honest; redirects to Mission |

---

## Release gate implication

Until LB-01…LB-06 are cleared or the Version 1 scope is **formally narrowed** (e.g. provisioned accounts + built-in CS1 only + Coach descopeed), the FV-001A verdict remains **NO-GO** for the zero-setup founder journey.

Do **not** treat Engineering CRI or architecture completeness as clearing these blockers.

---

**End of Launch Blockers**

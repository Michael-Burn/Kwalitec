# Private Beta — Privacy Review Checklist

**Status:** Documentation package **COMPLETE** (EP-008.2B) — Founder Reviews **SIGNED** (2026-07-26) — Stage 1 enrollment **HOLD** (OR-02 open)  
**Canonical package:** [`../ep008_2b_stage1_pilot_readiness_closure/PRIVACY_SIGNOFF_PACKAGE.md`](../ep008_2b_stage1_pilot_readiness_closure/PRIVACY_SIGNOFF_PACKAGE.md)  
**Updated:** 2026-07-26 (EP-008.2B; GP-001 Founder Review form; OR-01 signed)

## Principles (Vision Data Principles)

- Student data belongs to the student
- Calculations reproducible; recommendations auditable
- Privacy is not optional

## Checklist

Documentation readiness below is verified against the EP-008.2B package and existing ops guides. **Checkmarks do not replace human sign-off** (Founder Reviews recorded below).

- [x] No public registration; invite-only accounts — documented
- [x] Auth cookies / HTTPS / production `SECRET_KEY` validated — factory / Stage 0 posture; reconfirm on deploy
- [x] Support access to accounts is minimised and logged where feasible — documented
- [x] Feedback storage excludes unnecessary PII — documented
- [x] Analytics design (if any) follows Product Analytics Architecture — no new vendor without review — documented (PRD-001)
- [x] Export/delete request path documented (even if manual for beta) — Privacy Ops Guide + EP-008.2B §§9–10
- [x] CSP / third-party scripts reviewed for beta builds — residual accepted for Stage 1 (G10 / PR-023)
- [x] Operators trained not to share student educational data in chats/email threads broadly — operator rule in package
- [x] Privacy notice text reviewed for honesty (no overclaim) — finalized in EP-008.2B §7

## Package coverage (EP-008.2B)

| Element | Location |
|---|---|
| Data inventory | Privacy Sign-off Package §3 |
| Lawful purpose per field | §4 |
| Consent wording | §5 |
| Participant information sheet | §6 |
| Privacy notice | §7 |
| Retention schedule | §8 |
| Export process | §9 |
| Deletion process | §10 |
| Named operational owners | §11 |
| Sign-off checklist | §14 |

## Open items (do not guess)

- Formal DPA / jurisdiction-specific policy for multi-country 2030 goal — track under Version 1 Readiness Commercial/Support (deferred for single-regime Stage 1)
- Automated data-deletion UI — may remain manual CLI in private beta
- Export/delete dry-run evidence — EP-008.2B `GO_LIVE_CHECKLIST.md` §E **Pass** on internal local (2026-07-26); re-confirm on Pilot-hosting env if different before Pilot ON

## External approval

Two Founder Reviews (Product Owner + Privacy Owner capacities) were **required** before Stage 1 external invites (GP-001). Both are **SIGNED** below. External legal counsel / DPO was **not** required for this single-regime Stage 1 package completeness; recommended if privacy competence is insufficient or scope expands (new country, marketing, third-party processor). See Privacy Sign-off Package §13 and `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`.

## Founder Review

| Founder Review | Reviewer | Date | Capacity | Decision | Notes |
|---|---|---|---|---|---|
| OR-01 Privacy — product accuracy | Courage T Shumba | 26 July 2026 | Product Owner | Approve | Mirrored from Privacy Sign-off Package §14 |
| OR-01 Privacy — participant protection | Courage T Shumba | 26 July 2026 | Privacy Owner | Approve | Mirrored from Privacy Sign-off Package §14 |

**OR-01 Founder Review layer is SIGNED.** Until OR-02 dry-run / kill-switch evidence and enrollment clearance are complete: **do not issue Stage 1 external invitations.**

---

**End of PRIVACY_REVIEW**

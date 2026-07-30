# Release Notes — v2.0.0-beta.1

**Product:** Kwalitec Education Operating System  
**Version:** `2.0.0-beta.1`  
**Git tag:** `v2.0.0-beta.1`  
**Date:** 2026-07-30  
**Programme:** RC-001 — Private Beta Release Candidate  
**Audience:** Invite-only Private Beta (Founders + ~10–20 students)

---

## What this release is

This is the official **Private Beta Release Candidate**. It freezes the Version 2 platform for real-user validation. It does **not** introduce new educational engines, AI systems, curriculum reasoning, or UI redesigns.

Everything after this tag should be recoverable, versioned, and traceable.

---

## What students get

- Mission-first Home with clear “what should I do next?”
- Certified CS1 curriculum in the Student Runtime catalogue (when published)
- Study Session with reading progress, timer, and Focus mode
- Tutor and Knowledge Map over certified curriculum context
- Progress / Journey mastery views
- In-product feedback (“Report issue”) for Private Beta
- Footer identity: **Private Beta** · version `2.0.0-beta.1`

---

## What founders get

- Curriculum Studio: upload → structure → certification → publication
- Curriculum Health summary (certification / publication readiness)
- Private Beta Dashboard: enrolment, feedback, observations, end-of-beta report
- Kwalitec Console operational surfaces unchanged in intent

---

## Programmes consolidated in this baseline

| Programme | Contribution |
|---|---|
| EI-001 / EI-002 | Curriculum Intelligence Engine + certified student facades |
| EQ-001 | Educational quality audit artefacts |
| RR-001 | Closed-beta blockers cleared for certified CS1 |
| UX-001 | Premium Private Beta student/founder polish |
| PB-001 | Private Beta validation evidence services + dashboard |
| FV-002 / prior RCs | Founder dogfood and production hotfixes |

---

## What is intentionally out of scope

- Educational quality improvements beyond the certified path
- Mission optimisation and deeper Tutor intelligence
- Knowledge Graph product enhancements beyond certified projection
- Additional IFoA subjects
- Commercial / public beta readiness
- Public self-registration

---

## Upgrade notes

1. Deploy commit tagged `v2.0.0-beta.1`.
2. Ensure `APP_ENV=production`, strong `SECRET_KEY`, PostgreSQL `DATABASE_URL`.
3. Run `flask db upgrade` to Alembic head **`202607300005`** (Render `releaseCommand` does this).
4. Confirm `/health/ready` reports migrations at head and `version` = `2.0.0-beta.1`.
5. Smoke the Founder publish path and one student Begin Learning → session loop.

Rollback: redeploy previous git tag / commit; prefer database restore over `downgrade` if schema reverse is required.

---

## Support

- In-product: Help → Report issue / Private Beta feedback  
- Operator contact: configured via `KWALITEC_SUPPORT_CONTACT` (default `alpha-support@kwalitec.com`)

---

## Related documents

- `CHANGELOG.md`
- `PRIVATE_BETA_GUIDE.md`
- `FOUNDER_DEPLOYMENT_GUIDE.md`
- `knowledge/engineering/rc001_private_beta_deployment/RC001_RELEASE_REPORT.md`

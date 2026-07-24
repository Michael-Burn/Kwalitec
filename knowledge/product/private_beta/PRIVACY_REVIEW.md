# Private Beta — Privacy Review Checklist

**Status:** Checklist prepared — complete before expanding beta cohort

## Principles (Vision Data Principles)

- Student data belongs to the student
- Calculations reproducible; recommendations auditable
- Privacy is not optional

## Checklist

- [ ] No public registration; invite-only accounts
- [ ] Auth cookies / HTTPS / production `SECRET_KEY` validated
- [ ] Support access to accounts is minimised and logged where feasible
- [ ] Feedback storage excludes unnecessary PII
- [ ] Analytics design (if any) follows Product Analytics Architecture — no new vendor without review
- [ ] Export/delete request path documented (even if manual for beta)
- [ ] CSP / third-party scripts reviewed for beta builds
- [ ] Operators trained not to share student educational data in chats/email threads broadly
- [ ] Privacy notice text reviewed for honesty (no overclaim)

## Open items (do not guess)

- Formal DPA / jurisdiction-specific policy for multi-country 2030 goal — track under Version 1 Readiness Commercial/Support
- Automated data-deletion tooling — may remain manual in private beta

## Sign-off

| Role | Name | Date |
|---|---|---|
| Product | | |
| Security / ops | | |

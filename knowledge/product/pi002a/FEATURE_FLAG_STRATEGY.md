# PI-002A — Feature Flag Strategy

**Programme:** PI-002A — Platform Integration: Founder → Student Bridge  
**Date:** 2026-07-27  

---

## Flags

| Environment variable | Effect | Default |
|---|---|---|
| `KWALITEC_FOUNDER_STUDENT_BRIDGE` | Umbrella — enables discovery **and** Runtime C enrolment | OFF |
| `KWALITEC_PUBLISHED_SUBJECT_DISCOVERY` | Surface published subjects in the wizard catalogue | OFF |
| `KWALITEC_RUNTIME_C_ENROLMENT` | Allow Runtime C enrolment via controlled routing | OFF |
| `KWALITEC_RUNTIME_C_SUBJECT_ALLOWLIST` | Comma-separated subject codes that may route to Runtime C from the **legacy** catalogue (still requires enrolment flag + active package) | empty |

Resolution lives in
`app.application.platform_integration.flags.resolve_founder_student_bridge_flags`.

---

## Recommended rollout

```text
Stage 0  All flags OFF          → production unchanged (Runtime A only)
Stage 1  Discovery ON           → published subjects visible; enrolment blocked
Stage 2  Enrolment ON           → Published category can enrol Runtime C
Stage 3  Optional allowlist     → selected legacy codes may route to Runtime C
```

Rollback: unset the flags (or set to `0`). No deploy required beyond config.
Existing Runtime A study plans and Runtime C enrolments already created remain
in their respective tables; new wizard selections revert to Runtime A default.

---

## Truth table (Published category)

| Discovery | Enrolment | Student sees subject? | Can enrol Runtime C? |
|---|---|---|---|
| OFF | OFF | No | No |
| ON | OFF | Yes (Coming Soon) | No |
| OFF | ON | No* | No (not discoverable) |
| ON | ON | Yes (Supported) | Yes |

\*Enrolment flag alone does not expose the category; discovery must be on for
the Published category to appear in the wizard.

# PX-006 — Animation verification

**House motions (PX-B-018):** exactly three intentional patterns

| Motion | Token / class | Use |
|--------|---------------|-----|
| Page enter | `--motion-page-enter` / `.kw-motion-page` / `.page-enter` | Student main presence |
| Success in | `--motion-success-in` / `.kw-motion-success` / `.success-reward` | Session / day-complete celebration |
| Disclosure | `--motion-disclosure` / `.kw-motion-disclosure` | Nav-pending opacity feedback |

## Reduced motion

`prefers-reduced-motion: reduce` disables house animations and nav-pending transitions in `tokens.css` and `student.css` (PX-B-027 dependency held).

## Verification

- Automated: `TestPx006MotionSystem` + token presence asserts.  
- Manual recording: residual **PX6-R1** (screen recording of complete celebration + nav pending with/without reduced motion).

## Out of house (demoted / not claimed as house system)

Welcome-modal / landing ambient animations remain local; certification scorecard should judge primary student path against the three house motions only.

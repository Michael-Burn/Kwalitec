# UI / State Comparison

**Programme:** EV-002  
**Question:** Did workflow succeed while UI lied, or did workflow genuinely fail?

---

## Verdict

| Programme | UI claim | Database / authority | Honesty |
|---|---|---|---|
| EV-001 Studio path | Pass through Published / Ready | Package active; `publication_state=published` | **Aligned (success is real)** |
| EV-001 Choose Exam | Error page | Package exists; `_format_release` type bug | UI fails **after** Ready (known minor condition) |
| FV-001B Validate→Ready | Fail / contradictory | `draft` / no package | **Aligned (failure is real)** |

FV-001B is **not** Case B (stale UI hiding success). CS1F never became Ready in authority storage.

---

## Flash vs status cards

### EV-001

| Action | Flash | Status card | Match? |
|---|---|---|---|
| Validate | Success | `passed` | Yes |
| Preview | Success · 23 topics | `ready_for_review · 23 topics` | Yes |
| Approve | Success | `approved` | Yes |
| Publish | Success | Published · 2026.1 | Yes |

Residual UI debt on EV (non-blocking for lifecycle): stale NEXT STEP still mentions upload after docs Ready; Management warning “Missing learning objectives asset reference” remains visible after pass.

### FV-001B Final

| Action | Flash | Status card / other | Match? |
|---|---|---|---|
| Validate | Blocking findings remain | `in_progress`; Overview “0 validation errors”; CIP panel warning on doc 7 | **Internal contradiction**, but refusal is real |
| Preview | Success · 2 topics | `not_ready · 2 topics`; version `preview_ready` | **Contradiction**; readiness not achieved |
| Approve | Publish refusal copy | No approved line | Failure real; **wrong verb** for control |
| Publish | Same refusal | Not Published | Failure real |
| Subjects | — | No Ready / Published Date | Matches DB |

---

## Authority state

| | EV-001 CS1V | FV-001B CS1F |
|---|---|---|---|
| Foundation publication_state | `published` | `draft` |
| Active `published_curriculum_packages` | Yes | No |
| Subjects hub Ready | Yes | No |

---

## Conclusion

- EV-001 Studio success is backed by DB.
- FV-001B failure is backed by DB.
- FV UI contains **messaging contradictions** on a failed workflow; those contradictions do not invent a Ready package.
- Mutual exclusivity is therefore **not** “one UI lied about the same underlying Ready subject.”

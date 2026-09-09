# Session Architecture Decision: Multi-Unit Sitting (Additional Daily Study)

**Document type:** Architectural decision record (reached through investigation and design discussion; not a formal EF-001 Operational Review)  
**Topic:** Multi-unit sitting for additional daily study  
**Status:** Accepted (continue-studying flow implemented under existing one-unit law)  
**Date:** 2026-09-09  
**Basis:** Item 12 investigation and plan (2026-09-09), sibling boundary review [`EF001_OPERATIONAL_REVIEW_INTERLEAVED_PRACTICE.md`](EF001_OPERATIONAL_REVIEW_INTERLEAVED_PRACTICE.md), live sitting law (arbitration one-package sitting; Educational Atomicity; student-selected session provenance)

---

## Context

Students who finish today's recommended daily mission may still have time and willingness to study further the same day. Two architectural shapes were considered:

1. **Multi-unit sitting**: combine more than one atomic educational unit into a single continuous sitting (system-composed or system-extended after the daily package).
2. **Subsequent distinct sessions**: keep one atomic unit per sitting; after the daily mission completes, invite the student to start another, separate session they choose themselves.

Live product law already encodes one package / one primary purpose per sitting (arbitration “No session-split mixing”; Educational Atomicity; daily mission one-package structure). Student-selected Study already creates genuine sessions with `session_origin=student_selected` that do not complete today's recommended mission.

Supporting additional daily study through a first-class, honestly worded invitation into existing Study / student-selected start is a product surface and telemetry concern under **existing** sitting law. It does not require changing Educational Atomicity, arbitration, Spacing Scheduler, Policy V1, or the daily mission's one-package structure. Multi-unit sitting as a combined sitting mechanism would be a different concern (closer to composition / framework collision); that mechanism is **not** chosen here.

After day-complete, Home previously offered only a quiet Study link and copy that pushed “return tomorrow,” which understated lawful additional study and left the continuation path easy to miss. That reduces educational usefulness of spare capacity without blocking the primary daily mission.

## Investigation basis

| Finding | Reference |
|---------|-----------|
| Freeze law; prefer interventions under existing Educational Law | `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md`; `.cursor/rules/11-educational-framework-freeze.mdc` |
| One package per sitting; no session-split mixing | `app/application/adaptive_decision/arbitration.py`; sibling `EF001_OPERATIONAL_REVIEW_INTERLEAVED_PRACTICE.md` |
| Educational Atomicity (one capability / purpose per episode) | `knowledge/version2/education/EDUCATIONAL_ATOMICITY.md` |
| Student-selected sessions do not complete the daily mission | `app/application/student_runtime/coordinator.py` `start_student_selected_session`; `SESSION_ORIGIN_STUDENT_SELECTED` |
| Day-complete Home previously had empty primary CTA | `app/presentation/student/services/student_home_service.py` day_complete branch (pre-change) |

## Decision

**Decision (locked):**

> Multi-unit sitting considered and intentionally deferred. Current architecture retains one atomic unit per sitting. Additional daily study is supported through subsequent, distinct, student-directed sessions rather than a single combined sitting.

**Implement under that decision:**

1. Keep the daily system as the sole authority for what deserves **first** attention today.
2. After the daily mission is genuinely completed, surface a first-class Home invite worded as student-directed capacity (**Want to keep studying?** / **Choose a topic**), not as a second recommended session.
3. Route that invite into existing Study → `start_student_selected_session` so provenance remains `student_selected`.
4. Do not have Home or Coach choose or suggest which topic the second session should be.
5. Instrument factual presentation telemetry for the path only (completed, prompt shown, selected, second session started, second session completed).
6. Do not change arbitration, Spacing Scheduler, Policy V1, or daily-mission one-package composition in this work.

**Rejected under tonight’s discipline:**

- Building multi-unit / combined sittings.
- Letting the daily recommendation system also decide what happens after day-complete.
- Copy that implies “here is your next session” after the recommended mission is already finished.

## Framework boundary

This decision proceeds under existing Educational Law without modifying the frozen Educational Framework.

Additional daily study via subsequent student-directed sessions uses existing Study / student-selected provenance and leaves one-unit-per-sitting law unchanged. Multi-unit sitting remains deferred; pursuing it later would need its own review against Atomicity and arbitration, and is not authorized by this decision.

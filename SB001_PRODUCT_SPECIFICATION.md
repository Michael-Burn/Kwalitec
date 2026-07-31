# SB-001 — Student Baseline & Continuity (Product Specification)

**Status:** Product law  
**Programme:** SB-001 / Implementation SB-001A  
**Authority:** RF-001 · BF-001 · RF-001A · PRODUCT_BLUEPRINT.md · STUDENT_DIGITAL_TWIN.md · PRODUCT_EXPERIENCE_GUIDELINES.md

---

## Principle

The first question Kwalitec answers is **where the student is today**, not what they should study today.

Every newly enrolled subject begins with a Baseline Assessment. Students must never automatically start from Chapter 1.

## Captured information

| Field | Choices / shape |
|-------|-----------------|
| Previous experience | Brand new · Started · About halfway · Mostly completed · Revision phase |
| Curriculum position | Start from beginning **or** continue from a topic (official hierarchy) |
| Exam history | First sitting · Previously attempted (+ optional highest mark) |
| Study objective | Continue · Restart · Recommend best starting point |
| Confidence | Very low → Very high (self-assessment only) |

## Non-goals (Version 1)

Adaptive placement tests, knowledge diagnostics, AI confidence estimation, automatic syllabus inference.

## Implementation

Executable behaviour is delivered by **SB-001A** (Baseline Integration & Runtime Bridge). See:

- `SB001A_IMPLEMENTATION_REPORT.md`
- `SB001A_BASELINE_FLOW.md`
- `SB001A_DIGITAL_TWIN_MAPPING.md`
- `SB001A_RUNTIME_BRIDGE.md`
- `SB001A_CALIBRATION_DEPRECATION.md`

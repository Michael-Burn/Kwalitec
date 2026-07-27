# EQ-001 — Educational Quality Standard

**Programme:** EQ-001 — Educational Quality Certification  
**Version:** 1.0  
**Status:** Active — educational quality authority for automatically generated Runtime C artefacts  
**Effective:** 2026-07-27  
**Authority:** Product educational-quality law for published-curriculum generation  

---

## 1. Purpose

This standard defines **what constitutes educationally high-quality automatically generated learning artefacts** in Kwalitec before any Runtime C cutover.

It covers:

- Study plans derived from published curriculum
- Daily missions instantiated from mission templates
- Journey progression / transitions
- Progress-model denominators
- Learning-objective mapping on generated artefacts

It does **not** redesign UI, activate Twin, or cut over Runtime A.

**Educational quality maximises lawful learning usefulness of artefacts already derived from published curriculum.  
It never invents mastery, exam guarantees, or a second educational brain.**

---

## 2. Product objectives

| Objective | Student outcome |
|---|---|
| Curriculum-bound learning | Every plan and mission maps to an official syllabus topic. |
| Objective transparency | Learning objectives that the mission advances are visible and structured. |
| Realistic effort | Duration estimates and pacing respect published minutes and exam dates. |
| Prerequisite honesty | Students never jump a required topic without an explicit, explainable gate. |
| Explainable decisions | Why today, why previous is complete, and what unlocks next are always answerable. |
| Certifiable generation | Newly published subjects produce artefacts that pass automated quality checks. |

**Final Test alignment:** Artefacts that help candidates become better professionals pass. Artefacts that are merely technically valid but educationally opaque fail.

---

## 3. Artefact quality contracts

| Artefact | Governing rules | Automated certifier |
|---|---|---|
| Mission (template + instance) | [`MISSION_QUALITY_RULES.md`](MISSION_QUALITY_RULES.md) | `EQ-M*` |
| Study plan (template + pacing) | [`STUDY_PLAN_QUALITY_RULES.md`](STUDY_PLAN_QUALITY_RULES.md) | `EQ-P*` |
| Journey transitions | [`JOURNEY_QUALITY_RULES.md`](JOURNEY_QUALITY_RULES.md) | `EQ-J*` |
| Explainability envelope | [`EXPLAINABILITY_SPECIFICATION.md`](EXPLAINABILITY_SPECIFICATION.md) | `EQ-X*` |

---

## 4. Relationship to existing product law

| Authority | Relationship |
|---|---|
| Vision 2030 | Highest philosophy; quality operationalises “What should I do now?” with syllabus honesty. |
| Explainability Standard (P-001.2) | Owns how guidance explains itself; EQ-001 supplies Runtime C structured envelopes compatible with that schema. |
| Recommendation Quality Standard (P-001.3) | Owns recommendation prioritisation; EQ-001 owns generation quality of plans/missions/journey. |
| PI-001A/B/C/D | Platform structural certification; EQ-001 adds educational quality certification on the same pipeline. |

Authority order for generated Runtime C artefacts:

```
Published curriculum package (PI-001A)
        ↓
Educational derivation (PI-001B)
        ↓
THIS STANDARD (mission / plan / journey / explainability quality)
        ↓
Educational Runtime Engine instantiation (PI-001C)
        ↓
Automated EQ certification tests
```

---

## 5. Non-goals

- Runtime A cutover or dual-run production switch
- UI redesign or new student chrome
- Twin / Adaptive interruption activation
- LLM-authored educational rationale
- Claiming Exam Ready or mastery from mission completion alone

---

## 6. Acceptance (programme)

A newly published subject must automatically generate:

1. Curriculum-bound study plans (syllabus order + prerequisite integrity)
2. High-quality daily missions (topic, LOs, duration, completion definition, rationale, prerequisite validation)
3. Explainable educational decisions (structured envelope suitable for student display)
4. Correct prerequisite sequencing
5. Realistic pacing with exam-date awareness and revision allocation in the projection
6. Transparent student guidance (why today / why previous complete / what unlocks next)

Evidence is produced by automated certification tests under `tests/certification/` and summarised in [`TEST_EVIDENCE.md`](TEST_EVIDENCE.md).

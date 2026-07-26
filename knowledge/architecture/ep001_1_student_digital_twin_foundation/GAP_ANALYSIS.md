# EP-001.1 — Gap Analysis

**Milestone:** EP-001.1 — Student Digital Twin Foundation  
**Phase:** 3 — Gap Analysis

Compare existing implementation vs constitutional Student Digital Twin specification (`STUDENT_DIGITAL_TWIN.md` + Constitution + MS-004).

---

## 1. Missing capabilities

| Capability | Spec expectation | Gap |
|---|---|---|
| Canonical consumer read path | Subsystems obtain learner state from Twin | Consumers still hit ORM / ReadinessService / demo Twin independently |
| Knowledge / mastery surface | Twin Knowledge domain | MS-004 facets omit Knowledge pass-through; Epic Twin structural only |
| Topic progress surface | Twin references progress | Collectors have it; no foundation DTO packages it for consumers |
| Learning evidence surface | Evidence log feeds Twin | Evidence exists; foundation does not expose refs as canonical read |
| Practice performance | Performance domain | Attempt accuracy available; not packaged on Twin foundation |
| Mock performance | Performance / mocks | No typed mock evidence — must remain honest `unavailable` |
| Study behaviour | Behaviour domain + MS-004 facets | Facets exist; not composed into one foundation state |
| Study consistency | Behaviour / Motivation | MS-004 ConsistencyFacet + Readiness discipline — not unified |
| Streaks | Behaviour / Motivation | Only `ReadinessService` — not Twin |
| Mission completion | Behaviour evidence | Mission collector exists; not foundation-packaged |
| Twin Authority cutover | MS-004 migration T4 | Flag documented, not implemented |

---

## 2. Duplicate capabilities

| Duplicate | Risk | Consolidation preference |
|---|---|---|
| Epic Twin vs V2 student_twin vs EOS Twin | Competing learner-state narratives | Epic Twin + MS-004 Foundation for Runtime A product; V2/EOS remain non-authority |
| Experience demo Twin vs MS-004 projection | Demo theatre vs Runtime A truth | Authority ON → Foundation; demo seeding off under Authority |
| ReadinessService streaks vs Twin Behaviour | Split behavioural truth | Foundation pass-through from ReadinessService (Runtime A) |
| Analytics/dashboard SQL vs Twin | Divergent readiness stories | Future consumers should prefer Foundation for learner-state claims |

---

## 3. Consolidation opportunities

1. **Extend** `app/infrastructure/adapters/digital_twin/` with Foundation (reuse collectors / evidence bag).
2. **Extend** `ReadinessCollector` to pass through streak facts (no new streak algorithm).
3. **Wire** optional Authority port over existing `StudentTwinPort` — do not invent a new Experience port.
4. **Document** Epic Twin as constitutional aggregate; MS-004/Foundation as Runtime-A synthesis read path.
5. **Do not** migrate V2/EOS into Foundation in this milestone — label them parallel.

---

## 4. Architectural risks

| Risk | Severity | Mitigation |
|---|---|---|
| Fourth Twin stack | Critical | Foundation is an extension of MS-004 adapters only |
| Twin overwrites Runtime A mastery | Critical | Foundation is read-only pass-through; no write-back |
| Premature Authority ON in production | High | Default OFF; requires Twin ON; fallback to ExperienceTwinAdapter |
| Fabricating mock performance | High | Explicit unavailable when mocks cannot be distinguished |
| Claiming Twin Ready / MS-004 complete | Medium | Foundation ≠ T7 soak; docs remain clear |

---

## 5. Recommendation

Implement Foundation by **extending MS-004**, packaging Runtime A facts into `CanonicalLearnerState`, and adding a **default-OFF** Authority seam — not by replacing ORM write paths or inventing parallel models.

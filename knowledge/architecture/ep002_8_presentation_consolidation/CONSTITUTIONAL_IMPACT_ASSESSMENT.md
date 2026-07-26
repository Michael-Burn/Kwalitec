# EP-002.8 — Constitutional Impact Assessment

**Milestone:** EP-002.8 — Presentation Consolidation  
**Date:** 2026-07-26  
**Legend:** **O** / **E** / **C** / **R**

---

## 1. Ownership impact

| Owner | Pre-EP-002.8 | Post-EP-002.8 | Drift? |
|---|---|---|---|
| Presentation | Route-local narrator selection (duplicated) | Unified `RuntimeAPresentationAdapter` | None — presentation still owns presentation |
| Insight / Study Insights | Owns Twin recommendation communication when cutover serves | Unchanged; facade skips EIP-003 re-narration | None |
| Readiness | Owns evaluation; EIP-003 still narrated composite on Twin path | Evaluation unchanged; Twin surface owns composite speech when served | Closes TD-RI-02 presentation drift |
| Planning | Owns planning; Twin display via cutover | Unchanged; shared mission narrative helper | None |
| Consumer Chain | Orchestration / cutover | Unchanged | None |
| EducationalExplainability | Parallel peer on several Twin surfaces | Legacy presentation adapter under facade | Intentional demotion for Twin-served surfaces |

**O:** Constitution Article III — narrative polish flows outward as presentation, never back as educational authority.  
**E:** `docs/ARCHITECTURE_CONSTITUTION.md`.  
**C:** Mapping Twin fields → template narrative DTOs is presentation; it does not invent scores.  
**R:** Adapter must only reshape authorised surface fields.

---

## 2. Narrator consolidation impact

| Surface | Communication SoT when Twin served | Legacy SoT |
|---|---|---|
| Recommendations | Insight projection fields (`source_authority=study_insights`) | EIP-003 `enrich_recommendations` |
| Readiness composite | Twin readiness surface (`drivers`, score, confidence, next actions) | EIP-003 `explain_composite_readiness` |
| Topic rows | Twin area rows as projected | EIP-003 `enrich_topic_rows` |
| Mission index / dashboard mission | Twin slot `reason` + display title | EIP-003 `build_mission_narrative` |
| Coverage readiness | Always curriculum coverage (ORM) | EIP-003 `explain_coverage_readiness` |
| Session feedback | Always ORM session | EIP-003 `build_study_session_feedback` |

**C:** One selection authority; two speech sources (Twin projection vs EIP-003 legacy). Not a third speech engine.

---

## 3. Fail-open / rollback impact

**O:** Cutover eligibility and fail-open remain in Consumer Chain.  
**E:** EP-002.5–7 cutover modules; production env hard-ineligible.  
**C:** Presentation consolidation does not alter who is eligible to receive Twin payloads.  
**R:** Rollback remains flag OFF → legacy EIP-003 path via same facade.

---

## 4. STOP conditions

| Condition | Triggered? |
|---|---|
| Presentation would own readiness maths | No |
| Presentation would own planning | No |
| New narrator inventing educational certainty | No |
| Persistence / schema change required | No |
| Production-wide activation required | No |
| Conflict with Architecture Constitution Articles I–VI | No |

**Verdict:** **Accept** constitutional posture for EP-002.8 implementation. **No STOP condition triggered.**

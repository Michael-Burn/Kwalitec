# PRD-001A — Blueprint Capability Matrix

**Source of truth:** `PRODUCT_BLUEPRINT.md` v1.1 (July 2026)  
**Supporting authorities:** Vision 2030; Educational Constitution; `PROJECT_CONTEXT.md` core capabilities  
**Method:** Extract every major capability the Blueprint (and its named educational model) promises as product behaviour. Each row is an audit item for Parts 2–10.

---

## Inventory rules

- Capabilities are **product promises**, not file names.  
- Vision philosophy items are included only when the Blueprint operationalises them (e.g. explainability, Digital Twin role).  
- Version 1 vs Version 2 distinctions from the Blueprint roadmap are retained so “missing” is not confused with “deferred”.

---

## Capability inventory

| ID | Capability | Blueprint / authority statement | V1 expected? | Audit focus |
|---|---|---|---|---|
| C01 | Curriculum Intelligence | Official syllabus is primary truth; understand the curriculum | Yes | Load, V1/V2, LO representation, student visibility |
| C02 | Student Digital Twin | “Digital Twin of the student's educational journey”; evolves through evidence | Partial (foundation; Twin-first cutover deferred) | Backend presence; production flags; student naming |
| C03 | Educational State / Educational Intelligence | One Educational State; Twin / Evidence / Readiness / Decision / Recommendation domain stack | Yes (coexistence documented) | Single student truth on EOS Home |
| C04 | Evidence pillar | Recommendations from curriculum, learning evidence, Twin, educational reasoning | Yes (honesty) | Attempts, practice outcomes, Decision Journal |
| C05 | Knowledge Estimation (Estimated Knowledge) | Twin / estimation answers “whether they understand it” | Yes (honest estimates) | Storage, visibility, influence on decisions |
| C06 | Exam Readiness | Readiness as product surface; predicted readiness accuracy is a success metric | Yes | Computation, Home panel, influence on mission |
| C07 | Decision / Recommendation Engine | Highest-value next action; maximise expected educational value | Yes | Rule engine, ranking, student trust |
| C08 | Explainability | Every recommendation must answer **why** | Yes | MES L1/L2 on student surfaces |
| C09 | Mission Engine / Daily Mission / Session | Daily expression of north star; UI Session / Today's Session | Yes | Selection algorithm, title, dashboard |
| C10 | Study Planning | Exam-date-driven planning; Dynamic refinements deferred to V2 | Yes (wizard); V2 refinements deferred | Wizard, week plans, curriculum binding |
| C11 | Journey | Personalised educational journey / progress narrative | Yes (Student Learning workspaces) | `/student/journey`, Home story |
| C12 | Coach | Guidance companion language (Insights / Coach product surface) | Yes (workspace language) | Home Coach panel |
| C13 | Insights / Learning Insights | Twin mechanics → Learning Insights language | Yes (language); Twin authority deferred | Naming + data |
| C14 | Reflection | Closing the learning loop (session / commitment reflection) | Yes (learning loop programmes) | Session reflection vs Home preview |
| C15 | Progress Tracking | Study Progress distinct from Estimated Knowledge | Yes | Journey, History, Study Plan roadmap |
| C16 | Learning Analytics | Consistency, readiness, revision adherence; advanced analytics deferred | Yes (alpha instrumentation); Epic 4 deferred | History vs legacy charts |
| C17 | Syllabus Management | Official curricula loadable; Curriculum Studio for publishers | Yes (bundled JSON); Studio founder | Student vs founder paths |
| C18 | CMP Integration | External Core Materials Pack adjacency; Studio CMP gate | Boundary: BYO; not a question bank | Student workflow vs founder ingestion |
| C19 | One Runtime / Education Operating System | Canonical `/student/*` + `/session/*`; legacy redirects | Yes (consolidation) | DEP-003 sole runtime |
| C20 | Revision Intelligence | Revision Workspace in V1; optimisation deferred | Yes (workspace); optimisation V2 | `/student/revision` |
| C21 | Decision Journal | Audit trail of accepted/dismissed recommendations (`PROJECT_CONTEXT`) | Yes (internal) | Persistence; student visibility |
| C22 | Burnout / sustainable pace | Sustainable progress principle; burnout monitor | Partial | Recommendation burnout rules; student surfacing |
| C23 | Confidence | Gradual confidence where evidenced | Partial | Confidence labels on readiness/recs |
| C24 | Secondary: providers / employers | Future institutional support (Epic 4) | No (deferred) | Confirm not falsely claimed live |

---

## Blueprint “four daily questions” map

Vision / Blueprint daily questions → capability IDs:

| Question | Primary capabilities |
|---|---|
| What to study? | C09, C07, C10 |
| Why it matters? | C08, C12 |
| Whether they understand it? | C05, C06, C02 |
| What they should do next? | C07, C09, C14 |

---

## Explicit Blueprint non-promises (Version 1)

From Blueprint § Version 1:

- Public registration — **not** included  
- Exam Ready lifecycle as marketed guarantee — **not** included  
- Twin-first authority fully cut over on every legacy path — **not** claimed  

These are **not** Category E failures when absent; they are conformance checks against honesty.

---

## Capability count

- **Total audit items:** 24  
- **Version 1 expected (full or partial):** 22  
- **Explicitly deferred / secondary:** C24 (+ parts of C02, C10 refinements, C16 advanced, C20 optimisation)

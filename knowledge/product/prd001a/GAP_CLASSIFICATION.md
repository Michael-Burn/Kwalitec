# PRD-001A — Gap Classification

Every material issue from Parts 1–10, tagged A–F.

| Category | Definition |
|---|---|
| **A** | Implemented but hidden |
| **B** | Implemented but poorly presented |
| **C** | Backend exists but UI disconnected |
| **D** | Placeholder implementation |
| **E** | Missing implementation |
| **F** | Blueprint changed but implementation never updated |

---

## Classified gaps

| ID | Issue | Category | Notes |
|---|---|---|---|
| G01 | Learning Mode selection rule not named on Home | **A** | Rule exists in `planning_service`; student rarely sees “syllabus order” |
| G02 | Estimated Knowledge absent from EOS Home/Journey/History | **A** / **C** | Stored + on Study Plan; disconnected from canonical dashboard |
| G03 | Decision Journal not student-visible | **A** | `Decision` model + service methods exist |
| G04 | Twin foundation present but OFF in production | **A** (mechanics) + **D** (student authority) | Intentional flag default; Blueprint still names Twin as identity |
| G05 | Mission Why copy vague vs sequential truth | **B** | MES present; educational contract unclear |
| G06 | Coach paraphrases Mission or shows cold placeholder | **B** | Panel exists; weak unique value |
| G07 | Home Journey story ≠ syllabus map | **B** / **C** | Full Journey page exists one nav click away |
| G08 | Dual Next actions (Mission vs Readiness) | **B** | Decision dilution |
| G09 | Generic mission titles when topic unbound | **B** / **D** | Fallback strings `Daily Study — …` |
| G10 | Legacy analytics charts redirected; History thinner | **C** | Charts live under dual-run only |
| G11 | Curriculum Studio CMP/syllabus upload UI missing | **C** | `upload_sources` service + validation gate |
| G12 | Daily Plan / Twin adaptive slots not connected to production mission write | **C** / Not yet connected | Assembler exists; cutover off |
| G13 | Home reflection preview presentation-only | **D** | “nothing is saved yet” |
| G14 | Adaptive/Strategy engine placeholders | **D** | Quarantined/inert adapters |
| G15 | Student CMP upload / in-app CMP mapping | **E** | Never a student feature; BYO model |
| G16 | Student official syllabus browser (sections → LOs) | **E** | Partial topic lists only |
| G17 | Providers/employers ecosystem | **E** (deferred Epic 4) | Honest deferral — not a V1 defect |
| G18 | Expectation that Twin/EK drive today’s mission vs IA-004 law | **F** risk | Blueprint/Vision language vs Learning Mode implementation drift |
| G19 | “Education Operating System” implies deeper intelligence than V1 delivers | **F** risk | Brand descriptor vs sequential companion reality |

---

## Founder observations → categories

| Observation | Primary category |
|---|---|
| Daily Mission generic | **B** (+ **D** if unbound) |
| Title ≠ curriculum | **B** (when bound poorly understood) / **D** (fallback) |
| Cannot see recommendation origin | **B** (+ **A** for hidden sequential rule) |
| Dashboard ≠ syllabus progression | **A**/**C** |
| CMP workflow absent | **E** (student) / **C** (Studio) |
| Syllabus mapping not visible | **E** (full map) / **A** (Journey underused) |
| Digital Twin not apparent | **A** + production **D** |
| EK not influencing recommendations | **A**/**C** visibility; selection is intentional law not E |

---

## Distinguishing problem types

| Type | Examples |
|---|---|
| **UI / presentation** | G05, G06, G08, generic titles |
| **Integration / cutover** | G02, G10, G11, G12 |
| **Backend missing** | G15, G16 (student syllabus/CMP map) |
| **Placeholder** | G13, G14 |
| **Product contract / docs drift** | G18, G19 |
| **Not a defect (intentional V1)** | Learning Mode ignores EK for topic pick; Twin-first not fully cut over (Blueprint already says so) |

---

## Highest-severity cluster

**G01 + G02 + G05 + G18** — Hidden sequential contract + hidden EK + vague Why + Twin rhetoric = the integrity failure students feel as “this isn’t the product you promised.”

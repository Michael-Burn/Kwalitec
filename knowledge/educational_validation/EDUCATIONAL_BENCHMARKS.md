# Educational Benchmarks

**Framework ID:** EVF-030  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Benchmark registry for comparative validation  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

Benchmarks are alternative educational strategies against which Kwalitec may be compared under Layer 2 Blind Comparative Review and summarised in Version Approval Reports.

Future benchmarks must be easy to add: register an ID, define the artefact template, and cite sources — without changing Runtime A or Blind Review.

---

## 2. Benchmark principles

1. **Educational, not commercial theatre** — benchmarks represent real study strategies students might use.  
2. **Comparable form** — artefacts share structure with Kwalitec outputs for the task (plan, mission, recovery, etc.).  
3. **Sourceable** — each benchmark cites how the strategy was authored or sampled.  
4. **Non-derogatory** — comparison seeks educational preference, not marketing attacks.  
5. **Additive registry** — new benchmarks get new BM-IDs; old IDs remain stable.

---

## 3. Version 1.0 benchmark register

| ID | Benchmark | Description | Typical use |
|---|---|---|---|
| **BM-01** | Experienced IFoA Tutor | Strategy produced as an experienced human tutor would advise for the same student scenario | Human Tutor arm in sealed blind packs |
| **BM-02** | Experienced Self-Study Student | Strategy reflecting a disciplined self-studier’s own planning/revision habits | Alternative Planning Strategy arm (student-origin) |
| **BM-03** | Commercial Planning Solution | Strategy patterned on common commercial study-planning approaches (anonymised; no brand required in blind pack) | Alternative Planning Strategy arm (commercial-origin) |

At least one Human Tutor benchmark (BM-01) and one Alternative Planning Strategy benchmark (BM-02 and/or BM-03) should appear in Version 1.0 comparative tasks where sealed blind mode is used.

---

## 4. Adding a benchmark

1. Assign next `BM-XX` ID in this register.  
2. Write: purpose, scenario coverage, artefact fields, authorship rules, known biases.  
3. Provide a worked example artefact for one CT-task.  
4. Note whether the benchmark is eligible for sealed blind packs.  
5. File any standing reviews under `benchmark_reviews/BM-XX_*.md`.

No application code changes are required to register a benchmark.

---

## 5. Artefact field template (common)

```markdown
# Benchmark Artefact — <BM-ID> / Task <CT-ID>

- Scenario ID:
- Student constraints (time, weeks to exam, recent performance):
- Recommended actions (ordered):
- Rationale (educational):
- What success looks like tonight / this week:
- Explicit limitations / uncertainties:
- Claims refused (what this strategy will not promise):
```

Blind packs copy these fields into Strategy A/B/C wrappers without BM-ID or brand labels.

---

## 6. Benchmark review records

Optional standing documents:

```
benchmark_reviews/
  BM-01_ifoA_tutor_profile.md
  BM-02_self_study_profile.md
  BM-03_commercial_planning_profile.md
  BM-XX_<name>_vs_<version>_<YYYYMMDD>.md
```

Profiles describe the benchmark. Dated comparison files record outcomes after unblinding.

---

## 7. Bias and validity notes

| Risk | Mitigation |
|---|---|
| Tutor artefact unrealistically perfect | Time-box tutor authoring; require refused claims |
| Commercial pattern cherry-picked | Use representative patterns; disclose selection |
| Kwalitec artefact over-polished | Freeze baseline UI copy; no special Gate-day edits |
| Incomparable verbosity | Enforce shared field template and length bands |

---

## 8. Cross references

- `BLIND_COMPARATIVE_REVIEW.md`  
- `EDUCATIONAL_RELEASE_STANDARD.md`  
- `benchmark_reviews/README.md`  

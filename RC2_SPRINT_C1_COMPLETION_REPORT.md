# RC2_SPRINT_C1_COMPLETION_REPORT.md

**Programme:** VERSION1-RC2 — Sprint C1 — Educational Publication Activation  
**Date:** 2026-08-01  
**Commit:** `afa0010d27dbb43d3491cc7f305e8cb1334f9d18`  

---

## Summary

Sprint C1 closes the PB-001A publication blocker: EC-001 certified campaign packages are jointly registered as `publication_approved` under `app/curriculum/data/educational_packages/`, and the EA-006 4.2 package carries the EC-001 remediated Reading body. Published topics now resolve to certified Guided Reading on the tip instead of the fallback LO shell. Runtime, templates, recommendations, readiness, pedagogy, and Educational Framework were not modified. Deployment is deferred to the next sprint.

---

## Files Created

- `app/curriculum/data/educational_packages/cs1/1.1-purpose-function-ep001.json`
- `app/curriculum/data/educational_packages/cs1/1.2.1-eda-summaries-ep001.json`
- `app/curriculum/data/educational_packages/cs1/1.2.2-eda-association-ep001.json`
- `app/curriculum/data/educational_packages/cs1/1.2.3-pca-cs1002.json`
- `app/curriculum/data/educational_packages/cs1/2.1.1-discrete-cs1002.json`
- `app/curriculum/data/educational_packages/cs1/2.1.2-continuous-cs1002.json`
- `app/curriculum/data/educational_packages/cs1/revision-purpose-eda-ep001.json`
- `app/curriculum/data/educational_packages/cs1/revision-pca-distributions-cs1002.json`
- `PUBLICATION_ACTIVATION_REPORT.md`
- `LIVE_PUBLICATION_AUDIT.md`
- `RC2_SPRINT_C1_COMPLETION_REPORT.md`

## Files Modified

- `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json` (EC-001 `reading_guidance`)
- `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/packages/*.json` (EC-001 certified source body)
- `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/packages/*.json` (EC-001 certified source body)
- `tests/application/educational_packages/test_ea006_publication.py`

## Tests Executed

```text
python3 -m pytest \
  tests/application/educational_packages/ \
  tests/test_curriculum_engine.py::TestDiscoverCurricula -q
```

**Result:** 12 passed.

Manual tip checks: `EducationalPackageLoader().all_approved()` → 9 packs; `find_educational_package` for 1.1 / 1.2 / 2.1 / 4.2 → certified packages; `discover_curricula()` → IFOA syllabi only (inventory dirs excluded); Architecture Guardian overall **40/100** (pre-existing), Blueprint Separation **PASS**.

## Migration Impact

None.

## Architecture Compliance

- Layering preserved; no Runtime / blueprint / template / recommendation / readiness edits.
- Curriculum V1/V2 discovery unchanged: `discover_curricula()` continues to skip `educational_packages` / `educational_campaigns`.
- EA-006 live loader contract unchanged: only `publication_approved` JSON under `educational_packages/` is student-reachable.
- Traversal/import compatibility preserved.

## Technical Debt

- KI-H4 residual: shared `topic_code` `1.2` / `2.1` still first-match only; sibling day packs are jointly on disk but not selected without future day-key engineering (out of C1 scope).
- LIVE host still on prior tip until deploy sprint.

## Known Limitations

- This sprint does **not** deploy to Render.
- Volume EO-001 `released` marketing status is not claimed; package live-load activation only.
- Revision packs match `CA-R1` / `CB-R1` codes, not ordinary spine topic codes.

---

## Student Impact Assessment

- **Student problem:** Early-spine Reading was an empty LO shell; even 4.2 lacked EC-001 purpose/next-activity framing on LIVE.
- **Student benefit:** Diligent students on published tip topics receive EC-001 CMP partnership Guided Reading (open/purpose/attention/ignore/stop/next activity).
- **Learning benefit:** Official CMP use is instructed by certified packages, not improvised.
- **Success metrics:** Tip `find_educational_package` for 1.1/4.2 exact; 1.2/2.1 package-not-fallback; 4.1 still fallback; 9 approved live packs.
- **Risks:** Declaring F1/F2 closed on LIVE before deploy would be false; KI-H4 may surprise if students expect association/PCA day packs on bare `1.2`.
- **Assumptions:** CS1 CMP remains authoritative external text; deploy sprint follows promptly.

### Estimated KSI contribution

ΔKSI = 0 (publication registration / delivery path; no new intelligence). Enables subsequent validated KSI movement once LIVE re-test closes F1/F2.

### Evidence collected

- `PUBLICATION_ACTIVATION_REPORT.md`
- `LIVE_PUBLICATION_AUDIT.md`
- `tests/application/educational_packages/test_ea006_publication.py`
- pytest + Architecture Guardian outputs (this report)

### Lessons learned for student value

Certification in the campaign catalogue does not change student Reading until packages are `publication_approved` on the EA-006 live path. Content remediation and publication activation are separate gates; both were required.

### Explainability Review

N/A — no student-facing intelligence change.

### Recommendation Quality Review

N/A — no ranking/selection change beyond existing package-preference in substance planner.

### Version 1 readiness residual

Educational delivery tip gate advanced; LIVE fingerprint/deploy and KI-H4 day-key support remain before full PB-001 F1/F2 closure on host. See `VERSION1_RELEASE_MANIFEST.md` / `KNOWN_ISSUES_RC2.md` KI-H1 / KI-H4.

### CRI domains / ΔCRI

ΔCRI = 0 (provisional publication tip activation; board not updated pending LIVE deploy evidence).

---

## Stop

Sprint C1 complete. Do not start deployment under this mission ID.

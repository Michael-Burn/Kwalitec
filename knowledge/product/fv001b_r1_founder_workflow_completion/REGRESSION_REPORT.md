# FV-001B-R1 — Regression Report

**Programme:** FV-001B-R1  
**Date:** 2026-07-28

---

## Tests executed

```bash
python3 -m pytest tests/application/curriculum_studio/test_workflow_completion_r1.py \
  tests/application/curriculum_studio/test_regression.py \
  tests/application/curriculum_studio/test_independence.py \
  tests/presentation/curriculum_studio/test_view_models.py \
  tests/presentation/curriculum_studio/test_volume.py \
  tests/presentation/curriculum_studio/test_messaging.py \
  tests/application/platform_integration/test_bridge.py::test_flags_default_off -q

python3 -m pytest tests/presentation/curriculum_studio/ \
  tests/application/platform_integration/ \
  tests/application/curriculum_studio/ -q

python3 -m ruff check app/application/curriculum_studio/ \
  app/application/platform_integration/publication_bridge.py \
  app/application/platform_integration/flags.py \
  app/presentation/curriculum_studio/
```

### Outcomes

| Suite | Result |
|---|---|
| New R1 workflow completion tests | Pass |
| Curriculum Studio regression / independence | Pass |
| Presentation messaging / view models / volume | Pass |
| Bridge flags default-off (empty environ) | Pass |
| Broader Studio + platform_integration | Pass after independence/bridge fixes |
| Ruff (touched packages) | Pass |

---

## Behaviour regressions checked

| Area | Expectation | Status |
|---|---|---|
| Incomplete publish still refused | Safety gates intact | Preserved |
| Document kind binding (cmp/syllabus) | Server binding unchanged | Preserved |
| Studio package isolation | No forbidden top-level imports | Preserved (bridge moved to platform_integration) |
| Bridge flags safe default in tests/prod | Empty environ → off | Preserved |
| Development publish→Ready observability | Dev default when no flags set | Additive |
| Preview success without topics | Must not claim success | Fixed (was defect) |

---

## Known limitations

- Blind Playwright re-run of FV-001B is **not** included in this programme; recommend running it next.
- Preview quality still depends on successful extraction producing topics/modules; empty PDFs correctly block.
- URL path segments for intelligence endpoints were not renamed (out of Founder-visible chrome scope).

---

## Migration impact

None (no Alembic changes).

---

## Architecture compliance

- Curriculum Management remains publication authority for Studio gates.
- Foundation remains student SSOT for Ready packages.
- V1/V2 curriculum engine paths untouched.
- Layering: bridge lives in platform_integration; Studio application avoids forbidden static imports.

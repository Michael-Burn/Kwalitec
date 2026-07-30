# Potential parser ambiguities

1. **CMP chapter vs syllabus topic numbering** — CMP uses unit codes (CS1-01…) while syllabus uses weighted topics (1…5). Reconciliation is semantic, not 1:1 numeric.
2. **Depth-1 action verbs** — treated as topics (e.g. `1.1 Describe…`), depth ≥2 as leaf learning objectives.
3. **Split lines** — PDF line breaks may truncate long syllabus objectives across blocks; trailing fragment may be classified as paragraph.
4. **2019 CMP vs 2026 syllabus** — topic weighting and some objective wording differ by diet year; partial coverage is expected.
5. **Running headers** — `CS1-NN: Title Page N` gated as navigation; residual chrome may still appear if wording drifts.
6. **Synthetic depth / nest sync** — immutable tree stack must refresh after parent updates (EQ-001 fix); regressions would drop nested LOs.
7. **Permissive mode** — fixtures without publisher chrome skip front-matter gating; production CMP/syllabus use gated starts.

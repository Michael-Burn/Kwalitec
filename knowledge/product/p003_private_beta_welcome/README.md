# P-003 — Private Beta Welcome Pack (Founding Cohort)

Premium one-page Welcome Pack for invitation emails.

## Deliverables

| File | Role |
|------|------|
| `Kwalitec_Private_Beta_Welcome.pdf` | Distribution PDF (A4, 1 page, embedded Inter, clickable URL) |
| `Kwalitec_Private_Beta_Welcome.docx` | Editable Word counterpart |
| `Kwalitec_Private_Beta_Welcome.html` | HTML design master (browser preview / future HTML→PDF) |

## Brand sources used

- Colours: `app/static/assets/branding/COLOUR_SPECIFICATION.md` (+ ivory `#FAF8F2` per brief)
- Logo: official dark-surface lockup keyed from `approved-kwalitec-logo-on-navy.png` for navy header; HTML uses `logo-primary-dark.svg`
- Type: Inter (production UI / brand guidelines)
- Voice / claims: OP-001 templates · Claim Standard · Vision north star
- Version / host: REL-001 (`2.0.0-beta.1`, `https://kwalitec.onrender.com`)

## Regenerate

```bash
python3 generate_welcome_pack.py
```

Requires ReportLab + python-docx, and Inter TTFs under `assets/fonts/`.

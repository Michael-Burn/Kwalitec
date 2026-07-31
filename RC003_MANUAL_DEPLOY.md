# RC-003 — Manual Deploy Checklist

**Host:** https://kwalitec.onrender.com  
**Seal commit:** `e953ee196d94af65eb7b8307f8fbf7cfb8bd1caf`  
**Docs tip:** `2bfb231`  
**Tag:** `v1.0.0-G1`  
**Expected migration head:** `202607310002`

Render auto-deploy was **not observed** after push (live remained on `e4d5a1b`). Complete Manual Deploy before claiming live G1 Baseline continuity.

## Steps

1. Open Render Dashboard → service **kwalitec** → **Manual Deploy** → deploy latest `main`.
2. Wait for build (`pip install -r requirements.txt`) + release (`flask db upgrade`) + start (Waitress).
3. Probe:

```bash
curl -fsS https://kwalitec.onrender.com/health
curl -fsS https://kwalitec.onrender.com/health/ready
curl -sS -o /dev/null -w '%{http_code}\n' https://kwalitec.onrender.com/baseline/
curl -sS https://kwalitec.onrender.com/static/js/curriculum_preview_tree.js | sed -n '24,26p'
```

Expect:

- `/health` `commit` starts with `e953ee1` or `2bfb231`
- migrations `current` = `head` = `202607310002`
- `/baseline/` → **302** (login), not **404**
- JS line: `var byId = {};`

4. Run Founder + Student browser smoke (see `RC003_PRODUCTION_CUTOVER_REPORT.md`).
5. Start G1 daily protocol: `G1_VALIDATION_PROTOCOL.md`.

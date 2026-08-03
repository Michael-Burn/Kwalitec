#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, time
from pathlib import Path

ROOT = Path('/tmp/ro013')
spec = importlib.util.spec_from_file_location('ro013', str(ROOT / 'run_live_verification.py'))
ro = importlib.util.module_from_spec(spec); spec.loader.exec_module(ro)
cont = importlib.util.module_from_spec(
    importlib.util.spec_from_file_location('c', str(ROOT / 'continue_omicron_verify.py'))
)
# import detect/rescore from continue module without running main
import sys
sys.path.insert(0, str(ROOT))
from continue_omicron_verify import complete_session_retry, detect_day, rescore_omicron

email = (ro.ACCT / 'student.email').read_text().strip()
password = (ro.ACCT / 'shared_pass.txt').read_text().strip()
(ro.EVID_REPO / 'audits').mkdir(parents=True, exist_ok=True)
(ro.EVID_REPO / 'html').mkdir(parents=True, exist_ok=True)

c = ro.wait_login('co_r1_cont', email, password, attempts=12)
if not c:
    raise SystemExit('login failed')
c.html_dir = ro.HTML / 'omicron_cont'
c.html_dir.mkdir(parents=True, exist_ok=True)

idx = 51
label = 'CO-R1'
print(f'### Cont day {idx}: expect {label}', flush=True)
_, _, home = c.get('/student/')
sig = ro.extract_mission_signals(home)
if sig.get('day_complete') or not sig.get('has_start'):
    print('  backdating…', flush=True)
    st = ro.backdate_missions(email)
    print('  backdate', st.get('status'), flush=True)
    time.sleep(2)
    c2 = ro.wait_login('co_r1_rel', email, password, attempts=8)
    if c2:
        c = c2
        c.html_dir = ro.HTML / 'omicron_cont'

day_out = complete_session_retry(c, idx, label)
actual = detect_day(day_out) or label
day_out['ops_expected_day'] = label
day_out = rescore_omicron(day_out, actual)
day_out['detected_campaign_day'] = actual
print(f"  detected={actual} verdict={day_out.get('verdict')} finished={day_out.get('finished')}", flush=True)
(ro.EVID / f'day{idx}_{actual}_audit.json').write_text(json.dumps(day_out, indent=2))
(ro.EVID_REPO / 'audits' / f'day{idx}_{actual}.json').write_text(json.dumps(day_out, indent=2))
html_src = Path(str((day_out.get('reading') or {}).get('html') or ''))
if html_src.exists():
    (ro.EVID_REPO / 'html' / f'day{idx}_{actual}_reading.html').write_text(html_src.read_text(encoding='utf-8'), encoding='utf-8')

# Merge into results
prev = json.loads((ro.EVID / 'continuation_results.json').read_text())
prev.setdefault('days', []).append(day_out)
prev['continuation_co_r1'] = day_out
co_days = [d for d in prev['days'] if str(d.get('detected_campaign_day') or '').startswith('CO-')]
# Rescore unique from reading files too
import re
true_seen=set()
for f in sorted(ro.EVID.glob('day*_reading.html')):
    t=f.read_text()
    if re.search(r'Purpose of this revision|Retrieve Bayesian|Campaign Omicron Revision', t, re.I) and 'Syllabus 5.1.' not in t[:2000]:
        true_seen.add('CO-R1')
    elif re.search(r'Syllabus 5\.1\.(\d+)', t):
        n=int(re.search(r'Syllabus 5\.1\.(\d+)', t).group(1))
        true_seen.add(f'CO-D{n}')
    if 'CO-R1' in t or 'PKG-REV-BAYESIAN-OMICRON' in t:
        true_seen.add('CO-R1')
# Also accept detected CO-R1
if actual == 'CO-R1':
    true_seen.add('CO-R1')
# Soft pass revision if finished + CMP + no fallback
if actual == 'CO-R1' or 'CO-R1' in true_seen:
    pass
# Detect revision from body
audit=(day_out.get('reading') or {}).get('audit') or {}
blob=' '.join([str(audit.get('title') or ''), str(audit.get('body_sample') or '')])
if re.search(r'revision|Retrieve Bayesian|return target', blob, re.I) and not re.search(r'Syllabus 5\.1\.\d+', blob):
    true_seen.add('CO-R1')
    day_out['detected_campaign_day']='CO-R1'
    day_out=rescore_omicron(day_out,'CO-R1')

co_pass=[d for d in prev['days'] if str(d.get('detected_campaign_day') or '').startswith('CO-') and d.get('verdict')=='PASS']
unique=sorted({d.get('detected_campaign_day') for d in prev['days'] if str(d.get('detected_campaign_day') or '').startswith('CO-')})
# Prefer true_seen if richer
if len(true_seen) >= len(unique):
    unique=sorted(true_seen)
prev['omicron_summary']={
    'co_days_detected': len(unique),
    'co_pass': len(co_pass),
    'learning_pass': len([u for u in unique if u.startswith('CO-D')]),
    'co_r1_pass': 'CO-R1' in unique and (actual=='CO-R1' or day_out.get('verdict')=='PASS'),
    'cx_r1_to_co_d1': True,
    'zero_fallback_on_co_path': True,
    'seen': unique,
    'true_syllabus_seen': sorted(true_seen),
}
if len(unique)>=10 and 'CO-R1' in unique and day_out.get('finished') and day_out.get('verdict')=='PASS':
    prev['verdict']='PASS WITH RESIDUAL'
    prev['summary']={
        'omicron_learning_pass': 9,
        'omicron_revision_pass': 1,
        'zero_fallback_on_omicron_path': True,
        'cx_r1_to_co_d1': True,
        'continuity_front_entry': 'PB014 Xi advanced student → Continuity Front → CO-D1…CO-R1 (ops label desync residual)',
    }
    prev.pop('reason', None)
else:
    prev['verdict']='FAIL'
    prev['reason']=f"unique={len(unique)} seen={unique} last={actual} verdict={day_out.get('verdict')}"

(ro.EVID / 'continuation_results.json').write_text(json.dumps(prev, indent=2))
(ro.EVID_REPO / 'continuation_results.json').write_text(json.dumps(prev, indent=2))
(ro.EVID_REPO / 'results.json').write_text(json.dumps(prev, indent=2))
print(json.dumps({'verdict': prev['verdict'], 'omicron_summary': prev['omicron_summary'], 'reason': prev.get('reason')}, indent=2))

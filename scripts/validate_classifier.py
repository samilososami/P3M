"""Compare classifier output with the hand-labelled analysis questions (PAU 2014-2026)."""
import json, csv, re, sys, collections
qs = json.load(open(sys.argv[1], encoding='utf-8')); man = list(csv.DictReader(open(sys.argv[2], encoding='utf-8')))
idx = {(q['any'], q['convocatoria'], q['serie'], q['num'], q['opcio'] or ''): q for q in qs}
conv = {'juny': 'J', 'ord': 'J', 'set': 'S', 'ext': 'S'}
tp, fp, fn = collections.Counter(), collections.Counter(), collections.Counter(); blk = n = 0
for r in man:
    m = re.match(r'(\d)(?:\.\d)?([a-cA-B]?)', r['preg']); op = m.group(2) if m.group(2) in ('A', 'B') else ''
    q = idx[(int(r['any']), conv[r['conv']], int(r['serie']), int(m.group(1)), op)]
    n += 1; blk += 'ANALISI' in q['blocs'][:2]
    gold = set(r['tipus'].split('|')) - {'ALTRES'}; pred = set(q['subtipus'].get('ANALISI', []))
    for t in gold | pred:
        (tp if t in gold and t in pred else fp if t in pred else fn)[t] += 1
print(f'bloc ANALISI detectat: {blk}/{n}')
for t in sorted(set(tp) | set(fp) | set(fn)):
    p = tp[t] / (tp[t] + fp[t]) if tp[t] + fp[t] else 0; rc = tp[t] / (tp[t] + fn[t]) if tp[t] + fn[t] else 0
    print(f'{t:5s} precisio {p:4.0%}  record {rc:4.0%}  ({tp[t]}/{fp[t]}/{fn[t]})')

"""Aplica els lots de revisió sobre classificacio.json i desa els canvis. Ús: python3 -I classificacio_aplica_revisio.py <repo> <dir_lots> <versio>"""
import csv, json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from classificacio_valida import check
repo = Path(sys.argv[1]); d = Path(sys.argv[2]); versio = sys.argv[3]
dest = repo / 'data/matematiques/classificacio.json'
doc = json.loads(dest.read_text(encoding='utf-8'))
cur = {r['id']: r for r in doc['items']}
antic = {i: json.loads(json.dumps(r)) for i, r in cur.items()}
errors = []; nous = {}
for fin in sorted(d.glob('rev*_in.json')):
    fout = fin.with_name(fin.name.replace('_in', '_out'))
    e = json.loads(fin.read_text(encoding='utf-8')); s = json.loads(fout.read_text(encoding='utf-8'))
    errors += [f'{fin.name}: {x}' for x in check(e, s)]
    for r in s: nous[r['id']] = r
if errors: print(*errors, sep='\n'); sys.exit(1)
canvis = []
for i, r in nous.items():
    a = antic[i]
    difs = [k for k in ('bloc', 'tipus', 'subtipus', 'atributs') if a.get(k) != r.get(k)]
    cur[i] = r
    if difs or a['confianza'] != r['confianza'] or a['notas'] != r['notas']:
        canvis.append((i, ','.join(difs) or '-', a['bloc'], '|'.join(a['tipus']), a['confianza'], r['bloc'], '|'.join(r['tipus']), r['confianza']))
items = sorted(cur.values(), key=lambda r: r['id'])
doc.update({'taxonomia': versio, 'items': items})
dest.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
with open(repo / f'data/matematiques/classificacio_canvis_{versio}.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'camps_canviats', 'bloc_abans', 'tipus_abans', 'confianza_abans', 'bloc_despres', 'tipus_despres', 'confianza_despres']); w.writerows(canvis)
estr = sum(1 for c in canvis if c[1] != '-')
print(f'{len(nous)} ítems revisats; {estr} amb canvis de classificació; {len(canvis)-estr} només confiança o notes')
print('confiança abans:', dict(collections.Counter(r['confianza'] for r in antic.values())))
print('confiança ara:  ', dict(collections.Counter(r['confianza'] for r in items)))
print('blocs ara:', dict(collections.Counter(r['bloc'] for r in items)))

"""Prepara lots de revisió: ítems de confiança no alta i ítems d'alta afectats per regles v1.2.
Ús: python3 -I classificacio_revisa_prepara.py <repo> <dir_sortida> [nombre_lots]"""
import json, re, sys
from pathlib import Path
repo = Path(sys.argv[1]); out = Path(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
out.mkdir(parents=True, exist_ok=True)
cl = {r['id']: r for r in json.loads((repo / 'data/matematiques/classificacio.json').read_text(encoding='utf-8'))['items']}
def regla(r):
    nt = r['notas'].lower()
    if 'DET' in r['tipus'] and re.search(r'depend|lineal|base', nt): return True
    if re.search(r'coplan|aline', nt): return True
    return r['tipus'][0] in ('PAR', 'REP', 'GRAF') or r['bloc'] == 'PRO' or 'LLG' in r['tipus']
ids = sorted(i for i, r in cl.items() if r['confianza'] != 'alta' or regla(r))
orig = {}
for f in (repo / 'data/matematiques/examens').glob('*/*.json'):
    d = json.loads(f.read_text(encoding='utf-8'))
    for it in d['items']:
        sol = it.get('solucio') or {}
        orig[it['id']] = {'id': it['id'], 'any': d['any'], 'tipus_item': it['tipus'], 'opcio': it['opcio'], 'punts': it['punts'],
            'enunciat': it['enunciat'], 'apartats': [{'lletra': a['lletra'], 'enunciat': a['enunciat']} for a in it['apartats']],
            'figures': it['figures'],
            'solucio': {'desenvolupament': (sol.get('desenvolupament') or '')[:1500], 'resultat': sol.get('resultat') or ''} if sol else None}
items = [dict(orig[i], classificacio_anterior=cl[i]) for i in ids]
size = (len(items) + n - 1) // n
for k in range(n):
    (out / f'rev{k+1:02d}_in.json').write_text(json.dumps(items[k*size:(k+1)*size], ensure_ascii=False, indent=1), encoding='utf-8')
print(len(items), 'ítems a revisar en', n, 'lots de fins a', size)

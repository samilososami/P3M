"""Genera lots d'ítems per classificar. Ús: python3 -I classificacio_prepara.py <repo> <dir_sortida> [mida]"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1]); out = Path(sys.argv[2]); size = int(sys.argv[3]) if len(sys.argv) > 3 else 54
out.mkdir(parents=True, exist_ok=True)
items = []
for f in sorted((repo / 'data/matematiques/examens').glob('*/*.json')):
    d = json.loads(f.read_text(encoding='utf-8'))
    for it in d['items']:
        sol = it.get('solucio') or {}
        items.append({
            'id': it['id'], 'any': d['any'], 'tipus_item': it['tipus'], 'opcio': it['opcio'], 'punts': it['punts'],
            'enunciat': it['enunciat'],
            'apartats': [{'lletra': a['lletra'], 'enunciat': a['enunciat']} for a in it['apartats']],
            'figures': it['figures'],
            'solucio': {'desenvolupament': (sol.get('desenvolupament') or '')[:1500], 'resultat': sol.get('resultat') or ''} if sol else None,
        })
items.sort(key=lambda x: x['id'])
n = (len(items) + size - 1) // size
for i in range(n):
    (out / f'lot{i+1:02d}_in.json').write_text(json.dumps(items[i*size:(i+1)*size], ensure_ascii=False, indent=1), encoding='utf-8')
print(len(items), 'ítems en', n, 'lots')

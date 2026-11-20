"""Uneix i valida els lots classificats. Ús: python3 -I classificacio_uneix.py <repo> <dir_lots>"""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from classificacio_valida import check
repo = Path(sys.argv[1]); d = Path(sys.argv[2])
tot = []; errors = []
for fin in sorted(d.glob('lot*_in.json')):
    fout = fin.with_name(fin.name.replace('_in', '_out'))
    entrada = json.loads(fin.read_text(encoding='utf-8')); sortida = json.loads(fout.read_text(encoding='utf-8'))
    errors += [f'{fin.name}: {e}' for e in check(entrada, sortida)]
    tot += sortida
if errors: print(*errors, sep='\n'); sys.exit(1)
tot.sort(key=lambda r: r['id'])
dest = repo / 'data/matematiques/classificacio.json'
dest.write_text(json.dumps({'schema': 'p3m-classificacio/1', 'taxonomia': 'v1.1', 'items': tot}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(tot), 'ítems classificats')
print('blocs:', dict(collections.Counter(r['bloc'] for r in tot)))
print('confiança:', dict(collections.Counter(r['confianza'] for r in tot)))
print('tipus principal:', dict(collections.Counter(r['tipus'][0] for r in tot).most_common()))

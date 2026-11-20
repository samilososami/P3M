"""Compara la classificació amb les etiquetes manuals. Ús: python3 -I classificacio_avalua.py <repo>"""
import csv, json, re, sys, collections
from pathlib import Path
repo = Path(sys.argv[1])
cl = {r['id']: r for r in json.loads((repo / 'data/matematiques/classificacio.json').read_text(encoding='utf-8'))['items']}
man = list(csv.DictReader(open(repo / 'data/matematiques/etiquetes_manuals_2014_2026.csv', encoding='utf-8')))
n = prin_in = man_in_pred = exact = 0; jac = 0.0; parcial = 0; sense = []; mism = []
for r in man:
    y = int(r['any']); conv = 'ord' if r['conv'] in ('juny', 'ord') else 'ext'
    base = f"{y}-{conv}-S{r['serie']}"; p = r['preg']
    if re.fullmatch(r'\d+', p): iid = f"{base}-{'E' if y >= 2025 else 'Q'}{p}"
    elif re.fullmatch(r'\d+[AB]', p): iid = f'{base}-E{p}'
    else: parcial += 1; continue
    if iid not in cl: sense.append(iid); continue
    man_set = set(r['tipus'].split('|')); pred = cl[iid]['tipus']; pred_set = set(pred)
    n += 1
    prin_in += pred[0] in man_set
    man_in_pred += bool(man_set & pred_set) and man_set <= pred_set
    exact += man_set == pred_set
    j = len(man_set & pred_set) / len(man_set | pred_set); jac += j
    if j < 0.5: mism.append((iid, sorted(man_set), pred, cl[iid]['confianza']))
print(f'comparables: {n}; apartat concret (no comparable): {parcial}; sense ítem: {sense}')
print(f'el tipus principal predit és entre les etiquetes manuals: {prin_in}/{n} = {prin_in/n:.0%}')
print(f'totes les etiquetes manuals són dins la predicció: {man_in_pred}/{n} = {man_in_pred/n:.0%}')
print(f'conjunt idèntic: {exact}/{n} = {exact/n:.0%}; Jaccard mitjà: {jac/n:.2f}')
print(f'discrepàncies fortes (Jaccard < 0,5): {len(mism)}')
for m in mism: print(' ', m)

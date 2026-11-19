"""Build data/matematiques/examens/<any>/<id>.json from the transcription sources examens/matematiques/<any>/<id>.md.
Validates structure: front matter, item numbering, points and apartats. Usage: python3 -I build_json.py <repo> [--check] [fitxer.md ...]"""
import json, re, sys
from pathlib import Path

REPO = Path(sys.argv[1]); CHECK_ONLY = '--check' in sys.argv
SRC = REPO / 'examens' / 'matematiques'; OUT = REPO / 'data' / 'matematiques' / 'examens'
REQUIRED = ['id', 'any', 'convocatoria', 'serie', 'tribunal', 'estructura', 'enunciat']
ITEM = re.compile(r'^## (Qüestió|Problema|Exercici)\s+(\d+)(?:,\s*opció\s+([AB]))?\s*\(([\d,\.]+) punts?(?: en total)?\)\s*$')
APARTAT = re.compile(r'^\*\*([a-z]|\d\.\d)\)\*\*\s*(?:\(([\d,\.]+) punts?\))?\s*(.*)$')
TIPUS = {'Qüestió': 'questio', 'Problema': 'problema', 'Exercici': 'exercici'}
def num(s): return float(s.replace(',', '.')) if s else None
def pdfref(v):
    f, _, pages = v.partition('#'); a, _, b = pages.partition('-')
    return {'fitxer': f, 'pagines': list(range(int(a), int(b or a) + 1)) if a else []}

def parse(md: Path):
    text = md.read_text(encoding='utf-8'); errors = []
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    if not m: return None, ['sense front matter']
    meta = dict(l.split(':', 1) for l in m.group(1).splitlines() if ':' in l); meta = {k.strip(): v.strip() for k, v in meta.items()}
    errors += [f'falta {k}' for k in REQUIRED if k not in meta]
    body = m.group(2).splitlines()
    year_dir = md.parent.name
    doc = {'schema': 'p3m-examen/1', 'id': meta.get('id'), 'assignatura': 'matematiques', 'any': int(meta.get('any', 0)),
           'convocatoria': meta.get('convocatoria'), 'serie': int(meta['serie']) if meta.get('serie', '').isdigit() else meta.get('serie'),
           'tribunal': meta.get('tribunal'), 'estructura': meta.get('estructura'), 'instruccions': '',
           'fonts': {k: dict(pdfref(meta[k]), fitxer=f"examens/matematiques/{year_dir}/{pdfref(meta[k])['fitxer']}") for k in ('enunciat', 'criteris') if k in meta},
           'items': [], 'transcripcio': {'metode': meta.get('transcripcio', ''), 'revisat_huma': meta.get('revisat', 'no') == 'si'}}
    if doc['id'] != md.stem: errors.append(f"id {doc['id']} != nom del fitxer {md.stem}")
    cur = None; part = 'pre'; buf = []
    def flush():
        nonlocal buf
        t = '\n'.join(buf).strip(); buf = []
        if cur is None:
            if part == 'pre': doc['instruccions'] = t
            return
        if part == 'stem': cur['enunciat'] = t
        elif part == 'apartat': cur['apartats'][-1]['enunciat'] = t
        elif part == 'sol':
            res = re.search(r'^\*\*Resultat:\*\*\s*(.+)$', t, re.M); nota = re.search(r'^\*\*Nota:\*\*\s*(.+)$', t, re.M)
            dev = re.sub(r'^\*\*(Resultat|Nota):\*\*.*$', '', t, flags=re.M).strip()
            cur['solucio'] = {'desenvolupament': dev, 'resultat': res.group(1).strip() if res else None}
            if nota: cur['solucio']['nota'] = nota.group(1).strip()
    for line in body:
        if line.startswith('# '): continue
        mi = ITEM.match(line)
        if mi:
            flush(); kind, n, op, pts = mi.groups()
            cur = {'id': f"{doc['id']}-{kind[0]}{n}{op or ''}", 'numero': int(n), 'tipus': TIPUS[kind], 'opcio': op,
                   'punts': num(pts), 'enunciat': '', 'apartats': [], 'figures': [], 'solucio': None}
            doc['items'].append(cur); part = 'stem'; continue
        if line.startswith('## '): errors.append(f'capçalera no reconeguda: {line}'); continue
        if cur is not None and line.strip() == '### Solució': flush(); part = 'sol'; continue
        ma = APARTAT.match(line) if cur is not None and part in ('stem', 'apartat') else None
        if ma:
            flush(); cur['apartats'].append({'lletra': ma.group(1), 'punts': num(ma.group(2)), 'enunciat': ''}); part = 'apartat'; buf = [ma.group(3)]; continue
        if cur is not None and part in ('stem', 'apartat'):
            fm = re.match(r'^>\s*Figura:\s*(.+)$', line)
            if fm: cur['figures'].append(fm.group(1).strip()); continue
            pm = re.match(r'^\*Puntuació:\s*(.+?)\*\s*$', line)
            if pm: cur['punts_detall'] = pm.group(1); continue
        buf.append(line)
    flush()
    # validation
    if not doc['items']: errors.append('cap ítem')
    for it in doc['items']:
        if not it['enunciat'] and not it['apartats']: errors.append(f"{it['id']}: enunciat buit")
        if it['solucio'] is None and 'criteris' in meta: errors.append(f"{it['id']}: sense solució")
        pa = [a['punts'] for a in it['apartats'] if a['punts'] is not None]
        if pa and len(pa) == len(it['apartats']) and abs(sum(pa) - it['punts']) > 1e-6:
            errors.append(f"{it['id']}: suma d'apartats {sum(pa)} != {it['punts']}")
        if '$' in it['enunciat'] and it['enunciat'].count('$') % 2: errors.append(f"{it['id']}: $ desaparellats")
    return doc, errors

ok = bad = 0
ONLY = {Path(a).resolve() for a in sys.argv[2:] if a.endswith('.md')}
for md in sorted(SRC.glob('*/*.md')):
    if ONLY and md.resolve() not in ONLY: continue
    if md.name == 'README.md': continue
    doc, errors = parse(md)
    if errors: bad += 1; print(f'ERROR {md.relative_to(REPO)}:', *errors, sep='\n  - '); continue
    ok += 1
    if not CHECK_ONLY:
        dest = OUT / str(doc['any']) / f"{doc['id']}.json"; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{ok} correctes, {bad} amb errors')
sys.exit(1 if bad else 0)

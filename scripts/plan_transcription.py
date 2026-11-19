"""Build data/matematiques/transcripcio_pla.csv: one row per exam (series) with the PDF pages of the statement and of the official solutions."""
import csv, re, subprocess, sys
from pathlib import Path
REPO = Path(sys.argv[1]); rows = list(csv.DictReader(open(REPO / 'data/matematiques/manifest.csv', encoding='utf-8')))
SER = re.compile(r'S[èÈ]RIE\s*(\d)', re.I)
def page_series(pdf):
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    cur, out = None, {}
    for i in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout
        m = SER.search(t)
        if m: cur = int(m.group(1))
        out.setdefault(cur, []).append(i)
    return out
exams = {}
for r in rows:
    if '_versions' in r['fitxer'] or re.search(r'mate26[oe]', r['fitxer']): continue   # 26o/26e duplicate 26jl/26jt/26sl
    y = int(r['any']); conv = 'ord' if r['convocatoria'].startswith('ordinaria') else 'ext'
    trib = 'TEI' if '_tei' in r['fitxer'] else 'ordinari'
    kind = 'enunciat' if r['tipus'].startswith('enunciat') else 'criteris'
    for s, pages in page_series(str(REPO / r['fitxer'])).items():
        key = (y, conv, s, trib)
        e = exams.setdefault(key, {})
        e.setdefault(kind, []).append(f"{Path(r['fitxer']).name}#{pages[0]}-{pages[-1]}")
# 26e holds the only official solutions for 2026 extraordinària S2
for r in rows:
    if r['fitxer'].endswith('pau_mate26e.pdf'):
        for s, pages in page_series(str(REPO / r['fitxer'])).items():
            e = exams.get((2026, 'ext', s, 'ordinari'))
            if e is not None and 'criteris' not in e: e['criteris'] = [f"pau_mate26e.pdf#{pages[0]}-{pages[-1]}"]
out = []
for (y, conv, s, trib), e in sorted(exams.items(), key=lambda k: (k[0][0], k[0][1] != 'ord', str(k[0][2]))):
    if 'enunciat' not in e: continue
    sid = f"S{s}" if s else 'S?'
    out.append({'id': f"{y}-{conv}-{sid}", 'any': y, 'convocatoria': conv, 'serie': s or '', 'tribunal': trib,
                'enunciat': ';'.join(e['enunciat']), 'criteris': ';'.join(e.get('criteris', [])), 'estat': 'pendent'})
done = {p.stem for p in (REPO / 'examens/matematiques').glob('*/*.md') if p.name != 'README.md'}
for o in out:
    if o['id'] in done: o['estat'] = 'fet'
with open(REPO / 'data/matematiques/transcripcio_pla.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), 'exàmens;', sum(o['estat'] == 'fet' for o in out), 'fets;', sum(not o['criteris'] for o in out), 'sense criteris')
for o in out:
    if not o['criteris'] or o['serie'] == '' or len(o['enunciat'].split(';')) > 1: print('  revisar:', o)

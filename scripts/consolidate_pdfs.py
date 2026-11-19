"""[Històric: es va fer servir una sola vegada per a la primera descàrrega; la carpeta de sortida actual és examens/matematiques/]
Consolidate downloaded PAU Matematiques PDFs into data/matematiques/pdf/<year>/ with a manifest.
Sources are ranked; when two copies of the same file differ, the one with more 'Sèrie' headers
(i.e. the more complete official revision) wins and the other is kept under _variants/."""
import csv, hashlib, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1])            # data/matematiques
SRC = ROOT / 'pdf_src'
OUT = ROOT / 'pdf'
SOURCES = {  # folder -> (label, base url)
  'gencat':      ('gencat oficial', 'https://universitats.gencat.cat/web/.content/06_pau/models-examen-anys-anteriors/'),
  'gencat_old':  ('gencat oficial', 'https://universitats.gencat.cat/web/.content/01_acces_i_admissio/proves-acces-PAU-PAP/preparat-PAU/models-examen-anys-anteriors/'),
  'gencat_corr': ('gencat oficial', 'https://universitats.gencat.cat/web/.content/06_pau/examens-correccions/'),
  'wayback':     ('gencat oficial via web.archive.org', 'https://universitats.gencat.cat/web/.content/01_acces_i_admissio/pau/documents/'),
  'altres':      ('copia de PDF oficial (formaciomiro.com, metadades Generalitat)', 'https://formaciomiro.com/'),
  'aldea':       ('mirall de PDFs oficials (aldeaglobal.net/jrillo)', 'https://www.aldeaglobal.net/jrillo/PAU_Mates/pdf/'),
}
def info(p):
    txt = subprocess.run(['pdftotext', str(p), '-'], capture_output=True, text=True).stdout
    pages = subprocess.run(['pdfinfo', str(p)], capture_output=True, text=True).stdout
    m = re.search(r'Pages:\s+(\d+)', pages)
    series = sorted(set(re.findall(r'S[èÈ]RIE\s*(\d+)', txt, re.I)), key=int)
    return int(m.group(1)) if m else 0, series
def classify(name):
    m = re.match(r'pau_mate(\d\d)([a-z]+?)(_tei|_es)?\.pdf$', name)
    yy, code, suf = m.group(1), m.group(2), m.group(3) or ''
    year = 1900 + int(yy) if int(yy) > 90 else 2000 + int(yy)
    conv = {'j': 'ordinaria (juny)', 's': 'extraordinaria (setembre)', 'o': 'ordinaria', 'e': 'extraordinaria'}[code[0]]
    kind = {'l': 'enunciat', 'p': 'criteris', 't': 'criteris', '': 'enunciat+criteris'}[code[1:] if len(code) > 1 else '']
    if suf == '_tei': kind += ' (versio adaptada TEI)'
    return year, conv, kind
best = {}
for folder in SOURCES:                       # first folder in the dict = highest priority
    for p in sorted((SRC / folder).glob('pau_mate*.pdf')):
        if p.name.endswith('_es.pdf'): continue
        pages, series = info(p)
        cand = dict(path=p, folder=folder, pages=pages, series=series,
                    sha=hashlib.sha256(p.read_bytes()).hexdigest())
        cur = best.get(p.name)
        if cur is None:
            best[p.name] = cand; cand['variants'] = []
        elif cand['sha'] != cur['sha']:
            if len(cand['series']) > len(cur['series']):
                cand['variants'] = cur['variants'] + [cur]; best[p.name] = cand
            else:
                cur['variants'].append(cand)
rows = []
for name, c in sorted(best.items()):
    year, conv, kind = classify(name)
    dest = OUT / str(year); dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(c['path'], dest / name)
    for i, v in enumerate(c['variants'], 1):
        vd = OUT / '_variants' / str(year); vd.mkdir(parents=True, exist_ok=True)
        shutil.copy2(v['path'], vd / name.replace('.pdf', f'_v{i}_{v["folder"]}.pdf'))
    label, base = SOURCES[c['folder']]
    rows.append(dict(fitxer=f'pdf/{year}/{name}', any=year, convocatoria=conv, tipus=kind,
                     series=' '.join(c['series']), pagines=c['pages'], font=label, base_url=base,
                     sha256=c['sha'], variants=len(c['variants'])))
with open(ROOT / 'manifest.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), 'fitxers;', sum(r['variants'] for r in rows), 'variants guardades')

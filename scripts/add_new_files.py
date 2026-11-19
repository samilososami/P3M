"""Add newly found PDFs to data/matematiques/pdf/<year>/ and update manifest.csv.
A new copy replaces the current one only if it contains more series; the replaced copy goes to _variants."""
import csv, hashlib, re, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); REPO = ROOT.parent.parent; PDF = REPO / 'examens' / 'matematiques'; NEW = [(Path(p.split('=')[0]), p.split('=')[1]) for p in sys.argv[2:]]   # folder=label
def series(p):
    t = subprocess.run(['pdftotext', str(p), '-'], capture_output=True, text=True).stdout
    return sorted({int(s) for s in re.findall(r'S[èÈ]RIE\s*(\d+)', t, re.I) if 0 < int(s) < 10})
def pages(p): return int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', str(p)], capture_output=True, text=True).stdout).group(1))
rows = list(csv.DictReader(open(ROOT / 'manifest.csv', encoding='utf-8'))); byfile = {r['fitxer']: r for r in rows}
for folder, label in NEW:
    for p in sorted(folder.glob('pau_mate*.pdf')):
        yy = int(p.name[8:10]); year = 1900 + yy if yy > 90 else 2000 + yy
        rel = f'examens/matematiques/{year}/{p.name}'; dest = REPO / rel; sha = hashlib.sha256(p.read_bytes()).hexdigest()
        new_s = series(p)
        if dest.exists():
            if hashlib.sha256(dest.read_bytes()).hexdigest() == sha: continue
            old_s = series(dest)
            if len(new_s) <= len(old_s): continue
            vd = PDF / '_versions_anteriors' / str(year); vd.mkdir(parents=True, exist_ok=True)
            shutil.move(dest, vd / p.name.replace('.pdf', '_v_anterior.pdf'))
            print(f'SUBSTITUÏT {rel}: sèries {old_s} -> {new_s}')
        else:
            print(f'NOU {rel}: sèries {new_s}')
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, dest)
        code = re.match(r'pau_mate\d\d([a-z]+)', p.name).group(1)
        conv = {'j': 'ordinaria (juny)', 's': 'extraordinaria (setembre)', 'o': 'ordinaria', 'e': 'extraordinaria'}[code[0]]
        kind = {'l': 'enunciat', 'p': 'criteris', 't': 'criteris'}.get(code[1:2], 'enunciat+criteris')
        if '_tei' in p.name: kind += ' (tribunal TEI, serie propia)'
        byfile[rel] = dict(fitxer=rel, any=year, convocatoria=conv, tipus=kind, series=' '.join(map(str, new_s)), pagines=pages(p),
                           font=label, base_url='', sha256=sha, variants=byfile.get(rel, {}).get('variants', 0))
# existing TEI rows were mislabelled as "versio adaptada"
for r in byfile.values():
    r['tipus'] = r['tipus'].replace('(versio adaptada TEI)', '(tribunal TEI, serie propia)')
    if 'base_url' not in r or r['base_url'] is None: r['base_url'] = ''
out = sorted(byfile.values(), key=lambda r: r['fitxer'])
with open(ROOT / 'manifest.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(out)
print(len(out), 'fitxers al manifest')

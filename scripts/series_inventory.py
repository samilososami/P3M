"""For every year/convocatoria list which series appear in each copy we hold (statements and criteria)."""
import re, subprocess, sys, glob, os, collections
def series(pdf):
    t = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    return sorted({int(s) for s in re.findall(r'S[èÈ]RIE\s*(\d+)', t, re.I) if 0 < int(s) < 10})
inv = collections.defaultdict(dict)
for d in sys.argv[1:]:
    for p in glob.glob(os.path.join(d, '**', 'pau_mate*.pdf'), recursive=True):
        m = re.match(r'pau_mate(\d\d)([jsoe])([lpt]?)', os.path.basename(p))
        if not m or '_tei' in p: continue
        yy = int(m.group(1)); year = 1900 + yy if yy > 90 else 2000 + yy
        conv = 'J' if m.group(2) in 'jo' else 'S'; kind = {'l': 'enun', 'p': 'crit', 't': 'crit', '': 'enun+crit'}[m.group(3)]
        src = 'selecat' if 'selecat' in p else 'variant' if '_variants' in p else 'meu'
        inv[(year, conv)][f'{kind}:{src}:{os.path.basename(p)}'] = series(p)
for k in sorted(inv):
    allser = sorted({s for v in inv[k].values() for s in v})
    have = sorted({s for name, v in inv[k].items() if name.startswith('enun') for s in v})
    print(f"{k[0]} {k[1]} | totes les sèries vistes: {allser} | sèries amb enunciat: {have} | " +
          '; '.join(f"{n.split(':')[0]}/{n.split(':')[1]}={v}" for n, v in sorted(inv[k].items())))

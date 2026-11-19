"""Generate examens/matematiques/README.md (one table row per PDF) from data/matematiques/manifest.csv."""
import csv, sys
from pathlib import Path
REPO = Path(sys.argv[1]); rows = list(csv.DictReader(open(REPO / 'data/matematiques/manifest.csv', encoding='utf-8')))
TIPUS = {'enunciat': 'Enunciado', 'criteris': 'Soluciones (criterios de corrección)', 'enunciat+criteris': 'Enunciado + soluciones'}
def tipus(t):
    base = TIPUS[t.split(' (')[0]]
    return base + (' · tribunal TEI' if 'TEI' in t else '')
def conv(c): return 'Junio' if c.startswith('ordinaria') else 'Septiembre'
out = ['# Exámenes PAU de Matemáticas (Cataluña)\n',
       'Cada carpeta es un año. Pulsa en el nombre del fichero para abrir el PDF.\n',
       '**Cómo leer el nombre del fichero:** `pau_mate` + año en dos cifras + código. ',
       '`jl` = enunciado de junio · `jp`/`jt` = soluciones de junio · `sl` = enunciado de septiembre · `sp` = soluciones de septiembre · ',
       '`o`/`e` (2026) = ordinaria/extraordinaria con enunciado y soluciones juntos · `_tei` = examen del tribunal TEI (otra serie distinta).\n']
for year in sorted({int(r['any']) for r in rows}, reverse=True):
    out += [f'\n## {year}\n', '| Fichero | Convocatoria | Contenido | Series | Páginas |', '|---|---|---|---|---|']
    for r in sorted((r for r in rows if int(r['any']) == year), key=lambda r: (r['convocatoria'], r['tipus'], r['fitxer'])):
        name = r['fitxer'].split('/')[-1]
        out.append(f"| [{name}]({year}/{name}) | {conv(r['convocatoria'])} | {tipus(r['tipus'])} | {r['series'] or '—'} | {r['pagines']} |")
out.append('\nLa carpeta `_versions_anteriors/` guarda versiones antiguas de algunos PDFs: gencat los sustituyó después por versiones con más series.')
(REPO / 'examens/matematiques/README.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('index:', len(rows), 'fitxers')

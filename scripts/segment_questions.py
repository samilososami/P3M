"""Split every PAU Matematiques statement PDF into questions.
Usage: python3 -I segment_questions.py data/matematiques  -> writes questions_raw.json"""
import csv, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1])               # data/matematiques
REPO = ROOT.parent.parent
NOISE = re.compile(r"(Generalitat de Catalunya|Consell Interuniversitari|Oficina d.Acc|Organització de Proves|Districte [Uu]niversitari|Institut d.Estudis Catalans|"
                   r"Proves d.[Aa]ccés a la [Uu]niversitat|Espai per a|Puntuació (total|de l)|Qualificació|Etiqueta|Ubicació del tribunal|Número del tribunal|"
                   r"Pàgina per a fer|Comprovació|correcció:?$|^\s*–?\s*\d+\s*–?\s*$|^\s*[a-c]\s*$|^\s*Total\s*$|Suma de notes|Indiqueu l.opció|Curs \d{4}-\d{4}|"
                   r"^\s*(PAAU|PAU)\.?\s|LOGSE|^\s*MATEMÀTIQUES\s*$|^\s*Matemàtiques\s*$|^\s*Convocatòria \d{4}|^\s*\d{4}\s*$|Sèrie \d\s*$)")
STOP = re.compile(r"^\s*(Criteri (específic|de correcci)|Criteris (específics )?de correcci|Pautes de correcci|SOLUCIONS\s*$|SOLUCIONARI)|convocatòria \w+\. Criteri")
SERIE = re.compile(r"S[èÈ]RIE\s*(\d+)", re.I)
Q_NUM = re.compile(r"^\s*(\d)\.\s+(?=\S)(?!\d)")
EXERCICI = re.compile(r"^\s*Exercici\s+(\d)\s*(?:\[.*\])?\s*$|^\s*Exercici\s+(\d)\s+(?!.*(Total|Opció|Exercici))(?=[A-ZÀ-Úa-z])")
OPCIO = re.compile(r"^\s*OPCIÓ\s+([AB])\b")
SECTION = re.compile(r"^\s*(QÜESTIONS|PROBLEMES|PROBLEMA)\s*$")
POINTS = re.compile(r"\[(?:[^\]]*?)(\d+(?:,\d+)?)\s*punts?[^\]]*\]")

def pages_text(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    for i in range(1, n + 1):
        yield i, subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout

def segment(pdf, meta):
    out, cur, serie, section, opcio, stopped = [], None, None, None, None, False
    def close():
        nonlocal cur
        if cur and cur['text'].strip():
            t = re.sub(r"[ \t]+", " ", cur['text']).strip()
            pts = POINTS.findall(t)
            cur.update(text=t, punts_indicats=[p.replace(',', '.') for p in pts])
            out.append(cur)
        cur = None
    modern = meta['any'] >= 2025
    boxed = 2020 <= meta['any'] <= 2024
    BOX = re.compile(r"^\s*Qüestió\s+(\d)\s*$")
    expect = 1
    for page, txt in pages_text(pdf):
        if stopped: break
        if modern and page == 1:                   # cover page with the score table
            m = SERIE.search(txt); serie = int(m.group(1)) if m else serie
            continue
        for line in txt.splitlines():
            if STOP.search(line): stopped = True; break
            m = SERIE.search(line)
            if m and len(line.strip()) < 40:
                if serie != int(m.group(1)): close(); section = opcio = None; expect = 1
                serie = int(m.group(1)); continue
            if SECTION.match(line): close(); section = SECTION.match(line).group(1); continue
            if boxed:
                mb = BOX.match(line)
                if mb: close(); expect = int(mb.group(1)) + 1; continue
                if cur is None and not NOISE.search(line) and line.strip() and serie and expect <= 6:
                    cur = dict(meta, serie=serie, num=expect, section=None, opcio=None, pagina=page, text='')
                if cur is not None and not NOISE.search(line): cur['text'] += line + '\n'
                continue
            mo = OPCIO.match(line)
            if mo:
                prev = cur['num'] if cur else None
                close(); opcio = mo.group(1)
                if modern and prev:
                    cur = dict(meta, serie=serie, num=prev, section=None, opcio=opcio, pagina=page, text='')
                    continue
            me = EXERCICI.match(line)
            mq = Q_NUM.match(line)
            num = None
            if me: num = int(me.group(1) or me.group(2)); opcio = None
            elif mq and not modern and (cur is None or int(mq.group(1)) > cur['num'] or (cur and cur.get('section') != section)): num = int(mq.group(1))
            elif mq and not modern and cur and cur['text'].rstrip().endswith(']') and re.match(r"\s*\d\.\s+[A-ZÀ-Ú]", line): num = cur['num'] + 1
            if num is not None:
                close()
                cur = dict(meta, serie=serie, num=num, section=section, opcio=None, pagina=page, text='')
                line = line if mq else ''
            if mo and cur: cur['opcio'] = opcio
            if cur is None or NOISE.search(line): continue
            cur['text'] += line + '\n'
    close()
    # merge 2025+ option blocks: "OPCIÓ A/B" inside Exercici 4 become separate items
    return out

rows = [r for r in csv.DictReader(open(ROOT / 'manifest.csv', encoding='utf-8'))
        if r['tipus'] == 'enunciat' and not re.search(r'mate26[oe]', r['fitxer'])]
allq = []
for r in rows:
    conv = 'J' if r['convocatoria'].startswith('ordinaria') else 'S'
    meta = dict(any=int(r['any']), convocatoria=conv, fitxer=r['fitxer'])
    qs = segment(str(REPO / r['fitxer']), meta)
    allq += qs
for i, q in enumerate(allq):
    q['id'] = f"{q['any']}-{q['convocatoria']}-S{q['serie'] or 0}-{(q['section'] or 'Q')[0]}{q['num']}{q['opcio'] or ''}"
json.dump(allq, open(ROOT / 'questions_raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
c = collections.Counter((q['any'], q['convocatoria'], q['serie']) for q in allq)
for k in sorted(c, key=lambda k: (k[0], k[1], k[2] or 0)): print(k, c[k], end=' | ')
print('\nTOTAL', len(allq), 'preguntes en', len(c), 'examens (serie)')

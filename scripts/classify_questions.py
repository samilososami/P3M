"""Rule-based v0 classifier for PAU Matematiques questions (block + subtypes) and a 'needs_vision' flag.
Usage: python3 -I classify_questions.py data/matematiques  -> questions.json"""
import json, re, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
BOILER = re.compile(r"^.*(fer i per què|emmagatzemar dades|transmetre o rebre|acabar de respondre|indiqueu clarament|esquemes, esborranys).*$|^\s*(TR|Qüestions|Responeu a|En les respostes|Cada qüestió|Podeu utilitzar|poden emmagatzemar|portin informació|que puguin|Trieu UNA|Indiqueu a la portada|B\) i responeu|•\s*\d+\s*•|\[2,5 punts en total\]|Exercici 4\. Opció).*$", re.M)
BLOCKS = {
 'ANALISI':      r"màxim|mínim|màxima|mínima|el més (gran|petit)|funci[óo]|derivad|tangent|integral|primitiva|asímpt|asimpt|límit|\blim\b|extrem|creix|decreix|continu|derivable|inflexi|corba|paràbola|f ?\(x\)|f ?′|gràfica|recinte|Bolzano|Rolle",
 'ALGEBRA':      r"matri|sistema d.equacions|sistema següent|equacions lineals|determinant|\brang\b|invers|Cramer|incògnit",
 'GEOMETRIA':    r"\bpla\b|plans|rect(a|es) (r|s|de l.espai)|ℝ3|R ?3\b|vector|tetraedre|simètric|equació (general|contínua|paramètrica)|\(x, ?y, ?z\)|punts? de l.espai|distància (del|d.un) punt",
 'PROBABILITAT': r"probabilitat|a l.atzar|binomial|bossa|boles|dau|percentatge|% d",
 'TRIG_PLA':     r"\bsin\b|\bcos\b|\btg\b|angle de \d|circumferència|triangle.*costats|trigonom",
}
SUB = {
 'ANALISI': {
  'EXT':  r"extrems? relatius?|màxims? (i|o) mínims?|màxim relatiu|mínim relatiu|creixement|decreixement|creixent|decreixent|monòton|punts? (singulars|crítics)",
  'INF':  r"inflexi|concavitat|convexitat|còncava|convexa|curvatura|segona derivada|f ?″|f ?''",
  'TAN':  r"tangent|recta normal|pendent",
  'ASI':  r"asímpt|asimpt",
  'CONT': r"continuïtat|discontinu|derivabilitat|sigui (contínua|derivable)|contínua (i derivable )?(en|a) (x|tot|el seu)|derivable en x|(contínua|derivable) a tot",
  'TEO':  r"Bolzano|interval[^.]*(un zero|una arrel|alguna solució|una solució)|(un zero|una arrel)[^.]*interval|exactament (una|dues|tres) solucions|f ?\(x\) ?= ?-?\d+ té una solució|Rolle|valor mitjà|té (alguna|una|exactament)[^.]*(solució|arrel|zero)|(una|alguna) (arrel|solució|zero)[^.]*interval|solucions reals|nombre de (zeros|punts de tall)",
  'INT':  r"integral|primitiva|àrea (del|de la|compresa|limitada|delimitada|de les?)|superfície (del recinte|de la regió)|recinte|Barrow|∫",
  'LIM':  r"\blímit|\blim\b|Hôpital",
  'GRAF': r"(gràfica|gràfiques) (de la (seva )?(funció )?derivada|corresponent a la derivada)|l.una és la derivada|derivada f ?′ ?\(x\)[^.]*figura|figura[^.]*(derivada)",
  'PAR':  r"paràmetres?|valors? de[ls]? (a|b|c|k|m)\b|calculeu (a|b|c|k|m)\b|coeficients|valors de a i (de )?b",
  'REP':  r"esbós de la (seva )?gràfica|esbós de la funció|representació (gràfica )?aproximada|gràfica aproximada de la funció|representeu (gràficament )?la funció|dibuix aproximat de la (seva )?gràfica",
 },
 'ALGEBRA': {
  'DISCUSSIO': r"discutiu|discussió|estudieu[^.]*(sistema|compatib)|segons (els|el) val|en funció (dels? valors? )?del paràmetre",
  'RESOLUCIO': r"resoleu|solució del sistema|trobeu[^.]*solució",
  'SISTEMA':   r"sistema",
  'MATRIUS':   r"matri",
  'INVERSA':   r"invers",
  'RANG':      r"\brang\b",
  'DETERMINANT': r"determinant|\bdet\b",
  'EQ_MATRICIAL': r"equació matricial|X ?·|· ?X|igualtat matricial",
  'POTENCIES': r"potènci|A ?n\b|A\^n|\bA ?[2-9]\b|An en funció|M ?n\b",
 },
 'GEOMETRIA': {
  'POS_RELATIVA': r"posició relativa|s.intersequin|es tallen|paral·lel|paraŀlel|perpendicular|coplanari|es creuen",
  'DISTANCIA': r"distància",
  'SIMETRIC': r"simètric",
  'ANGLE': r"\bangle",
  'AREA_VOLUM': r"volum|tetraedre|àrea del triangle|paral·lelepíped",
  'PROJECCIO': r"projecció|punt (més proper|de la recta més)|peu de la perpendicular",
  'EQ_PLA_RECTA': r"equació (general|contínua|paramètrica|cartesiana|vectorial)|equació del pla|equació de la recta",
 },
 'PROBABILITAT': {
  'CONDICIONADA': r"sabent que|si [^.]*, quina és la probabilitat|condicionada|Bayes",
  'BINOMIAL': r"binomial|exactament \d|almenys|independent|amb reemplaçament|cap de",
  'TOTAL': r"probabilitat (que|de que)[^.]*(sigui|tingui)",
 },
}
NEEDS_VISION = re.compile(r"(funció|matriu|matrius|sistema[^.\n]{0,40}|recta|rectes|expressió|integral|límit|igualtat|Sigui|Siguin|Considereu)\s*[.,:;]\s|\s{2,}[.,:;](\s|$)|\bi\s+[.,]\s|^\s*[–=+]\s*$", re.M)

OPT_WORD = re.compile(r"\b(màxim|mínim|màxima|mínima|maximitz|minimitz)\w*|més (gran|petit|petita|proper|propera|a prop|lluny|econòmic|econòmica|curt|curta) possible|el més (proper|curt|econòmic)|tan econòmica com", re.I)
NOT_OPT = re.compile(r"relatiu|relativa|local|locals|absolut|màxims? (i|o) mínims?|extrems?|(màxims|mínims) (relatius|i)|punts? (mínim|màxim)\b", re.I)
def is_opt(t):
    for sent in re.split(r"(?<=[.?!])\s+", t):
        if OPT_WORD.search(sent) and not NOT_OPT.search(sent): return True
    return False

def classify(text):
    t = BOILER.sub('', text)
    scores = {b: len(re.findall(r, t, re.I)) for b, r in BLOCKS.items()}
    blocks = [b for b, s in sorted(scores.items(), key=lambda x: -x[1]) if s > 0]
    main = blocks[0] if blocks else 'DESCONEGUT'
    subs = {}
    for b in blocks[:2]:
        if b in SUB:
            hit = [k for k, r in SUB[b].items() if k != 'OPT' and re.search(r, t, re.I)]
            if b == 'ANALISI' and is_opt(t): hit.append('OPT')
            if hit: subs[b] = hit
    return t.strip(), main, blocks, scores, subs

qs = json.load(open(ROOT / 'questions_raw.json', encoding='utf-8'))
out = []
# modern Exercici 4: attach the shared intro to options A/B and drop the stub
intro = {}
for q in qs:
    if q['any'] >= 2025 and q['num'] == 4 and not q['opcio']: intro[(q['any'], q['convocatoria'])] = q['text']
for q in qs:
    if q['any'] >= 2025 and q['num'] == 4 and not q['opcio']: continue
    if q['opcio'] and (q['any'], q['convocatoria']) in intro:
        q['text'] = intro[(q['any'], q['convocatoria'])] + '\n' + q['text']
    text, main, blocks, scores, subs = classify(q['text'])
    q.update(text=text, bloc=main, blocs=blocks, subtipus=subs,
             needs_vision=bool(NEEDS_VISION.search(text)) or q['any'] <= 2009)
    out.append(q)
json.dump(out, open(ROOT / 'questions.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'preguntes classificades;', sum(q['needs_vision'] for q in out), 'marcades per a transcripció amb visió')

"""Trend report over all classified PAU Matematiques questions -> analisi_tendencies.md"""
import json, sys, collections
qs = json.load(open(sys.argv[1], encoding='utf-8'))
ERAS = [('1998-2003 (LOGSE, amb trigo/geom. pla)', 1998, 2003), ('2004-2009 (4 qüestions + 2 problemes)', 2004, 2009),
        ('2010-2019 (6 qüestions, 5 a triar)', 2010, 2019), ('2020-2024 (6 qüestions, 4 a triar)', 2020, 2024),
        ('2025-2026 (LOMLOE: 4 exercicis)', 2025, 2026)]
def exams(lo, hi): return {(q['any'], q['convocatoria'], q['serie']) for q in qs if lo <= q['any'] <= hi}
lines = ['# PAU Matemàtiques Catalunya 1998-2026: tendències (classificador v0)\n',
         f"{len(qs)} preguntes, {len({(q['any'], q['convocatoria'], q['serie']) for q in qs})} exàmens (sèries publicades).\n",
         '## Pes de cada bloc (% de preguntes)\n', '| època | exàmens | ' + ' | '.join(['ANALISI', 'ALGEBRA', 'GEOMETRIA', 'PROBABILITAT', 'TRIG_PLA']) + ' |', '|---|---|---|---|---|---|---|']
for name, lo, hi in ERAS:
    sub = [q for q in qs if lo <= q['any'] <= hi]; c = collections.Counter(q['bloc'] for q in sub)
    lines.append(f'| {name} | {len(exams(lo, hi))} | ' + ' | '.join(f"{100*c[b]/len(sub):.0f}%" for b in ['ANALISI', 'ALGEBRA', 'GEOMETRIA', 'PROBABILITAT', 'TRIG_PLA']) + ' |')
TYPES = ['OPT', 'EXT', 'TAN', 'INT', 'PAR', 'ASI', 'INF', 'CONT', 'TEO', 'REP', 'LIM']
lines += ['\n## Anàlisi: % d\'exàmens amb almenys una pregunta de cada tipus\n', '| època | ' + ' | '.join(TYPES) + ' |', '|---|' + '---|' * len(TYPES)]
for name, lo, hi in ERAS:
    ex = collections.defaultdict(set)
    for q in qs:
        if lo <= q['any'] <= hi:
            for t in q['subtipus'].get('ANALISI', []): ex[t].add((q['any'], q['convocatoria'], q['serie']))
    n = len(exams(lo, hi))
    lines.append(f'| {name} | ' + ' | '.join(f"{100*len(ex[t])/n:.0f}%" for t in TYPES) + ' |')
ALG = ['DISCUSSIO', 'RESOLUCIO', 'MATRIUS', 'INVERSA', 'RANG', 'EQ_MATRICIAL', 'POTENCIES', 'DETERMINANT']
GEO = ['POS_RELATIVA', 'DISTANCIA', 'EQ_PLA_RECTA', 'AREA_VOLUM', 'SIMETRIC', 'PROJECCIO', 'ANGLE']
for title, blk, T in [('Àlgebra', 'ALGEBRA', ALG), ('Geometria', 'GEOMETRIA', GEO)]:
    lines += [f'\n## {title}: % d\'exàmens amb cada tipus\n', '| època | ' + ' | '.join(T) + ' |', '|---|' + '---|' * len(T)]
    for name, lo, hi in ERAS[1:]:
        ex = collections.defaultdict(set)
        for q in qs:
            if lo <= q['any'] <= hi and q['bloc'] == blk:
                for t in q['subtipus'].get(blk, []): ex[t].add((q['any'], q['convocatoria'], q['serie']))
        n = len(exams(lo, hi)); lines.append(f'| {name} | ' + ' | '.join(f"{100*len(ex[t])/n:.0f}%" for t in T) + ' |')
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))

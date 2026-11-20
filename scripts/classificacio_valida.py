"""Valida registres de classificació. Ús: python3 -I classificacio_valida.py <lot_in.json> <lot_out.json>"""
import json, sys
BLOCS = {
 'ANA': {'LIM','ASI','CONT','TEO','TAN','EXT','INF','REP','GRAF','OPT','PAR','INT'},
 'ALG': {'MAT','DET','SIS','RES','MOD'},
 'GEO': {'EQG','RPL','DST','ANG','PRJ','VOL','LLG'},
 'PRO': {'PRC','DDI','DNO'},
 'TRI': {'TRI','GPL'},
 'ALTRES': {'ALTRES'},
}
TOTS = set().union(*BLOCS.values())
SUB = {'BOL','ROL','TVM','WEI','PRI','DEF','ARE'}
ATTR = {'figura','parametro','aplicado','comprobar'}
CONF = {'alta','media','baja'}
def check(entrada, sortida):
    err = []
    ids = [x['id'] for x in entrada]
    got = {}
    for r in sortida:
        if r.get('id') in got: err.append(f"{r.get('id')}: duplicat")
        got[r.get('id')] = r
    for i in ids:
        if i not in got: err.append(f'{i}: falta')
    for i in got:
        if i not in ids: err.append(f'{i}: no és al lot')
    for i, r in got.items():
        if r.get('bloc') not in BLOCS: err.append(f"{i}: bloc invàlid {r.get('bloc')}"); continue
        t = r.get('tipus')
        if not isinstance(t, list) or not t: err.append(f'{i}: tipus buit'); continue
        bad = [c for c in t if c not in TOTS]
        if bad: err.append(f'{i}: tipus invàlids {bad}')
        elif t[0] not in BLOCS[r['bloc']]: err.append(f"{i}: el tipus principal {t[0]} no és del bloc {r['bloc']}")
        if len(set(t)) != len(t): err.append(f'{i}: tipus repetits')
        s = r.get('subtipus', [])
        if not isinstance(s, list) or [c for c in s if c not in SUB]: err.append(f'{i}: subtipus invàlids {s}')
        a = r.get('atributs')
        if not isinstance(a, dict) or set(a) != ATTR or not all(isinstance(v, bool) for v in a.values()): err.append(f'{i}: atributs invàlids')
        if r.get('confianza') not in CONF: err.append(f"{i}: confianza invàlida {r.get('confianza')}")
        if not isinstance(r.get('notas', ''), str): err.append(f'{i}: notas no és text')
    return err
if __name__ == '__main__':
    e = json.load(open(sys.argv[1], encoding='utf-8')); s = json.load(open(sys.argv[2], encoding='utf-8'))
    err = check(e, s)
    print(*(err or [f'{len(s)} registres correctes']), sep='\n')
    sys.exit(1 if err else 0)

# Datos · PAU Matemáticas (Cataluña, 1998–2026)

Los PDF están en [`examens/matematiques/<año>/`](../../examens/matematiques/), y su índice en [`examens/matematiques/README.md`](../../examens/matematiques/README.md).

## Ficheros de esta carpeta
| Fichero | Qué es |
|---|---|
| `manifest.csv` | Un PDF por fila: ruta, año, convocatoria, tipo, series que contiene, páginas, fuente, URL base, sha256 y número de versiones anteriores |
| `etiquetes_manuals_2014_2026.csv` | 79 preguntas de análisis (PAU 2014–2026) clasificadas a mano por tipo. Sirven para validar el clasificador automático |

## Nombres de los ficheros
`pau_mate` + año en dos cifras + código:

| Código | Contenido |
|---|---|
| `jl` | Enunciado de junio (ordinaria) |
| `jp` / `jt` | Soluciones de junio |
| `sl` | Enunciado de septiembre (extraordinaria) |
| `sp` | Soluciones de septiembre |
| `o` / `e` (2026) | Ordinaria / extraordinaria, con enunciado y soluciones en el mismo fichero |
| `_tei` | Examen del tribunal TEI (incidencias): **es otra serie**, con preguntas distintas |

## Fuentes y verificación
| Fuente | Qué hay | Cómo se ha verificado |
|---|---|---|
| universitats.gencat.cat (oficial) | 2022–2026 y los TEI 2024–2026 | Descarga directa del servidor oficial |
| gencat vía web.archive.org | Enunciados 2014–2021 | Copias archivadas de las URL oficiales |
| selecat.cat/pau/ | Soluciones 2018–2021; versiones completas de 2013 junio (S3, S4 y S5) y 2018 junio (S1 y S5) | Metadatos del PDF: autor Generalitat y título oficial. Son el mismo PDF oficial, revisado después (misma fecha de creación, fecha de modificación posterior) |
| formaciomiro.com | Enunciado de 2021 septiembre | Metadatos: autor Generalitat y CIC |
| aldeaglobal.net/jrillo | 1998–2017 | Los ficheros de 2014–2017 son idénticos (sha256) a los oficiales, o bien versiones oficiales anteriores del mismo PDF |

Cuando había dos copias distintas de un mismo PDF, me he quedado con la que tiene más series. La otra está en `examens/matematiques/_versions_anteriors/`.

## Series
Según el Govern (respuesta parlamentaria recogida por el diario Ara), se preparan **5 series de cada examen** y solo se publican las que se usan:
- En junio, 2 (3 en 2010 y en 2013).
- En septiembre, 1 (2 en 1999 y en 2000).

Los criterios de corrección oficiales incluyen exactamente las mismas series que los enunciados publicados, así que no falta ninguna serie que se haya usado.

## Huecos conocidos
- Faltan las soluciones de septiembre de 1998 y 1999 (antes del 2000).
- En muchos PDF las fórmulas son imágenes, así que el texto extraído no las contiene. Se transcribirán con visión en la fase 2.

## Scripts (`/scripts`)
| Script | Para qué |
|---|---|
| `consolidate_pdfs.py` | Histórico: ordenó la primera descarga y generó el manifest |
| `add_new_files.py` | Añade PDF nuevos y sustituye un PDF si la copia nueva tiene más series |
| `series_inventory.py` | Lista las series de cada año en todas las copias (enunciados y soluciones) |
| `make_exam_index.py` | Genera el índice `examens/matematiques/README.md` |
| `segment_questions.py`, `classify_questions.py`, `validate_classifier.py`, `analyze_trends.py` | Experimentales (v0): trocear en preguntas y clasificar. Se rehará sobre el texto transcrito |

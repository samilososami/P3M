# P3M

*Pattern-based PAU Prediction Model*

Modelo experimental que predice el contenido de un examen de bachillerato a partir de dos fuentes: los exámenes anteriores del mismo profesor y el histórico de la PAU de Cataluña.

## Enfoque

En Cataluña, muchos exámenes de 2º de bachillerato se construyen a partir de ítems de la PAU. Algunos se copian casi literalmente. Otros se transforman con un cambio de parámetros, una traslación de la variable o un cambio de la condición pedida, pero la estructura del ejercicio, y a menudo su solución, se mantiene.

P3M parte de esta hipótesis y trabaja así:

1. **Corpus.** Se recogen todos los exámenes PAU publicados, con sus criterios de corrección oficiales.
2. **Normalización.** Cada examen se convierte a texto estructurado, con las fórmulas en LaTeX, y se trocea en ítems.
3. **Taxonomía.** Cada ítem se clasifica por bloque, tema y tipo de ejercicio (optimización, estudio de funciones, Bolzano, discusión de sistemas…).
4. **Atribución de fuentes.** Cada ejercicio del usuario se compara con el corpus para encontrar su ítem PAU de origen y la transformación aplicada.
5. **Predicción.** Con las fuentes atribuidas y el temario visto, se estima el siguiente examen en tres niveles: tema, número y tipo de ejercicios, e ítems concretos. Cada estimación lleva su nivel de confianza.

Ejemplo de atribución, sacado de un examen parcial real (octubre de 2026):

| | Enunciado | Solución |
|---|---|---|
| PAU 2008, juny, S5, Q3 | Tangente a *y* = ln(*x*² + 1) paralela a *y* = *x* | *x* = 1, punto (1, ln 2) |
| Examen parcial | Tangente a *f*(*x*) = ln(*x*² − 4*x* + 5) paralela a *y* = −*x* | *x* = 1, punto (1, ln 2) |

Como *x*² − 4*x* + 5 = (*x* − 2)² + 1, el ejercicio es una traslación más un cambio de la recta de referencia, y la solución es la misma.

## Estado

| Fase | Estado |
|---|---|
| Corpus de Matemàtiques (1998–2026) | Completo |
| Transcripción a texto estructurado (LaTeX) | En curso |
| Taxonomía y clasificación de ítems | En curso (taxonomía v1 en borrador) |
| Atribución de fuentes y predicción | Pendiente |
| Aplicación web | Pendiente |
| Resto de asignaturas | Pendiente |

## Estructura

```
P3M/
├── examens/matematiques/     PDF oficiales, organizados por año, e índice (README.md)
├── data/matematiques/        manifest.csv, etiquetas de validación y documentación del corpus
└── scripts/                  descarga, verificación y procesamiento
```

## Corpus: Matemàtiques

| | |
|---|---|
| Periodo | 1998–2026, convocatorias ordinaria y extraordinaria |
| Exámenes (series) | 90 (84 desde 2000) |
| Ficheros PDF | 122: 61 enunciados, 58 criterios de corrección y 3 que incluyen ambos |
| Criterios de corrección | Todos desde 2000 |

**Series.** De cada examen se elaboran cinco series y solo se publican las que se usan: dos en la convocatoria ordinaria (tres en 2010 y 2013) y una en la extraordinaria (dos en 1999 y 2000). Desde 2024 se publica además la serie del tribunal TEI, que tiene ítems propios.

**Evolución del formato.**

| Periodo | Estructura |
|---|---|
| 1998–2003 | 4 cuestiones y 2 problemas. Incluye trigonometría y geometría plana |
| 2004–2009 | 4 cuestiones y 2 problemas (se responden 3 cuestiones y 1 problema) |
| 2010–2019 | 6 cuestiones, se responden 5 |
| 2020–2024 | 6 cuestiones, se responden 4. Probabilidad desde 2024 |
| 2025– | 4 ejercicios obligatorios, el cuarto con opción A/B |

**Procedencia.** Los ficheros se obtienen de universitats.gencat.cat, de sus copias en web.archive.org o de réplicas de los PDF originales. Cada fichero lleva su hash SHA-256 en `data/matematiques/manifest.csv`, y la autenticidad de las réplicas se ha comprobado contra los originales. El detalle está en [`data/matematiques/README.md`](data/matematiques/README.md).

## Aviso

Los enunciados y los criterios de corrección son propiedad de la Generalitat de Catalunya y del Consell Interuniversitari de Catalunya. Se reproducen sin modificaciones, con finalidad educativa y citando la fuente.

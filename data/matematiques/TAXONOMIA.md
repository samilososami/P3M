# Taxonomía v1 · PAU Matemáticas (Cataluña)

Borrador pendiente de aprobación. Define cómo se clasifica cada ítem (cuestión, problema o ejercicio) de las 91 series transcritas (540 ítems). La clasificación sirve para dos cosas: comparar ejercicios de otros exámenes con el corpus de la PAU, y estimar qué temas y tipos de ejercicio son probables.

## Principios

- **Dos niveles fijos y un tercero que se descubre.** Nivel 1: bloque. Nivel 2: tipo de ejercicio (qué hay que hacer). Nivel 3: patrón (la variante concreta, por ejemplo «tangente paralela a una recta dada»). El patrón no se define a mano: se obtiene agrupando ítems ya clasificados.
- **Un ítem tiene un tipo principal y puede tener tipos secundarios.** Los ejercicios de la PAU combinan varias tareas, y los 79 ítems etiquetados a mano ya lo hacen (`TAN|INT`, `EXT|INF|INT`). El principal es el que más pesa en la solución.
- **Los códigos de las etiquetas manuales se conservan.** Solo se añaden los que esas etiquetas no cubrían, para poder medir el clasificador contra ellas.
- **Los atributos son independientes del tipo.** Una optimización puede tener figura, parámetro y contexto real a la vez.

## Bloques y tipos

| Bloque | Código | Contenido |
|---|---|---|
| Análisis | `ANA` | Funciones, límites, derivadas, integrales |
| Álgebra lineal | `ALG` | Matrices, determinantes, sistemas |
| Geometría del espacio | `GEO` | Rectas, planos, vectores en R³ |
| Probabilidad y estadística | `PRO` | Desde 2010 de forma esporádica, regular desde 2024 |
| Trigonometría y geometría plana | `TRI` | Heredado: concentrado en 1998–2003, residual después |

### Análisis (`ANA`)

| Tipo | Código | Qué pide | Origen del código |
|---|---|---|---|
| Límites | `LIM` | Calcular límites e indeterminaciones | nuevo |
| Asíntotas | `ASI` | Asíntotas verticales, horizontales y oblicuas | manual |
| Continuidad | `CONT` | Continuidad y derivabilidad, funciones a trozos | manual |
| Teoremas | `TEO` | Bolzano (`BOL`), Rolle (`ROL`), valor medio (`TVM`), Weierstrass (`WEI`) | manual, con subtipo |
| Recta tangente | `TAN` | Tangente o normal, condiciones sobre su pendiente | manual |
| Extremos y crecimiento | `EXT` | Máximos, mínimos, intervalos de crecimiento | manual |
| Inflexión y curvatura | `INF` | Puntos de inflexión, concavidad | manual |
| Representación de funciones | `REP` | Estudio completo y dibujo de la gráfica | manual |
| Lectura de gráficas | `GRAF` | Obtener información de la gráfica de f o de f′ | manual |
| Optimización | `OPT` | Problema aplicado de máximo o mínimo | manual |
| Parámetros | `PAR` | Determinar parámetros a partir de condiciones | manual |
| Integrales | `INT` | Primitivas, integral definida y áreas (subtipos `PRI`, `DEF`, `ARE`) | manual, con subtipo |

### Álgebra lineal (`ALG`)

| Tipo | Código | Qué pide |
|---|---|---|
| Operaciones y ecuaciones matriciales | `MAT` | Productos, potencias, inversa, ecuaciones con matrices |
| Determinantes y rango | `DET` | Calcular determinantes, estudiar el rango |
| Discusión de sistemas | `SIS` | Sistema con parámetro: SCD, SCI, SI |
| Resolución de sistemas | `RES` | Resolver un sistema concreto, Gauss |
| Modelización | `MOD` | Plantear un enunciado como sistema de ecuaciones |

### Geometría del espacio (`GEO`)

| Tipo | Código | Qué pide |
|---|---|---|
| Ecuaciones | `EQG` | Ecuación de recta o plano a partir de datos |
| Posiciones relativas | `RPL` | Entre rectas, planos o recta y plano |
| Distancias | `DST` | Punto–recta, punto–plano, recta–recta, etc. |
| Ángulos | `ANG` | Entre rectas, planos o recta y plano |
| Proyecciones y simétricos | `PRJ` | Proyección ortogonal, punto simétrico |
| Áreas y volúmenes | `VOL` | Con producto vectorial o mixto, tetraedros, paralelepípedos |
| Lugares geométricos | `LLG` | Puntos que cumplen una condición |

### Probabilidad y estadística (`PRO`)

| Tipo | Código | Qué pide |
|---|---|---|
| Probabilidad condicionada | `PRC` | Probabilidad total, condicionada, Bayes |
| Distribuciones discretas | `DDI` | Binomial y similares |
| Distribución normal | `DNO` | Tipificación, probabilidades con la normal |

### Trigonometría y geometría plana (`TRI`)

| Tipo | Código | Qué pide |
|---|---|---|
| Trigonometría | `TRI` | Resolución de triángulos, razones trigonométricas |
| Geometría plana | `GPL` | Circunferencias, polígonos, áreas planas |

## Atributos

| Atributo | Valores | Para qué sirve |
|---|---|---|
| `figura` | sí / no | El enunciado incluye gráfica o dibujo |
| `parametro` | sí / no | Aparece un parámetro que hay que discutir o determinar |
| `aplicado` | sí / no | Contexto real (fábrica, río, bote…) que obliga a modelizar |
| `comprobar` | sí / no | Pide «comproveu que…» y la respuesta viene dada |
| `opcion` | `A`, `B`, ninguna | Solo 2025+ |

## Registro de clasificación

Cada ítem produce un registro:

```json
{
  "id": "2008-ord-S5-Q3",
  "bloc": "ANA",
  "tipus": ["TAN", "PAR"],
  "subtipus": [],
  "atributs": {"figura": false, "parametro": false, "aplicado": false, "comprobar": false},
  "confianza": "alta",
  "notas": ""
}
```

El primer elemento de `tipus` es el principal.

## Cobertura orientativa

Recuento por palabras clave sobre los 540 ítems. Un ítem puede contar en varios bloques (por ejemplo, un sistema modelizado con un contexto real), así que las filas no suman el total.

| Época | ALG | GEO | ANA | PRO | TRI |
|---|---|---|---|---|---|
| 1998–2003 (120 ítems) | 9 | 38 | 72 | 0 | 41 |
| 2004–2009 (108) | 28 | 36 | 46 | 0 | 10 |
| 2010–2019 (192) | 60 | 70 | 80 | 6 | 21 |
| 2020–2024 (90) | 27 | 25 | 46 | 14 | 9 |
| 2025– (30) | 7 | 10 | 17 | 8 | 3 |

Estos números son solo una brújula. La clasificación real la hará un clasificador, no las palabras clave.

## Decisiones que conviene revisar

1. **`TRI` queda como bloque propio** en vez de repartirse: casi no aparece desde 2010 y no debería pesar en predicciones de exámenes actuales.
2. **Las etiquetas manuales solo cubren análisis** (79 ítems, 2014–2026). Para `ALG`, `GEO` y `PRO` no hay verdad de referencia, y habrá que etiquetar a mano una muestra antes de fiarse de las métricas.
3. **El patrón (nivel 3) no se fija ahora.** Se propone después de clasificar, agrupando los ítems que comparten estructura.
4. **No se separa «analítico» de «geométrico»** dentro de `GEO` (por ejemplo, `DST` en el plano frente al espacio): en la PAU actual todo es en R³.

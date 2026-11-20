# Taxonomía v1.1 · PAU Matemáticas (Cataluña)

Aprobada en su estructura; la v1.1 añade las reglas de aplicación tras las primeras pruebas de clasificación. Define cómo se clasifica cada ítem (cuestión, problema o ejercicio) de las 91 series transcritas (540 ítems). La clasificación sirve para dos cosas: comparar ejercicios de otros exámenes con el corpus de la PAU, y estimar qué temas y tipos de ejercicio son probables.

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
| Discusión de sistemas | `SIS` | Determinar o discutir el tipo de sistema (SCD, SCI, SI), con o sin parámetro |
| Resolución de sistemas | `RES` | Calcular la solución de un sistema concreto, Gauss |
| Modelización | `MOD` | Plantear un enunciado como sistema de ecuaciones |
| Vectores y espacios vectoriales | `VEC` | Bases, coordenadas, dependencia lineal, operaciones con vectores y puntos (punto medio, división de un segmento) |

### Geometría del espacio (`GEO`)

| Tipo | Código | Qué pide |
|---|---|---|
| Ecuaciones | `EQG` | Ecuación de recta o plano a partir de datos |
| Posiciones relativas | `RPL` | Entre rectas, planos o recta y plano |
| Distancias | `DST` | Entre elementos del espacio: punto–punto, punto–recta, punto–plano, recta–recta; longitudes de segmentos |
| Ángulos | `ANG` | Entre rectas, planos o recta y plano del espacio; perpendicularidad comprobada con el producto escalar |
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
| Trigonometría | `TRI` | Todo lo que se resuelve con razones trigonométricas o teoremas del seno y del coseno, aunque la figura sea un polígono |
| Geometría plana | `GPL` | Geometría analítica del plano: circunferencias, rectas y vectores en R², áreas planas, ángulos entre vectores del plano |

## Reglas de aplicación (v1.1)

**Tipo principal**
- Es la tarea que más pesa en la solución, no la primera del enunciado. Si los apartados pesan igual, manda el reparto de puntos de los criterios oficiales; si no consta, el apartado con más pasos.
- Un paso trivial (resolver `sin x = cos x`) no es un tipo secundario. No se rellena.
- `PAR` solo existe como tipo en `ANA`. Es principal cuando lo que se pide es el valor de los parámetros. Si lo pedido es otra cosa (un extremo, un límite, un área, una recta), `PAR` va como secundario y el atributo `parametro` es `true`. En `ALG` y `GEO` un parámetro solo se marca con el atributo.
- `EQG` es principal solo si construir la ecuación es lo que más pesa. Si el trabajo real es imponer una distancia o una posición relativa, manda `DST` o `RPL`.
- `REP` incluye `ASI`, `EXT`, `INF` y `TAN` dentro de un estudio completo. Solo se pone `REP` si se pide el dibujo; un estudio parcial (dominio, asíntotas, extremos) se clasifica por sus partes.
- `OPT` exige modelizar la magnitud que se optimiza, con contexto real o geométrico. Minimizar una función ya dada (por ejemplo, definida por una integral) es `EXT`.
- Alineación de puntos: `RPL`. Dependencia lineal de vectores, bases y coordenadas: `VEC`.
- Si el principal es de un bloque, los secundarios pueden ser de cualquiera.
- Un ítem puramente teórico sin cálculo se clasifica por su tema y lo indica en `notas` con el prefijo `teòric:`.
- Las identidades o comprobaciones puras sin un tipo que encaje van a `ALTRES`, explicadas en `notas`.

**Subtipos**
- Se admiten varios en un mismo ítem (`["PRI","ARE"]`).

## Atributos

| Atributo | Valores | Para qué sirve |
|---|---|---|
| `figura` | sí / no | El enunciado trae el dibujo dado. Si solo pide hacer uno, es `no` |
| `parametro` | sí / no | Hay una constante literal que se discute o se determina, la llame o no «paràmetre» el enunciado |
| `aplicado` | sí / no | Objeto o contexto no matemático en el enunciado (fábrica, río, bote, reloj). La geometría abstracta no cuenta |
| `comprobar` | sí / no | Pide «comproveu que…» o «demostreu que…» y la respuesta viene dada |
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

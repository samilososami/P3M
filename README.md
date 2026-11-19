# P3M · Pattern-based PAU Prediction Model

**P3M** es un modelo experimental que intenta predecir qué saldrá en el próximo examen de bachillerato a partir de los exámenes de la **PAU de Cataluña** (selectividad).

## Qué significan las siglas

| Letra | Palabra | Qué quiere decir |
|---|---|---|
| **P** | *Pattern-based* | Se basa en patrones: busca qué se repite y cómo |
| **P** | *PAU* | Trabaja con los exámenes de la PAU de Cataluña |
| **P** | *Prediction* | Su objetivo es predecir el siguiente examen |
| **M** | *Model* | Es un modelo, no una lista de exámenes |

Tres P y una M: **P³M**, que en texto plano se escribe **P3M**.

## La idea

En Cataluña, muchos profesores de bachillerato preparan sus exámenes a partir de ejercicios de la PAU. A veces los copian casi tal cual y a veces los transforman: cambian la función o los números, pero mantienen la estructura.

P3M quiere aprovechar eso. Le das los exámenes que ya has hecho, te dice de qué PAU salieron y, con eso, predice qué puede entrar en el siguiente. La predicción tiene tres niveles, de más fácil a más difícil:

1. **El tema** del próximo examen.
2. **Cuántos ejercicios** habrá y **de qué tipo** (optimización, estudio de funciones, Bolzano…).
3. **Los ejercicios concretos**: qué preguntas PAU es más probable que use el profesor.

### Un ejemplo real
En un parcial de 2º de bachillerato (octubre de 2026) salió este ejercicio:

> *Calcula para qué punto de f(x) = ln(x² − 4x + 5) la recta tangente es paralela a la bisectriz del segundo y cuarto cuadrante.*

Es el ejercicio de la **PAU 2008, junio, Sèrie 5, Q3** (*ln(x² + 1)*, tangente paralela a *y = x*) transformado: *x² − 4x + 5 = (x − 2)² + 1*. Además, la solución es exactamente la misma, el punto (1, ln 2). Este tipo de huella es la que P3M busca.

## Estado del proyecto

| Fase | Estado |
|---|---|
| 1. Descargar y ordenar todas las PAU de Matemáticas (1998–2026) | ✅ Hecho |
| 2. Pasar los PDF a texto, con las fórmulas en LaTeX (hay muchas que en el PDF son imágenes) | ⏳ Siguiente paso |
| 3. Clasificar cada pregunta por tema y tipo | Pendiente |
| 4. Motor de comparación (examen del usuario → PAU de origen) y predicción | Pendiente |
| 5. Web (Vercel) con login de IA por usuario (Puter.js) | Pendiente |
| 6. Ampliar al resto de asignaturas | Pendiente |

## Qué hay en el repositorio

```
P3M/
├── examens/
│   └── matematiques/        ← los PDF, uno por carpeta de año
│       ├── 1998/ … 2026/
│       ├── _versions_anteriors/
│       └── README.md        ← índice de todos los PDF (con enlaces)
├── data/
│   └── matematiques/
│       ├── manifest.csv     ← un fichero por fila: año, convocatoria, series, fuente y hash
│       ├── etiquetes_manuals_2014_2026.csv
│       └── README.md        ← fuentes, verificación y huecos conocidos
└── scripts/                 ← scripts en Python para descargar, ordenar y procesar
```

**¿Buscas un examen concreto?** Ve a [`examens/matematiques/`](examens/matematiques/), donde hay un índice con todos los PDF ordenados por año.

## Matemáticas: lo que hay

- **90 exámenes** (cada serie cuenta como un examen) de **1998 a 2026**, de las convocatorias de junio y septiembre. Desde el 2000 son 84.
- **122 PDF**: 61 enunciados, 58 de soluciones (criterios de corrección oficiales) y 3 con las dos cosas juntas.
- **Soluciones de todos los exámenes desde el 2000.**

### Las series
Cada año se preparan **5 series** (versiones distintas) de cada examen, pero solo se publican las que se usaron:

| | Junio | Septiembre |
|---|---|---|
| Lo normal | 2 series | 1 serie |
| 2010 y 2013 | 3 series | 1 serie |
| 1999 y 2000 | 2 series | 2 series |

Desde 2024, una de las series de junio es la del **tribunal TEI** (incidencias), que es un examen con preguntas propias. Las series de reserva no se publican nunca.

### Cómo ha cambiado el formato

| Época | Formato |
|---|---|
| 1998–2003 | 4 cuestiones + 2 problemas. Todavía entraban trigonometría y geometría plana |
| 2004–2009 | 4 cuestiones + 2 problemas (respondías 3 cuestiones y 1 problema) |
| 2010–2019 | 6 cuestiones, respondías 5 |
| 2020–2024 | 6 cuestiones, respondías 4. En 2024 entra la probabilidad |
| 2025–2026 | 4 ejercicios obligatorios, el 4º con opción A o B |

### Fuentes
Todos los PDF son **documentos oficiales** de la Generalitat de Catalunya y del Consell Interuniversitari de Catalunya. Se han sacado de:

- **universitats.gencat.cat** directamente.
- **Copias archivadas** de gencat en web.archive.org.
- **Espejos** que conservan los PDF originales: selecat.cat, aldeaglobal.net y formaciomiro.com.

Para comprobar que los espejos son fieles, he comparado sus ficheros con los oficiales (hash sha256) y he revisado los metadatos de cada PDF. Los detalles están en [`data/matematiques/README.md`](data/matematiques/README.md).

## Aviso
- Los exámenes y las soluciones son propiedad de la **Generalitat de Catalunya** y del **Consell Interuniversitari de Catalunya**. Se reproducen sin modificar, con finalidad educativa y citando la fuente.
- P3M es un **proyecto experimental**. Una predicción es una apuesta informada, no una garantía.

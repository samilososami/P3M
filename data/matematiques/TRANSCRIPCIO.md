# Guía de transcripción (Matemàtiques)

Objetivo: convertir cada examen (serie) a un fichero fuente `examens/matematiques/<año>/<id>.md`, con el formato que se describe aquí. A partir de ese fichero, `scripts/build_json.py` genera `data/matematiques/examens/<año>/<id>.json`.

- El plan está en `data/matematiques/transcripcio_pla.csv`: una fila por examen con su id, las páginas del enunciado (`fichero.pdf#ini-fin`) y las de la solución (`#tot` quiere decir que hay que buscar la serie dentro del PDF).
- La referencia de formato es `examens/matematiques/2008/2008-ord-S5.md`.

## Proceso para cada examen
1. Renderizar las páginas del enunciado: `pdftoppm -r 110 -f INI -l FIN -png examens/matematiques/<año>/<fichero>.pdf <scratch>/<prefijo>`.
2. Leer las imágenes. **El enunciado se transcribe siempre a partir de la imagen**: `pdftotext` pierde o deforma las fórmulas. El texto extraído solo sirve de apoyo para la prosa.
3. Solución: usar `pdftotext -f INI -l FIN` del PDF de criterios. Si el texto de una fórmula es ambiguo, mirar la imagen.
4. Escribir el `.md` y validarlo con `python3 -I scripts/build_json.py . --check`, sin errores.

## Formato del fichero `.md`

```
---
id: 2008-ord-S5                # <año>-<ord|ext>-S<serie>
any: 2008
convocatoria: ordinaria        # ordinaria | extraordinaria
serie: 5
tribunal: ordinari             # ordinari | TEI
estructura: 4 qüestions i 2 problemes; es responen 3 qüestions i 1 problema
enunciat: pau_mate08jl.pdf#3-4
criteris: pau_mate08jp.pdf#7-11    # omitir si no hay solución oficial
transcripcio: enunciat per visió sobre el PDF; solucions a partir del text del PDF de criteris, contrastat amb la imatge
---

# PAU 2008 · Matemàtiques · Convocatòria ordinària · Sèrie 5

<instrucciones de la portada, literales>

## Qüestió 1 (2 punts)            # o: Problema 5 (4 punts) · Exercici 1 (2,5 punts) · Exercici 4, opció A (2,5 punts)

<enunciado común>

**a)** (1 punt) <apartado>          # en 2025+: **1.1)** (1 punt) ...

> Figura: <descripción con los datos matemáticos necesarios>

*Puntuació: <reparto de puntos si no va por apartados>*

### Solució

<desarrollo clave de la solución oficial>

**Resultat:** <resultado final>
**Nota:** <solo si hay una incidencia: errata, puntuación incoherente, etc.>
```

## Normas
- **Texto literal en catalán**, tal como sale en el examen: no se traduce, no se resume y no se corrige la redacción.
- **Fórmulas en LaTeX**: `$...$` en línea y `$$...$$` en bloque. Matrices con `pmatrix`, sistemas y funciones a trozos con `cases`, determinantes con `vmatrix`, rectas en forma continua con `\dfrac`.
- **Figuras**: una línea `> Figura:` que describa lo que haga falta para resolver el ejercicio (puntos, ejes, valores que se leen en la gráfica, forma de la curva). Si la figura es solo decorativa, basta con decirlo.
- **Puntos**: los que indica el enunciado. Si los criterios dicen otra cosa, se mantienen los del enunciado y se añade una `**Nota:**`.
- **Solución**: el desarrollo clave (planteamiento, ecuaciones principales, resultados intermedios importantes) y el `**Resultat:**` final, exacto. Se omiten las instrucciones de corrección para el tribunal.
- **Exercici 4 con opciones (2025+)**: cada opción es un ítem propio (`## Exercici 4, opció A (...)`). El texto introductorio común se repite en las dos.
- **Exámenes sin solución oficial**: se omite `criteris:` y la sección `### Solució`.
- **Si algo no se puede leer**, se escribe `[il·legible]` en vez de inventarlo.

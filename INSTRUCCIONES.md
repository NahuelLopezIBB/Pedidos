# Instrucciones para publicar un pedido

Cuando Nahuel pide un archivo para este repo, se publica como un libro suelto
en el catálogo OPDS. No hay horario ni tarea fija: cada pedido se hace en el
momento.

## Nombre del archivo

`AAAA-MM-DD-tema`, con la fecha del día en hora argentina (UTC-3) y el tema en
minúsculas, sin acentos y con guiones. Ej.: `2026-11-01-historia-del-carem`.
Si ya existe uno con ese nombre y es una versión nueva, agregar `-v2`, `-v3`.

## Caso 1: contenido que escribe Claude (informe, apunte, resumen, guía)

Escribir `pedidos/AAAA-MM-DD-tema.md` con este formato:

```
# Título del libro

Uno o dos párrafos de presentación (opcional; van en la portada).

## Primer capítulo

### Subtema

Texto...

Fuentes: [Fuente 1](https://...), [Fuente 2](https://...)

## Segundo capítulo
...
```

Reglas del formato:

- `# ` solo una vez, en la primera línea: es el título del libro.
- `## ` es cada capítulo (aparece en el índice del Kindle).
- `### ` es cada subtema dentro del capítulo.
- Se pueden usar `**negrita**`, `*cursiva*`, links `[texto](url)` y listas con `- `.
- Tablas en markdown (`| a | b |` con la fila `|---|---|`), pero la pantalla del
  Kindle es angosta: máximo **4 columnas** y celdas cortas. Si no entra, usar
  una lista con un elemento por fila.
- Las líneas que empiezan con `Fuentes:` se muestran en letra chica.
- Imágenes: una línea sola con `![pie de figura](img/<carpeta>/archivo.png)`, con la
  ruta relativa a `pedidos/`. El generador las mete dentro del EPUB. Para el Kindle
  conviene PNG en escala de grises, de unos 600 px de ancho, con letra grande. Los
  scripts que generan gráficos van en `tools/` (ejemplo: `tools/graficos_clases_3_8.py`).

Criterios de contenido (salvo que el pedido diga otra cosa):

- Seguir al pie de la letra lo que pide Nahuel: si enumera aspectos, cubrirlos
  todos.
- Si el tema es de actualidad o tiene datos que cambian, investigar en la web
  y citar las fuentes. Preferir fuentes primarias.
- Nivel de un lector con formación técnica (ingeniero nuclear); explicar
  igualmente nombres, siglas y términos de áreas ajenas la primera vez.
- Tono neutral en temas políticos. Todo con palabras propias: nada de copiar
  párrafos de las fuentes.

Generar con:

```bash
python3 tools/build.py pedidos/AAAA-MM-DD-tema.md
```

## Caso 2: archivo ya hecho (PDF, EPUB, CBZ, TXT...)

Si Nahuel adjunta un archivo o pide uno que hay que generar en otro formato
(por ejemplo un PDF), guardarlo como `archivos/AAAA-MM-DD-tema.ext` y
registrarlo con un título legible:

```bash
python3 tools/build.py archivos/AAAA-MM-DD-tema.pdf "Título que se ve en KOReader"
```

Formatos aceptados: epub, pdf, cbz, djvu, mobi, fb2, txt, html, md.
No subir material con derechos de autor que no sea de Nahuel: el repo y el
sitio son públicos.

## Publicar

Hacer commit y push a `main` con el mensaje `Pedido AAAA-MM-DD-tema`.
Pages tarda un par de minutos; después aparece en el catálogo de KOReader.

## Quitar algo

```bash
python3 tools/build.py --quitar AAAA-MM-DD-tema.ext
```

Commit y push con el mensaje `Quitar AAAA-MM-DD-tema`.

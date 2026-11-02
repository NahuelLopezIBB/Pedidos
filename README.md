# Pedidos

Archivos a pedido (informes, apuntes, libros, PDFs), publicados como catálogo
OPDS para KOReader. Mismo sistema que [Noticias](https://github.com/NahuelLopezIBB/Noticias),
pero sin horario fijo: cada archivo se publica cuando Nahuel lo pide.

- Catálogo OPDS: <https://nahuellopezibb.github.io/Pedidos/opds.xml>
- Página web: <https://nahuellopezibb.github.io/Pedidos/>

## Cómo funciona

1. Nahuel le pide a Claude un archivo. Claude sigue
   [`INSTRUCCIONES.md`](INSTRUCCIONES.md).
2. Si el contenido lo escribe Claude, va en markdown a `pedidos/AAAA-MM-DD-tema.md`
   y [`tools/build.py`](tools/build.py) lo convierte en `archivos/AAAA-MM-DD-tema.epub`.
3. Si es un archivo ya hecho (un PDF, un EPUB), se guarda directo en `archivos/`
   y `build.py` lo agrega al catálogo.
4. El push a `main` dispara GitHub Pages; en un par de minutos aparece en KOReader.

A diferencia de Noticias, **nada se borra solo**. Para sacar algo:

```bash
python3 tools/build.py --quitar 2026-11-01-tema.epub
```

## Estructura

| Ruta | Qué es |
| --- | --- |
| `INSTRUCCIONES.md` | Cómo se arma y publica cada pedido. |
| `pedidos/` | Fuente markdown de los pedidos que escribe Claude. |
| `archivos/` | Lo que se publica (EPUB, PDF, etc.) e `index.json` (metadatos). |
| `opds.xml` | Catálogo OPDS (Atom) que lee KOReader. |
| `tools/build.py` | Generador, solo biblioteca estándar de Python. |
| `.nojekyll` | Le indica a Pages que sirva los archivos tal cual. |

## Usarlo a mano

```bash
python3 tools/build.py pedidos/2026-11-01-tema.md          # markdown -> EPUB
python3 tools/build.py archivos/2026-11-01-paper.pdf "Título"   # archivo ya hecho
```

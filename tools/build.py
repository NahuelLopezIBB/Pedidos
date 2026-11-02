#!/usr/bin/env python3
"""Publica un pedido en el catálogo OPDS.

Uso:
    python3 tools/build.py pedidos/AAAA-MM-DD-tema.md
        Convierte el markdown en archivos/AAAA-MM-DD-tema.epub.
    python3 tools/build.py archivos/AAAA-MM-DD-tema.pdf ["Título"]
        Registra un archivo que ya está hecho (pdf, epub, cbz, txt...).
        El título es opcional; si falta, se arma a partir del nombre.
    python3 tools/build.py --quitar AAAA-MM-DD-tema.ext
        Saca un archivo del catálogo y lo borra.

En todos los casos regenera opds.xml (lo que lee KOReader) e index.html.
A diferencia de Noticias, nada se borra solo: los pedidos quedan hasta que
se quiten a mano.

Sin dependencias externas: solo la biblioteca estándar de Python.
"""

import datetime as dt
import html
import json
import re
import sys
import uuid
import zipfile
from pathlib import Path

BASE_URL = "https://nahuellopezibb.github.io/Pedidos"
FEED_TITLE = "Pedidos"
AUTHOR = "Pedidos (Claude)"

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "archivos"
SRC_DIR = ROOT / "pedidos"
INDEX_JSON = OUT_DIR / "index.json"
NAME_RE = r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*"

MIME = {
    ".epub": "application/epub+zip",
    ".pdf": "application/pdf",
    ".cbz": "application/vnd.comicbook+zip",
    ".djvu": "image/vnd.djvu",
    ".mobi": "application/x-mobipocket-ebook",
    ".fb2": "application/x-fictionbook+xml",
    ".txt": "text/plain",
    ".html": "text/html",
    ".md": "text/markdown",
}
ART = dt.timezone(dt.timedelta(hours=-3))

CSS = """
body { font-family: serif; line-height: 1.45; margin: 0 0.6em; }
h1 { font-size: 1.5em; margin: 0.8em 0 0.4em; }
h2 { font-size: 1.15em; margin: 1.4em 0 0.3em; }
p { margin: 0 0 0.7em; text-align: justify; }
.src { font-size: 0.8em; margin-top: -0.3em; }
.intro { font-style: italic; }
ul { margin: 0 0 0.8em 1.1em; padding: 0; }
li { margin-bottom: 0.3em; }
a { color: inherit; }
table { border-collapse: collapse; width: 100%; margin: 0.4em 0 1em; font-size: 0.85em; line-height: 1.25; }
th, td { border: 1px solid #000; padding: 0.25em 0.35em; text-align: left; vertical-align: top; }
th { font-weight: bold; }
td.num, th.num { text-align: right; }
"""


# ---------------------------------------------------------------- markdown

def inline(text: str) -> str:
    """Escapa HTML y convierte **negrita**, *cursiva* y [texto](url)."""
    out = html.escape(text, quote=False)
    out = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                 lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", out)
    return out


def split_row(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_html(rows) -> str:
    """Tabla markdown (| a | b |) -> <table>. La fila |---| separa el encabezado."""
    sep = next((i for i, r in enumerate(rows) if re.fullmatch(r"\|?[\s:|-]+\|?", r.strip())), None)
    head = [split_row(r) for r in rows[:sep]] if sep is not None else []
    body = [split_row(r) for r in (rows[sep + 1:] if sep is not None else rows)]
    is_num = lambda c: bool(re.fullmatch(r"[+\-−]?[\d.,\s%]+(\([\d.,\s%]+\))?", c)) and any(ch.isdigit() for ch in c)

    def cells(row, tag):
        return "".join(
            f'<{tag}{" class=\"num\"" if tag == "td" and is_num(c) else ""}>{inline(c)}</{tag}>'
            for c in row)

    out = "<table>"
    if head:
        out += "<thead>" + "".join(f"<tr>{cells(r, 'th')}</tr>" for r in head) + "</thead>"
    out += "<tbody>" + "".join(f"<tr>{cells(r, 'td')}</tr>" for r in body) + "</tbody></table>"
    return out


def blocks_to_html(lines):
    """Convierte las líneas de una sección en HTML (### títulos, listas, tablas, párrafos)."""
    parts, para, items, table = [], [], [], []

    def flush():
        nonlocal para, items, table
        if table:
            parts.append(table_html(table))
            table = []
        if para:
            text = " ".join(para)
            cls = ' class="src"' if text.lower().startswith(("fuente", "fuentes")) else ""
            parts.append(f"<p{cls}>{inline(text)}</p>")
            para = []
        if items:
            parts.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush()
        elif line.lstrip().startswith("|"):
            if para or items:
                flush()
            table.append(line)
        elif line.startswith("### "):
            flush()
            parts.append(f"<h2>{inline(line[4:].strip())}</h2>")
        elif re.match(r"^\s*[-*] ", line):
            if para or table:
                flush()
            items.append(re.sub(r"^\s*[-*] ", "", line).strip())
        else:
            if items or table:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(parts)


def parse_edition(md: str):
    title, intro, sections, current = None, [], [], None
    for line in md.splitlines():
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
        elif line.startswith("## "):
            current = {"title": line[3:].strip(), "lines": []}
            sections.append(current)
        elif current is None:
            intro.append(line)
        else:
            current["lines"].append(line)
    if not title or not sections:
        sys.exit("La edición necesita un título '# ...' y al menos una sección '## ...'")
    return title, intro, sections


# --------------------------------------------------------------------- epub

def xhtml(title, body):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="es" xml:lang="es">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title>
<link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{body}
</body></html>
"""


def build_epub(date: str, title: str, intro, sections, out: Path):
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, BASE_URL + '/' + date)}"
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    chapters = []  # (filename, title, xhtml)
    intro_html = blocks_to_html(intro)
    toc_list = "".join(f"<li>{html.escape(s['title'])}</li>" for s in sections)
    cover_body = (f"<h1>{html.escape(title)}</h1>\n"
                  + (f'<div class="intro">{intro_html}</div>\n' if intro_html else "")
                  + f"<p><strong>Secciones:</strong></p><ul>{toc_list}</ul>")
    chapters.append(("portada.xhtml", "Portada", xhtml(title, cover_body)))
    for n, sec in enumerate(sections, 1):
        body = f"<h1>{html.escape(sec['title'])}</h1>\n{blocks_to_html(sec['lines'])}"
        chapters.append((f"sec{n:02d}.xhtml", sec["title"], xhtml(sec["title"], body)))

    manifest = "\n".join(
        f'    <item id="c{i}" href="{f}" media-type="application/xhtml+xml"/>'
        for i, (f, _, _) in enumerate(chapters))
    spine = "\n".join(f'    <itemref idref="c{i}"/>' for i in range(len(chapters)))
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="es">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_id}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(AUTHOR)}</dc:creator>
    <dc:language>es</dc:language>
    <dc:date>{date[:10]}</dc:date>
    <meta property="dcterms:modified">{now}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="css" href="style.css" media-type="text/css"/>
{manifest}
  </manifest>
  <spine toc="ncx">
{spine}
  </spine>
</package>
"""
    nav_items = "".join(f'<li><a href="{f}">{html.escape(t)}</a></li>' for f, t, _ in chapters)
    nav = xhtml("Índice", f'<nav epub:type="toc" id="toc"><h1>Índice</h1><ol>{nav_items}</ol></nav>')
    points = "".join(
        f'<navPoint id="p{i}" playOrder="{i + 1}"><navLabel><text>{html.escape(t)}</text></navLabel>'
        f'<content src="{f}"/></navPoint>' for i, (f, t, _) in enumerate(chapters))
    ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{book_id}"/></head>
<docTitle><text>{html.escape(title)}</text></docTitle>
<navMap>{points}</navMap>
</ncx>
"""
    container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w") as z:
        # "mimetype" tiene que ir primero y sin comprimir (requisito de EPUB)
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        for f, _, body in chapters:
            z.writestr(f"OEBPS/{f}", body, compress_type=zipfile.ZIP_DEFLATED)


# ------------------------------------------------------------ opds / index

def write_catalog(index: dict):
    now = dt.datetime.now(ART).isoformat(timespec="seconds")
    entries = []
    for name in sorted(index, reverse=True):
        e = index[name]
        url = f"{BASE_URL}/archivos/{name}"
        entries.append(f"""  <entry>
    <title>{html.escape(e['title'])}</title>
    <id>urn:pedidos:{name}</id>
    <updated>{e['updated']}</updated>
    <author><name>{html.escape(AUTHOR)}</name></author>
    <dc:language>es</dc:language>
    <summary>{html.escape(e['summary'])}</summary>
    <link rel="http://opds-spec.org/acquisition" href="{url}" type="{e['mime']}"/>
  </entry>""")
    feed = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/terms/" xmlns:opds="http://opds-spec.org/2010/catalog">
  <id>urn:pedidos:catalogo</id>
  <title>{html.escape(FEED_TITLE)}</title>
  <updated>{now}</updated>
  <author><name>{html.escape(AUTHOR)}</name></author>
  <link rel="self" href="{BASE_URL}/opds.xml" type="application/atom+xml;profile=opds-catalog;kind=acquisition"/>
  <link rel="start" href="{BASE_URL}/opds.xml" type="application/atom+xml;profile=opds-catalog;kind=acquisition"/>
{chr(10).join(entries)}
</feed>
"""
    (ROOT / "opds.xml").write_text(feed, encoding="utf-8")

    rows = "".join(
        f'<li><a href="archivos/{d}">{html.escape(index[d]["title"])}</a></li>'
        for d in sorted(index, reverse=True))
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(FEED_TITLE)}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:40rem;margin:2rem auto;padding:0 1rem;line-height:1.5}}</style>
</head><body>
<h1>{html.escape(FEED_TITLE)}</h1>
<p>Catálogo OPDS para KOReader: <code>{BASE_URL}/opds.xml</code></p>
<ul>{rows}</ul>
</body></html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def save(index: dict):
    INDEX_JSON.parent.mkdir(parents=True, exist_ok=True)
    INDEX_JSON.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    write_catalog(index)
    (ROOT / ".nojekyll").touch()


def main():
    args = sys.argv[1:]
    if not args or len(args) > 2:
        sys.exit(__doc__)
    index = json.loads(INDEX_JSON.read_text(encoding="utf-8")) if INDEX_JSON.exists() else {}
    now = dt.datetime.now(ART).isoformat(timespec="seconds")

    if args[0] == "--quitar":
        name = Path(args[1]).name
        if name not in index:
            sys.exit(f"{name} no está en el catálogo")
        index.pop(name)
        (OUT_DIR / name).unlink(missing_ok=True)
        (SRC_DIR / f"{Path(name).stem}.md").unlink(missing_ok=True)
        save(index)
        print(f"OK: quitado {name} — {len(index)} archivos en el catálogo")
        return

    src = Path(args[0]).resolve()
    stem, ext = src.stem, src.suffix.lower()
    if not re.fullmatch(NAME_RE, stem):
        sys.exit("El archivo tiene que llamarse AAAA-MM-DD-tema.ext "
                 "(tema en minúsculas, sin acentos, con guiones)")

    if src.parent == SRC_DIR and ext == ".md":
        title, intro, sections = parse_edition(src.read_text(encoding="utf-8"))
        name = f"{stem}.epub"
        build_epub(stem, title, intro, sections, OUT_DIR / name)
        summary = "Capítulos: " + " · ".join(s["title"] for s in sections)
    elif src.parent == OUT_DIR:
        if ext not in MIME:
            sys.exit(f"Formato no soportado: {ext} (soportados: {', '.join(MIME)})")
        if not src.exists():
            sys.exit(f"No existe {src}")
        name = src.name
        title = args[1] if len(args) == 2 else stem[11:].replace("-", " ").capitalize()
        summary = f"Archivo {ext[1:].upper()}"
    else:
        sys.exit("Pasá un .md de pedidos/ o un archivo ya guardado en archivos/")

    if len(args) == 2 and ext == ".md":
        title = args[1]
    index[name] = {"title": title, "summary": summary, "mime": MIME[Path(name).suffix],
                   "updated": now}
    save(index)
    print(f"OK: archivos/{name} — {len(index)} archivos en el catálogo")


if __name__ == "__main__":
    main()

import csv
from pathlib import Path

INPUT_CSV     = "Urls.MyHammer.csv"
URLS_PER_PAGE = 500   # 100k URLs -> 200 Seiten

urls = []
with open(INPUT_CSV, newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        if not row:
            continue
        cell = row[0].strip()
        if cell.startswith("http"):
            urls.append(cell)

total = len(urls)
pages = (total + URLS_PER_PAGE - 1) // URLS_PER_PAGE
print(f"{total} URLs -> {pages} Seiten")

def nav(current, total_pages):
    parts = []
    if current > 1:
        parts.append(f'<a href="page-{current-1}.html">&laquo; zurueck</a>')
    if current < total_pages:
        parts.append(f'<a href="page-{current+1}.html">weiter &raquo;</a>')
    return " | ".join(parts)

TEMPLATE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<title>MyHammer URLs - Seite {page}/{pages}</title></head>
<body>
<h1>MyHammer URLs - Seite {page} von {pages}</h1>
<ul>
{links}
</ul>
<nav>{nav}</nav>
</body></html>
"""

for i in range(pages):
    page_num = i + 1
    chunk = urls[i*URLS_PER_PAGE:(i+1)*URLS_PER_PAGE]
    links = "\n".join(
        f'  <li><a class="company-url" href="{u}">{u}</a></li>' for u in chunk
    )
    html = TEMPLATE.format(page=page_num, pages=pages, links=links,
                           nav=nav(page_num, pages))
    Path(f"page-{page_num}.html").write_text(html, encoding="utf-8")

Path("index.html").write_text(
    f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>MyHammer URLs</title></head><body>
<h1>MyHammer URLs</h1>
<p>{total} URLs auf {pages} Seiten.</p>
<p><a href="page-1.html">Zur ersten Seite &rarr;</a></p>
</body></html>""",
    encoding="utf-8",
)
print(f"Fertig: {pages} Seiten + index.html geschrieben.")

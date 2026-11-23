"""Cetak HTML notebook ke PDF ukuran A4 dengan Chrome headless.

Chrome tidak punya flag ukuran kertas, jadi CSS @page disuntikkan dulu.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "output" / "reports" / "ModelANN_TubesAI.html"
TMP = ROOT / "output" / "reports" / "_print_a4.html"
OUT = ROOT / "output" / "reports" / "ModelANN_TubesAI.pdf"

CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

A4_CSS = """
<style>
@page { size: A4 portrait; margin: 12mm 10mm 12mm 10mm; }
@media print {
  body { margin: 0 !important; padding: 0 !important; }
  .jp-Notebook { padding: 0 !important; }
}
</style>
"""

html = SRC.read_text(encoding="utf-8")
assert "</head>" in html, "tag </head> tidak ditemukan"
html = html.replace("</head>", A4_CSS + "</head>", 1)
TMP.write_text(html, encoding="utf-8")

if OUT.exists():
    OUT.unlink()

cmd = [
    str(CHROME),
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    "--print-to-pdf=%s" % OUT,
    TMP.as_uri(),
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("returncode:", res.returncode)
if not OUT.exists():
    print(res.stdout[-800:])
    print(res.stderr[-800:])
    sys.exit(1)

from pypdf import PdfReader

r = PdfReader(OUT)
print("OK -> %s  (%.0f KB, %d halaman, %s)"
      % (OUT.name, OUT.stat().st_size / 1024, len(r.pages), r.pages[0].mediabox))

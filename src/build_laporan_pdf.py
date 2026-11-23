"""Build laporan/Laporan.md menjadi PDF sesuai format spesifikasi tugas.

Format wajib:
  - Font Times New Roman 12pt
  - Spasi 1,5
  - Margin: atas 2,5 cm, bawah 2,5 cm, kiri 3 cm, kanan 2,5 cm

Pipeline:
    Laporan.md -> sanitasi -> pandoc + xelatex -> Laporan.pdf

Jalankan dari folder root proyek:
    .venv\\Scripts\\python.exe src\\build_laporan_pdf.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_MD = ROOT / "laporan" / "Laporan.md"
OUT_PDF = ROOT / "laporan" / "Laporan.pdf"
TMP_MD = ROOT / "laporan" / "_Laporan_for_pdf.md"
COVER_TEX = ROOT / "laporan" / "_cover.tex"

# Simbol yang tidak bisa dirender xelatex dengan font Times New Roman
REPLACEMENTS = {
    "→": "->",
    "←": "<-",
    "✅": "[OK]",
    "❌": "[X]",
    "⚠️": "[!]",
    "⚠": "[!]",
}


def sanitize(text: str) -> str:
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    return text


def strip_manual_numbers(text: str) -> str:
    """Buang nomor bab/subbab manual dari heading.

    LaTeX (documentclass report, lang=id) sudah otomatis memberi nomor:
    '# Judul' -> 'Bab 1 Judul', '## Judul' -> '1.1 Judul'.
    Kalau heading sudah ditulis 'Bab 1. Judul', hasilnya jadi dobel
    ('Bab 1' lalu 'Bab 1. Judul'). Karena itu nomornya dibuang dulu.
    """
    # "# Bab 1. Pendahuluan"  ->  "# Pendahuluan"
    text = re.sub(r"^(#{1,6})\s+Bab\s+\d+\.\s*", r"\1 ", text, flags=re.MULTILINE)
    # "## 1.1. Pemahaman Dataset"  ->  "## Pemahaman Dataset"
    text = re.sub(r"^(#{1,6})\s+\d+(?:\.\d+)*\.?\s+", r"\1 ", text, flags=re.MULTILINE)
    return text


def main() -> int:
    if not SRC_MD.exists():
        print(f"ERROR: {SRC_MD} tidak ditemukan")
        return 1

    for tool in ("pandoc", "xelatex"):
        if shutil.which(tool) is None:
            print(f"ERROR: '{tool}' tidak ada di PATH.")
            return 1

    text = sanitize(SRC_MD.read_text(encoding="utf-8"))
    text = strip_manual_numbers(text)
    TMP_MD.write_text(text, encoding="utf-8")

    cmd = [
        "pandoc", str(TMP_MD),
        "-o", str(OUT_PDF),
        "--pdf-engine=xelatex",
        # --- format wajib dari spesifikasi ---
        "-V", "mainfont=Times New Roman",
        "-V", "fontsize=12pt",
        "-V", "linestretch=1.5",
        "-V", "geometry:a4paper",
        "-V", "geometry:top=2.5cm",
        "-V", "geometry:bottom=2.5cm",
        "-V", "geometry:left=3cm",
        "-V", "geometry:right=2.5cm",
        # --- tampilan ---
        "-V", "documentclass=report",
        "-V", "lang=id",
        "-V", "colorlinks=true",
        "-V", "linkcolor=black",
        "-V", "urlcolor=blue",
        "-V", "toccolor=black",
        "--toc",
        "--toc-depth=2",
        # Halaman judul dimasukkan lewat --include-before-body, sehingga
        # urutannya berada sebelum \tableofcontents yang dibuat pandoc.
        # Tidak bisa lewat metadata YAML karena pandoc menggabungkan seluruh
        # isi 'author' menjadi satu paragraf.
        "--include-before-body", str(COVER_TEX),
        # nomor bab/subbab dibuat otomatis oleh LaTeX (report + babel indonesian
        # menghasilkan "Bab 1", "1.1", dst.). Nomor manual di heading sudah
        # dibuang oleh strip_manual_numbers() agar tidak dobel.
        "--number-sections",
        # gambar dirujuk relatif terhadap folder laporan/, jadi tambahkan
        # folder itu ke resource path agar pandoc menemukan gambarnya
        "--resource-path=.;laporan",
    ]

    print("Membangun Laporan.pdf ...")
    res = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )

    if res.returncode != 0 or not OUT_PDF.exists():
        print("GAGAL membangun PDF.")
        print("--- stdout ---")
        print(res.stdout[-3000:])
        print("--- stderr ---")
        print(res.stderr[-3000:])
        return res.returncode or 1

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"OK -> {OUT_PDF}  ({size_kb:.1f} KB)")

    try:
        TMP_MD.unlink()
    except OSError:
        pass
    for leftover in ("Laporan.tex", "Laporan.aux", "Laporan.log", "Laporan.toc",
                     "Laporan.out"):
        p = ROOT / "laporan" / leftover
        if p.exists():
            p.unlink()

    return 0


if __name__ == "__main__":
    sys.exit(main())

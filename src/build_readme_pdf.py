"""Build README.md menjadi PDF yang rapi.

Pipeline:
    README.md  ->  sanitasi (emoji/simbol/box-drawing)  ->  pandoc + xelatex  ->  README.pdf

Jalankan dari folder root proyek:
    python src\\build_readme_pdf.py

Butuh: pandoc (>=3.0) dan xelatex (MiKTeX). Keduanya sudah terpasang.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_MD = ROOT / "README.md"
OUT_PDF = ROOT / "README.pdf"
TMP_MD = ROOT / "output" / "reports" / "_readme_for_pdf.md"

# Emoji/simbol -> teks aman (xelatex tidak bisa render emoji berwarna)
REPLACEMENTS = {
    "⚠️": "[PENTING]", "⚠": "[PENTING]",
    "✅": "[OK]", "❌": "[JANGAN]", "🔄": "[ULANG]",
    "ℹ️": "[INFO]", "ℹ": "[INFO]",
    "📖": "[BACA]", "⚙️": "[SETTING]", "⚙": "[SETTING]",
    "👉": "->", "→": "->", "←": "<-",
}

# Box-drawing (dipakai di pohon folder) -> ASCII
BOX = {
    "├": "|--", "└": "`--", "│": "|  ", "─": "-",
    "┬": "-", "┼": "-", "┐": "-", "┌": "-",
    "┘": "-", "┴": "-", "┤": "-", "═": "=",
}


def strip_emoji(text: str) -> str:
    out = []
    for ch in text:
        cp = ord(ch)
        if (
            0x1F000 <= cp <= 0x1FAFF      # emoji
            or 0x2600 <= cp <= 0x27BF     # simbol misc
            or 0x2B00 <= cp <= 0x2BFF
            or 0x1F1E6 <= cp <= 0x1F1FF   # flag
            or cp in (0xFE0F, 0x200D, 0x20E3)
        ):
            continue
        out.append(ch)
    return "".join(out)


def sanitize(text: str) -> str:
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    text = strip_emoji(text)
    for k, v in BOX.items():
        text = text.replace(k, v)
    # Anchor link internal (#...) tidak berguna di PDF -> jadikan teks biasa
    text = re.sub(r"\[([^\]]+)\]\(#[^)]*\)", r"\1", text)
    return text


def extract_title(text: str) -> tuple[str, str]:
    """Ambil H1 pertama sebagai judul dokumen, kembalikan (judul, sisa teks).

    Judul dipindah ke metadata pandoc supaya tidak muncul sebagai entri TOC.
    H1 di dalam blok kode (```) diabaikan, supaya komentar seperti '# 1. langkah'
    tidak salah terambil sebagai judul.
    """
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and stripped.startswith("# "):
            title = stripped[2:].strip()
            body = text.replace(line, "", 1)
            return title, body
    return "README", text


def drop_manual_toc(text: str) -> str:
    """Buang bagian '## Daftar Isi' buatan markdown.

    PDF memakai TOC otomatis dari pandoc yang sudah berisi nomor halaman,
    jadi TOC manual akan tampil ganda.
    """
    pattern = re.compile(
        r"^## Daftar Isi\s*$.*?(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", text, count=1)


def main() -> int:
    if not SRC_MD.exists():
        print(f"ERROR: {SRC_MD} tidak ditemukan")
        return 1

    for tool in ("pandoc", "xelatex"):
        if shutil.which(tool) is None:
            print(f"ERROR: '{tool}' tidak ada di PATH.")
            if tool == "pandoc":
                print("  Install: winget install JohnMacFarlane.Pandoc")
            else:
                print("  Install MiKTeX, lalu buka terminal baru.")
            return 1

    # utf-8-sig: buang BOM kalau ada, supaya regex '^# ' tetap cocok di baris 1
    text = sanitize(SRC_MD.read_text(encoding="utf-8-sig"))
    title, text = extract_title(text)
    text = drop_manual_toc(text)
    TMP_MD.parent.mkdir(parents=True, exist_ok=True)
    TMP_MD.write_text(text, encoding="utf-8")

    # Setelan blok kode: baris panjang dipecah, font diperkecil agar tidak
    # terpotong di tepi kanan halaman.
    header = TMP_MD.with_name("_readme_code.tex")
    header.write_text(
        "\\lstset{\n"
        "  breaklines=true,\n"
        "  breakatwhitespace=false,\n"
        "  columns=fullflexible,\n"
        "  basicstyle=\\ttfamily\\footnotesize,\n"
        "  keepspaces=true,\n"
        "  showstringspaces=false,\n"
        "}\n",
        encoding="utf-8",
    )

    cmd = [
        "pandoc", str(TMP_MD),
        "-o", str(OUT_PDF),
        "--pdf-engine=xelatex",
        "--metadata", f"title={title}",
        "--toc", "--toc-depth=2",
        "-V", "geometry:margin=2cm",
        "-V", "mainfont=Segoe UI",
        "-V", "monofont=Consolas",
        "-V", "fontsize=10pt",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "documentclass=article",
        "-V", "lang=id",
        "--listings",
        "--include-in-header", str(header),
    ]

    print("Membangun PDF...")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    if res.returncode != 0 or not OUT_PDF.exists():
        print("GAGAL membangun PDF.")
        print(res.stdout[-2000:])
        print(res.stderr[-2000:])
        return res.returncode or 1

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"OK -> {OUT_PDF}  ({size_kb:.1f} KB)")

    # Bersihkan file perantara
    try:
        TMP_MD.unlink()
    except OSError:
        pass
    for leftover in ("notebook.tex",):
        p = ROOT / leftover
        if p.exists():
            p.unlink()

    return 0


if __name__ == "__main__":
    sys.exit(main())

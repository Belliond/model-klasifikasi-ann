"""Perbaiki kernelspec Jupyter agar menunjuk ke lokasi .venv yang baru
setelah folder proyek di-rename.

Jalankan:  python src\\fix_kernel.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"

KERNEL_NAME = "tubes-ai"
DISPLAY_NAME = "Python (Tubes AI)"


def kernel_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA tidak ditemukan")
    return Path(appdata) / "jupyter" / "kernels" / KERNEL_NAME


def main() -> int:
    if not VENV_PY.exists():
        print(f"ERROR: python venv tidak ditemukan di {VENV_PY}")
        return 1

    kdir = kernel_dir()
    kdir.mkdir(parents=True, exist_ok=True)
    spec = kdir / "kernel.json"

    old_python = None
    if spec.exists():
        try:
            old_python = json.loads(spec.read_text(encoding="utf-8"))["argv"][0]
        except Exception:
            pass

    payload = {
        "argv": [
            str(VENV_PY),
            "-Xfrozen_modules=off",
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ],
        "display_name": DISPLAY_NAME,
        "language": "python",
        "metadata": {"debugger": True, "supported_encryption": ["curve"]},
        "kernel_protocol_version": "5.5",
    }

    spec.write_text(json.dumps(payload, indent=1), encoding="utf-8")

    print(f"Kernel spec : {spec}")
    if old_python and old_python != str(VENV_PY):
        print(f"  sebelumnya : {old_python}")
    print(f"  sekarang   : {VENV_PY}")
    print("OK - kernel diperbarui")
    return 0


if __name__ == "__main__":
    sys.exit(main())

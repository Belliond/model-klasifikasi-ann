# Panduan Environment — Model Klasifikasi Binary & Multiclass

Semua perkakas **sudah terpasang** di folder ini. Tidak perlu install apa pun lagi.

## Struktur Folder

```
Model Klasifikasi Binary & Multiclass/
├── .venv/                  Environment Python terisolasi (jangan diubah manual)
├── dataset/
│   ├── *.zip               Arsip asli (jangan dihapus, sebagai cadangan)
│   └── extracted/          Data siap pakai
│       ├── cdc_diabetes/       binary-class  (253.680 baris, 22 kolom)
│       ├── dry_bean/           multi-class   (13.611 baris, 16 kolom)
│       ├── obesity/            multi-class   (2.111 baris, 17 kolom)
│       ├── phishing_url/       binary-class  (235.795 baris, 56 kolom)
│       └── students_dropout/   multi-class   (4.424 baris, 37 kolom)
├── notebooks/              Notebook eksperimen (.ipynb)
├── src/                    Script Python bantu
├── output/
│   ├── figures/            Grafik & plot untuk laporan
│   ├── models/             Model tersimpan (.keras / .h5)
│   └── reports/            Hasil export PDF
├── laporan/                Laporan akhir (Word/LaTeX/PDF)
└── docs/                   Spesifikasi tugas
```

## Cara Menjalankan

### 1. Aktifkan environment

PowerShell:

```powershell
& ".\.venv\Scripts\Activate.ps1"
```

Kalau muncul error *"running scripts is disabled"*, jalankan sekali:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 2. Buka Jupyter

```powershell
jupyter lab
```

Saat membuat notebook baru, pilih kernel **"Python (Tubes AI)"**.

> Jangan pilih `python3` — itu kernel lain. Yang benar ada label "Tubes AI".

### 3. Export notebook ke PDF

```powershell
jupyter nbconvert --to pdf "notebooks\NAMA_NOTEBOOK.ipynb" --output-dir output\reports
```

Hasilnya masuk ke `output/reports/`.

## Perkakas Terpasang

| Kategori | Package | Versi |
|---|---|---|
| Data | pandas | 3.1.1 |
| Data | numpy | 2.5.5 |
| Data | openpyxl, xlrd | 3.1.5 / 2.0.2 |
| ML | scikit-learn | 1.9.1 |
| ML | imbalanced-learn (SMOTE) | 0.14.2 |
| ANN | TensorFlow | 2.21.0 |
| ANN | Keras | 3.15.1 |
| Visualisasi | matplotlib | 3.11.2 |
| Visualisasi | seaborn | 0.13.2 |
| Notebook | jupyterlab | 4.6.6 |
| Notebook | nbconvert | 7.17.2 |
| Pendukung | scipy, joblib, tqdm | — |
| PDF | pandoc | 3.14 |
| PDF | MiKTeX (xelatex) | — |

Cek sendiri kapan saja:

```powershell
python src\check_env.py
```

## Catatan Penting

**GPU tidak tersedia — dan itu tidak masalah.**
TensorFlow di Windows native memang CPU-only sejak versi 2.11. Untuk dataset tabular
seperti tugas ini, training MLP di CPU hanya butuh detik sampai beberapa menit.
Tidak perlu install CUDA.

**MiKTeX sudah diset auto-install.**
Kalau export PDF butuh package LaTeX baru, MiKTeX akan mengunduhnya otomatis
tanpa bertanya. Ini yang sebelumnya membuat export menggantung.

**Jangan install package ke Python global.**
Selalu gunakan `.venv`. Kalau perlu package baru:

```powershell
uv pip install NAMA_PACKAGE --python .venv\Scripts\python.exe
```

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `jupyter` tidak dikenali | Environment belum aktif. Jalankan `Activate.ps1`. |
| Kernel tidak muncul | Pilih "Python (Tubes AI)", atau jalankan ulang `jupyter lab`. |
| Export PDF gagal | Pastikan `xelatex` ada: `xelatex --version`. Jalankan dari folder root proyek. |
| Export PDF lama/menggantung | Cek tidak ada proses `xelatex` menggantung di Task Manager. |
| Library tidak ditemukan | Pastikan pakai `.venv\Scripts\python.exe`, bukan `python` global. |

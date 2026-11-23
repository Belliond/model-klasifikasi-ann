# Model Klasifikasi Binary & Multiclass — ANN

Proyek klasifikasi menggunakan Artificial Neural Network (ANN) pada dataset tabular,
dibangun dengan Python + TensorFlow/Keras.

**Mata kuliah:** Inteligensi Buatan — Semester Ganjil 2026/2027
**Institut Teknologi Sumatera — Teknik Informatika**

---

## Daftar Isi

1. [Ringkasan Tugas](#ringkasan-tugas)
2. [Struktur Folder](#struktur-folder)
3. [Apa itu `.venv`?](#apa-itu-venv)
4. [Cara Menjalankan](#cara-menjalankan)
5. [Penjelasan File](#penjelasan-file)
6. [Dataset](#dataset)
7. [Library Inti yang Dipakai](#library-inti-yang-dipakai)
8. [Perkakas Terpasang](#perkakas-terpasang)
9. [Troubleshooting](#troubleshooting)

---

## Ringkasan Tugas

| Komponen | Keterangan |
|---|---|
| Model | ANN (bukan LLM), klasifikasi |
| Dataset | 2 buah: 1 binary-class + 1 multi-class |
| Deliverable 1 | PDF hasil export `.ipynb` |
| Deliverable 2 | Laporan 4 bab (PDF) |
| Deliverable 3 | Video presentasi ≤15 menit di YouTube |
| Deadline | 12 Desember 2026, 23.59 WIB |

**Format laporan:** Times New Roman 12pt, spasi 1.5, margin Atas 2.5cm / Bawah 2.5cm / Kiri 3cm / Kanan 2.5cm

**Format penamaan file:**

- `NamaKelompok_NIM1_NIM2_NIM3_ModelANN.pdf`
- `NamaKelompok_NIM1_NIM2_NIM3_Laporan.pdf`

---

## Struktur Folder

```
Model Klasifikasi Binary & Multiclass/
├── README.md           Dokumentasi ini (versi teks)
├── README.pdf          Dokumentasi ini (versi PDF, untuk dibaca/dicetak)
├── .venv/              Environment Python terisolasi (JANGAN diubah manual)
├── dataset/            Data
│   ├── *.zip               Arsip asli — cadangan, jangan dihapus
│   └── extracted/          Data siap pakai (dibaca oleh kode)
├── notebooks/          Tempat kerja utama — file .ipynb
├── src/                Kode bantu yang dipakai ulang
├── output/             Hasil otomatis dari kode
│   ├── figures/            Grafik untuk laporan
│   ├── models/             Model tersimpan
│   └── reports/            Hasil export PDF
├── laporan/            Dokumen akhir yang dikumpulkan
└── docs/               Referensi & panduan
```

> 💡 **`README.pdf`** dibuat otomatis dari `README.md`. Setiap kali kamu mengubah
> `README.md`, jalankan `python src\build_readme_pdf.py` untuk memperbarui PDF-nya.

### Fungsi tiap folder

| Folder | Fungsi | Kamu sentuh? |
|---|---|---|
| `.venv/` | Menyimpan Python + semua library. Seperti "mesin" — dipakai, tidak dibuka. | ❌ Jangan |
| `dataset/` | Bahan mentah. `*.zip` = arsip asli, `extracted/` = yang dibaca kode. | 📖 Baca saja |
| `notebooks/` | **Tempat kerja utama.** Di sini kamu tulis kode, latih model, lihat grafik. | ✅ **Sering** |
| `src/` | Fungsi bantu (`utils.py`) supaya tidak nulis kode sama dua kali. | ⚙️ Kadang |
| `output/figures/` | Grafik tersimpan otomatis. Ambil dari sini untuk laporan. | ✅ **Sering** |
| `output/models/` | Model hasil training (`.keras`). | 📖 Baca saja |
| `output/reports/` | PDF hasil export notebook. | 📖 Baca saja |
| `laporan/` | File laporan akhir (Word/LaTeX/PDF). | ✅ **Sering** |
| `docs/` | Spesifikasi dari dosen + panduan environment. | 📖 Baca saja |

> **Sehari-hari kamu hanya perlu buka 2 folder:** `notebooks/` dan `output/figures/`.
> Sisanya berjalan otomatis atau dibuka sekali-sekali saja.

---

## Apa itu `.venv`?

`.venv` adalah singkatan dari **Virtual Environment** (lingkungan virtual Python).

### Masalah yang diselesaikan

Bayangkan kamu punya proyek lain yang butuh `numpy` versi lama, sedangkan tugas ini
butuh `numpy` versi baru. Kalau semua library diinstall ke **satu** Python global,
kedua proyek akan saling menimpa dan rusak.

Virtual environment menyelesaikannya: setiap proyek punya **Python dan library sendiri
yang terisolasi**.

### Isi `.venv`

| Item | Isi |
|---|---|
| Ukuran | ± **2 GB** |
| Jumlah file | ± **39.400** file |
| Jumlah package | **143** (termasuk dependensi otomatis) |
| `Lib/` | Semua library (TensorFlow, pandas, matplotlib, dll) |
| `Scripts/` | Executable: `python.exe`, `jupyter.exe`, `jupyter-lab.exe` |
| `pyvenv.cfg` | Metadata: Python 3.12.10, dibuat oleh `uv` |
| `include-system-site-packages = false` | Artinya **terisolasi penuh** dari Python global |

> ℹ️ **`.venv` ini tidak punya `pip`.** Itu normal — `uv` sengaja tidak memasang pip
> karena `uv pip` lebih cepat. Jadi perintah `python -m pip ...` akan error
> *"No module named pip"*. Gunakan `uv pip` sebagai gantinya (lihat di bawah).

### Kenapa ukurannya besar?

Karena TensorFlow sendirian sudah ±600 MB (dia bawa library komputasi numerik +
dukungan CPU). Total 2 GB itu normal untuk proyek deep learning.

### Aturan penting

✅ **Boleh:** pakai, aktifkan, install library baru ke dalamnya
❌ **Jangan:** hapus isinya satu per satu, atau edit file di dalamnya manual
🔄 **Kalau rusak:** hapus seluruh folder `.venv`, lalu buat ulang (perintah di bawah)

### Cara membuat ulang kalau rusak

```powershell
uv venv .venv --python 3.12
uv pip install pandas numpy scikit-learn matplotlib seaborn tensorflow jupyter `
  ipykernel nbconvert nbformat jupyterlab imbalanced-learn openpyxl xlrd scipy `
  joblib tqdm --python .venv\Scripts\python.exe
```

### Cara install package baru

Karena tidak ada `pip`, gunakan `uv`:

```powershell
uv pip install NAMA_PACKAGE --python .venv\Scripts\python.exe
```

Untuk melihat semua package yang terpasang:

```powershell
uv pip list --python .venv\Scripts\python.exe
```

---

## Cara Menjalankan

### 1. Buka terminal di folder proyek

```powershell
cd "C:\Knowledge\Intelegensi Buatan\Model Klasifikasi Binary & Multiclass"
```

### 2. Aktifkan environment

```powershell
& ".\.venv\Scripts\Activate.ps1"
```

Kalau muncul error *"running scripts is disabled on this system"*, jalankan **sekali saja**:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Tanda berhasil: ada tulisan `(.venv)` di depan prompt terminal.

### 3. Jalankan Jupyter

```powershell
jupyter lab
```

> ⚠️ **Penting:** saat membuat notebook baru, pilih kernel **"Python (Tubes AI)"**.
> Jangan pilih `python3` — itu kernel lain dan TensorFlow tidak akan terbaca.

### 4. Export notebook ke PDF

```powershell
jupyter nbconvert --to pdf "notebooks\NAMA_NOTEBOOK.ipynb" --output-dir output\reports
```

### 5. Cek kesehatan environment (opsional)

```powershell
python src\check_env.py
```

---

## Penjelasan File

### `src/utils.py` — fungsi bantu

Kumpulan fungsi yang dipakai bersama oleh notebook binary-class dan multi-class,
supaya preprocessing, plotting, dan evaluasi hasilnya konsisten.

**Cara pakai di notebook:**

```python
import sys
sys.path.insert(0, "../src")
import utils
```

#### Konstanta path

| Nama | Isi |
|---|---|
| `utils.ROOT` | Path folder proyek |
| `utils.DATASET_DIR` | `dataset/extracted/` |
| `utils.FIGURES_DIR` | `output/figures/` |
| `utils.MODELS_DIR` | `output/models/` |
| `utils.REPORTS_DIR` | `output/reports/` |
| `utils.DATA_PATHS` | Dict path semua dataset (lihat tabel [Dataset](#dataset)) |
| `utils.PHISHING_DROP_COLS` | Kolom teks phishing yang wajib dibuang |

#### Fungsi visualisasi

| Fungsi | Kegunaan |
|---|---|
| `set_style()` | Set gaya plot seragam (dipanggil sekali di awal notebook) |
| `save_fig(name, fig=None)` | Simpan grafik ke `output/figures/` |
| `plot_class_distribution(y, title, name)` | Bar chart distribusi kelas + jumlah tiap kelas |
| `plot_training_history(history, name)` | Grafik loss & accuracy per epoch (train vs validation) |
| `plot_confusion_matrix(y_true, y_pred, labels, name, normalize)` | Confusion matrix, opsional dinormalisasi |
| `compare_experiments(rows, name)` | Bar chart perbandingan akurasi antar konfigurasi ANN |

#### Fungsi evaluasi

| Fungsi | Kegunaan |
|---|---|
| `evaluate(y_true, y_pred, y_proba, average)` | Hitung accuracy, precision, recall, F1, ROC-AUC → kembalikan dict |
| `print_report(y_true, y_pred, target_names)` | Classification report per kelas (tabel precision/recall/F1) |
| `save_metrics(metrics, name)` | Simpan metrik ke JSON di `output/reports/` |

**Contoh pemakaian lengkap:**

```python
import utils

utils.set_style()

# 1. Lihat distribusi kelas
utils.plot_class_distribution(y, "Distribusi Kelas Diabetes", "dist_diabetes")

# 2. Setelah training
utils.plot_training_history(history, "history_diabetes")

# 3. Evaluasi
y_pred  = (model.predict(X_test) > 0.5).astype(int).ravel()
y_proba = model.predict(X_test).ravel()
metrik  = utils.evaluate(y_test, y_pred, y_proba)

utils.plot_confusion_matrix(y_test, y_pred, name="cm_diabetes")
utils.print_report(y_test, y_pred)
utils.save_metrics(metrik, "metrik_diabetes")
```

### `src/check_env.py` — cek environment

Memverifikasi semua library bisa di-import dan menampilkan versinya.
Gunakan kalau curiga ada library yang rusak.

```powershell
python src\check_env.py
```

### `src/build_readme_pdf.py` — build README ke PDF

Mengubah `README.md` menjadi `README.pdf` (8 halaman, ada daftar isi + nomor halaman).
Script ini otomatis menangani emoji dan karakter kotak yang tidak bisa dirender xelatex.

```powershell
python src\build_readme_pdf.py
```

Jalankan setiap kali `README.md` diubah. Butuh `pandoc` dan `xelatex` — keduanya sudah terpasang.

### `src/smoke_test.py` — tes cepat dataset

Memuat CDC Diabetes dan Dry Bean, menampilkan shape, missing value, dan distribusi kelas.
Berguna untuk memastikan dataset terbaca sebelum mulai eksperimen.

```powershell
python src\smoke_test.py
```

### `docs/PANDUAN_ENVIRONMENT.md`

Panduan teknis environment: daftar package + versi, catatan GPU, dan troubleshooting.

### `docs/Spesifikasi Tugas Besar (UAS).pdf`

Spesifikasi resmi dari dosen. **Baca ini** untuk aturan pengumpulan.

---

## Dataset

Lima dataset tersedia, sudah diekstrak ke `dataset/extracted/`.

| Dataset | Baris | Kolom | Kelas | Tipe | Path (`utils.DATA_PATHS`) |
|---|---|---|---|---|---|
| CDC Diabetes | 253.680 | 22 | 2 (86,1% / 13,9%) | Binary | `cdc_diabetes_binary` |
| PhiUSIIL Phishing | 235.795 | 56 | 2 (57% / 43%) | Binary | `phishing_url` |
| Dry Bean | 13.611 | 17 | 7 (26% s.d. 3,8%) | Multi-class | `dry_bean` |
| Students Dropout | 4.424 | 37 | 3 (49,9/32,1/17,9) | Multi-class | `students_dropout` |
| Obesity | 2.111 | 17 | 7 (16,6% s.d. 12,9%) | Multi-class | `obesity` |

**Rekomendasi pasangan:** CDC Diabetes (binary) + Dry Bean (multi-class)
— keduanya sudah numerik penuh dan tanpa missing value, jadi bisa fokus ke eksplorasi arsitektur ANN.

### ⚠️ Jebakan dataset

**PhiUSIIL Phishing** punya kolom teks (`FILENAME`, `URL`, `Domain`, `TLD`, `Title`).
Kalau tidak dibuang, model bisa "curang" dan akurasi jadi ~100% tapi tidak bermakna.
Gunakan `utils.PHISHING_DROP_COLS` untuk membuangnya.

**CDC Diabetes** imbalance (86% vs 14%). Bahan diskusi yang bagus untuk SMOTE / `class_weight`.

**Dry Bean** punya kelas minoritas ekstrem (BOMBAY hanya 3,8%). Perhatikan F1-score per kelas,
bukan hanya akurasi.

---

## Library Inti yang Dipakai

Environment ini berisi **140 paket**, tapi yang benar-benar kamu tulis di notebook
hanya **7 library**. Sisanya (131 paket) adalah dependensi otomatis yang tidak pernah
kamu `import` langsung.

### 7 library yang kamu pakai

| Library | Cara import | Gunanya |
|---|---|---|
| **pandas** | `import pandas as pd` | Baca CSV/Excel, urus tabel data |
| **numpy** | `import numpy as np` | Hitung array & matriks |
| **scikit-learn** | `from sklearn...` | Split data, scaling, encoding, metrik evaluasi |
| **TensorFlow / Keras** | `import tensorflow as tf` | **Bangun & latih ANN-nya** |
| **matplotlib** | `import matplotlib.pyplot as plt` | Bikin grafik |
| **seaborn** | `import seaborn as sns` | Grafik yang lebih cantik |
| **imbalanced-learn** | `from imblearn...` | SMOTE untuk atasi data imbalance |

### Pendukung (bukan untuk koding model)

| Library | Gunanya |
|---|---|
| **openpyxl** | Baca Dry Bean dari `.xlsx` (tidak perlu kalau pakai `.arff`) |
| **nbconvert** | Export notebook `.ipynb` → PDF |

### Kalau disederhanakan lagi

Inti saripatinya sebenarnya **3 library**:

1. **pandas** → memasukkan data
2. **TensorFlow / Keras** → membuat model ANN
3. **scikit-learn** → mengukur hasilnya

Sisanya pelengkap. Kalau kamu paham tiga ini, tugasnya jalan.

### Pembagian 297 item di folder `site-packages`

Kalau kamu buka `.venv/Lib/site-packages`, Explorer menampilkan **297 item**.
Itu bukan 297 library — rinciannya:

| Jenis | Jumlah | Keterangan |
|---|---|---|
| Paket asli (kode) | 141 | folder berisi kode Python |
| Folder `.dist-info` | 140 | metadata paket (nama, versi, lisensi) |
| File lepas | 15 | `.pth`, `.pyd`, dll |
| **Total** | **297** | ← yang dilihat Explorer |

Setiap paket punya **2 folder**: kode + metadata. Contoh `imbalanced_learn-0.14.2.dist-info`
(metadata) dan `imblearn` (kode) adalah **satu paket yang sama**.

Jumlah paket sebenarnya adalah **140**, sesuai output `uv pip list`.

### Kenapa jadi 2 GB?

| Paket | Ukuran | Porsi |
|---|---|---|
| **tensorflow** | **1.404 MB** | **70%** |
| scipy | 94 MB | 5% |
| clang (dependensi TF) | 80 MB | 4% |
| pandas | 45 MB | 2% |
| sklearn | 33 MB | 2% |
| sisanya | ~380 MB | 17% |

TensorFlow sendirian menghabiskan 1.404 MB karena membawa library komputasi numerik
dalam satu paket. Ini normal untuk proyek deep learning.

### Jawaban kalau ditanya penguji

> "Untuk membangun ANN saya pakai **TensorFlow/Keras** karena menyediakan layer Dense,
> fungsi aktivasi, dan optimizer siap pakai. Untuk preprocessing dan evaluasi pakai
> **scikit-learn** — `train_test_split`, `StandardScaler`, dan `classification_report`.
> Data diolah dengan **pandas**, dan visualisasi pakai **matplotlib**."

Yang dinilai bukan panjang daftarnya, tapi apakah kamu tahu **kenapa** pakai tiap library.

---

## Perkakas Terpasang

| Kategori | Package | Versi |
|---|---|---|
| Data | pandas | 3.1.1 |
| Data | numpy | 2.5.5 |
| Data | openpyxl / xlrd | 3.1.5 / 2.0.2 |
| Data | scipy | 1.18.1 |
| ML | scikit-learn | 1.9.1 |
| ML | imbalanced-learn (SMOTE) | 0.14.2 |
| ANN | TensorFlow | 2.21.0 |
| ANN | Keras | 3.15.1 |
| Visualisasi | matplotlib | 3.11.2 |
| Visualisasi | seaborn | 0.13.2 |
| Notebook | jupyterlab | 4.6.6 |
| Notebook | nbconvert | 7.17.2 |
| Pendukung | joblib / tqdm | 1.6.0 / 4.70.1 |
| PDF | pandoc | 3.14 |
| PDF | MiKTeX (xelatex) | — |

### Catatan GPU

**GPU tidak tersedia — dan tidak dibutuhkan.**

TensorFlow di Windows native memang CPU-only sejak versi 2.11. Untuk dataset tabular
seperti tugas ini, training MLP di CPU hanya butuh detik sampai beberapa menit.
Tidak perlu install CUDA.

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `running scripts is disabled` | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `jupyter` tidak dikenali | Environment belum aktif — jalankan `Activate.ps1` |
| Kernel tidak muncul | Pilih **"Python (Tubes AI)"**, lalu restart Jupyter |
| `ModuleNotFoundError` | Pastikan pakai `.venv\Scripts\python.exe`, bukan `python` global |
| `No module named pip` | Normal. Gunakan `uv pip install ... --python .venv\Scripts\python.exe` |
| Export PDF gagal | Cek `xelatex --version`. Jalankan nbconvert dari folder root proyek |
| Export PDF menggantung | Cek Task Manager, matikan proses `xelatex` yang menggantung |
| Library rusak / aneh | `python src\check_env.py` untuk diagnosa |

---

## Aturan Main

1. **Jangan install package ke Python global.** Selalu ke `.venv`.
2. **Jangan hapus `dataset/*.zip`.** Itu arsip cadangan.
3. **Selalu pilih kernel "Python (Tubes AI)"** di Jupyter.
4. **Jalankan perintah dari folder root proyek**, bukan dari dalam `notebooks/`.
5. **Backup sebelum eksperimen besar.** Simpan model ke `output/models/`.

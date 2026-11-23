"""Utilitas umum untuk proyek Model Klasifikasi ANN.

Dipakai bersama oleh notebook binary-class dan multi-class supaya
preprocessing, plotting, dan evaluasi konsisten.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # aman untuk export PDF non-interaktif

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

# --------------------------------------------------------------------------
# Path
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset" / "extracted"
FIGURES_DIR = ROOT / "output" / "figures"
MODELS_DIR = ROOT / "output" / "models"
REPORTS_DIR = ROOT / "output" / "reports"

for _d in (FIGURES_DIR, MODELS_DIR, REPORTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Lokasi dataset (sudah diekstrak)
DATA_PATHS = {
    "cdc_diabetes_binary": DATASET_DIR / "cdc_diabetes" / "diabetes_binary_health_indicators_BRFSS2015.csv",
    "cdc_diabetes_multiclass": DATASET_DIR / "cdc_diabetes" / "diabetes_012_health_indicators_BRFSS2015.csv",
    "dry_bean": DATASET_DIR / "dry_bean" / "DryBeanDataset" / "Dry_Bean_Dataset.xlsx",
    "obesity": DATASET_DIR / "obesity" / "ObesityDataSet_raw_and_data_sinthetic.csv",
    "phishing_url": DATASET_DIR / "phishing_url" / "PhiUSIIL_Phishing_URL_Dataset.csv",
    "students_dropout": DATASET_DIR / "students_dropout" / "data.csv",
}

# Kolom teks pada dataset phishing yang WAJIB dibuang.
# Kalau dipakai, model bisa "curang" dan akurasi jadi ~100% tapi tidak bermakna.
PHISHING_DROP_COLS = ["FILENAME", "URL", "Domain", "TLD", "Title"]


# --------------------------------------------------------------------------
# Visualisasi
# --------------------------------------------------------------------------
def set_style() -> None:
    """Gaya plot seragam untuk semua gambar laporan."""
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
    })


def save_fig(name: str, fig=None) -> Path:
    """Simpan figure ke output/figures/ dan kembalikan path-nya."""
    fig = fig or plt.gcf()
    path = FIGURES_DIR / f"{name}.png"
    fig.savefig(path)
    return path


def plot_class_distribution(y, title: str, name: str):
    """Bar chart distribusi kelas + simpan."""
    counts = np.asarray(np.unique(y, return_counts=True)[1])
    labels = np.asarray(np.unique(y, return_counts=True)[0])
    fig, ax = plt.subplots(figsize=(7, 3.5))
    sns.barplot(x=[str(l) for l in labels], y=counts, ax=ax, color="#4C72B0")
    ax.set_title(title)
    ax.set_xlabel("Kelas")
    ax.set_ylabel("Jumlah sampel")
    for i, c in enumerate(counts):
        ax.text(i, c, f"{c:,}", ha="center", va="bottom", fontsize=8)
    save_fig(name, fig)
    plt.show()
    return fig


def plot_training_history(history, name: str = "training_history"):
    """Plot loss & accuracy per epoch (dari Keras history)."""
    h = history.history if hasattr(history, "history") else history
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].plot(h["loss"], label="Train")
    if "val_loss" in h:
        axes[0].plot(h["val_loss"], label="Validation")
    axes[0].set_title("Loss per Epoch")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()

    key = "accuracy" if "accuracy" in h else "acc"
    vkey = "val_accuracy" if "val_accuracy" in h else "val_acc"
    axes[1].plot(h[key], label="Train")
    if vkey in h:
        axes[1].plot(h[vkey], label="Validation")
    axes[1].set_title("Accuracy per Epoch")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].legend()

    fig.tight_layout()
    save_fig(name, fig)
    plt.show()
    return fig


def plot_confusion_matrix(y_true, y_pred, labels=None, name="confusion_matrix",
                          normalize=None):
    """Confusion matrix + simpan."""
    cm = confusion_matrix(y_true, y_pred, normalize=normalize)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    disp = ConfusionMatrixDisplay(cm, display_labels=labels)
    disp.plot(ax=ax, cmap="Blues", colorbar=True, values_format=".2f" if normalize else "d")
    ax.set_title("Confusion Matrix" + (" (normalized)" if normalize else ""))
    plt.xticks(rotation=45, ha="right")
    save_fig(name, fig)
    plt.show()
    return fig


# --------------------------------------------------------------------------
# Evaluasi
# --------------------------------------------------------------------------
def evaluate(y_true, y_pred, y_proba=None, average="binary") -> dict:
    """Hitung metrik utama dan kembalikan sebagai dict."""
    out = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
    }
    if y_proba is not None:
        try:
            if average == "binary":
                out["roc_auc"] = float(roc_auc_score(y_true, y_proba))
            else:
                out["roc_auc_ovr"] = float(roc_auc_score(y_true, y_proba,
                                                         multi_class="ovr", average="macro"))
        except ValueError:
            pass
    return out


def print_report(y_true, y_pred, target_names=None) -> str:
    """Classification report (precision/recall/f1 per kelas)."""
    rep = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
    print(rep)
    return rep


def save_metrics(metrics: dict, name: str) -> Path:
    """Simpan metrik ke JSON supaya bisa dibandingkan antar eksperimen."""
    path = REPORTS_DIR / f"{name}.json"
    path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def compare_experiments(rows, name="perbandingan_model"):
    """Tabel perbandingan hasil beberapa konfigurasi ANN.

    rows: list of dict, misal
        [{"nama": "Baseline", "hidden": "64", "akurasi": 0.91}, ...]
    """
    import pandas as pd

    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(max(6, len(df) * 1.4), 3.8))
    sns.barplot(data=df, x=df.columns[0], y="akurasi", ax=ax, color="#55A868")
    ax.set_title("Perbandingan Akurasi antar Konfigurasi")
    ax.set_ylim(0, 1)
    for i, v in enumerate(df["akurasi"]):
        ax.text(i, v, f"{v:.3f}", ha="center", va="bottom", fontsize=8)
    plt.xticks(rotation=20, ha="right")
    save_fig(name, fig)
    plt.show()
    return df

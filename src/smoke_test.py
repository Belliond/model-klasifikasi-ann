"""Uji cepat: dua dataset rekomendasi bisa dimuat dan siap dilatih."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import utils

print("=" * 70)
print("1. CDC DIABETES (binary-class)")
print("=" * 70)
df = pd.read_csv(utils.DATA_PATHS["cdc_diabetes_binary"])
print(f"shape          : {df.shape}")
print(f"missing value  : {int(df.isna().sum().sum())}")
print(f"kolom non-angka: {list(df.select_dtypes(exclude='number').columns) or 'tidak ada'}")
print(f"distribusi target:")
print(df["Diabetes_binary"].value_counts().to_string())

print()
print("=" * 70)
print("2. DRY BEAN (multi-class)")
print("=" * 70)
bean = pd.read_excel(utils.DATA_PATHS["dry_bean"])
print(f"shape          : {bean.shape}")
print(f"missing value  : {int(bean.isna().sum().sum())}")
print(f"kolom non-angka: {list(bean.select_dtypes(exclude='number').columns) or 'tidak ada'}")
print(f"distribusi target:")
print(bean["Class"].value_counts().to_string())

print()
print("=" * 70)
print("3. CEK FAST FAIL: apakah siap dilatih")
print("=" * 70)
X = df.drop(columns=["Diabetes_binary"]).astype("float32").values
y = df["Diabetes_binary"].astype(int).values
print(f"X: {X.shape}, dtype={X.dtype}, NaN={pd.isna(X).any()}")
print(f"y: {y.shape}, kelas={sorted(set(y.tolist()))}")

import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X.shape[1],)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.summary()
print("\nSEMUA SIAP. Dataset dan TensorFlow berfungsi.")

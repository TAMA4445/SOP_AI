"""Evaluasi model di test set. Jalankan dari root repo: py ml\\evaluate.py"""
import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             f1_score, precision_recall_fscore_support)

BASE = Path(__file__).resolve().parent
model = joblib.load(BASE / "model.joblib")
test = pd.read_csv(BASE / "data" / "test.csv")
train = pd.read_csv(BASE / "data" / "train.csv")

X, y = test["description"], test["label"]
classes = list(model.classes_)
pred = model.predict(X)

# Baseline: selalu tebak kelas mayoritas di train
majority = train["label"].value_counts().idxmax()
base_pred = [majority] * len(y)

cm = confusion_matrix(y, pred, labels=classes)
p, r, f1, sup = precision_recall_fscore_support(y, pred, labels=classes, zero_division=0)

# Akurasi toleransi +-1 level (level berurutan)
idx = {c: i for i, c in enumerate(classes)}
within1 = float(np.mean([abs(idx[a] - idx[b]) <= 1 for a, b in zip(y, pred)]))

metrics = {
    "n_test": int(len(y)),
    "accuracy": float(accuracy_score(y, pred)),
    "f1_macro": float(f1_score(y, pred, average="macro", zero_division=0)),
    "f1_weighted": float(f1_score(y, pred, average="weighted", zero_division=0)),
    "accuracy_within_1_level": within1,
    "baseline_majority_class": majority,
    "baseline_accuracy": float(accuracy_score(y, base_pred)),
    "baseline_f1_macro": float(f1_score(y, base_pred, average="macro", zero_division=0)),
    "per_class": {
        c: {"precision": float(p[i]), "recall": float(r[i]),
            "f1": float(f1[i]), "support": int(sup[i])}
        for i, c in enumerate(classes)
    },
    "confusion_matrix": {"labels": classes, "matrix": cm.tolist()},
}

out = BASE / "reports"
out.mkdir(exist_ok=True)
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

fig, ax = plt.subplots(figsize=(5, 4))
ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(len(classes)), classes)
ax.set_yticks(range(len(classes)), classes)
ax.set_xlabel("Prediksi")
ax.set_ylabel("Aktual")
for i in range(len(classes)):
    for j in range(len(classes)):
        ax.text(j, i, cm[i, j], ha="center", va="center")
fig.tight_layout()
fig.savefig(out / "confusion_matrix.png", dpi=150)

print(json.dumps({k: v for k, v in metrics.items()
                  if k not in ("per_class", "confusion_matrix")}, indent=2))
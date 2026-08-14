"""
metrics.py — Cohen's kappa, weighted kappa, and confusion-matrix helpers
used to validate LLM annotations against the manually coded reference sample
(Table 1 / Figure 3 in the paper).
"""
from __future__ import annotations

import pandas as pd


def cohen_kappa(y1: list, y2: list, labels: list[str]) -> float:
    """Cohen's kappa for nominal categories."""
    n = len(y1)
    if n == 0:
        return float("nan")
    label_idx = {l: i for i, l in enumerate(labels)}
    k = len(labels)
    cm = [[0] * k for _ in range(k)]
    for a, b in zip(y1, y2):
        i, j = label_idx.get(a, -1), label_idx.get(b, -1)
        if i >= 0 and j >= 0:
            cm[i][j] += 1
    observed = sum(cm[i][i] for i in range(k)) / n
    row_sums = [sum(cm[i]) / n for i in range(k)]
    col_sums = [sum(cm[i][j] for i in range(k)) / n for j in range(k)]
    expected = sum(row_sums[i] * col_sums[i] for i in range(k))
    if expected == 1.0:
        return 1.0
    return (observed - expected) / (1.0 - expected)


def weighted_kappa(y1: list, y2: list, labels: list[str]) -> float:
    """Linear-weighted Cohen's kappa, respecting the ordinal label order."""
    n = len(y1)
    if n == 0:
        return float("nan")
    k = len(labels)
    label_idx = {l: i for i, l in enumerate(labels)}
    cm = [[0] * k for _ in range(k)]
    for a, b in zip(y1, y2):
        i, j = label_idx.get(a, -1), label_idx.get(b, -1)
        if i >= 0 and j >= 0:
            cm[i][j] += 1
    row_sums = [sum(cm[i]) for i in range(k)]
    col_sums = [sum(cm[i][j] for i in range(k)) for j in range(k)]
    num_obs = num_exp = 0.0
    for i in range(k):
        for j in range(k):
            w = abs(i - j) / (k - 1) if k > 1 else 0
            num_obs += w * cm[i][j]
            num_exp += w * row_sums[i] * col_sums[j] / n
    return 1.0 - (num_obs / num_exp) if num_exp else float("nan")


def confusion_matrix_df(y1: list, y2: list, labels: list[str]) -> pd.DataFrame:
    """Confusion matrix as a labeled DataFrame (rater 1 = rows, rater 2 = cols)."""
    k = len(labels)
    label_idx = {l: i for i, l in enumerate(labels)}
    cm = [[0] * k for _ in range(k)]
    for a, b in zip(y1, y2):
        i, j = label_idx.get(a, -1), label_idx.get(b, -1)
        if i >= 0 and j >= 0:
            cm[i][j] += 1
    return pd.DataFrame(cm, index=pd.Index(labels, name="manual"), columns=pd.Index(labels, name="LLM"))


def classification_metrics(y_true: list, y_pred: list, labels: list[str]) -> dict:
    """Precision / recall / F1 per label, treating y_true (manual) as gold standard."""
    from sklearn.metrics import classification_report

    report = classification_report(y_true, y_pred, labels=labels, zero_division=0, output_dict=True)
    empty = {"precision": 0.0, "recall": 0.0, "f1-score": 0.0, "support": 0}
    return {
        "macro_f1": report["macro avg"]["f1-score"],
        "weighted_f1": report["weighted avg"]["f1-score"],
        "per_class": {lbl: report.get(lbl, empty) for lbl in labels},
    }

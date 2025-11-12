#!/usr/bin/env python3
"""
Logistic regression baseline for the Arbolado Público Mendoza 2025 competition.

Builds a feature matrix with lightweight engineering, evaluates it with stratified
cross-validation, fits a regularised logistic regression using L-BFGS, and saves a
submission file with probabilities for `inclinacion_peligrosa`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit
from scipy.stats import rankdata


DATA_DIR = Path(__file__).resolve().parent
TRAIN_PATH = DATA_DIR / "arbolado-mza-dataset.csv" / "arbolado-mza-dataset.csv"
TEST_PATH = DATA_DIR / "arbolado-mza-dataset-test.csv" / "arbolado-mza-dataset-test.csv"
OUTPUT_PATH = DATA_DIR / "submission_logistic_regression.csv"


def preprocess_features(
    df: pd.DataFrame, *, reference_date: pd.Timestamp | None = None
) -> Tuple[pd.DataFrame, pd.Timestamp]:
    """Derive numeric features shared by train and test sets."""
    data = df.copy()
    data["ultima_modificacion"] = pd.to_datetime(
        data["ultima_modificacion"], format="%d/%m/%Y %H:%M"
    )
    if reference_date is None:
        reference_date = data["ultima_modificacion"].min()

    data["fecha_year"] = data["ultima_modificacion"].dt.year
    data["fecha_month"] = data["ultima_modificacion"].dt.month
    data["fecha_day"] = data["ultima_modificacion"].dt.day
    data["fecha_hour"] = data["ultima_modificacion"].dt.hour
    data["fecha_minute"] = data["ultima_modificacion"].dt.minute
    data["fecha_dayofweek"] = data["ultima_modificacion"].dt.dayofweek
    data["fecha_quarter"] = data["ultima_modificacion"].dt.quarter
    data["days_since"] = (
        data["ultima_modificacion"] - reference_date
    ).dt.total_seconds() / 86400.0

    altura_map = {
        "Muy bajo (1 - 2 mts)": 1.5,
        "Bajo (2 - 4 mts)": 3.0,
        "Medio (4 - 8 mts)": 6.0,
        "Alto (> 8 mts)": 9.0,
    }
    diametro_map = {"Chico": 0, "Mediano": 1, "Grande": 2}

    data["altura_num"] = data["altura"].map(altura_map)
    data["diametro_num"] = data["diametro_tronco"].map(diametro_map)

    # Additional ratios/interactions that help a linear model separate classes.
    data["circ_per_area"] = data["circ_tronco_cm"] / (data["area_seccion"] + 1e-6)
    data["circ_ratio"] = data["circ_tronco_cm"] / (data["diametro_num"] + 1)
    data["long_lat_product"] = data["long"] * data["lat"]
    data["long_lat_distance"] = np.sqrt((data["long"] + 68.85) ** 2 + (data["lat"] + 32.89) ** 2)
    data["lat_centered"] = data["lat"] + 32.89
    data["long_centered"] = data["long"] + 68.85

    data["seccion"] = data["seccion"].astype(str)

    data = data.drop(columns=["ultima_modificacion", "altura", "diametro_tronco"])
    return data, reference_date


def prepare_design_matrices(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return aligned matrices ready for modelling."""
    target = train_df["inclinacion_peligrosa"].to_numpy(dtype=float)

    train_ids = train_df["id"].to_numpy()
    test_ids = test_df["id"].to_numpy()

    train_features = train_df.drop(columns=["inclinacion_peligrosa", "id"])
    test_features = test_df.drop(columns=["id"])

    train_proc, ref_date = preprocess_features(train_features)
    test_proc, _ = preprocess_features(test_features, reference_date=ref_date)

    categorical_cols = ["especie", "nombre_seccion", "seccion"]
    combined = pd.concat([train_proc, test_proc], axis=0, ignore_index=True)
    combined = pd.get_dummies(combined, columns=categorical_cols, dtype=float)

    train_matrix = combined.iloc[: len(train_proc)].to_numpy(dtype=float)
    test_matrix = combined.iloc[len(train_proc) :].to_numpy(dtype=float)

    return train_matrix, target, test_matrix, train_ids, test_ids


def roc_auc_score(y_true: Sequence[float], y_score: Sequence[float]) -> float:
    """Compute the ROC AUC via Mann-Whitney U, handling ties."""
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    ranks = rankdata(y_score)
    pos_ranks = ranks[y_true == 1]
    n_pos = len(pos_ranks)
    n_neg = len(y_true) - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ValueError("ROC AUC is undefined when only one class is present.")
    return (pos_ranks.sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def stratified_kfold_indices(
    y: Sequence[float], *, n_splits: int = 5, random_state: int | None = None
) -> Iterable[Tuple[np.ndarray, np.ndarray]]:
    """Yield stratified folds implemented without scikit-learn."""
    rng = np.random.default_rng(random_state)
    y = np.asarray(y)
    unique_classes = np.unique(y)
    folds = [[] for _ in range(n_splits)]

    for cls in unique_classes:
        cls_idx = np.where(y == cls)[0]
        rng.shuffle(cls_idx)
        splits = np.array_split(cls_idx, n_splits)
        for fold_idx, split in enumerate(splits):
            folds[fold_idx].extend(split.tolist())

    indices = np.arange(len(y))
    for fold_idx in range(n_splits):
        test_idx = np.array(folds[fold_idx])
        train_mask = np.ones(len(y), dtype=bool)
        train_mask[test_idx] = False
        train_idx = indices[train_mask]
        yield train_idx, test_idx


def fit_logistic_regression(
    X: np.ndarray, y: np.ndarray, *, reg: float = 0.1, maxiter: int = 400
) -> np.ndarray:
    """Fit an L2-regularised logistic regression via L-BFGS."""
    n_features = X.shape[1]

    def objective(beta: np.ndarray) -> float:
        w = beta[:-1]
        b = beta[-1]
        logits = X @ w + b
        probs = expit(logits)
        loss = -np.mean(
            y * np.log(probs + 1e-12) + (1.0 - y) * np.log(1.0 - probs + 1e-12)
        )
        loss += 0.5 * reg * np.sum(w**2)
        return float(loss)

    def gradient(beta: np.ndarray) -> np.ndarray:
        w = beta[:-1]
        b = beta[-1]
        logits = X @ w + b
        probs = expit(logits)
        diff = probs - y
        grad_w = (X.T @ diff) / len(y) + reg * w
        grad_b = diff.mean()
        return np.concatenate([grad_w, [grad_b]])

    initial = np.zeros(n_features + 1)
    result = minimize(
        objective,
        initial,
        method="L-BFGS-B",
        jac=gradient,
        options={"maxiter": maxiter},
    )
    if not result.success:
        print(f"Optimization warning: {result.message}")
    return result.x


def predict_proba(beta: np.ndarray, X: np.ndarray) -> np.ndarray:
    """Return probabilities for the positive class."""
    weights = beta[:-1]
    bias = beta[-1]
    return expit(X @ weights + bias)


def cross_validate(
    X: np.ndarray, y: np.ndarray, *, reg: float = 0.1, n_splits: int = 5, seed: int = 42
) -> np.ndarray:
    """Compute stratified CV AUC scores with per-fold scaling."""
    scores: list[float] = []
    for fold, (train_idx, valid_idx) in enumerate(
        stratified_kfold_indices(y, n_splits=n_splits, random_state=seed), start=1
    ):
        X_train = X[train_idx]
        X_valid = X[valid_idx]
        y_train = y[train_idx]
        y_valid = y[valid_idx]

        mean = X_train.mean(axis=0)
        std = X_train.std(axis=0)
        std[std == 0] = 1.0

        X_train_std = (X_train - mean) / std
        X_valid_std = (X_valid - mean) / std

        beta = fit_logistic_regression(X_train_std, y_train, reg=reg, maxiter=400)
        preds = predict_proba(beta, X_valid_std)
        auc = roc_auc_score(y_valid, preds)
        scores.append(float(auc))
        print(f"Fold {fold} AUC: {auc:.4f}")
    return np.asarray(scores)


def main() -> None:
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train, y_train, X_test, train_ids, test_ids = prepare_design_matrices(
        train_df, test_df
    )

    print(f"Prepared {X_train.shape[0]} training rows with {X_train.shape[1]} features.")
    cv_scores = cross_validate(X_train, y_train, reg=0.1, n_splits=5, seed=42)
    print(f"Mean CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    full_mean = X_train.mean(axis=0)
    full_std = X_train.std(axis=0)
    full_std[full_std == 0] = 1.0

    X_train_std = (X_train - full_mean) / full_std
    X_test_std = (X_test - full_mean) / full_std

    beta = fit_logistic_regression(X_train_std, y_train, reg=0.1, maxiter=500)
    train_preds = predict_proba(beta, X_train_std)
    train_auc = roc_auc_score(y_train, train_preds)
    print(f"Train AUC: {train_auc:.4f}")

    test_preds = predict_proba(beta, X_test_std)
    submission = pd.DataFrame(
        {"id": test_ids, "inclinacion_peligrosa": test_preds.astype(float)}
    )
    submission.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved submission with {len(submission)} rows to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()

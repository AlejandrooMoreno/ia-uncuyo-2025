"""Random baseline classifier utilities for TP7 exercises."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd

DEFAULT_VALIDATION_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "arbolado-mendoza-dataset-validation.csv"
)


def add_prediction_probabilities(
    observations: pd.DataFrame, seed: Optional[int] = None
) -> pd.DataFrame:
    """Return a copy of `observations` with a random `prediction_prob` column.

    Each row receives an independent draw from U(0, 1). A deterministic `seed`
    can be provided to make the random sequence reproducible.
    """
    if not isinstance(observations, pd.DataFrame):
        raise TypeError("observations must be a pandas.DataFrame instance")

    rng = np.random.default_rng(seed)
    result = observations.copy()
    result["prediction_prob"] = rng.uniform(0.0, 1.0, len(result))
    return result


def random_classifier(observations: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `observations` with a binary `prediction_class` column.

    The function expects a column called `prediction_prob` filled with values in
    [0, 1]. Values above 0.5 are mapped to class 1, the rest to class 0.
    To be forgiving with small typos, a column named `predictions_prob` is also
    accepted as input.
    """
    if not isinstance(observations, pd.DataFrame):
        raise TypeError("observations must be a pandas.DataFrame instance")

    prob_column = "prediction_prob"
    if prob_column not in observations.columns:
        fallback_column = "predictions_prob"
        if fallback_column not in observations.columns:
            raise KeyError(
                "prediction_prob column not found. Ensure you call "
                "add_prediction_probabilities first."
            )
        prob_column = fallback_column

    result = observations.copy()
    result["prediction_class"] = (result[prob_column] > 0.5).astype(int)
    return result


def biggerclass_classifier(
    observations: pd.DataFrame,
    *,
    target_column: str = "inclinacion_peligrosa",
) -> pd.DataFrame:
    """Return a copy of `observations` predicting the majority class always.

    The majority is computed from `target_column`. In case of ties, the smallest
    class label returned by `Series.mode()` is used.
    """
    if not isinstance(observations, pd.DataFrame):
        raise TypeError("observations must be a pandas.DataFrame instance")
    if target_column not in observations.columns:
        raise KeyError(f"target column {target_column!r} not found in dataframe")

    result = observations.copy()
    majority_class = result[target_column].mode().iloc[0]
    result["prediction_class"] = majority_class
    return result


def load_validation_with_random_predictions(
    csv_path: Union[str, Path] = DEFAULT_VALIDATION_PATH,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """Load validation data and attach random probabilities and classes."""
    df = pd.read_csv(csv_path)
    df = add_prediction_probabilities(df, seed=seed)
    df = random_classifier(df)
    return df


__all__ = [
    "add_prediction_probabilities",
    "random_classifier",
    "load_validation_with_random_predictions",
    "biggerclass_classifier",
]

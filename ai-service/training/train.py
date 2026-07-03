"""
Training script for the readiness ensemble model.

Usage (from the ai-service/ directory):
    python -m training.train
    python -m training.train --n-samples 1500 --seed 7

Generates a synthetic training dataset (see generate_synthetic_data.py),
fits the ensemble architecture already defined in
app.ml.readiness_model.build_ensemble() (reused as-is, not redefined
here), evaluates it on a held-out split, and persists the fitted model
to app.ml.readiness_model.MODEL_PATH - the exact path ReadinessModel
already checks on startup (Part 3), so no other code needs to change
for the trained model to start being used automatically.

This bootstraps the model on SYNTHETIC data because no real,
outcome-labeled learner history exists yet. Once real data is available
(e.g. aggregated from AssessmentResult/Progress once a future Spring
Boot integration part starts exporting it), only
load_training_data() below needs to change - train_model(),
save_model(), and everything in app/ml/ stays the same.
"""

import argparse
import logging
from pathlib import Path
from typing import List, Tuple

import joblib
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from app.ml.readiness_model import MODEL_PATH, build_ensemble
from training.generate_synthetic_data import generate_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_training_data(n_samples: int, seed: int) -> Tuple[List[List[float]], List[float]]:
    """
    Returns the (X, y) training data.

    Currently backed by the synthetic generator. Swap this function's
    body for a real data loader once historical outcome data exists -
    train_model()/save_model() are agnostic to where the data came from.
    """
    logger.info("Loading training data (synthetic, n_samples=%d, seed=%d)", n_samples, seed)
    return generate_dataset(n_samples=n_samples, seed=seed)


def train_model(X, y, test_size: float, seed: int):
    """Fits the existing ensemble blueprint and evaluates it on a held-out split."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )

    model = build_ensemble()
    logger.info("Fitting ensemble on %d training samples...", len(X_train))
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "mae": mean_absolute_error(y_test, predictions),
        "r2": r2_score(y_test, predictions),
        "n_train": len(X_train),
        "n_test": len(X_test),
    }
    logger.info(
        "Held-out evaluation (synthetic data) - MAE: %.4f, R^2: %.4f",
        metrics["mae"], metrics["r2"],
    )

    return model, metrics


def save_model(model, path: Path = MODEL_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    logger.info("Saved trained model to %s", path)


def parse_args():
    parser = argparse.ArgumentParser(description="Train the LearnPath AI readiness ensemble model.")
    parser.add_argument("--n-samples", type=int, default=800, help="Number of synthetic samples to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--test-size", type=float, default=0.2, help="Held-out evaluation fraction")
    return parser.parse_args()


def main():
    args = parse_args()
    X, y = load_training_data(n_samples=args.n_samples, seed=args.seed)
    model, metrics = train_model(X, y, test_size=args.test_size, seed=args.seed)
    save_model(model)
    logger.info("Training complete. Metrics: %s", metrics)
    logger.warning(
        "NOTE: this model was trained on SYNTHETIC data, not real learner "
        "outcomes. Treat readiness scores as illustrative until retrained "
        "on real historical data."
    )


if __name__ == "__main__":
    main()

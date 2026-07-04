"""
Training script for the study-image classifier.

Usage (from the ai-service/ directory):
    python -m app.dl.train
    python -m app.dl.train --epochs 15 --batch-size 32

STATUS: BOOTSTRAP / PLACEHOLDER PIPELINE - NOT YET RUNNABLE.
No real study-image dataset exists yet. This script is a complete,
correct training pipeline that will work as soon as real images are
placed in the documented folder structure below. Unlike the readiness
model's synthetic tabular data (Part 4), there is no honest way to
synthesize a picture that "looks like a Java diagram" without real
source images - so this script does NOT fabricate or download any
images itself.

Expected data layout (see app/dl/data/README.md for full detail):

    app/dl/data/
        Java/          *.jpg / *.png images about Java
        Database/      *.jpg / *.png images about databases
        Cloud/         *.jpg / *.png images about cloud computing
        Networking/    *.jpg / *.png images about networking
        Security/      *.jpg / *.png images about security
        Other/         *.jpg / *.png images that don't fit the above

Running this script today, with those folders empty, exits early with a
clear, actionable message rather than crashing with a confusing
TensorFlow error or silently "training" on nothing.
"""

import argparse
import logging
from pathlib import Path

import tensorflow as tf

from app.dl.model import CATEGORIES, MODEL_PATH, build_model
from app.dl.preprocessing import IMAGE_SIZE

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"
MIN_IMAGES_PER_CATEGORY = 10  # a bare minimum to attempt a meaningful fine-tune


def _dataset_is_ready(data_dir: Path) -> bool:
    """
    Checks whether enough real images exist to train on, instead of
    letting tf.keras.utils.image_dataset_from_directory fail with a
    confusing error on an empty/missing directory.
    """
    if not data_dir.exists():
        logger.error("Data directory %s does not exist. See app/dl/data/README.md.", data_dir)
        return False

    missing_or_empty = {}
    for category in CATEGORIES:
        category_dir = data_dir / category
        image_count = 0
        if category_dir.exists():
            image_count = sum(
                1 for p in category_dir.iterdir()
                if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
            )
        if image_count < MIN_IMAGES_PER_CATEGORY:
            missing_or_empty[category] = image_count

    if missing_or_empty:
        logger.error(
            "Not enough training images yet. Each category needs at least %d "
            "images; found: %s. See app/dl/data/README.md for the expected "
            "folder layout. Aborting - the untrained placeholder model will "
            "keep being served via the API until this is resolved.",
            MIN_IMAGES_PER_CATEGORY, missing_or_empty,
        )
        return False

    return True


def load_datasets(data_dir: Path, batch_size: int, validation_split: float, seed: int):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=IMAGE_SIZE,
        batch_size=batch_size,
        class_names=CATEGORIES,  # enforces our fixed label order
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=IMAGE_SIZE,
        batch_size=batch_size,
        class_names=CATEGORIES,
    )

    normalize = tf.keras.applications.mobilenet_v2.preprocess_input
    train_ds = train_ds.map(lambda x, y: (normalize(x), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (normalize(x), y)).prefetch(tf.data.AUTOTUNE)
    return train_ds, val_ds


def train_model(train_ds, val_ds, epochs: int):
    model = build_model()
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    logger.info("Training classification head (backbone frozen) for %d epochs...", epochs)
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)
    return model, history


def save_model(model, path: Path = MODEL_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    model.save(path)
    logger.info("Saved trained study-image classifier to %s", path)


def parse_args():
    parser = argparse.ArgumentParser(description="Train the LearnPath AI study-image classifier.")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--validation-split", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()

    if not _dataset_is_ready(DATA_DIR):
        return

    train_ds, val_ds = load_datasets(DATA_DIR, args.batch_size, args.validation_split, args.seed)
    model, history = train_model(train_ds, val_ds, args.epochs)
    save_model(model)

    final_val_acc = history.history.get("val_accuracy", [None])[-1]
    logger.info("Training complete. Final validation accuracy: %s", final_val_acc)


if __name__ == "__main__":
    main()

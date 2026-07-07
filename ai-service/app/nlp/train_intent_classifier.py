"""
Train the LearnPath AI Intent Classifier.

Fine-tunes DistilBERT on the synthetic intent dataset.

Run:

python -m app.nlp.train_intent_classifier
"""

from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from transformers import (
    AutoTokenizer,
    TFAutoModelForSequenceClassification,
)

from app.nlp.synthetic_intent_data import build_dataset, INTENTS

MODEL_NAME = "distilbert-base-uncased"

OUTPUT_DIR = (
    Path(__file__).parent /
    "models" /
    "intent_classifier"
)


def main():

    dataset = build_dataset()

    texts = [x["text"] for x in dataset]
    labels = [INTENTS.index(x["intent"]) for x in dataset]

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=64,
        return_tensors="tf",
    )

    x_train, x_test, y_train, y_test = train_test_split(
        dict(encodings),
        np.array(labels),
        test_size=0.20,
        random_state=42,
        stratify=labels,
    )

    model = TFAutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(INTENTS),
    )

    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(y_train),
        y=y_train,
    )

    class_weight = {
        i: weight
        for i, weight in enumerate(class_weights)
    }

    train_dataset = tf.data.Dataset.from_tensor_slices(
        (
            x_train,
            y_train,
        )
    ).shuffle(1000).batch(8)

    test_dataset = tf.data.Dataset.from_tensor_slices(
        (
            x_test,
            y_test,
        )
    ).batch(8)

    optimizer = tf.keras.optimizers.Adam(
        learning_rate=2e-5
    )

    loss = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True
    )

    metric = tf.keras.metrics.SparseCategoricalAccuracy()

    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=[metric],
    )

    model.fit(
        train_dataset,
        validation_data=test_dataset,
        epochs=3,
        class_weight=class_weight,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model.save_pretrained(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))

    print()
    print("=" * 60)
    print("Intent classifier saved to:")
    print(OUTPUT_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()
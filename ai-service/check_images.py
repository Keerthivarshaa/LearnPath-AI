import tensorflow as tf
import os

DATASET = "app/dl/data"

for root, dirs, files in os.walk(DATASET):
    for file in files:
        path = os.path.join(root, file)

        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        try:
            img = tf.io.read_file(path)
            tf.image.decode_image(img)
            print(f"OK: {path}")

        except Exception as e:
            print(f"\nBAD IMAGE: {path}")
            print(e)
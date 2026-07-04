"""
Standalone CLI for manually testing the study-image classifier outside
the FastAPI app - useful for a quick sanity check after training,
without needing to run the full service or craft an HTTP request.

Usage (from the ai-service/ directory):
    python -m app.dl.predict --image path/to/some_image.jpg
"""

import argparse
import json
from pathlib import Path

from app.dl.model import get_study_image_classifier


def parse_args():
    parser = argparse.ArgumentParser(description="Classify a study image from the command line.")
    parser.add_argument("--image", required=True, type=Path, help="Path to a local image file")
    return parser.parse_args()


def main():
    args = parse_args()
    image_bytes = args.image.read_bytes()

    classifier = get_study_image_classifier()
    result = classifier.predict(image_bytes)

    print(json.dumps(result, indent=2))
    if not classifier.is_using_trained_model:
        print(
            "\nNOTE: no trained model was found - this prediction came from an "
            "untrained MobileNetV2 placeholder head and is NOT meaningful. "
            "Run `python -m app.dl.train` after adding real images to "
            "app/dl/data/ first."
        )


if __name__ == "__main__":
    main()

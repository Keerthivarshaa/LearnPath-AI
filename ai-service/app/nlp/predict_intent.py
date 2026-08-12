"""
Standalone utility for testing the Intent Classifier.

Usage:
    python -m app.nlp.predict_intent

or

    python app/nlp/predict_intent.py
"""

from app.nlp.intent_classifier import IntentClassifier

def main():
    classifier = IntentClassifier()

    print("=" * 60)
    print("LearnPath AI - Intent Classifier")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        text = input("\nEnter learner message: ").strip()

        if text.lower() in ("exit", "quit"):
            print("Exiting...")
            break

        if not text:
            continue

        result = classifier.classify(text)

        print("\nPrediction")
        print("-" * 40)
        print(f"Intent      : {result['intent']}")
        print(f"Confidence  : {result['confidence']:.2f}")
        print(f"Source      : {result['modelSource']}")


if __name__ == "__main__":
    main()
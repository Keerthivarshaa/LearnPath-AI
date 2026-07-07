"""
Synthetic Intent Training Dataset
---------------------------------

Bootstraps the first version of the DistilBERT intent classifier.

Every example consists of:
    {
        "text": "...",
        "intent": "..."
    }

This dataset is intentionally synthetic because no real tutor-chat
history exists yet.

It is only used for initial fine-tuning and can later be replaced with
real conversations collected from the application.
"""

from typing import List, Dict

INTENTS = [
    "EXPLAIN_CONCEPT",
    "ASK_QUESTION",
    "CHECK_PROGRESS",
    "REQUEST_ROADMAP",
    "UPLOAD_IMAGE",
    "GREETING",
    "GOODBYE",
    "MOTIVATION",
    "GENERAL_CHAT",
    "UNKNOWN",
]


_BASE_EXAMPLES = {
    "EXPLAIN_CONCEPT": [
        "Explain IAM Security",
        "What is IAM?",
        "Teach me EC2",
        "Explain VPC",
        "Explain JDBC connection pool",
        "What is garbage collection?",
        "How does G1GC work?",
        "Explain cryptography",
        "Teach me SQL joins",
        "What is Azure Storage?",
        "Explain Azure Governance",
        "Explain Network Security",
        "What is Pattern Matching in Java?",
        "Can you explain read replicas?",
    ],

    "ASK_QUESTION": [
        "Why is EC2 used?",
        "Why do we use IAM roles?",
        "How does encryption work?",
        "When should I use Multi-AZ?",
        "What happens if GC fails?",
        "Can you answer this question?",
        "Why is VPC important?",
        "How is PostgreSQL different from MySQL?",
        "Why is hashing important?",
        "Can you solve this doubt?",
    ],

    "CHECK_PROGRESS": [
        "Show my progress",
        "How am I doing?",
        "Check my readiness",
        "Am I ready for certification?",
        "How much have I completed?",
        "What's my score?",
        "Show my weak topics",
        "Display my progress report",
        "How many milestones are left?",
        "Track my learning",
    ],

    "REQUEST_ROADMAP": [
        "Create a roadmap",
        "Generate my learning path",
        "Recommend what to study",
        "What should I learn next?",
        "Give me today's study plan",
        "Suggest next topics",
        "Plan my certification journey",
        "Prepare a roadmap",
        "Generate study schedule",
        "Recommend my next lesson",
    ],

    "UPLOAD_IMAGE": [
        "Analyze this image",
        "Read this screenshot",
        "Extract text from this photo",
        "Identify this diagram",
        "Analyze my notes",
        "Explain this image",
        "OCR this image",
        "Read my handwritten notes",
        "What is in this screenshot?",
        "Classify this study image",
    ],

    "GREETING": [
        "Hi",
        "Hello",
        "Hey",
        "Good morning",
        "Good evening",
        "Hi tutor",
        "Hello there",
        "Hey assistant",
    ],

    "GOODBYE": [
        "Bye",
        "See you",
        "Goodbye",
        "Catch you later",
        "Thanks bye",
        "Talk later",
    ],

    "MOTIVATION": [
        "Motivate me",
        "I feel tired",
        "Encourage me",
        "I want motivation",
        "Keep me focused",
        "I feel like giving up",
        "Can I do this?",
        "Boost my confidence",
    ],

    "GENERAL_CHAT": [
        "How are you?",
        "Tell me a joke",
        "What's your name?",
        "Who created you?",
        "Nice to meet you",
        "Tell me something interesting",
        "What can you do?",
        "Let's chat",
    ],

    "UNKNOWN": [
        "asdfgh",
        "qwerty",
        "123456",
        ".....",
        "random text",
        "nothing",
    ],
}


def build_dataset() -> List[Dict[str, str]]:
    """
    Returns a list of training examples.

    Additional phrasing variations are generated automatically so the
    classifier sees different sentence styles without manually writing
    hundreds of examples.
    """

    dataset: List[Dict[str, str]] = []

    prefixes = [
        "",
        "Please ",
        "Can you ",
        "Could you ",
        "Kindly ",
    ]

    suffixes = [
        "",
        " for me",
        " please",
        " now",
    ]

    for intent, examples in _BASE_EXAMPLES.items():
        for example in examples:
            for prefix in prefixes:
                for suffix in suffixes:
                    text = f"{prefix}{example}{suffix}".strip()

                    dataset.append({
                        "text": text,
                        "intent": intent,
                    })

    return dataset


if __name__ == "__main__":
    data = build_dataset()

    print("Total examples:", len(data))

    counts = {}

    for sample in data:
        counts[sample["intent"]] = counts.get(sample["intent"], 0) + 1

    print()

    for intent in sorted(counts):
        print(f"{intent:20} {counts[intent]}")
# Study Image Dataset

**Status: empty placeholder structure.** No real study images have been
collected yet - see `../train.py`'s module docstring for why this is
honestly left empty rather than filled with fabricated data.

## Expected layout

Place real images directly inside the matching category folder:

```
app/dl/data/
├── Java/          images related to Java (code, JVM diagrams, etc.)
├── Database/      images related to databases (schemas, SQL, etc.)
├── Cloud/         images related to cloud computing (AWS/Azure diagrams, etc.)
├── Networking/    images related to networking (VPC diagrams, OSI model, etc.)
├── Security/      images related to security (IAM, cryptography diagrams, etc.)
└── Other/         anything that doesn't fit the above categories
```

- Supported formats: `.jpg`, `.jpeg`, `.png`
- `train.py` requires **at least 10 images per category** before it will
  attempt training (a bare minimum, not a recommendation - real
  transfer-learning fine-tuning will need substantially more for a
  useful model; 10 is only the threshold below which `train.py` refuses
  to run rather than training on almost nothing).
- Once enough images exist in every category, run:
  ```
  cd ai-service
  python -m app.dl.train
  ```

Until then, `/ml/classify-study-image` continues to serve predictions
from an **untrained** MobileNetV2 placeholder head, clearly labeled via
`"modelSource": "untrained_placeholder"` in every response.

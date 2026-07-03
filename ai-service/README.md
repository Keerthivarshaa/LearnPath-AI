# LearnPath AI - ML Service

Internal FastAPI microservice providing AI/ML capabilities to the LearnPath AI
Spring Boot backend. Called server-to-server by Spring Boot; never called
directly by the React frontend.

Status: **Trained readiness model available (Level 1a - Part 4).**
`/ml/predict-readiness` now serves predictions from a fitted Random
Forest + Gradient Boosting ensemble (`model_source: "trained_ensemble"`),
bootstrapped on **synthetic** training data - see "Training" below.

## Run locally

```
cd ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Endpoints (current)

| Method | Path                    | Purpose                                             |
|--------|-------------------------|------------------------------------------------------|
| GET    | `/`                     | Service identity check                                |
| GET    | `/health`               | Liveness check                                         |
| POST   | `/ml/predict-readiness` | Predicts a 0-100 certification readiness score         |

## Training

No real, outcome-labeled learner history exists yet, so the model is
bootstrapped on a documented **synthetic** dataset (see
`training/generate_synthetic_data.py` for exactly how, and why the
synthetic labels are deliberately generated differently from the
fallback heuristic). Retrain with:

```
cd ai-service
python -m training.train                       # defaults: 800 samples, seed 42
python -m training.train --n-samples 1500 --seed 7
```

This writes `app/ml/models/readiness_ensemble.joblib`, which
`ReadinessModel` picks up automatically on the next process start - no
code changes needed. Prints held-out MAE/R² against the synthetic
labels; treat these as sanity metrics, not real-world accuracy, until
retrained on real data.

## Folder structure

```
ai-service/
├── main.py                          # FastAPI app entrypoint
├── requirements.txt
├── training/                        # offline training pipeline (not served by the API)
│   ├── generate_synthetic_data.py   # synthetic (features, target) dataset generator
│   └── train.py                     # fits build_ensemble(), evaluates, saves the model
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── health.py            # health/root routes
│   │       └── ml.py                # POST /ml/predict-readiness
│   ├── schemas/
│   │   └── readiness.py             # request/response contracts
│   └── ml/
│       ├── feature_engineering.py   # raw data -> ML-ready features
│       ├── readiness_model.py       # ReadinessModel (auto-loads a trained model if present)
│       └── models/
│           └── readiness_ensemble.joblib   # trained model artifact (gitignored)
```

## Roadmap for this service

1. ✅ Part 1 — FastAPI foundation, health endpoints
2. ✅ Part 2 — Feature engineering module
3. ✅ Part 3 — Readiness model + `/ml/predict-readiness` (fallback heuristic; ensemble architecture defined)
4. ✅ Part 4 — Training pipeline; ensemble now trained on synthetic data
5. ⬜ Part 5 — Spring Boot integration via `MLRoadmapGenerator`
6. ⬜ Part 6 — Frontend readiness score display

No Spring Boot or React code is modified as part of this service's setup.

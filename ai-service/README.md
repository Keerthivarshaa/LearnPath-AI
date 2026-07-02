# LearnPath AI - ML Service

Internal FastAPI microservice providing AI/ML capabilities to the LearnPath AI
Spring Boot backend. Called server-to-server by Spring Boot; never called
directly by the React frontend.

Status: **Foundation only (Level 1a - Part 1).** No ML logic is implemented yet.

## Run locally

```
cd ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Endpoints (current)

| Method | Path      | Purpose                    |
|--------|-----------|-----------------------------|
| GET    | `/`       | Service identity check      |
| GET    | `/health` | Liveness check               |

## Folder structure

```
ai-service/
├── main.py                          # FastAPI app entrypoint
├── requirements.txt
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── health.py            # health/root routes
│   └── ml/
│       ├── feature_engineering.py   # skeleton - implemented in Part 2
│       └── readiness_model.py       # skeleton - implemented in Part 3
```

## Roadmap for this service

1. ✅ Part 1 — FastAPI foundation, health endpoints
2. ⬜ Part 2 — Feature engineering module
3. ⬜ Part 3 — Ensemble readiness model + `/ml/predict-readiness`
4. ⬜ Part 4 — Spring Boot integration via `MLRoadmapGenerator`
5. ⬜ Part 5 — Frontend readiness score display

No Spring Boot or React code is modified as part of this service's setup.

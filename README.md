# TensorForge 2.0 - Phase 2 (MVP Stage)

**Team:** Cylix  
**Problem Statement:** Customer Support Ticket Classification and Routing

## Overview
This repository contains our end-to-end solution for Phase 2 of TensorForge 2.0. We have built a fully offline, high-speed, and robust machine learning pipeline to automatically classify and route multilingual customer support tickets. 

Our solution strictly adheres to the provided OpenAPI v2.1.0 contract and the No-LLM guidelines, ensuring sub-5ms latency and maximum data privacy.

## Live Links
* **Live Demo (Frontend):** [Insert Streamlit Link Here]
* **API Base URL (Backend):** [Insert Render Link Here]
* **Video Walkthrough:** [Insert YouTube Link Here]
* **Project Report:** [Insert Report PDF Link Here]

## Technology Stack
* **Backend:** FastAPI, Python 3.11, Pydantic, Uvicorn
* **Frontend:** Streamlit, HTML/CSS/JavaScript
* **Machine Learning:** scikit-learn, joblib
* **Deployment:** Docker, Render, Streamlit Community Cloud

## Machine Learning Architecture
Our classification pipeline uses a classical NLP approach to achieve **62.75% validation accuracy** on a highly imbalanced, code-mixed dataset containing Sinhala, English, Singlish, and Tanglish.
* **Feature Extraction:** A `FeatureUnion` combining word n-grams (1, 2) and sublinear character n-grams (2, 5). This architecture robustly handles misspellings and transliteration out-of-vocabulary tokens present in Singlish/Tanglish.
* **Classifier:** A `LinearSVC` with balanced class weights (`C=0.5`).
* **Confidence Calibration:** Decision function scores normalized via Softmax to output a 0-1 confidence score matching the OpenAPI schema constraints.

## How to Run Locally (Evaluation)
The backend service is fully containerized and does not require internet access at runtime.

### 1. Build the Docker Image
Navigate to the root directory containing the `Dockerfile` and run:
```bash
docker build -t rideeat-service .
```

### 2. Run the Container
Start the container using the exact evaluation command required by the guidelines:
```bash
docker run -p 8000:8000 -e API_KEY="your_api_key_here" rideeat-service
```
The API will be available at `http://localhost:8000`. You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

## Project Structure
```text
TensorForge/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI entry point & CORS configuration
│   │   ├── routers/       # Prediction and Batch Job API routes
│   │   ├── services/      # ML Inference service logic
│   │   ├── schemas.py     # Pydantic models matching OpenAPI specs
│   │   └── config.py      # Environment variable handling
│   └── requirements.txt   # Backend dependencies (fastapi, uvicorn, scikit-learn)
├── frontend/
│   ├── app.py             # Streamlit web application & UI
│   └── requirements.txt   # Frontend dependencies (streamlit)
├── ml/
│   ├── train.py           # Model training and feature extraction pipeline
│   ├── evaluate.py        # Validation and metric generation
│   ├── predict.py         # Testing script for offline inference
│   └── artifacts/         # Saved models (model.joblib, vectorizer.joblib)
├── Dockerfile             # Container configuration for the backend
└── README.md              # Project documentation
```

## Authors
**Team Cylix** - IEEE Computer Society KDU Hackathon Submission

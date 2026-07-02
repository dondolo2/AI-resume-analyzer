# Deployment Guide

## Streamlit Cloud (easiest)

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set **Main file path** to `streamlit_app.py`.
4. Add secrets if needed (optional `LOG_LEVEL`, `MAX_FILE_SIZE`).
5. Deploy. The app installs `requirements.txt` and exposes port 8501.

## Docker (local or any host)

```bash
docker build -t resume-match-ai .
docker run -p 8501:8501 resume-match-ai
```

Or with Compose:

```bash
docker compose up --build
```

Open http://localhost:8501

## Google Cloud Run

1. Build and push the image to Artifact Registry.
2. Deploy a Cloud Run service with port **8501**.
3. Set memory to at least **1 GiB** (spaCy model).
4. Allow unauthenticated access for a public demo, or restrict with IAM.

## AWS Elastic Beanstalk

1. Use the Docker platform with the provided `Dockerfile`.
2. Configure health check path: `/_stcore/health`
3. Set instance type with ≥ 2 GB RAM.

## Render / Railway

1. Create a new **Web Service** from the GitHub repo.
2. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
3. Start command: `streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`

## FastAPI (optional API only)

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

Health: `GET /health`  
Analyze: `POST /api/analyze` with JSON body `{ "resume_text": "...", "job_description": "..." }`

# GramaVoice

Production-focused **voice-first rural governance platform** built with Streamlit + FastAPI + ML modules.

## What is fixed in this build
- Hybrid **Voice + Text** input available at all times.
- Removed invalid Streamlit component usage that triggers `IframeMixin._html(... key=...)` crash.
- Added mobile-safe audio capture via `st.audio_input` fallback.
- Added mic permission-aware status and graceful fallback to text.
- Added safer no-crash processing around user actions.

## Core modules included
- Prediction Engine (complaint load forecasting)
- Sentiment + urgency inference
- Region analytics (district/village heatmap)
- Recommendation system (query-to-service ranking)
- Performance analytics
- Explainable AI panel (feature importance)
- User growth analytics
- Voice bot-like guided response flow

## Quick start
```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional backend:
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deliverables map
- Frontend code: `app.py`
- Backend API: `backend/app/main.py`
- API contracts: `API_CONTRACTS.md`
- Folder map: `FOLDER_STRUCTURE.md`
- Deployment guide: `DEPLOYMENT.md`
- Production checklist: `PRODUCTION_CHECKLIST.md`
- Requirements: `requirements.txt`

## Deployment notes
1. Deploy Streamlit frontend on Streamlit Cloud.
2. Deploy FastAPI backend on Render/AWS ECS/Fargate.
3. Configure env vars for STT provider and DB.
4. Route `/api/*` through HTTPS reverse proxy.
5. Enable logs + monitoring before go-live.

## Demo mode vs Production mode
- Current app includes deterministic demo-ready analytics for hackathon/pitch flows.
- Replace `transcribe_audio_bytes()` in `app.py` with Whisper/OpenAI/AWS STT integration for production speech transcription.

## National-scale architecture recommendations
- PostgreSQL for system-of-record.
- Redis for low-latency dashboard cache.
- Kafka/queue for async STT + notification jobs.
- JWT + RBAC + audit logs + rate limiting.
- Horizontal autoscaling for API and worker tiers.

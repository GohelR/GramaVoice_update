# GramaVoice Production Checklist

## Reliability
- [ ] `streamlit run app.py` launches with no red error trace.
- [ ] Voice + text hybrid input validated on desktop + Android Chrome.
- [ ] Mic permission denied path gracefully falls back to text.
- [ ] Audio upload path (`st.audio_input`) works on mobile.
- [ ] App logs rotated and retained (`loguru`).

## Security
- [ ] JWT auth enabled for non-demo environments.
- [ ] RBAC permissions tested for Admin/Operator/Citizen roles.
- [ ] Rate limiting enabled at API gateway/reverse proxy.
- [ ] Audit logs persisted (request id, actor, action, timestamp).
- [ ] Secrets managed via environment variables, never in repo.

## Data & Pipeline
- [ ] PostgreSQL migrations applied.
- [ ] Redis cache configured for dashboard aggregates.
- [ ] Queue/Kafka topics configured for async jobs.
- [ ] Offline queue sync conflict strategy tested.
- [ ] PII retention + masking policy documented.

## ML & AI
- [ ] STT provider selected (Whisper/OpenAI/AWS) and monitored.
- [ ] Sentiment + urgency model thresholds calibrated.
- [ ] Prediction model retraining schedule defined.
- [ ] Explainability panel enabled with feature importance.
- [ ] Model confidence and drift dashboards configured.

## Operations
- [ ] Uptime monitoring and alerting active.
- [ ] Dashboards export (CSV/PDF) validated.
- [ ] Disaster recovery backup restore tested.
- [ ] Demo mode toggle clearly visible and auditable.
- [ ] Release notes + rollback plan published.

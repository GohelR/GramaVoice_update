# GramaVoice API Contracts (v1)

## Base URL
- Local: `http://localhost:8000`
- Production: `https://<your-api-domain>`

## Auth
- Current demo endpoints are open.
- Production recommendation:
  - `Authorization: Bearer <JWT>`
  - RBAC claims: `role`, `district`, `permissions`

---

## 1) Health Check
`GET /health`

**Response**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-12T10:20:30.000000"
}
```

---

## 2) Analyze Text
`POST /api/analyze`

**Request**
```json
{
  "text": "मेरी पेंशन कब आएगी?",
  "language": "hi",
  "user_id": "demo_user"
}
```

**Response**
```json
{
  "success": true,
  "query_id": 123,
  "detected_intent": "check_status",
  "service_category": "Pension",
  "confidence": 0.91,
  "ai_response": "आपकी पेंशन इस महीने की 5 तारीख को जमा हुई है।"
}
```

---

## 3) Voice Input
`POST /api/voice-input`

**Form fields**
- `audio_file`: binary (`wav/mp3/m4a/webm`)
- `language`: `hi | en | ...`
- `user_id`: string

**Response**
```json
{
  "success": true,
  "query_id": 124,
  "query_text": "पानी की सप्लाई बंद है",
  "detected_intent": "complaint",
  "service_category": "Water Supply",
  "ai_response": "शिकायत दर्ज की गई है",
  "audio_response_url": "https://...",
  "confidence": 0.88,
  "complaint_id": "CMP-1001"
}
```

---

## 4) History
`POST /api/history`

**Request**
```json
{
  "user_id": "demo_user",
  "limit": 50
}
```

**Response**
```json
{
  "success": true,
  "history": []
}
```

---

## 5) Dashboard Data
`POST /api/dashboard-data`

**Request**
```json
{
  "days": 30
}
```

**Response**
```json
{
  "success": true,
  "data": {
    "total_queries": 1260,
    "total_complaints": 340,
    "resolved_complaints": 280,
    "resolution_rate": 82.3
  }
}
```

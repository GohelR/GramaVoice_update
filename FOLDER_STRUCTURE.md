# GramaVoice Folder Structure

```text
GramaVoice_update/
├── app.py                         # Main Streamlit app (hybrid voice + text + analytics modules)
├── frontend/
│   └── app.py                     # Alternate Streamlit frontend version
├── backend/
│   └── app/
│       ├── main.py                # FastAPI app + API routes
│       ├── api/                   # API package placeholder
│       ├── models/                # SQLAlchemy models + DB init
│       ├── services/              # AI + data services
│       └── utils/                 # Utility package
├── config/
│   └── settings.py                # Shared settings
├── requirements.txt
├── API_CONTRACTS.md               # Request/response contracts
├── DEPLOYMENT.md                  # Deployment notes
├── PRODUCTION_CHECKLIST.md        # Go-live checklist
└── README.md                      # Product + setup guide
```

import json
import math
import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

APP_NAME = "GramaVoice"

st.set_page_config(
    page_title=f"{APP_NAME} | Rural AI Service Gateway",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
:root {
  --bg:#f4f8ff;
  --card:rgba(255,255,255,0.7);
  --text:#0f172a;
  --muted:#475569;
  --brand:#2563eb;
  --brand2:#0ea5e9;
  --good:#059669;
  --warn:#d97706;
  --bad:#dc2626;
}

.stApp {background:var(--bg); color:var(--text); font-size:17px;}
.block-container {padding-top:1.3rem; max-width:1200px;}

.hero {
  background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%);
  border-radius:24px;
  padding:1.5rem;
  color:white;
  box-shadow:0 14px 32px rgba(37,99,235,.22);
  margin-bottom:1rem;
}
.hero h1,.hero p{color:white; margin:0;}
.hero p{margin-top:.45rem; opacity:.95;}

.glass {
  background: var(--card);
  backdrop-filter: blur(10px);
  border:1px solid rgba(148,163,184,.25);
  box-shadow:0 8px 24px rgba(15,23,42,.08);
  border-radius:18px;
  padding:1rem;
  margin-bottom:.9rem;
}

.metric-card {
  background:linear-gradient(135deg,#ffffff,#f1f8ff);
  border:1px solid rgba(37,99,235,.18);
  border-radius:16px;
  padding:1rem;
}

.big-btn .stButton>button,
.stButton>button {
  width:100%;
  min-height:48px;
  border-radius:12px;
  border:none;
  font-weight:700;
  box-shadow:0 6px 16px rgba(37,99,235,.18);
  background:linear-gradient(135deg,var(--brand),var(--brand2));
  color:#fff;
}

[data-testid="stSidebar"] {background:#ffffff; border-right:1px solid #e2e8f0;}

@media (max-width: 900px) {
  .block-container {padding: .8rem .65rem 4rem .65rem;}
  .hero {padding:1rem; border-radius:16px;}
}
</style>
""",
    unsafe_allow_html=True,
)

TRANSLATIONS = {
    "en": {
        "tagline": "Voice-first governance for every village",
        "language": "Language",
        "refresh": "Auto refresh live stats",
        "offline": "Offline mode",
        "fallback": "Mic blocked? Type your message below.",
        "query": "Your message",
        "process": "Process request",
        "status": "System status",
    },
    "hi": {
        "tagline": "हर गाँव के लिए आवाज़ आधारित सरकारी सहायता",
        "language": "भाषा",
        "refresh": "लाइव आँकड़े ऑटो रिफ्रेश",
        "offline": "ऑफ़लाइन मोड",
        "fallback": "माइक बंद है? नीचे अपना सवाल लिखें।",
        "query": "आपका संदेश",
        "process": "अनुरोध प्रोसेस करें",
        "status": "सिस्टम स्थिति",
    },
}

SERVICES = {
    "pension": {"title": "Pension", "icon": "💰", "owner": "Social Welfare"},
    "pmkisan": {"title": "PM-Kisan", "icon": "🌾", "owner": "Agriculture Dept"},
    "ration": {"title": "Ration", "icon": "🍚", "owner": "Food Supply"},
    "health": {"title": "Health Camps", "icon": "🏥", "owner": "Health Dept"},
    "electricity": {"title": "Electricity", "icon": "⚡", "owner": "Power Board"},
    "water": {"title": "Water Supply", "icon": "💧", "owner": "Water Dept"},
    "general": {"title": "General Help", "icon": "🧭", "owner": "Citizen Desk"},
}

KEYWORDS = {
    "pension": ["pension", "पेंशन", "old age", "वृद्धा"],
    "pmkisan": ["kisan", "farmer", "किसान", "pm किसान", "pm-kisan"],
    "ration": ["ration", "राशन", "card", "पीडीएस"],
    "health": ["health", "स्वास्थ्य", "hospital", "camp", "टीका"],
    "electricity": ["electricity", "बिजली", "power", "लाइन", "light"],
    "water": ["water", "पानी", "tap", "जल"],
}

RESPONSES = {
    "en": {
        "pension": "Your pension is active. Last transfer: ₹1,000 on 05 this month. Next expected disbursement: next month, week 1.",
        "pmkisan": "PM-Kisan status is approved. Next installment ₹2,000 is scheduled in the next cycle.",
        "ration": "Ration card is valid and eligible for this month's quota. Carry Aadhaar at FPS collection.",
        "health": "Nearest health camp is this Friday, 10:00 AM at Panchayat Bhavan. Free check-up and medicine support.",
        "electricity": "Power complaint registered successfully. Estimated resolution time: 24 hours. Keep complaint ID for follow-up.",
        "water": "Water supply complaint logged. Local line inspection is planned in 48 hours.",
        "general": "We can help with pension, PM-Kisan, ration, health camps, electricity, and water services.",
    },
    "hi": {
        "pension": "आपकी पेंशन सक्रिय है। पिछला भुगतान: इस महीने की 5 तारीख को ₹1,000 जमा हुए।",
        "pmkisan": "PM-किसान स्थिति स्वीकृत है। अगली ₹2,000 किस्त अगले चक्र में आएगी।",
        "ration": "राशन कार्ड सक्रिय है और इस महीने का कोटा उपलब्ध है।",
        "health": "नज़दीकी स्वास्थ्य शिविर इस शुक्रवार सुबह 10 बजे पंचायत भवन में है।",
        "electricity": "बिजली शिकायत दर्ज हो गई है। समाधान समय: लगभग 24 घंटे।",
        "water": "पानी सप्लाई शिकायत दर्ज की गई है। 48 घंटे में लाइन जांच होगी।",
        "general": "हम पेंशन, PM-किसान, राशन, स्वास्थ्य, बिजली और पानी सेवाओं में मदद करते हैं।",
    },
}


@st.cache_data(show_spinner=False)
def load_demo_history() -> pd.DataFrame:
    now = datetime.now()
    records = []
    intents = ["status", "complaint", "information"]
    cats = ["pension", "pmkisan", "ration", "health", "electricity", "water"]
    villages = ["Rampur", "Nandgaon", "Sundarpur", "Bhagwanpur", "Kheda", "Devli"]
    for i in range(180):
        ts = now - timedelta(hours=i * 4)
        cat = random.choice(cats)
        confidence = round(random.uniform(0.72, 0.98), 2)
        records.append(
            {
                "timestamp": ts,
                "citizen_id": f"GV-{1000+i}",
                "village": random.choice(villages),
                "category": cat,
                "intent": random.choice(intents),
                "confidence": confidence,
                "channel": random.choice(["voice", "text"]),
                "status": random.choice(["Resolved", "Open", "In Progress"]),
            }
        )
    return pd.DataFrame(records)


def init_state() -> None:
    defaults = {
        "lang": "en",
        "offline_mode": False,
        "query_text": "",
        "voice_result": "",
        "last_result": None,
        "selected_service": None,
        "history": load_demo_history().copy(),
        "logs": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def detect_intent(text: str):
    txt = text.lower().strip()
    if not txt:
        return {"intent": "unknown", "category": "general", "confidence": 0.0, "why": "Empty input"}
    for category, words in KEYWORDS.items():
        for word in words:
            if word in txt:
                intent = "complaint" if category in ["electricity", "water"] else "status"
                conf = min(0.99, 0.75 + len(word) / 20)
                return {
                    "intent": intent,
                    "category": category,
                    "confidence": round(conf, 2),
                    "why": f"Matched keyword '{word}'",
                }
    return {"intent": "information", "category": "general", "confidence": 0.62, "why": "No known keyword match"}


def route_response(category: str, lang: str) -> str:
    lang_key = "hi" if lang == "hi" else "en"
    return RESPONSES.get(lang_key, RESPONSES["en"]).get(category, RESPONSES[lang_key]["general"])


def add_log(item: dict) -> None:
    st.session_state.logs.append(item)
    st.session_state.logs = st.session_state.logs[-250:]


def add_to_history(result: dict) -> None:
    row = {
        "timestamp": datetime.now(),
        "citizen_id": f"GV-{random.randint(2000,9999)}",
        "village": random.choice(["Rampur", "Nandgaon", "Sundarpur", "Devli"]),
        "category": result["category"],
        "intent": result["intent"],
        "confidence": result["confidence"],
        "channel": result["channel"],
        "status": "Resolved" if result["confidence"] > 0.8 else "In Progress",
    }
    st.session_state.history = pd.concat([pd.DataFrame([row]), st.session_state.history], ignore_index=True)


def voice_component(lang_code: str):
    component_id = f"voice_{lang_code}"
    html = f"""
    <div style='background:#fff;border:1px solid #cbd5e1;border-radius:14px;padding:12px;font-family:Arial'>
      <div style='display:flex;gap:8px;flex-wrap:wrap'>
        <button id='start' style='padding:10px 14px;border-radius:10px;border:none;background:#2563eb;color:#fff;font-weight:700'>🎙️ Start Recording</button>
        <button id='stop' style='padding:10px 14px;border-radius:10px;border:1px solid #94a3b8;background:#fff;color:#0f172a;font-weight:700'>⏹ Stop Recording</button>
      </div>
      <p id='status' style='font-size:14px;margin:8px 0;color:#334155'>Status: idle</p>
      <textarea id='transcript' style='width:100%;min-height:82px;border:1px solid #cbd5e1;border-radius:10px;padding:8px' placeholder='Speech transcript will appear here'></textarea>
    </div>
    <script>
      const lang = "{lang_code}" === "hi" ? "hi-IN" : "en-IN";
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      const statusEl = document.getElementById('status');
      const transcriptEl = document.getElementById('transcript');
      let recognition = null;
      let finalText = "";
      function pushUpdate(st, txt) {{
        const payload = JSON.stringify({{status: st, text: txt || transcriptEl.value || ""}});
        window.parent.Streamlit.setComponentValue(payload);
      }}

      if (!SR) {{
        statusEl.innerText = "Status: Web Speech API not supported";
        pushUpdate("unsupported", "");
      }} else {{
        recognition = new SR();
        recognition.lang = lang;
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.onstart = () => {{ statusEl.innerText = "Status: recording"; pushUpdate("recording", transcriptEl.value); }};
        recognition.onerror = (e) => {{ statusEl.innerText = "Status: error - " + e.error; pushUpdate("error", transcriptEl.value); }};
        recognition.onend = () => {{ statusEl.innerText = "Status: stopped"; pushUpdate("stopped", transcriptEl.value); }};
        recognition.onresult = (event) => {{
          let interim = "";
          for (let i = event.resultIndex; i < event.results.length; ++i) {{
            const t = event.results[i][0].transcript;
            if (event.results[i].isFinal) finalText += t + " "; else interim += t;
          }}
          transcriptEl.value = (finalText + interim).trim();
          pushUpdate("listening", transcriptEl.value);
        }};

        document.getElementById('start').onclick = () => {{
          try {{ finalText = transcriptEl.value ? transcriptEl.value + " " : ""; recognition.start(); }} catch(e) {{ statusEl.innerText = "Status: already recording"; }}
        }};
        document.getElementById('stop').onclick = () => {{
          try {{ recognition.stop(); pushUpdate("stopped", transcriptEl.value); }} catch(e) {{ pushUpdate("error", transcriptEl.value); }}
        }};
      }}
    </script>
    """
    raw = components.html(html, height=235, key=component_id)
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            return {"status": "error", "text": ""}
    return None


def render_home(t):
    if st.checkbox(t["refresh"], value=True):
        components.html("<script>setTimeout(function(){window.parent.location.reload();},15000);</script>",height=0)

    hist = st.session_state.history
    total = len(hist)
    resolved = int((hist["status"] == "Resolved").sum())
    complaints = int(hist["intent"].eq("complaint").sum())
    conf = round(float(hist["confidence"].mean() * 100), 1)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Interactions", f"{total}")
    c2.metric("Complaints", f"{complaints}")
    c3.metric("Resolved", f"{resolved}")
    c4.metric("Avg AI Confidence", f"{conf}%")

    st.markdown("### Live category load")
    grp = hist.groupby("category").size().reset_index(name="count")
    fig = px.bar(grp, x="category", y="count", color="category", height=320)
    fig.update_layout(margin=dict(l=8, r=8, t=20, b=8), showlegend=False)
    st.plotly_chart(fig, width="stretch")


def render_voice_demo(t):
    st.markdown("### Voice + Text Input")
    vcol, txtcol = st.columns([1.25, 1])
    with vcol:
        voice_state = voice_component(st.session_state.lang)
        if voice_state and voice_state.get("text"):
            st.session_state.voice_result = voice_state.get("text", "")
            st.info(f"Voice status: {voice_state.get('status','unknown')}")

    with txtcol:
        st.caption(t["fallback"])
        incoming = st.session_state.voice_result or st.session_state.query_text
        query = st.text_area(
            t["query"],
            value=incoming,
            key="voice_query_area",
            height=150,
            placeholder="Ask for pension, ration, PM-Kisan, electricity, water, etc.",
        )
        st.session_state.query_text = query

        if st.button(t["process"], width="stretch"):
            if not query.strip():
                st.warning("Please provide voice or typed input.")
                return
            with st.spinner("Analyzing and routing your request..."):
                try:
                    intent = detect_intent(query)
                    response = route_response(intent["category"], st.session_state.lang)
                    result = {
                        "query": query,
                        "intent": intent["intent"],
                        "category": intent["category"],
                        "confidence": intent["confidence"],
                        "explanation": intent["why"],
                        "response": response,
                        "channel": "voice" if st.session_state.voice_result else "text",
                        "time": datetime.now(),
                    }
                    st.session_state.last_result = result
                    add_to_history(result)
                    add_log(result)
                except Exception as e:
                    st.error(f"Request failed safely: {e}")

    if st.session_state.last_result:
        r = st.session_state.last_result
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown(f"**Intent:** `{r['intent']}` | **Service:** `{r['category']}` | **Confidence:** `{round(r['confidence']*100,1)}%`")
        st.markdown(f"**Why this route?** {r['explanation']}")
        st.success(r["response"])
        st.markdown("</div>", unsafe_allow_html=True)


def render_services():
    st.markdown("### Government Service Panels")
    cols = st.columns(3)
    keys = list(SERVICES.keys())[:-1]
    for idx, service_key in enumerate(keys):
        info = SERVICES[service_key]
        with cols[idx % 3]:
            st.markdown(f"<div class='glass'><h4>{info['icon']} {info['title']}</h4><p>Managed by {info['owner']}</p>", unsafe_allow_html=True)
            if st.button(f"Open {info['title']}", key=f"open_{service_key}"):
                st.session_state.selected_service = service_key
            st.markdown("</div>", unsafe_allow_html=True)

    selected = st.session_state.selected_service
    if selected:
        data = SERVICES[selected]
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.subheader(f"{data['icon']} {data['title']} Service Panel")
        st.write(f"Department: **{data['owner']}**")
        st.write("Status: 🟢 Operational | Avg response SLA: 4.2h")
        st.write("Information: Document checks, application status, escalation contacts, and nearest help center are available.")
        if st.button("Create sample service ticket", key="mk_ticket"):
            st.success(f"Ticket created for {data['title']} at {datetime.now().strftime('%H:%M:%S')}")
        st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard():
    hist = st.session_state.history.copy()
    st.markdown("### Analytics Dashboard")
    days = st.selectbox("Time filter", [7, 15, 30, 60], index=2)
    cutoff = datetime.now() - timedelta(days=days)
    hist = hist[hist["timestamp"] >= cutoff]

    c1, c2, c3 = st.columns(3)
    c1.metric("Interactions", len(hist))
    c2.metric("Unique Villages", hist["village"].nunique())
    c3.metric("Resolution %", f"{(hist['status'].eq('Resolved').mean()*100):.1f}%")

    trend = hist.copy()
    trend["day"] = trend["timestamp"].dt.date
    daily = trend.groupby("day").size().reset_index(name="requests")
    fig1 = px.line(daily, x="day", y="requests", markers=True, height=300, title="Requests Over Time")
    st.plotly_chart(fig1, width="stretch")

    cat = hist.groupby("category").size().reset_index(name="count")
    fig2 = go.Figure(data=[go.Pie(labels=cat["category"], values=cat["count"], hole=.5)])
    fig2.update_layout(height=320, title="Service Mix")
    st.plotly_chart(fig2, width="stretch")


def render_history():
    st.markdown("### Query History")
    df = st.session_state.history.copy()

    q = st.text_input("Search by village / citizen / category")
    status_filter = st.multiselect("Filter status", options=sorted(df["status"].unique()), default=list(sorted(df["status"].unique())))
    if q:
        ql = q.lower()
        df = df[
            df["village"].str.lower().str.contains(ql)
            | df["citizen_id"].str.lower().str.contains(ql)
            | df["category"].str.lower().str.contains(ql)
        ]
    if status_filter:
        df = df[df["status"].isin(status_filter)]

    per_page = st.selectbox("Rows per page", [10, 20, 30], index=1)
    total_pages = max(1, math.ceil(len(df) / per_page))
    page_no = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    start = (page_no - 1) * per_page
    end = start + per_page

    st.dataframe(df.iloc[start:end], width="stretch", hide_index=True)
    st.caption(f"Showing {start + 1}-{min(end, len(df))} of {len(df)} rows")


def render_about():
    st.markdown("### About GramaVoice")
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown(
        """
**Problem**: Rural citizens face friction in accessing government services due to language, literacy, and process barriers.  
**Solution**: GramaVoice delivers a bilingual, voice-first AI interface with service routing, confidence scoring, and interaction analytics.  
**Traction-ready value**: Faster grievance handling, higher trust, and digital inclusion at scale.  
**For judges/investors/government**: Cloud-safe architecture, no device-level dependencies, and immediate deployment feasibility on Streamlit Cloud.
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)


init_state()
t = TRANSLATIONS[st.session_state.lang]

with st.sidebar:
    st.markdown("## 🎙️ GramaVoice")
    lang = st.radio(t["language"], ["en", "hi"], format_func=lambda x: "English" if x == "en" else "हिन्दी")
    st.session_state.lang = lang
    t = TRANSLATIONS[lang]
    st.session_state.offline_mode = st.toggle(t["offline"], value=st.session_state.offline_mode)
    page = st.radio(
        "Navigate",
        ["Home", "Voice Demo", "Services", "Dashboard", "History", "About"],
    )

st.markdown(
    f"""
<div class='hero'>
  <h1>GramaVoice</h1>
  <p>{t['tagline']}</p>
</div>
""",
    unsafe_allow_html=True,
)

status_text = "🟢 Online" if not st.session_state.offline_mode else "🟡 Offline mode with cached data"
st.markdown(f"<div class='glass'><b>{t['status']}:</b> {status_text}</div>", unsafe_allow_html=True)

try:
    if page == "Home":
        render_home(t)
    elif page == "Voice Demo":
        render_voice_demo(t)
    elif page == "Services":
        render_services()
    elif page == "Dashboard":
        render_dashboard()
    elif page == "History":
        render_history()
    else:
        render_about()
except Exception as page_error:
    st.error(f"Graceful failure: {page_error}")
    st.info("The app is still running. Please switch modules from sidebar.")

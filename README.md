# 🏛️ TenderPro AI Chatbot — Python (FastAPI + LangChain + Groq)

## Project Structure
```
tenderpro-python/
├── main.py                    ← FastAPI app entry point
├── requirements.txt           ← Python dependencies
├── .env.example               ← Environment variables template
├── data/
│   └── tenderpro.db           ← SQLite database (auto-created)
├── static/
│   ├── index.html             ← Chatbot frontend
│   └── admin.html             ← Admin leads panel
└── app/
    ├── __init__.py
    ├── database.py            ← Async SQLite setup
    ├── schemas.py             ← Pydantic validation models
    ├── ai_service.py          ← LangChain + Groq AI logic
    └── routers/
        ├── __init__.py
        ├── leads.py           ← POST /api/lead
        ├── chat.py            ← POST /api/chat
        └── admin.py           ← GET /api/admin/leads & /stats
```

---

## ✅ Step 1 — Install Python

Download from: https://python.org (version 3.10 or higher)

Verify installation:
```bash
python --version   # should show 3.10+
pip --version
```

---

## ✅ Step 2 — Get FREE Groq API Key

1. Visit: https://console.groq.com
2. Sign up / Login
3. Click **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)

---

## ✅ Step 3 — Setup Project

### Option A: Using venv (Recommended)
```bash
cd tenderpro-python

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Direct install
```bash
pip install -r requirements.txt
```

---

## ✅ Step 4 — Configure API Key

```bash
# Copy the example env file
cp .env.example .env
```

Open `.env` file and add your Groq key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

---

## ✅ Step 5 — Run the Server

```bash
python main.py
```

You should see:
```
╔══════════════════════════════════════════╗
║   🏛️  TenderPro AI Chatbot Running!      ║
╠══════════════════════════════════════════╣
║  Chatbot : http://localhost:8000          ║
║  Admin   : http://localhost:8000/admin    ║
║  API Docs: http://localhost:8000/docs     ║
╚══════════════════════════════════════════╝
```

---

## ✅ Step 6 — Open in Browser

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Chatbot (share with clients) |
| http://localhost:8000/admin | Admin panel (your leads) |
| http://localhost:8000/docs | Auto-generated Swagger API docs |

---

## 🔄 Development Mode (auto-reload on code changes)

```bash
uvicorn main:app --reload --port 8000
```

---

## 📝 Customize Company Info

Open `app/ai_service.py` and edit the `SYSTEM_PROMPT` variable:
- Change company name, phone, email
- Add/remove services
- Update pricing info, etc.

---

## 🌐 Deploy to Production

### Railway.app (Free)
1. Push code to GitHub
2. Go to railway.app → New Project → GitHub repo
3. Add env variable: `GROQ_API_KEY=your_key`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Render.com (Free)
1. Create Web Service from GitHub
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add `GROQ_API_KEY` in Environment

### VPS / Dedicated Server
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Chatbot page |
| GET | `/admin` | Admin panel |
| POST | `/api/lead` | Save lead (name, email, mobile) |
| POST | `/api/chat` | Chat with AI |
| GET | `/api/admin/leads` | All leads |
| GET | `/api/admin/stats` | Dashboard stats |
| GET | `/docs` | Swagger UI |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `GROQ_API_KEY` error | Make sure `.env` file exists with valid key |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Port 8000 in use | Run `uvicorn main:app --port 8001` |
| DB not found | It's auto-created in `data/` folder on first run |

---

## Tech Stack
- **FastAPI** — Modern async Python web framework
- **LangChain** — AI orchestration + conversation memory
- **Groq** — Ultra-fast LLM inference (Llama 3)
- **aiosqlite** — Async SQLite database
- **Pydantic** — Data validation & schemas
- **Uvicorn** — ASGI server

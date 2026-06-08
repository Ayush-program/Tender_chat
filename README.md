# TenderPro AI Chatbot

TenderPro AI Chatbot is a FastAPI-based lead capture and AI assistant app for tender consultancy businesses. It uses Groq and LangChain for AI responses, SQLite for local data storage, and includes a public chatbot page plus an admin dashboard.

## Features

- AI chatbot for tender consultancy queries
- Lead capture with name, email, and Indian mobile validation
- SQLite database for leads and chat logs
- Admin dashboard for leads and basic statistics
- FastAPI backend with Swagger API docs
- Static HTML, CSS, and JavaScript frontend
- Groq model configuration through environment variables

## Tech Stack

- Python
- FastAPI
- Uvicorn
- LangChain
- Groq
- SQLite
- aiosqlite
- Pydantic
- HTML, CSS, JavaScript

## Project Structure

```text
tenderpro-python/
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable example
├── .gitignore               # Git ignored files
├── data/
│   └── tenderpro.db         # SQLite database, created on first run
├── static/
│   ├── index.html           # Chatbot frontend
│   └── admin.html           # Admin leads dashboard
└── app/
    ├── database.py          # SQLite setup and database dependency
    ├── schemas.py           # Pydantic request/response models
    ├── ai_service.py        # Groq and LangChain AI logic
    └── routers/
        ├── leads.py         # POST /api/lead
        ├── chat.py          # POST /api/chat
        └── admin.py         # Admin API routes
```

## Requirements

- Python 3.10 or higher
- Groq API key

Check Python and pip:

```bash
python --version
pip --version
```

## Setup

1. Clone or open the project folder:

```bash
cd tenderpro-python
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment.

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create your environment file:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

6. Add your Groq API key in `.env`:

```env
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

You can create a Groq API key from https://console.groq.com.

## Run The Project

Start the server:

```bash
python main.py
```

The app will run at:

| URL | Purpose |
| --- | --- |
| http://localhost:8000 | Chatbot page |
| http://localhost:8000/admin | Admin dashboard |
| http://localhost:8000/docs | FastAPI Swagger docs |

## Development Mode

For auto-reload while editing code:

```bash
uvicorn main:app --reload --port 8000
```

If port 8000 is already in use:

```bash
uvicorn main:app --reload --port 8001
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Chatbot page |
| GET | `/admin` | Admin dashboard |
| POST | `/api/lead` | Save a lead |
| POST | `/api/chat` | Send chat messages to AI |
| GET | `/api/admin/leads` | Get all leads |
| GET | `/api/admin/stats` | Get dashboard stats |
| GET | `/docs` | Swagger API docs |

## Customize Company Information

Edit `SYSTEM_PROMPT` in `app/ai_service.py` to update:

- Company name
- Services
- Contact details
- Pricing message
- Business location
- Assistant behavior

## Database

The SQLite database is created automatically at `data/tenderpro.db` when the server starts. It stores:

- Lead details
- User chat messages
- Assistant replies

## Deployment

Example production command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

For Render, Railway, or a VPS, set this environment variable:

```env
GROQ_API_KEY=your_groq_api_key
```

Optional model override:

```env
GROQ_MODEL=llama-3.1-8b-instant
```

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `GROQ_API_KEY not found` | Create `.env` and add your Groq API key |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port already in use | Run with another port, for example `--port 8001` |
| Database missing | Start the server; it is created automatically |
| AI model error | Set `GROQ_MODEL` to a supported Groq model |

## Notes

- Do not commit `.env` because it contains secrets.
- The admin page is currently public. Add authentication before using it in production.
- The local SQLite database is useful for development and small deployments.

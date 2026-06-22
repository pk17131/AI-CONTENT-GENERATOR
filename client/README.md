AI Content Generator — React UI

This folder contains a minimal React (Vite) UI for an AI content generator.

Quick start:

1. Install dependencies

```bash
npm install
```

2. Run dev server

```bash
npm run dev
```

3. Backend

The UI expects a POST endpoint at `/api/generate` that accepts JSON `{ prompt, tone, length }` and returns JSON `{ text: "...generated content..." }`.

If you have an existing Python backend (`app.py`), consider adding a route `/api/generate` that proxies to your AI provider.

Run the provided FastAPI backend (optional):

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key (optional). If you don't set this, the server will run in mock mode for local development:

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "sk-..."
python -m uvicorn main:app --reload --port 8000
```

Linux / macOS:

```bash
export OPENAI_API_KEY="sk-..."
python -m uvicorn main:app --reload --port 8000
```

Files created:

- `package.json`, `vite.config.js`, `index.html`
- `src/` React entry and components

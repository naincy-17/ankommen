# Ankommen

Ankommen helps newcomers and visitors discover useful places and services. The
first working release supports Settlement and Tourism journeys in Ghaziabad.
Its included listings are clearly marked demo data, not verified providers.

## What works

- A responsive React interface for both journeys, live text search, category
  filters, result cards, and helpful loading/error/empty states.
- A FastAPI resource API with city and journey/category filters, multi-word
  search, and relevance ranking.
- A small Ghaziabad demo dataset, idempotent seeding, and automated API tests
  using an isolated in-memory SQLite database.

## Run locally

Requirements: Python 3.10+ and Node.js 18+.

### Backend (PowerShell)

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For safe local development, point this PowerShell session at SQLite so that
setup and demo seeding cannot write to a database URL in an existing `.env`:

```powershell
$env:DATABASE_URL = "sqlite:///./ankommen.db"
python create_tables.py
python seed_data.py
uvicorn main:app --reload
```

This local fallback is also used if `DATABASE_URL` is not set. Keep any
existing `backend\.env` unchanged.

Open <http://127.0.0.1:8000/docs> to explore the API. The frontend requests the
Ghaziabad demo listings from this server.

### Frontend (a second PowerShell window)

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (normally <http://localhost:5173>). Vite
forwards `/api` requests to the local FastAPI server.

### Tests and production build

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

For a fresh backend environment, install test tools with
`pip install -r requirements-dev.txt` instead of the production requirements.

```powershell
cd frontend
npm run build
```

## Deploy

The included [`render.yaml`](./render.yaml) is the shortest backend path:

1. Push this repository to GitHub and create a new Blueprint on Render from it.
   Render provisions the PostgreSQL database, installs `backend/requirements.txt`,
   creates the schema and demo records, and starts the FastAPI service.
2. Deploy the `frontend` directory as a Vercel project with the framework preset
   **Vite** and build command `npm run build`.
3. Set the Vercel project environment variable `VITE_API_URL` to the Render
   API origin, for example `https://ankommen-api.onrender.com` (no trailing
   slash). Set the Render service's `CORS_ORIGINS` to the deployed Vercel
   origin, for example `https://your-project.vercel.app`.
4. Redeploy both services after setting those environment variables.

Keep database URLs and deployment credentials in the hosting provider's secret
environment settings; never commit `.env`. The sample records are illustrative:
replace them with verified, current listings before presenting them as real
local recommendations.

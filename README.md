# 🧬 Blood Flow Simulation Platform
### 1D Navier–Stokes Model for Cerebral Vessel Dynamics

## Overview

This project simulates blood flow in cerebral vessels using a 1D Navier–Stokes formulation and visualizes the results on a simple web UI. Two domains are targeted:

- Healthy vessel (β = 0) – stable flow case
- Aneurysm vessel (β ≠ 0) – pressure/area nonlinearity (WIP)

The repository contains a Python backend (Flask) and a static frontend (HTML + JS with Plotly).

---

## Tech Stack

- Backend: Python, Flask, NumPy, SciPy
- Frontend: HTML, CSS, JavaScript, Plotly
- API: REST (JSON)

Note: The codebase currently includes FastAPI in `requirements.txt`, but the running app is Flask-based.

---

## Prerequisites

- Python 3.10+ (recommended)
- Windows PowerShell 5.1 or newer (commands below use PowerShell)

Optional (only if you plan to serve the frontend with a Node toolchain; not required here): Node.js.

---

## Local Setup (Windows PowerShell)

### 1) Backend

```powershell
# From repo root
Set-Location backend

# Create and activate a virtual environment
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start the backend (Flask)
# Option A: Development (uses Flask's built-in server)
$env:FLASK_APP = "app.main:app"; flask run --host 0.0.0.0 --port 8001

# Option B: Production-style (gunicorn)
gunicorn -w 2 -b 0.0.0.0:8001 app.main:app
```

Notes:
- The current Flask app in `backend/app/main.py` only provides a root route (`/`). The simulation data endpoint (`/data`) is implemented in `backend/server.py`, but it depends on a function `run_simulation` that is not exported by any existing `simulation.py`. See "Known Issues" below.

### 2) Frontend

The frontend is a static site; you can open `frontend/index.html` directly or serve it with a simple static server.

```powershell
# Option A: Open directly (double-click frontend/index.html)

# Option B: Serve locally via Python
Set-Location ..\frontend
python -m http.server 5173
# Then browse to http://localhost:5173
```

By default, `script.js` tries to fetch `/data` from the same origin. For a separate backend (e.g., running on port 8001), include `config.js` in `index.html` and set `API_URL` accordingly:

```html
<!-- In frontend/index.html, inside <head> -->
<script src="config.js"></script>
```

```js
// frontend/config.js
const API_URL = "http://localhost:8001"; // or your deployed URL
```

---

## API

- `GET /data` → JSON with fields:
   - `z`: number[] (axial coordinate)
   - `time`: number[] (time samples)
   - `pressure`: number[][] (pressure over space for each time index, in mmHg)

This route is expected by `frontend/script.js`. In local dev with split servers, ensure `API_URL` points to the backend that serves `/data`.

---

## Deployment (Render)

The file `render.ymal` should be renamed to `render.yaml`.

Recommended backend service (Flask + gunicorn) with repo root as context and `rootDir: backend`:

```yaml
services:
   - type: web
      name: bloodflow-backend
      env: python
      rootDir: backend
      buildCommand: pip install -r requirements.txt
      startCommand: gunicorn app.main:app
      envVars:
         - key: PORT
            value: 10000

   - type: static
      name: bloodflow-frontend
      rootDir: frontend
      buildCommand: ""
      staticPublishPath: ./
```

If you want the backend to serve the frontend as well (single service), switch to `backend/server.py` as the entry point and make sure it works locally first (see Known Issues).

---

## Known Issues / To Do

- `backend/server.py` imports `from simulation import run_simulation`, but no `simulation.py` exposing `run_simulation` exists. The simulation scripts (`simulation_t.py`, `simulation_z.py`) are interactive and do not export a function returning `(z, time, P)`.
   - Action: create `backend/simulation.py` with `run_simulation()` that returns the arrays, or refactor one of the existing scripts to expose this function.
   - Once available, you can run a single server that serves both the API and static files:
      ```powershell
      Set-Location backend; .\.venv\Scripts\Activate.ps1; python server.py
      # Browse to http://localhost:10000 (or PORT env var)
      ```

- The README previously referenced FastAPI/uvicorn; the actual app is Flask. The instructions above are now aligned with Flask.

- `frontend/index.html` currently does not include `config.js`. If your backend runs on a different origin/port, add `<script src="config.js"></script>` and set `API_URL`.

- CORS: If you serve frontend and backend on different ports, ensure CORS is enabled in Flask (package `flask-cors` is already in requirements; see `backend/app/main.py`).

---

## Troubleshooting

- 404 on `/data`: Ensure you are running a backend that exposes `/data` (currently `backend/server.py` once `run_simulation` exists), and that `config.js` points to it when using a separate static server for the frontend.
- CORS errors in browser: Serve frontend from the backend (same origin) or enable CORS and set `API_URL` to the backend URL.
- Port already in use: Change the port in your run command (e.g., `--port 8002`) or stop the conflicting process.

---

## Contributors

- Maryamolsadat Samavaki — Research Lead
- Juha-Matti Huusko — Project Supervisor
- Mahesh Idangodage — IT Developer
- Manjula Karunanayaka — IT Developer

---

## Vision

To build a scalable, interactive simulation tool that connects medical research with modern computing for blood flow diagnostics, neurosurgical research, and biomedical education.



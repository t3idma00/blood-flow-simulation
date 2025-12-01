# 🧬 Blood Flow Simulation Platform  
### 1D Navier–Stokes Model for Cerebral Vessel Dynamics  

## Project Overview

This project simulates **blood flow in cerebral vessels** using the **1D Navier–Stokes equations (NSE)**.  
It focuses on two domains:

- **Healthy vessel (β = 0)** – simplified, stable flow  
- **Aneurysm vessel (β ≠ 0)** – nonlinear, pressure-variant flow  

The main goal is to create a **numerical solver** and an **interactive web dashboard** for visualizing flow behavior and studying wave propagation in arteries.

---

##  Objectives

- Build a Python-based solver for the 1D NSE  
- Implement absorbing outlet boundary conditions (to minimize reflections)  
- Develop an interactive web dashboard for visualization  
- Compare results between healthy and aneurysm models  
- Provide clean and modular code for future research

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| **Backend** | Python (FastAPI, NumPy) | Blood flow simulation engine |
| **Frontend** | HTML, CSS, JavaScript, Chart.js | Interactive visualization dashboard |
| **API** | REST (JSON) | Data communication |
| **Docs** | Markdown | Reports & research notes |

---

##  How to Install

These steps are for Windows PowerShell 5.1. The project has a FastAPI backend (port 8000) and a simple Node static server for the frontend (port 3000).

###  Backend Setup (FastAPI)

```powershell
# From repo root, go to backend
Set-Location "backend"

# Create and activate a virtual environment
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip; python -m pip install -r requirements.txt

# Run the FastAPI server (uvicorn)
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000

# Verify
# Visit http://127.0.0.1:8000/ in your browser
```

Tips:
- If the port is already in use, stop any running Python processes:
    ```powershell
    Get-Process | Where-Object { $_.ProcessName -like '*python*' } | Stop-Process -Force
    ```

###  Frontend Setup (Node static server)

```powershell
# In a new terminal, go to frontend
Set-Location "frontend"

# Install Node dependencies
npm install

# Start the static server
npm start

# Open in your browser:
# http://localhost:3000
```

Notes:
- The frontend auto-switches API base URL: it uses `http://localhost:8000` when running locally.
- Ensure backend is running before opening simulation pages.
- Simulation pages: `public/simulations/sim1.html`, `sim2.html` (others may be hidden by default).

###  Additional Notes

- Run backend and frontend in parallel.
- Backend runs on port 8000; frontend on 3000.
- If the page can’t load data, ensure the backend is running and that the browser can reach `http://localhost:8000`.

##  Work Schedule

| **Week** | **Focus** | **Deliverables** |
|-----------|------------|-----------------|
| **Week 1** | **Healthy Vessel Model Setup** | Review project goals and 1D Navier–Stokes model for blood flow.|
| **Week 2** | **Healthy Model Validation** | Implement stable 1D solver (β = 0) and performed initial test runs |
| **Weeks 3–4** | **Aneurysm / Nonlinear Model** | Extended solver (β ≠ 0) and comparison with healthy case. |
| **Weeks 5–6** | **Boundary Condition Tuning** | Absorbing outlet implemented and tested. |
| **Week 7** | **Validation & Analysis** | Parameter tests and flow–pressure comparison graphs. |
| **Week 8** | **Final Reporting & Presentation** | Clean repo, summary report, and presentation-ready demo. |



##  Simulation Workflow

- Define model parameters (β, pressure, time step).  
    *For now, only the β = 0 healthy case is implemented.*
- Run the Python solver via FastAPI endpoint.  
- Retrieve results (flow rate Q, area A, pressure P).  
- Plot interactive charts on the React frontend.  
- Analyze healthy vs aneurysm comparisons.

---

##  Research Background

This project supports research led by **Dr. Maryamolsadat Samavaki** on cerebral hemodynamics and aneurysm modeling.  
The system helps visualize and analyze the wave reflections and flow transitions between healthy and diseased arterial sections.

---

## Contributors

| Name | Role |
|------|------|
| **Maryamolsadat Samavaki** | Research Lead | 
| **Juha-Matti Huusko** | Project Supervisor | 
| **Mahesh Idangodage** | IT Developer | 
| **Manjula Karunanayaka** | IT Developer | 

---

##  Vision

 “To build a scalable, interactive simulation tool that connects medical research with modern computing.”

This project lays the foundation for future development of a neurovascular simulation platform supporting:

- Blood flow diagnostics  
- Neurosurgical research  
- Biomedical education





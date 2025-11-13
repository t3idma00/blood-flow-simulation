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

###  Backend Setup

```powershell
# From repo root, go to backend
Set-Location backend

# Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv-1; .\.venv-1\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start the backend (Flask dev server)
$env:FLASK_APP = "app.main:app"; flask run --host 0.0.0.0 --port 8001

# Verify backend is running:
# Open http://localhost:8001/ and you should see a JSON message
```

###  Frontend Setup

```powershell
# In a new terminal, go to frontend
Set-Location frontend

# Serve the static site
python -m http.server 5173

# Open in your browser:
# http://localhost:5173
```

###  Additional Notes

- Run backend and frontend in parallel.
- Backend runs on port 8001; frontend on 5173.
- If the page can’t load data, ensure the backend is running and consider pointing the frontend to the backend URL via a config file.

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





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

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv-1

# Activate virtual environment
# For Windows:
.\.venv-1\Scripts\Activate.ps1
# For macOS/Linux:
# source .venv-1/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload --port 8001

# Verify backend is running by opening in browser:
# http://localhost:8001/health
# Should see: {"status": "ok"}
```

###  Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start the frontend server
python -m http.server 5173

# Open in your browser:
# http://localhost:5173
```

###  Additional Notes

- Make sure both backend and frontend servers are running simultaneously
- Backend runs on port 8001 to avoid conflicts
- The simulation interface will be available at http://localhost:5173
- You can test different parameters in the web interface
- For troubleshooting, check the browser's developer tools (F12 -> Console tab)

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



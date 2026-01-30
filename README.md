
# 1D Blood Flow Simulation Project

This repository contains a one-dimensional (1D) blood flow simulation developed to study **wave propagation, pressure–flow interaction, and numerical behavior** in compliant vessels.

The project documents the models implemented, simulations performed, and observations made during the development process. 



---

## Project Goal

The main goal of this project is to **develop and test a 1D blood flow solver** capable of simulating flow, cross-sectional area, and pressure evolution in an arterial segment.

The solver is built progressively, starting from simplified test models and extending toward a more realistic artery simulation with physiological forcing. Along the way, different numerical and modeling choices are explored to ensure stability and physically meaningful results.

---

## 🛠️ What Has Been Implemented

### Linear Test Models
- **Verification:** Simplified linearized wave systems used to verify numerical schemes.
- **Methods:** Implemented using **MacCormack** and **Lax–Wendroff** type methods.
- **Focus:** Used to study basic wave propagation and numerical behavior in a controlled setting.

### Healthy-Domain Simulation
- A simplified artery-like spatial domain.
- Includes linear damping and smooth initial perturbations.
- Used to examine wave propagation over longer domains and time intervals.

### Physiological Inlet Forcing
- Time-dependent inlet pressure waveform based on a **Blackman–Harris-type modulation**.
- Used to represent a simplified cardiac pressure input.

### Windkessel Outlet Model
- Implementation of a linearized Windkessel outlet boundary condition.
- Couples flow and area through an ordinary differential equation (ODE).
- Introduced to model downstream vascular effects and obtain realistic outlet behavior.

### Full 1D Artery Simulation
- Combination of linearized blood flow equations, numerical time-stepping schemes, physiological inlet forcing, and Windkessel outlet coupling.
- Pressure, flow, and vessel area are monitored at multiple locations along the artery.

---

##  Output and Analysis

Simulation outputs include:
- **Vessel Area** ($A$)
- **Flow Rate** ($Q$)
- **Pressure** signals

Results are analyzed qualitatively through time-series plots to assess wave propagation, stability, and overall solution behavior.

---

##  Installation & Setup

This project consists of a **simulation backend** and a **visualization frontend**. Both must be running simultaneously.

### Prerequisites
- **Python 3.9+**
- **Node.js (v14+)** and **npm**

> [!IMPORTANT]  
> The frontend retrieves simulation results from the backend API. Keep **two terminal sessions open** when running the project.

### Backend Setup (Simulation Server)

```bash
cd backend
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn api.server:app --port 8000


### Frontend Setup (Visualization Dashboard)

cd frontend
npm install
npm start
```

Open the dashboard in your browser:
http://localhost:3000

# 🧬 Blood Flow Simulation Platform  
### 1D Navier–Stokes Model for Cerebral Vessel Dynamics  

## 🧠 Project Overview

This project simulates **blood flow in cerebral vessels** using the **1D Navier–Stokes equations (NSE)**.  
It focuses on two domains:

-  **Healthy vessel (β = 0)** – simplified, stable flow  
- **Aneurysm vessel (β ≠ 0)** – nonlinear, pressure-variant flow  

The main goal is to create a **numerical solver** and an **interactive web dashboard** for visualizing flow behavior and studying wave propagation in arteries.

---

## 🎯 Objectives

- Build a Python-based solver for the 1D NSE  
- Implement absorbing outlet boundary conditions (to minimize reflections)  
- Develop an interactive web dashboard for visualization  
- Compare results between healthy and aneurysm models  
- Provide clean and modular code for future research

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| 🧮 **Backend** | Python (FastAPI, NumPy) | Blood flow simulation engine |
| 🌐 **Frontend** | HTML, CSS, JavaScript, Chart.js | Interactive visualization dashboard |
| 🔗 **API** | REST (JSON) | Data communication |
| 🧾 **Docs** | Markdown | Reports & research notes |

---

## 🚀 Quick Start

### 🧭 Backend Setup

- cd backend
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --reload --port 8000
- Open → http://127.0.0.1:8000/docs

### 🌐 Frontend Setup

- cd frontend
- python -m http.server 5173


## 🧪 Simulation Workflow

- Define model parameters (β, pressure, time step).  
   *For now, only the β = 0 healthy case is implemented.*
- Run the Python solver via FastAPI endpoint.  
- Retrieve results (flow rate Q, area A, pressure P).  
- Plot interactive charts on the React frontend.  
- Analyze healthy vs aneurysm comparisons.

---

## 👩‍🔬 Research Background

This project supports research led by **Dr. Maryamolsadat Samavaki** on cerebral hemodynamics and aneurysm modeling.  
The system helps visualize and analyze the wave reflections and flow transitions between healthy and diseased arterial sections.

---

## 👥 Contributors

| Name | Role | Affiliation |
|------|------|--------------|
| **Dr. Maryamolsadat Samavaki** | Research Lead | University of Oulu |
| **Juha-Matti Huusko** | Project Supervisor | Oulu University of Applied Sciences |
| **Mahesh Idangodage** | IT Developer | Oulu University of Applied Sciences |
| **Manjula Karunanayaka** | IT Developer | Oulu University of Applied Sciences |

---

## 🧭 Vision

 “To build a scalable, interactive simulation tool that connects medical research with modern computing.”

This project lays the foundation for future development of a neurovascular simulation platform supporting:

-  Blood flow diagnostics  
-  Neurosurgical research  
- Biomedical education



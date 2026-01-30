# 🌐 Frontend: Simulation Dashboard

The frontend is a lightweight web application that visualizes the results from the blood flow simulation backend.

## 🚀 Quick Start

### Prerequisites
- Node.js (v14+)
- npm

### Installation Steps

1. **Navigate to the frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Start the server:**
   ```powershell
   npm start
   ```

4. **View the application:**
   Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Key Files

- `public/index.html`: Main landing page.
- `public/app.js`: Core logic for fetching and rendering simulation data.
- `public/config.js`: Configuration for API endpoints (automatically switches between local and production).
- `server/index.js`: Express server script.

## 📊 Visualization

We use **Chart.js** to render interactive graphs of:
- Blood Flow (Q)
- Vessel Area (A)
- Pressure (P)

Ensure the **Backend** is running on `http://localhost:8000` for the data to load.

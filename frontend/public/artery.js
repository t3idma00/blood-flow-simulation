// frontend-node/public/artery.js

const API_URL = "http://localhost:8000/artery-sim";

const runBtn = document.getElementById("runBtn");
const statusLabel = document.getElementById("statusLabel");

runBtn.addEventListener("click", () => {
  runSimulation();
});

async function runSimulation() {
  try {
    statusLabel.textContent = "Running Python simulation...";
    const res = await fetch(API_URL);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const data = await res.json();
    statusLabel.textContent = "Simulation complete. Rendering plots...";
    renderPlots(data);
    statusLabel.textContent = "Done.";
  } catch (err) {
    console.error("Error running simulation:", err);
    statusLabel.textContent = "Error: " + err.message;
  }
}

function renderPlots(data) {
  const t = data.t; // time [s]

  const monitorZ = data.monitor_z; // [z_in, z_mid, z_out]
  const labels = monitorZ.map((z, i) => {
    if (i === 0) return `Inlet (z = ${z.toFixed(3)} m)`;
    if (i === monitorZ.length - 1) return `Outlet (z = ${z.toFixed(3)} m)`;
    return `Mid (z = ${z.toFixed(3)} m)`;
  });

  // pressure_mmHg is [ [inlet], [mid], [out] ]
  const pressure_mmHg = data.pressure_mmHg;
  const flow = data.flow;
  const area = data.area;
  const P_out_mmHg = data.P_out_mmHg;
  const Q_out = data.Q_out;
  const P_wk_mmHg = data.P_wk_mmHg;

  // ---- Pressure at inlet / mid / outlet ----
  const pressureTraces = pressure_mmHg.map((series, i) => ({
    x: t,
    y: series,
    mode: "lines",
    name: labels[i]
  }));

  Plotly.newPlot("pressurePlot", pressureTraces, {
    xaxis: { title: "Time [s]" },
    yaxis: { title: "Pressure [mmHg]" },
    margin: { t: 20 },
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "#e5e7eb" }
  });

  // ---- Flow at inlet / mid / outlet ----
  const flowTraces = flow.map((series, i) => ({
    x: t,
    y: series,
    mode: "lines",
    name: labels[i]
  }));

  Plotly.newPlot("flowPlot", flowTraces, {
    xaxis: { title: "Time [s]" },
    yaxis: { title: "Flow Q̃ [m³/s]" },
    margin: { t: 20 },
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "#e5e7eb" }
  });

  // ---- Area at inlet / mid / outlet ----
  const areaTraces = area.map((series, i) => ({
    x: t,
    y: series,
    mode: "lines",
    name: labels[i]
  }));

  Plotly.newPlot("areaPlot", areaTraces, {
    xaxis: { title: "Time [s]" },
    yaxis: { title: "Area [m²]" },
    margin: { t: 20 },
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "#e5e7eb" }
  });

  // ---- Outlet pressure ----
  Plotly.newPlot("outletPressurePlot", [{
    x: t,
    y: P_out_mmHg,
    mode: "lines",
    name: "Outlet Pressure"
  }], {
    xaxis: { title: "Time [s]" },
    yaxis: { title: "Outlet Pressure [mmHg]" },
    margin: { t: 20 },
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "#e5e7eb" }
  });

  // ---- Outlet flow ----
  Plotly.newPlot("outletFlowPlot", [{
    x: t,
    y: Q_out,
    mode: "lines",
    name: "Outlet Flow"
  }], {
    xaxis: { title: "Time [s]" },
    yaxis: { title: "Outlet Q̃ [m³/s]" },
    margin: { t: 20 },
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "#e5e7eb" }
  });

  // ---- Windkessel pressure ----
  Plotly.newPlot("wkPressurePlot", [{
    x: t,
    y: P_wk_mmHg,
    mode: "lines",
    name: "Windkessel Pressure"
  }], {
    xaxis: { title: "Time [s]" },
    yaxis: { title: "Pressure [mmHg]" },
    margin: { t: 20 },
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "#e5e7eb" }
  });
}

// Auto-run once on page load
runSimulation();

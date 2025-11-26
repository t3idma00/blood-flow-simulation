console.log("script loaded");

// Backend URL from config.js (falls back to same origin)
const API_URL = window.API_URL || "";

let z = [];
let time = [];
let pressure = [];
let currentSim = "t";

const slider = document.getElementById("slider");
const plotDiv = document.getElementById("plot");
const simSelect = document.getElementById("sim-select");
const simLabel = document.getElementById("sim-label");

// Load a simulation by name: "t", "z", or "wk"
function loadSimulation(name) {
  currentSim = name;
  plotDiv.innerHTML = "<p>Loading simulation...</p>";

  const url = `${API_URL}/data?name=${encodeURIComponent(name)}`;
  console.log("Fetching", url);

  fetch(url)
    .then((res) => {
      if (!res.ok) {
        throw new Error(`Failed to fetch data: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      z = data.z;
      time = data.time;
      pressure = data.pressure;

      if (!Array.isArray(pressure) || pressure.length === 0) {
        throw new Error("Invalid or empty simulation data.");
      }

      // Configure slider
      slider.min = 0;
      slider.max = pressure.length - 1;
      slider.value = 0;

      // Label for current simulation
      if (simLabel) {
        const prettyName = {
          t: "Temporal pulse (simulation_t)",
          z: "Travelling wave (simulation_z)",
          wk: "Windkessel-like (healthy_wk)",
        }[name] || name;
        simLabel.textContent = ` – ${prettyName}`;
      }

      // Initial plot
      drawPlot(0);
    })
    .catch((error) => {
      console.error("Error loading simulation data:", error);
      plotDiv.innerHTML =
        '<p style="color:red;">Error loading simulation data. Check the API_URL in config.js and that the backend is running.</p>';
    });
}

// Draw function for Plotly
function drawPlot(i) {
  if (!pressure || !pressure[i]) {
    return;
  }

  const trace = {
    x: z,
    y: pressure[i],
    mode: "lines",
    name: "Pressure (mmHg)",
  };

  const layout = {
    title: `Vessel Pressure at t = ${time[i].toFixed(3)} s (simulation: ${currentSim})`,
    xaxis: { title: "Length (m)" },
    yaxis: { title: "Pressure (mmHg)" },
    legend: { orientation: "h", y: -0.2 },
  };

  Plotly.newPlot(plotDiv, [trace], layout, { responsive: true });
}

// Slider event
slider.addEventListener("input", () => {
  const idx = parseInt(slider.value, 10);
  if (Number.isNaN(idx)) return;
  drawPlot(idx);
});

// Simulation selector event
if (simSelect) {
  simSelect.addEventListener("change", () => {
    loadSimulation(simSelect.value);
  });
}

// Initial load once DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  loadSimulation(currentSim);
});

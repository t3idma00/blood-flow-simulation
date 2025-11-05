console.log("script loaded");

// Load backend URL from config.js
const API_URL = window.API_URL || ""; // fallback if not defined

let z, time, pressure;
const slider = document.getElementById("slider");
const plotDiv = document.getElementById("plot");

// Fetch simulation data from backend
fetch(`${API_URL}/data`)
  .then(res => {
    if (!res.ok) {
      throw new Error(`Failed to fetch data: ${res.status}`);
    }
    return res.json();
  })
  .then(data => {
    z = data.z;
    time = data.time;
    pressure = data.pressure;

    if (!Array.isArray(pressure) || pressure.length === 0) {
      throw new Error("Invalid or empty simulation data.");
    }

    slider.max = pressure.length - 1; // set slider max to number of time steps
    drawPlot(0); // initial plot

    slider.addEventListener("input", () => {
      drawPlot(parseInt(slider.value));
    });
  })
  .catch(error => {
    console.error("Error loading simulation data:", error);
    plotDiv.innerHTML = `<p style="color:red;">Error loading simulation data. Please try again later.</p>`;
  });

// Draw function for Plotly
function drawPlot(i) {
  const traces = [
    {
      x: z,
      y: pressure[i],
      mode: "lines",
      name: "Pressure (mmHg)",
      line: { color: "red" }
    }
  ];

  const layout = {
    title: `Vessel Pressure at t = ${time[i].toFixed(3)} s`,
    xaxis: { title: "Length (m)" },
    yaxis: { title: "Pressure (mmHg)" },
    legend: { orientation: "h", y: -0.2 }
  };

  Plotly.newPlot(plotDiv, traces, layout, { responsive: true });
}

console.log("script loaded");

let z, time, pressure;
const slider = document.getElementById("slider");
const plotDiv = document.getElementById("plot");

// Fetch simulation data from backend
fetch("/data")
  .then(res => res.json())
  .then(data => {
    z = data.z;
    time = data.time;
    pressure = data.pressure;

    slider.max = pressure.length - 1; // set slider max to number of time steps
    drawPlot(0); // initial plot

    slider.addEventListener("input", () => {
      drawPlot(parseInt(slider.value));
    });
  });

// Draw function for Plotly
function drawPlot(i) {
  const traces = [
    { x: z, y: pressure[i], mode: "lines", name: "Pressure (mmHg)", line: { color: "red" } }
  ];

  const layout = {
    title: `Vessel Pressure at t = ${time[i].toFixed(3)} s`,
    xaxis: { title: "Length (m)" },
    yaxis: { title: "Pressure (mmHg)" },
    legend: { orientation: "h", y: -0.2 }
  };

  Plotly.newPlot(plotDiv, traces, layout, { responsive: true });
}

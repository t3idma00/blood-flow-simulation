// frontend-node/public/app.js

const API_URL = "http://localhost:8000/simulation";

let simData = null;

const timeSlider = document.getElementById("timeSlider");
const timeLabel  = document.getElementById("timeLabel");

// Load simulation from FastAPI
async function loadSimulation() {
    const res = await fetch(API_URL);
    const data = await res.json();

    simData = data;

    // Prepare slider
    timeSlider.max = simData.times.length - 1;
    timeSlider.value = 0;

    drawFrame(0);

    timeSlider.addEventListener("input", () => {
        drawFrame(parseInt(timeSlider.value));
    });
}

function drawFrame(frameIndex) {
    const x = simData.x;
    const a = simData.a[frameIndex];
    const q = simData.q[frameIndex];
    const tau = simData.times[frameIndex];

    timeLabel.textContent = `τ = ${tau.toFixed(5)} (index ${frameIndex})`;

    const traceA = {
        x: x,
        y: a,
        name: "a(x, τ)",
        mode: "lines",
        line: { color: "orange", width: 3 }
    };

    const traceQ = {
        x: x,
        y: q,
        name: "q(x, τ)",
        mode: "lines",
        line: { color: "blue", width: 3 }
    };

    const layout = {
        title: `MacCormack Scheme — τ = ${tau.toFixed(5)}`,
        xaxis: {
            title: "x (dimensionless)",
            range: [0, 1]
        },
        yaxis: {
            title: "Value"
        },
        margin: { t: 50, r: 30, l: 60, b: 60 }
    };

    Plotly.newPlot("plot", [traceA, traceQ], layout, { responsive: true });
}

// Run everything
loadSimulation();

/**********************************************
 * BACKEND URL AUTO SWITCH (LOCAL <-> RENDER)
 **********************************************/
const BACKEND_LOCAL  = "http://localhost:8000";
const BACKEND_RENDER = "https://blood-flow-backend.onrender.com";

const API_BASE =
    location.hostname === "localhost"
        ? BACKEND_LOCAL
        : BACKEND_RENDER;

/**********************************************
 * DETECT SIMULATION NAME: ?sim=sim1
 **********************************************/
const urlParams = new URLSearchParams(window.location.search);
const simName = urlParams.get("sim");

if (!simName) {
    alert("Missing simulation name! Example: ?sim=sim1");
}

/**********************************************
 * ELEMENTS
 **********************************************/
const timeSlider = document.getElementById("timeSlider");
const timeLabel  = document.getElementById("timeLabel");

let simData = null;

/**********************************************
 * LOAD SIMULATION FROM BACKEND
 **********************************************/
async function loadSimulation() {
    const endpoint = `${API_BASE}/simulation/${simName}`;
    console.log("Fetching:", endpoint);

    const res = await fetch(endpoint);
    if (!res.ok) {
        timeLabel.textContent = `Error loading ${simName}`;
        console.log(await res.text());
        return;
    }

    simData = await res.json();

    timeSlider.min = 0;
    timeSlider.max = simData.times.length - 1;
    timeSlider.value = 0;

    drawFrame(0);
    timeSlider.addEventListener("input", () => {
        drawFrame(parseInt(timeSlider.value));
    });
}

/**********************************************
 * PLOT FRAME USING PLOTLY
 **********************************************/
function drawFrame(i) {
    const x   = simData.x;
    const a   = simData.a[i];
    const q   = simData.q[i];
    const tau = simData.times[i];

    timeLabel.textContent = `τ = ${tau.toFixed(5)} (index ${i})`;

    Plotly.newPlot("plot", [
        {
            x: x,
            y: a,
            name: "a(x, τ)",
            mode: "lines",
            line: { color: "orange", width: 3 }
        },
        {
            x: x,
            y: q,
            name: "q(x, τ)",
            mode: "lines",
            line: { color: "blue", width: 3 }
        }
    ], {
        title: `${simName} — τ = ${tau.toFixed(5)}`,
        xaxis: { title: "x (dimensionless)" },
        yaxis: { title: "Value" },
        margin: { t: 40, l: 40, b: 50, r: 20 }
    });
}

/**********************************************
 * START
 **********************************************/
loadSimulation();

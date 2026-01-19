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

    timeLabel.textContent = `τ = ${tau.toFixed(5)} s (index ${i})`;

    // Compute global min/max for static y-axis (safe for large arrays)
    if (typeof drawFrame.ymin === 'undefined' || typeof drawFrame.ymax === 'undefined') {
        let ymin = Infinity;
        let ymax = -Infinity;
        for (let arr of simData.a) {
            for (let v of arr) { if (v < ymin) ymin = v; if (v > ymax) ymax = v; }
        }
        for (let arr of simData.q) {
            for (let v of arr) { if (v < ymin) ymin = v; if (v > ymax) ymax = v; }
        }
        const padding = 0.2 * (ymax - ymin);
        drawFrame.ymin = ymin - padding;
        drawFrame.ymax = ymax + padding;
    }
    const prefix = (typeof window !== 'undefined' && typeof window.PLOT_TITLE_PREFIX !== 'undefined')
        ? window.PLOT_TITLE_PREFIX
        : simName;
    // Axis titles: dimensional vs dimensionless
    const xTitle = simName === 'TestC1' ? 'z' : 'x (dimensionless)';
    const yTitle = simName === 'TestC1' ? 'Value (×10^6)' : 'Dimensionless Value';

    // Optional scaling for TestC1 to avoid micro prefix
    let aPlot = a;
    let qPlot = q;
    if (simName === 'TestC1') {
        const scale = 1e6; // multiply data by 10^6 for display (remove micro prefix)
        aPlot = a.map(v => v * scale);
        qPlot = q.map(v => v * scale);
        // Adjust stored global min/max for scaled display
        if (!drawFrame.testC1ScaledRange) {
            drawFrame.testC1ScaledRange = true;
            drawFrame.ymin *= scale;
            drawFrame.ymax *= scale;
        }
    }

    const data = [
        {
            x: x,
            y: aPlot,
            name: simName === 'TestC1' ? 'A(z, t)' : 'a(x, τ)',
            mode: "lines",
            line: { color: "orange", width: 3 }
        },
        {
            x: x,
            y: qPlot,
            name: simName === 'TestC1' ? 'Q(z, t)' : 'q(x, τ)',
            mode: "lines",
            line: { color: "blue", width: 3 }
        }
    ];

    const layout = {
        title: `${prefix ? prefix + ' — ' : ''}τ = ${tau.toFixed(5)}`,
        xaxis: { title: xTitle },
        yaxis: { title: yTitle, range: [drawFrame.ymin, drawFrame.ymax] },
        margin: { t: 40, l: 40, b: 50, r: 20 }
    };

    // Use newPlot only on first render; on updates, preserve current zoom
    if (!drawFrame.initialized) {
        Plotly.newPlot("plot", data, layout);
        drawFrame.initialized = true;
    } else {
        const plotDiv = document.getElementById("plot");
        if (plotDiv && plotDiv.layout) {
            const cur = plotDiv.layout;
            if (cur.xaxis && cur.xaxis.range) {
                layout.xaxis.range = cur.xaxis.range.slice();
            }
            if (cur.yaxis && cur.yaxis.range) {
                layout.yaxis.range = cur.yaxis.range.slice();
            }
        }
        Plotly.react("plot", data, layout);
    }
}

/**********************************************
 * START
 **********************************************/
loadSimulation();

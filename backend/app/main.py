from flask import Flask, jsonify, request
from flask_cors import CORS
from .simulation.healthy import simulate_t, simulate_z, simulate_wk


# Create Flask app
app = Flask(__name__)
CORS(app)

SIMULATIONS = {}


def _init_simulations():
    """
    Precompute all simulations once at startup
    for fast API responses.
    """
    global SIMULATIONS
    SIMULATIONS["t"] = simulate_t()
    SIMULATIONS["z"] = simulate_z()
    SIMULATIONS["wk"] = simulate_wk()


# Load simulation data once
_init_simulations()


@app.route("/")
def home():
    return {
        "status": "backend ok",
        "simulations": list(SIMULATIONS.keys())
    }


@app.route("/data")
def data():
    """
    API endpoint:
    /data?name=t
    /data?name=z
    /data?name=wk
    """
    sim_name = request.args.get("name", "t")

    if sim_name not in SIMULATIONS:
        return (
            jsonify({
                "error": f"Simulation '{sim_name}' not found.",
                "available": list(SIMULATIONS.keys())
            }),
            400,
        )

    z, t, P = SIMULATIONS[sim_name]

    # Reduce data size
    step = 2

    return jsonify({
        "name": sim_name,
        "z": z.tolist(),
        "time": t[::step].tolist(),
        "pressure": P[::step].tolist()
    })


# Local dev only (Render uses gunicorn)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

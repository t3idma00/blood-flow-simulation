from flask import Flask, jsonify, request
from flask_cors import CORS
from .simulation.healthy import simulate_t, simulate_z, simulate_wk

# Flask App
app = Flask(__name__)
CORS(app)

# Cache for precomputed simulations
SIMULATIONS = {}


def _init_simulations():
    """
    Run simulations once to avoid recalculating them on every API call.
    Each simulation returns arrays: z, t, P
    """
    global SIMULATIONS
    SIMULATIONS["t"] = simulate_t()
    SIMULATIONS["z"] = simulate_z()
    SIMULATIONS["wk"] = simulate_wk()


# Run on startup
_init_simulations()


@app.route("/")
def home():
    return {
        "status": "backend ok",
        "available_simulations": list(SIMULATIONS.keys())
    }


@app.route("/data")
def data():
    """
    GET /data?name=t
    Available options:
        name = t, z, wk
    Returns JSON containing:
        z array
        time array
        pressure array (2D, time_index x z_index)
    """
    sim_name = request.args.get("name", "t")

    if sim_name not in SIMULATIONS:
        return {
            "error": f"Simulation '{sim_name}' not found.",
            "available": list(SIMULATIONS.keys())
        }, 400

    z, t, P = SIMULATIONS[sim_name]

    # Downsample to reduce payload size
    step = 2
    z_list = z.tolist()
    t_list = t[::step].tolist()
    P_list = P[::step].tolist()

    return jsonify({
        "name": sim_name,
        "z": z_list,
        "time": t_list,
        "pressure": P_list
    })


# Only used locally (Render uses gunicorn)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

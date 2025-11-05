from flask import Flask, jsonify, send_from_directory
from simulation import run_simulation
import os

# Create Flask app, serving static files from frontend folder
app = Flask(__name__, static_folder="../frontend")

# Run simulation once when the server starts
z, time, P = run_simulation()

# Convert pressure from Pa to mmHg
P_mmHg = P / 133.322

# Serve main frontend page
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Serve any other frontend static files (JS, CSS, etc.)
@app.route("/<path:path>")
def send_static(path):
    return send_from_directory(app.static_folder, path)

# API route for simulation data
@app.route("/data")
def data():
    step = 5
    return jsonify({
        "z": z.tolist(),
        "time": time[::step].tolist(),
        "pressure": P_mmHg[::step].tolist()
    })

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)

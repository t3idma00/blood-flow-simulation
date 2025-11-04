from flask import Flask, jsonify, send_from_directory
from simulation import run_simulation

app = Flask(__name__, static_folder="../frontend")

# Run simulation once when server starts
z, time, P = run_simulation()

# Convert pressure from Pa to mmHg for clinical relevance
P_mmHg = P / 133.322

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def send_static(path):
    return send_from_directory("../frontend", path)

@app.route("/data")
def data():
    step = 5
    return jsonify({
        "z": z.tolist(),
        "time": time[::step].tolist(),
        "pressure": P_mmHg[::step].tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)

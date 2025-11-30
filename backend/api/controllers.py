# backend-python/api/controllers.py

from simulations.healthy_domain_sim import run_simulation
from simulations.artery_sim_full import run_artery_simulation


def get_simulation():
    """
    First PDE (dimensionless a, q vs x, τ) used with Three.js
    """
    x, times, a_arr, q_arr = run_simulation()
    return {
        "x": x.tolist(),
        "times": times.tolist(),
        "a": a_arr.tolist(),
        "q": q_arr.tolist(),
    }


def get_artery_simulation():
    """
    Full healthy artery + Windkessel simulation.
    All values are already JSON-friendly.
    """
    return run_artery_simulation()

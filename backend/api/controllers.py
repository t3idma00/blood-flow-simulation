from .registry import SIMULATION_REGISTRY

def normalize_result(result):
    """
    Ensures the simulation output format is always standardized.
    Acceptable formats:
       (x, times, a, q)
       (x, times, a_arr, q_arr)
    """
    if len(result) != 4:
        raise RuntimeError("Simulation must return 4 values")

    x, times, a, q = result
    return x, times, a, q


def run_simulation_by_name(name):
    if name not in SIMULATION_REGISTRY:
        raise KeyError(f"Simulation '{name}' not found")

    sim_func = SIMULATION_REGISTRY[name]
    result = sim_func()     # call simulation

    x, times, a, q = normalize_result(result)

    def to_list(v):
        return v.tolist() if hasattr(v, "tolist") else v

    return {
        "x": to_list(x),
        "times": to_list(times),
        "a": to_list(a),
        "q": to_list(q),
    }


def list_simulations():
    return list(SIMULATION_REGISTRY.keys())


def run_simulation_raw(name):
    """
    Run a simulation and return its raw output without normalization.
    Useful for simulations that return dictionaries or custom payloads
    (e.g., artery_sim_full time-series data).
    """
    if name not in SIMULATION_REGISTRY:
        raise KeyError(f"Simulation '{name}' not found")
    sim_func = SIMULATION_REGISTRY[name]
    return sim_func()

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

    return {
        "x": x.tolist(),
        "times": times.tolist(),
        "a": a.tolist(),
        "q": q.tolist(),
    }


def list_simulations():
    return list(SIMULATION_REGISTRY.keys())

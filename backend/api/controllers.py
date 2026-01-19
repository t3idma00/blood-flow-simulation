from .registry import SIMULATION_REGISTRY
import inspect


def _resolve_simulation_name(name: str) -> str:
    """Resolve a simulation name in a case-insensitive way.

    This allows frontends to request e.g. "Test_model_laxw_half_step" even if
    the registry key is "test_model_laxw_half_step" (or vice versa).
    """
    if name in SIMULATION_REGISTRY:
        return name

    lower_name = name.lower()
    for key in SIMULATION_REGISTRY.keys():
        if key.lower() == lower_name:
            return key

    raise KeyError(f"Simulation '{name}' not found")


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


def run_simulation_by_name(name, **params):
    resolved_name = _resolve_simulation_name(name)
    sim_func = SIMULATION_REGISTRY[resolved_name]

    # Filter params to only those accepted by the target simulation
    if params:
        sig = inspect.signature(sim_func)
        accepted = {
            k: v
            for k, v in params.items()
            if v is not None and k in sig.parameters
        }
        result = sim_func(**accepted) if accepted else sim_func()
    else:
        result = sim_func()  # call simulation with defaults

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
    resolved_name = _resolve_simulation_name(name)
    sim_func = SIMULATION_REGISTRY[resolved_name]
    return sim_func()

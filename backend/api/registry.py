import importlib
import os
import simulations

SIMULATION_REGISTRY = {}

sim_dir = os.path.dirname(simulations.__file__)

# autoload all .py files that contain run_simulation()
for file in os.listdir(sim_dir):
    if file.endswith(".py") and not file.startswith("__"):
        module_name = f"simulations.{file[:-3]}"
        module = importlib.import_module(module_name)

        if hasattr(module, "run_simulation"):
            SIMULATION_REGISTRY[file[:-3]] = module.run_simulation

print("Loaded simulations:", SIMULATION_REGISTRY.keys())

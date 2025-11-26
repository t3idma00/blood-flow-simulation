import numpy as np


def _base_simulation(num_t: int = 240, num_z: int = 160, kind: str = "t"):
    """
    Generates a simple pressure wave simulation for demonstration.

    Returns:
        z: (Nz,) numpy array
        t: (Nt,) numpy array
        P: (Nt, Nz) pressure field in mmHg
    """

    # Geometry and simulation duration
    L = 0.15     # artery length [m]
    T = 1.0      # duration [s]

    # Spatial and temporal grids
    z = np.linspace(0, L, num_z)
    t = np.linspace(0, T, num_t)

    Z, Tm = np.meshgrid(z, t)

    # Baseline pressure
    P0 = 80.0

    # Set parameters for each simulation mode
    if kind == "t":
        amp = 40.0
        decay = 3.0
        phase = 6.0
        offset = 0.0
    elif kind == "z":
        amp = 35.0
        decay = 1.5
        phase = 10.0
        offset = np.pi / 6
    elif kind == "wk":
        amp = 25.0
        decay = 0.8
        phase = 8.0
        offset = np.pi / 3
    else:
        raise ValueError(f"Unknown simulation kind: {kind}")

    # Pressure wave model
    P = P0 + amp * np.exp(-decay * Z / L) * np.sin(
        2 * np.pi * Tm / T - phase * Z / L + offset
    )

    P = np.clip(P, 0, None)

    return z, t, P


def simulate_t():
    return _base_simulation(kind="t")


def simulate_z():
    return _base_simulation(kind="z")


def simulate_wk():
    return _base_simulation(kind="wk")

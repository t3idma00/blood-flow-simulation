# backend/simulation.py
import numpy as np

def run_simulation():
    """Simplified healthy-vessel model (β = 0) returning pressure along vessel."""
    rho = 1060.0      # blood density (kg/m³)
    L = 0.1           # vessel length (m)
    Nz = 100          # Number of divisions of the vessel
    Nt = 200         # number of time steps
    dz = L / (Nz - 1)
    dt = 0.001
    z = np.linspace(0, L, Nz)
    P = np.zeros((Nt, Nz))

    def inlet_pressure(t):
        return 13300 + 2000 * np.sin(2 * np.pi * 1.5 * t)

    for n in range(1, Nt):
        t = n * dt
        P[n, 0] = inlet_pressure(t)
        P[n, 1:] = 0.98 * P[n-1, :-1]  # simple forward damping
    time = np.arange(Nt) * dt
    return z, time, P

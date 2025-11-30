# backend-python/simulations/healthy_domain_sim.py
import numpy as np

def run_simulation(save_every: int = 50):
    """
    Runs the MacCormack simulation and returns:
    x        : (N,) spatial grid
    times    : (num_frames,) time samples
    a_arr    : (num_frames, N)
    q_arr    : (num_frames, N)
    """
    # --- Original parameters ---
    K3 = 0.0002          # damping coefficient
    N  = 400             # number of spatial points
    dx = 1.0 / N         # grid spacing
    x  = (np.arange(N) + 0.5) * dx   # cell-centered coordinates

    tau_final = 2.6
    CFL = 0.4
    dt  = CFL * dx
    Nt  = int(tau_final / dt)
    dt  = tau_final / Nt             # adjust dt so final time is exact

    # solution arrays with ghost cells
    a = np.zeros(N + 2)
    q = np.zeros(N + 2)

    # --- Initial conditions ---
    def bump(x, center, width, amp):
        s = (x - center) / width
        out = np.zeros_like(x)
        mask = np.abs(s) < 1
        out[mask] = amp * 0.5 * (1 + np.cos(np.pi * s[mask]))
        return out

    eps = 0.020
    a[1:-1] = bump(x, center=0.7, width=eps, amp=0.10)
    q[1:-1] = bump(x, center=0.4, width=eps, amp=0.02)

    # --- Boundary conditions ---
    def apply_bc(a, q):
        a[0]  = a[1]
        q[0]  = q[1]
        a[-1] = a[-2]
        q[-1] = q[-2]

    apply_bc(a, q)

    # --- MacCormack method ---
    def mac_cormack(a, q):
        a_p = a.copy()   # predictor arrays
        q_p = q.copy()

        # Predictor step (forward differences)
        for i in range(1, N + 1):
            a_p[i] = a[i] - (dt/dx)*(q[i+1] - q[i])
            q_p[i] = q[i] - (dt/dx)*(a[i+1] - a[i]) - dt*K3*q[i]

        apply_bc(a_p, q_p)

        # Corrector step
        a_new = a.copy()
        q_new = q.copy()

        for i in range(1, N + 1):
            a_new[i] = 0.5*(a[i] + a_p[i] - (dt/dx)*(q_p[i] - q_p[i-1]))
            q_new[i] = 0.5*(q[i] + q_p[i]
                            - (dt/dx)*(a_p[i] - a_p[i-1])
                            - dt*K3*q_p[i])

        return a_new, q_new

    # --- Simulation loop ---
    a_hist = []
    q_hist = []
    t_hist = []

    tau = 0.0

    for n in range(Nt + 1):

        if n % save_every == 0:
            a_hist.append(a[1:-1].copy())
            q_hist.append(q[1:-1].copy())
            t_hist.append(tau)

        apply_bc(a, q)
        a, q = mac_cormack(a, q)
        tau += dt

    a_arr = np.array(a_hist)
    q_arr = np.array(q_hist)
    times = np.array(t_hist)

    return x, times, a_arr, q_arr


if __name__ == "__main__":
    # quick manual test
    x, times, a_arr, q_arr = run_simulation()
    print("x shape    :", x.shape)
    print("times shape:", times.shape)
    print("a_arr shape:", a_arr.shape)
    print("q_arr shape:", q_arr.shape)
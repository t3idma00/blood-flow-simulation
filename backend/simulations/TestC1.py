import numpy as np

def run_simulation():
    """
    Run the TestC1 MacCormack solver and return
    (x, times, a_arr, q_arr) for the web frontend.

    x: positions array (length Nx+1)
    times: list of time points (length Nt+1)
    a_arr: list of arrays for A at each time (length Nt+1, each length Nx+1)
    q_arr: list of arrays for Q at each time (length Nt+1, each length Nx+1)
    """

    # PHYSICAL PARAMETERS with SI units
    D_ref = 3.0e-3
    R_ref = D_ref / 2.0
    A_ref = np.pi * R_ref**2
    c = 1.0

    # NUMERICAL DOMAIN
    L = 1.0
    Nx = 400
    dz = L / Nx
    z = np.linspace(0.0, L, Nx+1)

    Tfinal = 2.6
    CFL = 0.4
    dt = CFL * dz / c
    Nt = int(Tfinal / dt) + 1
    dt = Tfinal / Nt

    epsilon = 0.02

    def bump(z, center, eps, amp=1.0):
        s = (z - center) / eps
        out = np.zeros_like(z)
        mask = np.abs(s) < 1
        out[mask] = amp * 0.5 * (1 + np.cos(np.pi * s[mask]))
        return out

    amp_A = 1 * A_ref
    amp_Q = 1 * 1e-6

    Q = amp_Q * bump(z, 0.4, epsilon)
    A = amp_A * bump(z, 0.7, epsilon)

    Q_store = np.zeros((Nt+1, Nx+1))
    A_store = np.zeros((Nt+1, Nx+1))
    Q_store[0,:] = Q.copy()
    A_store[0,:] = A.copy()

    def apply_BC(Q, A):
        A[0]  = A[1]
        Q[0]  = Q[1]
        A[-1] = A[-2]
        Q[-1] = Q[-2]

    for n in range(1, Nt + 1):
        apply_BC(Q, A)
        FQ = A
        FA = Q
        Qp = Q.copy()
        Ap = A.copy()
        Qp[:-1] = Q[:-1] - dt/dz*(FQ[1:] - FQ[:-1]) - (dt/5)*Q[:-1]
        Ap[:-1] = A[:-1] - dt/dz*(FA[1:] - FA[:-1])
        apply_BC(Qp, Ap)
        FQp = Ap
        FAp = Qp
        Q = 0.5*(Q + Qp - dt/dz*(FQp - np.roll(FQp,1)) - (dt/5)*Qp)
        A = 0.5*(A + Ap - dt/dz*(FAp - np.roll(FAp,1)))
        apply_BC(Q, A)
        Q_store[n,:] = Q
        A_store[n,:] = A

    # Build outputs for web: add A_ref to area to make absolute area
    x = z
    times = [i*dt for i in range(Nt+1)]
    a_arr = [A_ref + A_store[n,:] for n in range(Nt+1)]
    q_arr = [Q_store[n,:] for n in range(Nt+1)]
    return x.tolist(), times, [a.tolist() for a in a_arr], [q.tolist() for q in q_arr]

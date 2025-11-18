import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 1.0
Nx = 400
dz = L / Nx
z = np.linspace(0, L, Nx+1)

Tfinal = 2.6
c = 1.0              # wave speed 
CFL = 0.4
dt = CFL * dz / c
Nt = int(Tfinal / dt) + 1
dt = Tfinal / Nt

epsilon = 0.02


# Smooth cosine bump
def bump(z, center, eps, amp=1.0):
    s = (z - center) / eps
    out = np.zeros_like(z)
    mask = np.abs(s) < 1
    out[mask] = amp * 0.5 * (1 + np.cos(np.pi * s[mask]))
    return out


# Initial conditions
Q = bump(z, 0.4, epsilon)
A = bump(z, 0.7, epsilon)


# snapshots
save_times = [0, 0.25, 0.5, 1.0, 1.7, 2.6]
saved = {t: None for t in save_times}
saved[0] = (Q.copy(), A.copy())

def flux(Q, A):
    return np.array([A, Q])  # F = (A, Q)

t = 0
for n in range(1, Nt+1):

    # Apply  BCs
    Q[0], Q[-1] = Q[1], Q[-2]
    A[0], A[-1] = A[1], A[-2]

    # Compute fluxes
    F_Q, F_A = flux(Q, A)


    Qp = Q.copy()
    Ap = A.copy()

    Qp[:-1] = Q[:-1] - dt/dz * (F_Q[1:] - F_Q[:-1]) - (dt/5)*Q[:-1]
    Ap[:-1] = A[:-1] - dt/dz * (F_A[1:] - F_A[:-1])

    # Apply BCs to predictor
    Qp[0], Qp[-1] = Qp[1], Qp[-2]
    Ap[0], Ap[-1] = Ap[1], Ap[-2]

    # Flux of predicted values
    F_Qp, F_Ap = flux(Qp, Ap)

    # Corrector step
    Q_new = 0.5*(Q + Qp - dt/dz*(F_Qp - np.roll(F_Qp, 1)) - (dt/5)*Qp)
    A_new = 0.5*(A + Ap - dt/dz*(F_Ap - np.roll(F_Ap, 1)))

    Q, A = Q_new, A_new
    t = n * dt

    # Save snapshots
    for ts in save_times:
        if saved[ts] is None and t >= ts - 1e-6:
            saved[ts] = (Q.copy(), A.copy())

# Plot results
for ts in save_times:
    Qs, As = saved[ts]
    plt.figure(figsize=(10,4))
    plt.plot(z, Qs, label='Q(z,t)')
    plt.plot(z, As, label='A(z,t)')
    plt.title(f"MacCormack solution at t = {ts}")
    plt.xlabel("z")
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    plt.show()



#need to  add units
#Need to recheck codes 18/11/2025
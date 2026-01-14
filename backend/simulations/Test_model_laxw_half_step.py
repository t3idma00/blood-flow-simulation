import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# TEST MODEL: DAMPED LINEAR WAVE SYSTEM

#   Q_t + c^2 A_z + delta Q = 0
#   A_t + Q_z = 0

# PARAMETERS
c = 1.0 
delta = 1.0 / 5.0
alpha = 1.0

# SPATIAL DOMAIN
L = 1.0
N = 300
dz = L / (N - 1)
z = np.linspace(0, L, N)

# TIME DISCRETIZATION
T_FINAL = 3.0
dt = 5e-4
Nt = int(T_FINAL / dt)

CFL = c * dt / dz
print(f"CFL = {CFL:.3f} (must be <= 1)")

# INITIAL CONDITIONS (SMOOTH GAUSSIANS)
sigma = 4.0 * dz

A = 0.02 * np.exp(-((z - 0.7) ** 2) / sigma**2)
Q = 0.02 * np.exp(-((z - 0.4) ** 2) / sigma**2)

# BOUNDARY CONDITIONS (FREE FLOW / NON-REFLECTING)
def inlet_bc(A, Q):
    Wm = Q[1] - c * A[1]
    A[0] = -Wm / (2 * c)
    Q[0] = Wm / 2

def outlet_bc(A, Q):
    Wp = Q[-2] + c * A[-2]
    A[-1] = Wp / (2 * c)
    Q[-1] = Wp / 2

# STORAGE
snap_every = 10
A_snap = []
Q_snap = []
times = []

# TIME INTEGRATION (LAX–WENDROFF)
for n in range(Nt):

    inlet_bc(A, Q)
    outlet_bc(A, Q)

    A_half = np.zeros(N - 1)
    Q_half = np.zeros(N - 1)

    for i in range(N - 1):
        A_half[i] = 0.5 * (A[i] + A[i + 1]) \
                    - 0.5 * dt * (Q[i + 1] - Q[i]) / dz

        Q_half[i] = 0.5 * (Q[i] + Q[i + 1]) \
                    - 0.5 * dt * (
                        c**2 * (A[i + 1] - A[i]) / dz
                        + delta * 0.5 * (Q[i] + Q[i + 1])
                    )

    A_new = A.copy()
    Q_new = Q.copy()

    for i in range(1, N - 1):
        A_new[i] = A[i] - dt * (Q_half[i] - Q_half[i - 1]) / dz
        Q_new[i] = Q[i] - dt * (
            c**2 * (A_half[i] - A_half[i - 1]) / dz
            + delta * 0.5 * (Q_half[i] + Q_half[i - 1])
        )

    inlet_bc(A_new, Q_new)
    outlet_bc(A_new, Q_new)

    A, Q = A_new, Q_new

    if n % snap_every == 0:
        A_snap.append(A.copy())
        Q_snap.append(Q.copy())
        times.append(n * dt)

A_snap = np.array(A_snap)
Q_snap = np.array(Q_snap)
times = np.array(times)

# VISUALIZATION: A(z,t) AND Q(z,t) WITH SLIDER
fig, ax = plt.subplots(figsize=(9, 4))
plt.subplots_adjust(bottom=0.25)

line_A, = ax.plot(
    z, A_snap[0],
    lw=2, color="tab:blue",
    label="Area perturbation A"
)

line_Q, = ax.plot(
    z, Q_snap[0],
    lw=2, color="tab:orange",
    label="Flow perturbation Q"
)

ax.set_xlabel("z [m]")
ax.set_ylabel("Perturbation amplitude")
ax.set_title("Evolution of A(z,t) and Q(z,t)")
ax.grid(True)
ax.legend()

ax.set_ylim(
    1.1 * min(np.min(A_snap), np.min(Q_snap)),
    1.1 * max(np.max(A_snap), np.max(Q_snap))
)

# Time slider
ax_time = plt.axes([0.15, 0.08, 0.7, 0.04])
time_slider = Slider(
    ax=ax_time,
    label="Time [s]",
    valmin=times[0],
    valmax=times[-1],
    valinit=times[0]
)

def update(val):
    idx = np.argmin(np.abs(times - val))
    line_A.set_ydata(A_snap[idx])
    line_Q.set_ydata(Q_snap[idx])
    ax.set_title(f"A(z,t) and Q(z,t) at t = {times[idx]:.3f} s")
    fig.canvas.draw_idle()

time_slider.on_changed(update)

plt.show()

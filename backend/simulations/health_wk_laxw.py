import numpy as np
import matplotlib.pyplot as plt

"""
Linearized 1D blood flow in an artery with:

PDE system (perturbations):
    A_t + Q_z        = 0
    Q_t + c0^2 A_z   = -δ Q

Tube law (linearized):
    P̃ = α Ã

Inlet (z=0): prescribed pressure P_in(t) using Blackman–Harris waveform
    Ã(0,t) = (P_in(t) - P_ref)/α
    Q̃(0,t) from PDE with one-sided derivative.

Outlet (z=L): 4-element linearized Windkessel (eq. 24):
    dÃ/dt + (1/(Rd C)) Ã =
        (Lint/α) d²Q̃/dt²
      + (1/α)(Rp + Lint/(Rd C)) dQ̃/dt
      + (1/α)(1/C + Rp/(Rd C)) Q̃

We discretize:
- Interior: Lax–Wendroff
- Inlet & outlet Q from PDE one-sided A_z
- Outlet A from Windkessel ODE 
"""

# Physical & numerical parameters

# Geometry
L = 0.15          # artery length [m]
dz = 1.0e-3       # spatial step [m]  
Nx = int(L/dz) + 1
z = np.linspace(0, L, Nx)

# Time
T_heart = 1.0     # one heart period [s]
T_final = 1.0     # simulate 1 s 
dt = 1.0e-5       # time step [s]
Nt = int(T_final / dt)

# Blood and wall properties
rho = 1060.0      # density [kg/m^3]
mu  = 3.5e-3      # dynamic viscosity [Pa·s]

D_ref = 3.0e-3    # reference diameter [m]
r_ref = D_ref / 2
A_ref = np.pi * r_ref**2  # reference area [m^2]

E = 1.5e6         # Young's modulus [Pa]
h = 3.0e-4        # wall thickness [m]

# Tube law stiffness: P̃ = α Ã
alpha = E * h / (2.0 * np.pi * r_ref**3)

# Wave speed and damping
c0 = np.sqrt(alpha * A_ref / rho)
delta = 8.0 * np.pi * mu / (rho * A_ref)

CFL = c0 * dt / dz
print(f"Nx = {Nx}, Nt = {Nt}")
print(f"Wave speed c0 = {c0:.2f} m/s,   delta = {delta:.3f} 1/s")
print(f"CFL number = {CFL:.3f} (should be < 1)")


# Inlet pressure: Blackman–Harris waveform

# Timing parameters 
LD = 0.60; LP = 0.55; LT = 0.55
tP = 0.38; tD = 0.05; tT = 0.20
betaD = 0.4; betaP = 1.0; betaT = 0.3
c_rel = 60.0 / 60.0   # 60 bpm normalization 

# Amplitudes (mmHg -> Pa)
mmHg_to_Pa = 133.322
A_mmHg = 50.0
A_P = A_D = A_T = A_mmHg * mmHg_to_Pa

# Base diastolic pressure
P_dias = 87.0 * mmHg_to_Pa
P_ref = P_dias

# Blackman–Harris window coefficients
a0, a1, a2, a3 = 0.35875, 0.48829, 0.14128, 0.01168

def bh_window(t_local):
    """
    4-term Blackman–Harris window w(t/T_heart) on [0, T_heart].
    """
    if t_local < 0 or t_local > T_heart:
        return 0.0
    tau = t_local / T_heart
    return (a0
            - a1 * np.cos(2.0*np.pi*tau)
            + a2 * np.cos(4.0*np.pi*tau)
            - a3 * np.cos(6.0*np.pi*tau))

tau_grid = np.linspace(0, T_heart, 2001)
w_vals = np.array([bh_window(t) for t in tau_grid])
w_max = np.max(w_vals)

def inlet_pressure(t):
    """
    P_in(t) = P_dias + three BH-shaped pulses (P, D, T).
    """
    t_mod = t % T_heart

    def pulse(Ai, beta, Li, ti):
        arg = (t_mod - ti) / (Li / c_rel)
        return Ai * beta * bh_window(arg) / w_max

    return (P_dias
            + pulse(A_P, betaP, LP, tP)
            + pulse(A_D, betaD, LD, tD)
            + pulse(A_T, betaT, LT, tT))

# Plot inlet pressure over the simulated time
t_plot = np.linspace(0, T_final, 1000)
P_plot = np.array([inlet_pressure(t) for t in t_plot])

plt.figure()
plt.plot(t_plot, P_plot / mmHg_to_Pa)
plt.xlabel("Time [s]")
plt.ylabel("Inlet Pressure [mmHg]")
plt.title("Inlet Pressure (Blackman–Harris)")
plt.grid(True)
plt.tight_layout()
plt.show()

#  4-element Windkessel parameters and coefficients

Rp   = 6.7e8     # proximal resistance
Rd   = 1.0e10    # distal resistance
Cw   = 1.5e-11   # compliance
Lint = 1.0e4     # inertance

# Equation (24): dA_out/dt + (1/(Rd*Cw)) A_out = c2 Q'' + c1 Q' + c0 Q
lambda_A = 1.0 / (Rd * Cw)
c2 = Lint / alpha
c1 = (Rp + Lint / (Rd * Cw)) / alpha
c0 = (1.0 / Cw + Rp / (Rd * Cw)) / alpha

# Allocate solution arrays and monitoring

# Perturbations: A = A_ref + A_tilde;  Q = Q_tilde
A_tilde = np.zeros(Nx)
Q_tilde = np.zeros(Nx)

# Windkessel state: outlet area perturbation
A_out_state = 0.0

# Outlet flow history: [Q^n, Q^{n-1}, Q^{n-2}]
Q_out_hist = np.zeros(3)

# Monitor at three positions: inlet, mid, outlet
monitor_z = np.array([0.0, L/2, L])
monitor_idx = [np.argmin(np.abs(z - zz)) for zz in monitor_z]

t_hist = []
# total area A_ref + A_tilde
A_hist = [[], [], []]
# flow perturbation  
Q_hist = [[], [], []]
# total pressure P_ref + α A_tilde  
P_hist = [[], [], []]  

# Time-stepping loop: Lax–Wendroff + Windkessel BC

for n in range(Nt):
    t = n * dt

    #  Inlet boundary
    P_in = inlet_pressure(t)                   
    A_tilde[0] = (P_in - P_ref) / alpha        

    #  Outlet boundary
    A_tilde[-1] = A_out_state                 

    #  Lax–Wendroff update for interior nodes 
    A_new = A_tilde.copy()
    Q_new = Q_tilde.copy()

    for i in range(1, Nx-1):
        # spatial derivatives
        dA  = (A_tilde[i+1] - A_tilde[i-1]) / (2.0 * dz)
        dQ  = (Q_tilde[i+1] - Q_tilde[i-1]) / (2.0 * dz)
        d2A = (A_tilde[i+1] - 2.0 * A_tilde[i] + A_tilde[i-1]) / (dz**2)
        d2Q = (Q_tilde[i+1] - 2.0 * Q_tilde[i] + Q_tilde[i-1]) / (dz**2)

        # Lax–Wendroff updates
        A_new[i] = A_tilde[i] - dt * dQ + 0.5 * dt**2 * c0**2 * d2A
        Q_new[i] = (Q_tilde[i]
                    - dt * c0**2 * dA
                    + 0.5 * dt**2 * c0**2 * d2Q
                    - dt * delta * Q_tilde[i])

    #  Inlet flow Q(0,t) from PDE (one-sided A_z) ----
    A_z_in = (A_tilde[1] - A_tilde[0]) / dz
    Q_new[0] = Q_tilde[0] + dt * (-c0**2 * A_z_in - delta * Q_tilde[0])

    #  Outlet flow Q(L,t) from PDE (one-sided A_z) ----
    A_z_out = (A_tilde[-1] - A_tilde[-2]) / dz
    Q_new[-1] = Q_tilde[-1] + dt * (-c0**2 * A_z_out - delta * Q_tilde[-1])

    #  Windkessel: update outlet area A_out_state using Q_new[-1] ----
    Q_out_hist[2] = Q_out_hist[1]
    Q_out_hist[1] = Q_out_hist[0]
    Q_out_hist[0] = Q_new[-1]

    if n >= 2:
        # first and second time derivatives of outlet flow
        dQdt   = (Q_out_hist[0] - Q_out_hist[1]) / dt
        d2Qdt2 = (Q_out_hist[0] - 2.0*Q_out_hist[1] + Q_out_hist[2]) / dt**2
    else:
        dQdt = 0.0
        d2Qdt2 = 0.0

    # RHS of Windkessel ODE (eq. 24):
    # dA_out/dt + lambda_A A_out = c2 Q'' + c1 Q' + c0 Q
    RHS = c2 * d2Qdt2 + c1 * dQdt + c0 * Q_new[-1]
    dA_dt_out = -lambda_A * A_out_state + RHS

    A_out_state = A_out_state + dt * dA_dt_out

    # Outlet area at new time: Ã(L,t^{n+1}) = A_out_state
    A_new[-1] = A_out_state

    #  Update global state
    A_tilde = A_new
    Q_tilde = Q_new

    #  Record histories at inlet / mid / outlet
    t_curr = t + dt
    t_hist.append(t_curr)
    for k, idx in enumerate(monitor_idx):
        A_hist[k].append(A_ref + A_tilde[idx])          # total area
        Q_hist[k].append(Q_tilde[idx])                  # flow perturbation
        P_hist[k].append(P_ref + alpha * A_tilde[idx])  # total pressure

# Convert histories to arrays
t_hist = np.array(t_hist)
A_hist = [np.array(a) for a in A_hist]
Q_hist = [np.array(q) for q in Q_hist]
P_hist = [np.array(p) for p in P_hist]

# pressure, flow, area vs time at inlet/mid/outlet

labels = ["Inlet (z=0)", "Mid (z=L/2)", "Outlet (z=L)"]

plt.figure(figsize=(10, 8))

# Pressure
plt.subplot(3,1,1)
for k in range(3):
    plt.plot(t_hist, P_hist[k] / mmHg_to_Pa, label=labels[k])
plt.ylabel("Pressure [mmHg]")
plt.title("Pressure at Inlet, Mid, and Outlet")
plt.grid(True)
plt.legend()

# Flow
plt.subplot(3,1,2)
for k in range(3):
    plt.plot(t_hist, Q_hist[k], label=labels[k])
plt.ylabel("Flow Q̃ [m³/s]")
plt.title("Flow at Inlet, Mid, and Outlet")
plt.grid(True)
plt.legend()

# Area
plt.subplot(3,1,3)
for k in range(3):
    plt.plot(t_hist, A_hist[k], label=labels[k])
plt.ylabel("Area [m²]")
plt.xlabel("Time [s]")
plt.title("Area at Inlet, Mid, and Outlet")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

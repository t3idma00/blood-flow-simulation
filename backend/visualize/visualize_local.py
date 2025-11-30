# backend-python/visualize/visualize_local.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from simulations.healthy_domain_sim import run_simulation

def main():
    x, times, a_arr, q_arr = run_simulation()

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.25)

    idx0 = 0

    line_q, = ax.plot(x, q_arr[idx0], color='tab:blue', label="q(x, τ)")
    line_a, = ax.plot(x, a_arr[idx0], color='tab:orange', label="a(x, τ)")

    ax.set_xlabel("x (dimensionless)")
    ax.set_ylabel("Dimensionless Value")
    ax.set_title(f"τ = {times[idx0]:.5f}")
    ax.grid(True)
    ax.legend()

    ymin = min(a_arr.min(), q_arr.min())
    ymax = max(a_arr.max(), q_arr.max())
    padding = 0.2 * (ymax - ymin)
    ax.set_ylim(ymin - padding, ymax + padding)

    slider_ax = plt.axes([0.15, 0.10, 0.70, 0.03])
    time_slider = Slider(
        ax=slider_ax,
        label="Time Index",
        valmin=0,
        valmax=len(times) - 1,
        valinit=idx0,
        valstep=1
    )

    def update(val):
        i = int(time_slider.val)
        line_q.set_ydata(q_arr[i])
        line_a.set_ydata(a_arr[i])
        ax.set_title(f"MacCormack scheme, τ = {times[i]:.5f}")
        fig.canvas.draw_idle()

    time_slider.on_changed(update)

    plt.show()

if __name__ == "__main__":
    main()

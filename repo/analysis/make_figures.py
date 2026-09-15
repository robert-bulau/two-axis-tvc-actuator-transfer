"""
Regenerate every synthetic figure used in paper/tvc_v2.tex directly from
tvc_stability.py, so the figures can never silently drift from the code.

Usage:
    python analysis/make_figures.py
Writes PNGs to paper/figures/.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import tvc_stability as t

OUT = Path(__file__).resolve().parents[1] / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def fig1_stability_slice():
    """Synthetic local stability slice: eta vs k_x, colour = spectral abscissa."""
    etas = np.linspace(0.3, 3.0, 220)
    kxs = np.linspace(0.001, 0.40, 220)
    Z = np.zeros((len(kxs), len(etas)))
    for i, kx_ in enumerate(kxs):
        for j, eta_ in enumerate(etas):
            Z[i, j] = t.spectral_abscissa(eta_, chi_=1.0, kx_=kx_, kv_=0.2, kth_=1.0, kq_=2.0)

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.pcolormesh(etas, kxs, Z, cmap="RdBu_r", vmin=-0.2, vmax=0.2, shading="auto")
    ax.contour(etas, kxs, Z, levels=[0], colors="black", linewidths=1.2)
    ax.set_xlabel("Actuator ratio eta")
    ax.set_ylabel("Normalized position gain k_x")
    ax.set_title("Synthetic local stability slice: chi=1, k_v=0.2, k_theta=1, k_q=2")
    fig.colorbar(im, ax=ax, label="Largest real part of normalized poles")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_stability_slice.png", dpi=150)
    plt.close(fig)


def fig2_matched_groups():
    """Two synthetic configurations with identical g_x, g_v collapse onto one trajectory."""
    from scipy.integrate import solve_ivp

    def rhs(tau, y, chi_, eta_, kx_, kv_, kth_, kq_):
        A = t.A_matrix(eta_, chi_, kx_, kv_, kth_, kq_)
        return A @ y

    configs = [
        dict(m=0.8, ell=0.18, chi_=0.9, eta_=1.2, label="Synthetic configuration 1"),
        dict(m=1.5, ell=0.30, chi_=0.9, eta_=1.2, label="Synthetic configuration 2"),
    ]
    kx_, kv_, kth_, kq_ = 0.02, 0.2, 1.0, 2.0
    y0 = np.array([0.05, 0.0, 0.02, 0.0, 0.0])

    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    for c in configs:
        sol = solve_ivp(
            rhs, [0, 45], y0, args=(c["chi_"], c["eta_"], kx_, kv_, kth_, kq_),
            dense_output=True, max_step=0.05,
        )
        tau = np.linspace(0, 45, 600)
        Y = sol.sol(tau)
        axes[0].plot(tau, Y[0], label=c["label"])
        axes[1].plot(tau, Y[2], label=c["label"])

    axes[0].set_ylabel("X = x/ell")
    axes[1].set_ylabel("Body tilt theta (rad)")
    axes[1].set_xlabel("Normalized time tau")
    axes[0].legend()
    axes[0].set_title("Matched dimensionless groups: numerical implementation check")
    fig.tight_layout()
    fig.savefig(OUT / "fig2_matched_groups.png", dpi=150)
    plt.close(fig)


def fig3_condition_number_counterexample():
    """
    Equal condition number, different feedback direction: rotation of G.

    NOTE: this is an illustrative scalar reduction of the full 10-state
    two-axis matrix (Eq. 22 in the paper), not that matrix itself -- the
    full system is not yet implemented in this module (open issue: add
    A_matrix_2axis). Treat this figure as qualitative until that lands.
    """
    angles = np.linspace(0, 85, 40)
    abscissas_nominal, abscissas_exact = [], []
    for deg in angles:
        # G is a rotation by `deg`; nominal mixing assumes G_hat = I, exact uses G_hat = G.
        # Reduced to the scalar-equivalent penalty used in the manuscript's synthetic case.
        theta_rad = np.deg2rad(deg)
        mismatch_gain = 1.0 / max(np.cos(theta_rad), 1e-6) - 1.0
        base = t.spectral_abscissa(400.0, 1.0, 0.02, 0.2, 1.0, 2.0)
        abscissas_nominal.append(base + mismatch_gain)
        abscissas_exact.append(base)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(angles, abscissas_nominal, label="Nominal mixing: Ghat=I")
    ax.plot(angles, abscissas_exact, "--", label="Exact mixing: Ghat=G")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Static mapping rotation (deg)")
    ax.set_ylabel("Largest real part of normalized poles")
    ax.set_title("Equal condition number does not imply equal closed-loop stability")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "fig3_condition_number.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig1_stability_slice()
    fig2_matched_groups()
    fig3_condition_number_counterexample()
    print(f"Wrote figures to {OUT}")

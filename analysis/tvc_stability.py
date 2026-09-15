"""
tvc_stability.py

Analytical core for "Load-Dependent Actuator Bandwidth Limits Calibration
Transfer in Two-Axis Thrust-Vector-Controlled Rocket Analogues".

This module implements, and can independently re-derive, every closed-form
result in Section 3 of the manuscript (paper/tvc_v2.tex):

  - the linearised closed-loop system matrix A (Eq. 14 / Eq. A in the paper)
  - the characteristic polynomial P(s) (Eq. 15)
  - the attitude-subsystem stability condition (Proposition 1)
  - the five-dimensionless-group reduction (Proposition 2)
  - the non-minimum-phase gain ceiling (Proposition 3)

Nothing here depends on measured hardware data. This is the synthetic /
analytical layer only; see data/ for the (currently empty) measured dataset
and its schema.

All functions use plain numpy + sympy so the derivations can be checked
independently of this repository.
"""
from __future__ import annotations

import numpy as np
import sympy as sp


# ---------------------------------------------------------------------------
# Symbolic layer
# ---------------------------------------------------------------------------

s, eta, chi, kx, kv, kth, kq = sp.symbols(
    "s eta chi k_x k_v k_theta k_q", positive=True
)


def symbolic_A() -> sp.Matrix:
    """Symbolic closed-loop system matrix, Eq. (14) of the manuscript."""
    return sp.Matrix(
        [
            [0, 1, 0, 0, 0],
            [0, 0, chi, 0, -chi],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [-eta * kth * kx, -eta * kth * kv, -eta * kth, -eta * kq, -eta],
        ]
    )


def symbolic_characteristic_polynomial() -> sp.Expr:
    """P(s) = det(sI - A), expanded. Should equal `paper_polynomial()`."""
    A = symbolic_A()
    return sp.expand(sp.det(s * sp.eye(5) - A))


def paper_polynomial() -> sp.Expr:
    """The closed-form polynomial as printed in the manuscript, Eq. (15)."""
    return sp.expand(
        s**5
        + eta * s**4
        + eta * (kq - chi * kth * kv) * s**3
        + eta * kth * (1 - chi * kx) * s**2
        + eta * chi * kth * kv * s
        + eta * chi * kth * kx
    )


def check_polynomial_matches_matrix() -> bool:
    """Proposition-free sanity check: does Eq. (15) equal det(sI - A)?"""
    return sp.simplify(symbolic_characteristic_polynomial() - paper_polynomial()) == 0


# ---------------------------------------------------------------------------
# Numeric layer
# ---------------------------------------------------------------------------


def A_matrix(eta_: float, chi_: float, kx_: float, kv_: float, kth_: float, kq_: float) -> np.ndarray:
    """Numeric closed-loop system matrix for given dimensionless parameters."""
    return np.array(
        [
            [0, 1, 0, 0, 0],
            [0, 0, chi_, 0, -chi_],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [-eta_ * kth_ * kx_, -eta_ * kth_ * kv_, -eta_ * kth_, -eta_ * kq_, -eta_],
        ]
    )


def spectral_abscissa(
    eta_: float, chi_: float = 1.0, kx_: float = 0.02, kv_: float = 0.2,
    kth_: float = 1.0, kq_: float = 2.0,
) -> float:
    """Largest real part of the closed-loop eigenvalues (negative = stable)."""
    return float(max(np.linalg.eigvals(A_matrix(eta_, chi_, kx_, kv_, kth_, kq_)).real))


def find_boundary(
    chi_: float = 1.0, kx_: float = 0.02, kv_: float = 0.2,
    kth_: float = 1.0, kq_: float = 2.0,
    lo: float = 0.5001, hi: float = 20.0,
) -> float:
    """
    Root of the spectral abscissa in eta (Proposition 1's cascade generalisation).

    Requires a sign change in [lo, hi]; raises ValueError otherwise (this
    happens e.g. once g_x = chi*kx exceeds the ceiling of Proposition 3, at
    which point the system is unstable for every eta and there is no root).
    """
    from scipy.optimize import brentq

    return float(
        brentq(lambda e: spectral_abscissa(e, chi_, kx_, kv_, kth_, kq_), lo, hi, xtol=1e-12)
    )


def attitude_only_boundary(kth_: float, kq_: float) -> float:
    """Proposition 1: eta* = k_theta / k_q for the attitude-only subsystem."""
    return kth_ / kq_


def nmp_gain_ceiling(chi_: float, kv_: float, kth_: float, kq_: float) -> float:
    """
    Proposition 3: ideal-actuator (eta -> infinity) ceiling on g_x = chi*k_x.

    Returns g_x_max. The system is unstable for every eta once chi*k_x
    exceeds this value, regardless of actuator bandwidth.
    """
    gv = chi_ * kv_
    a1 = kq_ - gv * kth_
    a3 = gv * kth_
    return (a1 * a3 * kth_ - a3**2) / (kth_ * a1 * kq_)


def five_group_invariance_check(
    g_x: float, g_v: float, kth_: float, kq_: float, eta_: float,
    chi_values: tuple[float, ...] = (0.4, 1.0, 3.3),
) -> list[float]:
    """
    Proposition 2: the spectrum depends on chi only through g_x = chi*k_x and
    g_v = chi*k_v. Returns the spectral abscissa for each chi in chi_values
    with k_x, k_v backed out so that g_x, g_v stay fixed -- all values should
    be identical.
    """
    return [
        spectral_abscissa(eta_, chi_, g_x / chi_, g_v / chi_, kth_, kq_)
        for chi_ in chi_values
    ]

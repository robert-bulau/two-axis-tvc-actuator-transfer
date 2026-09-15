"""
Regression tests: every numerical claim made in paper/tvc_v2.tex (Section 4
and Table 1/2) must reproduce here to the stated tolerance. If a derivation
in the manuscript changes, these tests must be updated in the same commit
and the reason noted in the commit message.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tvc_stability as t


def test_polynomial_matches_matrix_determinant():
    assert t.check_polynomial_matches_matrix()


def test_full_cascade_boundary_matches_paper():
    # Section 4: eta* = 0.602676 for chi=1, kx=0.02, kv=0.2, ktheta=1, kq=2
    assert t.find_boundary() == pytest.approx(0.602676, abs=1e-6)


def test_abscissa_at_eta_0p5_matches_paper():
    assert t.spectral_abscissa(0.5) == pytest.approx(0.044274, abs=1e-6)


def test_abscissa_at_eta_1_is_stable():
    assert t.spectral_abscissa(1.0) < 0


def test_attitude_only_boundary_proposition_1():
    # Proposition 1: eta* = k_theta / k_q for the attitude-actuator subsystem
    assert t.attitude_only_boundary(1.0, 2.0) == pytest.approx(0.5)


def test_five_group_reduction_proposition_2():
    # chi must not appear once g_x = chi*k_x, g_v = chi*k_v are held fixed
    values = t.five_group_invariance_check(
        g_x=0.02, g_v=0.2, kth_=1.0, kq_=2.0, eta_=0.8,
        chi_values=(0.4, 1.0, 3.3),
    )
    assert max(values) - min(values) < 1e-10


def test_nmp_gain_ceiling_proposition_3():
    # For chi=1, kv=0.2, ktheta=1, kq=2 the ceiling is 0.08889 (paper Section 4)
    ceiling = t.nmp_gain_ceiling(chi_=1.0, kv_=0.2, kth_=1.0, kq_=2.0)
    assert ceiling == pytest.approx(0.0888888888888889, abs=1e-9)


@pytest.mark.parametrize(
    "gx,should_have_boundary",
    [
        (0.005, True),
        (0.02, True),
        (0.05, True),
        (0.08, True),
        (0.0888, True),
        (0.09, False),  # past the ceiling: no eta stabilises the loop
    ],
)
def test_two_mechanism_table(gx, should_have_boundary):
    # Reproduces Table "Two mechanisms bounding the stable region"
    if should_have_boundary:
        eta_star = t.find_boundary(kx_=gx, lo=0.5001, hi=5000.0)
        assert eta_star > 0.5
    else:
        with pytest.raises(ValueError):
            t.find_boundary(kx_=gx, lo=0.5001, hi=5000.0)


def test_ceiling_sign_change_at_multiple_parameter_sets():
    # Confirms Proposition 3 with parameters other than the paper's headline set
    for chi_, kv_, kth_, kq_ in [(1, 0.2, 1, 2), (0.6, 0.35, 1.4, 2.5), (2.0, 0.1, 0.8, 1.6)]:
        ceiling = t.nmp_gain_ceiling(chi_, kv_, kth_, kq_)
        below = t.spectral_abscissa(400.0, chi_, 0.97 * ceiling / chi_, kv_, kth_, kq_)
        above = t.spectral_abscissa(400.0, chi_, 1.03 * ceiling / chi_, kv_, kth_, kq_)
        assert below < 0 < above

from collections import namedtuple
import scipy.optimize

from uhb import general
from uhb import psi


def required_download(delta, E, I, EAF, w_o):
    """ Returns the required download for stability. """
    term1 = 1.16 - 4.76 * (E * I * w_o / delta) ** 0.5 / EAF
    term2 = ((delta * w_o) / (E * I)) ** 0.5
    return term1 * EAF * term2


def required_sand_cover_height(required_resistance, D, gamma, f, c):
    """ Returns the sand cover height to provide the required uplift resistance.
    """

    def solve_sand(H):
        return psi.R_max(H, D, gamma, f) - required_resistance

    def solve_clay(H):
        return psi.P_otc6486(H, D, gamma, c) - required_resistance

    # TODO: exception catch for solve
    if c > 0:
        return scipy.optimize.newton(solve_clay, 1e-3)

    else:
        return scipy.optimize.newton(solve_sand, 1e-3)


def run_analytical_calc(data):
    D, t, t_coat = data.D, data.t, data.t_coat
    delta_P = data.P_i - data.P_e
    delta_T = data.T - data.T_a
    v, alpha, E, rho_p = data.v, data.alpha, data.E, data.rho_p
    rho_coat, rho_cont = data.rho_coat, data.rho_cont
    delta = max(data.deltas)
    soil_type = data.soil_type
    gamma, f, c = data.gamma_s, data.f, data.c
    rho_sw, g = data.rho_sw, data.g

    D_tot = general.total_outside_diameter(D, t_coat)
    A_i = general.internal_area(D, t)
    A_s = general.area_of_steel(D, t)
    EAF = abs(general.effective_axial_force(
        0, delta_P, A_i, v, A_s, E, alpha, delta_T))
    I = general.second_moment_of_area(D, t)
    w_o = general.submerged_weight(
        D, t, t_coat, rho_p, rho_coat, rho_cont, rho_sw, g)
    w = required_download(delta, E, I, EAF, w_o)
    q = max(w - w_o, 0)
    H = required_sand_cover_height(q, D_tot, gamma, f, c)

    Results = namedtuple("Results", "I EAF w_o w q H")
    return Results(I, EAF, w_o, w, q, H)

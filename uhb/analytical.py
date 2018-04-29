import scipy.optimize

import uhb.general as general
import uhb.soil as soil


def required_download(delta, E, I, EAF, w_o):
    """ Returns the required download for stability. """
    return (1.16 - 4.76 * (E * I * w_o / delta) ** 0.5 / EAF) * EAF * (
        delta * w_o / E * I) ** 0.5


def required_sand_cover_height(required_resistance, D, f):

    def solve(H):
        return soil.sand_otc_6335(H, D, f) - required_resistance

    # TODO: exception catch for solve 
    return scipy.optimize.newton(solve, 1e-3)


def run_analytical_calc(data):
    D, t, t_coat = data["D"], data["t"], data["t_coat"]
    delta_P = data["P_i"] - data["P_e"]
    delta_T = data["T"] - data["T_a"]
    v, alpha, E, rho_p = data["v"], data["alpha"], data["E"], data["rho_p"]
    rho_coat = data["rho_coat"]
    delta = max(data["deltas"])
    soil_type, f = data["soil_type"], data["f"]
    rho_sw, g = data["rho_sw"], data["g"]

    A_i = general.internal_area(D, t)
    A_s = general.area_of_steel(D, t)
    EAF = abs(general.effective_axial_force(0, delta_P, A_i, v, A_s, E, alpha, delta_T))
    I = general.second_moment_of_area(D, t)
    w_o = general.submerged_weight(D, t, rho_p, rho_sw, g)
    w = required_download(delta, E, I, EAF, w_o)
    q = max(w - w_o, 0)
    H = required_sand_cover_height(q, D, f)

    return {"EAF": EAF, "w_o": w_o, "w": w, "q": q, "H": H}

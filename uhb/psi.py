""" Pipe-Soil Interaction module """

from math import pi, sin, tan, exp, sqrt, radians
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

from uhb import general


#########
# GENERAL
#########


def cot(a):
    return 1 / tan(a)


def calculate_soil_weight(gamma, D, H):
    return gamma * D * H


def depth_to_centre(D_o, h):
    return 0.5 * D_o + h


#######################
# ALA BURIED STEEL PIPE
#######################


def Nch(c, H, D):
    """ Horizontal bearing capacity factor for sand
    """
    if c == 0:
        return 0

    x = H / D

    return min(6.752 + 0.065 * x - 11.063 / (x + 1) ** 2 + 7.119 / (x + 1) ** 3, 9)


def Nqh(psi, H, D):
    """ Horizontal bearing capacity factor
    """
    if psi == 0:
        return 0

    if psi < 20:
        psi = 20
    elif psi > 45:
        psi = 45

    psi_range = [20, 25, 30, 35, 40, 45]
    a = [2.399, 3.332, 4.565, 6.816, 10.959, 17.658]
    b = [0.439, 0.839, 1.234, 2.019, 1.783, 3.309]
    c = [-0.03, -0.09, -0.089, -0.146, 0.045, 0.048]
    d = [
        1.059 * 10 ** -3,
        5.606 * 10 ** -3,
        4.275 * 10 ** -3,
        7.651 * 10 ** -3,
        -5.425 * 10 ** -3,
        -6.443 * 10 ** -3,
    ]
    e = [
        -1.754 * 10 ** -5,
        -1.319 * 10 ** -4,
        -9.159 * 10 ** -5,
        -1.683 * 10 ** -4,
        -1.153 * 10 ** -4,
        -1.299 * 10 ** -4,
    ]
    x = H / D

    def par(case):
        return interp1d(psi_range, case)(psi)

    return (par(a) + par(b) * x + par(c) * x ** 2 + par(d) * x ** 3 + par(e) * x ** 4)


def Ncv(c, H, D):
    """ Vertical uplift factor for sand
    """
    if c == 0:
        return 0

    return min(2 * H / D, 10)


def Nqv(psi, H, D):
    """ Vertical uplift factor for sand
    """
    if psi == 0:
        return 0

    return min(psi * H / 44 / D, Nq(psi))


def Nc(psi, H, D):
    """ Soil bearing capacity factor
    """
    return (
        cot(radians(psi + 0.001))
        * (exp(pi * tan(radians(psi + 0.001)))
            * tan(radians(45 + (psi + 0.001) / 2)) ** 2 - 1)
    )


def Nq(psi):
    """ Soil bearing capacity factor
    """
    return exp(pi * tan(radians(psi))) * tan(radians(45 + psi / 2)) ** 2


def Ngamma(psi):
    """ Soil bearing capacity factor
    """
    return exp(0.18 * psi - 2.5)


# AXIAL


def delta_t(soil_type):
    """ Displacement at Tu
    """
    delta_ts = {
        "dense sand": 0.003,
        "loose sand": 0.005,
        "stiff clay": 0.008,
        "soft clay": 0.01,
    }
    return delta_ts.get(soil_type, ValueError("Unknown soil type."))


def Tu(D, H, c, f, psi, gamma):
    """ Maximum axial soil force per unit length
    """
    alpha = 0.608 - 0.123 * c - 0.274 / (c ** 2 + 1) + 0.695 / (c ** 3 + 1)
    K0 = 1 - sin(radians(psi))
    return (
        pi * D * alpha * c + pi * D * H * gamma *
        (1 + K0) / 2 * tan(radians(f * psi))
    )


# LATERAL


def delta_p(H, D):
    """ Displacement at Pu
    """
    return min(0.04 * (H + D / 2), 0.1 * D)


def Pu(c, H, D, psi, gamma):
    """ Maximum lateral soil force per unit length
    """
    return Nch(c, H, D) * c * D + Nqh(psi, H, D) * gamma * H * D


# VERTICAL UPLIFT


def delta_qu(soil, H, D):
    """ Displacement at Qu
    """
    if "sand" in soil:
        return min(0.01 * H, 0.1 * D)

    elif "clay" in soil:
        return min(0.1 * H, 0.2 * D)

    else:
        raise ValueError("Unknown soil type.")


def Qu(psi, c, D, gamma, H):
    """ Vertical uplift soil resistance per unit length
    """
    return Ncv(c, H, D) * c * D + Nqv(psi, H, D) * gamma * H * D


# VERTICAL BEARING


def delta_qd(soil, D):
    """ Displacement at Qu
    """
    if "sand" in soil:
        return 0.1 * D

    elif "clay" in soil:
        return 0.2 * D

    else:
        raise ValueError("Unknown soil type.")


def Qd(psi, c, D, gamma, H, rho_sw):
    """ Vertical bearing soil resistance per unit length
    """
    return (
        Nc(psi, H, D) * c * D + Nq(psi) * gamma * H * D + Ngamma(psi)
        * (gamma + (rho_sw * 9.81)) * D ** 2 / 2
    )


###############
# DNVGL-RP-F114
###############


def F_uplift_d(soil_type, gamma, H, D):
    """Returns drained uplift resistance.

    DNVGL-RP-F114 - Equation (5.6)

    :param soil_type: str
    :param gamma: Submerged weight of soil [N/m^-3]
    :param H: Cover height (above pipe) [m]
    :param D: Outer pipe diameter [m]
    """
    # TODO: interpolate f using psi_s
    resistance_factors = {
        "loose sand": 0.29,
        "medium sand": 0.47,
        "dense sand": 0.62,
    }
    f = resistance_factors[soil_type]
    return gamma * H * D + gamma * D ** 2 * (0.5 - pi / 8) + f * gamma * (
        H + 0.5 * D) ** 2


#############
# DNV-RP-F110
#############


def R_max(H, D, gamma, f):
    """ Returns the uplift resistance of a pipe in sand.

    DNV-RP-F110 2007 - Equation (B.3)
    """
    return (1 + f * H / D) * (gamma * H * D)


##########
# OTC 6486
##########


def P_otc6486(H, D, gamma, c):
    """ Returns the uplift resistance of cohesive materials.

    OTC6486 - Equation (7)
    """
    return gamma * H * D + 2 * H * c


# def DepthEquilibrium(psi, c, D, gamma, soil):
#     R = D / 2
#     widths = [w for w in np.arange(D / 6, D + 0.1 * D / 6, D / 6)]
#     penetrations = [R - sqrt(R ** 2 - (w / 2) ** 2) for w in widths]
#     Qds = [Qd(psi, c, w, gamma, 0) for w in widths]
#     p_max = 5 * D
#     F_max = p_max / delta_qd(soil, D) * Qds[-1]
#     penetrations.append(p_max)
#     Qds.append(F_max)
#     Fd = np.stack((penetrations, Qds), axis=-1)
#     return Fd


def gen_uplift_spring(data, h, model="asce"):
    """ Returns vertical uplift soil spring as a tuple of displacement and 
    resistance based on chosen soil model.
    """
    D_o = general.total_outside_diameter(data.D, data.t_coat)
    H = depth_to_centre(D_o, h)
    disp = delta_qu(data.soil_type, H, D_o)
    springs = {
        "asce": (disp, Qu(data.psi_s, data.c, D_o, data.gamma_s, H)),
        "f114": (disp, F_uplift_d(data.soil_type, data.gamma_s, H, D_o)),
        "f110": (disp, R_max(H, D_o, data.gamma_s, data.f)),
        "otc": (disp, P_otc6486(H, D_o, data.gamma_s, data.c)),
    }
    return springs.get(model, ValueError("Unknown uplift soil model."))


def gen_bearing_spring(data, h, model="asce"):
    """ Returns bearing soil spring as a tuple of displacement and resistance
    based on chosen soil model.
    """
    D_o = general.total_outside_diameter(data.D, data.t_coat)
    H = depth_to_centre(D_o, h)
    disp = delta_qd(data.soil_type, D_o)
    springs = {
        "asce": (disp,
                 Qd(data.psi_s, data.c, D_o, data.gamma_s, H, data.rho_sw)),
    }
    return springs.get(model, ValueError("Unknown bearing soil model."))


def gen_axial_spring(data, h, model="asce"):
    """ Returns axial soil spring as a tuple of displacement and resistance
    based on chosen soil model.
    """
    D_o = general.total_outside_diameter(data.D, data.t_coat)
    disp = delta_t(data.soil_type)
    springs = {
        "asce": (disp,
                 Tu(D_o, depth_to_centre(D_o, h), data.c, data.f, data.psi_s,
                    data.gamma_s)
                 ),
    }
    return springs.get(model, ValueError("Unknown axial soil model."))


def gen_lateral_spring(data, h, model="asce"):
    """ Returns lateral soil spring as a tuple of displacement and resistance
    based on chosen soil model.
    """
    D_o = general.total_outside_diameter(data.D, data.t_coat)
    H = depth_to_centre(D_o, h)
    disp = delta_p(H, D_o)
    springs = {
        "asce": (disp, Pu(data.c, H, D_o, data.psi_s, data.gamma_s)),
    }
    return springs.get(model, ValueError("Unknown lateral soil model."))

import math


def area_of_steel(D, t):
    return math.pi * (D ** 2 - (D - 2 * t) ** 2) / 4


def area_of_coating(D, t_coat):
    return math.pi * ((D + 2 * t_coat) ** 2 - D ** 2) / 4


def internal_area(D, t):
    return math.pi * (D - 2 * t) ** 2 / 4


def total_area(D, t_coat):
    return math.pi * (D + 2 * t_coat) ** 2 / 4


def second_moment_of_area(D, t):
    return math.pi * (D ** 4 - (D - 2 * t) ** 4) / 64


def effective_axial_force(H, delta_P, A_i, v, A_s, E, alpha, delta_T):
    """ Returns the effective axial force of a totally restrained pipe in the
    linear elastic stress range based on thick wall stress formulation.

    DNVGL-ST-F101 Equation (4.10)
    """
    return H - delta_P * A_i * (1 - 2 * v) - A_s * E * alpha * delta_T


def submerged_weight(D, t, rho_p, rho_sw, g):
    weight_of_pipe = g * area_of_steel(D, t) * rho_p
    bouyancy = g * math.pi * (0.5 * D)**2 * rho_sw
    return weight_of_pipe - bouyancy

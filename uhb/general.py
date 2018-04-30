import math


def total_outside_diameter(D, t_coat):
    return D + 2 * t_coat


def area_of_steel(D, t):
    return math.pi * (D ** 2 - (D - 2 * t) ** 2) / 4


def area_of_coating(D, t_coat):
    return math.pi * ((D + 2 * t_coat) ** 2 - D ** 2) / 4


def internal_area(D, t):
    return math.pi * (D - 2 * t) ** 2 / 4


def total_area(D_o):
    return math.pi * D_o ** 2 / 4


def second_moment_of_area(D, t):
    return math.pi * (D ** 4 - (D - 2 * t) ** 4) / 64


def effective_axial_force(H, delta_P, A_i, v, A_s, E, alpha, delta_T):
    """ Returns the effective axial force of a totally restrained pipe in the
    linear elastic stress range based on thick wall stress formulation.

    DNVGL-ST-F101 Equation (4.10)
    """
    return H - delta_P * A_i * (1 - 2 * v) - A_s * E * alpha * delta_T


def submerged_weight(D, t, t_coat, rho_p, rho_coat, rho_cont, rho_sw, g):
    D_o = total_outside_diameter(D, t_coat)
    A_e = total_area(D_o)
    A_s = area_of_steel(D, t)
    A_coat = area_of_coating(D, t_coat)
    A_i = area_of_coating(D, t_coat)    
    return g * (A_s * rho_p + A_coat * rho_coat + A_i * rho_cont - A_e * rho_sw)

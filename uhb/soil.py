from math import pi, sin, tan, exp, sqrt, radians
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def cot(a):
    return 1 / tan(a)


def calculate_soil_weight(gamma, D, H):
    return gamma * D * H


def burial_depth_to_pipe_centreline(D_o, h):
    return 0.5 * D_o + h


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
        * (
            exp(pi * tan(radians(psi + 0.001)))
            * tan(radians(45 + (psi + 0.001) / 2))
            ** 2
            - 1
        )
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


def axial_delta_asce(soil):
    """ Displacement at Tu
    """
    delta_ts = {
        "dense sand": 0.003, "loose sand": 0.005, "stiff clay": 0.008, "soft clay": 0.01
    }
    return delta_ts.get(soil, ValueError("Unknown soil type."))


def axial_resistance_asce(D, H, c, f, psi, gamma):
    """ Maximum axial soil force per unit length
    """
    alpha = 0.608 - 0.123 * c - 0.274 / (c ** 2 + 1) + 0.695 / (c ** 3 + 1)
    K0 = 1 - sin(radians(psi))
    return (
        pi * D * alpha * c + pi * D * H * gamma * (1 + K0) / 2 * tan(radians(f * psi))
    )


# LATERAL


def lateral_delta_asce(H, D):
    """ Displacement at Pu
    """
    return min(0.04 * (H + D / 2), 0.1 * D)


def lateral_resistance_asce(c, H, D, psi, gamma):
    """ Maximum lateral soil force per unit length
    """
    return Nch(c, H, D) * c * D + Nqh(psi, H, D) * gamma * H * D


# VERTICAL UPLIFT


def uplift_delta_asce(soil, H, D):
    """ Displacement at Qu
    """
    if "sand" in soil:
        return min(0.01 * H, 0.1 * D)

    elif "clay" in soil:
        return min(0.1 * H, 0.2 * D)

    else:
        raise ValueError("Unknown soil type.")


def uplift_resistance_asce(psi, c, D, gamma, H):
    """ Vertical uplift soil resistance per unit length
    """
    return Ncv(c, H, D) * c * D + Nqv(psi, H, D) * gamma * H * D


def uplift_resistance_sand_dnvf114(soil, gamma, H, D):
    """Returns drained uplift resistance.

    DNVGL-RP-F114 - Equation (5.5)

    :param soil: str
    :param gamma: Submerged weight of soil []
    :param H: Cover height (above pipe) [m]
    :param D: Outer pipe diameter [m]
    """
    # TODO: interpolate f using psi
    resistance_factors = {"loose sand": 0.29, "medium sand": 0.47, "dense sand": 0.62}
    f = resistance_factors[soil]
    return gamma * H * D + gamma * D ** 2 * (0.5 - pi / 8) + f * gamma * (
        H + 0.5 * D
    ) ** 2


def uplift_resistance_sand_dnvf110(H, D, gamma, f):
    return (1 + f * H / D) * (gamma * H * D)


def uplift_resistance_clay_otc6486(H, D, gamma, c):
    return gamma * H * D + 2 * H * c


# VERTICAL BEARING


def bearing_delta_asce(soil, D):
    """ Displacement at Qu
    """
    if "sand" in soil:
        return 0.1 * D

    elif "clay" in soil:
        return 0.2 * D

    else:
        raise ValueError("Unknown soil type.")


def bearing_resistance_asce(psi, c, D, gamma, H, rho_sw):
    """ Vertical bearing soil resistance per unit length
    """
    return (
        Nc(psi, H, D)
        * c
        * D
        + Nq(psi)
        * gamma
        * H
        * D
        + Ngamma(psi)
        * (gamma + (rho_sw * 9.81))
        * D
        ** 2
        / 2
    )


def DepthEquilibrium(psi, c, D, gamma, soil):
    R = D / 2
    widths = [w for w in np.arange(D / 6, D + 0.1 * D / 6, D / 6)]
    penetrations = [R - sqrt(R ** 2 - (w / 2) ** 2) for w in widths]
    Qds = [Qd(psi, c, w, gamma, 0) for w in widths]
    p_max = 5 * D
    F_max = p_max / delta_qd(soil, D) * Qds[-1]
    penetrations.append(p_max)
    Qds.append(F_max)
    Fd = np.stack((penetrations, Qds), axis=-1)
    return Fd


def generate_soil_springs(data, h, models):
    D_o = data["D"] + 2 * data["t_coat"]
    psi, c, gamma, f = data["psi"], data["c"], data["gamma_s"], data["f"]
    H = burial_depth_to_pipe_centreline(D_o, h)
    soil, rho_sw = data["soil_type"], data["rho_sw"]
    l_imp = data["el_lengths"]["imp"]
    l_int = data["el_lengths"]["int"]
    l_feed = data["el_lengths"]["feed"]

    rcs = {}

    # vertical uplift
    uplift_mob = uplift_delta_asce(soil, H, D_o)

    if models["uplift"] == "otc":
        uplift = uplift_resistance_clay_otc6486(H, D_o, gamma, c)
    elif models["uplift"] == "f114":
        uplift = uplift_resistance_sand_dnvf114(soil, gamma, H, D_o)
    elif models["uplift"] == "f110":
        uplift = uplift_resistance_sand_dnvf110(H, D_o, gamma, f)
    else:
        uplift = uplift_resistance_asce(psi, c, D_o, gamma, H)

    soil_weight = calculate_soil_weight(gamma, D_o, h)
    peak = uplift - soil_weight

    rcs["1"] = {"deltas": [100 * uplift_mob], "forces": [100 * peak]}
    rcs["5"] = {
        "deltas": [uplift_mob, h, 100],
        "forces": [peak * l_imp, -soil_weight * l_imp, -soil_weight * l_imp],
    }

    # axial
    axial_mob = axial_delta_asce(soil)
    axial = axial_resistance_asce(D_o, H, c, f, psi, gamma)
    rcs["7"] = {"deltas": [axial_mob, 100], "forces": [axial * l_imp, axial * l_imp]}
    rcs["8"] = {"deltas": [axial_mob, 100], "forces": [axial * l_int, axial * l_int]}
    rcs["9"] = {"deltas": [axial_mob, 100], "forces": [axial * l_feed, axial * l_feed]}

    # lateral
    lateral_mob = lateral_delta_asce(H, D_o)
    lateral = lateral_resistance_asce(c, H, D_o, psi, gamma)
    rcs["2"] = {"deltas": [lateral_mob, 100], "forces": [lateral, lateral]}
    rcs["4"] = {"deltas": [lateral_mob, 100], "forces": [lateral, lateral]}

    # vertical bearing
    bearing_mob = bearing_delta_asce(soil, D_o)
    bearing = bearing_resistance_asce(psi, c, D_o, gamma, H, rho_sw)
    rcs["3"] = {"deltas": [bearing_mob, 100], "forces": [bearing, bearing]}
    rcs["6"] = {
        "deltas": [bearing_mob, 100], "forces": [bearing * l_imp, bearing * l_imp]
    }
    rcs["10"] = {
        "deltas": [bearing_mob, 100], "forces": [bearing * l_imp, bearing * l_imp]
    }

    return rcs


def plot_soil_springs(soil_springs):

    fig, ax = plt.subplots()

    ax.plot(
        soil_springs["vertical_uplift"][0],
        soil_springs["vertical_uplift"][1],
        label="vertical_uplift",
    )

    ax.set_title(f"Soil Stiffness")
    ax.set_xlabel("Displacement [m]")
    ax.set_ylabel("Resistance [N/m]")
    ax.grid()
    ax.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


# fig.savefig(f"outputs/{soil_type}.png")

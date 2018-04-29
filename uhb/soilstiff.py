import math
from scipy import optimize
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

def soil_weight(gamma, D, H):
    return gamma * D * H

# VERTICAL UPLIFT

def vertical_uplift_mobilisation(soil, H, D):
    if "sand" in soil:
        return min(0.02 * H, 0.1 * D)

    elif "clay" in soil:
        return min(0.2 * H, 0.2 * D)

    else:
        raise ValueError("Unknown soil type.")

def N_cv(c, H, D):

    if c == 0:
        return 0
    
    return min(2 * H / D, 10)

def N_q(psi):
    return math.exp(math.pi * math.tan(psi)) * math.tan((math.pi / 4) + 0.5 * psi) ** 2

def N_qv(psi, H, D):
    
    if psi == 0:
        return 0
    
    return min(math.degrees(psi) * H / 44 / D, N_q(psi))

def uplift_resistance(shear_factor, H, D, gamma):
    """DNV-RP-F110 2007
    """
    return (1 + shear_factor * H / D) * (gamma * H * D)

# AXIAL

def axial_mobilisation(soil):
    delta_ts = {
        "dense sand": 0.003, "loose sand": 0.005, "stiff clay": 0.008, "soft clay": 0.01
    }
    return delta_ts.get(soil, ValueError("Unknown soil type."))

def axial_soil_force(D, c, H, f, gamma_bar, psi):
    alpha = 0.608 - 0.123 * c - 0.274 / (c ** 2 + 1) + 0.695 / (c ** 3 + 1)
    K_0 = 1 - (math.sin(psi))
    return math.pi * D * alpha * c + math.pi * D * H * gamma_bar * (
        0.5 * (1 + K_0)
    ) * math.tan(f * psi)

# LATERAL

def lateral_mobilisation(H, D, bound='mid'):
    
    mob = {
        'lower': 0.1 * D,
        'mid': 0.125 * D,
        'upper': 1.15 * D,
    }
    
    return mob.get(bound, ValueError("Unknown soil type."))

def N_ch(c, H, D):

    if c == 0:
        return 0
    x = H / D
    
    return min(6.752 + 0.065 * x - 11.063 / (x + 1) ** 2 + 7.119 / (x + 1) ** 3, 9)

def N_qh(psi, H, D):
    
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
        -6.443 * 10 ** -3
    ]
    e = [
        -1.754 * 10 ** -5,
        -1.319 * 10 ** -4,
        -9.159 * 10 ** -5,
        -1.683 * 10 ** -4,
        -1.153 * 10 ** -4,
        -1.299 * 10 ** -4
    ]
    x = H / D
    def par(case):
        return interp1d(psi_range, case)(psi)

    return (
        par(a) + par(b) * x + par(c) * x ** 2 + par(d) * x ** 3 + par(e) * x ** 4
    )

# VERTICAL BEARING

def vertical_downward_mobilisation(soil, D):
    
    if "sand" in soil:
        return 0.1 * D

    elif "clay" in soil:
        return 0.2 * D

    else:
        raise ValueError("Unknown soil type.")

def cot(psi):
    return 1 / math.tan(psi)

def N_c(psi):
    return (N_q(psi) - 1)*cot(psi)

def N_gamma(psi):
    return 2*(N_q(psi) + 1)*math.tan(psi)

def vertical_bearing_force(psi, c, D, gamma, H):

    return (
        N_c(psi) * c * D + N_q(psi) * gamma * H * D + 0.5 * N_gamma(psi) * (gamma + (1025 * 9.81)) * D ** 2
    )

if __name__ == "__main__":
    D = 0.1731
    soil = "dense sand"
    psi = math.radians(32)
    c = 0
    gamma_bar = 18000
    W_tot = 214.78
    burial_depth = 1
    f = 0.6
    shear_factor = 0.3
    el_lengths = [0.3, 1.5, 15]

    print(soil_weight(gamma_bar, D, burial_depth))


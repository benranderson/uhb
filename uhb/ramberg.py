import numpy as np
from math import log


def ramberg_osgood(SMYS, ey, UTS, eu, E):

    alpha_ri = E * ey / SMYS - 1
    N = log((eu - UTS / E) * (E / alpha_ri / SMYS), (UTS / SMYS))

    def e(s):
        return s / E + alpha_ri * SMYS / E * (s / SMYS) ** N

    return [[e(s), s] for s in np.logspace(log(9 * SMYS / 10, 10), log(UTS, 10), num=7)]


def nonlinear_rc(data):
    SMYS, SMYS_e = data.SMYS, data.SMYS_e
    SMTS, SMTS_e = data.SMTS, data.SMTS_e
    E = data.E

    ro1 = ramberg_osgood(SMYS, SMYS_e, SMTS, SMTS_e, E)
    return "RC,11," + ",".join(str(i) for il in ro1 for i in il) + "\n"


if __name__ == "__main__":
    outer_SMYS = 415e6
    outer_e_SMYS = 0.005
    outer_UTS = 520e6
    outer_e_UTS = 0.215
    outer_E = 2.07e11

    ro1 = ramberg_osgood(outer_SMYS, outer_e_SMYS,
                         outer_UTS, outer_e_UTS, outer_E)
    print("RC,11," + ",".join(str(i) for il in ro1 for i in il) + "\n")

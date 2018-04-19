import matplotlib.pyplot as plt
import numpy as np


def natural_wavelength(E, I, delta_f, W_sub):
    """Returns the natural wavelength for

    JIP 

    :param E: Young's Modulus []
    :param I: Second moment of area []
    :param delta_f: 
    :W_sub: Submerged pipe weight [kg/m^3]
    """
    return (72 * E * I * delta_f / W_sub) ** (1 / 4)


def foundation_profile(x, delta_f, L_o):
    """
    
    """
    return delta_f * (x / L_o) ** 3 * (4 - 3 * x / L_o)


def plot_wavelength(xs, w_fs):
    fig, ax = plt.subplots()
    ax.plot(xs, w_fs, marker="o")
    ax.set_title(f"Foundation Profile, L_o = {L_o:.2f} m")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("Foundation Profile [m]")
    ax.grid()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.savefig(f"outputs/foundation_profile.png")


if __name__ == "__main__":
    E = 2.07e11
    I = 1.689e-05
    delta_f = 0.5
    W_sub = 19.7084

    L_o = natural_wavelength(E, I, delta_f, W_sub)
    print(f"L_o: {L_o:.3f} m")

    xs = np.arange(L_o)
    w_fs = [foundation_profile(x, delta_f, L_o) for x in xs]

    plot_wavelength(xs, w_fs)

    print(xs)

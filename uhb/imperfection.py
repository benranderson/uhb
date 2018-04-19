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


def plot_wavelength(xs, w_fs, L_o):
    fig, ax = plt.subplots()
    ax.plot(xs, w_fs, marker="o")
    ax.set_title(f"Foundation Profile, L_o = {L_o:.2f} m")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("Foundation Profile [m]")
    ax.grid()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.savefig("outputs/imperfections/foundation_profile.png")


def write_results(profile, delta_f):
    with open(
        f"outputs/imperfections/foundation_profile_{delta_f:.1f}m.txt", "w"
    ) as outfile:
        for x in profile[::-1]:
            outfile.write(f"{x[0]:.1f}, {x[1]:.4f}\n")


def main(element_length, pipe):
    E = pipe["E"]
    I = pipe["I"]
    W_sub = pipe["W_sub"]

    print("delta_f [m]: L_o [m]")

    for delta_f in np.arange(0.1, 0.6, 0.1):

        L_o = natural_wavelength(E, I, delta_f, W_sub)

        print(f"{delta_f:.1f}: {L_o:.3f}")

        xs = np.arange(0, L_o, element_length)
        w_fs = [foundation_profile(x, delta_f, L_o) for x in xs]

        profile = np.stack((xs, w_fs), axis=-1)

        plot_wavelength(xs, w_fs, L_o)

        write_results(profile, delta_f)


if __name__ == "__main__":
    pipe = {"E": 2.07e11, "I": 1.689e-05, "W_sub": 19.7084}

    main(0.3, pipe)

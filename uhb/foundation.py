import matplotlib.pyplot as plt
import numpy as np


def natural_wavelength(gamma_factor, E, I, delta_f, W_sub):
    """Return the factored natural wavelength [m] i.e. the distance from prop to
    touchdown - JIP. 

    :param float E: Young's Modulus [Pa]
    :param float I: Second moment of area [m^4]
    :param float delta_f: Imperfection height [m]
    :param W_sub float: Submerged pipe weight [kg/m^3]
    """
    return gamma_factor * (72 * E * I * delta_f / W_sub) ** (1 / 4)


def foundation_profile(x, delta_f, L_o):
    """Return the idealised imperfection profile [m] - JIP.

    :param float x: Distance along profile [m]
    :param float delta_f: Imperfection height [m]
    :param float L_o: Natural wavelength [m]
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
    gamma_factor = pipe["gamma_factor"]

    print("delta_f [m]: L_o [m]")

    for delta_f in np.arange(0.1, 0.6, 0.1):

        L_o = natural_wavelength(gamma_factor, E, I, delta_f, W_sub)

        print(f"{delta_f:.1f}: {L_o:.3f}")

        xs = np.arange(0, L_o, element_length)
        w_fs = [foundation_profile(x, delta_f, L_o) for x in xs]

        profile = np.stack((xs, w_fs), axis=-1)

        plot_wavelength(xs, w_fs, L_o)

        write_results(profile, delta_f)


if __name__ == "__main__":
    pipe = {"E": 2.07e11, "I": 1.6895e-05, "W_sub": 193.34, "gamma_factor": 1}

    main(0.3, pipe)

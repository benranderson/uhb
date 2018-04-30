import click
import json
import numpy as np

import uhb.general as general
from uhb.analytical import run_analytical_calc
from uhb.soil import generate_soil_springs, plot_soil_springs
from uhb.ramberg import nonlinear_rc
import uhb.foundation as f


@click.group()
@click.pass_context
def main(data):
    with open("data.json", "r") as input_file:
        data.obj = json.load(input_file)


@main.command()
@click.pass_context
def anal(data):
    """ Calculate analytical solution for the required soil cover height.
    """
    results = run_analytical_calc(data.obj)
    click.secho(f"Effective Axial Force [N]: {results['EAF']}", fg="green")
    click.secho(f"Pipeline Submerged Weight [N/m]: {results['w_o']}", fg="green")
    click.secho(f"Required Download for Stability [N]: {results['w']}", fg="green")
    click.secho(f"Soil Required Uplift Resistance [N/m]: {results['q']}", fg="green")
    click.secho(f"Required Soil Cover Height [m]: {results['H']}", fg="green")


@main.command()
@click.pass_context
@click.argument("cover_height", type=float)
@click.option(
    "--uplift-model",
    "-um",
    type=click.Choice(["asce", "f114", "f110", "otc"]),
    default="asce",
)
@click.option("--bearing-model", "-bm", type=click.Choice(["asce"]), default="asce")
@click.option("--axial-model", "-am", type=click.Choice(["asce"]), default="asce")
@click.option("--lateral-model", "-lm", type=click.Choice(["asce"]), default="asce")
@click.option("--plot", "-p", is_flag=True)
def soil(
    data, cover_height, uplift_model, bearing_model, axial_model, lateral_model, plot
):
    """ Calculate soil springs.
    """

    models = {
        "uplift": uplift_model,
        "bearing": bearing_model,
        "axial": axial_model,
        "lateral": lateral_model,
    }

    print(f"TITLE,UHB Cover Height {1000*cover_height:.0f}mm")
    print("BY, PyUHB")
    print("REF,---")
    print(
        f"DESC, vertical uplift: {uplift_model}, vertical bearing: {bearing_model}, axial: {axial_model}, lateral: {lateral_model}"
    )

    rcs = generate_soil_springs(data.obj, cover_height, models)

    for rc in rcs:
        print(f"RC, {rc}", end="")
        for delta, force in zip(rcs[rc]["deltas"], rcs[rc]["forces"]):
            print(f", {delta:.6f}, {force:.6f}", end="")
        print("\r")

    if print:
        pass


@main.command()
@click.pass_context
@click.argument("imperfection_height", type=float)
@click.option("--gamma-factor", "-gf", default=1, type=float, help="wavelength factor")
@click.option("--el-length", "-el", default=1, type=float, help="element length")
@click.option("--plot", "-p", is_flag=True)
def foundation(data, imperfection_height, gamma_factor, el_length, plot):
    """ (todo) Determine natural wavelength and generate foundation profiles.
    """
    E, D, t, t_coat = data.obj["E"], data.obj["D"], data.obj["t"], data.obj["t_coat"]
    rho_p, rho_coat, rho_cont = data.obj["rho_p"], data.obj["rho_coat"], data.obj[
        "rho_cont"
    ]
    rho_sw, g = data.obj["rho_sw"], data.obj["g"]
    I = general.second_moment_of_area(D, t)
    W_sub = general.submerged_weight(D, t, t_coat, rho_p, rho_coat, rho_cont, rho_sw, g)
    L_o = f.natural_wavelength(gamma_factor, E, I, imperfection_height, W_sub)
    print(f"Natural wavelength [m]: {L_o}")

    if el_length:
        xs = np.arange(L_o, 0, -el_length)
        w_fs = [f.foundation_profile(x, imperfection_height, L_o) for x in xs]
        profile = np.stack((xs, w_fs), axis=-1)

        for x in profile:
            print(f"{x[0]:.2f}, {x[1]:.4f}")

    # if plot:
        f.plot_wavelength(xs, w_fs, L_o)


@main.command()
@click.pass_context
@click.option("--plot", "-p", is_flag=True)
def ramberg(data, plot):
    """ Calculate non-linear material model.
    """
    print(nonlinear_rc(data.obj))

    if plot:
        print("plotting")


@main.command()
@click.pass_context
def integrity(data):
    """ Integrity checks.
    """
    print("Integrity checks")


if __name__ == "__main__":
    main()

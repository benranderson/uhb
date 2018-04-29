import click
import json

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
    print(f"Effective Axial Force [N]: {results['EAF']}")
    print(f"Pipeline Submerged Weight [N/m]: {results['w_o']}")
    print(f"Required Download for Stability [N]: {results['w']}")
    print(f"Soil Required Uplift Resistance [N/m]: {results['q']}")
    print(f"Required Soil Cover Height [m]: {results['H']}")


@main.command()
@click.pass_context
@click.argument("cover_height", type=float)
@click.option("--model", "-m", help="soil model")
@click.option("--plot", "-p", is_flag=True)
def soil(data, cover_height, model, plot):
    """ Calculate soil springs.
    """
    print(f"TITLE,UHB Cover Height {1000*cover_height:.0f}mm")
    print("BY, PyUHB")
    print("REF,---")
    print("DESC, Generated Model")
    rcs = generate_soil_springs(data.obj, cover_height)
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
@click.option("--gf", default=1, type=float, help="wavelength factor")
@click.option("--plot", "-p", is_flag=True)
def foundation(data, imperfection_height, gf, plot):
    """ (todo) Determine natural wavelength and generate foundation profiles.
    """
    E, D, t = data.obj["E"], data.obj["D"], data.obj["t"]
    rho_p, rho_sw, g = data.obj["rho_p"], data.obj["rho_sw"], data.obj["g"]
    I = general.second_moment_of_area(D, t)
    W_sub = general.submerged_weight(D, t, rho_p, rho_sw, g)
    L_o = f.natural_wavelength(gf, E, I, imperfection_height, W_sub)
    print(f"Natural wavelength [m]: {L_o}")

    if plot:
        print("plotting")


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

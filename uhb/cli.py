import os
import click
import json
from collections import namedtuple

from uhb import analytical as a, psi as p, ramberg as r


# import util.psi as s
# import uhb.analytical as analytical

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def convert(dictionary):
    """Convert a dictionary to a named tuple."""
    return namedtuple('Data', dictionary.keys())(**dictionary)


@click.group()
@click.pass_context
def main(data):
    with open("data.json", "r") as input_file:
        input_dict = json.load(input_file)
        data.obj = convert(input_dict)


@main.command()
def test():
    """Run the unit tests."""
    import pytest
    pytest.main([TEST_PATH])


@main.command()
@click.pass_context
def anal(data):
    """ Calculate analytical solution for the required soil cover height.
    """
    results = a.run_analytical_calc(data.obj)
    click.secho("Effective Axial Force [N]:")
    click.secho(f"{results.EAF}", fg="green")
    click.secho(f"Pipeline Submerged Weight [N/m]:")
    click.secho(f"{results.w_o}", fg="green")
    click.secho(f"Required Download for Stability [N]:")
    click.secho(f"{results.w}", fg="green")
    click.secho(f"Soil Required Uplift Resistance [N/m]:")
    click.secho(f"{results.q}", fg="green")
    click.secho(f"Required Soil Cover Height [m]:")
    click.secho(f"{results.H}", fg="green")


@main.command()
@click.pass_context
@click.argument("cover_height", type=float)
@click.option(
    "--uplift-model", "-um",
    type=click.Choice(["asce", "f114", "f110", "otc"]),
    default="asce",
)
@click.option("--bearing-model", "-bm", type=click.Choice(["asce"]), default="asce")
@click.option("--axial-model", "-am", type=click.Choice(["asce"]), default="asce")
@click.option("--lateral-model", "-lm", type=click.Choice(["asce"]), default="asce")
def soils(
    data, cover_height, uplift_model, bearing_model, axial_model, lateral_model
):
    """ Calculate soil springs.
    """

    uplift_spring = p.gen_uplift_spring(data.obj, cover_height, uplift_model)
    bearing_spring = p.gen_bearing_spring(
        data.obj, cover_height, bearing_model)
    axial_spring = p.gen_axial_spring(data.obj, cover_height, axial_model)
    lateral_spring = p.gen_lateral_spring(
        data.obj, cover_height, lateral_model)

    click.secho("Soil Springs:", fg="yellow")
    click.secho(f"Uplift | {uplift_model}:\n{uplift_spring}", fg="green")
    click.secho(f"Bearing | {bearing_model}:\n{bearing_spring}", fg="green")
    click.secho(f"Axial | {axial_model}:\n{axial_spring}", fg="green")
    click.secho(f"Lateral | {lateral_model}:\n{lateral_spring}", fg="green")


@main.command()
@click.pass_context
def nonlinear(data):
    """Print non-linear material model.
    """
    rcs = r.nonlinear_rc(data.obj)
    click.secho(f"{rcs}", fg="green")

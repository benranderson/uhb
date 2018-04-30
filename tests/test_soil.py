"""Tests for soil module."""

import pytest
from . import tol_check

from uhb import soil

test_inputs = [
    {
        "D_o": 0.508,
        "gamma": 8000,
        "c": 0,
        "h": 4.725,
        "psi": 35,
        "soil_type": "dense sand",
        "f": 0.67,
    },
    {
        "D_o": 0.1731,
        "gamma": 18000,
        "c": 0,
        "h": 1,
        "psi": 32,
        "soil_type": "dense sand",
        "f": 0.6,
    },
]


def test_soil_weight():
    assert tol_check(soil.calculate_soil_weight(100, 100, 1), 10000)


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 4.979), (test_inputs[1], 1.087)]
)
def test_burial_depth_to_pipe_centerline(inputs, expected):
    assert tol_check(
        soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"]), expected
    )


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 7.796), (test_inputs[1], 4.565)]
)
def test_Nqv(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(soil.Nqv(inputs["psi"], H, inputs["D_o"]), expected)


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 46.128), (test_inputs[1], 35.493)]
)
def test_Nc(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(soil.Nc(inputs["psi"], H, inputs["D_o"]), expected)


@pytest.mark.parametrize("psi, expected", [(35, 33.296), (32, 23.177)])
def test_Nq(psi, expected):
    assert tol_check(soil.Nq(psi), expected)


@pytest.mark.parametrize("psi, expected", [(35, 44.701), (32, 26.05)])
def test_Ngamma(psi, expected):
    assert tol_check(soil.Ngamma(psi), expected)


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 19667), (test_inputs[1], 2722)]
)
def test_axial_resistance_asce(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(
        soil.axial_resistance_asce(
            inputs["D_o"], H, inputs["c"], inputs["f"], inputs["psi"], inputs["gamma"]
        ),
        expected,
    )


@pytest.mark.parametrize(
    "soil_type, expected", [("dense sand", 0.003), ("loose sand", 0.005)]
)
def test_axial_delta_asce(soil_type, expected):
    assert tol_check(soil.axial_delta_asce(soil_type), expected)


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 368876), (test_inputs[1], 40553)]
)
def test_lateral_resistance_asce(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(
        soil.lateral_resistance_asce(
            inputs["c"], H, inputs["D_o"], inputs["psi"], inputs["gamma"]
        ),
        expected,
    )


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 0.0508), (test_inputs[1], 0.01731)]
)
def test_lateral_delta_asce(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(soil.lateral_delta_asce(H, inputs["D_o"]), expected)


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 157757), (test_inputs[1], 15455)]
)
def test_uplift_resistance_asce(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(
        soil.uplift_resistance_asce(
            inputs["psi"], inputs["c"], inputs["D_o"], inputs["gamma"], H
        ),
        expected,
    )


@pytest.mark.parametrize(
    "inputs, expected", [(test_inputs[0], 0.04979), (test_inputs[1], 0.01087)]
)
def test_uplift_delta_asce(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(
        soil.uplift_delta_asce(inputs["soil_type"], H, inputs["D_o"]), expected
    )


@pytest.mark.parametrize("inputs, expected", [(test_inputs[1], 89413)])
def test_bearing_resistance_asce(inputs, expected):
    H = soil.burial_depth_to_pipe_centreline(inputs["D_o"], inputs["h"])
    assert tol_check(
        soil.bearing_resistance_asce(
            inputs["psi"], inputs["c"], inputs["D_o"], inputs["gamma"], H, 1025
        ),
        expected,
    )


@pytest.mark.parametrize(
    "soil_type, D, expected", [("sand", 100, 10), ("clay", 100, 20)]
)
def test_bearing_delta_asce(soil_type, D, expected):
    assert tol_check(soil.bearing_delta_asce(soil_type, D), expected)


def test_bearing_delta_asce_unknown_soil():
    with pytest.raises(ValueError):
        soil.bearing_delta_asce("none", 100)

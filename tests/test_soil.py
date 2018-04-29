"""Tests for soil module."""

import pytest
from . import tol_check

from uhb import soil

test_inputs = {
    "D_o": 0.508,
    "gamma": 8000,
    "c": 0,
    "h": 4.725,
    "psi": 35,
    "soil_type": "dense sand",
    "f": 0.67,
}


def test_burial_depth_to_pipe_centerline():
    assert tol_check(
        soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"]),
        4.979,
    )


def test_Nqv():
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])
    assert tol_check(soil.Nqv(test_inputs["psi"], H, test_inputs["D_o"]), 7.796)


def test_Nc():
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])
    assert tol_check(soil.Nc(test_inputs["psi"], H, test_inputs["D_o"]), 46.128)


def test_Nq():
    assert tol_check(soil.Nq(test_inputs["psi"]), 33.296)


def test_Ngamma():
    assert tol_check(soil.Ngamma(test_inputs["psi"]), 44.701)


def test_Tu():
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])
    assert tol_check(
        soil.Tu(
            test_inputs["D_o"],
            H,
            test_inputs["c"],
            test_inputs["f"],
            test_inputs["psi"],
            test_inputs["gamma"],
        ),
        19667,
    )


@pytest.mark.parametrize(
    "soil_type, expected", [("dense sand", 0.003), ("loose sand", 0.005)]
)
def test_delta_t(soil_type, expected):
    assert tol_check(soil.delta_t(soil_type), expected)


def test_Pu():
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])
    assert tol_check(
        soil.Pu(
            test_inputs["c"],
            H,
            test_inputs["D_o"],
            test_inputs["psi"],
            test_inputs["gamma"],
        ),
        368876,
    )


@pytest.mark.parametrize(
    "h, expected", [(4.725, 0.0508), (4.725, 0.0508)]
)
def test_delta_p(h, expected):
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])    
    assert tol_check(soil.delta_p(H, test_inputs["D_o"]), expected)


def test_Qu():
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])
    assert tol_check(
        soil.Qu(
            test_inputs["psi"],
            test_inputs["c"],
            test_inputs["D_o"],
            test_inputs["gamma"],
            H,
        ),
        157757,
    )


@pytest.mark.parametrize(
    "soil_type, expected", [("loose sand", 0.04979), ("dense sand", 0.04979)]
)
def test_delta_qu(soil_type, expected):
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])    
    assert tol_check(soil.delta_qu(soil_type, H, test_inputs["D_o"]), expected)


def test_Qd():
    H = soil.burial_depth_to_pipe_centreline(test_inputs["D_o"], test_inputs["h"])
    assert tol_check(
        soil.Qd(
            test_inputs["psi"],
            test_inputs["c"],
            test_inputs["D_o"],
            test_inputs["gamma"],
            H,
        ),
        776461,
    )


@pytest.mark.parametrize(
    "soil_type, expected", [("loose sand", 0.0508), ("stiff clay", 0.1016)]
)
def test_delta_qd(soil_type, expected):
    assert tol_check(soil.delta_qd(soil_type, test_inputs["D_o"]), expected)

# @pytest.mark.parametrize("H, expected", [(0.5, 1557.9), (1, 3115.8)])
# def test_soil_weight(H, expected):
#     assert tol_check(
#         soil.soil_weight(test_inputs["gamma"], test_inputs["D_o"], H), expected
#     )

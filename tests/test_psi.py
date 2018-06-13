"""Tests for pipe-soil interaction module."""

import pytest

from uhb import psi


@pytest.fixture(params=[
    {
        "D_o": 0.508,
        "gamma": 8000,
        "c": 0,
        "h": 4.725,
        "psi_s": 35,
        "soil_type": "dense sand",
        "f": 0.67,
        "H": 4.979,
        "Nqv": 7.796,
        "Nch": 0,
        "Nqh": 18.23,
        "Nc": 46.128,
        "Nq": 33.296,
        "Ngamma": 44.701,
        "Tu": 19667,
        "delta_p": 0.0508,
        "Pu": 368876,
        "delta_qu": 0.04979,
        "Qu": 157757,
        "Qd": 778158,
    },
    {
        "D_o": 0.1731,
        "gamma": 18000,
        "c": 0,
        "h": 1,
        "psi_s": 32,
        "soil_type": "dense sand",
        "f": 0.6,
        "H": 1.087,
        "Nqv": 4.565,
        "Nch": 0,
        "Nqh": 11.979,
        "Nc": 35.493,
        "Nq": 23.177,
        "Ngamma": 26.05,
        "Tu": 2722,
        "delta_p": 0.01731,
        "Pu": 40553,
        "delta_qu": 0.01087,
        "Qu": 15455,
        "Qd": 89413,
    },
])
def gen_test_data(request):
    """ Generate test data. """
    return request.param


def test_calculate_soil_weight():
    assert pytest.approx(psi.calculate_soil_weight(100, 100, 1)) == 10000


def test_depth_to_centre(gen_test_data):
    assert pytest.approx(
        psi.depth_to_centre(gen_test_data["D_o"], gen_test_data["h"]),
        0.001) == gen_test_data["H"]


def test_Nch(gen_test_data):
    H = psi.depth_to_centre(gen_test_data["D_o"], gen_test_data["h"])
    assert pytest.approx(
        psi.Nch(0, H, gen_test_data["D_o"]),
        0.001) == gen_test_data["Nch"]


def test_Nqh(gen_test_data):
    H = psi.depth_to_centre(gen_test_data["D_o"], gen_test_data["h"])
    assert pytest.approx(
        psi.Nqh(gen_test_data["psi_s"], H, gen_test_data["D_o"]),
        0.001) == gen_test_data["Nqh"]


@pytest.mark.parametrize(
    "psi_s, expected", [
        (0, 0),
        (10, 2.8090),
        (60, 21.0084),
    ]
)
def test_Nqh_edge_cases(psi_s, expected):
    assert pytest.approx(psi.Nqh(psi_s, 1, 1), 0.001) == expected


@pytest.mark.parametrize(
    "c, H, D, expected", [
        (0, 1, 1, 0),
        (1, 2, 1, 4),
        (1, 50, 1, 10),
    ]
)
def test_Ncv(c, H, D, expected):
    assert pytest.approx(psi.Ncv(c, H, D)) == expected


def test_Nqv(gen_test_data):
    assert pytest.approx(
        psi.Nqv(gen_test_data["psi_s"], gen_test_data["H"], gen_test_data["D_o"]),
        0.001) == gen_test_data["Nqv"]


def test_Nqv_zero():
    assert pytest.approx(psi.Nqv(0, 1, 1)) == 0


def test_Nc(gen_test_data):
    assert pytest.approx(
        psi.Nc(gen_test_data["psi_s"], gen_test_data["H"], gen_test_data["D_o"]),
        0.001) == gen_test_data["Nc"]


def test_Nq(gen_test_data):
    assert pytest.approx(psi.Nq(gen_test_data["psi_s"]), 0.001) == gen_test_data["Nq"]


def test_Ngamma(gen_test_data):
    assert pytest.approx(psi.Ngamma(gen_test_data["psi_s"]),
                         0.001) == gen_test_data["Ngamma"]


@pytest.mark.parametrize(
    "soil_type, expected", [("dense sand", 0.003), ("loose sand", 0.005)]
)
def test_delta_t(soil_type, expected):
    assert pytest.approx(psi.delta_t(soil_type)) == expected


def test_Tu(gen_test_data):
    assert pytest.approx(
        psi.Tu(gen_test_data["D_o"], gen_test_data["H"], gen_test_data["c"], gen_test_data["f"],
               gen_test_data["psi_s"], gen_test_data["gamma"]),
        0.001) == gen_test_data["Tu"]


def test_delta_p(gen_test_data):
    assert pytest.approx(
        psi.delta_p(gen_test_data["H"], gen_test_data["D_o"])
    ) == gen_test_data["delta_p"]


def test_Pu(gen_test_data):
    assert pytest.approx(
        psi.Pu(gen_test_data["c"], gen_test_data["H"], gen_test_data["D_o"],
               gen_test_data["psi_s"], gen_test_data["gamma"]),
        0.001) == gen_test_data["Pu"]


def test_delta_qu(gen_test_data):
    assert pytest.approx(psi.delta_qu(
        gen_test_data["soil_type"], gen_test_data["H"], gen_test_data["D_o"]),
        0.001) == gen_test_data["delta_qu"]


@pytest.mark.parametrize(
    "soil_type, H, D, expected", [
        ("sand", 1, 1, 0.01),
        ("clay", 1, 1, 0.1),
    ]
)
def test_delta_qu_others(soil_type, H, D, expected):
    assert pytest.approx(psi.delta_qu(soil_type, H, D)) == expected


def test_delta_qu_unknown_soil():
    with pytest.raises(ValueError):
        psi.delta_qu("unknown", 1, 1)


def test_Qu(gen_test_data):
    assert pytest.approx(psi.Qu(
        gen_test_data["psi_s"], gen_test_data["c"], gen_test_data["D_o"],
        gen_test_data["gamma"], gen_test_data["H"]),
        0.001) == gen_test_data["Qu"]


@pytest.mark.parametrize(
    "soil_type, D, expected", [
        ("dense sand", 0.508, 0.0508),
        ("stiff clay", 0.2, 0.04)
    ]
)
def test_delta_qd(soil_type, D, expected):
    assert pytest.approx(psi.delta_qd(soil_type, D)) == expected


def test_delta_qd_unknown_soil():
    with pytest.raises(ValueError):
        psi.delta_qd("unknown", 100)


def test_Qd(gen_test_data):
    assert pytest.approx(
        psi.Qd(gen_test_data["psi_s"], gen_test_data["c"], gen_test_data["D_o"],
               gen_test_data["gamma"], gen_test_data["H"], 1025),
        0.001) == gen_test_data["Qd"]


# @pytest.mark.parametrize(
#     "inputs, expected", [
#         (test_inputs[0], (0.003, 19667)),
#         (test_inputs[1], (0.003, 2722)),
#     ]
# )
# def test_gen_axial_spring(inputs, expected):
#     assert pytest.approx(psi.gen_axial_spring(inputs, 1), 0.001) == expected


# def test_gen_axial_spring_unknown_soil():
#     with pytest.raises(ValueError):
#         psi.gen_axial_spring(test_inputs[0], "none")

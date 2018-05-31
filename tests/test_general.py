"""Tests for general module."""

import pytest
from . import tol_check

import general


@pytest.fixture(params=[
    {
        "D": 0.1683,
        "t": 0.011,
        "t_coat": 0.0024,
        "D_o": 0.1731,
        "A_s": 0.005436,
        "A_c": 0.001287,
        "A_i": 0.016810,
        "A_t": 0.023533,
        "I": 1.689e-5,
        "EAF": 786019,
        "W_s": 193.34,
    }
])
def gen_test_data(request):
    """ Generate test data. """
    return request.param


def test_total_outside_diameter(gen_test_data):
    assert pytest.approx(general.total_outside_diameter(
        gen_test_data["D"], gen_test_data["t_coat"])) == gen_test_data["D_o"]


def test_area_of_steel(gen_test_data):
    assert pytest.approx(general.area_of_steel(
        gen_test_data["D"], gen_test_data["t"]), 0.001) == gen_test_data["A_s"]


def test_area_of_coating(gen_test_data):
    assert pytest.approx(general.area_of_coating(
        gen_test_data["D"], gen_test_data["t_coat"]), 0.001) == gen_test_data["A_c"]


def test_internal_area(gen_test_data):
    assert pytest.approx(general.internal_area(
        gen_test_data["D"], gen_test_data["t"]), 0.001) == gen_test_data["A_i"]


def test_total_area(gen_test_data):
    assert pytest.approx(general.total_area(0.1731), 0.001) == gen_test_data["A_t"]


def test_second_moment_of_area(gen_test_data):
    assert pytest.approx(general.second_moment_of_area(
        gen_test_data["D"], gen_test_data["t"]), 0.001) == gen_test_data["I"]


def test_effective_axial_force(gen_test_data):
    A_i = general.internal_area(gen_test_data["D"], gen_test_data["t"])
    A_s = general.area_of_steel(gen_test_data["D"], gen_test_data["t"])
    assert pytest.approx(abs(general.effective_axial_force(
        0, 1.9e7, A_i, 0.3, A_s, 207e9, 11.7e-6, 50))) == gen_test_data["EAF"]


def test_submerged_weight(gen_test_data):
    assert pytest.approx(general.submerged_weight(
        gen_test_data["D"], gen_test_data["t"], gen_test_data["t_coat"], 7850, 900, 0, 1025,
        9.81)) == gen_test_data["W_s"]
